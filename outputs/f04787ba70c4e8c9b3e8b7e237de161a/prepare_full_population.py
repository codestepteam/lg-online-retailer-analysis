"""Map every Momoshop search card to the v3 population columns."""

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FINAL = ROOT / "outputs/momoshop-final-pdp-20261103-51e01084"
CARDS = FINAL / "all_search_card_judgments.csv"
CANDIDATES = FINAL / "candidate_judgments.csv"

V3_COLUMNS = [
    "행번호", "흐름", "국가", "리테일러", "제품군", "브랜드", "제품코드", "OSM브랜드",
    "상품명", "확인 요청 URL", "원본 상품 URL", "기준일", "검색어", "엑셀행번호", "광고여부",
    "출처파일", "모수 포함 여부", "제외단계", "제외사유", "메모", "페이지확인규칙",
    "페이지 접속 확인 결과", "접속 후 URL", "판매자", "판매자구분", "판매자근거",
]
COLUMNS = V3_COLUMNS
CATEGORY = {"Dryer": "DRY", "Refrigerator": "REF", "Washing Machine": "W/M"}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main():
    cards = read_csv(CARDS)
    candidates = {row["candidate_key"]: row for row in read_csv(CANDIDATES)}
    first_included = {}
    rows = []
    for number, card in enumerate(cards, 1):
        candidate = candidates[card["candidate_key"]]
        included = card["decision"] == "포함"
        if included:
            first_included[card["candidate_key"]] = number
        duplicate_of = first_included.get(card["candidate_key"]) if card["exclusion_stage"] == "④중복" else None
        if card["exclusion_stage"] == "④중복" and duplicate_of is None:
            raise ValueError(f"Duplicate without included representative: {number}")
        normal_page = candidate["page_type"] == "momo_goods" and bool(candidate["http_status"])
        page_result = ("화면 표시 안 됨" if card["exclusion_stage"] == "④페이지없음" else "정상") if normal_page else ""
        seller = ""
        seller_type = ""
        seller_basis = ""
        if page_result == "정상" and candidate["seller"] == "momo (추정)":
            seller = "momo (추정)"
            seller_type = "직판 추정"
            seller_basis = "상품 페이지에 입점 상점 표시 없음; 일반 /product/ 주소"
        elif candidate["page_type"] == "TP_shop" and candidate["seller"] == "입점 상점":
            match = re.search(r"/TP/(TP\d+)/", card["product_url"])
            if not match:
                raise ValueError(f"TP shop ID missing: {number}")
            shop_id = match.group(1)
            evidence = json.loads((FINAL / "pdp_evidence" / f"shop-{shop_id}.json").read_text())
            meta = evidence.get("meta_keywords", "")
            if "," not in meta:
                raise ValueError(f"TP seller name missing: {shop_id}")
            seller = meta.rsplit(",", 1)[-1].strip()
            seller_type = "입점 상점"
            seller_basis = f"같은 mo店+ 상점 대표 상품 페이지의 상점명 정보({shop_id})"
        row = {
            "행번호": number,
            "흐름": "검색",
            "국가": "Taiwan",
            "리테일러": "MOMOSHOP",
            "제품군": CATEGORY[card["category"]],
            "브랜드": card["brand"],
            "제품코드": "",
            "OSM브랜드": "",
            "상품명": card["name"],
            "확인 요청 URL": card["product_url"],
            "원본 상품 URL": card["product_url"],
            "기준일": "2026-11-03",
            "검색어": card["search_keyword"],
            "엑셀행번호": int(card["source_row"]),
            "광고여부": "",
            "출처파일": "search_cards.csv",
            "모수 포함 여부": card["decision"],
            "제외단계": card["exclusion_stage"],
            "제외사유": (f"같은 상품(대표 행 {duplicate_of})" if duplicate_of else card["reason"]),
            "메모": "",
            "페이지확인규칙": "",
            "페이지 접속 확인 결과": page_result,
            "접속 후 URL": candidate["final_url"] if normal_page else "",
            "판매자": seller,
            "판매자구분": seller_type,
            "판매자근거": seller_basis,
        }
        if list(row) != COLUMNS:
            raise AssertionError("Workbook column order differs from v3 mapping")
        rows.append([row[col] for col in COLUMNS])

    decisions = Counter(row[COLUMNS.index("모수 포함 여부")] for row in rows)
    stages = Counter(row[COLUMNS.index("제외단계")] for row in rows)
    assert len(rows) == 6407 and decisions == {"포함": 443, "제외": 5964}
    assert stages["④중복"] == 1420
    payload = {"columns": COLUMNS, "rows": rows, "decisions": dict(decisions), "stages": dict(stages)}
    (OUT / "workbook_data.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"rows": len(rows), "decisions": decisions, "duplicate_rows": stages["④중복"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
