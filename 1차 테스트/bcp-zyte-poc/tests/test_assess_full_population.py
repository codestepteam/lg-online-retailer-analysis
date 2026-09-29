#!/usr/bin/env python3
"""Protect page-type scope and source-identity handling in the 159-row ledger."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from assess_full_population import source_conflicts, redirected_brand_issues, metadata_checks, sidebar_nav_check
from capture_bcp_population import selected_records, prepared_recipe


class FullPopulationTests(unittest.TestCase):
    def test_scope_includes_both_page_types(self):
        inventory = {"records": [
            {"pageType": "Brand Category Page", "brand": "LG"},
            {"pageType": "Brand Category Page", "brand": "AEG"},
            {"pageType": "Brand Page", "brand": "LG"},
        ]}
        self.assertEqual(len(selected_records(inventory, "all-pages")), 3)
        self.assertEqual(len(selected_records(inventory, "all-bcp")), 2)
        self.assertEqual(len(selected_records(inventory, "lg-bcp")), 1)

    def test_brand_page_uses_brand_recipe(self):
        record = {"sourceRow": 1, "retailerSlug": "darty", "pageType": "Brand Page",
                  "url": "https://www.darty.com/nav/q/marque-samsung.html"}
        recipe, request = prepared_recipe(record)
        self.assertEqual(recipe["page_type"], "brand")
        self.assertEqual(request["url"], record["url"])

    def test_elgiganten_editorial_page_keeps_missing_h1_as_assessment_issue(self):
        record = {"sourceRow": 149, "retailerSlug": "elgiganten", "pageType": "Brand Category Page", "brand": "BOSCH",
                  "url": "https://www.elgiganten.se/brand/bosch/bosch-vitvaror/bosch-torktumlare"}
        recipe, _ = prepared_recipe(record)
        config_source = next(action["source"] for action in recipe["request"]["actions"]
                             if action.get("source", "").startswith("window.__lgConfig = "))
        config = json.loads(config_source.removeprefix("window.__lgConfig = ").rstrip(";"))
        self.assertEqual(config["required"], ["body"])
        self.assertEqual(recipe["evidence"]["title_contains"], ["BOSCH"])

    def test_duplicate_address_flags_only_brand_that_disagrees_with_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            batch = Path(tmp)
            page = batch / "pages" / "row-0001-amazon-it" / "brand-category"
            page.mkdir(parents=True)
            (page / "capture-state.json").write_text(json.dumps({"title": "Amazon.it: LG: LAVASCIUGA"}))
            records = [
                {"sourceRow": 1, "pageKey": "row-0001-amazon-it", "pageType": "Brand Category Page", "brand": "LG", "url": "https://amazon.it/stores/page/example"},
                {"sourceRow": 2, "pageKey": "row-0002-amazon-it", "pageType": "Brand Category Page", "brand": "SAMSUNG", "url": "https://amazon.it/stores/page/example"},
            ]
            self.assertEqual(list(source_conflicts(batch, records)), [2])

    def test_branded_url_redirecting_to_mixed_list_is_not_a_negative_content_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            batch = Path(tmp)
            page = batch / "pages" / "row-0001-datart" / "brand-category"
            page.mkdir(parents=True)
            (page / "capture-state.json").write_text(json.dumps({
                "title": "Lednice | DATART", "metadata": {"h1": ["Lednice"]},
                "images": [{"visible": True, "alt": "Bosch fridge"}, {"visible": True, "alt": "LG fridge"}],
            }))
            (page / "response.json").write_text(json.dumps({"final_url": "https://www.datart.cz/lednicky.html"}))
            records = [{"sourceRow": 1, "pageKey": "row-0001-datart", "pageType": "Brand Category Page",
                        "brand": "SAMSUNG", "url": "https://www.datart.cz/lednicky/samsung"},
                       {"sourceRow": 2, "pageKey": "row-0002-datart", "pageType": "Brand Category Page",
                        "brand": "BOSCH", "url": "https://www.datart.cz/lednicky/bosch"},
                       {"sourceRow": 3, "pageKey": "row-0003-datart", "pageType": "Brand Category Page",
                        "brand": "LG", "url": "https://www.datart.cz/lednicky/lg"}]
            self.assertIn(1, redirected_brand_issues(batch, records))

    def test_http_language_redirect_uses_landing_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp)
            requested = "https://www.alza.cz/freezers/bosch/18852764-v1877.htm"
            final = "https://www.alza.cz/mrazaky/bosch/18852764-v1877.htm"
            metadata = {"url": final, "title": ["Mrazáky BOSCH"], "metaDescription": ["Bosch freezers"],
                        "h1": ["Mrazáky BOSCH"], "robots": ["index, follow"], "canonical": [final]}
            (page / "capture-state.json").write_text(json.dumps({"url": final, "initialMetadata": metadata}))
            (page / "response.json").write_text(json.dumps({"final_url": final}))
            (page / "raw.html").write_text("<html><head></head><body></body></html>")
            record = {"url": requested, "retailerSlug": "alza", "brand": "BOSCH"}
            id9, id10 = metadata_checks(record, page)
            self.assertEqual((id9["status"], id10["status"]), ("Y", "Y"))
            self.assertEqual(id9["evidence"]["moment"], "landing_after_http_redirect")

    def test_opened_navigation_page_without_title_is_still_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            batch = Path(tmp)
            target = batch / "navigator-sidebar-check"
            target.mkdir()
            key = "row-0038-datart"
            (target / f"{key}.json").write_text(json.dumps({
                "sourceRawHtmlSha256": "saved-page-hash",
                "targets": [{"url": "https://www.datart.cz/lednice-lg-s-pripojenim-na-vodu.html"}],
                "results": [{"url": "https://www.datart.cz/lednice-lg-s-pripojenim-na-vodu.html",
                             "status": 200, "title": "", "h1": "", "bodyLength": 6792}],
            }))
            result = sidebar_nav_check(batch, {"pageKey": key, "brand": "LG"}, "saved-page-hash")
            self.assertEqual(result["status"], "REVIEW")


if __name__ == "__main__":
    unittest.main()
