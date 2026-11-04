"""Collect Momoshop search-card candidates from public HTML, without a paid API.

The site embeds 12 search products per page as JSON-LD. This captures that
server response, which can differ from the browser's client-rendered ad order.
"""

import csv
import json
import re
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urlsplit
from urllib.request import Request, urlopen

import openpyxl
from lxml import html


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = next((ROOT / "관련문서").glob("*v2.2_20261023*"))
SHEET = "Search Term"
BASE = "https://www.momoshop.com.tw/search/"
UA = "Mozilla/5.0"
LIMIT = 1000
PAGE_SIZE = 12
PACE_SECONDS = 0.55
_pace_lock = Lock()
_next_request = 0.0


def source_keywords():
    sheet = openpyxl.load_workbook(SOURCE, read_only=True, data_only=True)[SHEET]
    kept, skipped = [], []
    for n in range(294, 309):
        if (sheet.cell(n, 2).value, sheet.cell(n, 3).value, sheet.cell(n, 4).value) != (
            "TW", "Taiwan", "Momoshop"
        ):
            raise ValueError(f"unexpected source row {n}")
        original, proposal, flag = (sheet.cell(n, c).value for c in (10, 13, 14))
        term = original
        if flag and not str(flag).startswith("영문 번역 오류"):
            if proposal == "제외":
                skipped.append({"source_row": n, "j_keyword": original, "reason": flag})
                continue
            term = proposal
        kept.append({"source_row": n, "category": sheet.cell(n, 6).value,
                     "j_keyword": original, "search_keyword": term,
                     "review_flag": flag, "review_proposal": proposal})
    if len(kept) != 11 or {r["source_row"] for r in skipped} != {295, 296, 297, 299}:
        raise ValueError("reviewed Momoshop keyword scope changed")
    return kept, skipped


def _paced_fetch(url):
    global _next_request
    with _pace_lock:
        now = time.monotonic()
        wait = _next_request - now
        if wait > 0:
            time.sleep(wait)
        _next_request = time.monotonic() + PACE_SECONDS
    with urlopen(Request(url, headers={"User-Agent": UA}), timeout=25) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}")
        return response.read()


def parse_page(body, keyword, page):
    root = html.fromstring(body)
    scripts = root.xpath('//script[@type="application/ld+json"]')
    if len(scripts) != 1:
        raise ValueError(f"page {page}: JSON-LD scripts={len(scripts)}")
    document = json.loads(scripts[0].text)
    lists = [x for x in document.get("@graph", []) if x.get("@type") == "ItemList"]
    if len(lists) != 1:
        raise ValueError(f"page {page}: ItemList count={len(lists)}")
    products = lists[0].get("itemListElement", [])
    if len(products) > PAGE_SIZE:
        raise ValueError(f"page {page}: too many cards={len(products)}")
    raw = body.decode("utf-8", "replace")
    matches = re.findall(r'\\"maxPage\\":(\d+)', raw)
    max_page = int(matches[0]) if matches else None
    cards = []
    for item in products:
        url = (item.get("url") or "").strip()
        if urlsplit(url).netloc != "www.momoshop.com.tw":
            raise ValueError(f"page {page}: off-site product URL")
        name = item.get("name", "")
        if not url or not name:
            raise ValueError(f"page {page}: incomplete product")
        query = parse_qs(urlsplit(url).query)
        product_id = query.get("i_code", [""])[0]
        if not product_id:
            product = re.fullmatch(r"/product/(\d+)/?", urlsplit(url).path)
            product_id = product.group(1) if product else ""
        cards.append({"page": page, "position": item.get("position"), "product_id": product_id,
                      "name": name, "product_url": url, "search_keyword": keyword,
                      "availability": item.get("offers", {}).get("availability", "")})
    return cards, max_page


def collect_one(entry, resume=False):
    keyword = entry["search_keyword"]
    source_row = entry["source_row"]
    base = BASE + quote(keyword, safe="") + "?cateLevel=0&_isFuzzy=0&searchType=1"
    target = OUT / f"source-{source_row}.jsonl"
    lines = [json.loads(line) for line in target.read_text(encoding="utf-8").splitlines()] if resume and target.exists() else []
    max_page = lines[0].get("response_page_max") if lines else None
    start_page = max((line["page"] for line in lines), default=0) + 1
    error = None
    page_limit = (LIMIT + PAGE_SIZE - 1) // PAGE_SIZE
    for page in range(start_page, page_limit + 1):
        url = base + (f"&curPage={page}" if page > 1 else "")
        try:
            for attempt in range(3):
                try:
                    body = _paced_fetch(url)
                    cards, reported_max = parse_page(body, keyword, page)
                    break
                except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError):
                    if attempt == 2:
                        raise
                    time.sleep(1 + attempt)
            if max_page is None:
                max_page = reported_max
            elif reported_max is not None and max_page != reported_max:
                # Search rankings change during long collections; preserve all snapshots.
                pass
            for card in cards:
                card.update(source_row=source_row, category=entry["category"],
                            response_url=url, response_page_max=reported_max,
                            rank_by_response=(page - 1) * PAGE_SIZE + int(card["position"]))
                if card["rank_by_response"] <= LIMIT:
                    lines.append(card)
            target.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in lines), encoding="utf-8")
            if page % 10 == 0 or len(cards) < PAGE_SIZE:
                print(f"row {source_row} {keyword}: page {page}, cards {len(lines)}", flush=True)
            if not cards or len(cards) < PAGE_SIZE or (max_page and page >= max_page):
                break
        except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError) as exc:
            error = f"{type(exc).__name__}: {exc}"
            print(f"row {source_row} {keyword}: page {page} FAILED: {error}", flush=True)
            break
    return {**entry, "pages_fetched": page, "cards": len(lines), "reported_max_page": max_page,
            "error": error, "source_file": target.name}


