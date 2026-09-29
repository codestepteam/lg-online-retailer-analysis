#!/usr/bin/env python3
"""Check URL adaptation without changing the saved representative recipes."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from adapt_bcp_recipe import adapt_recipe


class AdaptRecipeTests(unittest.TestCase):
    def test_standard_retailer_changes_request_and_config(self):
        original = json.loads((ROOT / "capture/recipes/coolblue/brand-category.json").read_text())
        changed = adapt_recipe(original, "https://www.coolblue.nl/wasmachines/lg")
        self.assertEqual(changed["request"]["url"], "https://www.coolblue.nl/wasmachines/lg")
        self.assertNotIn("https://www.coolblue.nl/koelkasten/lg", json.dumps(changed))
        self.assertEqual(original["request"]["url"], "https://www.coolblue.nl/koelkasten/lg")

    def test_amazon_entry_page_and_url_check(self):
        original = json.loads((ROOT / "capture/recipes/amazon-it/brand-category.json").read_text())
        new_url = "https://www.amazon.it/stores/page/045E563A-5374-463E-BFDB-E7E47BDBC9F6"
        changed = adapt_recipe(original, new_url)
        self.assertEqual(changed["request"]["url"], "https://www.amazon.it/")
        self.assertEqual(changed["target_url"], new_url)
        self.assertIn(new_url, [action.get("url") for action in changed["request"]["actions"]])
        self.assertEqual(changed["evidence"]["url_contains"], ["045E563A-5374-463E-BFDB-E7E47BDBC9F6"])

    def test_other_host_is_rejected(self):
        original = json.loads((ROOT / "capture/recipes/coolblue/brand-category.json").read_text())
        with self.assertRaises(ValueError):
            adapt_recipe(original, "https://www.amazon.it/stores/page/test")


if __name__ == "__main__":
    unittest.main()
