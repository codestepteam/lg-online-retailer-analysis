"""S4 판매자 판정: 저장된 상품 페이지에서 본 상품의 판매자를 읽는다. 외부 호출 없음.

어느 리테일러가 어느 함수를 쓰는지는 retailer_rules.json의 sellers.functions가 정한다. 사람이 확인한 값은 sellers_manual.csv가 덮어쓴다.
"""
import gzip
import json
import re
from collections import Counter

from common import ConfigError, RunPaths, get_logger, load_config, new_parser, outputs_ready, read_csv, write_csv
from rules.sellers import CONTEXT_FUNCTIONS, FUNCTIONS
from rules.sellers.base import DIRECT, REFURB, main_heading

COLUMNS = ["요청URL", "국가", "리테일러", "판매자", "판매자구분", "근거"]
NORMAL_PAGE = "정상"
SELLER_PAGES = (NORMAL_PAGE, "품절", "판매중단")  # D108: 판매자(③)를 품절·판매중단(④)보다 먼저 본다
KINDS = {DIRECT, REFURB, "외부판매자", "브랜드공식점", "확인불가"}


def load_rules(run):
    rules = dict(load_config(run, "retailer_rules")["sellers"])
    rules["lazada_items"] = load_config(run, "lazada_sellers")["sellers"]
    unknown = set(rules["functions"].values()) - set(FUNCTIONS) - set(CONTEXT_FUNCTIONS)
    if unknown:
        raise ConfigError(f"설정에 있는 판매자 함수가 코드에 없습니다: {sorted(unknown)}")
    return rules


def apply_title_rule(item, html, rules, result):
    """설정에 적힌 리테일러의 본 상품 제목에 리퍼 단어가 있으면 판매자와 무관하게 리퍼·중고로 본다."""
    for rule in rules["title_refurb"]:
        if (rule["country"], rule["retailer"]) != (item["country"], item["retailer"]):
            continue
        title = main_heading(html)[0] or item["title"]
        hit = re.search(rule["pattern"], title, re.I)
        if hit:
            return result[0], REFURB, f"본 상품 제목 리퍼 표현: {hit.group()}; {result[2]}"
    return result


def judge_page(item, html, rules, context):
    name = rules["functions"].get(f"{item['country']}|{item['retailer']}")
    if name is None:
        return rules["names"].get(item["retailer"], item["retailer"]), DIRECT, rules["no_function_evidence"]
    if name in CONTEXT_FUNCTIONS:
        result = CONTEXT_FUNCTIONS[name][0](item, html, rules, context)
    else:
        result = FUNCTIONS[name](item, html, rules)
    result = apply_title_rule(item, html, rules, result)
    if result[1] not in KINDS:
        raise ConfigError(f"판매자구분 값이 약속과 다릅니다: {result[1]}")
    return result


def judge_all(items, read_html, rules):
    """(결과 행, 페이지를 못 읽은 URL). 다른 페이지 값이 필요한 함수는 판정 전에 해당 리테일러 페이지를 한 번 훑는다."""
    context = {}
    for item in items:
        name = rules["functions"].get(f"{item['country']}|{item['retailer']}")
        if name in CONTEXT_FUNCTIONS:
            html = read_html(item)
            if html is not None:
                CONTEXT_FUNCTIONS[name][1](item, html, rules, context)
    rows, unread = [], []
    for item in items:
        html = read_html(item)
        if html is None:
            unread.append(item["url"])
            result = ("", "확인불가", "저장된 HTML 파일 없음")
        else:
            result = judge_page(item, html, rules, context)
        rows.append(dict(zip(COLUMNS, (item["url"], item["country"], item["retailer"], result[0] or "", result[1], result[2]))))
    return rows, unread


def apply_manual(rows, manual):
    """사람이 확인한 표로 같은 URL 행을 덮어쓴다. 없는 URL이나 약속 밖의 구분 값은 멈춘다."""
    by_url = {row["요청URL"]: row for row in rows}
    for entry in manual:
        if entry["요청URL"] not in by_url:
            raise ConfigError(f"수동 보완표의 URL이 S3 결과에 없습니다: {entry['요청URL']}")
        if entry["판매자구분"] not in KINDS:
            raise ConfigError(f"수동 보완표의 판매자구분이 약속과 다릅니다: {entry['판매자구분']}")
        by_url[entry["요청URL"]].update({"판매자": entry["판매자"], "판매자구분": entry["판매자구분"], "근거": entry["근거"]})
    return rows


def html_reader(folder):
    def read(item):
        path = folder / item["html_file"]
        if not item["html_file"] or not path.exists():
            return None
        if path.suffix == ".gz":
            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as stream:
                return stream.read()
        return path.read_text(encoding="utf-8", errors="replace")
    return read


def load_items(path):
    if not path.exists():
        raise ConfigError(f"S4 입력이 없습니다: {path}")
    with path.open(encoding="utf-8") as stream:
        records = [json.loads(line) for line in stream if line.strip()]
    return [record for record in records if record["status"] in SELLER_PAGES]


def main(argv):
    args = new_parser("S4 판매자 판정: 저장 HTML에서 본 상품 판매자를 읽는다").parse_args(argv)
    run = RunPaths(args.month).create()
    logger = get_logger(run, "s4")
    folder = run.sub("judgments")
    output, manual_path = folder / "sellers.csv", folder / "sellers_manual.csv"
    if outputs_ready([output], args.force):
        logger.info("출력이 이미 있어 건너뜁니다(다시 하려면 --force)")
        return 0
    rules = load_rules(run)
    rows, unread = judge_all(load_items(folder / "pages.jsonl"), html_reader(run.sub("html")), rules)
    if manual_path.exists():
        rows = apply_manual(rows, read_csv(manual_path)[1])
    write_csv(output, COLUMNS, rows, overwrite=args.force)
    logger.info("S4 끝: %d행, 구분 %s, HTML 없음 %d건", len(rows), dict(Counter(row["판매자구분"] for row in rows)), len(unread))
    return 0
