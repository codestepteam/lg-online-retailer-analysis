#!/usr/bin/env python3
"""Build a self-contained, static copy of an HTML page.

The input may be an HTTP(S) URL or a local HTML file.  The original bytes are
kept as ``page.raw.html``; ``index.html`` is the offline copy.  The module is
deliberately stdlib-only so it can run beside the capture scripts without a
dependency install.
"""

from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html as html_lib
import json
import mimetypes
import os
import posixpath
import re
import sys
import threading
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, quote, unquote, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, url2pathname, urlopen


USER_AGENT = "LG-Clinic-OfflineCapture/1.0"
RETRYABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}
ZYTE_FALLBACK_STATUS = {400, 401, 403, 429}
SECRET_QUERY_RE = re.compile(r"(?:token|secret|signature|sig|password|passwd|api[_-]?key|auth|session|credential)", re.I)
CSS_URL_RE = re.compile(r"url\(\s*(?P<quote>[\"']?)(?P<url>.*?)(?P=quote)\s*\)", re.I | re.S)
CSS_IMPORT_RE = re.compile(r"(@import\s+)([\"'])([^\"']+)(\2)", re.I)
SRCSET_SPLIT_RE = re.compile(r"\s+", re.S)

LAZY_URL_ATTRS = (
    "data-src",
    "data-original",
    "data-lazy-src",
    "data-image",
    "data-image-url",
    "data-url",
    "data-poster",
)
SRCSET_ATTRS = ("srcset", "data-srcset", "data-lazy-srcset", "imagesrcset")
IMAGE_TAGS = {"img", "image", "source", "video", "audio", "track", "object", "embed"}
SVG_REFERENCE_TAGS = {"use", "image", "feimage"}
SVG_CSS_URL_ATTRS = {"fill", "stroke", "filter", "clip-path", "mask", "marker", "marker-start", "marker-mid", "marker-end"}
SKIP_SCHEMES = {"about", "blob", "data", "javascript", "mailto", "tel", "sms"}


def _public_url(value: str) -> str:
    """Return a URL safe to put in a manifest while preserving useful queries."""
    try:
        parts = urlsplit(value)
    except ValueError:
        return "[INVALID_URL]"
    query = [(key, "[REDACTED_SECRET]" if SECRET_QUERY_RE.search(key) else item) for key, item in parse_qsl(parts.query, keep_blank_values=True)]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), "")) or value.split("#", 1)[0]


def _has_query(value: str) -> bool:
    try:
        return bool(urlsplit(value).query)
    except ValueError:
        return "?" in value.split("#", 1)[0]


def _canonical_url(value: str) -> str:
    return urlunsplit(urlsplit(value)._replace(fragment=""))


def _normalize_url(value: str) -> str:
    """Quote literal whitespace/unicode while preserving existing escapes."""
    try:
        parts = urlsplit(value)
    except ValueError:
        return value
    if parts.scheme.lower() not in {"http", "https"}:
        return value
    path = quote(parts.path, safe="/%:@-._~!$&'()*+,;=")
    query = quote(parts.query, safe="=&%:@-._~!$'()*+,;/?")
    return urlunsplit((parts.scheme, parts.netloc, path, query, parts.fragment))


def _same_document_fragment(value: str, base_url: str) -> str | None:
    try:
        value_parts = urlsplit(value)
        base_parts = urlsplit(base_url)
    except ValueError:
        return None
    if not value_parts.fragment or not value_parts.scheme or not value_parts.netloc:
        return None
    if (value_parts.scheme.lower(), value_parts.netloc.lower(), value_parts.path, value_parts.query) == (
        base_parts.scheme.lower(), base_parts.netloc.lower(), base_parts.path, base_parts.query
    ):
        return f"#{value_parts.fragment}"
    return None


def _safe_path(value: str) -> str:
    return posixpath.normpath(value).lstrip("/")


def _guess_extension(url: str, content_type: str, kind: str) -> str:
    mime = content_type.split(";", 1)[0].strip().lower()
    known = {
        "text/css": ".css",
        "text/html": ".html",
        "application/xhtml+xml": ".html",
        "image/svg+xml": ".svg",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/avif": ".avif",
        "image/x-icon": ".ico",
        "font/woff": ".woff",
        "font/woff2": ".woff2",
        "application/font-woff": ".woff",
        "application/vnd.ms-fontobject": ".eot",
        "font/ttf": ".ttf",
        "font/otf": ".otf",
        "application/javascript": ".js",
        "text/javascript": ".js",
        "application/json": ".json",
    }
    if mime in known:
        return known[mime]
    suffix = Path(urlsplit(url).path).suffix.lower()
    if re.fullmatch(r"\.[a-z0-9]{1,8}", suffix):
        return suffix
    if kind == "stylesheet":
        return ".css"
    if kind == "iframe":
        return ".html"
    guessed = mimetypes.guess_extension(mime) if mime else None
    return guessed or ".bin"


def _decode_html(body: bytes, content_type: str = "") -> str:
    charset = None
    match = re.search(r"charset\s*=\s*[\"']?([^;\s\"']+)", content_type, re.I)
    if match:
        charset = match.group(1)
    if not charset:
        head = body[:4096].decode("ascii", errors="ignore")
        match = re.search(r"<meta[^>]+charset\s*=\s*[\"']?([^\s\"'>/]+)", head, re.I)
        if match:
            charset = match.group(1)
    for encoding in (charset, "utf-8", "cp1252"):
        if not encoding:
            continue
        try:
            return body.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            pass
    return body.decode("utf-8", errors="replace")


