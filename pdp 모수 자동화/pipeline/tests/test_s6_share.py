"""WP7 S6·다음 버전: 공유용 변환 재현, 검증 기록, 변경 대상 CSV 적용."""
import dataclasses
import json
import os
import tempfile
import unicodedata
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import common
import make_next_version as nv
import s6_share as s6

RUN = common.RunPaths("2026-11")
SPEC = common.load_output_spec(RUN)
OCTOBER = common.REPO_ROOT / "pdp 모수 추출" / "최종_20261029"
V5 = common.REPO_ROOT / common.load_config(RUN, "output")["october_reference_share"]


def october_file(name):
    return OCTOBER / next(item for item in os.listdir(OCTOBER) if unicodedata.normalize("NFC", item) == name)


def internal(number="1", status="남김", **fields):
    return {**{name: "" for name in SPEC.internal_columns}, "행번호": number, "판정": status, **fields}


def shared(number, status="포함", **fields):
    return {**{name: "" for name in SPEC.all_share_columns}, "행번호": str(number), "모수 포함 여부": status, **fields}


class Convert(unittest.TestCase):
    def test_columns_renames_and_drops(self):
        row = s6.to_share([internal(URL="u", 원본URL="o", 실제URL="f", 페이지상태="정상", OSM_RK="9")], SPEC)[0]
        self.assertEqual(tuple(row), SPEC.all_share_columns)
        self.assertEqual((row["확인 요청 URL"], row["원본 상품 URL"], row["접속 후 URL"], row["페이지 접속 확인 결과"]), ("u", "o", "f", "정상"))

    def test_1p3p_column_follows_seller_kind(self):
        """D145: 판매구분(1P/3P)은 판매자구분만 보고 정한다."""
        kinds = ["직판", "외부판매자", "브랜드공식점", "확인불가", "리퍼·중고", ""]
        rows = s6.to_share([internal(str(i + 1), 판매자구분=kind) for i, kind in enumerate(kinds)], SPEC)
        self.assertEqual([row["판매구분(1P/3P)"] for row in rows], ["1P(직판)", "3P(입점)", "3P(입점)", "확인불가", "", ""])
        self.assertEqual(SPEC.all_share_columns[-1], "판매구분(1P/3P)")

    def test_unknown_seller_kind_stops(self):
        with self.assertRaises(common.ConfigError):
            s6.to_share([internal(판매자구분="마켓")], SPEC)

    def test_status_map(self):
        self.assertEqual([s6.to_share([internal(status=value)], SPEC)[0]["모수 포함 여부"] for value in ("남김", "제외", "확인 필요")], ["포함", "제외", "포함"])

    def test_wording_is_neutral(self):
        self.assertEqual(s6.to_share([internal(판매자근거="Codex 화면: x")], SPEC)[0]["판매자근거"], "수집한 상품 화면: x")

    def test_file_name_starts_at_v1(self):
        self.assertEqual(s6.share_name(SPEC, 1, "11월", 5, "20261130"), "PDP모수_공유용_v1_11월_25개국_35개리테일러_전체판정_5행_20261130.csv")


class Check(unittest.TestCase):
    def problems(self, *rows):
        return s6.check_rows(list(SPEC.all_share_columns), list(rows), SPEC)

    def test_clean_rows_pass(self):
        self.assertEqual(self.problems(shared(1), shared(2, "제외", 제외단계="④중복", 제외사유="같음")), [])

    def test_excluded_needs_stage_and_reason(self):
        self.assertTrue(self.problems(shared(1, "제외")))

    def test_included_must_not_have_stage(self):
        self.assertTrue(self.problems(shared(1, 제외단계="④중복")))

    def test_bad_status_and_seller_kind(self):
        self.assertTrue(self.problems(shared(1, "검토 필요")))
        self.assertTrue(self.problems(shared(1, 판매자구분="마켓")))

    def test_row_numbers_must_be_sequential(self):
        self.assertTrue(self.problems(shared(2)))

    def test_tool_name_is_caught(self):
        self.assertTrue(self.problems(shared(1, 메모="Codex 화면")))

    def test_1p3p_mismatch_is_caught(self):
        self.assertTrue(self.problems(shared(1, 판매자구분="직판", **{"판매구분(1P/3P)": "3P(입점)"})))
        self.assertEqual(self.problems(shared(1, 판매자구분="직판", **{"판매구분(1P/3P)": "1P(직판)"})), [])

    def test_wrong_columns_are_caught(self):
        self.assertTrue(s6.check_rows(["행번호"], [shared(1)], SPEC))


