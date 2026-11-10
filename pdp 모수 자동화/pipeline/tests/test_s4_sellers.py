"""WP6 판매자 판정: 10월에 사람이 고친 결과를 그대로 재현하는지, 고친 결함이 다시 생기지 않는지 본다."""
import csv
import glob
import gzip
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import common
import s4_sellers as s4
from rules.sellers import group1, group4

RUN = common.RunPaths("2026-11")
RULES = s4.load_rules(RUN)
OUTPUTS = common.REPO_ROOT / "outputs"
MM_DE = OUTPUTS / "mediamarkt-de-v4-20261106"
SHARAF = OUTPUTS / "sharaf-157-20261105" / "v3_included_25_saudivpn_상품화면판매자_20261105.csv"


def item(country, retailer, url="https://x/p/1", title=""):
    return {"url": url, "country": country, "retailer": retailer, "title": title, "html_file": "a.html"}


def judged(country, retailer, html, **kwargs):
    return s4.judge_page(item(country, retailer, **kwargs), html, RULES, {})


class Table(unittest.TestCase):
    def test_every_target_has_a_function(self):
        targets = {f"{entry['country']}|{entry['retailer']}" for entry in common.load_config(RUN, "targets")["targets"]}
        self.assertEqual(len(targets), 35)
        self.assertEqual(targets, set(RULES["functions"]))

    def test_unknown_function_name_stops(self):
        settings = {"sellers": {"functions": {"a|b": "없는함수"}}}
        with mock.patch.object(s4, "load_config", side_effect=lambda run, name: settings if name == "retailer_rules" else {"sellers": {}}):
            with self.assertRaises(common.ConfigError):
                s4.load_rules(RUN)

    def test_retailer_without_function_is_presumed_direct(self):
        name, kind, evidence = judged("Nowhere", "COOLBLUE", "<html></html>")
        self.assertEqual((name, kind), ("Coolblue", "직판"))
        self.assertEqual(evidence, RULES["no_function_evidence"])


@unittest.skipUnless(MM_DE.exists(), "10월 재검토 HTML 없음")
class GermanMediaMarkt(unittest.TestCase):
    """K6: 사람이 11월 화면으로 확인한 195건이 그대로 나와야 한다."""

    @classmethod
    def setUpClass(cls):
        _, rows = common.read_csv(glob.glob(str(MM_DE / "*현재화면점검.csv"))[0])
        cls.rows = [(row, judged("Germany", "MEDIAMARKT", cls.page(row["확인 요청 URL"]), url=row["확인 요청 URL"])) for row in rows]

    @staticmethod
    def page(url):
        path = MM_DE / "current_html" / (hashlib.sha256(url.encode()).hexdigest()[:16] + ".html.gz")
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as stream:
            return stream.read()

    def test_all_195_decisions_match(self):
        self.assertEqual(len(self.rows), 195)
        for row, result in self.rows:
            self.assertEqual(result[1] != "직판", row["확인상태"] == "제외", row["확인 요청 URL"])
            self.assertNotEqual(result[1], "확인불가", row["확인 요청 URL"])

    def test_excluded_seller_names_match(self):
        excluded = [(row, result) for row, result in self.rows if row["확인상태"] == "제외"]
        self.assertEqual(len(excluded), 13)
        for row, result in excluded:
            self.assertEqual(result[0], row["현재_본상품_판매자"])

    def test_inspected_stock_is_refurbished(self):
        refurbished = [row for row, result in self.rows if result[1] == "리퍼·중고"]
        self.assertEqual(len(refurbished), 3)
        self.assertEqual({row["현재_본상품_판매자"] for row in refurbished}, {"MediaMarktSaturn geprüft"})


def sharaf_page(sold_by, first_seller="Sharaf DG"):
    return (f'<html><head><script>var d={{"seller_name":"{first_seller}"}}</script></head><body><h1>LG Fridge</h1>'
            f'<div><span>Sold by</span> <span>{sold_by}</span></div><div>Fulfilled by Sharaf DG</div></body></html>')


