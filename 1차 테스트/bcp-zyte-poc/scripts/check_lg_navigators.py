#!/usr/bin/env python3
"""Visit the LG category-navigation destinations missing from the 159-page review."""

from __future__ import annotations

import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

from lxml import html

from capture_bcp_population import ROOT
from check_failed_links_direct import check
from check_remaining_navigators import targets_for
import zyte_capture as zyte


BATCH = ROOT / "results_population" / "20260928-all-159"
ROWS = {14, 15, 16, 38, 39, 94, 112, 127, 142, 143, 156}


def links_for(record: dict, tree: html.HtmlElement) -> list[dict]:
    row = int(record["sourceRow"])
    if row in {14, 15, 16, 112, 156}:
        return targets_for(record, tree)
    if row in {38, 39}:
        anchors = tree.xpath('//a[parent::*[contains(@class,"subcategory-box-list")]][@href]')
        return [{"kind": "navigator", "label": " ".join(" ".join(a.itertext()).split())[:150],
                 "url": urljoin(str(record["url"]), a.get("href"))} for a in anchors]
    data = json.loads((BATCH / "parsed" / record["pageKey"] / "bcp-evidence.json").read_text())
    candidates = data["metrics"]["ID21"]["evidence"]["linkCandidates"]
    selected = []
    for item in candidates:
        url = str(item.get("href") or "")
        if row == 94 and re.search(r"/it/brand/lg/lavatrici/carico-\d+-kg", url):
            selected.append(item)
        elif row == 127 and re.search(r"/nl/category/lg-wasmachines-\d+-kg-", url):
            selected.append(item)
        elif row == 142 and re.search(r"/es/brand/lg-electronics/frigorificos/frigorificos-", url):
            selected.append(item)
        elif row == 143 and re.search(r"/es/brand/lg-electronics/lavado/lavador", url):
            selected.append(item)
    return [{"kind": "navigator", "label": str(item.get("text") or "")[:150], "url": str(item["href"])} for item in selected]


def main() -> None:
    records = {int(r["sourceRow"]): r for r in json.loads((BATCH / "manifest.json").read_text())["records"]}
    selected: dict[str, dict] = {}
    unique: dict[str, dict] = {}
    for row in sorted(ROWS):
        record = records[row]
        assert record["brand"] == "LG"
        page = BATCH / "pages" / record["pageKey"] / "brand-category" / "raw.html"
        raw = page.read_bytes()
        targets = links_for(record, html.fromstring(raw))
        assert targets, row
        selected[record["pageKey"]] = {"sourceWorkbookRow": row, "brand": "LG",
                                       "sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(), "targets": targets}
        unique.update({item["url"]: item for item in targets})
    target_dir = BATCH / "navigator-sidebar-check"
    target_dir.mkdir(exist_ok=True)
    existing = {}
    for path in target_dir.glob("*.json"):
        for item in json.loads(path.read_text()).get("results", []):
            if item.get("status") == 200 and (item.get("title") or item.get("h1")):
                existing[item["url"]] = item
    missing = [item for url, item in unique.items() if url not in existing]
    print(f"LG navigator pages={len(selected)} links={len(unique)} to-check={len(missing)}", flush=True)
    api_key = zyte._load_env(ROOT)
    if not api_key:
        raise RuntimeError("ZYTE_API_KEY is missing")
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(check, link, api_key): link for link in missing}
        for future in as_completed(futures):
            result = future.result()
            existing[result["url"]] = result
            print(result.get("status", result.get("error", "error")), result["url"][:105], flush=True)
    for key, value in selected.items():
        value["results"] = [existing.get(item["url"], {**item, "error": "not checked"}) for item in value["targets"]]
        value["source"] = "Zyte browser direct destination visits; source HTML locked by SHA-256"
        (target_dir / f"{key}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
