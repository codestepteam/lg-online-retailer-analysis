"""WP0 완료 기준: v5 CSV를 공통 모듈로 읽어 55,997행·26열·포함 10,215를 확인하고 입출력 약속을 검증."""
import contextlib
import io
import json
import logging
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import common

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "october_reference.json").read_text(encoding="utf-8"))
RUN = common.RunPaths(FIXTURE["config_month"])


def reference(name):
    return common.REPO_ROOT / FIXTURE[name]["path"]


class OctoberReference(unittest.TestCase):
    def test_october_files_unchanged(self):
        for name, item in FIXTURE.items():
            if isinstance(item, dict):
                self.assertEqual(common.sha256_file(reference(name)), item["sha256"], name)

    def test_v5_counts_and_header(self):
        columns, rows = common.read_csv(reference("v5_share"))
        spec = common.load_output_spec(RUN)
        self.assertEqual((len(rows), len(columns)), (55_997, 26))
        self.assertEqual(Counter(r["모수 포함 여부"] for r in rows), {"포함": 10_215, "제외": 45_782})
        self.assertEqual(tuple(columns), spec.share_columns)
        self.assertLessEqual({r["제외단계"] for r in rows} - {""}, set(spec.exclusion_stages))
        self.assertLessEqual({r["판매자구분"] for r in rows} - {""}, set(spec.seller_types))

    def test_rewrite_is_byte_identical(self):
        columns, rows = common.read_csv(reference("v5_share"))
        with tempfile.TemporaryDirectory() as folder:
            copy = common.write_csv(Path(folder) / "v5.csv", columns, rows)
            self.assertEqual(common.sha256_file(copy), FIXTURE["v5_share"]["sha256"])


class CsvContract(unittest.TestCase):
    def test_existing_file_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "a.csv"
            common.write_csv(path, ["x"], [{"x": "1"}])
            with self.assertRaises(FileExistsError):
                common.write_csv(path, ["x"], [{"x": "2"}])
            self.assertEqual(common.read_csv(path)[1], [{"x": "1"}])

    def test_mismatched_row_stops_without_leaving_files(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                common.write_csv(Path(folder) / "a.csv", ["x"], [{"x": "1", "y": "2"}])
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_short_row_is_rejected_on_read(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "a.csv"
            path.write_text('"x","y"\r\n"1"\r\n', encoding="utf-8-sig")
            with self.assertRaises(ValueError):
                common.read_csv(path)


class OutputSpecContract(unittest.TestCase):
    def test_broken_conversion_table_stops(self):
        raw = json.loads((RUN.sub("config") / "output.json").read_text(encoding="utf-8"))
        raw["share_dropped"] = ["OSM_RK"]
        with tempfile.TemporaryDirectory() as folder:
            run = common.RunPaths("2026-11", Path(folder)).create()
            (run.sub("config") / "output.json").write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(common.ConfigError):
                common.load_output_spec(run)


class RunArgs(unittest.TestCase):
    def test_paid_step_defaults_to_dry_run(self):
        parser = common.new_parser("t", paid=True)
        self.assertFalse(parser.parse_args([]).live)
        self.assertFalse(parser.parse_args(["--dry-run"]).live)
        self.assertTrue(parser.parse_args(["--run"]).live)

    def test_dry_run_and_run_cannot_be_combined(self):
        parser = common.new_parser("t", paid=True)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(["--dry-run", "--run"])

    def test_invalid_month_rejected(self):
        with self.assertRaises(ValueError):
            common.RunPaths("2026-13")


class ResumeLogContract(unittest.TestCase):
    def test_skips_done_and_retries_failed(self):
        with tempfile.TemporaryDirectory() as folder:
            log = common.ResumeLog(Path(folder) / "r.jsonl", "url")
            log.append({"url": "a", "ok": True})
            log.append({"url": "b", "ok": False})
            again = common.ResumeLog(Path(folder) / "r.jsonl", "url")
            self.assertTrue(again.done("a"))
            self.assertFalse(again.done("b"))
            self.assertFalse(again.done("c"))

    def test_partial_last_line_is_dropped(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "r.jsonl"
            path.write_text('{"url": "a", "ok": true}\n{"url": "b", "o', encoding="utf-8")
            log = common.ResumeLog(path, "url")
            self.assertTrue(log.done("a"))
            self.assertFalse(log.done("b"))
            log.append({"url": "b", "ok": True})
            self.assertTrue(common.ResumeLog(path, "url").done("b"))

    def test_outputs_ready(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "a"
            self.assertFalse(common.outputs_ready([path]))
            path.write_text("x")
            self.assertTrue(common.outputs_ready([path]))
            self.assertFalse(common.outputs_ready([path], force=True))


class SecretHandling(unittest.TestCase):
    def test_secret_is_masked_in_log_file(self):
        with tempfile.TemporaryDirectory() as folder:
            env = Path(folder) / ".env"
            env.write_text('FAKE_KEY="fake-secret-value"\n', encoding="utf-8")
            secret = common.read_secret("FAKE_KEY", env)
            self.assertEqual(secret, "fake-secret-value")
            run = common.RunPaths("2026-11", Path(folder)).create()
            logger = common.get_logger(run, "secret-test")
            for handler in logger.handlers:
                if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                    logger.removeHandler(handler)
            logger.info("키 %s 사용", secret)
            for handler in list(logger.handlers):
                handler.close()
                logger.removeHandler(handler)
            text = (run.sub("logs") / "secret-test.log").read_text(encoding="utf-8")
            self.assertNotIn("fake-secret-value", text)
            self.assertIn("***", text)

    def test_missing_secret_stops(self):
        with tempfile.TemporaryDirectory() as folder:
            env = Path(folder) / ".env"
            env.write_text("OTHER=1\n", encoding="utf-8")
            with self.assertRaises(common.ConfigError):
                common.read_secret("FAKE_KEY", env)


if __name__ == "__main__":
    unittest.main()