class Sharaf(unittest.TestCase):
    """K1: 스크립트의 첫 seller_name이 아니라 본 상품 영역의 Sold by를 읽는다. 실제 HTML은 없어 화면 기록으로 만든 시험용 페이지다."""

    @unittest.skipUnless(SHARAF.exists(), "Sharaf 조사표 없음")
    def test_25_screen_records_reproduce(self):
        _, rows = common.read_csv(SHARAF)
        self.assertEqual(len(rows), 25)
        outcomes = [judged("UAE", "Sharaf DG", sharaf_page(row["상품판매영역_판매자"])) for row in rows]
        for row, result in zip(rows, outcomes):
            self.assertEqual(result[0], row["상품판매영역_판매자"])
        self.assertEqual(sum(result[1] == "직판" for result in outcomes), 16)
        self.assertEqual(sum(result[1] == "외부판매자" for result in outcomes), 9)

    def test_first_seller_name_in_script_is_ignored(self):
        self.assertEqual(judged("UAE", "Sharaf DG", sharaf_page("HOME STORE"))[:2], ("HOME STORE", "외부판매자"))

    def test_seller_and_fulfilled_in_one_text(self):
        self.assertEqual(judged("UAE", "Sharaf DG", "<h1>x</h1><p>Sold by Applianzee Fulfilled by Sharaf DG</p>")[:2], ("Applianzee", "외부판매자"))

    def test_no_sold_by_is_unknown_even_if_script_says_sharaf(self):
        html = '<script>{"seller_name":"Sharaf DG"}</script><h1>x</h1><p>Fulfilled by Sharaf DG</p>'
        self.assertEqual(judged("UAE", "Sharaf DG", html)[1], "확인불가")

    def test_recommendations_are_not_read(self):
        self.assertEqual(judged("UAE", "Sharaf DG", "<h1>x</h1><div>You may also like</div><p>Sold by Other</p>")[1], "확인불가")


class Darty(unittest.TestCase):
    def test_marketplace_url_with_only_darty_meta_is_not_called_direct(self):
        html = '<meta itemprop="seller" content="Darty">'
        self.assertEqual(judged("France", "DARTY", html, url="https://d/p.html?ofmp=123")[1], "확인불가")

    def test_plain_url_with_darty_meta_is_direct(self):
        self.assertEqual(judged("France", "DARTY", '<meta itemprop="seller" content="Darty">')[:2], ("Darty", "직판"))

    def test_screen_block_wins_over_meta(self):
        html = '<div class="product-mkp-seller-info"><a class="mkp-seller-name x">Boutique</a></div><meta itemprop="seller" content="Darty">'
        self.assertEqual(judged("France", "DARTY", html, url="https://d/p.html?ofmp=1")[:2], ("Boutique", "외부판매자"))


class Lazada(unittest.TestCase):
    def rules(self):
        return {**RULES, "lazada_items": {"Thailand|123": {"seller": "LG Store", "kind": "브랜드공식점", "evidence": "화면"}}}

    def test_item_id_rule(self):
        self.assertEqual(group4.lazada_item_id("https://l/p-i123-s456.html"), "123")
        self.assertEqual(group4.lazada_item_id("https://l/p-i123.html?x=1"), "123")

    def test_known_item_says_october_value(self):
        result = group4.lazada(item("Thailand", "LAZADA", url="https://l/p-i123-s9.html"), '"sellerId":"777"', self.rules())
        self.assertEqual(result[:2], ("LG Store", "브랜드공식점"))
        self.assertIn("11월 화면 아님", result[2])

    def test_same_seller_number_is_not_joined(self):
        result = group4.lazada(item("Thailand", "LAZADA", url="https://l/p-i999-s9.html"), '"sellerId":"777"', self.rules())
        self.assertEqual(result[1], "확인불가")

    def test_october_table_has_no_blank_seller(self):
        self.assertEqual(len(RULES["lazada_items"]), 624)
        self.assertTrue(all(value["seller"] and value["kind"] for value in RULES["lazada_items"].values()))


