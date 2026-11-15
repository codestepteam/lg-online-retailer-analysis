"""WP4 완료 기준: 판정 순서가 맞고, 10월 입력을 넣었을 때 v5의 ①②③·요청 URL 중복과 다른 행은 모두 사유가 있다."""
import glob
import re
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import common
import s2_filter as s2

RUN = common.RunPaths("2026-11")
OCTOBER = common.RunPaths("2026-10")
SOURCE = str(common.REPO_ROOT / "pdp 모수 추출") + "/"
EUROPE, GERMANY_UK, ADDED = ("OSM_유럽13개리테일러_PDP후보_8160건_20261026.csv", "OSM_독일영국5개리테일러_PDP후보_1889건_20261029.csv", "OSM_추가9개리테일러_PDP후보_4942건_20261028.csv")
CARDS = "검색결과_20261028_734afcdd/상품카드.csv"
LATER_STEP = re.compile(r"외부 판매자|리퍼·중고|부품|브랜드 공식점")
PERSON_DECISION = re.compile(r"D0\d\d|D1\d\d|EY 검토|사용자 확인|재확인|EY 판정")
ALZA_WORDS = ("-bazar-", "-sleva-", "-levne-")
S2_STAGES = (s2.BRAND_STAGE, s2.CATEGORY_STAGE, s2.KEYWORD_STAGE, s2.DUPLICATE_STAGE)


def rules():
    return s2.load_rules(RUN)


def search(**changes):
    row = {"흐름": s2.SEARCH_FLOW, "국가": "Poland", "리테일러": "MEDIAEXPERT", "제품군": "REF", "상품명": "Lodówka LG GBB61", "URL": "https://www.mediaexpert.pl/lodowka-lg", "OSM브랜드": ""}
    return {**row, **changes}


def osm(**changes):
    row = {"흐름": s2.OSM_FLOW, "국가": "Germany", "리테일러": "OTTO", "제품군": "REF", "상품명": "LG Kühlschrank GBB61", "URL": "https://www.otto.de/p/a", "OSM브랜드": "LG"}
    return {**row, **changes}


class Judge(unittest.TestCase):
    rules = rules()

    def test_kept_rows(self):
        self.assertEqual(s2.judge(search(), self.rules)[:2], (s2.KEEP, ""))
        self.assertEqual(s2.judge(osm(), self.rules)[:2], (s2.KEEP, ""))

    def test_brand_comes_before_keyword(self):
        name = "Lodówka Noname używana"
        self.assertEqual(s2.judge(search(상품명=name, URL="https://www.mediaexpert.pl/a"), self.rules)[1], s2.BRAND_STAGE)

    def test_osm_brand_outside_list(self):
        self.assertEqual(s2.judge(osm(OSM브랜드="NONAME"), self.rules)[1], s2.BRAND_STAGE)

    def test_dishwasher_is_only_for_spain(self):
        self.assertEqual(s2.judge(osm(제품군="D/W"), self.rules)[:3], (s2.EXCLUDE, s2.CATEGORY_STAGE, "식기세척기는 스페인만(D061)"))

    def test_dryer_uses_washer_brands(self):
        self.assertEqual(self.rules.target_brands("Germany", "DRY"), self.rules.target_brands("Germany", "W/M"))

    def test_url_rules_need_right_country_and_retailer(self):
        url = "https://www.alza.cz/lg-gmg960evee-bazar-d12641998.htm"
        alza = search(국가="Czech Republic", 리테일러="ALZA", 상품명="LG GMG960EVEE", URL=url)
        self.assertEqual(s2.judge(alza, self.rules)[1], s2.KEYWORD_STAGE)
        self.assertIsNone(self.rules.url_exclusion({**alza, "리테일러": "DATART"}))

    def test_canada_french_page_is_case_sensitive(self):
        row = osm(국가="Canada", 리테일러="COSTCO", URL="https://www.costco.ca/p/-/a/1?langId=-25")
        self.assertEqual(self.rules.url_exclusion(row), "불어 페이지(D050)")
        self.assertIsNone(self.rules.url_exclusion({**row, "URL": "https://www.costco.ca/p/-/a/1?langid=-25"}))

    def test_darty_seller_address_gets_note_and_stays(self):
        result = s2.judge(osm(국가="France", 리테일러="DARTY", URL="https://www.darty.com/a?ofmp=1"), self.rules)
        self.assertEqual(result[0], s2.KEEP)
        self.assertIn("ofmp", result[3])

    def test_part_word_asks_for_check(self):
        name = "Filtr do lodówki LG"
        self.assertEqual(self.rules.head(name), "filtr do lodówki lg")
        self.assertEqual(s2.judge(osm(상품명=name), self.rules)[0], s2.CHECK)

    def test_arabic_brand_is_found(self):
        self.assertEqual(self.rules.brands_in("ثلاجة ال جي 300 لتر", ["LG"]), ["LG"])
        self.assertEqual(self.rules.brands_in("ال جى غسالة ملابس 8 كيلو", ["LG"]), ["LG"])  # 끝 글자가 ى인 표기(Cairo Sales 10월 3행)
        self.assertEqual(self.rules.brands_in("غسالة الجيل الجديد 8 كيلو", ["LG"]), [])  # 다른 단어의 앞부분은 LG로 보지 않는다

    def test_unknown_search_category_needs_check(self):
        self.assertEqual(s2.judge(search(제품군="?"), self.rules)[:2], (s2.CHECK, s2.CATEGORY_STAGE))


