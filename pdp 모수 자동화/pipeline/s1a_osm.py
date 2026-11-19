"""S1a OSM 후보: 콘솔 04 쿼리(audit)를 만들고, 승인 뒤에만 BigQuery로 실행한다.

기본은 SQL 파일, 호출 전 안내, 브랜드 보고서만 만든다(외부 호출 없음).
--estimate는 BigQuery 처리량만 확인하고, --run은 실제로 실행한 뒤 후보로 변환한다. 둘 다 사용자 승인 뒤에만 쓴다.
--from-audit는 이미 받은 자료로 후보 변환만 한다(외부 호출 없음).
"""
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from common import ConfigError, RunPaths, call_preview, get_logger, load_config, new_parser, read_csv, write_csv

RENDER_CODE = """
import json, sys
from bqconsole.pdp import render_pdp
from bqconsole.catalog import COUNTRY_CODES
request = json.load(sys.stdin)
sys.stdout.write(render_pdp(request["params"], request["countries"], request["targets"], COUNTRY_CODES))
"""


def normalized(brand):
    """콘솔 쿼리가 브랜드를 비교하는 방식과 같게 맞춘다(대문자, 공백 제거)."""
    return re.sub(r"\s+", "", brand.upper())


def console_targets(run):
    path = Path(load_config(run, "s0_input")["console_fixed_targets"]).expanduser()
    return json.loads(path.read_text(encoding="utf-8"))["targets"]


def brand_category(div, query, category_fallback):
    return query["div_to_brand_category"].get(div) or query["div_to_brand_category"].get(category_fallback.get(div))


def add_missing_divs(targets, additions):
    """콘솔 대상에 없는 제품군을 다른 제품군의 브랜드로 더한다. (넓힌 대상, 더한 (국가, 리테일러, 제품군) 목록)을 돌려준다."""
    expanded, added = [], []
    for target in targets:
        extra = {div: list(target["brands"][source]) for div, source in additions.items() if div not in target["brands"] and source in target["brands"]}
        expanded.append({**target, "brands": {**target["brands"], **extra}})
        added += [(target["country"], target["retailer"], div) for div in extra]
    return expanded, added


def exclude_from_date_choice(sql, added):
    """더한 제품군은 후보로는 뽑되, 리테일러 기준일을 고르는 계산에서는 뺀다."""
    if not added:
        return sql
    keys = ",".join(f"'{country}|{retailer}|{div}'" for country, retailer, div in added)
    condition = "CONCAT({0}CNTRY,'|',{0}RTLR_NAME,'|',{0}DIV) NOT IN ({1})"
    replacements = {
        "COUNT(DISTINCT DIV) GROUP_COUNT FROM brand_map GROUP BY 1,2": f"COUNT(DISTINCT DIV) GROUP_COUNT FROM brand_map WHERE {condition.format('', keys)} GROUP BY 1,2",
        "WHERE b.OBSERVED_DAYS>=3 AND d.URL_COUNT>=b.BASELINE_URLS*0.8": f"WHERE b.OBSERVED_DAYS>=3 AND d.URL_COUNT>=b.BASELINE_URLS*0.8 AND {condition.format('d.', keys)}",
    }
    for anchor, replacement in replacements.items():
        if sql.count(anchor) != 1:
            raise ConfigError(f"콘솔 쿼리 구조가 달라져 기준일 조건을 고칠 수 없습니다: {anchor}")
        sql = sql.replace(anchor, replacement)
    return sql


