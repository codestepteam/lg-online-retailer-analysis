"""Save local evidence for Momoshop PDP candidates and TP shop representatives.

Read-only public GET requests. Re-running skips already saved response records.
"""

import csv
import gzip
import json
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from lxml import html


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SOURCE = ROOT / "outputs/momoshop-search-pdp-20261103-76f0f589/unique_pdp_candidates.csv"
EVIDENCE = OUT / "pdp_evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)
BRANDS = ("PANASONIC", "WHIRLPOOL", "HITACHI", "SANLUX", "LG")
_pace_lock = Lock()
_next_request = 0.0


def search_urls():
    with SOURCE.open(encoding="utf-8-sig", newline="") as file:
        return {row["candidate_key"]: row["first_search_url"] for row in csv.DictReader(file)}


SEARCH_URLS = search_urls()


def brand_from_title(title):
    bracket = re.match(r"^\s*【([^】]+)】", title or "")
    first = (bracket.group(1) if bracket else title or "").strip().upper()
    for brand in BRANDS:
        if re.match(r"^" + brand + r"(?=$|[^A-Z0-9])", first):
            return brand
    return ""


def jobs():
    with SOURCE.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    goods = [r for r in rows if r["page_type"] == "momo_goods" and brand_from_title(r["first_name"])]
    stores = {}
    for row in rows:
        if row["page_type"] != "TP_shop" or not brand_from_title(row["first_name"]):
            continue
        match = re.search(r"/TP/(TP\d+)/", row["canonical_url"])
        if match:
            stores.setdefault(match.group(1), row)
    return [("goods", r["candidate_key"].split(":", 1)[1], r["canonical_url"]) for r in goods] + [
        ("shop", store, row["canonical_url"]) for store, row in stores.items()
    ]


def fetch(url):
    global _next_request
    with _pace_lock:
        now = time.monotonic()
        wait = _next_request - now
        if wait > 0:
            time.sleep(wait)
        _next_request = time.monotonic() + 0.6
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25) as response:
        return response.status, response.url, response.read()


def parse(status, final_url, body):
    doc = html.fromstring(body)
    scripts = doc.xpath('//script[@type="application/ld+json"]')
    graph = []
    for script in scripts:
        try:
            item = json.loads(script.text or "")
            graph.extend(item.get("@graph", []))
        except json.JSONDecodeError:
            pass
    breadcrumb = next((x for x in graph if x.get("@type") == "BreadcrumbList"), {})
    product = next((x for x in graph if x.get("@type") in ("ProductGroup", "Product")), {})
    variants = product.get("hasVariant", []) or [product]
    offers = [v.get("offers", {}) for v in variants]
    source = body.decode("utf-8", "replace")
    stock = re.search(r'\\"goodsStock\\":\\"([^\\"]*)\\"', source)
    title = doc.xpath("//title/text()")
    keywords = doc.xpath('//meta[@name="keywords"]/@content')
    description = doc.xpath('//meta[@name="description"]/@content')
    return {
        "http_status": status, "final_url": final_url,
        "title": title[0].strip() if title else "",
        "meta_keywords": keywords[0] if keywords else "",
        "meta_description": description[0] if description else "",
        "breadcrumb": [x.get("name", "") for x in breadcrumb.get("itemListElement", [])],
        "schema_product_type": product.get("@type", ""),
        "schema_name": product.get("name", ""),
        "schema_brand": (product.get("brand") or {}).get("name", "") if isinstance(product.get("brand"), dict) else product.get("brand", ""),
        "schema_sku": product.get("sku", ""),
        "conditions": sorted({x.get("itemCondition", "") for x in offers if x.get("itemCondition")}),
        "availability": sorted({x.get("availability", "") for x in offers if x.get("availability")}),
        "offer_prices": [x.get("price") for x in offers if x.get("price")],
        "goods_stock": stock.group(1) if stock else "",
        "visible_store_marker": "商店" in doc.xpath("string(//body)")[:100],
    }


def inspect(kind, key, url):
    stem = f"{kind}-{key}"
    result_file = EVIDENCE / f"{stem}.json"
    if result_file.exists():
        record = json.loads(result_file.read_text(encoding="utf-8"))
    else:
        record = {"kind": kind, "key": key, "request_url": url, "error": ""}
        for attempt in range(3):
            try:
                status, final_url, body = fetch(url)
                record.update(parse(status, final_url, body))
                (EVIDENCE / f"{stem}.html.gz").write_bytes(gzip.compress(body, compresslevel=6))
                break
            except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError) as exc:
                record["error"] = f"{type(exc).__name__}: {exc}"
                if isinstance(exc, HTTPError):
                    record["http_status"] = exc.code
                if attempt < 2:
                    time.sleep(1 + attempt)
    if kind == "goods" and not record.get("schema_product_type") and not record.get("fallback_checked_url"):
        fallback_url = SEARCH_URLS.get(f"goods:{key}")
        if fallback_url and fallback_url != url:
            record["fallback_checked_url"] = fallback_url
            try:
                status, final_url, body = fetch(fallback_url)
                parsed = parse(status, final_url, body)
                record["fallback_product_found"] = bool(parsed.get("schema_product_type"))
                if parsed.get("schema_product_type"):
                    html_path = EVIDENCE / f"{stem}.html.gz"
                    if html_path.exists():
                        shutil.copyfile(html_path, EVIDENCE / f"{stem}.canonical.html.gz")
                    record["canonical_failure_title"] = record.get("title", "")
                    record["canonical_failure_url"] = record.get("final_url", "")
                    record.update(parsed)
                    record["request_url"] = fallback_url
                    record["fallback_used"] = True
                    html_path.write_bytes(gzip.compress(body, compresslevel=6))
            except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError) as exc:
                record["fallback_error"] = f"{type(exc).__name__}: {exc}"
    if record.get("schema_product_type") or kind == "shop":
        record["error"] = "" if record.get("http_status") == 200 else record["error"]
    result_file.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


def main():
    todo = jobs()
    print(f"jobs={len(todo)} goods={sum(x[0]=='goods' for x in todo)} shops={sum(x[0]=='shop' for x in todo)}", flush=True)
    errors = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for n, future in enumerate(as_completed([pool.submit(inspect, *job) for job in todo]), 1):
            record = future.result()
            if record.get("error"):
                errors.append((record["kind"], record["key"], record["error"]))
            if n % 50 == 0 or n == len(todo):
                print(f"completed={n}/{len(todo)} errors={len(errors)}", flush=True)
    (OUT / "inspect_summary.json").write_text(json.dumps({"jobs": len(todo), "errors": errors}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