class OtherRetailers(unittest.TestCase):
    def test_falabella_seller_name(self):
        self.assertEqual(judged("Chile", "FALABELLA", '"sellerName":"FALABELLA"')[1], "직판")
        self.assertEqual(judged("Chile", "FALABELLA", '"sellerName":"TOTTUS"')[:2], ("TOTTUS", "외부판매자"))

    def test_magalu_screen_text(self):
        self.assertEqual(judged("Brazil", "MAGAZINELUIZA", "<p>Vendido por LG Store e entregue por Magalu</p>")[:2], ("LG Store", "외부판매자"))
        self.assertEqual(judged("Brazil", "MAGAZINELUIZA", "<p>Vendido por Magalu e entregue por Magalu</p>")[1], "직판")

    def test_appliance_online_shell_is_unknown(self):
        html = '<link id="canonicalLink" rel="canonical" href="https://www.appliancesonline.com.au/">'
        self.assertEqual(judged("Australia", "Appliance Online", html)[1], "확인불가")

    def test_marketplace_without_name_is_excluded_kind(self):
        html = '"id":"Media:hu:1","currency":"HUF","isProductOfTypeMarketplace":true,"marketplaceSeller":null'
        name, kind, evidence = judged("Hungary", "Mediamarkt", html, url="https://m/p-1.html")
        self.assertEqual((name, kind), ("", "외부판매자"))
        self.assertIn("D070", evidence)

    def test_spanish_refurbished_title_overrides_direct(self):
        html = '<h1>Frigorífico REACONDICIONADO</h1>"id":"Media:es:1","currency":"EUR","isProductOfTypeMarketplace":false,"marketplaceSeller":null'
        self.assertEqual(judged("Spain", "MEDIAMARKT", html, url="https://m/p-1.html")[1], "리퍼·중고")

    def test_boulanger_order_matches_october(self):
        block = '<p id="product-merchant__condition">Occasion vendu &amp; expédié par <a title="{}">x</a></p>'
        self.assertEqual(group1.boulanger(item("France", "BOULANGER"), block.format("Boulanger"), RULES)[1], "직판")
        self.assertEqual(group1.boulanger(item("France", "BOULANGER"), block.format("Shop"), RULES)[1], "리퍼·중고")

    def test_el_corte_ingles_name_with_comma(self):
        html = '"_single_sku":{"provider":"x","provider_name":"Tienda, S.L.","marketplace":true}'
        self.assertEqual(judged("Spain", "ELCORTEINGLES_ELECTRONICA", html)[:2], ("Tienda, S.L.", "외부판매자"))


class ContextFunctions(unittest.TestCase):
    def test_amazon_used_box_finds_name_from_other_pages(self):
        first = '<div id="merchantInfoFeature_feature_div"><a href="/x?seller=AAA">Shop A</a></div>'
        used = '<div id="buybox"><span>Gebraucht</span><input id="merchantID" name="merchantID" value="AAA"></div>'
        pages = {"1": first, "2": used}
        items = [item("Germany", "AMAZON", url=number) for number in pages]
        rows, _ = s4.judge_all(items, lambda entry: pages[entry["url"]], RULES)
        self.assertEqual((rows[1]["판매자"], rows[1]["판매자구분"]), ("Shop A", "리퍼·중고"))

    def test_amazon_options_only_keeps_distinct_evidence(self):
        html = '<div id="buybox"><a>Alle Kaufoptionen anzeigen</a></div>'
        result = judged("Germany", "AMAZON", html)
        self.assertEqual((result[1], result[2]), ("확인불가", RULES["amazon"]["options_only_evidence"]))

    def test_momo_shell_page_uses_shop_seen_elsewhere(self):
        full = '"shop":{"name":"Shop M","x":1,"entpCode":"TP0001"}'
        pages = {"https://m/TP/TP0001/goodsDetail/1": "<html></html>", "https://m/full": full}
        items = [item("Taiwan", "MOMOSHOP", url=url) for url in pages]
        rows, _ = s4.judge_all(items, lambda entry: pages[entry["url"]], RULES)
        self.assertEqual(rows[0]["판매자"], "Shop M")
        self.assertIn("추정", rows[0]["근거"])