def fix_selected_dates(sql, fixed):
    """사람이 정한 리테일러만 기준일을 고정한다(osm_query.fixed_dates). 나머지는 규칙대로 고른다.
    예: 2026-11 COSTCO는 규칙이 고른 11-16에 배너 노출 표가 비어 건조기가 0행이라 11-15로 고정했다."""
    if not fixed:
        return sql
    whens = " ".join(f"WHEN CONCAT(r.CNTRY,'|',r.RTLR_NAME)='{key}' THEN DATE '{value['date']}'" for key, value in fixed.items())
    reasons = " ".join(f"WHEN CONCAT(CNTRY,'|',RTLR_NAME)='{key}' THEN '사람 지정 기준일 · {value['reason']}'" for key, value in fixed.items())
    replacements = {
        "SELECT r.CNTRY,r.RTLR_NAME,MAX(e.RPT_DATE) SELECTED_DATE": f"SELECT r.CNTRY,r.RTLR_NAME,CASE {whens} ELSE MAX(e.RPT_DATE) END SELECTED_DATE",
        "CASE WHEN SELECTED_DATE IS NULL THEN": f"CASE {reasons} WHEN SELECTED_DATE IS NULL THEN",
    }
    for anchor, replacement in replacements.items():
        if sql.count(anchor) != 1:
            raise ConfigError(f"콘솔 쿼리 구조가 달라져 지정 기준일을 넣을 수 없습니다: {anchor}")
        sql = sql.replace(anchor, replacement)
    return sql


BRAND_KEY_ANCHOR = "CASE WHEN UPPER(TRIM(BRAND)) ='LG ELECTRONICS' THEN 'LG' ELSE"


def prefix_brand_key(sql, prefix):
    """osm_brand_prefix 리테일러는 BRAND_KEY를 맨 앞 영문 단어로 만든다(D142·D144: 'LG 樂金' → LG). 콘솔 쿼리는 공백만 지운 전체 이름을 비교해 이런 표기를 후보에서 뺀다.
    lgops 서버는 REGEXP_EXTRACT를 받지 않아(11-18 실호출 HTTP 400) 10월 momo_pid.sql처럼 REGEXP_REPLACE로 앞 단어만 남긴다."""
    retailers = (prefix or {}).get("retailers", [])
    if not retailers:
        return sql
    if sql.count(BRAND_KEY_ANCHOR) != 1:
        raise ConfigError(f"콘솔 쿼리 구조가 달라져 브랜드 비교를 고칠 수 없습니다: {BRAND_KEY_ANCHOR}")
    names = ",".join(f"'{name.upper()}'" for name in retailers)
    case = f"WHEN UPPER(RTLR_NAME) IN ({names}) AND REGEXP_CONTAINS(UPPER(TRIM(BRAND)),r'{prefix['pattern']}') THEN REGEXP_REPLACE(UPPER(TRIM(BRAND)),r'{prefix['pattern']}.*$',r'\\1')"
    return sql.replace(BRAND_KEY_ANCHOR, f"CASE WHEN UPPER(TRIM(BRAND)) ='LG ELECTRONICS' THEN 'LG' {case} ELSE")


def merge_brands(targets, ey_brands, category_fallback, query, country_alias):
    """제품군 목록은 그대로 두고 브랜드만 콘솔 ∪ EY로 넓힌다. (넘길 대상, 보고 행)을 돌려준다."""
    merged, report = [], []
    for target in targets:
        country = country_alias.get(target["country"], target["country"])
        brands = {}
        for div, console in target["brands"].items():
            category = brand_category(div, query, category_fallback)
            if category is None:
                raise ConfigError(f"제품군을 브랜드 구분으로 바꿀 수 없습니다: {div}")
            sheet = ey_brands.get(country, {}).get(category, [])
            have = {normalized(b) for b in console}
            added = [b for b in sheet if normalized(b) not in have]
            brands[div] = list(console) + added
            sheet_keys = {normalized(b) for b in sheet}
            report.append({"country": country, "retailer": target["retailer"], "div": div, "console": len(console), "sheet": len(sheet),
                           "added": added, "console_only": [b for b in console if normalized(b) not in sheet_keys]})
        merged.append({**target, "brands": brands})
    return merged, report


def render_sql(query, countries, targets):
    python = Path(query["console_python"]).expanduser()
    if not python.exists():
        raise ConfigError(f"콘솔 파이썬이 없습니다: {python}")
    payload = json.dumps({"params": query["render_params"], "countries": countries, "targets": targets})
    done = subprocess.run([str(python), "-c", RENDER_CODE], input=payload, capture_output=True, text=True)
    if done.returncode != 0:
        raise ConfigError(f"콘솔 쿼리 생성 실패: {done.stderr.strip()[-500:]}")
    return done.stdout