class Duplicates(unittest.TestCase):
    columns = common.load_output_spec(RUN).internal_columns

    def base(self, **changes):
        fields = {"출처파일": "a", "원본URL": "u", "기준일": "2026-11-01", "검색어": "", "엑셀행번호": "", "광고여부": "", "OSM_RK": "", "OSM_SOURCE_TYPE": ""}
        return {**fields, **osm(**changes)}

    def test_first_kept_row_is_representative(self):
        judged = s2.judge_all([self.base(), self.base()], rules(), self.columns)
        self.assertEqual([r["제외단계"] for r in judged], ["", s2.DUPLICATE_STAGE])
        self.assertEqual(judged[1]["제외사유"], "같은 주소(대표 행 1)")

    def test_excluded_row_cannot_be_representative(self):
        judged = s2.judge_all([self.base(OSM브랜드="NONAME"), self.base()], rules(), self.columns)
        self.assertEqual([r["제외단계"] for r in judged], [s2.BRAND_STAGE, ""])

    def test_every_output_column_is_filled(self):
        self.assertEqual(set(s2.judge_all([self.base()], rules(), self.columns)[0]), set(self.columns))

    def test_wrong_columns_stop(self):
        with self.assertRaises(common.ConfigError):
            s2.judge_all([self.base()], rules(), ["행번호"])


