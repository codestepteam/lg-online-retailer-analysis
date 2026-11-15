"""Rebuild the one-off Momoshop population from locally saved browser observations."""

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
PREVIOUS_SEARCH = OUT.parent / "momoshop-search-pdp-20261103-76f0f589"
PREVIOUS_FINAL = OUT.parent / "momoshop-final-pdp-20261103-51e01084"
EVIDENCE = OUT / "pdp_evidence"
LIMIT = 1000
SITE = "https://www.momoshop.com.tw"
sys.path.insert(0, str(PREVIOUS_FINAL))
import finalize as previous
import momo_checks

previous.EVIDENCE = EVIDENCE
load_evidence = previous.read_evidence


def legacy_evidence(kind, identity):
    evidence, path = load_evidence(kind, identity)
    # The old judge uses 200 as its gate. Here the gate is verified browser content.
    # The browser observation does not expose an HTTP code.
    return {**evidence, "http_status": 200 if evidence.get("verified") else ""}, path


previous.read_evidence = legacy_evidence


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def product_key(url):
    parsed = urlsplit(url)
    if parsed.netloc != "www.momoshop.com.tw":
        raise ValueError(f"Off-site product link: {url}")
    store = re.search(r"^/TP/(TP\d+)/", parsed.path)
    if store:
        return "path:" + parsed.path, "TP_shop", SITE + parsed.path, store.group(1)
    direct = re.fullmatch(r"/product/(\d+)/?", parsed.path)
    identifier = direct.group(1) if direct else parse_qs(parsed.query).get("i_code", [""])[0]
    if not identifier.isdigit():
        raise ValueError(f"Missing product identifier: {url}")
    return "goods:" + identifier, "momo_goods", SITE + "/product/" + identifier, identifier


def search_inputs():
    terms = json.loads((PREVIOUS_SEARCH / "keywords.json").read_text())["kept"]
    report, cards, failures = [], [], []
    for entry in terms:
        source_row = entry["source_row"]
        files = {int(path.stem.rsplit("-", 1)[1]): path for path in (OUT / "pages").glob(f"search-{source_row}-*.json")}
        rank, last, reported = 0, 0, 1
        for page in range(1, max(files, default=1) + 1):
            if page not in files:
                failures.append({"row": source_row, "page": page, "reason": "응답 자료 없음"})
                continue
            doc = json.loads(files[page].read_text())
            if page == 1 and doc["nav"]:
                reported = doc["nav"][1]
            last = page
            if not doc["matched"] or (doc["nav"] and doc["nav"][0] != page and not doc.get("empty_verified")):
                failures.append({"row": source_row, "page": page, "reason": "화면과 상품 목록 대조 실패"})
                continue
            for position, name, url, availability in doc["cards"]:
                rank += 1
                if rank > LIMIT:
                    break
                key, page_type, canonical, identity = product_key(url)
                cards.append({
                    "source_row": source_row, "category": entry["category"], "search_keyword": entry["search_keyword"],
                    "page": page, "position": position, "rank_by_response": rank,
                    "product_id": identity if page_type == "momo_goods" else "", "name": name,
                    "product_url": url, "availability": availability, "response_url": doc["url"],
                    "response_page_max": reported, "candidate_key": key, "page_type": page_type,
                    "canonical_url": canonical, "identity": identity,
                })
            if rank >= LIMIT:
                break
        if rank < LIMIT and last < reported:
            failures.append({"row": source_row, "page": last + 1, "reason": "사이트가 표시한 다음 페이지의 자료 없음"})
        report.append({"row": source_row, "keyword": entry["search_keyword"], "pages": last,
                       "reported_pages": reported, "cards": min(rank, LIMIT)})
    return report, cards, failures


