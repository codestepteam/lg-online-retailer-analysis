"""PDP 모수 자동화 공통 도구: 회차 폴더, 설정 읽기, CSV 읽기·쓰기, 로그, 실행 인자, 이어받기.

규칙 값(열 이름·제외단계 등)은 여기에 적지 않고 회차 폴더의 config/*.json에서 읽는다.
"""
import argparse
import csv
import hashlib
import json
import logging
import os
import re
import sys
import tempfile
import dataclasses
from dataclasses import dataclass
from datetime import date
from pathlib import Path

AUTOMATION_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = AUTOMATION_ROOT.parent
RUNS_ROOT = AUTOMATION_ROOT / "runs"
RUN_SUBDIRS = ("config", "candidates", "html", "judgments", "final", "changes", "logs")
ENCODING = "utf-8-sig"

csv.field_size_limit(sys.maxsize)


class ConfigError(Exception):
    """설정 파일이 없거나 형식이 약속과 다를 때 멈추기 위한 예외."""


@dataclass(frozen=True)
class RunPaths:
    """한 회차(runs/YYYY-MM/)의 경로. 모든 단계는 이 폴더만 읽고 쓴다."""

    month: str
    root: Path = RUNS_ROOT

    def __post_init__(self):
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", self.month):
            raise ValueError(f"회차는 YYYY-MM 형식이어야 합니다: {self.month}")

    @property
    def directory(self):
        return self.root / self.month

    def sub(self, name):
        if name not in RUN_SUBDIRS:
            raise ValueError(f"알 수 없는 회차 하위 폴더: {name}")
        return self.directory / name

    def create(self):
        for name in RUN_SUBDIRS:
            self.sub(name).mkdir(parents=True, exist_ok=True)
        return self


