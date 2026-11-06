"""Review v4 included German MediaMarkt PDPs against current rendered pages.

Dry run is the default. --execute makes exactly one Zyte browserHtml call per
v4 included URL; it never retries or edits the source CSV.
"""

import argparse
import base64
import csv
import gzip
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / "pdp 모수 추출/최종_20261029/PDP모수_공유용_v4_두레이157-159제외반영_25개국_35개리테일러_전체판정_55997행_20261106.csv"
AUDIT = OUT / "독일_MediaMarkt_v4_포함195행_현재화면점검.csv"
CHANGES = OUT / "독일_MediaMarkt_v4_포함에서제외_변경대상_20261106.csv"
RUN_LOG = OUT / "독일_MediaMarkt_v4_현재화면점검_수집기록.jsonl"
KEYWORDS = re.compile(r"refurbished|general(?:ü|ue|u)berholt|wiederaufbereitet|gebraucht", re.I)
SELLER_PHRASE = re.compile(r"Verkauf\s+und\s+Versand\s+durch", re.I)
BLOCK = re.compile(r"captcha|cf-chl|access denied|just a moment", re.I)


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def text_of(fragment):
    parser = VisibleText()
    parser.feed(fragment)
    return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()


def parse_page(page):
    # Remove scripts so a recommendation or serialized JSON cannot impersonate
    # the text of the main offer.
    visible = re.sub(r"(?is)<(?:script|style|noscript)\b[^>]*>.*?</(?:script|style|noscript)\s*>", "", page)
    h1 = re.search(r"(?is)<h1\b[^>]*>(.*?)</h1>", visible)
    title = text_of(h1.group(1)) if h1 else ""
    title_hit = KEYWORDS.search(title)
    if not h1:
        return title, "", "", "확인불가", "본 상품 제목 없음"
    # A recommended-products carousel can precede the description and contain
    # its own seller cards. Stop before it rather than treating those sellers
    # as the main product's seller.
    segment = visible[h1.end():h1.end() + 180_000]
    recommendation = re.search(r"Für\s+dich\s+empfohlen", segment, re.I)
    if recommendation:
        segment = segment[:recommendation.start()]
    description = re.search(r"(?is)<h[12][^>]*>\s*Produktbeschreibung\s*</h[12]>", segment)
    if description:
        segment = segment[:description.start()]
    match = SELLER_PHRASE.search(segment)
    seller = ""
    seller_link = ""
    if match:
        following = segment[match.end():match.end() + 2200]
        anchor = re.search(r"(?is)<a\b([^>]*)>(.*?)</a>", following)
        if anchor:
            seller = text_of(anchor.group(2))
            href = re.search(r"\bhref\s*=\s*['\"]([^'\"]+)", anchor.group(1), re.I)
            seller_link = html.unescape(href.group(1)) if href else ""
    if title_hit:
        return title, seller, seller_link, "제외", f"본 상품 제목 리퍼·중고 표현: {title_hit.group()}"
    if seller and ("/marketplace/seller/" in seller_link or "third-party-provider" in following.lower()):
        return title, seller, seller_link, "제외", f"본 상품 외부 판매자: {seller}"
    if seller and seller.casefold() not in ("mediamarkt", "media markt"):
        return title, seller, seller_link, "제외", f"본 상품 외부 판매자: {seller}"
    if match and not seller:
        return title, "", "", "확인필요", "판매자 문구는 있으나 판매자 이름 추출 불가"
    return title, seller, seller_link, "유지", "새 제외 조건 확인 안 됨"


def read_rows():
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames
        rows = [row for row in reader if row["국가"] == "Germany" and row["리테일러"] == "MEDIAMARKT" and row["모수 포함 여부"] == "포함"]
    assert len(rows) == 195 and len({row["확인 요청 URL"] for row in rows}) == 195
    return columns, rows


def api_key():
    key = os.getenv("ZYTE_API_KEY", "").strip()
    if key:
        return key
    path = ROOT / ".env"
    if path.exists():
        match = re.search(r"^ZYTE_API_KEY\s*=\s*(.*)$", path.read_text(), re.M)
        if match:
            return match.group(1).strip().strip("\"'")
    raise RuntimeError("ZYTE_API_KEY not configured")


def fetch(row, key):
    url = row["확인 요청 URL"]
    payload = json.dumps({"url": url, "browserHtml": True}).encode()
    credential = base64.b64encode((key + ":").encode()).decode()
    request = Request("https://api.zyte.com/v1/extract", data=payload, headers={"Content-Type": "application/json", "Authorization": "Basic " + credential})
    result = dict(row)
    result.update({"현재_확인시각_UTC": datetime.now(timezone.utc).isoformat(), "현재_접속후URL": "", "현재_제목": "", "현재_본상품_판매자": "", "현재_판매자링크": "", "변경요청_모수 포함 여부": "", "변경사유": "", "확인상태": ""})
    try:
        with urlopen(request, timeout=120) as response:
            body = json.load(response)
        page = body.get("browserHtml", "")
        result["현재_접속후URL"] = body.get("url", "")
        if not page or (len(page) < 60_000 and BLOCK.search(page)):
            result["확인상태"] = "확인불가"
            result["변경사유"] = "차단·빈 화면"
        else:
            name = hashlib.sha256(url.encode()).hexdigest()[:16] + ".html.gz"
            raw = OUT / "current_html" / name
            raw.parent.mkdir(exist_ok=True)
            raw.write_bytes(gzip.compress(page.encode()))
            title, seller, seller_link, status, why = parse_page(page)
            result.update({"현재_제목": title, "현재_본상품_판매자": seller, "현재_판매자링크": seller_link, "확인상태": status, "변경사유": why})
            if status == "제외":
                result["변경요청_모수 포함 여부"] = "제외"
    except (HTTPError, URLError, TimeoutError) as error:
        result["확인상태"] = "확인불가"
        result["변경사유"] = f"수집 실패: {type(error).__name__} {getattr(error, 'code', '')}"
    return result


