"""WP2 완료 기준: 엑셀에서 만든 설정이 10월 코드가 메모리에 만들던 값과 같고, 시트 구조가 바뀌면 멈춘다."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import common
import s0_config as s0

RUN = common.RunPaths("2026-11")
STEP1 = common.REPO_ROOT / "pdp 모수 추출/최종_20261029/판정근거/스크립트/step1_filter.py"
INPUT_TERMS = common.REPO_ROOT / "pdp 모수 추출/검색결과_20261028_734afcdd/입력검색어.json"
CONSOLE_PYTHON = Path("~/.local/share/uv/tools/lg-bq-console/bin/python").expanduser()
V5_PAIR_FIELDS = ("국가", "리테일러", "흐름")


def october_memory():
    """10월 step1 코드의 앞부분을 실제로 실행해 BRANDS·KW를 얻는다."""
    source = STEP1.read_text(encoding="utf-8").split("# ---------- 브랜드 찾기")[0]
    saved = sys.argv
    sys.argv = ["step1", "unused"]
    try:
        namespace = {}
        exec(compile(source, str(STEP1), "exec"), namespace)
    finally:
        sys.argv = saved
    return namespace["BRANDS"], namespace["KW"]


class RealWorkbook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s0_input = common.load_config(RUN, "s0_input")
        cls.search_urls = common.load_config(RUN, "search_urls")["retailers"]
        cls.sheets = s0.load_sheets(s0.find_workbook(cls.s0_input), cls.s0_input)
        cls.built = s0.build_all(cls.sheets, cls.s0_input, cls.search_urls, {"excel": "test"})
        cls.brands_memory, cls.keywords_memory = october_memory()

    def test_brands_match_october_memory(self):
        built = {(c, cat): set(v) for c, cats in self.built["brands"]["brands"].items() for cat, v in cats.items()}
        self.assertEqual(built, dict(self.brands_memory))

    def test_keywords_match_october_memory_in_order(self):
        built = {c: [(k["type"], k["keyword"]) for k in items] for c, items in self.built["keywords"]["keywords"].items()}
        self.assertEqual(built, dict(self.keywords_memory))

    def test_search_terms_match_october_input(self):
        reference = json.loads(INPUT_TERMS.read_text(encoding="utf-8"))
        fields = ("excel_row", "country", "retailer", "category", "english", "keyword", "ey_proposal", "source_note")
        # 10월 입력 자료의 리테일러 이름 끝 공백은 10월 판정 코드도 strip했다(v5 이름에 공백 없음).
        pick = lambda row: tuple(row[name].strip() if name == "retailer" else row[name] for name in fields)
        self.assertEqual(sorted(map(pick, self.built["search_terms"]["terms"]), key=repr), sorted(map(pick, reference["rows"]), key=repr))
        self.assertEqual(sorted(map(pick, self.built["search_terms"]["excluded"]), key=repr), sorted(map(pick, reference["excluded"]), key=repr))
        self.assertEqual((len(reference["rows"]), len(reference["excluded"])), (126, 4))

    def test_targets_match_v5_pairs(self):
        path = common.REPO_ROOT / json.loads((Path(__file__).parent / "fixtures" / "october_reference.json").read_text(encoding="utf-8"))["v5_share"]["path"]
        _, rows = common.read_csv(path)
        v5 = {tuple(r[f] for f in V5_PAIR_FIELDS) for r in rows}
        self.assertEqual({(t["country"], t["retailer"], t["flow"]) for t in self.built["targets"]["targets"]}, v5)
        self.assertEqual(len(v5), 35)

    def test_search_targets_have_zyte_values(self):
        search = [t for t in self.built["targets"]["targets"] if t["flow"] == "검색"]
        self.assertEqual(len(search), 12)
        self.assertTrue(all(t["zyte_geolocation"] and t["zyte_geolocation_group"] in ("standard", "extended") for t in search))

    def test_country_codes_match_console(self):
        code = "import json; from bqconsole.catalog import COUNTRY_CODES as C; print(json.dumps(C))"
        console = json.loads(subprocess.run([str(CONSOLE_PYTHON), "-c", code], capture_output=True, text=True, check=True).stdout)
        alias = self.s0_input["country_alias"]
        self.assertEqual({alias.get(k, k): v for k, v in console.items()}, self.s0_input["console_country_codes"])

    def test_changed_header_stops(self):
        for key in ("targets", "brands", "search_terms", "keywords"):
            spec = self.s0_input["sheets"][key]
            rows = copy.deepcopy(self.sheets[key][:spec["header_row"]])
            first_column = next(iter(spec["columns"].values()))[0]
            rows[spec["header_row"] - 1][first_column] = "바뀐 머리글"
            with self.subTest(key), self.assertRaises(common.ConfigError):
                list(s0.data_rows(rows, spec))

    def test_unknown_retailer_stops(self):
        spec = self.s0_input["sheets"]["targets"]
        rows = copy.deepcopy(self.sheets["targets"])
        rows[spec["header_row"]][spec["columns"]["retailer"][0]] = "처음 보는 소매점"
        with self.assertRaises(common.ConfigError):
            s0.build_targets(rows, self.s0_input, self.search_urls)

    def test_total_mismatch_stops(self):
        spec = self.s0_input["sheets"]["targets"]
        rows = copy.deepcopy(self.sheets["targets"])
        rows[spec["header_row"]][spec["columns"]["region"][0]] = None
        with self.assertRaises(common.ConfigError):
            s0.build_targets(rows, self.s0_input, self.search_urls)

    def test_console_mismatch_stops(self):
        targets = copy.deepcopy(self.built["targets"]["targets"])
        next(t for t in targets if t["osm"])["retailer"] = "없는 리테일러"
        with self.assertRaises(common.ConfigError):
            s0.check_console(targets, self.s0_input)

    def test_diff_reports_fake_changes(self):
        changed = copy.deepcopy(self.built)
        changed["brands"]["brands"]["Spain"]["REF"].append("NEWBRAND")
        changed["search_terms"]["terms"][0]["keyword"] = "바뀐 검색어"
        text = s0.render_diff("2026-12", "2026-11", changed, self.built)
        self.assertIn("NEWBRAND", text)
        self.assertIn("바뀐 검색어", text)
        self.assertIn("달라진 값 2개", text)
        self.assertIn("달라진 값 없음", s0.render_diff("2026-12", "2026-11", self.built, self.built))


class Helpers(unittest.TestCase):
    def test_previous_month(self):
        self.assertEqual(s0.previous_month("2026-11"), "2026-10")
        self.assertEqual(s0.previous_month("2027-01"), "2026-12")

    def test_workbook_must_be_unique(self):
        with self.assertRaises(common.ConfigError):
            s0.find_workbook({"excel_glob": "관련문서/없는파일*.xlsx"})

    def test_missing_previous_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertIsNone(s0.load_previous("2026-11", Path(folder)))
        self.assertIn("없어 비교하지", s0.render_diff("2026-11", "2026-10", {}, None))


if __name__ == "__main__":
    unittest.main()