@unittest.skipUnless(V5.exists(), "10월 파일이 없습니다")
class October(unittest.TestCase):
    def test_internal_to_share_matches_every_cell(self):
        """10월 내부판 v2 → 공유용(1차). 브랜드·제품코드는 그때 없었고, 확인 필요는 그때 규칙대로 검토 필요로 맞춰 비교한다."""
        _, rows = common.read_csv(october_file("PDP모수_25개국_35개리테일러_전체판정_55997행_20261029_v2.csv"))
        columns, expected = common.read_csv(october_file("PDP모수_공유용_25개국_35개리테일러_전체판정_55997행_20261029.csv"))
        then = dataclasses.replace(SPEC, share_extra={}, share_status_map={"남김": "포함", "제외": "제외", "확인 필요": "검토 필요"})
        converted = s6.to_share([{**row, "브랜드": "", "제품코드": ""} for row in rows], then)
        self.assertEqual(len(converted), 55997)
        self.assertEqual(sum(converted_row[column] != expected_row[column] for converted_row, expected_row in zip(converted, expected) for column in columns), 0)

    def test_v5_round_trip(self):
        columns, v5 = common.read_csv(V5)
        rename = {new: old for old, new in SPEC.share_renames.items()}
        back = []
        for row in v5:
            item = {**{rename.get(key, key): value for key, value in row.items()}, "OSM_RK": "", "OSM_SOURCE_TYPE": ""}
            item["판정"] = {"포함": "남김", "제외": "제외"}[item["판정"]]
            back.append(item)
        old = dataclasses.replace(SPEC, share_extra={})  # 10월 v5는 판매구분(1P/3P) 열이 없던 26열
        self.assertEqual(s6.to_share(back, old), v5)
        self.assertEqual(s6.check_rows(columns, v5, old), [])


