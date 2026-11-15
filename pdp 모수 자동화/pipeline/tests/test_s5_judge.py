"""WP7 S5: 판정 순서, 예외 포함, 실제 주소 중복, 브랜드·제품코드, 그리고 v5 재현."""
import json
import re
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import common
import s2_filter as s2
import s5_judge as s5

RUN = common.RunPaths("2026-11")
SETTINGS = common.load_config(RUN, "retailer_rules")["final"]
SPEC = common.load_output_spec(RUN)


def row(number="1", retailer="ALZA", country="Czech Republic", url="https://x/1", status=s2.KEEP, **fields):
    base = {name: "" for name in SPEC.internal_columns}
    return {**base, "행번호": number, "흐름": s2.SEARCH_FLOW, "국가": country, "리테일러": retailer, "URL": url, "원본URL": url, "판정": status, **fields}


def page(status="정상", url="https://x/1", **fields):
    return {"url": url, "status": status, "final_url": url, "title": "제목", **fields}


def seller(name="Shop", kind="외부판매자", evidence="근거"):
    return {"판매자": name, "판매자구분": kind, "근거": evidence}


def judged(item, page_record, seller_record):
    s5.judge_row(item, page_record, seller_record, SETTINGS)
    return item["판정"], item["제외단계"], item["제외사유"], item["메모"]


class PageAndSeller(unittest.TestCase):
    def test_no_page_record_needs_check(self):
        self.assertEqual(judged(row(), None, None), (s2.CHECK, "", "", "페이지 확인 기록 없음"))

    def test_missing_page_excluded_with_title(self):
        self.assertEqual(judged(row(), page("없음(404)"), None)[:3], (s2.EXCLUDE, "④페이지없음", "페이지 없음(없음(404), 제목)"))

    def test_not_found_address_counts_as_missing(self):
        result = judged(row(retailer="UNIEURO"), page(final_url="https://x/online/not-found"), seller("Unieuro", "직판"))
        self.assertEqual(result[:2], (s2.EXCLUDE, "④페이지없음"))

    def test_magalu_block_counts_as_missing_only_when_a_person_saw_it(self):
        self.assertEqual(judged(row(retailer="MAGAZINELUIZA"), {**page("차단화면"), "method": "manual"}, None)[1], "④페이지없음")
        self.assertEqual(judged(row(retailer="MAGAZINELUIZA"), {**page("차단화면"), "method": "zyte_browser"}, None)[:1], (s2.CHECK,))
        self.assertEqual(judged(row(), {**page("차단화면"), "method": "manual"}, None)[:1], (s2.CHECK,))

    def test_permanent_sold_out(self):
        self.assertEqual(judged(row(), page("영구품절"), None)[:3], (s2.EXCLUDE, "④영구품절", "영구 품절(단종) 표시"))

    def test_seller_comes_before_sold_out(self):
        self.assertEqual(judged(row(retailer="EXTRA"), page("품절"), seller())[1], "③리리부")
        self.assertEqual(judged(row(retailer="EXTRA"), page("품절"), seller("eXtra", "직판"))[1], "④품절")

    def test_discontinued_with_direct_seller(self):
        self.assertEqual(judged(row(retailer="DIENMAYXANH"), page("판매중단"), seller("DMX", "직판"))[1], "④판매중단")

    def test_seller_kinds_excluded_with_name(self):
        self.assertEqual(judged(row(), page(), seller("Shop", "외부판매자"))[2], "외부 판매자 (Shop)")
        self.assertEqual(judged(row(), page(), seller("B", "브랜드공식점"))[2], "브랜드 공식점(외부 판매자) (B)")
        self.assertEqual(judged(row(), page(), seller("R", "리퍼·중고"))[2], "리퍼·중고 (R)")

    def test_direct_stays(self):
        self.assertEqual(judged(row(), page(), seller("Alza", "직판"))[:2], (s2.KEEP, ""))

    def test_unknown_seller_needs_check(self):
        self.assertEqual(judged(row(), page(), seller("", "확인불가"))[:1] + judged(row(), page(), seller("", "확인불가"))[3:], (s2.CHECK, "판매자 확인 불가"))

    def test_amazon_unavailable_is_permanent_sold_out(self):
        result = judged(row(retailer="AMAZON", country="Italy"), page(), seller("", "확인불가", '구매상자에 "현재 구매 불가" 문구(판매자 표시 없음)'))
        self.assertEqual(result[:3], (s2.EXCLUDE, "④영구품절", "현재 구매 불가"))

    def test_amazon_no_seller_stays_for_review(self):
        self.assertEqual(judged(row(retailer="AMAZON", country="Italy"), page(), seller("", "확인불가", "구매상자에 판매자 표시 없음(제안 없음)"))[0], s2.CHECK)

    def test_datart_bazar_shell_page_is_refurbished(self):
        result = judged(row(retailer="DATART", url="https://x/bazar/a"), page(url="https://x/bazar/a"), seller("", "확인불가", "ld+json Product 없음, 본문이 빈 껍데기 페이지"))
        self.assertEqual(result[:3], (s2.EXCLUDE, "③리리부", "리퍼·중고(주소 /bazar/)"))

    def test_accessory_category_is_excluded(self):
        result = judged(row(retailer="ALZA"), page(category_path="Domácí spotřebiče > Příslušenství"), seller("Alza", "직판"))
        self.assertEqual(result[:2], (s2.EXCLUDE, "③리리부"))
        self.assertEqual(judged(row(retailer="ALZA"), page(category_path="Lednice"), seller("Alza", "직판"))[0], s2.KEEP)

    def test_row_values_are_filled(self):
        item = row()
        s5.judge_row(item, page(final_url="https://x/final"), seller("Alza", "직판", "e" * 300), SETTINGS)
        self.assertEqual((item["페이지상태"], item["실제URL"], item["판매자"], len(item["판매자근거"])), ("정상", "https://x/final", "Alza", 200))


