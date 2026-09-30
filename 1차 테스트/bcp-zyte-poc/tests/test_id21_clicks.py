#!/usr/bin/env python3
"""Regressions for the ID21 click source and landing-quality gate."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_id21_clicks import cards_from_saved_source, click_request, landing_evidence, captured_landing


class Id21ClickTests(unittest.TestCase):
    def test_czech_card_text_and_real_click_action_are_preserved(self):
        source = (ROOT / "results_population" / "20260928-all-159" / "pages" /
                  "row-0038-datart" / "brand-category" / "raw.html").read_bytes()
        cards = cards_from_saved_source(source, "https://www.datart.cz/lednice-lg.html")
        self.assertEqual(len(cards), 11)
        card = next(c for c in cards if c["label"] == "S připojením na vodu")
        self.assertEqual(card["url"], "https://www.datart.cz/lednice-lg-s-pripojenim-na-vodu.html")
        request = click_request("https://www.datart.cz/lednice-lg.html", card)
        self.assertEqual(request["url"], "https://www.datart.cz/lednice-lg.html")
        self.assertEqual([a["action"] for a in request["actions"][-3:]],
                         ["waitForSelector", "click", "waitForTimeout"])

    def test_title_or_h1_is_not_enough_without_a_product_lineup(self):
        evidence = landing_evidence("<html><head><title>LG refrigerators</title></head>"
                                    "<body><main><h1>LG refrigerators</h1></main></body></html>")
        response = {"url": "https://www.datart.cz/lg-water", "statusCode": 200,
                    "actions": [{"action": "click", "status": "success"}]}
        card = {"url": "https://www.datart.cz/lg-water"}
        good, reasons = captured_landing(response, card, "https://www.datart.cz/lednice-lg.html", evidence)
        self.assertFalse(good)
        self.assertIn("no rendered product records were found on the landing page", reasons)

    def test_czech_code_prompt_is_recorded_as_captcha_not_empty_lineup(self):
        evidence = landing_evidence("<html><body><main>Opište kód z obrázku: submit</main></body></html>")
        response = {"url": "https://www.datart.cz/chytre-lednice-lg.html", "statusCode": 200,
                    "actions": [{"action": "click", "status": "success"}]}
        good, reasons = captured_landing(response, {}, "https://www.datart.cz/lednice-lg.html", evidence)
        self.assertFalse(good)
        self.assertIn("landing is a CAPTCHA or access challenge, not a product page", reasons)


if __name__ == "__main__":
    unittest.main()
