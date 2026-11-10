"""S5 최종 판정: S2 결과에 페이지 상태·판매자를 합쳐 내부판을 만든다.

순서(D108): ③리리부(판매자) → ④페이지없음·영구품절·품절·판매중단 → ④중복. 한 행은 처음 걸린 단계에서 멈춘다.
페이지가 없거나 영구품절이면 판매자를 읽을 수 없으므로 그 상태로 바로 제외한다. 규칙 값은 retailer_rules.json의 final 절에서 읽는다.
"""
import json
import re
from collections import Counter
from datetime import date
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from common import REPO_ROOT, ConfigError, RunPaths, get_logger, load_config, load_output_spec, new_parser, outputs_ready, read_csv, write_csv
from rules import codes
from s2_filter import CHECK, DUPLICATE_STAGE, EXCLUDE, KEEP, OSM_FLOW
from s4_sellers import NORMAL_PAGE, html_reader

UNKNOWN_KIND = "확인불가"
NULL_VALUES = ("", "\\N")
OSM_FILE = "osm_candidates.csv"
CODE_EVIDENCE_NAME = "product_code_evidence.csv"
CODE_EVIDENCE_COLUMNS = ["행번호", "국가", "리테일러", "URL", "상품명", "브랜드", "제품코드", "브랜드 찾은곳", "제품코드 찾은곳"]
INTERNAL_NAME = "전체판정_내부_{rows}행_{date}.csv"
PREVIOUS_INCLUDED = "포함"
VS_COLUMNS = ["국가", "리테일러", "전월 포함", "이번 달 포함", "공통", "새로 포함", "빠짐"]


def add_memo(row, text):
    row["메모"] = "; ".join(part for part in (row["메모"], text) if part)


def exclude(row, stage, reason):
    row["판정"], row["제외단계"], row["제외사유"] = EXCLUDE, stage, reason


def effective_status(row, page, settings):
    """저장된 상태를 주소 기준으로 보정한다: not-found 주소로 간 페이지와, 사람이 직접 열어도 차단 화면만 나와 없는 페이지로 친 경우(D068)."""
    status = page["status"]
    if re.search(settings["not_found_url"], row["실제URL"]):
        return settings["not_found_status"]
    if status == settings["block_status"] and row["리테일러"] in settings["block_as_missing_retailers"] and page.get("method") in settings["block_as_missing_methods"]:
        return f'없음({status})'
    return status


def page_outcome(status, settings):
    return next((item for item in settings["page_outcomes"] if status.startswith(item["status_prefix"])), None)


def exception_for(row, name, kind, exceptions):
    for rule in exceptions:
        if rule["retailer"] != row["리테일러"] or rule.get("country", row["국가"]) != row["국가"]:
            continue
        if ("sellers" in rule and name not in rule["sellers"]) or ("kinds" in rule and kind not in rule["kinds"]) or name in rule.get("not_sellers", ()):
            continue
        return rule
    return None


def unknown_outcome(row, evidence, settings):
    for rule in settings["unknown_seller_outcomes"]:
        if rule["retailer"] == row["리테일러"] and rule.get("country", row["국가"]) == row["국가"] and rule.get("evidence", "") in evidence and rule.get("url_contains", "") in row["URL"]:
            return rule
    return None


def apply_seller(row, seller, settings):
    """판매자 규칙을 적용하고, 이 행이 제외로 끝났으면 True를 돌려준다."""
    if seller is None or seller["판매자구분"] == UNKNOWN_KIND:
        outcome = unknown_outcome(row, seller["근거"], settings) if seller else None
        if outcome:
            exclude(row, outcome["stage"], outcome["reason"])
            return True
        row["판정"] = CHECK
        add_memo(row, settings["unknown_seller_memo"])
        return False
    name, kind = seller["판매자"], seller["판매자구분"]
    label = settings["excluded_seller_types"].get(kind)
    if label is None:
        return False
    rule = exception_for(row, name, kind, settings["include_exceptions"])
    if rule:
        add_memo(row, rule["memo"])
        return False
    exclude(row, "③리리부", f"{label} ({name})")
    return True


def exclude_for_page(row, outcome, status, page, settings):
    exclude(row, outcome["stage"], outcome["reason"].format(status=status, title=page.get("title", "")[:settings["title_chars"]]))


def judge_row(row, page, seller, settings):
    """제외되지 않은 행 하나에 페이지·판매자 판정을 적용한다."""
    if page is None:
        row["판정"] = CHECK
        add_memo(row, settings["no_page_memo"])
        return
    row["페이지상태"], row["실제URL"] = page["status"], page.get("final_url") or row["URL"]
    if seller:
        row["판매자"], row["판매자구분"], row["판매자근거"] = seller["판매자"], seller["판매자구분"], seller["근거"][:settings["evidence_chars"]]
    status = effective_status(row, page, settings)
    outcome = page_outcome(status, settings)
    if outcome and status not in settings["seller_before_status"]:
        exclude_for_page(row, outcome, status, page, settings)
        return
    if status != NORMAL_PAGE and not outcome:
        row["판정"] = CHECK
        add_memo(row, f"페이지 {status}")
        return
    word = settings["accessory_category"].get(row["리테일러"])
    if word and word in page.get("category_path", ""):
        exclude(row, "③리리부", settings["accessory_reason"])
        return
    if apply_seller(row, seller, settings):
        return
    if outcome:
        exclude_for_page(row, outcome, status, page, settings)


