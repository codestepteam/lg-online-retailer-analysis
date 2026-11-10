import unittest
from verify_hungary_independent import extract


class SelectedProductStatus(unittest.TestCase):
    def page(self, state, extra=""):
        return ('<h1>LG washer</h1><div data-test="mms-pdp-offer-selection"><div data-test="mms-product-price">Price</div></div>'
                '<script>{"id":"Media:hu:1","isAvailableForDelivery":null,"onlineStatus":"' + state + '"}</script>' + extra)

    def test_permanent_state_is_caught_even_without_product_jsonld(self):
        result = extract(self.page("PERMANENTLY_NOT_AVAILABLE"), "https://www.mediamarkt.hu/hu/product/_lg-1.html", "refurbished")
        self.assertEqual(result["본상품판매상태"], "PERMANENTLY_NOT_AVAILABLE")
        self.assertEqual(result["직접연결상품요약수"], 0)

    def test_other_product_permanent_state_is_ignored(self):
        extra = '<script>{"id":"Media:hu:999","isAvailableForDelivery":null,"onlineStatus":"PERMANENTLY_NOT_AVAILABLE"}</script>'
        result = extract(self.page("AVAILABLE", extra), "https://www.mediamarkt.hu/hu/product/_lg-1.html", "refurbished")
        self.assertEqual(result["본상품판매상태"], "AVAILABLE")

    def test_recommendation_seller_link_is_ignored(self):
        extra = '<section><a href="/hu/marketplace/seller/999">Other Shop</a></section>'
        result = extract(self.page("AVAILABLE", extra), "https://www.mediamarkt.hu/hu/product/_lg-1.html", "refurbished")
        self.assertEqual(result["본상품판매자링크"], [])

    def test_missing_product_jsonld_does_not_imply_permanent_stock(self):
        result = extract(self.page("TEMPORARILY_NOT_AVAILABLE"), "https://www.mediamarkt.hu/hu/product/_lg-1.html", "refurbished")
        self.assertEqual(result["본상품판매상태"], "TEMPORARILY_NOT_AVAILABLE")


if __name__ == "__main__":
    unittest.main()