class NextVersion(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.run_paths = common.RunPaths("2026-11", Path(folder.name)).create()
        (self.run_paths.sub("config") / "output.json").write_text((RUN.sub("config") / "output.json").read_text(encoding="utf-8"), encoding="utf-8")
        for target, value in (("get_logger", mock.Mock()), ("RunPaths", self.run_paths)):
            patcher = mock.patch.object(nv, target, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.rows = [shared(1), shared(2), shared(3), shared(4), shared(5, "제외", 제외단계="④중복", 제외사유="같음"), shared(6, "제외", 제외단계="③리리부", 제외사유="외부", 메모="기존")]
        self.current = self.run_paths.sub("final") / s6.share_name(SPEC, 1, "첫", 6, "20261130")
        common.write_csv(self.current, list(SPEC.all_share_columns), self.rows)
        self.before = self.current.read_bytes()
        s6.save_verification(self.run_paths.sub("final") / s6.VERIFY_NAME, 1, {"passed": True})

    def changes(self, requests, name="c.csv", extra=()):
        columns = [*SPEC.all_share_columns, nv.REQUEST_COLUMN, nv.CONFIRM_COLUMN, nv.MEMO_COLUMN, "변경_제외단계", "변경_제외사유", *[column for column, _ in extra]]
        data = []
        for number, request in requests:
            stage = ("③리리부", "EY 지적") if request == "제외" else ("", "")
            data.append({**self.rows[number - 1], nv.REQUEST_COLUMN: request, nv.CONFIRM_COLUMN: request, nv.MEMO_COLUMN: f"메모{number}", "변경_제외단계": stage[0], "변경_제외사유": stage[1], **dict(extra)})
        common.write_csv(self.run_paths.sub("changes") / name, columns, data)
        return name

    def run_next(self, name):
        return nv.main(["--month", "2026-11", "--changes", name, "--summary", "EY반영", "--date", "20261201"])

    def output(self):
        return self.run_paths.sub("final") / s6.share_name(SPEC, 2, "EY반영", 6, "20261201")

    def test_applies_three_out_two_in(self):
        name = self.changes([(1, "제외"), (2, "제외"), (3, "제외"), (5, "포함"), (6, "포함")])
        self.assertEqual(self.run_next(name), 0)
        columns, rows = common.read_csv(self.output())
        self.assertEqual(tuple(columns), SPEC.all_share_columns)
        self.assertEqual([row["행번호"] for row in rows], list("123456"))
        self.assertEqual(Counter(row["모수 포함 여부"] for row in rows), {"제외": 3, "포함": 3})
        self.assertEqual((rows[0]["제외단계"], rows[0]["제외사유"], rows[0]["메모"]), ("③리리부", "EY 지적", "메모1"))
        self.assertEqual((rows[4]["제외단계"], rows[4]["제외사유"], rows[5]["메모"]), ("", "", "기존; 메모6"))

    def test_old_file_is_untouched_and_records_added(self):
        self.run_next(self.changes([(1, "제외")]))
        self.assertEqual(self.current.read_bytes(), self.before)
        records = json.loads((self.run_paths.sub("final") / s6.VERIFY_NAME).read_text(encoding="utf-8"))
        self.assertTrue(records["v2"]["passed"])
        self.assertIn("v1", records)
        self.assertIn("## v2", (self.run_paths.sub("final") / s6.READ_NAME).read_text(encoding="utf-8"))

    def test_next_run_uses_highest_version(self):
        self.run_next(self.changes([(1, "제외")]))
        self.assertEqual(nv.latest_version(self.run_paths.sub("final"))[0], 2)

    def test_stale_row_stops(self):
        name = self.changes([(1, "제외")])
        path = self.run_paths.sub("changes") / name
        columns, rows = common.read_csv(path)
        rows[0]["상품명"] = "다른 이름"
        common.write_csv(path, columns, rows, overwrite=True)
        with self.assertRaises(common.ConfigError):
            self.run_next(name)

    def test_excluding_without_stage_stops(self):
        columns = [*SPEC.all_share_columns, nv.REQUEST_COLUMN, nv.CONFIRM_COLUMN, nv.MEMO_COLUMN]
        common.write_csv(self.run_paths.sub("changes") / "x.csv", columns, [{**self.rows[0], nv.REQUEST_COLUMN: "제외", nv.CONFIRM_COLUMN: "제외", nv.MEMO_COLUMN: "m"}])
        with self.assertRaises(common.ConfigError):
            self.run_next("x.csv")

    def test_no_real_change_stops(self):
        with self.assertRaises(common.ConfigError):
            self.run_next(self.changes([(1, "포함")]))

    def test_confirmation_must_match_request(self):
        name = self.changes([(1, "제외")])
        path = self.run_paths.sub("changes") / name
        columns, rows = common.read_csv(path)
        rows[0][nv.CONFIRM_COLUMN] = "포함"
        common.write_csv(path, columns, rows, overwrite=True)
        with self.assertRaises(common.ConfigError):
            self.run_next(name)

    def test_never_overwrites_next_file(self):
        name = self.changes([(1, "제외")])
        common.write_csv(self.output(), list(SPEC.all_share_columns), self.rows)
        existing = self.output().read_bytes()
        with mock.patch.object(nv, "latest_version", return_value=(1, self.current)):
            with self.assertRaises(FileExistsError):
                self.run_next(name)
        self.assertEqual(self.output().read_bytes(), existing)


if __name__ == "__main__":
    unittest.main()
