"""D124 제목·판매자 조건만 대조한다. 판매 상태·영구품절은 독립 검증 파일에서 확인한다."""
import csv
import gzip
import hashlib
import json
import re
from collections import Counter

from bs4 import BeautifulSoup
import review_v6 as review
from rules.sellers.base import main_heading, visible_html


def main():
    records = [json.loads(line) for line in review.LOG.read_text().splitlines()]
    records = [r for r in records if r["country"] == "Hungary"]
    with review.AUDIT.open(encoding="utf-8-sig", newline="") as stream:
        audit = {r["row"]: r for r in csv.DictReader(stream) if r["country"] == "Hungary"}
    rules = json.loads(review.SNAPSHOT.read_text())["sellers"]
    settings = rules["mediamarkt_screen"]["Hungary"]
    counts, issues = Counter(), []
    assert len(records) == len(audit) == len({r["url"] for r in records}) == 268
    for record in records:
        counts["저장원문"] += review.html_path(record["url"]).exists()
        raw = gzip.decompress(review.html_path(record["url"]).read_bytes())
        assert hashlib.sha256(raw).hexdigest() == record["html_sha256"]
        page = raw.decode()
        title, end = main_heading(page)
        counts["수집성공"] += bool(record["ok"])
        counts["본문제목존재"] += bool(title)
        counts["제목제외단어"] += bool(re.search(settings["refurb_title"], title, re.I))
        segment = visible_html(page)[end:end + 180_000] if end is not None else ""
        for stop in settings["section_stops"]:
            match = re.search(stop, segment, re.I)
            if match:
                segment = segment[:match.start()]
        phrase = bool(re.search(settings["seller_phrase"], segment, re.I))
        counts["본상품판매자문구"] += phrase
        target = {k: record[k] for k in ("row", "country", "retailer", "url")}
        evaluated = review.evaluate(target, record, rules)
        counts["재판정_" + evaluated["status"]] += 1
        counts["본상품ID직판근거"] += "isProductOfTypeMarketplace=false" in evaluated["reason"]
        if any(evaluated[k] != audit[record["row"]][k] for k in ("title", "seller", "kind", "status", "reason")):
            issues.append({"행번호": record["row"], "문제": "기존 재판정 기록과 불일치"})
        soup = BeautifulSoup(page, "lxml")
        price = soup.select_one('[data-test="mms-product-price"]')
        counts["별도분석_본상품가격영역존재"] += price is not None
        links = price.select('a[href*="/marketplace/seller/"]') if price else []
        counts["별도분석_본상품외부판매자링크"] += bool(links)
        if links and not phrase:
            issues.append({"행번호": record["row"], "문제": "문구 검사 밖의 본 상품 판매자 링크 존재"})
    assert counts["저장원문"] == counts["수집성공"] == counts["본문제목존재"] == counts["별도분석_본상품가격영역존재"] == 268
    assert counts["본상품ID직판근거"] == counts["재판정_유지"] == 268
    assert counts["제목제외단어"] == counts["본상품판매자문구"] == counts["별도분석_본상품외부판매자링크"] == 0
    assert issues == []
    report = {"대상": "2026-11-10에 수집한 헝가리 MediaMarkt의 v5 포함 PDP 268개", "검사범위": "D124 제목·판매자 조건만 검사. 재고·영구품절 검사와 전체 모수 적합성 보증은 포함하지 않음.", "관련후속검토": "hungary_independent_stock_audit.json (기존 영구품절 기준 정정대상 2건)", "검사방식": "저장 원문 해시·제목·본 상품 판매자 검사 재실행 및 별도 HTML 분석 도구의 본 상품 가격 영역 대조", "새유료호출": 0, "결과": dict(counts), "실패및불일치목록": issues}
    (review.HERE / "hungary_recheck.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
