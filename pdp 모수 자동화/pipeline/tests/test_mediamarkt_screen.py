"""D124: 목록과 상세 제목 차이, 화면과 내부 값 불일치, 추천 상품 오탐을 검증한다."""
import unittest

from common import RunPaths
from s4_sellers import judge_page, load_rules


class MediaMarktScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(RunPaths("2026-11"))

    def judge(self, country, content, title="LG fridge", flag="false"):
        code, retailer = {"Hungary": ("hu", "Mediamarkt"), "Netherlands": ("nl", "MEDIAMARKT")}[country]
        item = {"country": country, "retailer": retailer, "url": f"https://www.mediamarkt.{code}/{code}/product/_lg-123.html", "title": "LG fridge"}
        html = (f'<h1>{title}</h1>{content}<script>{{"id":"Media:{code}:123","currency":"EUR",'
                f'"isProductOfTypeMarketplace":{flag},"marketplaceSeller":null}}</script>')
        return judge_page(item, html, self.rules, {})

    def test_detail_title_is_used_instead_of_list_title(self):
        for country, word in [("Hungary", "felújított"), ("Hungary", "használt"), ("Netherlands", "refurbished"), ("Netherlands", "tweede kans")]:
            with self.subTest(country=country, word=word):
                self.assertEqual(self.judge(country, "", title=f"LG {word} fridge")[1], "리퍼·중고")

    def test_external_screen_seller_wins_over_direct_internal_flag(self):
        for country, phrase in [("Hungary", "Értékesítő és szállító"), ("Netherlands", "Verkoop en verzending door")]:
            with self.subTest(country=country):
                body = f'<p>{phrase} <a href="/marketplace/seller/123">Example Shop</a></p>'
                self.assertEqual(self.judge(country, body)[:2], ("Example Shop", "외부판매자"))

    def test_tags_between_phrase_words(self):
        body = '<p><span>Értékesítő</span><b>és</b> szállító <a class="mms-third-party-provider-link" href="/marketplace/seller/123"><span>Bravosmart</span></a></p>'
        self.assertEqual(self.judge("Hungary", body)[:2], ("Bravosmart", "외부판매자"))

    def test_direct_seller_phrase_is_not_itself_an_exclusion(self):
        body = '<p>Verkoop en verzending door <a href="/marketplace/seller/123">MediaMarkt</a></p>'
        self.assertEqual(self.judge("Netherlands", body)[1], "직판")

    def test_seller_phrase_without_verified_link_is_unknown(self):
        body = '<p>Értékesítő és szállító <a href="/help">Help</a></p>'
        self.assertEqual(self.judge("Hungary", body)[1], "확인불가")

    def test_recommendation_and_description_sellers_are_ignored(self):
        for country, stop, phrase in [("Hungary", "Neked ajánljuk", "Értékesítő és szállító"), ("Hungary", "Termékleírás", "Értékesítő és szállító"), ("Netherlands", "Aanbevolen voor jou", "Verkoop en verzending door"), ("Netherlands", "Productbeschrijving", "Verkoop en verzending door")]:
            with self.subTest(country=country, stop=stop):
                body = f'<h2>{stop}</h2><p>{phrase} <a href="/marketplace/seller/123">Other Shop</a></p>'
                self.assertEqual(self.judge(country, body)[1], "직판")

    def test_hidden_and_specification_refurb_words_are_ignored(self):
        body = '<script>"Értékesítő és szállító": "Other Shop"</script><h2>Specifikáció</h2><p>Felújított: Nem</p>'
        self.assertEqual(self.judge("Hungary", body)[1], "직판")

    def test_plain_new_product_preserves_internal_direct_result(self):
        for country in ("Hungary", "Netherlands"):
            self.assertEqual(self.judge(country, "")[1], "직판")

    def test_group_shop_refurbished_offer_is_not_labelled_external_new_stock(self):
        body = ('<div data-test="mms-pdp-offer-selection"><div data-test="mms-product-price">'
                'Verkoop en verzending door <a href="/marketplace/seller/1">Media Markt Alkmaar</a></div>'
                '<span>Refurbished: Zeer goed</span></div>')
        result = self.judge("Netherlands", body)
        self.assertEqual(result[:2], ("Media Markt Alkmaar", "리퍼·중고"))
        self.assertIn("Refurbished: Zeer goed", result[2])

    def test_other_offer_refurbished_label_does_not_change_main_offer_kind(self):
        body = ('<div data-test="mms-pdp-offer-selection">Verkoop en verzending door '
                '<a href="/marketplace/seller/1">Other Shop</a><p>Ook refurbished beschikbaar</p></div>'
                '<h2>Aanbevolen voor jou</h2><span>Refurbished: Zeer goed</span>')
        self.assertEqual(self.judge("Netherlands", body)[1], "외부판매자")

    def test_missing_detail_heading_cannot_be_confirmed_direct(self):
        for country, retailer, code in [("Hungary", "Mediamarkt", "hu"), ("Netherlands", "MEDIAMARKT", "nl"), ("Spain", "MEDIAMARKT", "es")]:
            with self.subTest(country=country):
                item = {"country": country, "retailer": retailer, "url": f"https://www.mediamarkt.{code}/{code}/product/_lg-1.html", "title": "LG fridge"}
                html = f'<script>{{"id":"Media:{code}:1","currency":"EUR","isProductOfTypeMarketplace":false,"marketplaceSeller":null}}</script>'
                self.assertEqual(judge_page(item, html, self.rules, {})[1], "확인불가")


if __name__ == "__main__":
    unittest.main()
