"""S3 페이지 확인: S2를 통과한 주소를 Zyte로 열어 HTML을 저장하고 페이지 상태를 정한다.

순서: HTML 방식 → 차단·껍데기면 브라우저 방식(국가 지정). 설정상 브라우저 필수인 곳은 처음부터 브라우저 방식.
기본 실행은 호출 없이 건수·비용만 보여 준다(--run일 때만 호출). 규칙 값은 retailer_rules.json의 common.page_status·page_fetch에서 읽는다.
"""
import gzip
import json
import random
import re
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

from common import ConfigError, RunPaths, call_preview, get_logger, html_filename, load_config, new_parser, read_csv, read_secret, ResumeLog, write_csv
from s1b_search import now_text, page_html, zyte_post
from s2_filter import EXCLUDE

COMMAND = "uv run --python 3.12 --with-requirements pipeline/requirements.txt python pipeline/run.py s3 --month {month} --run"
LOG_NAME = "s3_pages_fetch.jsonl"
REPORT_NAME = "s3_pages_report.md"
PAGES_NAME = "pages.jsonl"
MANUAL_NAME = "pages_manual.csv"
MANUAL_LIST_NAME = "pages_manual_list.csv"
MANUAL_LIST_COLUMNS = ["요청URL", "국가", "리테일러", "상태", "방식", "문제"]
METHOD_HTML, METHOD_BROWSER, METHOD_MANUAL = "zyte_html", "zyte_browser", "manual"
NORMAL, BLOCKED, FAILED = "정상", "차단화면", "수집실패"


def geolocation_of(target, settings):
    """검색 리테일러는 지정된 값, OSM 리테일러는 콘솔 국가 코드를 Zyte 코드로 바꿔 쓴다."""
    if target.get("zyte_geolocation"):
        return target["zyte_geolocation"]
    code = target["console_country_codes"][0]
    return settings["geolocation_alias"].get(code, code)


def plan_pages(rows, targets, status_rules, fetch):
    """제외되지 않은 행의 주소를 중복 없이 모은다."""
    shops = {(target["country"], target["retailer"]): target for target in targets}
    planned, seen = [], set()
    for row in rows:
        if row["판정"] == EXCLUDE or row["URL"] in seen:
            continue
        seen.add(row["URL"])
        shop = (row["국가"], row["리테일러"])
        if shop not in shops:
            raise ConfigError(f"targets.json에 없는 리테일러입니다: {shop}")
        planned.append({"url": row["URL"], "country": row["국가"], "retailer": row["리테일러"], "geolocation": geolocation_of(shops[shop], fetch),
                        "browser_first": row["리테일러"] in status_rules["browser_required"]})
    return planned


def estimate_pages(planned, pricing):
    """(HTML 시작 수, 브라우저 시작 수, 재시도 없을 때 최저액·최고액, 브라우저 재시도 100건당 최저·최고 추가액)."""
    browser = sum(item["browser_first"] for item in planned)
    http = len(planned) - browser
    tiers = pricing["tiers"]
    low, high = tiers[min(tiers, key=int)], tiers[max(tiers, key=int)]
    amount = lambda tier: (http * tier["http"] + browser * tier["browser"]) / 1000
    return http, browser, amount(low), amount(high), low["browser"] / 10, high["browser"] / 10


