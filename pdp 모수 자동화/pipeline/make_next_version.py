"""이번 달 공유용의 다음 버전을 변경 대상 CSV로 만든다. 기존 파일은 고치지 않는다(D085).

변경 대상 CSV는 공유용 26열 + 변경요청_모수 포함 여부 + 확인상태 + 메모추가. 그 밖에 변경_{열이름} 열을 두면 그 칸을 새 값으로 바꾼다.
26열 값이 현재 파일과 하나라도 다르면(오래된 대상 파일) 멈춘다.
현재 공유본이 xlsx면 다음 버전도 같은 열 순서의 xlsx로, CSV면 CSV로 만든다(D163). 변경 대상 파일은 CSV나 xlsx 모두 읽는다.
"""
import re
from collections import Counter
from datetime import date

from common import ConfigError, RunPaths, get_logger, load_output_spec, new_parser, read_table
from s6_share import EXCLUDED, INCLUDED, READ_NAME, REASON_COLUMN, STAGE_COLUMN, STATUS_COLUMN, VERIFY_NAME, read_section, file_format, save_verification, share_name, verification, write_share

REQUEST_COLUMN, CONFIRM_COLUMN, MEMO_COLUMN, CHANGE_PREFIX = "변경요청_모수 포함 여부", "확인상태", "메모추가", "변경_"
VERSION_PATTERN = re.compile(r"PDP모수_공유용_v(\d+)_")


def latest_version(final):
    """(버전 번호, 경로) 중 가장 높은 버전."""
    found = [(int(match.group(1)), path) for path in final.glob("PDP모수_공유용_v*") if path.suffix.lower() in (".csv", ".xlsx") if (match := VERSION_PATTERN.match(path.name))]
    if not found:
        raise ConfigError("공유용 파일이 없습니다. S6를 먼저 실행하세요")
    return max(found, key=lambda item: item[0])


def apply_changes(columns, rows, changes_columns, changes, spec):
    """변경 대상을 적용한 새 행 목록을 돌려준다. 원본 행은 건드리지 않는다."""
    if list(changes_columns[:len(columns)]) != list(columns):
        raise ConfigError("변경 대상 CSV의 앞 26열이 공유용 열과 다릅니다")
    for name in (REQUEST_COLUMN, CONFIRM_COLUMN, MEMO_COLUMN):
        if name not in changes_columns:
            raise ConfigError(f"변경 대상 CSV에 {name} 열이 없습니다")
    if len({change["행번호"] for change in changes}) != len(changes):
        raise ConfigError("변경 대상 CSV에 같은 행번호가 두 번 있습니다")
    extra = [name for name in changes_columns if name.startswith(CHANGE_PREFIX)]
    unknown = [name for name in extra if name[len(CHANGE_PREFIX):] not in columns]
    if unknown:
        raise ConfigError(f"변경 대상 CSV에 없는 열을 바꾸려 합니다: {unknown}")
    updated = [dict(row) for row in rows]
    by_number = {row["행번호"]: row for row in updated}
    for change in changes:
        number = change["행번호"]
        row = by_number.get(number)
        if row is None:
            raise ConfigError(f"행번호 {number}: 공유용에 없습니다")
        if any(change[column] != row[column] for column in columns):
            raise ConfigError(f"행번호 {number}: 변경 대상의 값이 현재 공유용과 다릅니다")
        request = change[REQUEST_COLUMN]
        if request not in (INCLUDED, EXCLUDED) or request == row[STATUS_COLUMN] or change[CONFIRM_COLUMN] != request:
            raise ConfigError(f"행번호 {number}: 요청값·확인상태가 잘못됐습니다(현재 {row[STATUS_COLUMN]}, 요청 {request}, 확인 {change[CONFIRM_COLUMN]})")
        if not change[MEMO_COLUMN].strip():
            raise ConfigError(f"행번호 {number}: 메모추가가 비었습니다")
        row[STATUS_COLUMN] = request
        if request == INCLUDED:
            row[STAGE_COLUMN], row[REASON_COLUMN] = "", ""
        for name in extra:
            if change[name]:
                row[name[len(CHANGE_PREFIX):]] = change[name]
        if request == EXCLUDED and (row[STAGE_COLUMN] not in spec.exclusion_stages or not row[REASON_COLUMN]):
            raise ConfigError(f"행번호 {number}: 포함→제외에는 변경_제외단계·변경_제외사유가 필요합니다")
        row["메모"] = "; ".join(part for part in (row["메모"], change[MEMO_COLUMN].strip()) if part)
    return updated


def main(argv):
    parser = new_parser("다음 버전 만들기: 변경 대상 CSV → v{N+1}")
    parser.add_argument("--changes", required=True, help="changes 폴더 안 변경 대상 CSV 파일 이름")
    parser.add_argument("--summary", required=True, help="파일명의 변경요지")
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"), help="파일명에 쓸 날짜(YYYYMMDD)")
    args = parser.parse_args(argv)
    run = RunPaths(args.month).create()
    logger = get_logger(run, "next")
    spec = load_output_spec(run)
    final = run.sub("final")
    version, current = latest_version(final)
    columns, rows = read_table(current)
    changes_path = run.sub("changes") / args.changes
    if not changes_path.exists():
        raise ConfigError(f"변경 대상 CSV가 없습니다: {changes_path}")
    change_columns, changes = read_table(changes_path)
    updated = apply_changes(columns, rows, change_columns, changes, spec)
    output = final / share_name(spec, version + 1, args.summary, len(updated), args.date, file_format(current))
    write_share(output, list(columns), updated)
    record = verification(output, columns, updated, spec)
    save_verification(final / VERIFY_NAME, version + 1, record)
    with open(final / READ_NAME, "a", encoding="utf-8") as stream:
        stream.write(read_section(record, version + 1, args.month, f"{current.name}에서 {len(changes)}행 변경({args.summary})"))
    logger.info("다음 버전 끝: %s, 변경 %d행, 포함 여부 %s, 문제 %d건", output.name, len(changes), dict(Counter(row[STATUS_COLUMN] for row in updated)), record["problem_count"])
    return 0 if record["passed"] else 1
