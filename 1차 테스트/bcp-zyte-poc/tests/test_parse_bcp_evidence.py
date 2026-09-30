import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "parse_bcp_evidence.py"
SPEC = importlib.util.spec_from_file_location("parse_bcp_evidence", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ParserTests(unittest.TestCase):
    def test_extracts_headings_components_and_faq_json_ld(self):
        html = """
        <html><body>
          <section class="brand-hero"><h1>LG Refrigerators</h1></section>
          <section id="why-lg"><h2>Why choose LG?</h2><p>Reliable cooling.</p></section>
          <section class="technology"><h2>DoorCooling technology</h2></section>
          <details><summary>How cold?</summary><p>Four degrees.</p></details>
          <script type="application/ld+json">
          {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How cold?","acceptedAnswer":{"@type":"Answer","text":"Four degrees."}}]}
          </script>
        </body></html>
        """
        parser = MODULE.RawHtmlEvidenceParser()
        parser.feed(html)
        parser.close()
        self.assertTrue(parser.components["hero"])
        self.assertTrue(MODULE.keyword_matches(parser.headings, "why_lg"))
        self.assertTrue(MODULE.keyword_matches(parser.headings, "usp"))
        self.assertEqual(MODULE.faq_json_ld(parser.json_ld)[0]["questions"][0]["question"], "How cold?")
        self.assertIn("How cold?", parser.details[0]["text"])

    def test_top_images_uses_visible_loaded_rendered_area(self):
        state = {"images": [
            {"src": "small", "visible": True, "loaded": True, "renderedArea": 100, "naturalArea": 500},
            {"src": "large", "visible": True, "loaded": True, "renderedArea": 900, "naturalArea": 200},
            {"src": "hidden", "visible": False, "loaded": True, "renderedArea": 9999, "naturalArea": 9999},
        ]}
        images, count = MODULE.top_images(state, "renderedArea")
        self.assertEqual(count, 2)
        self.assertEqual([image["src"] for image in images], ["large", "small"])

    def test_metric_is_explicitly_not_assessed(self):
        value = MODULE.metric("ID10", {"canonical": ["https://example.com/"]})
        self.assertEqual(value["assessment"]["status"], "not_assessed")
        self.assertIsNone(value["assessment"]["value"])

    def test_id18_keeps_browser_positions_without_assigning_a_verdict(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory) / "batch"
            page = batch / "pages" / "row-0014-alza" / "brand-category"
            page.mkdir(parents=True)
            (page / "raw.html").write_text("<html><body><main><h1>LG</h1></main></body></html>")
            snapshots = {"before_scroll": {"url": "https://example.com/lg", "candidates": [
                {"kind": "image", "documentTop": 149, "width": 1084, "height": 363}
            ]}}
            (page / "capture-state.json").write_text(json.dumps({
                "url": "https://example.com/lg", "metadata": {}, "images": [],
                "heroEvidence": {"version": "id18-candidates-v1", "snapshots": snapshots},
            }))
            (page / "response.json").write_text(json.dumps({
                "ok": True, "requested_url": "https://example.com/lg", "final_url": "https://example.com/lg",
            }))
            detail, _ = MODULE.parse_page(page, batch / "parsed")
            id18 = detail["metrics"]["ID18"]
            self.assertEqual(id18["evidence"]["renderedCandidateSnapshots"], snapshots)
            self.assertEqual(id18["assessment"]["status"], "not_assessed")


if __name__ == "__main__":
    unittest.main()
