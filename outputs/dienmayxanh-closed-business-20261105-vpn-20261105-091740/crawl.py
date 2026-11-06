"""Save public Dienmayxanh PDP HTML for the 114 LG URLs included in v3."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
import csv
import glob
import gzip
import re
import time


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / "pdp 모수 추출/OSM_추가9개리테일러_PDP후보_4942건_20261028.csv"
V3 = Path(glob.glob(str(ROOT / "pdp 모수 추출/최종_20261029/*공유용_v3*.csv"))[0])
KST = ZoneInfo("Asia/Seoul")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128.0 Safari/537.36",
    "Accept-Language": "vi-VN,vi;q=0.9",
}


def norm(text):
    return " ".join(text.split()).upper()


class ProductText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.h1 = []
        self.markers = []
        self.buy = []

    def handle_starttag(self, tag, attrs):
        self.stack.append((tag, dict(attrs)))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not data.strip() or any(tag in {"script", "style", "svg", "template", "noscript"} for tag, _ in self.stack):
            return
        if any(tag == "h1" for tag, _ in self.stack):
            self.h1.append(data.strip())
        if "NGƯNG KINH DOANH" in norm(data):
            self.markers.append(data.strip())
        if any(tag == "button" for tag, _ in self.stack) and "MUA NGAY" in norm(data):
            self.buy.append(data.strip())


def fetch(row):
    url = row["확인 요청 URL"]
    item = {
        "v3_행번호": row["행번호"],
        "제품군": row["제품군"],
        "제품코드": row["제품코드"],
        "상품명_v3": row["상품명"],
        "URL": url,
        "OSM_기준일": "2026-10-19",
        "OSM_AVLBL_STAT": osm[url]["AVLBL_STAT"],
        "v3_판정": row["모수 포함 여부"],
        "확인시각_KST": "",
        "HTTP상태": "",
        "최종URL": "",
        "HTML바이트": "",
        "HTML_SHA256": "",
        "저장HTML": "",
        "상품제목_H1": "",
        "중단문구_발견수": "",
        "중단문구_원문": "",
        "구매버튼_발견수": "",
        "현재화면_분류": "",
        "오류": "",
    }
    for attempt in range(2):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=25) as response:
                body = response.read()
                item["HTTP상태"] = response.status
                item["최종URL"] = response.url
            item["확인시각_KST"] = datetime.now(KST).isoformat(timespec="seconds")
            item["HTML바이트"] = len(body)
            item["HTML_SHA256"] = sha256(body).hexdigest()
            filename = f"row-{int(row['행번호']):05d}-{item['HTML_SHA256'][:12]}.html.gz"
            with gzip.open(OUT / "html" / filename, "wb") as f:
                f.write(body)
            item["저장HTML"] = "html/" + filename
            parser = ProductText()
            parser.feed(body.decode("utf-8", errors="replace"))
            item["상품제목_H1"] = " ".join(parser.h1)
            item["중단문구_발견수"] = len(parser.markers)
            item["중단문구_원문"] = " | ".join(parser.markers)
            item["구매버튼_발견수"] = len(parser.buy)
            if not item["상품제목_H1"]:
                item["현재화면_분류"] = "미확인_상품제목없음"
            elif parser.markers:
                item["현재화면_분류"] = "NGƯNG KINH DOANH 표시"
            elif parser.buy:
                item["현재화면_분류"] = "중단문구없음_구매버튼있음"
            else:
                item["현재화면_분류"] = "미확인_중단문구및구매버튼없음"
            return item
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            item["오류"] = f"{type(exc).__name__}: {exc}"
            if attempt == 0:
                time.sleep(1)
    item["확인시각_KST"] = datetime.now(KST).isoformat(timespec="seconds")
    item["현재화면_분류"] = "수집실패"
    return item


with SOURCE.open(encoding="utf-8-sig", newline="") as f:
    osm = {r["CRAWL_URL"]: r for r in csv.DictReader(f) if r["RTLR_NAME"] == "DIENMAYXANH"}
with V3.open(encoding="utf-8-sig", newline="") as f:
    target = [r for r in csv.DictReader(f) if r["국가"] == "Vietnam" and r["리테일러"] == "DIENMAYXANH" and r["브랜드"] == "LG" and r["모수 포함 여부"] == "포함"]
assert len(target) == 114 and len({r["확인 요청 URL"] for r in target}) == 114
assert all(r["확인 요청 URL"] in osm for r in target)

results = []
with ThreadPoolExecutor(max_workers=5) as pool:
    futures = {pool.submit(fetch, row): row for row in target}
    for future in as_completed(futures):
        results.append(future.result())
results.sort(key=lambda r: int(r["v3_행번호"]))
path = OUT / "Dienmayxanh_LG_v3포함114_영업중단_조사결과_20261105.csv"
with path.open("x", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(results[0]))
    writer.writeheader()
    writer.writerows(results)
print(path)
from collections import Counter
print(Counter(r["현재화면_분류"] for r in results))
