"""Select study pairs by the exact v8.1 exclusion and keep URLs byte-for-byte."""

import csv
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from urllib.parse import urlsplit


OUT = Path(__file__).resolve().parent
SOURCE = OUT.parents[1] / "pdp 모수 추출/최종_20261029/PDP모수_공유용_v8.1_1P3P구분추가_25개국_35개리테일러_전체판정_55129행_20261118.csv"
PILOT_EXCLUDED = {"7995", "8093", "8458", "8627", "8690", "8911"}


def product_number(row):
    number = urlsplit(row["접속 후 URL"]).path.rstrip("/").rsplit("/", 1)[-1]
    return number if number.isascii() and number.isdigit() else None


def select():
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    by_id = {row["행번호"]: row for row in rows}
    assert len(rows) == len(by_id) == 55129
    excluded = [r for r in rows if r["제외단계"] == "④중복" and "주소의 상품 번호 같음" in r["제외사유"]]
    assert Counter(r["리테일러"] for r in excluded) == {"COSTCO": 43, "FALABELLA": 19}
    pairs = []
    for i, b in enumerate(excluded, 1):
        [rep_id] = re.findall(r"대표 행 (\d+)", b["제외사유"])
        a = by_id[rep_id]
        assert a["모수 포함 여부"] == "포함" and b["모수 포함 여부"] == "제외"
        assert (a["국가"], a["리테일러"]) == (b["국가"], b["리테일러"])
        assert product_number(a) and product_number(a) == product_number(b)
        assert urlsplit(a["접속 후 URL"]).path != urlsplit(b["접속 후 URL"]).path
        pairs.append({"pair": i, "rows": [a, b], "pilot": b["행번호"] in PILOT_EXCLUDED})
    target_ids = {r["행번호"] for p in pairs for r in p["rows"]}
    assert len(target_ids) == 124
    assert Counter(p["rows"][0]["리테일러"] for p in pairs if p["pilot"]) == {"COSTCO": 3, "FALABELLA": 3}
    controls = []
    for retailer in ("COSTCO", "FALABELLA"):
        groups = defaultdict(list)
        for r in rows:
            if (r["리테일러"] == retailer and r["모수 포함 여부"] == "포함" and r["제품코드"].strip()
                    and r["행번호"] not in target_ids and product_number(r)):
                groups[(r["국가"], r["브랜드"], r["제품코드"])].append(r)
        for group in groups.values():
            pair = next(((a, b) for a, b in combinations(group, 2) if product_number(a) != product_number(b)), None)
            if pair:
                controls.append({"retailer": retailer, "rows": pair})
            if sum(c["retailer"] == retailer for c in controls) == 3:
                break
    assert Counter(c["retailer"] for c in controls) == {"COSTCO": 3, "FALABELLA": 3}
    return {
        "source": SOURCE.name, "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "pairs": pairs, "controls": controls, "random_seed": 20261121,
        "crosscheck": sorted(random.Random(20261121).sample([p["pair"] for p in pairs], 10)),
    }


if __name__ == "__main__":
    manifest = select()
    (OUT / "raw" / "selection.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(manifest['pairs'])} target pairs, {len(manifest['controls'])} control pairs, 124 unique rows")
