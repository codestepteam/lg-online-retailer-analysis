"""v6와 원본·수집 기록·본 상품 HTML을 독립 대조한다(외부 호출 없음)."""
import csv
import gzip
import json
import re
from collections import Counter

from bs4 import BeautifulSoup
import review_v6 as review


def main():
    plan = review.validate_plan()
    columns, source, targets = review.source_rows()
    v6_columns, v6 = review.read_csv(review.V6)
    assert v6_columns == columns and len(v6) == len(source) == 55_997
    assert [r["행번호"] for r in source] == [r["행번호"] for r in v6]
    records = [json.loads(line) for line in review.LOG.read_text().splitlines()]
    assert len(records) == len({r["row"] for r in records}) == len(targets) == 546
    assert all(r["ok"] for r in records)
    _, audits = review.read_csv(review.AUDIT)
    assert len(audits) == 546 and all(r["status"] in ("유지", "제외") for r in audits)
    by_id = {r["row"]: r for r in audits}
    assert set(by_id) == {t["row"] for t in plan["targets"]}
    _, failures = review.read_csv(review.FAILURES)
    assert failures == []
    allowed = {"모수 포함 여부", "제외단계", "제외사유", "판매자", "판매자구분", "판매자근거", "접속 후 URL", "메모"}
    changed, evidence = [], []
    for old, new in zip(source, v6):
        audit = by_id.get(old["행번호"])
        expected_change = audit is not None and audit["status"] == "제외"
        assert (old != new) == expected_change, old["행번호"]
        if not expected_change:
            continue
        assert (old["국가"], old["리테일러"]) in review.SCOPE
        assert old["모수 포함 여부"] == "포함" and new["모수 포함 여부"] == "제외"
        assert {c for c in columns if old[c] != new[c]} <= allowed
        assert new["제외단계"] == "③리리부"
        page = gzip.decompress(review.html_path(old["확인 요청 URL"]).read_bytes()).decode()
        soup = BeautifulSoup(page, "lxml")
        title = soup.find("h1")
        assert title is not None and re.sub(r"\s+", " ", title.get_text(" ", strip=True)) == audit["title"]
        item = {"row": old["행번호"], "country": old["국가"], "title": audit["title"], "seller": audit["seller"], "reason": audit["reason"]}
        if audit["reason"].startswith("본 상품 제목"):
            settings = json.loads(review.SNAPSHOT.read_text())["sellers"]["mediamarkt_screen"][old["국가"]]
            assert re.search(settings["refurb_title"], title.get_text(" ", strip=True), re.I)
            item["confirmed_by"] = "본 상품 h1 제목"
        elif audit["reason"].startswith("본 상품 판매 영역"):
            offer = soup.select_one('[data-test="mms-product-price"]')
            assert offer is not None, (old["행번호"], "main price container missing")
            links = [(a.get_text(" ", strip=True), a.get("href")) for a in offer.select('a[href*="/marketplace/seller/"]')]
            assert any(name == audit["seller"] for name, _ in links), (old["행번호"], links)
            item.update(confirmed_by="본 상품 mms-product-price 판매자 링크", links=links,
                        offer_text=offer.get_text(" ", strip=True))
            if audit["kind"] == "리퍼·중고":
                selected = soup.select_one('[data-test="mms-pdp-offer-selection"]')
                labels = selected.find_all(string=re.compile(r'^Refurbished\s*:', re.I)) if selected else []
                assert labels, (old["행번호"], "selected offer refurbished label missing")
                item["selected_offer_condition"] = str(labels[0])
        else:
            # 화면 문구가 없으면 보조 내부값으로 판단했다는 사실을 분리해 기록한다.
            assert "isProductOfTypeMarketplace=true" in audit["reason"], (old["행번호"], audit["reason"])
            item["confirmed_by"] = "본 상품 ID의 내부 마켓플레이스 값(화면 문구와 구분)"
        changed.append(old["행번호"])
        evidence.append(item)
    expected_ids = {a["row"] for a in audits if a["status"] == "제외"}
    assert set(changed) == expected_ids
    result = {"rows": 55_997, "columns": len(columns), "reviewed": 546, "paid_attempts": len(records), "failures": 0,
              "changed": len(changed), "changed_by_country": dict(Counter(x["country"] for x in evidence)),
              "before": dict(Counter(r["모수 포함 여부"] for r in source)), "after": dict(Counter(r["모수 포함 여부"] for r in v6)),
              "v5_sha256": review.digest(review.SOURCE), "v6_sha256": review.digest(review.V6)}
    (review.HERE / "independent_verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (review.HERE / "changed_main_offer_evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