def write_csv(path, columns, rows):
    with path.open("x", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def reparse_local(columns, rows):
    """Correct saved results using stored HTML only; never make API calls."""
    saved = {item["행번호"]: item for line in RUN_LOG.open(encoding="utf-8") if (item := json.loads(line))}
    if len(saved) != len(rows):
        raise RuntimeError(f"Expected {len(rows)} saved requests, found {len(saved)}")
    outputs = []
    for row in rows:
        result = saved[row["행번호"]]
        name = hashlib.sha256(row["확인 요청 URL"].encode()).hexdigest()[:16] + ".html.gz"
        page = gzip.decompress((OUT / "current_html" / name).read_bytes()).decode()
        title, seller, seller_link, status, why = parse_page(page)
        result.update({"현재_제목": title, "현재_본상품_판매자": seller,
                       "현재_판매자링크": seller_link, "확인상태": status,
                       "변경사유": why,
                       "변경요청_모수 포함 여부": "제외" if status == "제외" else ""})
        outputs.append(result)
    extra = ["현재_확인시각_UTC", "현재_접속후URL", "현재_제목", "현재_본상품_판매자",
             "현재_판매자링크", "변경요청_모수 포함 여부", "변경사유", "확인상태"]
    for path, subset in ((AUDIT, outputs), (CHANGES, [row for row in outputs if row["확인상태"] == "제외"])):
        temp = path.with_name(path.name + ".tmp")
        with temp.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns + extra)
            writer.writeheader()
            writer.writerows(subset)
        temp.replace(path)
    temp = RUN_LOG.with_name(RUN_LOG.name + ".tmp")
    with temp.open("w", encoding="utf-8") as handle:
        for result in outputs:
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")
    temp.replace(RUN_LOG)
    print(json.dumps({"reviewed": len(outputs), "exclude": sum(row["확인상태"] == "제외" for row in outputs),
                      "unverified": sum(row["확인상태"] in ("확인불가", "확인필요") for row in outputs)}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Use paid Zyte browserHtml calls (one per URL)")
    parser.add_argument("--pilot-row", help="First call a single v4 row, within the 195-call total")
    parser.add_argument("--reparse-local", action="store_true", help="Rebuild CSV and log from saved HTML without paid calls")
    args = parser.parse_args()
    columns, rows = read_rows()
    if args.reparse_local:
        if args.execute or args.pilot_row:
            raise RuntimeError("Local reparse cannot be combined with paid execution")
        reparse_local(columns, rows)
        return
    title_hits = [row for row in rows if KEYWORDS.search(row["상품명"])]
    if not args.execute:
        print(f"DRY RUN: {len(rows)} unique Germany/MEDIAMARKT v4 included URLs; v4 title keyword hits={len(title_hits)}")
        print("Paid plan: 195 browserHtml calls, no retries, source v4 unchanged")
        print(f"Audit: {AUDIT}\nChanges: {CHANGES}")
        return
    if AUDIT.exists() or CHANGES.exists():
        raise RuntimeError("Output already exists; refusing to overwrite")
    key = api_key()
    completed = {}
    if RUN_LOG.exists():
        for line in RUN_LOG.open(encoding="utf-8"):
            item = json.loads(line)
            completed[item["행번호"]] = item
    if not set(completed) <= {row["행번호"] for row in rows}:
        raise RuntimeError("Run log contains a row outside the 195 URL scope")
    todo = [row for row in rows if row["행번호"] not in completed]
    if args.pilot_row:
        todo = [row for row in todo if row["행번호"] == args.pilot_row]
        if len(todo) != 1:
            raise RuntimeError("Pilot row not found or already attempted")
    print(f"Already attempted {len(completed)}; new paid calls {len(todo)}", flush=True)
    with ThreadPoolExecutor(max_workers=12) as pool:
        jobs = {pool.submit(fetch, row, key): row["행번호"] for row in todo}
        with RUN_LOG.open("a", encoding="utf-8") as log:
            for future in as_completed(jobs):
                item = future.result()
                completed[item["행번호"]] = item
                log.write(json.dumps(item, ensure_ascii=False) + "\n")
                log.flush()
                if len(completed) % 25 == 0 or len(completed) == len(rows):
                    print(f"Reviewed {len(completed)}/{len(rows)}", flush=True)
    outputs = sorted(completed.values(), key=lambda row: int(row["행번호"]))
    if len(outputs) != len(rows):
        print(f"Partial run saved: {len(outputs)}/{len(rows)}; no final CSV written")
        return
    extra = ["현재_확인시각_UTC", "현재_접속후URL", "현재_제목", "현재_본상품_판매자", "현재_판매자링크", "변경요청_모수 포함 여부", "변경사유", "확인상태"]
    write_csv(AUDIT, columns + extra, outputs)
    changes = [row for row in outputs if row["변경요청_모수 포함 여부"] == "제외"]
    write_csv(CHANGES, columns + extra, changes)
    print(json.dumps({"reviewed": len(outputs), "exclude": len(changes), "unverified": sum(row["확인상태"] in ("확인불가", "확인필요") for row in outputs)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