def main():
    keywords, skipped = source_keywords()
    (OUT / "keywords.json").write_text(json.dumps({"source": str(SOURCE), "sheet": SHEET,
        "limit_per_keyword": LIMIT, "kept": keywords, "skipped": skipped}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    if "--dry-run" in sys.argv:
        print(json.dumps({"keywords": len(keywords), "excluded": len(skipped),
                          "terms": [(r["source_row"], r["search_keyword"]) for r in keywords]},
                         ensure_ascii=False))
        return
    if "--resume" in sys.argv:
        old = json.loads((OUT / "summary.json").read_text(encoding="utf-8"))
        results_by_row = {r["source_row"]: r for r in old["keywords"]}
        pending = [entry for entry in keywords if results_by_row[entry["source_row"]]["error"]]
    else:
        results_by_row = {}
        pending = keywords
    with ThreadPoolExecutor(max_workers=2) as pool:
        for future in as_completed([pool.submit(collect_one, entry, "--resume" in sys.argv) for entry in pending]):
            result = future.result()
            results_by_row[result["source_row"]] = result
            print(f"DONE row {result['source_row']}: {result['cards']} cards, error={result['error']}", flush=True)
    results = list(results_by_row.values())
    results.sort(key=lambda x: x["source_row"])
    all_cards = []
    for result in results:
        path = OUT / result["source_file"]
        if path.exists():
            all_cards.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
    with (OUT / "search_cards.csv").open("w", encoding="utf-8-sig", newline="") as f:
        cols = ["source_row", "category", "search_keyword", "page", "position", "rank_by_response",
                "product_id", "name", "product_url", "availability", "response_url", "response_page_max"]
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows({k: row.get(k, "") for k in cols} for row in all_cards)
    candidates = {}
    occurrences = defaultdict(list)
    for card in all_cards:
        source_url = card["product_url"].strip()
        path = urlsplit(source_url).path
        if card["product_id"]:
            key = "goods:" + card["product_id"]
            canonical_url = BASE.replace("/search/", "/product/") + card["product_id"]
            page_type = "momo_goods"
        else:
            key = "path:" + path
            canonical_url = "https://www.momoshop.com.tw" + path
            page_type = "TP_shop"
        if key not in candidates:
            candidates[key] = {"candidate_key": key, "page_type": page_type,
                               "canonical_url": canonical_url, "first_search_url": source_url,
                               "first_name": card["name"]}
        occurrences[key].append(card)
    with (OUT / "unique_pdp_candidates.csv").open("w", encoding="utf-8-sig", newline="") as f:
        cols = ["candidate_key", "page_type", "canonical_url", "first_search_url", "first_name",
                "search_hits", "keyword_rows", "keywords", "best_rank", "review_status"]
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for key, record in candidates.items():
            hits = occurrences[key]
            writer.writerow({**record, "search_hits": len(hits),
                             "keyword_rows": ",".join(str(x) for x in sorted({h["source_row"] for h in hits})),
                             "keywords": " | ".join(dict.fromkeys(h["search_keyword"] for h in hits)),
                             "best_rank": min(h["rank_by_response"] for h in hits),
                             "review_status": "brand/category/seller/PDP verification pending"})
    ids = Counter(x["product_id"] for x in all_cards if x["product_id"])
    report = {"collection_method": "public server HTML JSON-LD, not browser-rendered result",
              "browser_pilot": "2026-11-03 same-page in-app browser comparison: 冰箱 pages 3 and 84, 乾衣機 and 洗衣機 page 1;"
                               " each had 12/12 matching card names, URLs, and order between visible screen and JSON-LD."
                               " An earlier different-request comparison was invalid because ads can change between requests.",
              "source": str(SOURCE), "keywords": results, "excluded_source_rows": skipped,
              "total_cards": len(all_cards), "unique_numeric_product_ids": len(ids),
              "unique_pdp_candidates": len(candidates),
              "unique_momo_goods": sum(x["page_type"] == "momo_goods" for x in candidates.values()),
              "unique_TP_shop": sum(x["page_type"] == "TP_shop" for x in candidates.values()),
              "blank_numeric_product_ids": sum(not x["product_id"] for x in all_cards),
              "duplicate_numeric_product_id_occurrences": sum(n - 1 for n in ids.values()),
              "failed_keywords": [x for x in results if x["error"]]}
    (OUT / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("total_cards", "unique_numeric_product_ids",
                                            "blank_numeric_product_ids", "duplicate_numeric_product_id_occurrences")},
                     ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
