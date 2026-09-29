#!/usr/bin/env python3
"""Run checked, sequential Zyte browserHtml captures from recipe JSON files."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

try:
    from offline_assets import capture as capture_offline_assets
except ImportError:  # Running as ``python scripts/zyte_capture.py`` from any cwd.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from offline_assets import capture as capture_offline_assets


API_URL = "https://api.zyte.com/v1/extract"
SECRET_QUERY_KEYS = re.compile(r"(?:token|secret|signature|sig|password|passwd|api[_-]?key|auth|session|credential)", re.I)
WALL_MARKERS = re.compile(
    r"(?:verify\s+(?:you\s+are\s+)?human|javascript\s+is\s+disabled|access\s+denied|unusual\s+traffic|robot\s+check|captcha(?:\s+challenge)?|cloudflare\s+ray\s+id|troppo\s+in\s+fretta|te\s+snel\s+voor\s+ons|demasiado\s+r[aá]pido)",
    re.I,
)


def _redact_url(value: str) -> str:
    try:
        parts = urlsplit(value)
        if not any(SECRET_QUERY_KEYS.search(key) for key, _ in parse_qsl(parts.query, keep_blank_values=True)):
            return value
        query = []
        for key, item in parse_qsl(parts.query, keep_blank_values=True):
            query.append((key, "[REDACTED_SECRET]" if SECRET_QUERY_KEYS.search(key) else item))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))
    except ValueError:
        return "[INVALID_URL]"


def _redact(value: object, key: str = "") -> object:
    if isinstance(value, dict):
        return {name: _redact(item, name) for name, item in value.items()}
    if isinstance(value, list):
        return [_redact(item, key) for item in value]
    if isinstance(value, str) and (key.lower().endswith("url") or key.lower() in {"url", "uri"}):
        return _redact_url(value)
    return value


def _load_env(root: Path) -> str | None:
    value = os.environ.get("ZYTE_API_KEY")
    if value:
        return value
    env_paths = [root / ".env", root.parent.parent / ".env"]
    for env_path in env_paths:
        try:
            for raw in env_path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, item = line.split("=", 1)
                if name.strip() != "ZYTE_API_KEY":
                    continue
                item = item.strip()
                if len(item) >= 2 and item[0] == item[-1] and item[0] in {"'", '"'}:
                    item = item[1:-1]
                return item
        except OSError:
            pass
    return None


def _prepare_action(path: Path) -> dict[str, str] | None:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if len(source.encode("utf-8")) > 6000:
        raise ValueError(f"{path} exceeds the 6000-byte evaluate-script limit")
    return {"action": "evaluate", "source": source} if source.strip() else None


def _recipe_request(recipe: dict[str, object], root: Path) -> dict[str, object]:
    raw = recipe.get("request") if isinstance(recipe.get("request"), dict) else recipe
    request = copy.deepcopy(raw)
    assert isinstance(request, dict)
    url = request.get("url") or recipe.get("url")
    if not isinstance(url, str) or not url.strip():
        raise ValueError("recipe request.url is required")
    request["url"] = url
    request.setdefault("browserHtml", True)
    request.setdefault("screenshot", True)
    request.setdefault("screenshotOptions", {"fullPage": True, "format": "jpeg"})
    actions = request.get("actions", [])
    if not isinstance(actions, list):
        raise ValueError("recipe request.actions must be an array")
    shared_prepare = _prepare_action(root / "capture" / "prepare.js")
    prepare_source = shared_prepare.get("source") if shared_prepare else None
    has_prepare = any(isinstance(action, dict) and action.get("action") == "evaluate" and action.get("source") == prepare_source for action in actions)
    request["actions"] = actions + ([shared_prepare] if shared_prepare and not has_prepare else [])
    return request


def _load_recipe(path: Path, root: Path) -> tuple[dict[str, object], dict[str, object]]:
    try:
        recipe = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read recipe {path}: {exc}") from exc
    if not isinstance(recipe, dict):
        raise ValueError(f"recipe must be an object: {path}")
    request = _recipe_request(recipe, root)
    return recipe, request


def _recipe_files(root: Path, retailer: str | None, page_type: str | None, all_pages: bool) -> list[Path]:
    recipe_root = root / "capture" / "recipes"
    if all_pages:
        paths = sorted(recipe_root.glob("*/*.json"))
        if retailer:
            paths = [path for path in paths if path.parent.name == retailer]
        if page_type:
            paths = [path for path in paths if path.stem == page_type]
        return paths
    if not retailer or not page_type:
        raise ValueError("--retailer and --page-type are required unless --all is used")
    return [recipe_root / retailer / f"{page_type}.json"]


def _action_errors(actions: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(actions, list):
        return ["response.actions is not an array"]
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            continue
        status = str(action.get("status", "")).lower()
        error = action.get("error") or action.get("message")
        if status in {"failed", "error", "timeout", "timedout"} or error:
            errors.append(f"action[{index}] {status or 'error'}: {error or 'unspecified'}")
    return errors


def _visible_text(html: str) -> str:
    text = re.sub(r"(?is)<(script|style|template)\b.*?</\1\s*>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _title(html: str) -> str:
    match = re.search(r"(?is)<title\b[^>]*>(.*?)</title\s*>", html)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", match.group(1))).strip() if match else ""


def _evidence_errors(recipe: dict[str, object], request: dict[str, object], response: dict[str, object], html: str) -> list[str]:
    errors: list[str] = []
    evidence = recipe.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}
    final_url = str(response.get("url") or "")
    title = _title(html)
    visible = _visible_text(html)
    required_text = evidence.get("required_text", [])
    if isinstance(required_text, str):
        required_text = [required_text]
    if isinstance(required_text, list):
        for value in required_text:
            if isinstance(value, str) and value and value.lower() not in visible.lower():
                errors.append(f"required text missing: {value[:120]}")
    required_any = evidence.get("required_any", [])
    if isinstance(required_any, list) and required_any and not any(isinstance(value, str) and value.lower() in visible.lower() for value in required_any):
        errors.append("none of evidence.required_any was found")
    title_contains = evidence.get("title_contains", [])
    if isinstance(title_contains, str):
        title_contains = [title_contains]
    if isinstance(title_contains, list) and title_contains and not any(isinstance(value, str) and value.lower() in title.lower() for value in title_contains):
        errors.append("title does not match evidence.title_contains")
    url_contains = evidence.get("url_contains", [])
    if isinstance(url_contains, str):
        url_contains = [url_contains]
    if isinstance(url_contains, list) and url_contains and not all(isinstance(value, str) and value in final_url for value in url_contains):
        errors.append("final URL does not match evidence.url_contains")
    for value in evidence.get("forbidden_text", []) if isinstance(evidence.get("forbidden_text", []), list) else []:
        if isinstance(value, str) and value.lower() in visible.lower():
            errors.append(f"forbidden text found: {value[:120]}")

    if not evidence.get("allow_wall_markers") and WALL_MARKERS.search((title + " " + visible)[:20000]):
        errors.append("captcha or access wall marker detected")
    requested = str(recipe.get("target_url") or request.get("url") or "")
    requested_parts, final_parts = urlsplit(requested), urlsplit(final_url)
    if requested_parts.netloc and final_parts.netloc and requested_parts.netloc != final_parts.netloc:
        errors.append("final URL host differs from requested URL")
    if requested_parts.path not in {"", "/"} and final_parts.path in {"", "/"} and not evidence.get("allow_root_redirect"):
        errors.append("requested page redirected to site root")
    if not html.strip():
        errors.append("browserHtml is empty")
    return errors


def _capture_state(html: str) -> dict[str, object]:
    """Return the structured evidence emitted by the browser actions."""
    match = re.search(r"(?is)<script[^>]+id=[\"']lg-capture-state[\"'][^>]*>(.*?)</script\s*>", html)
    if not match:
        raise ValueError("lg-capture-state is missing")
    try:
        state = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError(f"lg-capture-state is invalid JSON: {exc}") from exc
    if not isinstance(state, dict):
        raise ValueError("lg-capture-state is not a JSON object")
    return state


def _capture_state_errors(html: str) -> list[str]:
    """Validate the JSON state emitted by capture/load.js when present."""
    try:
        state = _capture_state(html)
    except ValueError as exc:
        return [str(exc)]
    errors: list[str] = []
    if state.get("error"):
        errors.append(f"capture state error: {state['error']}")
    if state.get("cookieRemaining"):
        errors.append(f"cookie consent remains visible: {state['cookieRemaining']}")
    if state.get("ready") is False:
        errors.append("capture ready selector was not found")
    if state.get("requireScrollBottom") and state.get("scroll", {}).get("reachedBottom") is not True:
        errors.append("configured full-page scroll did not reach the bottom")
    if not state.get("finishedAt"):
        errors.append("capture state has no finishedAt")
    required = state.get("required", [])
    if isinstance(required, list):
        for item in required:
            if isinstance(item, dict) and item.get("present") is False:
                errors.append(f"required selector missing: {item.get('selector', '')}")
    steps = state.get("steps", [])
    if isinstance(steps, list):
        for item in steps:
            if isinstance(item, dict) and item.get("panel") and item.get("status") == "missing":
                errors.append(f"captured panel missing: {item.get('panel')}")
    return errors


def _post_json(api_key: str, request_payload: dict[str, object], timeout: float, retries: int) -> dict[str, object]:
    body = json.dumps(request_payload, ensure_ascii=False).encode("utf-8")
    auth = base64.b64encode(f"{api_key}:".encode("utf-8")).decode("ascii")
    last: Exception | None = None
    for attempt in range(1, retries + 2):
        request = Request(API_URL, data=body, headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json", "Accept": "application/json"}, method="POST")
        try:
            with urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("Zyte response is not an object")
                return payload
        except HTTPError as exc:
            last = RuntimeError(f"Zyte HTTP {exc.code}: {exc.read(4096).decode('utf-8', errors='replace')[:500]}")
            if exc.code not in {408, 429, 500, 502, 503, 504} or attempt > retries:
                break
        except (URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
            last = exc
            if attempt > retries:
                break
        time.sleep(min(0.5 * attempt, 2.0))
    assert last is not None
    raise RuntimeError(str(last))


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _record_page_error(root: Path, recipe_path: Path, error: Exception) -> None:
    retailer = recipe_path.parent.name
    page_type = recipe_path.stem
    output_dir = root / "output" / "offline" / retailer / page_type
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "error.json", {"ok": False, "retailer": retailer, "page_type": page_type, "error": str(error), "recorded_at": datetime.now(timezone.utc).isoformat()})


def _asset_source_allowed(response_path: Path, raw_path: Path) -> tuple[bool, str]:
    try:
        response = json.loads(response_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"invalid response metadata: {exc}"
    if response.get("ok") is False:
        return False, "response metadata marks capture rejected"
    status = response.get("status_code", response.get("statusCode"))
    if response.get("ok") is not True:
        if not isinstance(status, int) or not 200 <= status < 400:
            return False, f"target status is not successful: {status}"
        try:
            state_errors = _capture_state_errors(raw_path.read_text(encoding="utf-8"))
        except OSError as exc:
            return False, f"cannot read raw HTML: {exc}"
        if state_errors:
            return False, "; ".join(state_errors)
    return True, ""


def _preserve_last_good(output_dir: Path, response_path: Path, raw_path: Path) -> None:
    try:
        response = json.loads(response_path.read_text(encoding="utf-8"))
        status = response.get("status_code", response.get("statusCode"))
        valid = response.get("ok") is True or ("ok" not in response and isinstance(status, int) and 200 <= status < 400 and not _capture_state_errors(raw_path.read_text(encoding="utf-8")))
        if not valid:
            return
        target = output_dir / "last-good"
        target.mkdir(parents=True, exist_ok=True)
        for source in (response_path, raw_path, output_dir / "screenshot.jpg", output_dir / "request.json", output_dir / "capture-state.json"):
            if source.is_file():
                shutil.copyfile(source, target / source.name)
    except (OSError, json.JSONDecodeError):
        return


def _capture_one(root: Path, recipe_path: Path, *, dry_run: bool, assets: bool, force: bool, api_key: str | None, timeout: float, retries: int, asset_cache: Path | None, asset_timeout: float, asset_retries: int, max_zyte_fallback: int) -> bool:
    recipe, request = _load_recipe(recipe_path, root)
    retailer = str(recipe.get("retailer") or recipe_path.parent.name)
    page_type = str(recipe.get("page_type") or recipe_path.stem)
    output_dir = root / "output" / "offline" / retailer / page_type
    output_dir.mkdir(parents=True, exist_ok=True)
    request_path = output_dir / "request.json"
    if dry_run:
        _write_json(output_dir / "request.preview.json", _redact(request))
        print(f"DRY RUN {retailer}/{page_type} -> {_redact_url(str(request['url']))}")
        return True
    if not api_key:
        raise RuntimeError("ZYTE_API_KEY is required for a live capture")
    response_meta_path = output_dir / "response.json"
    raw_path = output_dir / "raw.html"
    request_hash = hashlib.sha256(json.dumps(request, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    if not force and response_meta_path.is_file() and raw_path.is_file():
        try:
            old = json.loads(response_meta_path.read_text(encoding="utf-8"))
            old_status = old.get("status_code", old.get("statusCode"))
            old_hash = old.get("request_sha256")
            hash_matches = old_hash == request_hash if old_hash else True
            legacy_ok = "ok" not in old and isinstance(old_status, int) and 200 <= old_status < 400 and not _capture_state_errors(raw_path.read_text(encoding="utf-8"))
            if hash_matches and (old.get("ok") is True or legacy_ok):
                if assets:
                    capture_offline_assets(raw_path, output_dir / "view", base_url=str(old.get("final_url") or old.get("url") or request["url"]), timeout=asset_timeout, retries=asset_retries, zyte_timeout=asset_timeout, zyte_retries=asset_retries, prefetch_workers=8, zyte_api_key=api_key, max_zyte_fallback=max_zyte_fallback, cache_dir=asset_cache)
                print(f"RESUME {retailer}/{page_type}")
                return True
        except (OSError, json.JSONDecodeError):
            pass

    if response_meta_path.is_file() and raw_path.is_file():
        _preserve_last_good(output_dir, response_meta_path, raw_path)

    _write_json(request_path, _redact(request))
    response = _post_json(api_key, request, timeout, retries)
    html = response.get("browserHtml")
    if not isinstance(html, str):
        error = {"ok": False, "error": "Zyte response has no browserHtml", "response_keys": sorted(response)}
        _write_json(response_meta_path, error)
        raise RuntimeError(f"{retailer}/{page_type}: Zyte response has no browserHtml")
    raw_path.write_text(html, encoding="utf-8")
    screenshot_bytes = 0
    screenshot = response.get("screenshot")
    if isinstance(screenshot, str):
        try:
            data = base64.b64decode(screenshot, validate=True)
        except (ValueError, base64.binascii.Error) as exc:
            data = b""
            screenshot_error = f"invalid screenshot encoding: {exc}"
        else:
            (output_dir / "screenshot.jpg").write_bytes(data)
            screenshot_bytes = len(data)
            screenshot_error = ""
    else:
        screenshot_error = "Zyte response has no screenshot"
    action_errors = _action_errors(response.get("actions"))
    evidence_errors = _evidence_errors(recipe, request, response, html) + _capture_state_errors(html)
    status_code = response.get("statusCode")
    if isinstance(status_code, int) and not 200 <= status_code < 400:
        evidence_errors.append(f"target status {status_code}")
    if screenshot_error:
        evidence_errors.append(screenshot_error)
    if action_errors or evidence_errors:
        detail = {"ok": False, "action_errors": action_errors, "evidence_errors": evidence_errors, "status_code": response.get("statusCode"), "url": _redact_url(str(response.get("url") or "")), "actions": response.get("actions", []), "bytes": {"raw_html": len(html.encode("utf-8")), "screenshot": screenshot_bytes}}
        _write_json(response_meta_path, _redact(detail))
        raise RuntimeError(f"{retailer}/{page_type}: capture rejected: {'; '.join(action_errors + evidence_errors)}")
    _write_json(output_dir / "capture-state.json", _capture_state(html))
    metadata = {
        "ok": True,
        "retailer": retailer,
        "page_type": page_type,
        "requested_url": _redact_url(str(recipe.get("target_url") or request["url"])),
        "entry_url": _redact_url(str(request["url"])),
        "final_url": _redact_url(str(response.get("url") or "")),
        "status_code": status_code,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "response_keys": sorted(response),
        "actions": response.get("actions", []),
        "request_sha256": request_hash,
        "bytes": {"raw_html": len(html.encode("utf-8")), "screenshot": screenshot_bytes},
    }
    _write_json(response_meta_path, _redact(metadata))
    stale_error_path = output_dir / "error.json"
    if stale_error_path.is_file():
        stale_error_path.unlink()
    if assets:
        view_dir = output_dir / "view"
        capture_offline_assets(raw_path, view_dir, base_url=str(response.get("url") or request["url"]), timeout=asset_timeout, retries=asset_retries, zyte_timeout=asset_timeout, zyte_retries=asset_retries, prefetch_workers=8, zyte_api_key=api_key, max_zyte_fallback=max_zyte_fallback, cache_dir=asset_cache)
    print(f"OK {retailer}/{page_type} html={len(html.encode('utf-8'))} screenshot={screenshot_bytes}")
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retailer")
    parser.add_argument("--page-type")
    parser.add_argument("--all", action="store_true", dest="all_pages")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--assets", action="store_true", help="build the local HTML/CSS/image/font/iframe view after capture")
    parser.add_argument("--assets-only", action="store_true", help="build views from existing raw.html files without contacting Zyte")
    parser.add_argument("--force", action="store_true", help="recapture pages with an existing successful response")
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--asset-cache-dir", type=Path)
    parser.add_argument("--asset-timeout", type=float, default=10)
    parser.add_argument("--asset-retries", type=int, default=1)
    parser.add_argument("--max-zyte-fallback", type=int, default=600)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        paths = _recipe_files(root, args.retailer, args.page_type, args.all_pages)
        if not paths:
            raise ValueError("no matching capture recipes found")
        if not args.dry_run and not args.assets_only and not _load_env(root):
            raise RuntimeError("ZYTE_API_KEY is missing (set it in the environment or .env)")
        api_key = _load_env(root)
        failures: list[str] = []
        for path in paths:
            try:
                if not path.is_file():
                    raise ValueError(f"recipe not found: {path}")
                if args.assets_only:
                    recipe, request = _load_recipe(path, root)
                    retailer = str(recipe.get("retailer") or path.parent.name)
                    page_type = str(recipe.get("page_type") or path.stem)
                    output_dir = root / "output" / "offline" / retailer / page_type
                    raw_path = output_dir / "raw.html"
                    if not raw_path.is_file():
                        raise ValueError(f"raw.html not found: {raw_path}")
                    final_url = str(request["url"])
                    response_path = output_dir / "response.json"
                    if not response_path.is_file():
                        raise ValueError(f"response.json not found: {response_path}")
                    allowed, reason = _asset_source_allowed(response_path, raw_path)
                    if not allowed:
                        raise ValueError(f"raw capture rejected for offline view: {reason}")
                    try:
                        final_url = str(json.loads(response_path.read_text(encoding="utf-8")).get("final_url") or final_url)
                    except (OSError, json.JSONDecodeError):
                        pass
                    capture_offline_assets(raw_path, output_dir / "view", base_url=final_url, timeout=args.asset_timeout, retries=args.asset_retries, zyte_timeout=args.asset_timeout, zyte_retries=args.asset_retries, prefetch_workers=8, zyte_api_key=api_key, max_zyte_fallback=args.max_zyte_fallback, cache_dir=args.asset_cache_dir)
                    print(f"ASSETS {retailer}/{page_type}")
                else:
                    _capture_one(root, path, dry_run=args.dry_run, assets=args.assets, force=args.force, api_key=api_key, timeout=args.timeout, retries=args.retries, asset_cache=args.asset_cache_dir, asset_timeout=args.asset_timeout, asset_retries=args.asset_retries, max_zyte_fallback=args.max_zyte_fallback)
            except (OSError, ValueError, RuntimeError) as exc:
                _record_page_error(root, path, exc)
                failures.append(f"{path.parent.name}/{path.stem}: {exc}")
                print(f"FAIL {path.parent.name}/{path.stem}: {exc}", file=sys.stderr)
        if failures:
            print(f"zyte capture completed with {len(failures)} failure(s)", file=sys.stderr)
            return 1
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"zyte capture failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
