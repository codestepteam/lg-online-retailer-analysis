"""S6 공유용 변환: 내부판을 공유용 v1(기본 26열 + output.json share_extra_columns)으로 바꾸고 검증 기록과 READ.md 절 초안을 남긴다."""
import glob
import json
from collections import Counter
from datetime import date
from pathlib import Path

from common import ConfigError, RunPaths, get_logger, load_output_spec, new_parser, outputs_ready, read_csv, sha256_file, write_csv

STATUS_COLUMN, STAGE_COLUMN, REASON_COLUMN, SELLER_KIND_COLUMN = "모수 포함 여부", "제외단계", "제외사유", "판매자구분"
INCLUDED, EXCLUDED = "포함", "제외"
INTERNAL_PATTERN = "전체판정_내부_*행_*.csv"
VERIFY_NAME, READ_NAME = "verify.json", "READ.md"


def to_share(rows, spec):
    """내부판 행을 공유용 행으로 바꾼다. 행 수·순서는 그대로다."""
    shared = []
    for row in rows:
        converted = {}
        for column in spec.internal_columns:
            if column in spec.share_dropped:
                continue
            value = spec.share_status_map[row[column]] if column == "판정" else row[column]
            for old, new in spec.share_wording.items():
                value = value.replace(old, new)
            converted[spec.share_renames.get(column, column)] = value
        for name, rule in spec.share_extra.items():
            source = converted[rule["from"]]
            if source not in rule["map"]:
                raise ConfigError(f"행 {converted['행번호']}: {rule['from']} 값 {source!r}을 {name}로 바꿀 규칙이 없습니다")
            converted[name] = rule["map"][source]
        shared.append(converted)
    return shared


def share_name(spec, version, summary, rows, day):
    return spec.share_filename.format(version=version, summary=summary, rows=rows, yyyymmdd=day)


def check_rows(columns, rows, spec):
    """공유용 파일 약속을 검사해 문제 목록을 돌려준다."""
    problems = []
    if tuple(columns) != spec.all_share_columns:
        problems.append("열 이름·순서가 output.json과 다름")
        return problems
    if [row["행번호"] for row in rows] != [str(number) for number in range(1, len(rows) + 1)]:
        problems.append("행번호가 1부터 순서대로가 아님")
    for row in rows:
        number, status, stage, reason = row["행번호"], row[STATUS_COLUMN], row[STAGE_COLUMN], row[REASON_COLUMN]
        if status not in (INCLUDED, EXCLUDED):
            problems.append(f"행 {number}: 모수 포함 여부 값 {status}")
        if status == EXCLUDED and (stage not in spec.exclusion_stages or not reason):
            problems.append(f"행 {number}: 제외 행의 제외단계·사유가 비었거나 잘못됨")
        if status == INCLUDED and (stage or reason):
            problems.append(f"행 {number}: 포함 행에 제외단계·사유가 있음")
        if row[SELLER_KIND_COLUMN] and row[SELLER_KIND_COLUMN] not in spec.seller_types:
            problems.append(f"행 {number}: 판매자구분 값 {row[SELLER_KIND_COLUMN]}")
        for name, rule in spec.share_extra.items():
            if row[name] != rule["map"].get(row[rule["from"]]):
                problems.append(f"행 {number}: {name} 값 {row[name]}이 {rule['from']} 값 {row[rule['from']]}과 맞지 않음")
        if any(old in value for old in spec.share_wording for value in row.values()):
            problems.append(f"행 {number}: 공유용에 쓰면 안 되는 표현이 남음")
    return problems


def verification(path, columns, rows, spec):
    problems = check_rows(columns, rows, spec)
    return {"file": Path(path).name, "sha256": sha256_file(path), "rows": len(rows), "columns": len(columns),
            "status": dict(Counter(row[STATUS_COLUMN] for row in rows)), "stages": dict(Counter(row[STAGE_COLUMN] for row in rows if row[STAGE_COLUMN])),
            "problems": problems[:50], "problem_count": len(problems), "passed": not problems}


def save_verification(path, version, record):
    records = json.loads(Path(path).read_text(encoding="utf-8")) if Path(path).exists() else {}
    records[f"v{version}"] = record
    Path(path).write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_section(record, version, month, note):
    status = record["status"]
    lines = [f"## v{version} ({month})", "", f"- 파일: `{record['file']}`", f"- 행 {record['rows']:,} · 열 {record['columns']}", f"- 포함 {status.get(INCLUDED, 0):,} · 제외 {status.get(EXCLUDED, 0):,}", f"- {note}", "",
             "| 제외단계 | 행 수 |", "| --- | --- |"]
    return "\n".join(lines + [f"| {stage} | {count:,} |" for stage, count in sorted(record["stages"].items())]) + "\n\n"


def latest_internal(final):
    found = sorted(glob.glob(str(final / INTERNAL_PATTERN)))
    if len(found) != 1:
        raise ConfigError(f"내부판은 정확히 1개여야 합니다: {len(found)}개")
    return Path(found[0])


def main(argv):
    parser = new_parser("S6 공유용 변환: 내부판 → 공유용 v1")
    parser.add_argument("--summary", required=True, help="파일명의 변경요지")
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"), help="파일명에 쓸 날짜(YYYYMMDD)")
    args = parser.parse_args(argv)
    run = RunPaths(args.month).create()
    logger = get_logger(run, "s6")
    spec = load_output_spec(run)
    final = run.sub("final")
    columns, rows = read_csv(latest_internal(final))
    if tuple(columns) != spec.internal_columns:
        raise ConfigError("내부판의 열이 output.json과 다릅니다")
    output = final / share_name(spec, 1, args.summary, len(rows), args.date)
    if outputs_ready([output, final / VERIFY_NAME, final / READ_NAME], args.force):
        logger.info("출력이 이미 있어 건너뜁니다(다시 하려면 --force)")
        return 0
    shared = to_share(rows, spec)
    write_csv(output, list(spec.all_share_columns), shared, overwrite=args.force)
    record = verification(output, spec.all_share_columns, shared, spec)
    save_verification(final / VERIFY_NAME, 1, record)
    (final / READ_NAME).write_text(read_section(record, 1, args.month, "새 달 첫 결과"), encoding="utf-8")
    logger.info("S6 끝: %s, 문제 %d건", output.name, record["problem_count"])
    return 0 if record["passed"] else 1
