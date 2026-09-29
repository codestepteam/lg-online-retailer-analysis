#!/usr/bin/env python3
"""Check category-card destinations still unreviewed in the 159-row batch."""

from __future__ import annotations

import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from lxml import html

from capture_bcp_population import ROOT
from check_failed_links_direct import check
import zyte_capture as zyte


BATCH = ROOT / "results_population" / "20260928-all-159"
RETAILERS = {"alza", "coolblue", "elgiganten", "amazon-it"}


def targets_for(record: dict, tree: html.HtmlElement) -> list[dict]:
    row, brand, retailer = int(record["sourceRow"]), str(record["brand"]), str(record["retailerSlug"])
    if retailer == "amazon-it" and row not in {66, 67}:
        return []
    anchors = []
    if retailer == "alza":
        if row in {4, 9, 13, 18}:
            return []
        evidence = json.loads((BATCH / "parsed" / record["pageKey"] / "bcp-evidence.json").read_text())
        links = evidence["metrics"]["ID21"]["evidence"]["linkCandidates"]
        response = json.loads((BATCH / "pages" / record["pageKey"] / "brand-category" / "response.json").read_text())
        final_url = str(response.get("final_url") or "")
        for link in links:
            label, url = str(link.get("text") or ""), str(link.get("href") or "")
            if label.startswith("Vše od"):
                break
            if url.rstrip("/") in {str(record["url"]).rstrip("/"), final_url.rstrip("/")} or re.search(r"/v\d+\.htm$", url):
                continue
            if re.search(r"-d\d+\.htm", url):
                continue
            anchors.append((label, url))
    elif retailer == "coolblue":
        for anchor in tree.xpath('//a[contains(@class,"hb-1dtiqm5")][@href]'):
            label = " ".join(" ".join(anchor.itertext()).split())
            url = urljoin(record["url"], anchor.get("href"))
            if brand.casefold() in label.casefold() and "/advies/" not in url:
                anchors.append((label, url))
    elif retailer == "elgiganten":
        for anchor in tree.xpath('//article[contains(@class,"cms-module-container")]//a[@href]'):
            css = anchor.get("class", "")
            if not (css.startswith("flex snap-start") or css.startswith("grid grid-cols")):
                continue
            label = " ".join(" ".join(anchor.itertext()).split())
            url = urljoin(record["url"], anchor.get("href"))
            if f"/brand/{brand.casefold()}/" in urlsplit(url).path.casefold():
                anchors.append((label, url))
    else:
        for anchor in tree.xpath('//div[contains(@class,"EditorialTile__content")]//a[contains(@href,"/stores/page/")]'):
            anchors.append(("브랜드 매장 제품군 카드", urljoin(record["url"], anchor.get("href"))))
    unique = {}
    for label, url in anchors:
        unique[url] = {"kind": "navigator", "label": label[:150], "url": url}
    return list(unique.values())


def main() -> None:
    records = json.loads((BATCH / "manifest.json").read_text())["records"]
    target = BATCH / "navigator-sidebar-check"
    target.mkdir(exist_ok=True)
    selected, unique = {}, {}
    for record in records:
        if record["retailerSlug"] not in RETAILERS or record["pageType"] != "Brand Category Page" or record["brand"] == "LG":
            continue
        if record["retailerSlug"] == "amazon-it" and int(record["sourceRow"]) not in {66, 67}:
            continue
        page = BATCH / "pages" / record["pageKey"] / "brand-category"
        raw = (page / "raw.html").read_bytes()
        links = targets_for(record, html.fromstring(raw))
        selected[record["pageKey"]] = {"sourceWorkbookRow": record["sourceRow"], "brand": record["brand"],
                                       "sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(), "targets": links}
        for link in links:
            unique[link["url"]] = link
    existing = {}
    for path in target.glob("*.json"):
        for result in json.loads(path.read_text()).get("results", []):
            if result.get("status") == 200:
                existing[result["url"]] = result
    api_key = zyte._load_env(ROOT)
    if not api_key:
        raise RuntimeError("ZYTE_API_KEY is missing")
    missing = [link for url, link in unique.items() if url not in existing]
    print(f"pages={len(selected)} links={len(unique)} to-check={len(missing)}", flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(check, link, api_key): link for link in missing}
        for future in as_completed(futures):
            result = future.result()
            existing[result["url"]] = result
            print(result.get("status", result.get("error", "error")), result["url"][:130], result.get("title", "")[:70], flush=True)
    for key, value in selected.items():
        value["results"] = [existing.get(link["url"], {**link, "error": "not checked"}) for link in value["targets"]]
        value["source"] = "Zyte direct destination visits; source HTML locked by SHA-256"
        (target / f"{key}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