class Pipeline(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.run_paths = common.RunPaths("2026-11", Path(folder.name)).create()
        for name in ("retailer_rules", "lazada_sellers"):
            (self.run_paths.sub("config") / f"{name}.json").write_text((RUN.sub("config") / f"{name}.json").read_text(encoding="utf-8"), encoding="utf-8")
        for target, value in (("get_logger", mock.Mock()), ("RunPaths", self.run_paths)):
            patcher = mock.patch.object(s4, target, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.judgments = self.run_paths.sub("judgments")

    def write_pages(self, *pages):
        with (self.judgments / "pages.jsonl").open("w", encoding="utf-8") as stream:
            for page in pages:
                stream.write(json.dumps(page, ensure_ascii=False) + "\n")

    def page(self, url, status="정상", html_file="a.html"):
        return {"url": url, "country": "Chile", "retailer": "FALABELLA", "status": status, "final_url": url, "title": "t", "canonical": "", "html_file": html_file}

    def output(self):
        with (self.judgments / "sellers.csv").open(encoding="utf-8-sig", newline="") as stream:
            return list(csv.DictReader(stream))

    def test_only_normal_pages_with_columns_in_order(self):
        (self.run_paths.sub("html") / "a.html").write_text('"sellerName":"FALABELLA"', encoding="utf-8")
        self.write_pages(self.page("https://f/1"), self.page("https://f/2", status="페이지없음"))
        s4.main(["--month", "2026-11"])
        rows = self.output()
        self.assertEqual([row["요청URL"] for row in rows], ["https://f/1"])
        self.assertEqual(list(rows[0]), s4.COLUMNS)
        self.assertEqual(rows[0]["판매자구분"], "직판")

    def test_gzip_html_is_read(self):
        with gzip.open(self.run_paths.sub("html") / "b.html.gz", "wt", encoding="utf-8") as stream:
            stream.write('"sellerName":"TOTTUS"')
        self.write_pages(self.page("https://f/1", html_file="b.html.gz"))
        s4.main(["--month", "2026-11"])
        self.assertEqual(self.output()[0]["판매자"], "TOTTUS")

    def test_missing_html_is_unknown_not_a_crash(self):
        self.write_pages(self.page("https://f/1", html_file="없음.html"))
        s4.main(["--month", "2026-11"])
        self.assertEqual(self.output()[0]["판매자구분"], "확인불가")

    def manual(self, url, kind="직판"):
        common.write_csv(self.judgments / "sellers_manual.csv", s4.COLUMNS, [dict(zip(s4.COLUMNS, (url, "Chile", "FALABELLA", "사람", kind, "사람 확인")))])

    def test_manual_table_overrides(self):
        self.write_pages(self.page("https://f/1", html_file="없음.html"))
        self.manual("https://f/1")
        s4.main(["--month", "2026-11"])
        self.assertEqual(self.output()[0]["판매자"], "사람")

    def test_manual_unknown_url_stops(self):
        self.write_pages(self.page("https://f/1", html_file="없음.html"))
        self.manual("https://f/없는주소")
        with self.assertRaises(common.ConfigError):
            s4.main(["--month", "2026-11"])

    def test_manual_bad_kind_stops(self):
        self.write_pages(self.page("https://f/1", html_file="없음.html"))
        self.manual("https://f/1", kind="이상한값")
        with self.assertRaises(common.ConfigError):
            s4.main(["--month", "2026-11"])

    def test_existing_output_is_not_overwritten_without_force(self):
        (self.run_paths.sub("html") / "a.html").write_text('"sellerName":"FALABELLA"', encoding="utf-8")
        self.write_pages(self.page("https://f/1"))
        s4.main(["--month", "2026-11"])
        (self.run_paths.sub("html") / "a.html").write_text('"sellerName":"TOTTUS"', encoding="utf-8")
        s4.main(["--month", "2026-11"])
        self.assertEqual(self.output()[0]["판매자"], "FALABELLA")
        s4.main(["--month", "2026-11", "--force"])
        self.assertEqual(self.output()[0]["판매자"], "TOTTUS")


if __name__ == "__main__":
    unittest.main()