class Exceptions(unittest.TestCase):
    def status(self, retailer, country, name, kind):
        return judged(row(retailer=retailer, country=country), page(), seller(name, kind))[:2]

    def test_falabella_tottus_sodimac(self):
        for country in ("Chile", "Peru"):
            self.assertEqual(self.status("FALABELLA", country, "TOTTUS", "외부판매자"), (s2.KEEP, ""))

    def test_tienda_oficial_only_in_peru(self):
        self.assertEqual(self.status("FALABELLA", "Peru", "LG TIENDA OFICIAL", "외부판매자"), (s2.KEEP, ""))
        self.assertEqual(self.status("FALABELLA", "Chile", "LG TIENDA OFICIAL", "외부판매자")[0], s2.EXCLUDE)

    def test_other_official_store_stays_excluded(self):
        self.assertEqual(self.status("FALABELLA", "Peru", "CARSA TIENDA OFICIAL", "외부판매자")[0], s2.EXCLUDE)

    def test_liverpool(self):
        self.assertEqual(self.status("LIVERPOOL", "Mexico", "LG Store Mx", "브랜드공식점"), (s2.KEEP, ""))

    def test_lazada_official_except_subscription(self):
        self.assertEqual(self.status("LAZADA", "Thailand", "Samsung", "브랜드공식점"), (s2.KEEP, ""))
        self.assertEqual(self.status("LAZADA", "Thailand", "LG Subscribe.Th", "브랜드공식점")[0], s2.EXCLUDE)
        self.assertEqual(self.status("LAZADA", "Thailand", "Random", "외부판매자")[0], s2.EXCLUDE)

    def test_magalu_five_brands(self):
        for name in ("Electrolux", "Brastemp", "Midea Store", "Samsung", "LG"):
            self.assertEqual(self.status("MAGAZINELUIZA", "Brazil", name, "외부판매자"), (s2.KEEP, ""))
        self.assertEqual(self.status("MAGAZINELUIZA", "Brazil", "Loja X", "외부판매자")[0], s2.EXCLUDE)

    def test_exception_writes_memo(self):
        self.assertIn("E1", judged(row(retailer="FALABELLA", country="Chile"), page(), seller("SODIMAC"))[3])


