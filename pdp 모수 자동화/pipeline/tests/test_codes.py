"""검색 행 브랜드·제품코드 추출: 설정 연결과, 페이지가 있을 때 페이지 값을 먼저 쓰는지를 작은 가짜 HTML로 본다."""
import json
import pathlib
import shutil
import tempfile
import unittest
from unittest import mock

import common
import s2_filter as s2
import s5_judge as s5
from rules import codes
from rules.codes import retailers

RUN = common.RunPaths("2026-11")
CONFIG = common.load_config(RUN, "product_codes")


def row(name, number="1", country="Czech Republic", retailer="ALZA", url="https://x/1"):
    return {"행번호": number, "국가": country, "리테일러": retailer, "상품명": name, "URL": url}


def run(shop, name, html=None, url="https://x/1"):
    country, retailer = shop.split("|")
    return codes.extract([row(name, country=country, retailer=retailer, url=url)], lambda _: html, CONFIG)["1"]


def ld(data):
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


class Config(unittest.TestCase):
    def test_every_search_target_has_a_function(self):
        shops = {f"{t['country']}|{t['retailer']}" for t in common.load_config(RUN, "targets")["targets"] if t["flow"] == "검색"}
        self.assertEqual(shops, set(CONFIG["retailers"]))
        codes.check_config(CONFIG)

    def test_unknown_retailer_stops(self):
        with self.assertRaises(common.ConfigError):
            codes.extract([row("x", retailer="NOPE")], lambda _: None, CONFIG)

    def test_unknown_function_stops(self):
        with self.assertRaises(common.ConfigError):
            codes.check_config({"retailers": {"a|b": {"function": "nope"}}})


class NameOnly(unittest.TestCase):
    """페이지가 없는 행은 상품명에서만 찾는다."""

    def test_alza(self):
        self.assertEqual(run("Czech Republic|ALZA", "LG GBBS322APY chladnička"), ("LG", "GBBS322APY", "상품명", "상품명"))

    def test_worten_cuts_parenthesis(self):
        self.assertEqual(run("Portugal|Worten", "Frigorífico LG GBB72NSVCN (Modelo X123456)")[:2], ("LG", "GBB72NSVCN"))

    def test_appliance_online_end_of_name(self):
        self.assertEqual(run("Australia|Appliance Online", "Bosch Series 8 9kg Front Load Washing Machine WGG24403AU")[:2], ("BOSCH", "WGG24403AU"))

    def test_mediamarkt_brand_at_start(self):
        self.assertEqual(run("Netherlands|MEDIAMARKT", "SAMSUNG RB38C607AB1 Koelkast")[:2], ("SAMSUNG", "RB38C607AB1"))

    def test_cairo_arabic_brand(self):
        self.assertEqual(run("Egypt|Cairo Sales", "ثلاجة سامسونج RT38CG6000B")[:2], ("SAMSUNG", "RT38CG6000B"))

    def test_falabella_brand_from_address(self):
        result = run("Peru|FALABELLA", "Refrigeradora 300 litros", url="https://x/product/123/Refrigeradora-Samsung-300")
        self.assertEqual(result[0], "SAMSUNG")
        self.assertEqual(result[2], "URL")

    def test_electroplanet_brand_at_end(self):
        self.assertEqual(run("Morocco|Electroplanet", "REFRIGERATEUR GR-B392PLGB LG")[:2], ("LG", "GR-B392PLGB"))


