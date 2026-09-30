#!/usr/bin/env python3
"""Capture every selected BCP URL into one resumable, source-linked batch."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adapt_bcp_recipe import adapt_recipe
import zyte_capture as zyte


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "population" / "source_urls.json"
RESULTS = ROOT / "results_population"
CAPTURE_FILES = ("request.json", "response.json", "raw.html", "screenshot.jpg", "capture-state.json")


def selected_records(inventory: dict[str, object], scope: str) -> list[dict[str, object]]:
    records = inventory.get("records")
    if not isinstance(records, list):
        raise ValueError("source URL inventory has no records")
    if scope == "lg-bcp":
        return [r for r in records if r.get("pageType") == "Brand Category Page" and r.get("brand") == "LG"]
    if scope == "all-bcp":
        return [r for r in records if r.get("pageType") == "Brand Category Page"]
    if scope == "all-pages":
        return [r for r in records if r.get("pageType") in {"Brand Category Page", "Brand Page"}]
    raise ValueError(f"unsupported scope: {scope}")


def page_key(record: dict[str, object]) -> str:
    return f"row-{int(record['sourceRow']):04d}-{record['retailerSlug']}"


def prepared_recipe(record: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    slug = str(record["retailerSlug"])
    page_type = "brand-category" if record["pageType"] == "Brand Category Page" else "brand"
    recipe_path = ROOT / "capture" / "recipes" / slug / f"{page_type}.json"
    base = json.loads(recipe_path.read_text(encoding="utf-8"))
    recipe = adapt_recipe(base, str(record["url"]))
    # Elgiganten competitor BCPs use editorial layouts without the #result-top
    # listing selector. One inspected Hisense page also has no H1, which must be
    # assessed as ID9 N rather than rejected as a collection failure.
    if slug == "elgiganten" and page_type == "brand-category" and str(record["brand"]).casefold() != "lg":
        for action in recipe["request"]["actions"]:
            if action.get("action") == "waitForTimeout" and float(action.get("timeout", 0)) < 5:
                action["timeout"] = 5
                break
        for action in recipe["request"]["actions"]:
            source = action.get("source", "") if isinstance(action, dict) else ""
            if isinstance(source, str) and source.startswith("window.__lgConfig = "):
                config = json.loads(source.removeprefix("window.__lgConfig = ").rstrip(";"))
                config["ready"] = "body"
                config["required"] = ["body"]
                action["source"] = "window.__lgConfig = " + json.dumps(config, ensure_ascii=False) + ";"
                recipe.setdefault("evidence", {})["template_note"] = "Editorial category layout observed without #result-top; complete scroll and brand title required"
                recipe["evidence"]["title_contains"] = [str(record["brand"])]
        # The editorial section can finish while the product grid still shows
        # loading placeholders. Wait after scrolling, before serializing DOM.
        recipe["request"]["actions"].insert(-2, {"action": "evaluate", "source":
            "(async()=>{const until=Date.now()+18000;while(Date.now()<until){"
            "if(document.querySelector('a[href*=\"/product/\"]'))return;"
            "await new Promise(r=>setTimeout(r,500));}})();"})
    if page_type == "brand-category":
        for action in recipe["request"]["actions"]:
            source = action.get("source", "") if isinstance(action, dict) else ""
            if not isinstance(source, str) or not source.startswith("window.__lgConfig = "):
                continue
            config = json.loads(source.removeprefix("window.__lgConfig = ").rstrip(";"))
            config.update(target_brand=record["brand"], target_category=record["subcategory"],
                          target_category_code=record["categoryCode"])
            action["source"] = "window.__lgConfig = " + json.dumps(config, ensure_ascii=False) + ";"
            break
        else:
            raise ValueError(f"BCP config is missing for {page_key(record)}")
    request = zyte._recipe_request(recipe, ROOT)
    for action in request.get("actions", []):
        if isinstance(action, dict) and len(str(action.get("source") or "").encode("utf-8")) > 6000:
            raise ValueError(f"evaluate action exceeds 6000 bytes for {page_key(record)}")
    return recipe, request


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def capture_page(record: dict[str, object], batch: Path, api_key: str, timeout: float, retries: int) -> str:
    key = page_key(record)
    page_type = "brand-category" if record["pageType"] == "Brand Category Page" else "brand"
    output = batch / "pages" / key / page_type
    output.mkdir(parents=True, exist_ok=True)
    recipe, request = prepared_recipe(record)
    request_hash = hashlib.sha256(json.dumps(request, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    response_path = output / "response.json"
    if response_path.is_file() and all((output / name).is_file() for name in CAPTURE_FILES):
        old = json.loads(response_path.read_text(encoding="utf-8"))
        if old.get("ok") is True and old.get("request_sha256") == request_hash:
            return "reused"
    try:
        response = zyte._post_json(api_key, request, timeout, retries)
        html = response.get("browserHtml")
        if not isinstance(html, str):
            raise ValueError("Zyte response has no browserHtml")
        screenshot = response.get("screenshot")
        if not isinstance(screenshot, str):
            raise ValueError("Zyte response has no screenshot")
        screenshot_bytes = base64.b64decode(screenshot, validate=True)
        state = zyte._capture_state(html)
        errors = zyte._action_errors(response.get("actions")) + zyte._evidence_errors(recipe, request, response, html) + zyte._capture_state_errors(html)
        code = response.get("statusCode")
        if not isinstance(code, int) or not 200 <= code < 400:
            errors.append(f"target HTTP status {code}")
        if errors:
            raise ValueError("; ".join(errors))
        write_json(output / "request.json", zyte._redact(request))
        (output / "raw.html").write_text(html, encoding="utf-8")
        (output / "screenshot.jpg").write_bytes(screenshot_bytes)
        write_json(output / "capture-state.json", state)
        write_json(response_path, {
            "ok": True, "retailer": record["retailerSlug"], "page_type": page_type,
            "source_row": record["sourceRow"], "requested_url": record["url"],
            "entry_url": request["url"], "final_url": zyte._redact_url(str(response.get("url") or "")),
            "status_code": code, "captured_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
            "request_sha256": request_hash,
            "bytes": {"raw_html": len(html.encode()), "screenshot": (output / "screenshot.jpg").stat().st_size},
        })
        return "captured"
    except Exception as exc:
        write_json(output / "capture-error.json", {"ok": False, "requested_url": record["url"], "error": str(exc),
                                                  "recorded_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat()})
        return "failed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("lg-bcp", "all-bcp", "all-pages"), required=True)
    parser.add_argument("--batch", type=Path, help="existing batch to resume, or output path for a new batch")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, help="capture at most this many uncaptured URLs in this invocation")
    parser.add_argument("--only-row", type=int, action="append", help="process only this source workbook row; repeat for several")
    parser.add_argument("--workers", type=int, default=1, help="number of concurrent Zyte requests")
    parser.add_argument("--seed-from", type=Path, help="copy already validated captures for matching workbook rows")
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--retries", type=int, default=2)
    args = parser.parse_args()
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    records = selected_records(inventory, args.scope)
    workbook = ROOT.parent.parent / str(inventory["sourceWorkbook"])
    if hashlib.sha256(workbook.read_bytes()).hexdigest() != inventory["sourceWorkbookSha256"]:
        raise ValueError("source workbook changed; rebuild the URL inventory before capturing")
    for record in records:
        prepared_recipe(record)
    print(f"scope={args.scope} URLs={len(records)} recipes=valid", flush=True)
    if args.dry_run:
        for record in records:
            print(f"{page_key(record)} {record['brand']} {record['categoryCode']} {record['url']}")
        return 0
    api_key = zyte._load_env(ROOT)
    if not api_key:
        raise RuntimeError("ZYTE_API_KEY is missing")
    batch = args.batch or RESULTS / datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y%m%dT%H%M%SKST")
    batch.mkdir(parents=True, exist_ok=True)
    manifest_path = batch / "manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("scope") != args.scope or manifest.get("sourceWorkbookSha256") != inventory["sourceWorkbookSha256"]:
            raise ValueError("existing batch scope/source differs from this invocation")
    else:
        manifest = {"scope": args.scope, "sourceWorkbook": inventory["sourceWorkbook"],
                    "sourceWorkbookSha256": inventory["sourceWorkbookSha256"],
                    "createdAt": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
                    "records": [{**record, "pageKey": page_key(record), "collectionStatus": "pending"} for record in records]}
        write_json(manifest_path, manifest)
    if args.seed_from:
        seed_batch = args.seed_from.resolve()
        seed_manifest = json.loads((seed_batch / "manifest.json").read_text(encoding="utf-8"))
        if seed_manifest.get("sourceWorkbookSha256") != inventory["sourceWorkbookSha256"]:
            raise ValueError("seed batch came from a different workbook version")
        seed_records = {int(item["sourceRow"]): item for item in seed_manifest["records"]}
        for record in manifest["records"]:
            prior = seed_records.get(int(record["sourceRow"]))
            if not prior or prior.get("url") != record["url"] or prior.get("pageType") != record["pageType"]:
                continue
            page_type = "brand-category" if record["pageType"] == "Brand Category Page" else "brand"
            source = seed_batch / "pages" / record["pageKey"] / page_type
            destination = batch / "pages" / record["pageKey"] / page_type
            if all((source / name).is_file() for name in CAPTURE_FILES) and json.loads((source / "response.json").read_text()).get("ok") is True:
                if not destination.exists():
                    shutil.copytree(source, destination)
                record["collectionStatus"] = "seeded"
        write_json(manifest_path, manifest)
    attempted = 0
    pending = [record for record in manifest["records"]
               if (not args.only_row or int(record["sourceRow"]) in args.only_row)
               and record.get("collectionStatus") not in {"seeded", "captured", "reused"}]
    if args.limit is not None:
        pending = pending[:args.limit]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(capture_page, record, batch, api_key, args.timeout, args.retries): record for record in pending}
        for future in as_completed(futures):
            record = futures[future]
            result = future.result()
            record["collectionStatus"] = result
            write_json(manifest_path, manifest)
            attempted += int(result != "reused")
            print(f"{result.upper()} {record['pageKey']} {record['url']}", flush=True)
    print(batch, flush=True)
    return 1 if any(record["collectionStatus"] == "failed" for record in manifest["records"]) else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"BCP population capture failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