def load_config(run, name):
    path = run.sub("config") / f"{name}.json"
    if not path.exists():
        raise ConfigError(f"설정 파일이 없습니다: {path}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


@dataclass(frozen=True)
class OutputSpec:
    """output.json의 산출물 약속. 내부판에서 공유용 열이 정확히 나오는지 읽을 때 검사한다."""

    internal_columns: tuple
    share_columns: tuple
    share_renames: dict
    share_dropped: tuple
    share_status_map: dict
    share_wording: dict
    exclusion_stages: tuple
    seller_types: tuple
    share_filename: str
    share_extra: dict = dataclasses.field(default_factory=dict)

    @property
    def all_share_columns(self):
        """공유용 기본 열 뒤에 다른 열에서 정해지는 열(share_extra_columns)을 붙인 전체 열."""
        return self.share_columns + tuple(self.share_extra)


def load_output_spec(run):
    raw = load_config(run, "output")
    try:
        spec = OutputSpec(
            tuple(raw["internal_columns"]), tuple(raw["share_columns"]), raw["share_renames"],
            tuple(raw["share_dropped"]), raw["share_status_map"], raw["share_wording"],
            tuple(raw["exclusion_stages"]), tuple(raw["seller_types"]), raw["share_filename"],
            raw.get("share_extra_columns", {}),
        )
    except KeyError as error:
        raise ConfigError(f"output.json에 항목이 없습니다: {error}") from error
    derived = tuple(spec.share_renames.get(c, c) for c in spec.internal_columns if c not in spec.share_dropped)
    if derived != spec.share_columns:
        raise ConfigError(f"내부판에서 변환한 열이 공유용 열과 다릅니다: {derived}")
    for name, rule in spec.share_extra.items():
        if rule.get("from") not in spec.share_columns or not isinstance(rule.get("map"), dict):
            raise ConfigError(f"share_extra_columns의 {name} 규칙이 잘못됐습니다")
    return spec


def read_csv(path):
    """(열 목록, 행 목록)을 돌려준다. 열 수가 어긋난 행이 있으면 조용히 넘기지 않고 멈춘다."""
    with Path(path).open(encoding=ENCODING, newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        columns = list(reader.fieldnames or [])
    for number, row in enumerate(rows, start=2):
        if None in row or None in row.values():
            raise ValueError(f"{path}: {number}번째 줄의 칸 수가 머리글과 다릅니다")
    return columns, rows


def write_csv(path, columns, rows, overwrite=False):
    """UTF-8 BOM·모든 칸 따옴표로 쓴다. 중간에 끊겨도 반쪽 파일이 남지 않게 임시 파일을 거친다."""
    path = Path(path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"기존 CSV는 덮어쓰지 않습니다: {path}")
    expected = set(columns)
    for number, row in enumerate(rows, start=1):
        if set(row) != expected:
            raise ValueError(f"{number}번째 행의 열이 약속과 다릅니다: {sorted(set(row) ^ expected)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding=ENCODING, newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(rows)
        os.chmod(temp_name, 0o644)
        os.replace(temp_name, path)
    except BaseException:
        os.unlink(temp_name)
        raise
    return path


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def html_filename(url):
    """저장 HTML 이름 규칙(02 문서 2장, 10월 zyte_run.py와 같음)."""
    return hashlib.sha1(url.encode()).hexdigest()[:16] + ".html.gz"


def call_preview(service, why, sends, scale, commands):
    """유료·외부 호출 전에 사람이 읽을 안내문: 왜 부르는지, 무엇을 보내는지, 규모와 실행 명령. 비밀값은 넣지 않는다."""
    lines = [f"## 호출 전 안내: {service}", "", f"- 왜 부르나: {why}", "- 보내는 값:"]
    lines += [f"  - {name}: {value}" for name, value in sends]
    lines += [f"- 규모·비용: {scale}", "- 실행 명령(승인 뒤):"]
    lines += [f"  - `{command}`" for command in commands]
    return "\n".join(lines) + "\n"


_SECRETS = set()


def read_secret(name, env_path=None):
    """저장소 루트 .env에서 비밀값을 읽고, 이후 로그에는 가려서 나오게 등록한다."""
    text = Path(env_path or REPO_ROOT / ".env").read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(name)}=(.*)$", text, re.M)
    if not match or not match.group(1).strip():
        raise ConfigError(f".env에 {name} 값이 없습니다")
    value = match.group(1).strip().strip("\"'")
    _SECRETS.add(value)
    return value


class _RedactSecrets(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        for secret in _SECRETS:
            message = message.replace(secret, "***")
        record.msg, record.args = message, None
        return True


def get_logger(run, step):
    """화면과 logs/{step}.log에 함께 남기는 로거. 등록된 비밀값은 가린다."""
    logger = logging.getLogger(f"pdp.{run.month}.{step}")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    logger.propagate = False
    run.sub("logs").mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    for handler in (logging.FileHandler(run.sub("logs") / f"{step}.log", encoding="utf-8"), logging.StreamHandler()):
        handler.setFormatter(formatter)
        handler.addFilter(_RedactSecrets())
        logger.addHandler(handler)
    return logger


def add_run_args(parser, paid=False):
    """모든 단계 공통 인자. paid=True면 --dry-run이 기본이고 --run을 줘야 실제 호출한다."""
    parser.add_argument("--month", default=date.today().strftime("%Y-%m"), help="회차 YYYY-MM (기본: 이번 달)")
    parser.add_argument("--force", action="store_true", help="출력이 이미 있어도 다시 만든다")
    if paid:
        mode = parser.add_mutually_exclusive_group()
        mode.add_argument("--dry-run", dest="live", action="store_false", help="건수·예상 비용만 출력(기본)")
        mode.add_argument("--run", dest="live", action="store_true", help="사용자 승인 뒤 실제 호출")
        parser.set_defaults(live=False)
    return parser


def new_parser(description, paid=False):
    return add_run_args(argparse.ArgumentParser(description=description), paid=paid)


def outputs_ready(paths, force=False):
    """이어받기(단계 단위): 출력이 모두 있으면 True. --force면 항상 False."""
    return not force and all(Path(path).exists() for path in paths)


class ResumeLog:
    """이어받기(건 단위): JSONL에 한 건씩 남기고, 다시 실행하면 끝난 건을 건너뛴다."""

    def __init__(self, path, key_field, is_done=lambda record: record.get("ok", True)):
        self.path, self.key_field, self.is_done = Path(path), key_field, is_done
        self.records = {}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._drop_partial_last_line()
        if self.path.exists():
            with self.path.open(encoding="utf-8") as handle:
                for line in handle:
                    record = json.loads(line)
                    self.records[record[key_field]] = record

    def _drop_partial_last_line(self):
        """쓰는 중 끊겨 줄바꿈 없이 잘린 마지막 줄은 끝나지 않은 건이므로 잘라 낸다."""
        if not self.path.exists() or self.path.stat().st_size == 0:
            return
        data = self.path.read_bytes()
        if not data.endswith(b"\n"):
            with self.path.open("r+b") as handle:
                handle.truncate(data.rfind(b"\n") + 1)

    def done(self, key):
        record = self.records.get(key)
        return record is not None and self.is_done(record)

    def append(self, record):
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.records[record[self.key_field]] = record
