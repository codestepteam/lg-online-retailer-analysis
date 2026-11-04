"""Apply documented PDP population rules to the Momoshop search snapshot."""

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from openpyxl import load_workbook

from inspect_pdp import OUT, ROOT, SOURCE, EVIDENCE, brand_from_title, jobs


CARDS = ROOT / "outputs/momoshop-search-pdp-20261103-76f0f589/search_cards.csv"
WORKBOOK = next((ROOT / "관련문서").glob("*v2.2_20261023*"))
REF = re.compile(r"冰箱|冰櫃|冷凍櫃|冷藏櫃|冷藏展示櫃|冷凍庫|冷藏庫")
WM = re.compile(r"洗衣機|洗衣塔|洗乾衣機|洗脫烘")
DRY = re.compile(r"乾衣機|烘衣機|烘乾機|烘乾衣機|免曬衣")
STYLER = re.compile(r"電子衣櫥|衣物護理機|Styler", re.I)
PART = re.compile(r"濾網|濾心|濾芯|底座|支架|防塵罩|保護套|連接架|連接套件|清潔劑|清潔液|排水管|進水管|延長管|配件|零件|備品")
LG_WM_REF_BUNDLE = re.compile(r"\d+\s*公斤\s*\+\s*\d+\s*公升.*\bWT-[A-Z0-9]+\+(?:GN|GV)-[A-Z0-9]+", re.I)


def rules():
    wb = load_workbook(WORKBOOK, read_only=True, data_only=True)
    brands = defaultdict(set)
    for row in wb["경쟁브랜드"].iter_rows(values_only=True):
        if len(row) > 4 and row[2] == "Taiwan" and row[3] in ("REF", "W/M") and row[4]:
            brands[row[3]].add(str(row[4]).strip().upper())
    expected = {"REF": {"PANASONIC", "HITACHI", "SANLUX", "LG"},
                "W/M": {"PANASONIC", "LG", "SANLUX", "WHIRLPOOL"}}
    if dict(brands) != expected:
        raise ValueError(f"Taiwan competitor brands changed: {dict(brands)}")
    brands["DRY"] = set(brands["W/M"])  # Prior PDP population code's documented AI interpretation.
    keywords = []
    for row in wb["제외키워드(리리부)"].iter_rows(values_only=True):
        if len(row) > 10 and row[8] == "Taiwan" and row[9] and row[10]:
            keywords.append((str(row[9]).strip(), str(row[10]).strip()))
    if len(keywords) != 16:
        raise ValueError(f"Taiwan exclusion keyword count changed: {len(keywords)}")
    return brands, keywords


def candidate_key(card):
    url = card["product_url"].strip()
    product_id = card["product_id"]
    if product_id:
        return "goods:" + product_id
    return "path:" + urlsplit(url).path


def product_categories(name, breadcrumb):
    text = name or ""
    found = set()
    if REF.search(text):
        found.add("REF")
    if WM.search(text):
        found.add("W/M")
    if DRY.search(text):
        found.add("DRY")
    # These verified models include drying even when the short title omits 乾衣機.
    # Check manufacturer evidence before adding more model-specific patterns.
    if re.search(r"洗衣塔|洗乾堆疊|NA-V(?:1715|1515)SP-", text, re.I):
        found.update(("W/M", "DRY"))
    # LG Taiwan identifies the GN/GV models in these washer bundles as refrigerators.
    if LG_WM_REF_BUNDLE.search(text):
        found.update(("REF", "W/M"))
    if not found:
        crumb = " | ".join(breadcrumb or [])
        if REF.search(crumb):
            found.add("REF")
        elif WM.search(crumb):
            found.add("W/M")
        elif DRY.search(crumb) and not STYLER.search(text):
            found.add("DRY")
    return sorted(found)


def exclusion_hit(name, keywords):
    lower = (name or "").lower()
    for typ, word in keywords:
        pattern = (r"(?<![a-z0-9])" if word[0].isascii() else "") + re.escape(word.lower())
        if re.search(pattern, lower):
            return typ, word
    return None


def read_evidence(kind, key):
    path = EVIDENCE / f"{kind}-{key}.json"
    if not path.exists():
        return {}, ""
    return json.loads(path.read_text(encoding="utf-8")), str(path.relative_to(ROOT))


