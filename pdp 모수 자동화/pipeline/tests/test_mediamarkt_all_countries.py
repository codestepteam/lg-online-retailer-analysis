"""MediaMarkt 네 나라에 OSM 면제 없이 PDP 직접 검사와 현지 제목 검사가 연결되는지 확인한다."""
import unittest

from common import RunPaths, load_config
from s3_pages import plan_pages
from s4_sellers import judge_page, load_rules

RUN = RunPaths("2026-11")


class MediaMarktAllCountries(unittest.TestCase):
    def test_osm_and_search_both_plan_direct_pdp_visits(self):
        targets = [t for t in load_config(RUN, "targets")["targets"] if t["retailer"].lower() == "mediamarkt"]
        self.assertEqual({t["country"] for t in targets}, {"Spain", "Germany", "Hungary", "Netherlands"})
        rows = [{"국가": t["country"], "리테일러": t["retailer"], "URL": f'https://example.com/{t["country"]}/1',
                 "흐름": "OSM" if t["country"] in ("Spain", "Germany") else "검색", "판정": "남김"} for t in targets]
        common = load_config(RUN, "retailer_rules")["common"]
        planned = plan_pages(rows, targets, common["page_status"], common["page_fetch"])
        self.assertEqual({p["country"] for p in planned}, {r["국가"] for r in rows})
        self.assertEqual(len(planned), 4)

    def test_detail_title_is_checked_for_each_country(self):
        rules = load_rules(RUN)
        cases = [("Spain", "MEDIAMARKT", "es", "REACONDICIONADO"), ("Germany", "MEDIAMARKT", "de", "Generalüberholt"),
                 ("Hungary", "Mediamarkt", "hu", "felújított"), ("Netherlands", "MEDIAMARKT", "nl", "refurbished")]
        for country, retailer, code, word in cases:
            with self.subTest(country=country):
                item = {"country": country, "retailer": retailer, "url": f"https://www.mediamarkt.{code}/{code}/product/_lg-1.html", "title": "LG fridge"}
                html = f'<h1>LG fridge {word}</h1><script>{{"id":"Media:{code}:1","currency":"EUR","isProductOfTypeMarketplace":false,"marketplaceSeller":null}}</script>'
                self.assertEqual(judge_page(item, html, rules, {})[1], "리퍼·중고")

    def test_main_seller_phrase_is_checked_for_each_country(self):
        rules = load_rules(RUN)
        cases = [("Spain", "MEDIAMARKT", "es", "Vendido y enviado por"), ("Germany", "MEDIAMARKT", "de", "Verkauf und Versand durch"),
                 ("Hungary", "Mediamarkt", "hu", "Értékesítő és szállító"), ("Netherlands", "MEDIAMARKT", "nl", "Verkoop en verzending door")]
        for country, retailer, code, phrase in cases:
            with self.subTest(country=country):
                item = {"country": country, "retailer": retailer, "url": f"https://www.mediamarkt.{code}/{code}/product/_lg-1.html", "title": "LG fridge"}
                html = f'<h1>LG fridge</h1><p>{phrase} <a href="/marketplace/seller/1">Other Shop</a></p><script>{{"id":"Media:{code}:1","currency":"EUR","isProductOfTypeMarketplace":false,"marketplaceSeller":null}}</script>'
                self.assertEqual(judge_page(item, html, rules, {})[:2], ("Other Shop", "외부판매자"))

    def test_legacy_fallback_cannot_read_recommendation_seller(self):
        rules = load_rules(RUN)
        cases = [("Spain", "es", "Vendido y enviado por", "Recomendado para ti"),
                 ("Netherlands", "nl", "Verkoop en verzending door", "Aanbevolen voor jou")]
        for country, code, phrase, stop in cases:
            with self.subTest(country=country):
                item = {"country": country, "retailer": "MEDIAMARKT", "url": f"https://www.mediamarkt.{code}/{code}/product/_lg-1.html", "title": "LG fridge"}
                html = f'<h1>LG fridge</h1><h2>{stop}</h2><p data-test="additional-info-normal">{phrase} <a class="mms-third-party-provider-link" href="/marketplace/seller/1"><span>Other Shop</span></a></p><script>{{"id":"Media:{code}:1","currency":"EUR","isProductOfTypeMarketplace":false,"marketplaceSeller":null}}</script>'
                self.assertEqual(judge_page(item, html, rules, {})[1], "직판")


if __name__ == "__main__":
    unittest.main()