class Duplicates(unittest.TestCase):
    def run_rows(self, retailer, urls):
        rows = [row(str(number), retailer=retailer, 실제URL=url) for number, url in enumerate(urls, start=1)]
        s5.remove_duplicates(rows, SETTINGS["dedupe"])
        return rows

    def test_same_final_url_keeps_first(self):
        rows = self.run_rows("AO", ["https://www.a.com/p/", "http://a.com/p#x"])
        self.assertEqual(rows[1]["제외단계"], "④중복")
        self.assertEqual(rows[1]["제외사유"], "같은 상품(실제 도착 주소 같음, 대표 행 1)")
        self.assertEqual(rows[0]["판정"], s2.KEEP)

    def test_amazon_dp(self):
        rows = self.run_rows("AMAZON", ["https://www.amazon.de/a/dp/B01234567X?x=1", "https://www.amazon.de/dp/B01234567X"])
        self.assertEqual(rows[1]["제외단계"], "④중복")

    def test_eci_params_removed(self):
        rows = self.run_rows("ELCORTEINGLES_ELECTRONICA", ["https://e/p?stype=a&color=b", "https://e/p?parentCategoryId=c"])
        self.assertIn("꼬리표", rows[1]["제외사유"])

    def test_eci_keeps_other_params(self):
        rows = self.run_rows("ELCORTEINGLES_ELECTRONICA", ["https://e/p?id=1", "https://e/p?id=2"])
        self.assertEqual(rows[1]["판정"], s2.KEEP)

    def test_alza_tail_only(self):
        rows = self.run_rows("ALZA", ["https://www.alza.cz/a-d1.htm", "https://www.alza.cz/a-d1.htm?o=1"])
        self.assertEqual(rows[1]["제외사유"], "같은 상품(주소 꼬리표만 다름, 대표 행 1, #119)")

    def test_costco_and_falabella_number(self):
        costco = self.run_rows("COSTCO", ["https://www.costco.ca/p/-/old-name/4000123", "https://www.costco.ca/p/-/new-name/4000123"])
        falabella = self.run_rows("FALABELLA", ["https://f/falabella-pe/product/111/a/222", "https://f/falabella-pe/product/111/b/222"])
        self.assertEqual(costco[1]["제외사유"], "같은 상품(주소의 상품 번호 같음, 대표 행 1, #119)")
        self.assertIn("상품 번호", falabella[1]["제외사유"])

    def test_excluded_rows_are_not_representatives(self):
        rows = [row("1", retailer="AO", 실제URL="https://a/p", status=s2.EXCLUDE, 제외단계="③리리부"), row("2", retailer="AO", 실제URL="https://a/p")]
        s5.remove_duplicates(rows, SETTINGS["dedupe"])
        self.assertEqual(rows[1]["판정"], s2.KEEP)

    def test_other_country_is_not_duplicate(self):
        rows = [row("1", retailer="AO", country="Germany", 실제URL="https://a/p"), row("2", retailer="AO", country="UK", 실제URL="https://a/p")]
        s5.remove_duplicates(rows, SETTINGS["dedupe"])
        self.assertEqual(rows[1]["판정"], s2.KEEP)

    def test_canonical_is_not_used(self):
        self.assertNotIn("canonical", json.dumps(SETTINGS["dedupe"]))