def prepare():
    report, cards, failures = search_inputs()
    first = {}
    for row in cards:
        first.setdefault(row["candidate_key"], row)
    jobs = {}
    for row in first.values():
        if not previous.brand_from_title(row["name"]):
            continue
        kind = "goods" if row["page_type"] == "momo_goods" else "shop"
        key = row["identity"]
        jobs.setdefault((kind, key), [kind, key, row["canonical_url"], row["product_url"]])
    write_json(OUT / "jobs.json", list(jobs.values()))
    write_json(OUT / "search_summary.json", {"keywords": report, "failures": failures, "cards": len(cards),
                                             "unique_candidates": len(first), "detail_checks": len(jobs)})
    previous.write_csv(OUT / "search_cards.csv", cards, list(cards[0]))
    print(json.dumps({"cards": len(cards), "unique_candidates": len(first), "detail_checks": len(jobs),
                      "detail_by_kind": dict(Counter(kind for kind, _ in jobs)), "search_failures": failures}, ensure_ascii=False))


def sharing_v7():
    return next((ROOT / "pdp 모수 추출").rglob("*공유용_v7*.csv"))


def comparison(selected):
    old = read_csv(PREVIOUS_FINAL / "final_pdp_urls.csv")
    v7_file = sharing_v7()
    momo_v7 = [r for r in read_csv(v7_file) if r["리테일러"].upper() == "MOMOSHOP" and r["국가"] == "Taiwan"]
    v7 = [r for r in momo_v7 if r["모수 포함 여부"] == "포함"]
    current_keys = {r["candidate_key"] for r in selected}
    old_keys = {r["candidate_key"] for r in old}
    v7_keys = {product_key(r["확인 요청 URL"])[0] for r in v7}
    return {"nov03_included": len(old_keys), "nov03_same_product": len(old_keys & current_keys),
            "nov03_new_product": len(current_keys - old_keys), "nov03_missing_product": len(old_keys - current_keys),
            "v7_source": v7_file.name, "v7_all_rows": len(momo_v7), "v7_included": len(v7),
            "v7_included_unique_product": len(v7_keys), "v7_same_product": len(v7_keys & current_keys),
            "v7_new_product": len(current_keys - v7_keys), "v7_missing_product": len(v7_keys - current_keys)}


def write_sharing_csv(cards, by_key):
    with sharing_v7().open(encoding="utf-8-sig", newline="") as source:
        fields = next(csv.reader(source))
    categories = {"Dryer": "DRY", "Refrigerator": "REF", "Washing Machine": "W/M"}
    rows, first_included = [], {}
    for index, card in enumerate(cards, 1):
        key = card["candidate_key"]
        candidate = by_key[key]
        if card["decision"] == "포함":
            first_included[key] = index
        duplicate_of = first_included.get(key) if card["exclusion_stage"] == "④중복" else None
        evidence, _ = load_evidence("shop", card["identity"]) if card["page_type"] == "TP_shop" else ({}, "")
        seller = candidate["seller"]
        seller_type = "직판 추정" if seller == "momo (추정)" else ""
        if seller == "입점 상점" and evidence.get("verified"):
            seller = evidence["meta_keywords"].rsplit(",", 1)[-1].strip()
            seller_type = "입점 상점"
        checked = candidate["page_check"] == "상세 표시"
        rows.append({
            "행번호": index, "흐름": "검색", "국가": "Taiwan", "리테일러": "MOMOSHOP",
            "제품군": categories[card["category"]], "브랜드": card["brand"], "상품명": card["name"],
            "확인 요청 URL": card["product_url"], "원본 상품 URL": card["product_url"],
            "기준일": "2026-11-12", "검색어": card["search_keyword"], "엑셀행번호": card["source_row"],
            "출처파일": "search_cards.csv", "모수 포함 여부": card["decision"], "제외단계": card["exclusion_stage"],
            "제외사유": f"같은 상품(대표 행 {duplicate_of})" if duplicate_of else card["reason"],
            "페이지 접속 확인 결과": "정상" if checked else candidate["page_check"],
            "접속 후 URL": candidate["final_url"] if checked else "",
            "판매자": seller, "판매자구분": seller_type, "판매자근거": candidate["seller_basis"],
        })
    assert len(fields) == 26
    assert all(set(row) <= set(fields) for row in rows)
    previous.write_csv(OUT / "momoshop_all_judgments_26_columns.csv", rows, fields)