class PageFirst(unittest.TestCase):
    """페이지가 있으면 페이지 값을 먼저 쓴다(10월 페이지가 남아 있지 않아 모양을 흉내 낸 작은 HTML로 확인)."""

    def test_alza_uses_mpn_and_cuts_lg_tail(self):
        html = '"brand":{"@type":"Brand","name":"LG"} "mpn":"GBBS322APY.APYQEUZ"'
        self.assertEqual(run("Czech Republic|ALZA", "Chladnička GBBS322APY", html), ("LG", "GBBS322APY", "페이지", "페이지"))

    def test_alza_number_only_mpn_falls_back_to_name_found_on_page(self):
        html = '"brand":{"@type":"Brand","name":"LG"} "mpn":"123456" GBBS322APY'
        self.assertEqual(run("Czech Republic|ALZA", "Chladnička GBBS322APY", html)[1:4], ("GBBS322APY", "페이지", "상품명"))

    def test_datart_needs_code_on_page(self):
        html = '"@type": "Brand", "name": "Samsung" "sku": "XXRB38C607AB1"'
        self.assertEqual(run("Czech Republic|DATART", "Lednice XY12345Z", html), ("SAMSUNG", "", "페이지", "없음"))

    def test_media_expert_json_ld(self):
        html = ld({"@type": "Product", "brand": {"name": "Beko"}, "model": "B5RCNE406HXB"})
        self.assertEqual(run("Poland|MEDIAEXPERT", "Lodówka inna nazwa", html), ("BEKO", "B5RCNE406HXB", "페이지", "페이지"))

    def test_rtv_page_without_model_needs_name_on_page(self):
        html = ld({"@type": "Product", "brand": {"name": "Beko"}})
        self.assertEqual(run("Poland|RTV_EURO_AGD", "Lodówka ABC12345", html)[1:], ("", "페이지", "없음"))

    def test_worten_ignores_no_brand_marker(self):
        html = ld({"@type": "Product", "brand": {"name": "S/MARCA"}}) + "LGA12345"
        self.assertEqual(run("Portugal|Worten", "Frigorífico LG LGA12345", html)[:3], ("LG", "LGA12345", "상품명"))

    def test_sharaf_meta(self):
        html = '<meta property="brand" content="Hisense"><meta itemprop="mpn" content="RF 12+AB 3">'
        self.assertEqual(run("UAE|Sharaf DG", "Fridge", html), ("HISENSE", "RF 12 + AB 3", "페이지", "페이지"))

    def test_sharaf_null_mpn_is_ignored(self):
        html = '<meta property="brand" content="Hisense"><meta itemprop="mpn" content="NULL">'
        self.assertEqual(run("UAE|Sharaf DG", "Fridge", html)[1], "")

    def test_appliance_online_sku(self):
        html = ld({"@type": "Product", "brand": {"name": "Bosch"}, "sku": "wgg24403au"})
        self.assertEqual(run("Australia|Appliance Online", "Washer", html), ("BOSCH", "WGG24403AU", "페이지", "페이지"))

    def test_falabella_category_page_is_ignored(self):
        self.assertEqual(run("Peru|FALABELLA", "Samsung RF12345", "<html>list</html>")[0], "SAMSUNG")

    def test_falabella_model_field(self):
        html = '"brandName":"LG" "name":"Modelo","value":"GM-T123"'
        self.assertEqual(run("Peru|FALABELLA", "Fridge", html), ("LG", "GM-T123", "페이지", "페이지"))

    def test_falabella_bad_model_is_ignored(self):
        html = '"brandName":"LG" "name":"Modelo","value":"No aplica"'
        self.assertEqual(run("Peru|FALABELLA", "Fridge", html)[1], "")

    def test_cairo_table_model(self):
        html = '<div itemprop="brand"><meta itemprop="name" content="LG"></div><td>الموديل</td><td>gn-b123</td>'
        self.assertEqual(run("Egypt|Cairo Sales", "Fridge", html), ("LG", "GN-B123", "페이지", "페이지"))

    def test_electroplanet_page_brand_and_code_on_page(self):
        html = '<a class="manufacturer" href="/marques/lg">LG</a> GR-B392PLGB'
        self.assertEqual(run("Morocco|Electroplanet", "REFRIGERATEUR GR-B392PLGB SILVER", html), ("LG", "GR-B392PLGB", "페이지", "상품명"))

    def test_mediamarkt_spec_field(self):
        html = '"brand":{"@type":"Brand","name":"LG"} "name":"Model-ID","type":null,"unit":null,"value":"GBB72NSVCN"'
        self.assertEqual(run("Netherlands|MEDIAMARKT", "LG GBB72NSVCN Koelkast", html), ("LG", "GBB72NSVCN", "페이지", "페이지"))

    def test_mediamarkt_name_code_must_be_on_page(self):
        html = '"brand":{"@type":"Brand","name":"LG"}'
        self.assertEqual(run("Netherlands|MEDIAMARKT", "LG GBB72NSVCN Koelkast", html)[1], "")