def _local_zyte_key() -> str | None:
    value = os.environ.get("ZYTE_API_KEY")
    if value:
        return value
    try:
        for raw in (Path(__file__).resolve().parents[1] / ".env").read_text(encoding="utf-8").splitlines():
            name, separator, item = raw.partition("=")
            if separator and name.strip() == "ZYTE_API_KEY":
                item = item.strip()
                if len(item) >= 2 and item[0] == item[-1] and item[0] in {"'", '"'}:
                    item = item[1:-1]
                return item
    except OSError:
        pass
    return None


def _is_unsupported_url(value: str) -> bool:
    if not value or value.startswith("#"):
        return True
    try:
        scheme = urlsplit(value).scheme.lower()
    except ValueError:
        return True
    return scheme in SKIP_SCHEMES


def _file_url_disallowed(remote_source: bool, absolute_url: str) -> bool:
    """Never let a remote page turn an asset reference into a local file read."""
    return remote_source and urlsplit(absolute_url).scheme.lower() == "file"


def _split_srcset(value: str) -> list[tuple[str, str]]:
    """Split normal srcset candidates without breaking parentheses."""
    if value.lstrip().lower().startswith("data:"):
        return [(value.strip(), "")]
    pieces: list[str] = []
    current: list[str] = []
    depth = 0
    quote = ""
    for char in value:
        if quote:
            current.append(char)
            if char == quote:
                quote = ""
            continue
        if char in "\"'":
            quote = char
            current.append(char)
        elif char == "(":
            depth += 1
            current.append(char)
        elif char == ")":
            depth = max(0, depth - 1)
            current.append(char)
        elif char == "," and depth == 0:
            candidate = "".join(current)
            candidate_text = candidate.strip()
            # A comma followed by a descriptor boundary separates candidates;
            # commas inside query strings (for example Scene7 transforms) do not.
            if re.search(r"\s", candidate_text) or not re.search(r"[?&=]", candidate_text):
                pieces.append(candidate.strip())
                current = []
            else:
                current.append(char)
        else:
            current.append(char)
    if current:
        pieces.append("".join(current).strip())
    candidates: list[tuple[str, str]] = []
    for piece in pieces:
        if not piece:
            continue
        match = SRCSET_SPLIT_RE.split(piece, maxsplit=1)
        candidates.append((match[0], match[1] if len(match) == 2 else ""))
    return candidates


def _is_placeholder(value: str) -> bool:
    lowered = value.strip().lower()
    return (
        not lowered
        or lowered in {"#", "about:blank"}
        or lowered.startswith("data:image/gif;base64,r0lgod")
        or any(token in lowered for token in ("placeholder", "spacer", "transparent.gif", "blank.gif"))
    )


@dataclass
class FetchResult:
    body: bytes
    final_url: str
    status: int
    content_type: str
    attempts: int
    cached: bool = False
    source: str = "direct"


class FetchError(RuntimeError):
    def __init__(self, message: str, *, url: str, attempts: int, status: int | None = None):
        super().__init__(message)
        self.url = url
        self.attempts = attempts
        self.status = status


def _looks_like_html(body: bytes, mime: str) -> bool:
    if mime in {"text/html", "application/xhtml+xml"}:
        return True
    head = body[:512].lstrip().lower()
    return head.startswith((b"<!doctype html", b"<html", b"<head", b"<body"))