def judge():
    cards = read_csv(OUT / "search_cards.csv")
    jobs = json.loads((OUT / "jobs.json").read_text())
    brands, keywords = previous.rules()
    hits = defaultdict(list)
    for card in cards:
        hits[card["candidate_key"]].append(card)
    results, verified, audit = [], set(), []
    for key, rows in hits.items():
        first = rows[0]
        result = previous.judge({**first, "first_name": first["name"]}, rows, brands, keywords)
        kind = "goods" if first["page_type"] == "momo_goods" else "shop"
        evidence, _ = load_evidence(kind, first["identity"])
        result["http_status"] = evidence.get("http_status") or ""
        result["page_check"] = ("상세 표시" if evidence.get("schema_name") else "상점 표시" if kind == "shop" else "상품 없음 표시") if evidence.get("verified") else ""
        if previous.brand_from_title(first["name"]) and not evidence.get("verified"):
            result.update(decision="검토 필요", exclusion_stage="④페이지확인",
                          reason=evidence.get("error") or "상품 상세 확인 결과 없음")
        if result["decision"] == "포함":
            signals = momo_checks.inspect(first["identity"], result["product_name"])
            momo_checks.apply(result, signals)
            audit.append({"candidate_key": key, "url": result["final_url"], "title": result["product_name"],
                          "decision": result["decision"], "reason": result["reason"],
                          "search_availability": sorted({row["availability"] for row in rows if row["availability"]}),
                          **signals})
        if result["decision"] == "포함" and result["final_url"] in verified:
            result.update(decision="제외", exclusion_stage="④중복", reason="상세 도착 주소 중복")
        if result["decision"] == "포함":
            verified.add(result["final_url"])
        results.append(result)

    by_key = {row["candidate_key"]: row for row in results}
    represented, card_judgments = set(), []
    for card in cards:
        key = card["candidate_key"]
        base = by_key[key]
        row = {**card, **{f: base[f] for f in ("final_url", "brand", "product_categories", "decision", "exclusion_stage", "reason")}}
        if base["decision"] == "포함":
            if key in represented:
                row.update(decision="제외", exclusion_stage="④중복", reason="같은 상품의 다른 검색어·페이지 카드")
            represented.add(key)
        card_judgments.append(row)
    selected = [row for row in results if row["decision"] == "포함"]
    review = [row for row in results if row["decision"] == "검토 필요"]
    fields = list(results[0])
    for name, rows in (("candidate_judgments", results), ("included_pdp_urls", selected), ("review_needed", review)):
        previous.write_csv(OUT / f"{name}.csv", rows, fields)
    previous.write_csv(OUT / "all_search_card_judgments.csv", card_judgments, list(card_judgments[0]))
    write_sharing_csv(card_judgments, by_key)
    failed = []
    for kind, identity, url, _ in jobs:
        evidence, _ = load_evidence(kind, identity)
        if not evidence.get("verified"):
            failed.append({"kind": kind, "id": identity, "url": url, "error": evidence.get("error", "확인 자료 없음")})
    write_json(OUT / "detail_failures.json", failed)
    write_json(OUT / "momo_filter_audit.json", audit)
    summary = {"cards": len(cards), "unique_candidates": len(results), "included": len(selected),
               "excluded": sum(row["decision"] == "제외" for row in results), "review_needed": len(review),
               "detail_checks": len(jobs), "failed_detail_checks": len(failed),
               "included_brands": dict(Counter(r["brand"] for r in selected)),
               "excluded_by_stage": dict(Counter(r["exclusion_stage"] for r in results if r["decision"] == "제외")),
               "momo_shop_candidates": sum(r["page_type"] == "TP_shop" for r in results),
               "momo_audit_sources": dict(Counter(r["source"] for r in audit)),
               "momo_stock_review": sum(r["stock_review"] for r in audit),
               **comparison(selected)}
    assert len(cards) == len(card_judgments)
    assert sum(r["decision"] == "포함" for r in card_judgments) == len(selected) == len(verified)
    assert summary["included"] + summary["excluded"] + summary["review_needed"] == summary["unique_candidates"]
    write_json(OUT / "final_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    {"prepare": prepare, "judge": judge}[sys.argv[1]]()
