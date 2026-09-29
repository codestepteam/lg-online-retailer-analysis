#!/usr/bin/env python3
"""Protect the ID8 scope distinction between product images and decoration."""

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_id8_images.py"
SPEC = importlib.util.spec_from_file_location("audit_id8_images", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ImageScopeTests(unittest.TestCase):
    def test_product_image_is_included_even_when_aria_hidden(self):
        ancestors = [("main", {}), ("div", {"class": "product-card"})]
        scope, reason, _, signal = MODULE.classify({"alt": "", "aria-hidden": "true"}, ancestors, "/fridge.jpg")
        self.assertEqual(scope, "포함")
        self.assertEqual(reason, "제품 카드 이미지")
        self.assertEqual(signal, "aria-hidden=true")

    def test_marketing_image_inside_product_grid_is_excluded(self):
        ancestors = [("main", {}), ("div", {"class": "product-box"}), ("div", {"class": "amp-banner"})]
        scope, _, _, _ = MODULE.classify({"alt": "sale"}, ancestors, "/promotion.jpg")
        self.assertEqual(scope, "제외")

    def test_empty_alt_alone_does_not_make_image_decorative(self):
        scope, _, _, _ = MODULE.classify({"alt": ""}, [("main", {})], "/fridge.jpg")
        self.assertEqual(scope, "포함")


if __name__ == "__main__":
    unittest.main()