def render_preview(month, planned, status_rules, fetch, pricing):
    http, browser, low, high, retry_low, retry_high = estimate_pages(planned, pricing)
    extended = sorted({item["geolocation"] for item in planned} - set(pricing["standard_geolocations"]))
    sends = [("url", "S2를 통과한 상품 상세 페이지 주소(중복 없이)"), ("httpResponseBody", "true → HTML만 받는 싼 방식(지역 지정 없음, 10월과 같음)"),
             ("browserHtml", "true → 브라우저로 여는 방식. 브라우저 필수인 곳이거나 HTML 방식이 차단·껍데기일 때만"), ("geolocation", "브라우저 방식일 때만 그 나라 코드"),
             ("보내지 않는 값", "리테일러 로그인 정보·개인정보 없음. Zyte 키는 인증 머리글로만 쓰고 파일·로그에 남기지 않음")]
    scale = (f"주소 {len(planned)}개(HTML 시작 {http}, 브라우저 시작 {browser}). 공개 단가 최소치 ${low:.2f}~${high:.2f}(사이트 묶음을 몰라 1~5묶음 범위). "
             f"HTML이 막혀 브라우저로 다시 여는 건 100건마다 ${retry_low:.2f}~${retry_high:.2f} 추가. 성공 응답만 과금. "
             f"확장 지역({', '.join(extended) or '없음'})의 추가 금액은 공개 문서에 없어 포함하지 못함")
    text = call_preview("Zyte (페이지 확인 S3)", "상품 페이지가 살아 있는지·품절인지와 판매자 판정에 쓸 HTML을 얻는다", sends, scale, [COMMAND.format(month=month)])
    groups = defaultdict(list)
    for item in planned:
        groups[(item["country"], item["retailer"])].append(item)
    lines = ["", "| 국가 | 리테일러 | 주소 수 | 방식 | 브라우저 지역 |", "| --- | --- | ---: | --- | --- |"]
    for (country, retailer), items in sorted(groups.items()):
        way = "브라우저만" if items[0]["browser_first"] else "HTML → 막히면 브라우저"
        lines.append(f"| {country} | {retailer} | {len(items)} | {way} | {items[0]['geolocation']} |")
    return text + "\n".join(lines) + "\n"


def title_of(html):
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    return re.sub(r"\s+", " ", match.group(1)).strip()[:200] if match else ""


def canonical_of(html):
    match = re.search(r"<link[^>]+rel=[\"']canonical[\"'][^>]*>", html, re.I)
    href = re.search(r"href=[\"']([^\"']+)", match.group(0)) if match else None
    return href.group(1) if href else ""


def _nodes(data):
    if isinstance(data, list):
        for item in data:
            yield from _nodes(item)
    elif isinstance(data, dict):
        yield data
        yield from _nodes(data.get("@graph") or [])


def category_path_of(html):
    """구조화 데이터(JSON-LD)의 BreadcrumbList 이름을 ' > '로 잇는다. 없으면 빈칸."""
    for match in re.finditer(r"<script[^>]*ld\+json[^>]*>(.*?)</script>", html, re.I | re.S):
        try:
            data = json.loads(match.group(1).strip())
        except ValueError:
            continue
        for node in _nodes(data):
            if node.get("@type") != "BreadcrumbList" or not isinstance(node.get("itemListElement"), list):
                continue
            names = []
            for element in node["itemListElement"]:
                item = element.get("item") if isinstance(element, dict) else None
                name = (element.get("name") if isinstance(element, dict) else "") or (item.get("name") if isinstance(item, dict) else "")
                if name:
                    names.append(str(name).strip())
            if names:
                return " > ".join(names)
    return ""


def marker_status(html, retailer, rules):
    """리테일러별 표시로 정상 페이지를 품절·판매중단으로 바꾼다. (상태 또는 None, 알릴 말)."""
    for marker in rules["retailer_markers"].get(retailer, []):
        if "text" in marker and marker["text"] in html:
            return marker["status"], ""
        if "json_regex" not in marker:
            continue
        match = re.search(marker["json_regex"], html, re.S)
        if not match:
            continue
        try:
            value = json.loads(match.group(1))
        except ValueError:
            return None, "상품 JSON을 읽지 못해 품절 여부를 확인하지 못함"
        for name in marker["path"]:
            value = value.get(name) if isinstance(value, dict) else None
        if value == marker["equals"]:
            return marker["status"], ""
    return None, ""


def judge_status(html, code, retailer, rules):
    """(상태, 알릴 말). 차단 > 없음·영구품절 > 리테일러 표시 > 정상 순서로 본다."""
    title = title_of(html)
    shell = rules["shell_patterns"].get(retailer)
    if shell and re.search(shell, html):
        return BLOCKED, ""
    limit = rules["block_max_size_by_retailer"].get(retailer, rules["block_max_size"])
    if len(html) < limit and (re.search(rules["block_pattern"], html, re.I) or not title):
        return BLOCKED, ""
    if code in rules["not_found_codes"]:
        if code == rules["permanent_code"] and title and re.search(rules["permanent_pattern"], html, re.I):
            return rules["permanent_status"], ""
        return f"없음({code})", ""
    if re.match(rules["not_found_title"], title.strip(), re.I):
        return "없음(제목)", ""
    status, note = marker_status(html, retailer, rules)
    return status or NORMAL, note