def drop_params(url, names):
    parts = urlsplit(url)
    kept = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key not in names]
    return urlunsplit(parts._replace(query=urlencode(kept)))


def norm(url, dedupe):
    url = re.sub(r"^https?://(www\.)?", "", url.split("#")[0].rstrip("/"), flags=re.I).lower()
    found = re.search(dedupe["amazon_pattern"], url, re.I)
    return f"{found.group(1)}/dp/{found.group(2)}".lower() if found else url


def duplicate_keys(url, retailer, dedupe):
    """(비교 키, 정규화한 원래 주소, 비교 방식). 방식은 number(상품 번호)·tail(꼬리표 제거)·url 중 하나다."""
    raw = norm(url, dedupe)
    pattern = dedupe["product_number"].get(retailer)
    found = re.search(pattern, raw) if pattern else None
    if found:
        return f"number:{found.group(1)}", raw, "number"
    names = dedupe["drop_params"].get(retailer)
    return (norm(drop_params(url, names), dedupe), raw, "tail") if names else (raw, raw, "url")


def remove_duplicates(rows, dedupe):
    """제외되지 않은 행끼리 같은 국가·리테일러 안에서 실제 도착 주소가 같으면 앞 행만 남긴다. 대표 주소(canonical)는 쓰지 않는다."""
    first = {}
    for row in rows:
        if row["판정"] == EXCLUDE:
            continue
        key, raw, how = duplicate_keys(row["실제URL"] or row["URL"], row["리테일러"], dedupe)
        scope = (row["국가"], row["리테일러"], key)
        if scope in first:
            number, first_raw = first[scope]
            exclude(row, DUPLICATE_STAGE, dedupe["reasons"]["url" if raw == first_raw else how].format(first=number))
        else:
            first[scope] = (row["행번호"], raw)


def osm_codes(path):
    """OSM 후보 순서대로 (원본 주소, 브랜드, 제품코드). 제품코드는 MPC, 없으면 MODEL_DEDUP_KEY(D082)."""
    _, rows = read_csv(path)
    return [(row["RAW_URL"], row["BRAND"].strip().upper(), next((row[name].strip().upper() for name in ("MPC", "MODEL_DEDUP_KEY") if row[name] not in NULL_VALUES), "")) for row in rows]


def page_text_reader(run, pages):
    """검색 행의 저장 HTML을 읽는 함수. 그 주소를 받지 못했으면 None."""
    read_html = html_reader(run.sub("html"))

    def read(row):
        page = pages.get(row["URL"])
        return read_html(page) if page and page.get("html_file") else None

    return read


def search_codes(rows, read, config):
    return codes.extract([row for row in rows if row["흐름"] != OSM_FLOW], read, config)


def fill_codes(rows, osm, found):
    """브랜드·제품코드를 채운다. OSM 행은 후보 파일을 순서대로 맞추고, 검색 행은 리테일러별 추출 결과(found)를 행번호로 붙인다."""
    osm_rows = [row for row in rows if row["흐름"] == OSM_FLOW]
    if len(osm_rows) != len(osm):
        raise ConfigError(f"S2 결과의 OSM 행 수와 후보 파일이 다릅니다: {len(osm_rows)} != {len(osm)}")
    for row, (url, brand, code) in zip(osm_rows, osm):
        if row["원본URL"] != url:
            raise ConfigError(f"행번호 {row['행번호']}: OSM 후보 파일과 순서가 다릅니다")
        row["브랜드"], row["제품코드"] = brand, code
    for row in rows:
        if row["흐름"] != OSM_FLOW:
            brand, code = found[row["행번호"]][:2]
            row["브랜드"], row["제품코드"] = brand.strip().upper(), code.strip().upper()


def code_evidence(rows, found):
    """검색 행마다 브랜드·제품코드를 어디서 찾았는지."""
    return [{"행번호": row["행번호"], "국가": row["국가"], "리테일러": row["리테일러"], "URL": row["URL"], "상품명": row["상품명"], "브랜드": row["브랜드"], "제품코드": row["제품코드"],
             "브랜드 찾은곳": found[row["행번호"]][2], "제품코드 찾은곳": found[row["행번호"]][3]} for row in rows if row["흐름"] != OSM_FLOW]


def judge_all(rows, pages, sellers, settings):
    for row in rows:
        if row["판정"] != EXCLUDE:
            judge_row(row, pages.get(row["URL"]), sellers.get(row["URL"]), settings)
    remove_duplicates(rows, settings["dedupe"])
    return rows


