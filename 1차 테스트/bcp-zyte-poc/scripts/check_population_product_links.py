#!/usr/bin/env python3
"""Visit the first two distinct same-brand product-card URLs on each saved BCP."""

from __future__ import annotations

import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit

from capture_bcp_population import ROOT, prepared_recipe
from check_bcp_links import browser_script
from assess_full_population import source_conflicts, redirected_brand_issues
import zyte_capture as zyte


PRODUCT_PATHS = ("/product/", "/products/", "/produkt/", "/produit/", "/prodotto/", "/ref/", "/dp/")


def is_product_url(url: str, retailer: str) -> bool:
    path = urlsplit(url).path.casefold()
    if any(part in path for part in PRODUCT_PATHS):
        return True
    if retailer == "alza" and bool(re.search(r"-d\d+\.htm$", path)):
        return True
    if retailer == "datart" and bool(re.search(r"/(?:automaticka-|pracka-|susicka-|chladnicka-|lednice-|americka-lednice-|mrazak-|mraznicka-|mycka-|mycka-nadobi-)[^/]+", path)):
        return True
    return False


def selected_links(record: dict, state: dict) -> list[dict[str, str]]:
    host = urlsplit(str(record["url"])).hostname
    brand = str(record["brand"])
    retailer = str(record["retailerSlug"])
    selected, seen = [], set()
    for item in state.get("clickables", []):
        url = str(item.get("href") or "")
        parsed = urlsplit(url)
        if not url or parsed.hostname != host or not is_product_url(url, retailer):
            continue
        if retailer == "datart" and (parsed.fragment or not re.search(
            rf"-{re.escape(brand.casefold())}-[a-z0-9]*\d", parsed.path.casefold()
        )):
            continue
        label = str(item.get("text") or item.get("ariaLabel") or "")
        if not re.search(r"(?<![A-Za-z])" + re.escape(brand) + r"(?![A-Za-z])", label + " " + parsed.path, re.I):
            continue
        stable = parsed._replace(query="", fragment="").geturl()
        if stable in seen:
            continue
        seen.add(stable)
        selected.append({"kind": "product", "label": label[:180], "url": url})
        if len(selected) == 2:
            break
    return selected


def check_page(batch: Path, record: dict, api_key: str) -> tuple[str, dict]:
    key = str(record["pageKey"])
    state = json.loads((batch / "pages" / key / "brand-category" / "capture-state.json").read_text())
    selected = selected_links(record, state)
    if not selected:
        return key, {"pageKey": key, "targets": [], "results": [], "error": "상품 카드 링크를 선택하지 못함"}
    _, request = prepared_recipe(record)
    request["screenshot"] = False
    request.pop("screenshotOptions", None)
    script = browser_script(selected)
    if len(script.encode()) > 6000:
        raise ValueError(f"Zyte evaluate action exceeds 6000 bytes: {key}")
    request["actions"].append({"action": "evaluate", "source": script})
    try:
        response = zyte._post_json(api_key, request, 180, 1)
        html = str(response.get("browserHtml") or "")
        match = re.search(r'<script id="lg-link-check" type="application/json">(.*?)</script>', html, re.S)
        if not match:
            raise ValueError("링크 검사 결과가 HTML에 없음")
        return key, {"pageKey": key, "targets": selected, "results": json.loads(match.group(1)),
                     "source": "Zyte browser same-origin fetch", "sourcePageStatus": response.get("statusCode"),
                     "coverage": "first two distinct same-brand product cards"}
    except Exception as exc:
        return key, {"pageKey": key, "targets": selected, "results": [], "error": str(exc),
                     "coverage": "first two distinct same-brand product cards"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--only-row", type=int, action="append")
    parser.add_argument("--skip-seeded", action="store_true", help="reuse the prior LG page link checks separately")
    parser.add_argument("--force", action="store_true", help="recheck selected rows after recapture")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    batch = args.batch.resolve()
    all_records = json.loads((batch / "manifest.json").read_text())["records"]
    identity_issues = {**source_conflicts(batch, all_records), **redirected_brand_issues(batch, all_records)}
    records = [record for record in all_records
               if record["pageType"] == "Brand Category Page"
               and record["collectionStatus"] in ("captured", "reused", "seeded")
               and (not args.skip_seeded or record["collectionStatus"] != "seeded")
               and int(record["sourceRow"]) not in identity_issues
               and (not args.only_row or int(record["sourceRow"]) in args.only_row)]
    target = batch / "product-link-check"
    target.mkdir(exist_ok=True)
    if not args.force:
        records = [record for record in records if not (target / f"{record['pageKey']}.json").is_file()]
    if args.dry_run:
        for record in records:
            state = json.loads((batch / "pages" / record["pageKey"] / "brand-category" / "capture-state.json").read_text())
            print(record["pageKey"], selected_links(record, state))
        return
    api_key = zyte._load_env(ROOT)
    if not api_key:
        raise RuntimeError("ZYTE_API_KEY is missing")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check_page, batch, record, api_key): record for record in records}
        for future in as_completed(futures):
            key, result = future.result()
            (target / f"{key}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print(key, len(result["targets"]), [item.get("status", item.get("error")) for item in result["results"]], result.get("error", ""), flush=True)


if __name__ == "__main__":
    main()