def fetch_mode(item, method, fetch, key, post=None, sleep=None):
    """한 방식으로 받는다. 일시 오류는 설정 횟수만큼 다시 시도한다. 끝내 안 되면 html=None."""
    post, sleep = post or zyte_post, sleep or time.sleep
    payload = {"url": item["url"], **fetch["methods"][method]}
    if method == METHOD_BROWSER:
        payload["geolocation"] = item["geolocation"]
    problem = ""
    for attempt in range(1, fetch["retries"] + 2):
        status, body = post(payload, key, fetch["api_url"], fetch["timeout_seconds"])
        html = page_html(body) if status == 200 else None
        if html is not None:
            return {"html": html, "final_url": body.get("url", item["url"]), "http_status": body.get("statusCode"), "attempts": attempt, "problem": ""}
        problem = f"API {status} {body.get('title') or ''}".strip()
        if status != 0 and status not in fetch["retry_codes"]:
            break
        if attempt <= fetch["retries"]:
            sleep(fetch["backoff_seconds"] * attempt ** 2)
    return {"html": None, "final_url": "", "http_status": None, "attempts": attempt, "problem": problem}


def check_url(item, rules, fetch, key, html_folder, post=None, sleep=None):
    """주소 하나를 확인해 기록 한 줄을 만든다. 차단이 아닌 결과가 나오면 바로 멈춰 돈을 아낀다."""
    methods = [METHOD_BROWSER] if item["browser_first"] else [METHOD_HTML, METHOD_BROWSER]
    tries, best = [], None
    for method in methods:
        got = fetch_mode(item, method, fetch, key, post, sleep)
        tries.append({"method": method, "attempts": got["attempts"], "problem": got["problem"], "http_status": got["http_status"]})
        if got["html"] is None:
            continue
        got["method"] = method
        got["status"], got["note"] = judge_status(got["html"], got["http_status"], item["retailer"], rules)
        best = got
        if got["status"] != BLOCKED:
            break
    base = {"url": item["url"], "country": item["country"], "retailer": item["retailer"], "tries": tries, "fetched_at": now_text()}
    if best is None:
        return {**base, "ok": False, "status": FAILED, "final_url": "", "title": "", "canonical": "", "html_file": "", "category_path": "", "method": "", "http_status": None, "note": "", "problem": tries[-1]["problem"]}
    name = html_filename(item["url"])
    (html_folder / name).write_bytes(gzip.compress(best["html"].encode("utf-8")))
    html = best["html"]
    return {**base, "ok": True, "status": best["status"], "final_url": best["final_url"], "title": title_of(html), "canonical": canonical_of(html), "html_file": name,
            "category_path": category_path_of(html), "method": best["method"], "http_status": best["http_status"], "note": best["note"], "problem": ""}


def run_checks(planned, rules, fetch, log, key, html_folder, logger, post=None, sleep=None):
    """곳별 동시 수를 제한하며 받는다. 끝난 주소는 다시 부르지 않는다."""
    todo = [item for item in planned if not log.done(item["url"])]
    random.Random(1).shuffle(todo)  # 한 곳이 앞에 몰려 작업 줄을 막지 않게 섞는다
    gates = {retailer: threading.Semaphore(fetch["workers_per_retailer"]) for retailer in {item["retailer"] for item in todo}}
    write_lock = threading.Lock()
    finished = [0]

    def work(item):
        with gates[item["retailer"]]:
            record = check_url(item, rules, fetch, key, html_folder, post, sleep)
        with write_lock:
            log.append(record)
            finished[0] += 1
            if finished[0] % fetch["log_every"] == 0 or finished[0] == len(todo):
                logger.info("%d/%d 끝", finished[0], len(todo))

    with ThreadPoolExecutor(max_workers=fetch["workers"]) as pool:
        list(pool.map(work, todo))


