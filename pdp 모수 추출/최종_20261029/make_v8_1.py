"""공유용 v8 → v8.1: 맨 끝에 `판매구분(1P/3P)` 열 하나만 더한다 (2026-11-18, D145, 두레이 #203).

기존 26열의 값·순서와 행 순서는 바꾸지 않는다. 새 열은 `판매자구분`만 보고 정한다.
  직판 → 1P(직판) / 외부판매자, 브랜드공식점 → 3P(입점) / 확인불가 → 확인불가 / 리퍼·중고, 빈칸 → 빈칸
`1P`, `3P`만 쓰면 일부 표 프로그램(gridcraft)이 오후 1시, 오후 3시로 읽어서 괄호 설명을 붙인다.
저장된 v8 파일만 읽으며 웹 요청이나 유료 수집을 하지 않는다.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
V8 = HERE / "PDP모수_공유용_v8_MomoShopDarty_OSM쿼리수정교체_25개국_35개리테일러_전체판정_55129행_20261116.csv"
V81 = HERE / "PDP모수_공유용_v8.1_1P3P구분추가_25개국_35개리테일러_전체판정_55129행_20261118.csv"
NEW = "판매구분(1P/3P)"
RULE = {"직판": "1P(직판)", "외부판매자": "3P(입점)", "브랜드공식점": "3P(입점)", "확인불가": "확인불가", "리퍼·중고": "", "": ""}


def main() -> None:
    with V8.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = list(reader.fieldnames)
        rows = list(reader)
    unknown = {r["판매자구분"] for r in rows} - RULE.keys()
    if unknown:
        raise SystemExit(f"규칙에 없는 판매자구분 값: {sorted(unknown)}")
    for row in rows:
        row[NEW] = RULE[row["판매자구분"]]
    with V81.open("x", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns + [NEW], quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
