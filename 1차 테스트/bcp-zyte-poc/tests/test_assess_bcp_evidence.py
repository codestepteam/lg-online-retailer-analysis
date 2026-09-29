#!/usr/bin/env python3
"""Check the confirmed metadata and canonical decisions, including edge cases."""

import importlib.util
import hashlib
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "assess_bcp_evidence.py"
SPEC = importlib.util.spec_from_file_location("assess_bcp_evidence", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AssessmentTests(unittest.TestCase):
    def test_id9_requires_all_four_fields_and_index_follow(self):
        complete = {
            "title": "LG refrigerators", "metaDescription": ["LG range"],
            "h1": ["LG refrigerators"], "robots": ["index, follow"],
        }
        self.assertEqual(MODULE.assess_id9(complete)["status"], "Y")
        self.assertEqual(MODULE.assess_id9({**complete, "h1": []})["status"], "N")
        self.assertEqual(MODULE.assess_id9({**complete, "robots": ["noindex,follow"]})["status"], "N")
        self.assertEqual(MODULE.assess_id9({**complete, "robots": ["NOODP"]})["status"], "N")

    def test_conflicting_metadata_needs_review(self):
        data = {
            "title": "LG refrigerators", "metaDescription": ["first", "second"],
            "h1": ["LG refrigerators"], "robots": ["index, follow"],
        }
        self.assertEqual(MODULE.assess_id9(data)["status"], "REVIEW")

    def test_id10_checks_tag_presence_even_with_empty_href(self):
        self.assertEqual(MODULE.assess_id10('<link rel="canonical" href="">')["status"], "Y")
        self.assertIn("비어", MODULE.assess_id10('<link rel="canonical" href="">')["warnings"][0])
        self.assertEqual(MODULE.assess_id10('<link rel="alternate" href="/">')["status"], "N")
        self.assertEqual(MODULE.assess_id10('<link rel="alternate canonical" href="/">')["status"], "Y")

    def test_initial_metadata_prevents_paginated_page_false_negative(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            page_dir = batch / "pages" / "example" / "brand-category"
            parsed_dir = batch / "parsed" / "example"
            page_dir.mkdir(parents=True)
            parsed_dir.mkdir(parents=True)
            initial = {
                "url": "https://example.com/lg",
                "title": ["LG refrigerators"], "metaDescription": ["LG range"],
                "h1": ["LG refrigerators"], "robots": ["index, follow"],
                "canonical": ["https://example.com/lg"],
            }
            final = {
                "title": "LG refrigerators", "metaDescription": ["LG range"],
                "h1": ["LG refrigerators"], "robots": ["noindex,follow"],
            }
            state_path = page_dir / "capture-state.json"
            state_path.write_text(json.dumps({"initialMetadata": initial, "metadata": final}))
            (page_dir / "raw.html").write_text('<link rel="canonical" href="https://example.com/lg?page=4">')
            metrics = {metric_id: {"evidence": {}} for metric_id in MODULE.METRIC_IDS}
            evidence_path = parsed_dir / "bcp-evidence.json"
            evidence_path.write_text(json.dumps({"page": {
                "retailer": "example", "collectionOk": True,
                "requestedUrl": "https://example.com/lg", "finalUrl": "https://example.com/lg?page=4",
            }, "metrics": metrics}))

            assessment, _ = MODULE.assess_page(batch, evidence_path)
            self.assertEqual(assessment["results"]["ID9"]["status"], "Y")
            self.assertEqual(assessment["results"]["ID10"]["status"], "Y")
            self.assertEqual(assessment["results"]["ID9"]["evidence"]["metadataMoment"], "before_scroll")

            state_path.write_text(json.dumps({"metadata": final}))
            old_assessment, _ = MODULE.assess_page(batch, evidence_path)
            self.assertEqual(old_assessment["results"]["ID9"]["status"], "REVIEW")
            self.assertEqual(old_assessment["results"]["ID9"]["evidence"]["capturedFinalPageStatus"], "N")

    def test_id8_manual_review_is_locked_to_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            source = batch / "pages" / "example" / "brand-category"
            source.mkdir(parents=True)
            state = source / "capture-state.json"
            raw = source / "raw.html"
            state.write_text('{"images": []}')
            raw.write_text('<main><img alt="LG fridge" src="/lg.jpg"></main>')
            audit = batch / "id8-audit"
            audit.mkdir()
            (audit / "example.json").write_text(json.dumps({"top10": [{"index": 1, "alt": "LG fridge", "scopeSuggestion": "포함"}]}))
            (batch / "ID8_판정_검수.json").write_text(json.dumps({"reviewStatus": "AI 검수", "pages": {"example": {
                "decision": "Y", "reason": "이미지 설명 확인", "selectedImageIndices": [1],
                "captureStateSha256": hashlib.sha256(state.read_bytes()).hexdigest(),
                "rawHtmlSha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
            }}}))
            self.assertEqual(MODULE.assess_id8(batch, "example", source)["status"], "Y")
            raw.write_text(raw.read_text() + " changed")
            self.assertEqual(MODULE.assess_id8(batch, "example", source)["status"], "REVIEW")

    def test_unchanged_url_uses_final_metadata_not_svg_title(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            source = batch / "pages" / "example" / "brand-category"
            parsed = batch / "parsed" / "example"
            source.mkdir(parents=True)
            parsed.mkdir(parents=True)
            url = "https://example.com/lg"
            common = {"metaDescription": ["LG range"], "h1": ["LG refrigerators"],
                      "robots": ["index, follow"], "canonical": [url]}
            (source / "capture-state.json").write_text(json.dumps({
                "initialMetadata": {**common, "url": url, "title": ["LG refrigerators", "Filter"]},
                "metadata": {**common, "title": "LG refrigerators"},
            }))
            (source / "raw.html").write_text(f'<link rel="canonical" href="{url}">')
            evidence = parsed / "bcp-evidence.json"
            evidence.write_text(json.dumps({
                "page": {"retailer": "example", "collectionOk": True,
                         "requestedUrl": url, "finalUrl": url},
                "metrics": {metric_id: {"evidence": {}} for metric_id in MODULE.METRIC_IDS},
            }))
            assessment, _ = MODULE.assess_page(batch, evidence)
            self.assertEqual(assessment["results"]["ID9"]["status"], "Y")
            self.assertEqual(assessment["results"]["ID9"]["evidence"]["metadataMoment"], "captured_final_page")


if __name__ == "__main__":
    unittest.main()