def summarize(rows, stages):
    counts = {}
    for row in rows:
        counter = counts.setdefault((row["흐름"], row["국가"], row["리테일러"]), Counter())
        counter["전체"] += 1
        counter[row["제외단계"] if row["판정"] == EXCLUDE else row["판정"]] += 1
    names = ["전체", *stages, KEEP, CHECK]
    return ["흐름", "국가", "리테일러", *names], [{"흐름": flow, "국가": country, "리테일러": retailer, **{name: str(counter[name]) for name in names}} for (flow, country, retailer), counter in sorted(counts.items())]


def included_urls(rows, status_column, included, url_column):
    found = {}
    for row in rows:
        if row[status_column] in included:
            found.setdefault((row["국가"], row["리테일러"]), set()).add(row[url_column])
    return found


def compare_months(current, previous):
    """(국가, 리테일러)별 포함 URL 집합을 비교한 행 목록."""
    table = []
    for key in sorted(set(current) | set(previous)):
        now, before = current.get(key, set()), previous.get(key, set())
        table.append({"국가": key[0], "리테일러": key[1], "전월 포함": len(before), "이번 달 포함": len(now), "공통": len(now & before), "새로 포함": len(now - before), "빠짐": len(before - now)})
    return table


def render_compare(month, previous_name, table):
    lines = [f"# {month} 전월 대비", "", f"전월 파일: `{previous_name}`. 포함 행의 확인 요청 URL 집합을 비교했다. 내부용이며 EY에 보내지 않는다.", "",
             "| " + " | ".join(VS_COLUMNS) + " |", "| " + " | ".join("---" for _ in VS_COLUMNS) + " |"]
    lines += ["| " + " | ".join(str(item[column]) for column in VS_COLUMNS) + " |" for item in table]
    total = {column: sum(item[column] for item in table) for column in VS_COLUMNS[2:]}
    lines += ["| 합계 | | " + " | ".join(str(total[column]) for column in VS_COLUMNS[2:]) + " |"]
    return "\n".join(lines) + "\n"


def load_pages(path):
    with open(path, encoding="utf-8") as stream:
        return {record["url"]: record for record in map(json.loads, filter(str.strip, stream))}


def main(argv):
    parser = new_parser("S5 최종 판정: 페이지 상태·판매자·실제 주소 중복")
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"), help="파일명에 쓸 날짜(YYYYMMDD)")
    args = parser.parse_args(argv)
    run = RunPaths(args.month).create()
    logger = get_logger(run, "s5")
    spec = load_output_spec(run)
    judgments, final = run.sub("judgments"), run.sub("final")
    needed = [judgments / "step1.csv", judgments / "pages.jsonl", judgments / "sellers.csv", run.sub("candidates") / OSM_FILE]
    missing = [str(path) for path in needed if not path.exists()]
    if missing:
        raise ConfigError("S5 입력이 없습니다: " + ", ".join(missing))
    columns, rows = read_csv(needed[0])
    if tuple(columns) != spec.internal_columns:
        raise ConfigError("step1.csv의 열이 output.json과 다릅니다")
    internal, summary, compare = final / INTERNAL_NAME.format(rows=len(rows), date=args.date), final / "summary.csv", final / "vs_prev_month.md"
    if outputs_ready([internal, summary, compare], args.force):
        logger.info("출력이 이미 있어 건너뜁니다(다시 하려면 --force)")
        return 0
    pages = load_pages(needed[1])
    _, seller_rows = read_csv(needed[2])
    sellers = {row["요청URL"]: row for row in seller_rows}
    judge_all(rows, pages, sellers, load_config(run, "retailer_rules")["final"])
    found = search_codes(rows, page_text_reader(run, pages), load_config(run, "product_codes"))
    fill_codes(rows, osm_codes(needed[3]), found)
    write_csv(judgments / CODE_EVIDENCE_NAME, CODE_EVIDENCE_COLUMNS, code_evidence(rows, found), overwrite=True)
    write_csv(internal, list(spec.internal_columns), rows, overwrite=args.force)
    summary_columns, summary_rows = summarize(rows, spec.exclusion_stages)
    write_csv(summary, summary_columns, summary_rows, overwrite=args.force)
    previous_path = REPO_ROOT / load_config(run, "output")["previous_share"]
    if not previous_path.exists():
        raise ConfigError(f"전월 공유용 파일이 없습니다: {previous_path}")
    _, previous = read_csv(previous_path)
    current_urls = included_urls(rows, "판정", {status for status, shared in spec.share_status_map.items() if shared == PREVIOUS_INCLUDED}, "URL")
    table = compare_months(current_urls, included_urls(previous, "모수 포함 여부", {PREVIOUS_INCLUDED}, "확인 요청 URL"))
    compare.write_text(render_compare(args.month, previous_path.name, table), encoding="utf-8")
    logger.info("S5 끝: %d행, 판정 %s", len(rows), dict(Counter(row["판정"] for row in rows)))
    return 0
