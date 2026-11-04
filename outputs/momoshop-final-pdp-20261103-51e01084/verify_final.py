"""Check accounting and evidence for the Momoshop search PDP result."""

import csv
import gzip
import json
from collections import Counter

from finalize import OUT, CARDS, EVIDENCE, candidate_key, exclusion_hit, product_categories, rules


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main():
    brands, keywords = rules()
    cards = rows(CARDS)
    judged = rows(OUT / "candidate_judgments.csv")
    final = rows(OUT / "final_pdp_urls.csv")
    all_cards = rows(OUT / "all_search_card_judgments.csv")
    summary = json.loads((OUT / "final_summary.json").read_text())
    inspect = json.loads((OUT / "inspect_summary.json").read_text())
    source = json.loads((OUT.parent / "momoshop-search-pdp-20261103-76f0f589" / "summary.json").read_text())

    assert not inspect["errors"], inspect["errors"]
    assert not source["failed_keywords"], source["failed_keywords"]
    assert len(cards) == len(all_cards) == source["total_cards"] == summary["source_cards"]
    assert len(judged) == source["unique_pdp_candidates"] == summary["unique_candidates"]
    assert len(set(row["candidate_key"] for row in judged)) == len(judged)
    assert {candidate_key(row) for row in cards} == {row["candidate_key"] for row in judged}
    assert Counter(row["decision"] for row in judged) == summary["candidate_decisions"]
    assert not rows(OUT / "review_needed.csv")
    assert len(final) == summary["final_pdp_count"]
    assert len(set(row["final_url"] for row in final)) == len(final)
    bundle_ids = {"goods:13344761", "goods:13338351", "goods:13334769", "goods:13335576"}
    assert {row["candidate_key"] for row in final if row["candidate_key"] in bundle_ids and row["product_categories"] == "REF+W/M"} == bundle_ids
    assert {row["candidate_key"] for row in final} == {row["candidate_key"] for row in judged if row["decision"] == "포함"}
    assert Counter(row["decision"] for row in all_cards)["포함"] == len(final)
    assert all(row["decision"] in {"포함", "제외"} for row in all_cards)

    recovered = []
    for row in final:
        assert row["page_type"] == "momo_goods"
        assert row["brand"] in {brand for cat in row["product_categories"].split("+") for brand in brands[cat]}
        assert not exclusion_hit(row["product_name"], keywords)
        assert row["http_status"] == "200"
        evidence = json.loads((EVIDENCE / ("goods-" + row["candidate_key"].split(":", 1)[1] + ".json")).read_text())
        assert evidence["schema_product_type"] in ("Product", "ProductGroup")
        assert evidence["schema_name"] == row["product_name"]
        assert product_categories(evidence["schema_name"], evidence["breadcrumb"])
        assert evidence["final_url"] == row["final_url"]
        if evidence.get("fallback_used"):
            recovered.append(row["candidate_key"])
            assert evidence["canonical_failure_title"] == "momo購物網 -- Mobile管理訊息"
            assert evidence["fallback_checked_url"] == evidence["request_url"]
            assert "?" in row["final_url"]

    missing_pages = [row for row in judged if row["exclusion_stage"] == "④페이지없음"]
    for row in missing_pages:
        path = EVIDENCE / ("goods-" + row["candidate_key"].split(":", 1)[1] + ".html.gz")
        page = gzip.decompress(path.read_bytes()).decode("utf-8", "replace")
        assert "網頁無法顯示" in page and "商品目前無展售" in page

    assert len(recovered) == 12 and len(missing_pages) == 2

    print(json.dumps({"cards": len(cards), "unique_candidates": len(judged), "final_urls": len(final),
                      "excluded": len(judged) - len(final), "review_needed": 0,
                      "page_not_displayed": len(missing_pages), "fallback_recovered": len(recovered), "failed_keywords": 0,
                      "failed_pdp_inspections": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