def apply_manual(pages, manual):
    """사람이 직접 연 결과로 덮어쓴다(리테일러 접속이 끝내 안 된 주소용)."""
    known = {page["url"]: page for page in pages}
    for entry in manual:
        if entry["요청URL"] not in known:
            raise ConfigError(f"{MANUAL_NAME}의 주소가 이번 대상에 없습니다: {entry['요청URL']}")
        known[entry["요청URL"]].update(status=entry["상태"], title=entry["제목"], final_url=entry["실제URL"] or entry["요청URL"], method=METHOD_MANUAL, html_file=entry.get("HTML파일", ""), ok=True, problem="")
    return pages


def build_pages(planned, log):
    """이어받기 기록에서 계획 순서대로 최종 기록을 만든다. 내부 시도 기록은 뺀다."""
    pages = []
    for item in planned:
        record = log.records.get(item["url"])
        if record is None:
            raise ConfigError(f"받지 못한 주소가 있습니다: {item['url']}")
        pages.append({name: value for name, value in record.items() if name != "tries"})
    return pages


def render_report(pages):
    by_shop = defaultdict(Counter)
    for page in pages:
        by_shop[(page["country"], page["retailer"])][page["status"]] += 1
    statuses = sorted({page["status"] for page in pages})
    lines = ["# S3 페이지 확인 결과", "", f"전체 {len(pages)}건: {dict(Counter(page['status'] for page in pages))}", f"수집 방식: {dict(Counter(page['method'] or '실패' for page in pages))}", "",
             "| 국가 | 리테일러 | " + " | ".join(statuses) + " |", "| --- | --- | " + " | ".join("---:" for _ in statuses) + " |"]
    for (country, retailer), counts in sorted(by_shop.items()):
        lines.append(f"| {country} | {retailer} | " + " | ".join(str(counts[status]) for status in statuses) + " |")
    noted = [page for page in pages if page.get("note")]
    if noted:
        lines += ["", f"확인이 필요한 페이지 {len(noted)}건: {dict(Counter(page['note'] for page in noted))}"]
    return "\n".join(lines) + "\n"


def write_outputs(run, pages):
    """pages.jsonl, 수동 확인 목록, 보고서를 쓴다. 수동으로 볼 주소 목록(행)을 돌려준다."""
    judgments = run.sub("judgments")
    with (judgments / PAGES_NAME).open("w", encoding="utf-8") as stream:
        for page in pages:
            stream.write(json.dumps(page, ensure_ascii=False) + "\n")
    pending = [{"요청URL": page["url"], "국가": page["country"], "리테일러": page["retailer"], "상태": page["status"], "방식": page["method"], "문제": page["problem"]}
               for page in pages if page["status"] in (BLOCKED, FAILED) and page["method"] != METHOD_MANUAL]
    write_csv(judgments / MANUAL_LIST_NAME, MANUAL_LIST_COLUMNS, pending, overwrite=True)
    (run.sub("logs") / REPORT_NAME).write_text(render_report(pages), encoding="utf-8")
    return pending


def main(argv):
    args = new_parser("S3 페이지 확인", paid=True).parse_args(argv)
    run = RunPaths(args.month).create()
    logger = get_logger(run, "s3")
    step1 = run.sub("judgments") / "step1.csv"
    if not step1.exists():
        raise ConfigError(f"S3 입력이 없습니다: {step1}")
    common_rules = load_config(run, "retailer_rules")["common"]
    rules, fetch = common_rules["page_status"], common_rules["page_fetch"]
    planned = plan_pages(read_csv(step1)[1], load_config(run, "targets")["targets"], rules, fetch)
    preview = render_preview(args.month, planned, rules, fetch, load_config(run, "zyte_pricing"))
    if not args.live:
        print(preview)
        return 0
    log = ResumeLog(run.sub("logs") / LOG_NAME, "url")
    run_checks(planned, rules, fetch, log, read_secret("ZYTE_API_KEY"), run.sub("html"), logger)
    pages = build_pages(planned, log)
    manual_path = run.sub("judgments") / MANUAL_NAME
    if manual_path.exists():
        pages = apply_manual(pages, read_csv(manual_path)[1])
    pending = write_outputs(run, pages)
    logger.info("S3 끝: %d건, 상태 %s, 수동 확인 필요 %d건", len(pages), dict(Counter(page["status"] for page in pages)), len(pending))
    for row in pending:
        logger.warning("수동 확인 필요: %s %s %s — %s", row["국가"], row["리테일러"], row["요청URL"], row["문제"] or row["상태"])
    return 1 if pending else 0
