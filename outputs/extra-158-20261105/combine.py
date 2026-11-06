"""Join LG and other eXtra brands and verify every preserved response."""

import csv
import gzip
import hashlib
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
LG = OUT / "eXtra_LG_v3포함112_OSM재고및현재PDP_전수조사_20261105_최종.csv"
OTHER = OUT / "eXtra_nonLG_v3포함160_OSM재고및현재PDP_전수조사_20261105.csv"
FINAL = OUT / "eXtra_v3포함272_OSM재고및현재PDP_전수조사_20261105_최종.csv"
rows = []
for source in (LG, OTHER):
    with source.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if source == LG:
                row["브랜드"] = "LG"
            else:
                row["원본JSON_stockAvailableForHD"] = row.pop("현재_배송재고여부")
                row["전역설정_품절문구_HTML포함_판정미사용"] = row.pop("아랍어품절문구_HTML전체포함")
            rows.append(row)
assert len(rows) == 272
assert len({row["URL"] for row in rows}) == 272
assert len({row["v3_행번호"] for row in rows}) == 272
assert not any(row["오류"] for row in rows)
assert all(row["저장HTML"] and row["HTML_SHA256"] for row in rows)
for row in rows:
    body = gzip.open(OUT / row["저장HTML"], "rb").read()
    assert hashlib.sha256(body).hexdigest() == row["HTML_SHA256"]
    assert len(body) == int(row["HTML바이트"])
    if row["HTTP상태"] == "200":
        assert row["상품JSON_코드"] and row["상품JSON_코드"] in row["URL"]
    else:
        assert row["HTTP상태"] == "404" and row["현재_판정"] == "HTTP404_상품페이지없음"
columns = [
    "v3_행번호", "브랜드", "제품군", "제품코드", "URL", "v3_판정",
    "OSM_수집일", "OSM_AVLBL_STAT", "확인시각_KST", "HTTP상태", "최종URL",
    "HTML바이트", "HTML_SHA256", "저장HTML", "상품JSON_코드", "상품JSON_이름",
    "현재_재고코드", "현재_재고수량", "원본JSON_stockAvailableForHD",
    "현재_외부판매자여부", "전역설정_품절문구_HTML포함_판정미사용",
    "현재_판정", "오류",
]
rows.sort(key=lambda row: int(row["v3_행번호"]))
with FINAL.open("x", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
print(FINAL)
print("brands", Counter(row["브랜드"] for row in rows))
print("OSM", Counter(row["OSM_AVLBL_STAT"] for row in rows))
print("current", Counter(row["현재_판정"] for row in rows))
print("cross", Counter((row["OSM_AVLBL_STAT"], row["현재_판정"]) for row in rows))