def osm_preview(run, query, sql_path, sql, end_date, report, added_divs):
    """BigQuery를 부르기 전에 왜 부르는지와 보내는 값을 사람이 읽을 수 있게 정리한다."""
    places = list(dict.fromkeys((r["country"], r["retailer"]) for r in report))
    base = f"python pipeline/run.py s1a --month {run.month} --end-date {end_date}"
    sends = [
        ("요청 기준일", f"{end_date} (이 날까지 최근 30일 중 수집량이 충분한 가장 최근 날을 리테일러별로 자동 선택)"),
        ("조회 테이블", ", ".join(sorted(set(re.findall(r"(?:FROM|JOIN)\s+`([^`]+)`", sql))))),
        ("쿼리 옵션", ", ".join(f"{name}={value}" for name, value in query["params"].items()) + " (전체 행과 판정 표시를 받고, 콘솔 제외 필터는 끔)"),
        ("대상", f"{len(places)}곳: " + ", ".join(f"{c} {r}" for c, r in places)),
        ("제품군·브랜드", f"리테일러·제품군 {len(report)}줄, 브랜드 {sum(r['console'] + len(r['added']) for r in report):,}개 (곳별 표는 아래)"),
        ("콘솔 대상에 더한 제품군", f"{len(added_divs)}곳 — " + ", ".join(f"{c} {r} {d}" for c, r, d in added_divs)),
        ("SQL", f"{sql_path} ({len(sql):,}자, 지문 {hashlib.sha256(sql.encode()).hexdigest()[:12]})"),
    ]
    return call_preview(
        "BigQuery (lgops → 콘솔 서버)", "이번 회차 OSM 보유 리테일러의 PDP 후보 URL을 가져옵니다(S1a). 조회만 하고 데이터를 바꾸지 않습니다.", sends,
        "처리량은 `--estimate`로 확인합니다(이 안내만으로는 호출하지 않습니다). 실제 요금은 LG 계정 청구 방식을 확인하지 못했습니다.",
        [f"{base} --estimate", f"{base} --run"],
    )


