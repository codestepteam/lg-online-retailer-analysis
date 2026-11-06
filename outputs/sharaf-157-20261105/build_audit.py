"""Reconcile the saved v3 Sharaf DG rows with free access checks.

The indexed-page observations below refer to the product URL without ?promo=.
They must not be interpreted as the seller of the exact v3 offer URL.
"""

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PDP = ROOT / "pdp 모수 추출"
V3 = PDP / "최종_20261029/PDP모수_공유용_v3_EY검토반영_25개국_35개리테일러_전체판정_55997행_20261031.csv"
CARDS = PDP / "검색결과_20261028_734afcdd/상품카드.csv"
SELLERS = PDP / "최종_20261029/판정근거/판매자판정/seller_g4.csv"

# Read-only web index checks on 2026-11-05. Source URL is the product's base URL.
# A seller may change between index refreshes, and ?promo= could select another offer.
BASE_OBS = {
    "29731": ("Sharaf DG", "last week"),
    "29735": ("Applianzee", "last week"),
    "29739": ("Sharaf DG", "last week; other index snapshot: Digital Empire"),
    "29799": ("Sharaf DG", "today"),
    "29861": ("Sharaf DG", "yesterday"),
    "29936": ("Sharaf DG", "today"),
    "29959": ("Sharaf DG", "last week"),
    "29960": ("Sharaf DG", "today"),
    "30122": ("Bigzaya", "2 weeks ago"),
    "30252": ("Sharaf DG", "2 days ago"),
    "30595": ("Sharaf DG", "last month"),
    "31097": ("Sharaf DG", "4 weeks ago"),
    "31107": ("Digital Empire", "3 days ago"),
    "31191": ("Sharaf DG", "last week"),
    "31211": ("Sharaf DG", "today"),
    "31310": ("Safe Home", "4 days ago"),
    "31316": ("HOME STORE", "last week"),
    "31321": ("Safe Home", "today"),
    "31379": ("", "web index timed out"),
    "31446": ("Sharaf DG", "today"),
    "31447": ("Sharaf DG", "4 days ago; other index snapshot: Online Official Store"),
    "31453": ("KHAT AL SAMAA", "last month"),
    "31497": ("", "latest index: out of stock, seller hidden; older index: Safe Home"),
    "31516": ("Safe Home", "last month"),
    "31659": ("Sharaf DG", "3 days ago"),
}


def read_rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8-sig", newline="")))


def write_rows(path, rows, fields):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def base_url(url):
    s = urlsplit(url)
    return urlunsplit((s.scheme, s.netloc, s.path, "", ""))


def probe(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urlopen(req, timeout=15) as resp:
            body = resp.read()
            return str(resp.status), resp.url, body
    except HTTPError as exc:
        return str(exc.code), exc.url, exc.read()
    except (URLError, TimeoutError) as exc:
        return type(exc).__name__, url, str(exc).encode()


def main():
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    v3 = [r for r in read_rows(V3) if r["국가"] == "UAE" and r["리테일러"] == "Sharaf DG"]
    included = [r for r in v3 if r["모수 포함 여부"] == "포함"]
    assert len(v3) == 2793 and len(included) == 25
    assert set(BASE_OBS) == {r["행번호"] for r in included}
    sellers = {r["요청URL"]: r for r in read_rows(SELLERS) if r["국가"] == "UAE" and r["리테일러"] == "Sharaf DG"}
    cards = read_rows(CARDS)
    sharaf_cards = [r for r in cards if r["국가"] == "UAE" and r["리테일러"] == "Sharaf DG"]
    assert len(sharaf_cards) == 2793
    card_urls = {r["카드PDP링크"] for r in sharaf_cards}
    OUT.joinpath("http_responses").mkdir(exist_ok=True)
    audit = []
    for r in included:
        url = r["확인 요청 URL"]
        sid = r["행번호"]
        assert url in card_urls
        sr = sellers[url]
        assert sr["판매자"] == r["판매자"] and sr["판매자구분"] == r["판매자구분"]
        status, final_url, body = probe(url)
        body_path = OUT / "http_responses" / f"{sid}.html"
        body_path.write_bytes(body)
        observed, crawl_age = BASE_OBS[sid]
        audit.append({
            "v3행번호": sid,
            "브랜드": r["브랜드"],
            "상품명": r["상품명"],
            "검색어": r["검색어"],
            "검색카드수집일": r["기준일"],
            "v3포함여부": r["모수 포함 여부"],
            "v3판매자": r["판매자"],
            "v3판매자구분": r["판매자구분"],
            "v3판매자근거": r["판매자근거"],
            "과거판매자원본HTML": "저장소에 없음(판정근거 README)",
            "원본검색카드존재": "Y",
            "정확한promo_URL": url,
            "오늘정확한URL_HTTP상태": status,
            "오늘정확한URL_도착": final_url,
            "오늘HTTP응답파일": str(body_path.relative_to(ROOT)),
            "기본상품URL_promo없음": base_url(url),
            "검색인덱스_기본상품판매자": observed,
            "검색인덱스_수집시점표시": crawl_age,
            "기본상품판매자_정확한promo판매자같음": "미확인",
            "10월판정오류와판매자변경구분": "미확인",
            "조사시각UTC": ts,
        })
    write_rows(OUT / "v3_included_25_audit.csv", audit, list(audit[0]))

    term_rows = []
    by_term = Counter((r["엑셀행번호"], r["J열검색어"]) for r in sharaf_cards)
    for (excel_row, term), count in sorted(by_term.items(), key=lambda x: int(x[0][0])):
        term_rows.append({"EY_Search_Term_엑셀행번호": excel_row, "검색어": term, "저장카드수": count})
    write_rows(OUT / "search_terms_9_counts.csv", term_rows, list(term_rows[0]))

    summary = {
        "v3_sharaf_rows": len(v3),
        "v3_included": len(included),
        "v3_excluded": len(v3) - len(included),
        "v3_included_LG": sum(r["브랜드"] == "LG" for r in included),
        "search_card_rows": len(sharaf_cards),
        "search_term_rows": len(term_rows),
        "historical_seller_g4_rows": sum(r["국가"] == "UAE" and r["리테일러"] == "Sharaf DG" for r in read_rows(SELLERS)),
        "exact_promo_http_statuses": dict(Counter(r["오늘정확한URL_HTTP상태"] for r in audit)),
        "base_url_index_seller": dict(Counter(r["검색인덱스_기본상품판매자"] or "unknown/hidden" for r in audit)),
        "generated_utc": ts,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
