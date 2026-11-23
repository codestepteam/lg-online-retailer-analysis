"""S6 공유용 변환: 내부판을 공유용 v1(기본 26열 + output.json share_extra_columns)으로 바꾸고 검증 기록과 READ.md 절 초안을 남긴다.

기본은 꾸민 xlsx(열 순서 share_columns_xlsx, D163)이고, --format csv면 예전 CSV 형식(열 순서 share_columns)으로 만든다."""
import glob
import json
import os
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path

from common import ConfigError, RunPaths, get_logger, load_output_spec, new_parser, outputs_ready, read_csv, read_table, sha256_file, write_csv

STATUS_COLUMN, STAGE_COLUMN, REASON_COLUMN, SELLER_KIND_COLUMN = "모수 포함 여부", "제외단계", "제외사유", "판매자구분"
INCLUDED, EXCLUDED = "포함", "제외"
INTERNAL_PATTERN = "전체판정_내부_*행_*.csv"
VERIFY_NAME, READ_NAME = "verify.json", "READ.md"
FORMATS = ("xlsx", "csv")
# xlsx 꾸밈. 글자로만 쓰므로 앞자리 0이나 긴 번호가 숫자로 바뀌지 않는다.
FROZEN_COLUMNS = ("행번호", "국가", "리테일러", "제품군", "브랜드", "제품코드", "상품명")
LINK_COLUMNS = ("확인 요청 URL", "접속 후 URL")
MAX_LINKS = 65530  # 엑셀 한 시트에 넣을 수 있는 링크 수 한도
URL_WIDTH, MAX_WIDTH, NAME_WIDTH = 45, 40, 30
HEADER_FILL, EXCLUDED_FILL = "D9E1F2", "EDEDED"


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


def share_name(spec, version, summary, rows, day, file_format="csv"):
    name = spec.share_filename.format(version=version, summary=summary, rows=rows, yyyymmdd=day)
    return str(Path(name).with_suffix(f".{file_format}"))


def file_format(path):
    return "xlsx" if Path(path).suffix.lower() == ".xlsx" else "csv"


def link_columns(columns, rows):
    """링크로 만들 열. 엑셀 링크 한도를 넘지 않게 LINK_COLUMNS 앞 열부터 통째로 넣는다(반만 링크인 열은 만들지 않는다)."""
    chosen, used = [], 0
    for column in LINK_COLUMNS:
        if column not in columns:
            continue
        count = sum(1 for row in rows if row[column].startswith("http"))
        if used + count > MAX_LINKS:
            break
        chosen.append(column)
        used += count
    return chosen


def write_share_xlsx(path, columns, rows, overwrite=False):
    """공유본 xlsx: 열 머리 필터, 첫 줄과 왼쪽 상품 열 고정, 열 너비, 링크, 제외 행 회색. 링크로 만든 열 목록을 돌려준다."""
    from openpyxl import Workbook
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import Font, PatternFill
    from openpyxl.utils import get_column_letter

    path = Path(path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"기존 공유본은 덮어쓰지 않습니다: {path}")
    expected = set(columns)
    for number, row in enumerate(rows, start=1):
        if set(row) != expected:
            raise ValueError(f"{number}번째 행의 열이 약속과 다릅니다: {sorted(set(row) ^ expected)}")
    links = link_columns(columns, rows)
    book = Workbook()
    sheet = book.active
    sheet.title = "전체판정"
    sheet.append(list(columns))
    for row in rows:
        sheet.append([row[column] for column in columns])  # 모두 글자(str)로 들어간다
    for column in links:
        index = columns.index(column) + 1
        for cells in sheet.iter_rows(min_row=2, min_col=index, max_col=index):
            cell = cells[0]
            if cell.value.startswith("http"):
                cell.hyperlink = cell.value
                cell.style = "Hyperlink"
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor=HEADER_FILL)
    last = get_column_letter(len(columns))
    sheet.auto_filter.ref = f"A1:{last}{len(rows) + 1}"
    frozen = sum(1 for column in columns[:len(FROZEN_COLUMNS)] if column in FROZEN_COLUMNS)
    sheet.freeze_panes = f"{get_column_letter(frozen + 1)}2"
    for index, column in enumerate(columns, start=1):
        if "URL" in column:
            width = URL_WIDTH
        elif column == "상품명":
            width = NAME_WIDTH  # 고정 열이라 좁게. 칸을 누르면 전체가 보인다
        else:
            longest = max([len(column)] + [len(row[column]) for row in rows[:2000]])
            width = min(max(longest + 2, 8), MAX_WIDTH)
        sheet.column_dimensions[get_column_letter(index)].width = width
    if STATUS_COLUMN in columns and rows:
        status = get_column_letter(columns.index(STATUS_COLUMN) + 1)
        sheet.conditional_formatting.add(f"A2:{last}{len(rows) + 1}", FormulaRule(formula=[f'${status}2="{EXCLUDED}"'], fill=PatternFill("solid", fgColor=EXCLUDED_FILL, bgColor=EXCLUDED_FILL)))
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    os.close(descriptor)
    try:
        book.save(temp_name)
        os.chmod(temp_name, 0o644)
        os.replace(temp_name, path)
    except BaseException:
        os.unlink(temp_name)
        raise
    return links


def write_share(path, columns, rows, overwrite=False):
    """확장자에 맞춰 공유본을 쓴다."""
    if file_format(path) == "xlsx":
        return write_share_xlsx(path, columns, rows, overwrite=overwrite)
    write_csv(path, columns, rows, overwrite=overwrite)
    return []


def check_rows(columns, rows, spec, file_format="csv"):
    """공유용 파일 약속을 검사해 문제 목록을 돌려준다."""
    problems = []
    if tuple(columns) != spec.columns_for(file_format):
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
    problems = check_rows(columns, rows, spec, file_format(path))
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
    parser.add_argument("--format", choices=FORMATS, default="xlsx", help="공유본 형식. csv면 예전 CSV 형식(열 순서도 예전 그대로)")
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"), help="파일명에 쓸 날짜(YYYYMMDD)")
    args = parser.parse_args(argv)
    run = RunPaths(args.month).create()
    logger = get_logger(run, "s6")
    spec = load_output_spec(run)
    final = run.sub("final")
    columns, rows = read_csv(latest_internal(final))
    if tuple(columns) != spec.internal_columns:
        raise ConfigError("내부판의 열이 output.json과 다릅니다")
    output = final / share_name(spec, 1, args.summary, len(rows), args.date, args.format)
    if outputs_ready([output, final / VERIFY_NAME, final / READ_NAME], args.force):
        logger.info("출력이 이미 있어 건너뜁니다(다시 하려면 --force)")
        return 0
    shared = to_share(rows, spec)
    columns = list(spec.columns_for(args.format))
    links = write_share(output, columns, shared, overwrite=args.force)
    if args.format == "xlsx":
        logger.info("xlsx 링크 열: %s", links or "없음(링크 한도 초과)")
    written_columns, written = read_table(output)  # 쓴 파일을 다시 읽어 검사한다
    if written != [{column: row[column] for column in columns} for row in shared]:
        raise ConfigError(f"쓴 공유본을 다시 읽은 값이 만든 값과 다릅니다: {output.name}")
    record = verification(output, written_columns, written, spec)
    save_verification(final / VERIFY_NAME, 1, record)
    (final / READ_NAME).write_text(read_section(record, 1, args.month, "새 달 첫 결과"), encoding="utf-8")
    logger.info("S6 끝: %s, 문제 %d건", output.name, record["problem_count"])
    return 0 if record["passed"] else 1
