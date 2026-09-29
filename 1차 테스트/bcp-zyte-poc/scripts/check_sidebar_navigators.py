#!/usr/bin/env python3
"""Verify every category link in the visible MediaWorld/MediaMarkt sidebar."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin

from lxml import html as lxml_html

from capture_bcp_population import ROOT
from check_failed_links_direct import check
import zyte_capture as zyte


BATCH = ROOT / "results_population" / "20260928-all-159"
RETAILERS = {"mediaworld", "mediamarkt-es"}


def main() -> None:
    records = json.loads((BATCH / "manifest.json").read_text())["records"]
    target = BATCH / "navigator-sidebar-check"
    target.mkdir(exist_ok=True)
    selected = {}
    unique = {}
    for record in records:
        if record["retailerSlug"] not in RETAILERS or record["pageType"] != "Brand Category Page" or record["brand"] == "LG":
            continue
        key = record["pageKey"]
        page = BATCH / "pages" / key / "brand-category"
        tree = lxml_html.fromstring((page / "raw.html").read_bytes())
        headings = [node for node in tree.xpath("//h3") if " ".join(node.itertext()).strip() in {"Categorie", "Categorías"}]
        links = []
        if headings:
            for anchor in headings[0].getparent().xpath(".//a[@href]"):
                url = urljoin(record["url"], anchor.get("href"))
                link = {"kind": "navigator", "label": " ".join(anchor.itertext()).strip(), "url": url}
                links.append(link)
                unique[url] = link
        selected[key] = {"sourceWorkbookRow": record["sourceRow"], "brand": record["brand"],
                         "sourceRawHtmlSha256": __import__("hashlib").sha256((page / "raw.html").read_bytes()).hexdigest(),
                         "targets": links}
    existing = {}
    for path in target.glob("*.json"):
        for result in json.loads(path.read_text()).get("results", []):
            if result.get("status") == 200:
                existing[result["url"]] = result
    api_key = zyte._load_env(ROOT)
    if not api_key:
        raise RuntimeError("ZYTE_API_KEY is missing")
    missing = [link for url, link in unique.items() if url not in existing]
    print(f"pages={len(selected)} links={len(unique)} retry={len(missing)}", flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(check, link, api_key): link for link in missing}
        for future in as_completed(futures):
            result = future.result()
            existing[result["url"]] = result
            print(result.get("status", result.get("error")), result["url"], result.get("title", "")[:50], flush=True)
    for key, value in selected.items():
        value["results"] = [existing.get(link["url"], {**link, "error": "not checked"}) for link in value["targets"]]
        value["source"] = "Zyte direct destination visits"
        (target / f"{key}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
