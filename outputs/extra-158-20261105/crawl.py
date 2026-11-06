"""Free direct-HTTP evidence crawl of all v3-included LG Saudi eXtra PDPs.

The Arabic unavailable phrase also occurs in a global ACC.config string, so
classification uses this product's pdpDetails.stock.stockLevelStatus.code.
"""

import csv
import glob
import gzip
import hashlib
import json
import re
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
V3 = Path(glob.glob(str(ROOT / "pdp 모수 추출/최종_20261029/*공유용_v3*.csv"))[0])
OSM = ROOT / "pdp 모수 추출/OSM_추가9개리테일러_PDP후보_4942건_20261028.csv"
KST = ZoneInfo("Asia/Seoul")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
    "Accept-Language": "ar-SA,ar;q=0.9,en;q=0.5",
}
PATTERN = re.compile(r"var pdpDetails\s*=\s*(\{.*?\});", re.S)


with OSM.open(encoding="utf-8-sig", newline="") as f:
    osm = {r["CRAWL_URL"]: r for r in csv.DictReader(f)
           if r["CNTRY"] == "SaudiArabia" and r["RTLR_NAME"] == "EXTRA" and r["BRAND"] == "LG"}
with V3.open(encoding="utf-8-sig", newline="") as f:
    target = [r for r in csv.DictReader(f)
              if r["국가"] == "Saudi Arabia" and r["리테일러"] == "EXTRA"
              and r["브랜드"] == "LG" and r["모수 포함 여부"] == "포함"]
assert len(target) == 112 and len({r["확인 요청 URL"] for r in target}) == 112
assert all(r["확인 요청 URL"] in osm for r in target)


def fetch(row):
    url = row["확인 요청 URL"]
    source = osm[url]
    result = {
        "v3_행번호": row["행번호"],
        "제품군": row["제품군"],
        "제품코드": row["제품코드"],
        "URL": url,
        "v3_판정": row["모수 포함 여부"],
        "OSM_수집일": source["RPT_DATE"],
        "OSM_AVLBL_STAT": source["AVLBL_STAT"],
        "확인시각_KST": "",
        "HTTP상태": "",
        "최종URL": "",
        "HTML바이트": "",
        "HTML_SHA256": "",
        "저장HTML": "",
        "상품JSON_코드": "",
        "상품JSON_이름": "",
        "현재_재고코드": "",
        "현재_재고수량": "",
        "현재_배송재고여부": "",
        "현재_장바구니활성": "",
        "현재_외부판매자여부": "",
        "아랍어품절문구_HTML전체포함": "",
        "현재_판정": "",
        "오류": "",
    }
    for attempt in range(2):
        try:
            with urlopen(Request(url, headers=HEADERS), timeout=35) as response:
                body = response.read()
                result["HTTP상태"] = response.status
                result["최종URL"] = response.url
            result["확인시각_KST"] = datetime.now(KST).isoformat(timespec="seconds")
            result["HTML바이트"] = len(body)
            digest = hashlib.sha256(body).hexdigest()
            result["HTML_SHA256"] = digest
            filename = f"row-{int(row['행번호']):05d}-{digest[:12]}.html.gz"
            with gzip.open(OUT / "html" / filename, "xb") as f:
                f.write(body)
            result["저장HTML"] = "html/" + filename
            html = body.decode("utf-8", "replace")
            result["아랍어품절문구_HTML전체포함"] = "غير متوفر حاليًا" in html
            match = PATTERN.search(html)
            if match:
                product = json.loads(match.group(1))
                stock = product.get("stock") or {}
                stock_status = stock.get("stockLevelStatus") or {}
                result["상품JSON_코드"] = product.get("code", "")
                result["상품JSON_이름"] = product.get("name", "")
                result["현재_재고코드"] = stock_status.get("code", "")
                result["현재_재고수량"] = stock.get("stockLevel", "")
                result["현재_배송재고여부"] = product.get("stockAvailableForHD", "")
                result["현재_장바구니활성"] = product.get("isAddToCartEnabled", "")
                result["현재_외부판매자여부"] = product.get("marketPlaceProduct", "")
                if stock_status.get("code") == "outOfStock":
                    result["현재_판정"] = "상품JSON_재고없음"
                elif stock_status.get("code") == "inStock":
                    result["현재_판정"] = "상품JSON_재고있음"
                else:
                    result["현재_판정"] = "확인필요_재고코드기타"
            else:
                result["현재_판정"] = "확인필요_상품JSON없음"
            return result
        except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            result["오류"] = f"{type(exc).__name__}: {exc}"
            if attempt == 0:
                time.sleep(2)
    result["확인시각_KST"] = datetime.now(KST).isoformat(timespec="seconds")
    result["현재_판정"] = "수집실패"
    return result


results = []
with ThreadPoolExecutor(max_workers=5) as pool:
    for future in as_completed([pool.submit(fetch, row) for row in target]):
        results.append(future.result())
results.sort(key=lambda r: int(r["v3_행번호"]))
output = OUT / "eXtra_LG_v3포함112_OSM재고및현재PDP_전수조사_20261105.csv"
with output.open("x", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(results[0]))
    writer.writeheader()
    writer.writerows(results)
print(output)
print("current", Counter(r["현재_판정"] for r in results))
print("OSM", Counter(r["OSM_AVLBL_STAT"] for r in results))
print("cross", Counter((r["OSM_AVLBL_STAT"], r["현재_판정"]) for r in results))