def render_report(end_date, sql_length, query, report, added_divs, preview):
    added = [r for r in report if r["added"]]
    lines = [
        preview,
        f"# OSM 쿼리 생성 보고 (요청 기준일 {end_date})", "",
        f"- SQL 길이: {sql_length:,}자 (한도 {query['max_sql_chars']:,}자)",
        f"- 대상: {len({(r['country'], r['retailer']) for r in report})}곳, 리테일러·제품군 {len(report)}줄",
        f"- 콘솔 브랜드 목록에 없어 EY 시트·#110에서 더한 줄: {len(added)}줄, 브랜드 {sum(len(r['added']) for r in added)}개",
        f"- 콘솔 대상에 없어 더한 제품군(후보로만 뽑고 기준일 선정에는 안 씀): {len(added_divs)}곳 — " + ", ".join(f"{c} {r} {d}" for c, r, d in added_divs), "",
        "| 국가 | 리테일러 | 제품군 | 콘솔 수 | 시트 수 | 더한 브랜드 | 콘솔에만 있는 브랜드(S2에서 거름) |", "| --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    lines += [f"| {r['country']} | {r['retailer']} | {r['div']} | {r['console']} | {r['sheet']} | {', '.join(r['added'])} | {', '.join(r['console_only'])} |" for r in report]
    return "\n".join(lines) + "\n"


def build(run, end_date):
    """(설정, 넘긴 대상, 보고 행, 더한 제품군, SQL)을 돌려준다. 파일은 쓰지 않는다."""
    query = load_config(run, "osm_query")
    s0_input = load_config(run, "s0_input")
    brands = load_config(run, "brands")
    expanded, added_divs = add_missing_divs(console_targets(run), query["add_missing_divs"])
    targets, report = merge_brands(expanded, brands["brands"], brands["category_fallback"], query, s0_input["country_alias"])
    query["render_params"] = {**query["params"], "end_date": end_date}
    countries = list(dict.fromkeys(t["country"] for t in targets))
    sql = exclude_from_date_choice(render_sql(query, countries, targets), added_divs)
    sql = prefix_brand_key(sql, load_config(run, "retailer_rules")["common"].get("osm_brand_prefix"))
    sql = fix_selected_dates(sql, {key: value for key, value in query.get("fixed_dates", {}).items() if not key.startswith("_")})
    if len(sql) > query["max_sql_chars"]:
        raise ConfigError(f"SQL이 {len(sql)}자로 한도를 넘습니다")
    return query, targets, report, added_divs, sql


def prepare(run, end_date):
    query, _, report, added_divs, sql = build(run, end_date)
    run.sub("candidates").mkdir(parents=True, exist_ok=True)
    path = run.sub("candidates") / "osm_query.sql"
    path.write_text(sql, encoding="utf-8")
    preview = osm_preview(run, query, path, sql, end_date, report, added_divs)
    (run.sub("candidates") / "osm_query_report.md").write_text(render_report(end_date, len(sql), query, report, added_divs, preview), encoding="utf-8")
    return query, path, sql, report, preview


def read_audit(path):
    """lgops가 저장한 JSONL 또는 콘솔에서 내려받은 CSV를 같은 행 목록으로 읽는다."""
    path = Path(path)
    if path.suffix.lower() == ".csv":
        return read_csv(path)[1]
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def cell(value):
    """값 없음(None·BigQuery의 \\N)은 빈칸으로, 참·거짓은 소문자로 맞춘다."""
    if value is None or value == "\\N":
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def crawl_url(row, rules):
    for rule in rules:
        if (rule["country"], rule["retailer"]) == (row["CNTRY"], row["RTLR_NAME"]):
            return re.sub(rule["strip_pattern"], "", row["CAT_URL_ADDR"]) + rule["append"]
    return row["RAW_URL"]


def to_candidates(audit, settings):
    """콘솔이 대표로 남긴 행만 후보로 바꾼다. (후보 행, 사이트 첫 화면이라 뺀 행 수)를 돌려준다."""
    source_columns = set(settings["columns"]) - {"CRAWL_URL"} | {"RESULT_STATUS", "CAT_URL_ADDR", "REQUESTED_DATE", "DATE_LAG_DAYS", "DATE_SELECTION_REASON"}
    missing = source_columns - set(audit[0]) if audit else source_columns
    if missing:
        raise ConfigError(f"audit 자료에 필요한 열이 없습니다: {sorted(missing)}")
    candidates, home_rows = [], 0
    for row in audit:
        if row["RESULT_STATUS"] != settings["keep_status"] or not cell(row["RAW_URL"]):
            continue
        if re.search(settings["home_url_pattern"], row["RAW_URL"].strip()):
            home_rows += 1
            continue
        values = {name: cell(row[name]) for name in settings["columns"] if name != "CRAWL_URL"}
        candidates.append({**values, "CRAWL_URL": crawl_url(row, settings["crawl_url_rules"])})
    return candidates, home_rows


def render_date_report(audit, candidates, home_rows, targets, needs_check_prefix):
    """리테일러별 선정 기준일과 사유. 결과가 한 줄도 없는 곳도 빠뜨리지 않고 확인 필요로 적는다."""
    first, audit_counts = {}, Counter()
    for row in audit:
        key = (row["CNTRY"], row["RTLR_NAME"])
        first.setdefault(key, row)
        audit_counts[key] += 1
    candidate_counts = Counter((row["CNTRY"], row["RTLR_NAME"]) for row in candidates)
    table = []
    for target in targets:
        key = (target["country"], target["retailer"])
        row = first.get(key)
        table.append([*key, *(cell(row[name]) for name in ("REQUESTED_DATE", "RPT_DATE", "DATE_LAG_DAYS", "DATE_SELECTION_REASON"))] if row
                     else [*key, "", "", "", f"{needs_check_prefix} · 결과 행 없음"])
        table[-1] += [audit_counts[key], candidate_counts[key]]
    flagged = [line for line in table if line[5].startswith(needs_check_prefix)]
    lines = ["# OSM 기준일 보고", "", f"- 대상 {len(table)}곳, 후보 {len(candidates):,}행 (audit {len(audit):,}행, 사이트 첫 화면이라 뺀 행 {home_rows:,})",
             f"- `{needs_check_prefix}` {len(flagged)}곳" + (": " + ", ".join(f"{line[0]} {line[1]}" for line in flagged) if flagged else ""), "",
             "| 국가 | 리테일러 | 요청 기준일 | 선정 기준일 | 며칠 전 | 선정 사유 | audit 행 | 후보 행 |", "| --- | --- | --- | --- | ---: | --- | ---: | ---: |"]
    lines += ["| " + " | ".join(str(value) for value in line) + " |" for line in table]
    return "\n".join(lines) + "\n"


def convert(run, audit_path, overwrite=False):
    """audit 자료로 osm_candidates.csv와 osm_date_report.md를 만든다. 외부 호출 없음."""
    settings = load_config(run, "osm_query")["candidates"]
    audit = read_audit(audit_path)
    candidates, home_rows = to_candidates(audit, settings)
    folder = run.sub("candidates")
    write_csv(folder / "osm_candidates.csv", settings["columns"], candidates, overwrite=overwrite)
    (folder / "osm_date_report.md").write_text(render_date_report(audit, candidates, home_rows, console_targets(run), settings["needs_check_prefix"]), encoding="utf-8")
    return len(audit), len(candidates), home_rows


def lgops_command(query, sql_path, out_path=None, estimate=False):
    executable = shutil.which(query["lgops"])
    if executable is None:
        raise ConfigError(f"{query['lgops']} 명령을 찾지 못했습니다")
    command = [executable]
    if out_path is not None:
        command += ["--out", str(out_path)]
    command += ["bq", f"@{sql_path}"]
    return command + (["--dry-run"] if estimate else [])


def run_lgops(command, capture=False):
    return subprocess.run(command, check=True, capture_output=capture, text=capture)


def report_conversion(logger, counts):
    logger.info("변환: audit %d행 → 후보 %d행 (사이트 첫 화면 제외 %d행)", *counts)


def main(argv):
    parser = new_parser("S1a OSM 후보: 콘솔 04 쿼리 생성·처리량 확인·실행·후보 변환", paid=True)
    parser.add_argument("--estimate", action="store_true", help="사용자 승인 뒤 BigQuery 처리량만 확인")
    parser.add_argument("--end-date", default=None, help="요청 기준일 YYYY-MM-DD (기본: 어제)")
    parser.add_argument("--from-audit", default=None, help="이미 받은 audit 자료(JSONL 또는 콘솔 CSV)로 후보 변환만 한다. 외부 호출 없음")
    args = parser.parse_args(argv)
    if args.estimate and args.live:
        parser.error("--estimate와 --run은 함께 쓸 수 없습니다")
    if args.from_audit and (args.estimate or args.live):
        parser.error("--from-audit는 --estimate·--run과 함께 쓸 수 없습니다")
    run = RunPaths(args.month).create()
    logger = get_logger(run, "s1a")
    if args.from_audit:
        report_conversion(logger, convert(run, args.from_audit, overwrite=args.force))
        return 0
    out_path = run.sub("candidates") / "osm_audit.jsonl"
    if args.live and out_path.exists() and not args.force:
        logger.info("%s 가 이미 있어 실행하지 않습니다(다시 하려면 --force, 변환만 하려면 --from-audit)", out_path)
        return 0
    end_date = args.end_date or (date.today() - timedelta(days=1)).isoformat()
    query, sql_path, sql, report, preview = prepare(run, end_date)
    logger.info("SQL 생성: %s (%d자), 요청 기준일 %s, 대상 %d곳", sql_path, len(sql), end_date, len({(r["country"], r["retailer"]) for r in report}))
    if args.estimate:
        logger.info("BigQuery 처리량: %s", run_lgops(lgops_command(query, sql_path, estimate=True), capture=True).stdout)
    elif args.live:
        run_lgops(lgops_command(query, sql_path, out_path=out_path))
        logger.info("저장: %s", out_path)
        report_conversion(logger, convert(run, out_path, overwrite=True))
    else:
        logger.info("외부 호출 없이 끝냈습니다.\n%s", preview)
    return 0