class Fetcher:
    def __init__(self, *, timeout: float, retries: int, max_bytes: int, cache_dir: Path | None, zyte_api_key: str | None = None, zyte_timeout: float = 20, zyte_retries: int = 1, max_zyte_fallback: int = 600):
        self.timeout = max(0.5, min(float(timeout), 120.0))
        self.retries = max(0, min(int(retries), 5))
        self.max_bytes = max(1024, int(max_bytes))
        self.cache_dir = cache_dir
        self.zyte_api_key = zyte_api_key
        self.zyte_timeout = max(0.5, min(float(zyte_timeout), 120.0))
        self.zyte_retries = max(0, min(int(zyte_retries), 3))
        self.max_zyte_fallback = max(0, int(max_zyte_fallback))
        self.zyte_fallback_count = 0
        self.zyte_lock = threading.Lock()
        self.memory: dict[str, FetchResult] = {}
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_paths(self, url: str) -> tuple[Path, Path]:
        digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
        assert self.cache_dir is not None
        return self.cache_dir / f"{digest}.bin", self.cache_dir / f"{digest}.json"

    def _cached(self, url: str) -> FetchResult | None:
        if not self.cache_dir:
            return None
        body_path, meta_path = self._cache_paths(url)
        if not body_path.is_file() or not meta_path.is_file():
            return None
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            return FetchResult(
                body=body_path.read_bytes(),
                final_url=meta.get("final_url", url),
                status=int(meta.get("status", 200)),
                content_type=str(meta.get("content_type", "")),
                attempts=0,
                cached=True,
                source=str(meta.get("source", "cache")),
            )
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return None

    def _save_cache(self, url: str, result: FetchResult) -> None:
        if not self.cache_dir:
            return
        body_path, meta_path = self._cache_paths(url)
        try:
            body_path.write_bytes(result.body)
            meta_path.write_text(
                json.dumps({"status": result.status, "content_type": result.content_type, "final_url": _public_url(result.final_url), "source": result.source}),
                encoding="utf-8",
            )
        except OSError:
            pass

    def _read_bounded(self, response) -> bytes:
        """Read in chunks so a keep-alive response cannot wait forever for EOF."""
        chunks: list[bytes] = []
        total = 0
        deadline = time.monotonic() + self.timeout
        while total <= self.max_bytes:
            if time.monotonic() >= deadline:
                raise TimeoutError("resource read timeout")
            chunk = response.read(min(64 * 1024, self.max_bytes + 1 - total))
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)
            total += len(chunk)
        return b"".join(chunks)

    def get(self, url: str) -> FetchResult:
        key = _canonical_url(_normalize_url(url))
        if key in self.memory:
            previous = self.memory[key]
            return FetchResult(**{**previous.__dict__, "cached": True, "attempts": 0})
        cached = self._cached(key)
        if cached:
            self.memory[key] = cached
            return cached

        parts = urlsplit(key)
        if parts.scheme == "file":
            path = Path(url2pathname(unquote(parts.path)))
            try:
                body = path.read_bytes()
            except OSError as exc:
                raise FetchError(str(exc), url=key, attempts=1) from exc
            if len(body) > self.max_bytes:
                raise FetchError("resource exceeds max-bytes", url=key, attempts=1)
            result = FetchResult(body, key, 200, mimetypes.guess_type(path.name)[0] or "", 1)
            self.memory[key] = result
            return result

        last_error: FetchError | None = None
        for attempt in range(1, self.retries + 2):
            try:
                request = Request(key, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
                with urlopen(request, timeout=self.timeout) as response:
                    length = response.headers.get("Content-Length")
                    if length and int(length) > self.max_bytes:
                        raise FetchError("resource exceeds max-bytes", url=key, attempts=attempt)
                    body = self._read_bounded(response)
                    if len(body) > self.max_bytes:
                        raise FetchError("resource exceeds max-bytes", url=key, attempts=attempt)
                    result = FetchResult(
                        body=body,
                        final_url=response.geturl(),
                        status=int(response.status),
                        content_type=response.headers.get_content_type(),
                        attempts=attempt,
                    )
                    self.memory[key] = result
                    self._save_cache(key, result)
                    return result
            except FetchError as exc:
                last_error = exc
                if attempt > self.retries or exc.status not in RETRYABLE_STATUS:
                    break
            except HTTPError as exc:
                last_error = FetchError(f"HTTP {exc.code}", url=key, attempts=attempt, status=exc.code)
                if attempt > self.retries or exc.code not in RETRYABLE_STATUS:
                    break
            except (URLError, TimeoutError, OSError, ValueError) as exc:
                last_error = FetchError(str(exc), url=key, attempts=attempt)
                if attempt > self.retries:
                    break
            time.sleep(min(0.25 * attempt, 1.0))
        if self.zyte_api_key and last_error and (last_error.status in ZYTE_FALLBACK_STATUS or last_error.status is None):
            try:
                return self._get_via_zyte(key)
            except FetchError as exc:
                last_error = exc
        assert last_error is not None
        raise last_error

    def _get_via_zyte(self, url: str) -> FetchResult:
        with self.zyte_lock:
            if self.zyte_fallback_count >= self.max_zyte_fallback:
                raise FetchError("max-Zyte-fallback reached", url=url, attempts=0)
            self.zyte_fallback_count += 1
        payload = json.dumps({"url": url, "httpResponseBody": True, "httpResponseHeaders": True}).encode("utf-8")
        auth = base64.b64encode(f"{self.zyte_api_key}:".encode("utf-8")).decode("ascii")
        last_error: FetchError | None = None
        for attempt in range(1, self.zyte_retries + 2):
            request = Request(
                "https://api.zyte.com/v1/extract",
                data=payload,
                headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json", "Accept": "application/json"},
                method="POST",
            )
            try:
                with urlopen(request, timeout=self.zyte_timeout) as response:
                    body = json.loads(response.read().decode("utf-8"))
                encoded = body.get("httpResponseBody")
                if not isinstance(encoded, str):
                    raise ValueError("Zyte asset response has no httpResponseBody")
                data = base64.b64decode(encoded, validate=True)
                if len(data) > self.max_bytes:
                    raise ValueError("resource exceeds max-bytes")
                status = int(body.get("statusCode", 200))
                if not 200 <= status < 400:
                    raise FetchError(f"HTTP {status} via Zyte", url=url, attempts=attempt, status=status)
                content_type = ""
                headers = body.get("httpResponseHeaders", [])
                if isinstance(headers, list):
                    for item in headers:
                        if isinstance(item, dict) and str(item.get("name", "")).lower() == "content-type":
                            content_type = str(item.get("value", ""))
                            break
                result = FetchResult(data, str(body.get("url") or url), status, content_type, attempt, source="zyte-http")
                self.memory[_canonical_url(url)] = result
                self._save_cache(_canonical_url(url), result)
                return result
            except FetchError as exc:
                last_error = exc
                if attempt > self.zyte_retries or exc.status not in RETRYABLE_STATUS:
                    break
            except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
                status = exc.code if isinstance(exc, HTTPError) else None
                last_error = FetchError(str(exc), url=url, attempts=attempt, status=status)
                if attempt > self.zyte_retries or (status is not None and status not in RETRYABLE_STATUS):
                    break
            time.sleep(min(0.25 * attempt, 1.0))
        assert last_error is not None
        raise last_error


@dataclass
class Event:
    kind: str
    tag: str = ""
    attrs: list[tuple[str, str | None]] | None = None
    data: str = ""
    self_closing: bool = False


class EventParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.events: list[Event] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.events.append(Event("start", tag.lower(), list(attrs)))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.events.append(Event("start", tag.lower(), list(attrs), self_closing=True))

    def handle_endtag(self, tag: str) -> None:
        self.events.append(Event("end", tag.lower()))

    def handle_data(self, data: str) -> None:
        self.events.append(Event("data", data=data))

    def handle_entityref(self, name: str) -> None:
        self.events.append(Event("raw", data=f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self.events.append(Event("raw", data=f"&#{name};"))

    def handle_comment(self, data: str) -> None:
        self.events.append(Event("raw", data=f"<!--{data}-->"))

    def handle_decl(self, decl: str) -> None:
        self.events.append(Event("raw", data=f"<!{decl}>"))

    def handle_pi(self, data: str) -> None:
        self.events.append(Event("raw", data=f"<?{data}>"))

    def unknown_decl(self, data: str) -> None:
        self.events.append(Event("raw", data=f"<![{data}]>"))


def _attrs_dict(attrs: Iterable[tuple[str, str | None]]) -> dict[str, str | None]:
    return {key.lower(): value for key, value in attrs}


def _render_attrs(attrs: Iterable[tuple[str, str | None]]) -> str:
    rendered = []
    for key, value in attrs:
        if value is None:
            rendered.append(key)
        else:
            rendered.append(f'{key}="{html_lib.escape(value, quote=True)}"')
    return (" " + " ".join(rendered)) if rendered else ""


class OfflineCapture:
    def __init__(
        self,
        output_dir: Path,
        *,
        base_url: str | None = None,
        timeout: float = 20,
        retries: int = 2,
        max_assets: int = 10000,
        max_asset_bytes: int = 32 * 1024 * 1024,
        max_total_bytes: int = 300 * 1024 * 1024,
        max_frames: int = 16,
        max_frame_depth: int = 2,
        prefetch_workers: int = 8,
        zyte_api_key: str | None = None,
        zyte_timeout: float = 20,
        zyte_retries: int = 1,
        max_zyte_fallback: int = 600,
        cache_dir: Path | None = None,
    ) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_url_override = base_url
        self.remote_source = bool(base_url and urlsplit(base_url).scheme.lower() in {"http", "https"})
        self.fetcher = Fetcher(timeout=timeout, retries=retries, max_bytes=max_asset_bytes, cache_dir=cache_dir, zyte_api_key=zyte_api_key, zyte_timeout=zyte_timeout, zyte_retries=zyte_retries, max_zyte_fallback=max_zyte_fallback)
        self.max_assets = max(1, max_assets)
        self.max_total_bytes = max(1024, max_total_bytes)
        self.max_frames = max(0, max_frames)
        self.max_frame_depth = max(0, max_frame_depth)
        self.prefetch_workers = max(1, min(int(prefetch_workers), 16))
        self.asset_paths: dict[str, str] = {}
        self.asset_records: dict[str, dict[str, object]] = {}
        self.asset_hash_paths: dict[tuple[str, str], str] = {}
        self.failures: list[dict[str, object]] = []
        self.failed_urls: set[str] = set()
        self.frames: list[dict[str, object]] = []
        self.total_bytes = 0
        self.frame_index = 0
        self.frame_stack: set[str] = set()

    def _failure(self, url: str, kind: str, error: str, *, attempts: int = 0, status: int | None = None) -> None:
        key = _canonical_url(url) if url else url
        if key in self.failed_urls:
            return
        self.failed_urls.add(key)
        self.failures.append(
            {
                "url": _public_url(url),
                "query_present": _has_query(url),
                "kind": kind,
                "error": error,
                "attempts": attempts,
                **({"status": status} if status is not None else {}),
            }
        )

    def _asset_ref(self, raw: str, base_url: str, kind: str, doc_dir: str) -> str | None:
        if _is_unsupported_url(raw):
            return raw if raw else None
        absolute = _normalize_url(urljoin(base_url, raw.strip()))
        if _is_unsupported_url(absolute):
            return raw
        if _file_url_disallowed(self.remote_source, absolute):
            self._failure(absolute, kind, "file URL disallowed for remote source")
            return None
        parts = urlsplit(absolute)
        key = _canonical_url(absolute)
        fragment = f"#{parts.fragment}" if parts.fragment else ""
        if key in self.asset_paths:
            path = self.asset_paths[key]
            return posixpath.relpath(path, doc_dir or ".") + fragment
        if key in self.failed_urls:
            return None
        if len(self.asset_paths) >= self.max_assets:
            self._failure(key, kind, "max-assets reached")
            return None
        try:
            result = self.fetcher.get(key)
        except FetchError as exc:
            self._failure(key, kind, str(exc), attempts=exc.attempts, status=exc.status)
            return None
        mime = result.content_type.lower().split(";", 1)[0]
        if kind in {"image", "font", "css-url", "stylesheet"} and _looks_like_html(result.body, mime):
            if result.source != "zyte-http" and self.fetcher.zyte_api_key:
                try:
                    retry = self.fetcher._get_via_zyte(key)
                except FetchError as exc:
                    self._failure(key, kind, str(exc), attempts=exc.attempts, status=exc.status)
                    return None
                retry_mime = retry.content_type.lower().split(";", 1)[0]
                if not _looks_like_html(retry.body, retry_mime):
                    result = retry
                    mime = retry_mime
                else:
                    self._failure(key, kind, f"unexpected content-type {retry_mime or 'html'} via Zyte", attempts=retry.attempts, status=retry.status)
                    return None
            else:
                self._failure(key, kind, f"unexpected content-type {mime or 'html'}", attempts=result.attempts, status=result.status)
                return None
        if self.total_bytes + len(result.body) > self.max_total_bytes:
            self._failure(key, kind, "max-total-bytes reached", attempts=result.attempts, status=result.status)
            return None

        ext = _guess_extension(result.final_url or key, result.content_type, kind)
        digest = hashlib.sha256(result.body).hexdigest()
        hash_key = (digest, ext)
        path = self.asset_hash_paths.get(hash_key)
        if path is None:
            path = f"assets/{digest}{ext}"
            self.asset_hash_paths[hash_key] = path
            (self.output_dir / path).parent.mkdir(parents=True, exist_ok=True)
            (self.output_dir / path).write_bytes(result.body)
        self.asset_paths[key] = path
        record = {
            "url": _public_url(key),
            "query_present": _has_query(key),
            "final_url": _public_url(result.final_url),
            "path": path,
            "kind": kind,
            "content_type": result.content_type,
            "status": result.status,
            "bytes": len(result.body),
            "sha256": digest,
            "attempts": result.attempts,
            "cached": result.cached,
            "source": result.source,
        }
        self.asset_records[key] = record
        self.total_bytes += len(result.body)

        if result.content_type.lower().split(";", 1)[0] == "text/css" or ext == ".css" or kind == "stylesheet":
            css = _decode_html(result.body, result.content_type)
            rewritten = self._rewrite_css(css, result.final_url or key, "assets")
            final_body = rewritten.encode("utf-8")
            (self.output_dir / path).write_bytes(final_body)
            record["bytes"] = len(final_body)
            record["sha256"] = hashlib.sha256(final_body).hexdigest()
        return posixpath.relpath(path, doc_dir or ".") + fragment

    def _rewrite_css(self, css: str, base_url: str, doc_dir: str) -> str:
        css_urls: dict[str, str] = {}
        for match in CSS_URL_RE.finditer(css):
            raw = match.group("url").strip()
            if not _is_unsupported_url(raw) and not raw.startswith("#"):
                css_urls.setdefault(_canonical_url(_normalize_url(urljoin(base_url, raw))), "css-url")
        for match in CSS_IMPORT_RE.finditer(css):
            raw = match.group(3).strip()
            if not _is_unsupported_url(raw):
                css_urls.setdefault(_canonical_url(_normalize_url(urljoin(base_url, raw))), "stylesheet")
        candidates = list(css_urls.items())[: self.max_assets]
        if candidates:
            with ThreadPoolExecutor(max_workers=self.prefetch_workers) as executor:
                list(executor.map(lambda item: self._prefetch_one(*item), candidates))

        def replace_url(match: re.Match[str]) -> str:
            raw = match.group("url").strip()
            local_fragment = _same_document_fragment(raw, base_url)
            if local_fragment:
                quote = match.group("quote") or ""
                return f"url({quote}{local_fragment}{quote})"
            if _is_unsupported_url(raw) or raw.startswith("#"):
                return match.group(0)
            local = self._asset_ref(raw, base_url, "css-url", doc_dir)
            if local is None:
                local = "data:,"
            quote = match.group("quote") or ""
            return f"url({quote}{local}{quote})"

        rewritten = CSS_URL_RE.sub(replace_url, css)

        def replace_import(match: re.Match[str]) -> str:
            local = self._asset_ref(match.group(3), base_url, "stylesheet", doc_dir)
            return f"{match.group(1)}{match.group(2)}{local or 'data:,'}{match.group(4)}"

        return CSS_IMPORT_RE.sub(replace_import, rewritten)

    def _rewrite_srcset(self, value: str, base_url: str, doc_dir: str) -> str | None:
        output: list[str] = []
        for raw_url, descriptor in _split_srcset(value):
            local = self._asset_ref(raw_url, base_url, "image", doc_dir)
            if local is None:
                continue
            output.append(local + (f" {descriptor}" if descriptor else ""))
        return ", ".join(output) or None

    def _document_base(self, events: list[Event], fallback: str) -> str:
        for event in events:
            if event.kind != "start" or event.tag != "base" or not event.attrs:
                continue
            attrs = _attrs_dict(event.attrs)
            if attrs.get("href"):
                return _normalize_url(urljoin(fallback, str(attrs["href"])))
        return fallback

    def _capture_frame(self, raw_url: str, base_url: str, doc_dir: str, srcdoc: str | None, depth: int) -> str:
        self.frame_index += 1
        frame_name = f"frames/iframe-{self.frame_index:03d}.html"
        frame_path = self.output_dir / frame_name
        frame_path.parent.mkdir(parents=True, exist_ok=True)
        absolute = _normalize_url(urljoin(base_url, raw_url)) if raw_url else ""
        key = _canonical_url(absolute) if absolute else ""
        if key and _file_url_disallowed(self.remote_source, key):
            frame_path.write_text("<!doctype html><meta charset=\"utf-8\"><p>Offline iframe capture unavailable.</p>", encoding="utf-8")
            self._failure(key, "iframe", "file URL disallowed for remote source")
            self.frames.append({"url": _public_url(key), "path": frame_name, "status": None, "error": "file URL disallowed"})
            return posixpath.relpath(frame_name, doc_dir or ".")
        if depth > self.max_frame_depth or self.frame_index > self.max_frames or (key and key in self.frame_stack):
            body = "<!doctype html><meta charset=\"utf-8\"><p>Offline iframe capture unavailable.</p>"
            frame_path.write_text(body, encoding="utf-8")
            self._failure(key or raw_url, "iframe", "frame-depth or frame-count limit")
            self.frames.append({"url": _public_url(key or raw_url), "path": frame_name, "status": None, "error": "limit"})
            return posixpath.relpath(frame_name, doc_dir or ".")

        if srcdoc is not None:
            body = srcdoc.encode("utf-8")
            final_url = base_url
            status = 200
            content_type = "text/html"
            attempts = 0
        else:
            try:
                result = self.fetcher.get(key)
                body, final_url, status, content_type, attempts = result.body, result.final_url, result.status, result.content_type, result.attempts
            except FetchError as exc:
                placeholder = "<!doctype html><meta charset=\"utf-8\"><p>Offline iframe capture unavailable.</p>"
                frame_path.write_text(placeholder, encoding="utf-8")
                self._failure(key, "iframe", str(exc), attempts=exc.attempts, status=exc.status)
                self.frames.append({"url": _public_url(key), "path": frame_name, "status": exc.status, "error": str(exc)})
                return posixpath.relpath(frame_name, doc_dir or ".")

        self.frame_stack.add(key)
        try:
            parser = EventParser()
            parser.feed(_decode_html(body, content_type))
            frame_base = self._document_base(parser.events, final_url)
            self._prefetch(parser.events, frame_base)
            rendered = self._render_events(parser.events, frame_base, "frames", depth)
            frame_path.write_text(rendered, encoding="utf-8")
        finally:
            self.frame_stack.discard(key)
        digest = hashlib.sha256(frame_path.read_bytes()).hexdigest()
        self.frames.append(
            {
                "url": _public_url(key or final_url),
                "query_present": _has_query(key or final_url),
                "path": frame_name,
                "status": status,
                "bytes": frame_path.stat().st_size,
                "sha256": digest,
                "attempts": attempts,
            }
        )
        return posixpath.relpath(frame_name, doc_dir or ".")

    def _prefetch(self, events: list[Event], base_url: str) -> None:
        """Warm direct page assets concurrently; recursive CSS stays demand-driven."""
        urls: dict[str, str] = {}
        style_depth = 0
        for event in events:
            if event.kind == "data" and style_depth:
                for match in CSS_URL_RE.finditer(event.data):
                    raw = match.group("url").strip()
                    if not _is_unsupported_url(raw):
                        absolute = _canonical_url(_normalize_url(urljoin(base_url, raw)))
                        urls.setdefault(absolute, "css-url")
                continue
            if event.kind != "start":
                if event.kind == "end" and event.tag == "style":
                    style_depth = max(0, style_depth - 1)
                continue
            attrs = _attrs_dict(event.attrs or [])
            if event.tag == "style":
                style_depth += 1
            if attrs.get("style"):
                for match in CSS_URL_RE.finditer(str(attrs["style"])):
                    raw = match.group("url").strip()
                    if not _is_unsupported_url(raw):
                        urls.setdefault(_canonical_url(_normalize_url(urljoin(base_url, raw))), "css-url")
            if event.tag in {"img", "source"}:
                primary = str(attrs.get("src") or "")
                for key in LAZY_URL_ATTRS:
                    candidate = str(attrs.get(key) or "")
                    if candidate and (not primary or _is_placeholder(primary)):
                        primary = candidate
                        break
                candidates = [primary] if primary else []
                for key in SRCSET_ATTRS:
                    if attrs.get(key):
                        candidates.extend(item[0] for item in _split_srcset(str(attrs[key])))
                for raw in candidates:
                    if not _is_unsupported_url(raw):
                        urls.setdefault(_canonical_url(_normalize_url(urljoin(base_url, raw))), "image")
            elif event.tag in IMAGE_TAGS or event.tag in SVG_REFERENCE_TAGS:
                for key in {"src", "poster", "data", "href", "xlink:href", "data-poster"}:
                    raw = str(attrs.get(key) or "")
                    if raw and not _is_unsupported_url(raw):
                        urls.setdefault(_canonical_url(_normalize_url(urljoin(base_url, raw))), "image")
            elif event.tag == "link":
                rel = {part.lower() for part in str(attrs.get("rel") or "").split()}
                kind = "stylesheet" if "stylesheet" in rel else None
                if any("icon" in token for token in rel):
                    kind = "image"
                if "preload" in rel:
                    continue
                raw = str(attrs.get("href") or "")
                if kind and raw and not _is_unsupported_url(raw):
                    urls.setdefault(_canonical_url(_normalize_url(urljoin(base_url, raw))), kind)
        candidates = list(urls.items())[: self.max_assets]
        if not candidates:
            return
        with ThreadPoolExecutor(max_workers=self.prefetch_workers) as executor:
            list(executor.map(lambda item: self._prefetch_one(*item), candidates))

    def _prefetch_one(self, url: str, _kind: str) -> None:
        if _file_url_disallowed(self.remote_source, url):
            return
        try:
            self.fetcher.get(url)
        except FetchError:
            pass

    def _render_events(self, events: list[Event], base_url: str, doc_dir: str, depth: int) -> str:
        output: list[str] = []
        stack: list[str] = []
        style_depth = 0
        for event in events:
            if event.kind == "raw":
                output.append(event.data)
                continue
            if event.kind == "data":
                if style_depth:
                    output.append(self._rewrite_css(event.data, base_url, doc_dir))
                else:
                    output.append(event.data)
                continue
            if event.kind == "end":
                if event.tag == "style" and style_depth:
                    style_depth -= 1
                output.append(f"</{event.tag}>")
                if stack and stack[-1] == event.tag:
                    stack.pop()
                continue

            attrs = list(event.attrs or [])
            amap = _attrs_dict(attrs)
            tag = event.tag
            if tag == "base":
                continue
            if tag == "meta" and str(amap.get("http-equiv", "")).lower() == "refresh":
                continue
            attrs = [(key, value) for key, value in attrs if not key.lower().startswith("on")]
            amap = _attrs_dict(attrs)
            if tag in {"link", "img", "source", "script", "video", "audio", "iframe"}:
                attrs = [(key, value) for key, value in attrs if key.lower() not in {"integrity", "crossorigin"}]
                amap = _attrs_dict(attrs)
            if amap.get("style"):
                attrs = [(key, self._rewrite_css(value, base_url, doc_dir) if key.lower() == "style" and value else value) for key, value in attrs]
                amap = _attrs_dict(attrs)
            attrs = [(key, self._rewrite_css(value, base_url, doc_dir) if value and key.lower() in SVG_CSS_URL_ATTRS and "url(" in value else value) for key, value in attrs]

            if tag == "script":
                attrs = [(key, value) for key, value in attrs if key.lower() not in {"src", "async", "defer", "crossorigin", "integrity", "nomodule"}]
                script_type = str(amap.get("type") or "").lower()
                if script_type == "speculationrules":
                    attrs = [(key, value) for key, value in attrs if key.lower() != "type"]
                    attrs.append(("type", "application/x-offline-disabled"))
                    attrs.append(("data-offline-disabled", "true"))
                elif not script_type or "javascript" in script_type or "ecmascript" in script_type or script_type == "module":
                    attrs = [(key, value) for key, value in attrs if key.lower() != "type"]
                    attrs.append(("type", "application/x-offline-disabled"))
                    attrs.append(("data-offline-disabled", "true"))
                output.append(f"<script{_render_attrs(attrs)}>")
                stack.append(tag)
                continue

            if tag == "iframe":
                srcdoc = amap.get("srcdoc")
                src = str(amap.get("src") or "")
                if srcdoc is None and _is_unsupported_url(src):
                    local = "about:blank"
                else:
                    local = self._capture_frame(src, base_url, doc_dir, str(srcdoc) if srcdoc is not None else None, depth + 1)
                attrs = [(key, value) for key, value in attrs if key.lower() not in {"src", "srcdoc"}]
                attrs.append(("src", local))
            elif tag in {"img", "source"}:
                attrs_map = _attrs_dict(attrs)
                primary = str(attrs_map.get("src") or "")
                for lazy_key in LAZY_URL_ATTRS:
                    lazy = str(attrs_map.get(lazy_key) or "")
                    if lazy and (not primary or _is_placeholder(primary)):
                        primary = lazy
                        break
                if primary:
                    local = self._asset_ref(primary, base_url, "image", doc_dir)
                    attrs = [(key, value) for key, value in attrs if key.lower() != "src"]
                    if local:
                        attrs.append(("src", local))
                rewritten_srcset = None
                for key, value in attrs:
                    if key.lower() in SRCSET_ATTRS and value:
                        rewritten_srcset = self._rewrite_srcset(value, base_url, doc_dir)
                        if rewritten_srcset is not None:
                            break
                clean: list[tuple[str, str | None]] = []
                for key, value in attrs:
                    lower = key.lower()
                    if lower in LAZY_URL_ATTRS or lower in {"data-srcset", "data-lazy-srcset"}:
                        continue
                    if lower in SRCSET_ATTRS:
                        if rewritten_srcset is not None and not any(k.lower() == "srcset" for k, _ in clean):
                            clean.append(("srcset", rewritten_srcset))
                        continue
                    clean.append((key, value))
                attrs = clean
            elif tag in IMAGE_TAGS or tag in SVG_REFERENCE_TAGS:
                rewritten: list[tuple[str, str | None]] = []
                for key, value in attrs:
                    lower = key.lower()
                    if value and lower in {"src", "poster", "data", "href", "xlink:href", "data-poster"}:
                        local = self._asset_ref(value, base_url, "image", doc_dir)
                        rewritten.append((key, local if local is not None else "about:blank"))
                    else:
                        rewritten.append((key, value))
                attrs = rewritten
            elif tag == "link":
                rel = {part.lower() for part in str(amap.get("rel") or "").split()}
                href = str(amap.get("href") or "")
                kind = None
                if "stylesheet" in rel:
                    kind = "stylesheet"
                elif any("icon" in token for token in rel):
                    kind = "image"
                elif "preload" in rel:
                    continue
                elif "manifest" in rel:
                    kind = "document"
                if kind and href:
                    local = self._asset_ref(href, base_url, kind, doc_dir)
                    attrs = [(key, local if key.lower() == "href" and local else value) for key, value in attrs]
                    if local is None:
                        attrs = [(key, value) for key, value in attrs if key.lower() != "href"]
                elif rel & {"preconnect", "dns-prefetch", "modulepreload", "prefetch", "prerender"}:
                    continue
                elif "preload" in rel and kind is None:
                    continue

            output.append(f"<{tag}{_render_attrs(attrs)}{' /' if event.self_closing else ''}>")
            if tag == "style":
                style_depth += 1
            if not event.self_closing:
                stack.append(tag)
        return "".join(output)

    def capture(self, source: str) -> dict[str, object]:
        source_url = source
        source_result: FetchResult | None = None
        if urlsplit(source).scheme in {"http", "https", "file"}:
            if urlsplit(source).scheme in {"http", "https"}:
                self.remote_source = True
            source_result = self.fetcher.get(source)
            raw_body = source_result.body
            source_url = source_result.final_url
        else:
            path = Path(source).expanduser().resolve()
            raw_body = path.read_bytes()
            source_url = path.as_uri()
        (self.output_dir / "page.raw.html").write_bytes(raw_body)
        parser = EventParser()
        parser.feed(_decode_html(raw_body, source_result.content_type if source_result else "text/html"))
        base_url = self._document_base(parser.events, self.base_url_override or source_url)
        self._prefetch(parser.events, base_url)
        rendered = self._render_events(parser.events, base_url, "", 0)
        (self.output_dir / "index.html").write_text(rendered, encoding="utf-8")

        manifest: dict[str, object] = {
            "version": 1,
            "source": {
                "input": _public_url(source),
                "query_present": _has_query(source),
                "final_url": _public_url(source_url),
                "base_url": _public_url(base_url),
                "status": source_result.status if source_result else 200,
                "bytes": len(raw_body),
                "attempts": source_result.attempts if source_result else 1,
            },
            "files": {"html": "index.html", "raw_html": "page.raw.html"},
            "assets": sorted(self.asset_records.values(), key=lambda item: str(item.get("path", ""))),
            "frames": self.frames,
            "failures": self.failures,
            "limits": {
                "max_assets": self.max_assets,
                "max_asset_bytes": self.fetcher.max_bytes,
                "max_total_bytes": self.max_total_bytes,
                "max_frames": self.max_frames,
                "max_frame_depth": self.max_frame_depth,
                "timeout_seconds": self.fetcher.timeout,
                "retries": self.fetcher.retries,
                "prefetch_workers": self.prefetch_workers,
                "zyte_fallback": bool(self.fetcher.zyte_api_key),
                "max_zyte_fallback": self.fetcher.max_zyte_fallback,
            },
            "stats": {
                "asset_count": len(self.asset_records),
                "asset_bytes": self.total_bytes,
                "failure_count": len(self.failures),
                "frame_count": len(self.frames),
                "zyte_fallback_count": self.fetcher.zyte_fallback_count,
            },
        }
        (self.output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return manifest


def capture(source: str | Path, output_dir: str | Path, **kwargs: object) -> dict[str, object]:
    return OfflineCapture(Path(output_dir), **kwargs).capture(str(source))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="HTML URL or local HTML file")
    parser.add_argument("output_dir", type=Path, help="directory for index.html, page.raw.html, assets/, frames/")
    parser.add_argument("--base-url", help="origin URL used to resolve relative assets for a local HTML file")
    parser.add_argument("--cache-dir", type=Path, help="optional shared raw-response cache directory")
    parser.add_argument("--timeout", type=float, default=20, help="per-request timeout seconds (default: 20)")
    parser.add_argument("--retries", type=int, default=2, help="retries for transient HTTP failures (default: 2)")
    parser.add_argument("--max-assets", type=int, default=10000)
    parser.add_argument("--max-asset-bytes", type=int, default=32 * 1024 * 1024)
    parser.add_argument("--max-total-bytes", type=int, default=300 * 1024 * 1024)
    parser.add_argument("--max-frames", type=int, default=16)
    parser.add_argument("--max-frame-depth", type=int, default=2)
    parser.add_argument("--prefetch-workers", type=int, default=8)
    parser.add_argument("--zyte-fallback", action="store_true", help="use ZYTE_API_KEY from the environment or project .env for direct 400/401/403/429 asset failures")
    parser.add_argument("--zyte-timeout", type=float, default=20)
    parser.add_argument("--zyte-retries", type=int, default=1)
    parser.add_argument("--max-zyte-fallback", type=int, default=600)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest = capture(
            args.source,
            args.output_dir,
            base_url=args.base_url,
            timeout=args.timeout,
            retries=args.retries,
            max_assets=args.max_assets,
            max_asset_bytes=args.max_asset_bytes,
            max_total_bytes=args.max_total_bytes,
            max_frames=args.max_frames,
            max_frame_depth=args.max_frame_depth,
            prefetch_workers=args.prefetch_workers,
            zyte_api_key=_local_zyte_key() if args.zyte_fallback else None,
            zyte_timeout=args.zyte_timeout,
            zyte_retries=args.zyte_retries,
            max_zyte_fallback=args.max_zyte_fallback,
            cache_dir=args.cache_dir,
        )
    except (OSError, FetchError, ValueError) as exc:
        print(f"offline capture failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"html": str(args.output_dir / 'index.html'), "assets": manifest["stats"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
