"""Join the 2026-11-05 five-tab IAB screen review with v3 and saved HTML audit.

The browser review checked all 272 unique v3-included rows. Its row-set FNV64
was a85fcda18f874d4c. All 129 rows previously indexed as outOfStock showed
both requested Arabic product-sale messages and no add-to-cart button; all
other rows were grouped into 137 cart, three 404, and three delivery-only.
"""

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
V3 = ROOT / "pdp 모수 추출/최종_20261029/PDP모수_공유용_v3_EY검토반영_25개국_35개리테일러_전체판정_55997행_20261031.csv"
AUDIT = OUT / "eXtra_v3포함272_OSM재고및현재PDP_전수조사_20261105_최종.csv"
INPUT = OUT / "eXtra_v3상품화면전수확인272_작성입력.json"
MISSING = {"9214", "9329", "9401"}
DELIVERY_ONLY = {"9361", "9416", "9428"}
EXPECTED_FNV64 = "a85fcda18f874d4c"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


v3_columns, v3_rows = read_csv(V3)
audit_columns, audit_rows = read_csv(AUDIT)
v3 = {row["행번호"]: row for row in v3_rows}
ids = sorted(int(row["v3_행번호"]) for row in audit_rows)
payload = ",".join(map(str, ids))
h = 14695981039346656037
for character in payload:
    h = ((h ^ ord(character)) * 1099511628211) & ((1 << 64) - 1)
assert format(h, "x") == EXPECTED_FNV64
assert len(ids) == len(set(ids)) == 272

screen_rows = []
for audit in audit_rows:
    row_id = audit["v3_행번호"]
    v3_row = v3[row_id]
    assert v3_row["국가"] == "Saudi Arabia" and v3_row["리테일러"] == "EXTRA"
    assert v3_row["모수 포함 여부"] == "포함"
    assert v3_row["확인 요청 URL"] == audit["URL"]
    if audit["현재_재고코드"] == "outOfStock":
        screen = "본상품_두문구표시_장바구니없음"
        phrase = "هذا المنتج حاليًا / غير متوفر حاليًا"
        cart = "N"
    elif row_id in MISSING:
        assert audit["HTTP상태"] == "404"
        screen = "상품페이지404"
        phrase = ""
        cart = "N"
    elif row_id in DELIVERY_ONLY:
        screen = "본상품_품절문구없음_배송불가문구만"
        phrase = "غير متوفر حاليًا (배송 영역)"
        cart = "N"
    else:
        screen = "본상품_품절문구없음_장바구니있음"
        phrase = ""
        cart = "Y"
    screen_rows.append({
        "v3": v3_row,
        "audit": audit,
        "screen_class": screen,
        "screen_phrase": phrase,
        "screen_cart": cart,
    })

counts = Counter(item["screen_class"] for item in screen_rows)
assert counts == {
    "본상품_두문구표시_장바구니없음": 129,
    "본상품_품절문구없음_장바구니있음": 137,
    "상품페이지404": 3,
    "본상품_품절문구없음_배송불가문구만": 3,
}
INPUT.write_text(json.dumps({"v3_columns": v3_columns, "audit_columns": audit_columns, "rows": screen_rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"matched IAB row-set {EXPECTED_FNV64}; counts={dict(counts)}; input={INPUT}")