class Main(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.run_paths = common.RunPaths("2026-11", Path(folder.name)).create()
        for name in ("brands", "keywords", "categories", "retailer_rules", "s0_input", "output"):
            shutil.copy(RUN.sub("config") / f"{name}.json", self.run_paths.sub("config") / f"{name}.json")
        for target, value in (("get_logger", mock.Mock()), ("RunPaths", self.run_paths)):
            patcher = mock.patch.object(s2, target, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def write_inputs(self):
        folder = self.run_paths.sub("candidates")
        osm_columns = ["CNTRY", "RTLR_NAME", "DIV", "BRAND", "PRODUCT_DESC", "CRAWL_URL", "RAW_URL", "RPT_DATE", "RK", "SOURCE_TYPE"]
        common.write_csv(folder / "osm_candidates.csv", osm_columns, [dict(zip(osm_columns, ["Germany", "OTTO", "REF", "LG", "LG Kühlschrank", "https://www.otto.de/p/a", "https://www.otto.de/p/a", "2026-11-01", "1", "x"]))])
        card_columns = ["엑셀행번호", "국가", "리테일러", "F열제품군", "J열검색어", "최종검색결과URL", "페이지번호", "카드순번", "상품명", "카드PDP링크", "광고여부", "표시된전체수", "수집시각", "접속국가"]
        common.write_csv(folder / "search_cards.csv", card_columns, [dict(zip(card_columns, ["5", "Poland", "MEDIAEXPERT", "Refrigerator", "lodówka", "u", "1", "1", "Lodówka LG", "https://www.mediaexpert.pl/lodowka-lg", "N", "1", "2026-11-02T00:00:00", "PL"]))])

    def test_missing_input_stops(self):
        with self.assertRaises(common.ConfigError):
            s2.main(["--month", "2026-11"])

    def test_writes_judgments_and_summary_then_skips(self):
        self.write_inputs()
        self.assertEqual(s2.main(["--month", "2026-11"]), 0)
        folder = self.run_paths.sub("judgments")
        columns, rows = common.read_csv(folder / "step1.csv")
        self.assertEqual(columns, list(common.load_output_spec(self.run_paths).internal_columns))
        self.assertEqual([(r["흐름"], r["판정"]) for r in rows], [(s2.OSM_FLOW, s2.KEEP), (s2.SEARCH_FLOW, s2.KEEP)])
        self.assertEqual(len(common.read_csv(folder / "step1_summary.csv")[1]), 2)
        before = (folder / "step1.csv").stat().st_mtime_ns
        s2.main(["--month", "2026-11"])
        self.assertEqual((folder / "step1.csv").stat().st_mtime_ns, before)


def reason_for_difference(new, old):
    """새 S2와 v5가 다를 때 사유 이름을 돌려준다. 어디에도 안 맞으면 None."""
    new_stage, old_stage = new["제외단계"], old["제외단계"] if old["제외단계"] in S2_STAGES else ""
    if any(word in new["제외사유"] for word in ALZA_WORDS):
        return "Alza 세 단어(새 규칙)"
    if not new_stage and old_stage == s2.KEYWORD_STAGE and LATER_STEP.match(old["제외사유"]):
        return "S2 뒤 단계에서 제외(판매자·리퍼·부품)"
    if not new_stage and old_stage == s2.DUPLICATE_STAGE and old["제외사유"].startswith("같은 상품"):
        return "S2 뒤 단계에서 제외(실제 도착 주소 중복)"
    if PERSON_DECISION.search(old["메모"]) or PERSON_DECISION.search(old["제외사유"]):
        return "행별 사람 결정(EY·사용자)"
    return None


class OctoberComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rules_for_october = s2.load_rules(RUN, OCTOBER)
        rows = list(s2.osm_rows(SOURCE + EUROPE, EUROPE, rules_for_october, lambda row: row["CNTRY"] not in ("Germany", "UK")))
        rows += s2.osm_rows(SOURCE + GERMANY_UK, GERMANY_UK, rules_for_october)
        rows += s2.osm_rows(SOURCE + ADDED, ADDED, rules_for_october)
        rows += s2.search_rows(SOURCE + CARDS, CARDS, rules_for_october)
        cls.new = s2.judge_all(rows, rules_for_october, common.load_output_spec(RUN).internal_columns)
        cls.old = sorted(common.read_csv(glob.glob(SOURCE + "최종_20261029/PDP모수_공유용_v5_*.csv")[0])[1], key=lambda row: int(row["행번호"]))

    def test_same_rows_and_urls(self):
        self.assertEqual(len(self.new), len(self.old))
        for new, old in zip(self.new, self.old):
            self.assertEqual((new["URL"], new["원본URL"], new["페이지확인규칙"]), (old["확인 요청 URL"], old["원본 상품 URL"], old["페이지확인규칙"]))

    def differences(self):
        return [(new, old) for new, old in zip(self.new, self.old) if new["제외단계"] != (old["제외단계"] if old["제외단계"] in S2_STAGES else "")]

    def test_every_difference_has_a_reason(self):
        unexplained = [(new["행번호"], new["제외단계"], old["제외단계"], old["제외사유"][:40]) for new, old in self.differences() if not reason_for_difference(new, old)]
        self.assertEqual(unexplained[:20], [])

    def test_reason_counts(self):
        counts = Counter(reason_for_difference(new, old) for new, old in self.differences())
        self.assertEqual(counts, Counter({"S2 뒤 단계에서 제외(판매자·리퍼·부품)": 7346, "S2 뒤 단계에서 제외(실제 도착 주소 중복)": 394, "Alza 세 단어(새 규칙)": 300, "행별 사람 결정(EY·사용자)": 27}))  # 27 = Electroplanet 23 + RTV_EURO_AGD 3 + COSTCO 1(모두 10월에 사람이 ②제품군으로 뺀 행). Cairo Sales `ال جى` 3행은 2026-11-14 무늬 수정으로 v5와 같아짐

    def test_duplicate_representatives_match(self):
        pairs = [(new["제외사유"], old["제외사유"]) for new, old in zip(self.new, self.old) if new["제외단계"] == s2.DUPLICATE_STAGE]
        self.assertEqual(len(pairs), 6897)  # Cairo Sales `ال جى` 2행이 v5처럼 같은 주소 중복으로 잡힘(2026-11-14)
        self.assertTrue(all(new == old for new, old in pairs))


if __name__ == "__main__":
    unittest.main()