class Codes(unittest.TestCase):
    def test_osm_row_uses_mpc_then_dedup_key(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "o.csv"
            columns = ["RAW_URL", "BRAND", "MPC", "MODEL_DEDUP_KEY"]
            common.write_csv(path, columns, [dict(zip(columns, values)) for values in (("u1", " lg ", " a1 ", "K1"), ("u2", "LG", "\\N", "k2"), ("u3", "LG", "", "\\N"))])
            self.assertEqual(s5.osm_codes(path), [("u1", "LG", "A1"), ("u2", "LG", "K2"), ("u3", "LG", "")])

    def test_search_row_takes_extracted_values_in_upper_case(self):
        rows = [row("1"), row("2", url="https://x/2")]
        found = {"1": (" lg ", "", "상품명", "없음"), "2": ("Samsung", " rb1 ", "페이지", "페이지")}
        s5.fill_codes(rows, [], found)
        self.assertEqual((rows[0]["브랜드"], rows[0]["제품코드"], rows[1]["브랜드"], rows[1]["제품코드"]), ("LG", "", "SAMSUNG", "RB1"))
        self.assertEqual(s5.code_evidence(rows, found)[1]["제품코드 찾은곳"], "페이지")

    def test_osm_order_mismatch_stops(self):
        rows = [row("1", 흐름=s2.OSM_FLOW, 원본URL="a")]
        with self.assertRaises(common.ConfigError):
            s5.fill_codes(rows, [("b", "LG", "x")], {})

    def test_osm_count_mismatch_stops(self):
        with self.assertRaises(common.ConfigError):
            s5.fill_codes([row("1", 흐름=s2.OSM_FLOW)], [], {})


class Reports(unittest.TestCase):
    def test_compare_months(self):
        table = s5.compare_months({("A", "R"): {"u1", "u2"}}, {("A", "R"): {"u2", "u3"}, ("B", "S"): {"u4"}})
        self.assertEqual(table[0], {"국가": "A", "리테일러": "R", "전월 포함": 2, "이번 달 포함": 2, "공통": 1, "새로 포함": 1, "빠짐": 1})
        self.assertEqual(table[1]["빠짐"], 1)

    def test_render_has_total(self):
        table = s5.compare_months({("A", "R"): {"u1"}}, {})
        self.assertIn("| 합계 | | 0 | 1 | 0 | 1 | 0 |", s5.render_compare("2026-11", "prev.csv", table))

    def test_summary_counts_every_stage(self):
        columns, rows = s5.summarize([row(status=s2.KEEP), row("2", status=s2.EXCLUDE, 제외단계="④중복"), row("3", status=s2.CHECK)], SPEC.exclusion_stages)
        self.assertEqual(columns[3:], ["전체", *SPEC.exclusion_stages, s2.KEEP, s2.CHECK])
        self.assertEqual((rows[0]["전체"], rows[0]["④중복"], rows[0][s2.KEEP], rows[0][s2.CHECK]), ("3", "1", "1", "1"))


def v5_path():
    return common.REPO_ROOT / load_previous()


def load_previous():
    return common.load_config(RUN, "output")["october_reference_share"]  # 10월 대조 기준은 v5 고정(D124). 전월 비교용 previous_share와 따로 둔다


@unittest.skipUnless((common.REPO_ROOT / load_previous()).exists(), "10월 v5 파일이 없습니다")
class ReplayV5(unittest.TestCase):
    """v5의 페이지·판매자 값을 입력으로 되돌려 S5 규칙을 다시 적용한다. 차이는 전부 사유가 정해진 행이어야 한다."""

    @classmethod
    def setUpClass(cls):
        _, cls.v5 = common.read_csv(v5_path())
        rename = {new: old for old, new in SPEC.share_renames.items()}
        cls.rows, pages, sellers = [], {}, {}
        for original in cls.v5:
            item = {**{rename.get(key, key): value for key, value in original.items()}, "OSM_RK": "", "OSM_SOURCE_TYPE": ""}
            if cls.decided_in_s2(original):
                item["판정"] = s2.EXCLUDE
            else:
                item.update({"판정": s2.KEEP, "제외단계": "", "제외사유": "", "메모": "", "페이지상태": "", "실제URL": "", "판매자": "", "판매자구분": "", "판매자근거": ""})
                url, status = original["확인 요청 URL"], original["페이지 접속 확인 결과"]
                status = {"④품절": "품절", "④판매중단": "판매중단"}.get(original["제외단계"], status)
                if status:
                    pages[url] = {"url": url, "status": status, "final_url": original["접속 후 URL"], "title": "", "method": "manual"}  # v5의 Magalu 2건은 사람이 확인한 기록(D068)
                if original["판매자구분"]:
                    sellers[url] = {"판매자": original["판매자"], "판매자구분": original["판매자구분"], "근거": original["판매자근거"]}
            cls.rows.append(item)
        s5.judge_all(cls.rows, pages, sellers, SETTINGS)

    @staticmethod
    def decided_in_s2(row_):
        return row_["제외단계"] in ("①브랜드", "②제품군") or (row_["제외단계"] == "③리리부" and not row_["판매자구분"]) or (row_["제외단계"] == "④중복" and row_["제외사유"].startswith("같은 주소"))

    def test_differences_are_the_reviewed_ones(self):
        found = Counter()
        for row_, original in zip(self.rows, self.v5):
            if (SPEC.share_status_map[row_["판정"]], row_["제외단계"]) != (original["모수 포함 여부"], original["제외단계"]):
                found[(original["리테일러"], original["제외단계"], row_["제외단계"])] += 1
        self.assertEqual(found, Counter({
            # 11월엔 S3가 읽어 올 카테고리 경로가 없어 이 시험에서만 안 걸리는 부품 행(D071·D083)
            ("RTV_EURO_AGD", "③리리부", ""): 29, ("ALZA", "③리리부", ""): 9, ("Worten", "③리리부", ""): 3, ("Electroplanet", "③리리부", ""): 1,
            ("DATART", "③리리부", ""): 1,  # EY 행별 판단(주소에 /bazar/ 없음)
            ("DARTY", "③리리부", "④영구품절"): 4,  # 근거 문구가 같아 품절과 구분 불가
            ("FALABELLA", "", "④중복"): 4,  # v5가 놓친 같은 상품
            ("MEDIAMARKT", "④중복", ""): 1,  # 대표 행 5710이 v5(D103)에서 제외됨
            ("CURRYS", "④중복", "④페이지없음"): 1,  # 판정 순서상 상품 페이지 아님이 먼저
        }))

    def test_duplicates_reproduced_with_same_reason(self):
        ours = {row_["행번호"]: row_["제외사유"] for row_ in self.rows if row_["제외단계"] == "④중복"}
        theirs = {row_["행번호"]: row_["제외사유"] for row_ in self.v5 if row_["제외단계"] == "④중복"}
        self.assertEqual(len(ours.keys() & theirs.keys()), 7589)
        self.assertEqual(len(theirs.keys() - ours.keys()), 2)
        self.assertEqual({key: value for key, value in ours.items() if key in theirs and re.sub(r", #119", "", value) != re.sub(r", #119", "", theirs[key])}, {})


if __name__ == "__main__":
    unittest.main()
