import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_bcp_links import selected_links  # noqa: E402


class SelectedLinkTests(unittest.TestCase):
    def test_alza_navigation_uses_full_href_from_captured_html(self):
        batch = ROOT / "results_population" / "20260928-all-159"
        if not (batch / "manifest.json").is_file():
            self.skipTest("population capture not present")
        manifest = json.loads((batch / "manifest.json").read_text())
        record = next(r for r in manifest["records"] if r["sourceRow"] == 14)
        links = selected_links(batch, record)
        upper_freezer = next(x for x in links if "lednice-s-mrazakem-nahore" in x["url"])
        self.assertEqual(
            upper_freezer["url"],
            "https://www.alza.cz/lednice-s-mrazakem-nahore/lg/18865689-v1357.htm",
        )
        self.assertEqual(len([x for x in links if x["kind"] == "navigator"]), 7)


if __name__ == "__main__":
    unittest.main()