def judge(candidate, hits, brands, keywords):
    name = candidate["first_name"]
    title_brand = brand_from_title(name)
    result = {"candidate_key": candidate["candidate_key"], "page_type": candidate["page_type"],
              "product_name": name, "brand": title_brand, "product_categories": "",
              "final_url": candidate["canonical_url"], "decision": "검토 필요", "exclusion_stage": "",
              "reason": "", "seller": "", "seller_basis": "", "http_status": "",
              "evidence_file": "", "source_rows": ",".join(str(n) for n in sorted({int(h["source_row"]) for h in hits})),
              "search_terms": " | ".join(dict.fromkeys(h["search_keyword"] for h in hits)),
              "search_hits": len(hits), "best_rank": min(int(h["rank_by_response"]) for h in hits)}
    if not title_brand:
        result.update(decision="제외", exclusion_stage="①브랜드", reason="상품명 선두에 대만 대상 브랜드가 없음")
        return result
    if candidate["page_type"] == "momo_goods":
        product_id = candidate["candidate_key"].split(":", 1)[1]
        evidence, evidence_file = read_evidence("goods", product_id)
        result["evidence_file"] = evidence_file
        result["http_status"] = evidence.get("http_status", "")
        result["final_url"] = evidence.get("final_url") or result["final_url"]
        if evidence.get("schema_brand"):
            schema_brand = brand_from_title(evidence["schema_brand"])
            if schema_brand:
                result["brand"] = schema_brand
            else:
                result["brand"] = evidence["schema_brand"]
        name = evidence.get("schema_name") or name
        result["product_name"] = name
        breadcrumb = evidence.get("breadcrumb", [])
    else:
        match = re.search(r"/TP/(TP\d+)/", candidate["canonical_url"])
        evidence, evidence_file = read_evidence("shop", match.group(1)) if match else ({}, "")
        result["evidence_file"] = evidence_file
        breadcrumb = []
    cats = product_categories(name, breadcrumb)
    result["product_categories"] = "+".join(cats)
    if cats and not any(result["brand"] in brands[cat] for cat in cats):
        result.update(decision="제외", exclusion_stage="①브랜드", reason=f"실제 제품군 {result['product_categories']}의 대상 브랜드 아님")
        return result
    if candidate["page_type"] == "TP_shop":
        if evidence.get("http_status") != 200 or not evidence.get("meta_keywords"):
            result.update(decision="검토 필요", exclusion_stage="③리리부", reason="입점 상점 대표 페이지 확인 실패")
            return result
        result.update(decision="제외", exclusion_stage="③리리부", reason="mo店+ 입점 상점 상품(/TP/ 경로)",
                      seller="입점 상점", seller_basis=f"대표 PDP의 商店 표시·상점명: {evidence.get('meta_keywords','')[-100:]}")
        return result
    if STYLER.search(name) and not cats:
        result.update(decision="제외", exclusion_stage="②제품군", reason="전자 의류관리기만 있는 상품")
        return result
    if not cats:
        result.update(decision="검토 필요", exclusion_stage="②제품군", reason="상품명·상세 카테고리에서 대상 제품군 미확인")
        return result
    # Category paths and title both matter: a bundled target appliance stays eligible.
    if PART.search(name) and not (WM.search(name) or REF.search(name) or DRY.search(name)):
        result.update(decision="제외", exclusion_stage="③리리부", reason="부품·액세서리 단독 상품")
        return result
    hit = exclusion_hit(name, keywords)
    if hit:
        result.update(decision="제외", exclusion_stage="③리리부", reason=f"{hit[0]}: 상품명에 {hit[1]} (EY 제외키워드 시트)")
        return result
    result["seller"] = "momo (추정)"
    result["seller_basis"] = "일반 /product/ 상품 페이지; /TP/ 상점 경로 아님; 기존 Momoshop OSM v3와 같은 분류 근거"
    if evidence.get("http_status") != 200 or not evidence.get("schema_product_type") or not evidence.get("schema_name"):
        result.update(decision="제외", exclusion_stage="④페이지없음", reason="정상 상품 상세 정보가 확인되지 않음")
        return result
    if evidence.get("conditions") and all(x != "https://schema.org/NewCondition" for x in evidence["conditions"]):
        result.update(decision="검토 필요", exclusion_stage="③리리부", reason="상품 상태가 NewCondition이 아님")
        return result
    result["decision"] = "포함"
    return result


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: row.get(key, "") for key in fields} for row in rows)


def main():
    expected_jobs = jobs()
    missing = [f"{kind}-{key}" for kind, key, _ in expected_jobs if not (EVIDENCE / f"{kind}-{key}.json").exists()]
    if missing:
        raise RuntimeError(f"PDP inspection incomplete: {len(missing)} missing, examples {missing[:5]}")
    brands, keywords = rules()
    with SOURCE.open(encoding="utf-8-sig", newline="") as file:
        candidates = list(csv.DictReader(file))
    with CARDS.open(encoding="utf-8-sig", newline="") as file:
        cards = list(csv.DictReader(file))
    hits = defaultdict(list)
    for card in cards:
        hits[candidate_key(card)].append(card)
    judged = [judge(row, hits[row["candidate_key"]], brands, keywords) for row in candidates]
    by_key = {row["candidate_key"]: row for row in judged}
    fields = list(judged[0])
    selected = [row for row in judged if row["decision"] == "포함"]
    seen = set()
    for row in selected:
        if row["final_url"] in seen:
            row.update(decision="제외", exclusion_stage="④중복", reason="실제 도착 주소 중복")
        else:
            seen.add(row["final_url"])
    selected = [row for row in judged if row["decision"] == "포함"]
    write_csv(OUT / "candidate_judgments.csv", judged, fields)
    write_csv(OUT / "final_pdp_urls.csv", selected, fields)
    write_csv(OUT / "review_needed.csv", [row for row in judged if row["decision"] == "검토 필요"], fields)
    represented = set()
    card_judgments = []
    for card in cards:
        key = candidate_key(card)
        base = by_key[key]
        row = {**card, "candidate_key": key, "final_url": base["final_url"],
               "brand": base["brand"], "product_categories": base["product_categories"],
               "decision": base["decision"], "exclusion_stage": base["exclusion_stage"],
               "reason": base["reason"]}
        if base["decision"] == "포함" and key in represented:
            row.update(decision="제외", exclusion_stage="④중복", reason="같은 상품의 다른 검색어·페이지 카드")
        if base["decision"] == "포함":
            represented.add(key)
        card_judgments.append(row)
    write_csv(OUT / "all_search_card_judgments.csv", card_judgments, list(card_judgments[0]))
    report = {"source_cards": len(cards), "unique_candidates": len(candidates),
              "candidate_decisions": dict(Counter(row["decision"] for row in judged)),
              "excluded_by_stage": dict(Counter(row["exclusion_stage"] for row in judged if row["decision"] == "제외")),
              "final_pdp_count": len(selected),
              "final_by_brand": dict(Counter(row["brand"] for row in selected)),
              "final_by_category": dict(Counter(row["product_categories"] for row in selected)),
              "review_count": sum(row["decision"] == "검토 필요" for row in judged)}
    (OUT / "final_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