class PageBrandDictionary(unittest.TestCase):
    def test_brand_seen_on_one_page_helps_a_row_without_page(self):
        rows = [row("x", "1"), row("NEWBRAND ABC12345 lednice", "2", url="https://x/2")]
        pages = {"1": '"brand":{"@type":"Brand","name":"NEWBRAND"}'}
        found = codes.extract(rows, lambda r: pages.get(r["행번호"]), CONFIG)
        self.assertEqual(found["2"][0], "NEWBRAND")

    def test_results_keep_every_row(self):
        rows = [row("a", "1"), row("b", "2", country="Peru", retailer="FALABELLA")]
        self.assertEqual(set(codes.extract(rows, lambda _: None, CONFIG)), {"1", "2"})


class S5Wiring(unittest.TestCase):
    """가짜 회차 폴더로 S5 main 전체를 지나가 추출 결과가 내부 CSV·근거 CSV에 들어가는지 본다."""

    def test_main_fills_codes_from_saved_page_and_writes_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            run_paths = common.RunPaths("2026-11", pathlib.Path(folder)).create()
            shutil.rmtree(run_paths.sub("config"))
            shutil.copytree(RUN.sub("config"), run_paths.sub("config"))
            spec = common.load_output_spec(run_paths)
            judgments, candidates = run_paths.sub("judgments"), run_paths.sub("candidates")

            def item(number, url, flow, country, retailer, name):
                return {**{column: "" for column in spec.internal_columns}, "행번호": number, "URL": url, "원본URL": url, "흐름": flow, "국가": country, "리테일러": retailer, "상품명": name, "제품군": "REF", "판정": s2.KEEP}

            common.write_csv(judgments / "step1.csv", list(spec.internal_columns), [
                item("1", "https://me/1", "검색", "Poland", "MEDIAEXPERT", "Lodówka bez kodu"),
                item("2", "https://osm/2", s2.OSM_FLOW, "Germany", "OTTO", "LG fridge"),
            ])
            (run_paths.sub("html") / "me1.html").write_text(ld({"@type": "Product", "brand": {"name": "Beko"}, "model": "b5rcne406hxb"}), encoding="utf-8")
            pages = [{"url": "https://me/1", "status": "정상", "final_url": "https://me/1", "title": "", "html_file": "me1.html", "method": "zyte_html"},
                     {"url": "https://osm/2", "status": "정상", "final_url": "https://osm/2", "title": "", "html_file": "", "method": "zyte_html"}]
            (judgments / "pages.jsonl").write_text("".join(json.dumps(page, ensure_ascii=False) + "\n" for page in pages), encoding="utf-8")
            common.write_csv(judgments / "sellers.csv", ["요청URL", "판매자", "판매자구분", "근거"], [])
            common.write_csv(candidates / "osm_candidates.csv", ["RAW_URL", "BRAND", "MPC", "MODEL_DEDUP_KEY"], [{"RAW_URL": "https://osm/2", "BRAND": " lg ", "MPC": " gn1 ", "MODEL_DEDUP_KEY": ""}])

            with mock.patch.object(s5, "RunPaths", lambda month: run_paths), mock.patch("urllib.request.urlopen", side_effect=AssertionError("호출 금지")):
                self.assertEqual(s5.main(["--month", "2026-11", "--date", "20261109"]), 0)

            _, evidence = common.read_csv(judgments / s5.CODE_EVIDENCE_NAME)
            self.assertEqual([(row["행번호"], row["브랜드"], row["제품코드"], row["브랜드 찾은곳"], row["제품코드 찾은곳"]) for row in evidence], [("1", "BEKO", "B5RCNE406HXB", "페이지", "페이지")])
            _, rows = common.read_csv(run_paths.sub("final") / s5.INTERNAL_NAME.format(rows=2, date="20261109"))
            self.assertEqual([(row["브랜드"], row["제품코드"]) for row in rows], [("BEKO", "B5RCNE406HXB"), ("LG", "GN1")])


class Helpers(unittest.TestCase):
    def test_module_has_no_config_words_left_as_globals(self):
        for name in ("GENERIC", "GENERIC_BRANDS", "DROP", "KEEP_IF_UPPER", "STOP"):
            for module in (retailers.mix, retailers.pl_pt, retailers.cz):
                self.assertFalse(hasattr(module, name), f"{module.__name__}.{name}")
