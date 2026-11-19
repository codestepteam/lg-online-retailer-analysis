"""WP3-1 완료 기준: audit·필터 끔 SQL이 20,000자 안에 들고, EY 브랜드가 빠지지 않으며, 승인 없이는 외부 호출을 안 한다."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import common
import s1a_osm as s1a

RUN = common.RunPaths("2026-11")
END_DATE = "2026-11-08"
NINE_WITHOUT_DRY = {("Canada", "COSTCO"), ("Chile", "FALABELLA"), ("Mexico", "LIVERPOOL"), ("Brazil", "MAGAZINELUIZA"), ("SaudiArabia", "EXTRA"),
                    ("Singapore", "LAZADA"), ("Thailand", "LAZADA"), ("Taiwan", "MOMOSHOP"), ("Vietnam", "DIENMAYXANH")}


def audit_row(**changes):
    settings = common.load_config(RUN, "osm_query")["candidates"]
    row = {name: "" for name in settings["columns"] if name != "CRAWL_URL"}
    row.update(CNTRY="Germany", RTLR_NAME="OTTO", RAW_URL="https://www.otto.de/p/a?x=1", CAT_URL_ADDR="https://www.otto.de/p/a", RESULT_STATUS="포함",
               REQUESTED_DATE=END_DATE, RPT_DATE="2026-11-07", DATE_LAG_DAYS=1, DATE_SELECTION_REASON="최근 충분한 수집일 사용")
    return {**row, **changes}


class BrandPrefix(unittest.TestCase):
    SQL = "x CASE WHEN UPPER(TRIM(BRAND)) ='LG ELECTRONICS' THEN 'LG' ELSE REGEXP_REPLACE(UPPER(TRIM(BRAND)),r'\\s+','') END BRAND_KEY y"

    def test_momoshop_brand_key_uses_leading_word(self):
        prefix = common.load_config(RUN, "retailer_rules")["common"]["osm_brand_prefix"]
        sql = s1a.prefix_brand_key(self.SQL, prefix)
        self.assertIn("WHEN UPPER(RTLR_NAME) IN ('MOMOSHOP') AND REGEXP_CONTAINS(UPPER(TRIM(BRAND)),r'^【?\\s*([A-Z]+)') THEN REGEXP_REPLACE(UPPER(TRIM(BRAND)),r'^【?\\s*([A-Z]+).*$',r'\\1') ELSE", sql)
        self.assertNotIn("REGEXP_EXTRACT", sql)  # lgops 서버가 받지 않는 함수
        self.assertEqual(s1a.prefix_brand_key(self.SQL, None), self.SQL)

    def test_changed_console_query_stops(self):
        with self.assertRaises(common.ConfigError):
            s1a.prefix_brand_key("no brand key here", {"retailers": ["MOMOSHOP"], "pattern": "x"})


class FixedDates(unittest.TestCase):
    SQL = ("chosen_dates AS (\n SELECT r.CNTRY,r.RTLR_NAME,MAX(e.RPT_DATE) SELECTED_DATE\n FROM retailer_map r GROUP BY 1,2\n), "
           "date_decisions AS (\n SELECT *,\n CASE WHEN SELECTED_DATE IS NULL THEN 'x' END")

    def test_fixed_retailer_gets_given_date_and_reason(self):
        sql = s1a.fix_selected_dates(self.SQL, {"Canada|COSTCO": {"date": "2026-11-15", "reason": "배너 표 없음"}})
        self.assertIn("CASE WHEN CONCAT(r.CNTRY,'|',r.RTLR_NAME)='Canada|COSTCO' THEN DATE '2026-11-15' ELSE MAX(e.RPT_DATE) END SELECTED_DATE", sql)
        self.assertIn("CASE WHEN CONCAT(CNTRY,'|',RTLR_NAME)='Canada|COSTCO' THEN '사람 지정 기준일 · 배너 표 없음' WHEN SELECTED_DATE IS NULL THEN", sql)

    def test_empty_keeps_sql_and_changed_template_stops(self):
        self.assertEqual(s1a.fix_selected_dates(self.SQL, {}), self.SQL)
        with self.assertRaises(common.ConfigError):
            s1a.fix_selected_dates("no anchors", {"Canada|COSTCO": {"date": "2026-11-15", "reason": "x"}})

    def test_real_query_applies_the_month_setting(self):
        _, _, _, _, sql = s1a.build(RUN, END_DATE)
        for key, value in common.load_config(RUN, "osm_query").get("fixed_dates", {}).items():
            if not key.startswith("_"):
                self.assertIn(f"='{key}' THEN DATE '{value['date']}'", sql)


class Conversion(unittest.TestCase):
    settings = common.load_config(RUN, "osm_query")["candidates"]

    def convert(self, *rows):
        return s1a.to_candidates(list(rows), self.settings)

    def test_kept_rows_use_raw_url(self):
        candidates, home = self.convert(audit_row(), audit_row(RESULT_STATUS="제외"))
        self.assertEqual((len(candidates), home), (1, 0))
        self.assertEqual(candidates[0]["CRAWL_URL"], "https://www.otto.de/p/a?x=1")
        self.assertEqual(list(sorted(candidates[0])), sorted(self.settings["columns"]))

    def test_home_page_is_dropped(self):
        for url in ("https://www.costco.ca/", "https://ao.com", "https://ao.com/?a=1"):
            self.assertEqual(self.convert(audit_row(RAW_URL=url)), ([], 1), url)

    def test_canada_costco_asks_for_english(self):
        row = audit_row(CNTRY="Canada", RTLR_NAME="COSTCO", RAW_URL="https://www.costco.ca/p/-/a/1?x=1", CAT_URL_ADDR="https://www.costco.ca/p/-/a/1?x=1")
        self.assertEqual(self.convert(row)[0][0]["CRAWL_URL"], "https://www.costco.ca/p/-/a/1?langId=-24")

    def test_empty_values_and_flags(self):
        candidate = self.convert(audit_row(AVLBL_STAT="\\N", SLLR_NAME=None, MARKETPLACE=True, OUTLET=False))[0][0]
        self.assertEqual((candidate["AVLBL_STAT"], candidate["SLLR_NAME"], candidate["MARKETPLACE"], candidate["OUTLET"]), ("", "", "true", "false"))

    def test_missing_column_stops(self):
        row = audit_row()
        del row["RAW_URL"]
        with self.assertRaises(common.ConfigError):
            self.convert(row)

    def test_date_report_flags_check_and_missing_targets(self):
        rows = [audit_row(), audit_row(CNTRY="Canada", RTLR_NAME="COSTCO", DATE_SELECTION_REASON="확인 필요 · 15일 초과 과거 데이터")]
        targets = [{"country": "Germany", "retailer": "OTTO"}, {"country": "Canada", "retailer": "COSTCO"}, {"country": "Chile", "retailer": "FALABELLA"}]
        text = s1a.render_date_report(rows, self.convert(*rows)[0], 0, targets, self.settings["needs_check_prefix"])
        self.assertIn("`확인 필요` 2곳: Canada COSTCO, Chile FALABELLA", text)
        self.assertIn("확인 필요 · 결과 행 없음", text)


class RealConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.query = common.load_config(RUN, "osm_query")
        cls.alias = common.load_config(RUN, "s0_input")["country_alias"]
        cls.brands = common.load_config(RUN, "brands")
        cls.console = s1a.console_targets(RUN)
        cls.query, cls.merged, cls.report, cls.added_divs, cls.sql = s1a.build(RUN, END_DATE)

    def test_only_dry_is_added_to_the_nine_retailers(self):
        self.assertEqual(len(self.merged), 23)
        self.assertEqual({(c, r) for c, r, _ in self.added_divs}, NINE_WITHOUT_DRY)
        self.assertEqual({d for _, _, d in self.added_divs}, {"DRY"})
        for before, after in zip(self.console, self.merged):
            self.assertEqual(set(after["brands"]) - set(before["brands"]), {"DRY"} if (before["country"], before["retailer"]) in NINE_WITHOUT_DRY else set())
            self.assertLessEqual(set(before["brands"]), set(after["brands"]))

    def test_every_v5_osm_category_is_requested(self):
        path = common.REPO_ROOT / json.loads((Path(__file__).parent / "fixtures" / "october_reference.json").read_text(encoding="utf-8"))["v5_share"]["path"]
        _, rows = common.read_csv(path)
        requested = {(self.alias.get(t["country"], t["country"]), t["retailer"], div) for t in self.merged for div in t["brands"]}
        missing = {(r["국가"], r["리테일러"], r["제품군"]) for r in rows if r["흐름"] == "OSM"} - requested
        self.assertEqual(missing, set())

    def test_added_div_is_left_out_of_date_choice(self):
        for anchor in ("FROM brand_map WHERE CONCAT(CNTRY", "b.BASELINE_URLS*0.8 AND CONCAT(d.CNTRY"):
            self.assertEqual(self.sql.count(anchor), 1)
        self.assertEqual(self.sql.count("'Singapore|LAZADA|DRY'"), 2)

    def test_changed_console_sql_stops(self):
        with self.assertRaises(common.ConfigError):
            s1a.exclude_from_date_choice("SELECT 1", [("Canada", "COSTCO", "DRY")])

    def test_sql_parses_as_bigquery(self):
        code = "import sqlglot, sys; sqlglot.parse_one(sys.stdin.read(), dialect='bigquery'); print('ok')"
        python = Path(self.query["console_python"]).expanduser()
        done = subprocess.run([str(python), "-c", code], input=self.sql, capture_output=True, text=True)
        self.assertEqual(done.stdout.strip(), "ok", done.stderr[-500:])

    def test_console_brands_kept_and_sheet_brands_added(self):
        for target, before in zip(self.merged, self.console):
            country = self.alias.get(target["country"], target["country"])
            for div, brands in target["brands"].items():
                keys = {s1a.normalized(b) for b in brands}
                self.assertLessEqual({s1a.normalized(b) for b in before["brands"].get(div, [])}, keys)
                category = s1a.brand_category(div, self.query, self.brands["category_fallback"])
                self.assertLessEqual({s1a.normalized(b) for b in self.brands["brands"].get(country, {}).get(category, [])}, keys, f"{country} {target['retailer']} {div}")

    def test_german_amazon_ref_gets_samsung_and_liebherr(self):
        target = next(t for t in self.merged if t["country"] == "Germany" and t["retailer"] == "AMAZON")
        self.assertLessEqual({"SAMSUNG", "LIEBHERR"}, set(target["brands"]["REF"]))

    def test_sql_is_audit_without_filter_and_within_limit(self):
        self.assertLessEqual(len(self.sql), self.query["max_sql_chars"])
        self.assertIn("RESULT_STATUS", self.sql)
        self.assertNotIn("WHERE EXCLUSION_REASON=''", self.sql)
        self.assertNotIn("{{", self.sql)
        self.assertIn(f"DATE '{END_DATE}'", self.sql)


class RunMode(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.run_paths = common.RunPaths("2026-11", Path(self.folder.name)).create()
        for name in ("osm_query", "s0_input", "brands", "retailer_rules"):
            shutil.copy(RUN.sub("config") / f"{name}.json", self.run_paths.sub("config") / f"{name}.json")
        logger_patch = mock.patch.object(s1a, "get_logger", return_value=mock.Mock())
        logger_patch.start()
        self.addCleanup(logger_patch.stop)
        run_patch = mock.patch.object(s1a, "RunPaths", return_value=self.run_paths)
        run_patch.start()
        self.addCleanup(run_patch.stop)
        which_patch = mock.patch.object(s1a.shutil, "which", return_value="/fake/lgops")
        which_patch.start()
        self.addCleanup(which_patch.stop)

    def run_main(self, *arguments):
        with mock.patch.object(s1a, "run_lgops") as fake:
            s1a.main(["--month", "2026-11", "--end-date", END_DATE, *arguments])
        return fake

    def test_default_makes_no_external_call(self):
        self.run_main().assert_not_called()
        self.assertTrue((self.run_paths.sub("candidates") / "osm_query.sql").exists())
        report = (self.run_paths.sub("candidates") / "osm_query_report.md").read_text(encoding="utf-8")
        self.assertIn("SQL 길이", report)

    def test_preview_says_why_and_what_is_sent(self):
        self.run_main()
        report = (self.run_paths.sub("candidates") / "osm_query_report.md").read_text(encoding="utf-8")
        for expected in ("왜 부르나", "보내는 값", END_DATE, "pjt-lge-oned.L1_ONED.TRPURC_OSM_PRODUCT_DAILY_L", "pdp_view=audit", "Germany AMAZON", "--estimate", "--run"):
            self.assertIn(expected, report)

    def test_from_audit_makes_no_external_call(self):
        audit = self.run_paths.sub("candidates") / "sample.jsonl"
        audit.write_text(json.dumps(audit_row()) + "\n", encoding="utf-8")
        with mock.patch.object(s1a, "console_targets", return_value=[{"country": "Germany", "retailer": "OTTO"}]):
            self.run_main("--from-audit", str(audit)).assert_not_called()
        self.assertEqual(len(common.read_csv(self.run_paths.sub("candidates") / "osm_candidates.csv")[1]), 1)

    def test_estimate_uses_bq_dry_run_without_output(self):
        command = self.run_main("--estimate").call_args.args[0]
        self.assertEqual(command[-1], "--dry-run")
        self.assertNotIn("--out", command)

    def test_run_writes_to_audit_file(self):
        with mock.patch.object(s1a, "convert", return_value=(0, 0, 0)) as convert:
            command = self.run_main("--run").call_args.args[0]
        convert.assert_called_once()
        self.assertEqual(command[1], "--out")
        self.assertTrue(command[2].endswith("osm_audit.jsonl"))
        self.assertLess(command.index("--out"), command.index("bq"))
        self.assertNotIn("--dry-run", command)

    def test_existing_audit_is_not_replaced(self):
        (self.run_paths.sub("candidates") / "osm_audit.jsonl").write_text("{}\n", encoding="utf-8")
        self.run_main("--run").assert_not_called()


if __name__ == "__main__":
    unittest.main()
