"""Read v3 and the saved browser audit into a small, validated JSON input."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
V3 = ROOT / "pdp 모수 추출/최종_20261029/PDP모수_공유용_v3_EY검토반영_25개국_35개리테일러_전체판정_55997행_20261031.csv"
OBSERVED = OUT / "v3_included_25_saudivpn_상품화면판매자_20261105.csv"
INPUT = OUT / "SharafDG_v3외부판매자9_작성입력.json"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


columns, v3_rows = read_csv(V3)
_, observed_rows = read_csv(OBSERVED)
v3 = {row["행번호"]: row for row in v3_rows}
included = [row for row in v3_rows if row["국가"] == "UAE" and row["리테일러"] == "Sharaf DG" and row["모수 포함 여부"] == "포함"]
assert len(included) == 25 and len({row["행번호"] for row in included}) == 25
assert len(observed_rows) == 25 and len({row["v3행번호"] for row in observed_rows}) == 25
assert {row["행번호"] for row in included} == {row["v3행번호"] for row in observed_rows}

selected = []
for observation in observed_rows:
    row = v3[observation["v3행번호"]]
    assert row["확인 요청 URL"] == observation["정확한promo_URL"]
    assert row["모수 포함 여부"] == "포함"
    assert observation["내부브라우저_상품화면도달"] == "Y"
    assert observation["내부브라우저_최종URL"] == observation["정확한promo_URL"]
    if observation["현재판매자_기준"] != "외부 판매자":
        continue
    assert observation["상품판매영역_판매자"] != "Sharaf DG"
    selected.append({"v3": row, "observation": observation})

assert len(selected) == 9
assert sum(item["v3"]["브랜드"] == "LG" for item in selected) == 3
INPUT.write_text(json.dumps({"v3_columns": columns, "selected": selected}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"validated {len(included)} v3 included rows, selected {len(selected)} external sellers; input={INPUT}")
