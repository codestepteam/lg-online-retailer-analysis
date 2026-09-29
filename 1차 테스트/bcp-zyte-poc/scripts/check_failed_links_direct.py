#!/usr/bin/env python3
"""Retry failed BCP link checks as separate Zyte browser visits."""

from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

from capture_bcp_population import ROOT
import zyte_capture as zyte


class PageTitle(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.in_h1 = False
        self.title = ""
        self.h1 = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title" and not self.title:
            self.in_title = True
        if tag == "h1" and not self.h1:
            self.in_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self.in_h1:
            self.h1 += data


def check(link: dict[str, object], api_key: str) -> dict[str, object]:
    try:
        response = zyte._post_json(api_key, {"url": link["url"], "browserHtml": True, "screenshot": False}, 120, 1)
        html = str(response.get("browserHtml") or "")
        parser = PageTitle()
        parser.feed(html)
        return {**link, "status": response.get("statusCode"), "finalUrl": response.get("url"),
                "title": unescape(parser.title).strip()[:250], "h1": unescape(parser.h1).strip()[:250],
                "bodyLength": len(html)}
    except Exception as exc:
        return {**link, "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    batch = args.batch.resolve()
    api_key = zyte._load_env(ROOT)
    if not api_key:
        raise RuntimeError("ZYTE_API_KEY is missing")
    check_dir = batch / "link-check"
    target = batch / "link-check-direct"
    target.mkdir(exist_ok=True)
    links: list[tuple[str, dict[str, object]]] = []
    grouped: dict[str, list[dict[str, object]]] = {}
    for path in sorted(check_dir.glob("*.json")):
        data = json.loads(path.read_text())
        existing_path = target / path.name
        existing = json.loads(existing_path.read_text()).get("results", []) if existing_path.is_file() else []
        grouped[path.stem] = [x for x in existing if x.get("status") == 200 and re.search(r"\bLG\b", str(x.get("title") or "") + " " + str(x.get("h1") or ""), re.I)]
        verified_urls = {str(x.get("url")) for x in grouped[path.stem]}
        for link in data["results"]:
            title = str(link.get("title") or "")
            if link.get("status") == 200 and not re.search(r"captcha|confirm you are human|verify you are human", title, re.I):
                continue
            if str(link.get("url")) in verified_urls:
                continue
            links.append((path.stem, {k: link[k] for k in ("kind", "label", "url")}))
    print(f"retry targets={len(links)}", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check, link, api_key): key for key, link in links}
        for future in as_completed(futures):
            key = futures[future]
            result = future.result()
            grouped[key] = [x for x in grouped.get(key, []) if x.get("url") != result.get("url")] + [result]
            print(key, result.get("status", "error"), result.get("title", result.get("error", ""))[:70], flush=True)
            (target / f"{key}.json").write_text(json.dumps({"pageKey": key, "results": grouped[key],
                   "source": "Zyte browser direct navigation"}, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"direct BCP link check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
