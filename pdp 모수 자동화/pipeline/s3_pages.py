"""S3 페이지 확인: S2를 통과한 주소를 Zyte로 열어 HTML을 저장하고 페이지 상태를 정한다.

순서: HTML 방식 → 차단·껍데기면 브라우저 방식(국가 지정). 설정상 브라우저 필수인 곳은 처음부터 브라우저 방식.
꼬리를 뗀 일반 주소로 여는 곳(osm_query.json crawl_url_rules의 fallback_to_raw, D158)은 일반 주소가 페이지 없음(없음…)일 때만 그 일반 주소로 묶인
원래 꼬리 주소를 모두 하나씩 다시 열어 따로 기록한다. 일반 주소 기록은 페이지 없음 그대로 둔다. 어느 행이 어느 기록으로 판정되는지는 S5가 정한다.
기본 실행은 호출 없이 건수·비용만 보여 준다(--run일 때만 호출). 규칙 값은 retailer_rules.json의 common.page_status·page_fetch에서 읽는다.
"""
import gzip
import json
from html import unescape
import random
import re
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

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
MISSING_PREFIX = "없음"  # 페이지 없음 상태: 없음(404), 없음(제목) 등. 이때만 꼬리 주소로 다시 연다(D158)


def geolocation_of(target, settings):
    """검색 리테일러는 지정된 값, OSM 리테일러는 콘솔 국가 코드를 Zyte 코드로 바꿔 쓴다."""
    if target.get("zyte_geolocation"):
        return target["zyte_geolocation"]
    code = target["console_country_codes"][0]
    return settings["geolocation_alias"].get(code, code)


def fallback_shops(osm_query):
    """일반 주소가 페이지 없음일 때 원래 꼬리 주소로 다시 열 (국가, 리테일러). osm_query.json crawl_url_rules의 fallback_to_raw(D158)."""
    return {(rule["country"], rule["retailer"]) for rule in osm_query["candidates"]["crawl_url_rules"] if rule.get("fallback_to_raw")}


def plan_pages(rows, targets, status_rules, fetch, fallbacks=frozenset()):
    """제외되지 않은 행의 주소를 중복 없이 모은다. fallbacks에 든 곳은 같은 주소 행들의 원본URL 가운데 주소와 다른 것(꼬리 주소)을 모두, 중복 없이 행 순서대로 붙인다."""
    shops = {(target["country"], target["retailer"]): target for target in targets}
    planned, by_url = [], {}
    for row in rows:
        if row["판정"] == EXCLUDE:
            continue
        shop = (row["국가"], row["리테일러"])
        if row["URL"] not in by_url:
            if shop not in shops:
                raise ConfigError(f"targets.json에 없는 리테일러입니다: {shop}")
            by_url[row["URL"]] = {"url": row["URL"], "country": row["국가"], "retailer": row["리테일러"], "geolocation": geolocation_of(shops[shop], fetch),
                                  "browser_first": row["리테일러"] in status_rules["browser_required"]}
            planned.append(by_url[row["URL"]])
        entry, raw = by_url[row["URL"]], row.get("원본URL") or ""
        if shop in fallbacks and raw and raw != row["URL"] and raw not in entry.setdefault("fallback_urls", []):
            entry["fallback_urls"].append(raw)
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
    reopen = sum(len(item.get("fallback_urls", [])) for item in planned)
    extended = sorted({item["geolocation"] for item in planned} - set(pricing["standard_geolocations"]))
    sends = [("url", "S2를 통과한 상품 상세 페이지 주소(중복 없이)"), ("httpResponseBody", "true → HTML만 받는 싼 방식"),
             ("browserHtml", "true → 브라우저로 여는 방식. 브라우저 필수인 곳이거나 HTML 방식이 차단·껍데기일 때만"),
             ("다시 여는 url", f"꼬리를 뗀 일반 주소가 페이지 없음(없음…)일 때만 그 주소로 묶인 원래 꼬리 주소(원본URL)를 모두 한 번씩 더 엶. 대상 꼬리 주소 {reopen}개(D158)"), ("geolocation", "두 방식 모두 리테일러 나라 코드(2026-11-23부터. 그전 HTML 방식은 지정 없음)"),
             ("보내지 않는 값", "리테일러 로그인 정보·개인정보 없음. Zyte 키는 인증 머리글로만 쓰고 파일·로그에 남기지 않음")]
    scale = (f"주소 {len(planned)}개(HTML 시작 {http}, 브라우저 시작 {browser}). 공개 단가 최소치 ${low:.2f}~${high:.2f}(사이트 묶음을 몰라 1~5묶음 범위). "
             f"HTML이 막혀 브라우저로 다시 여는 건 100건마다 ${retry_low:.2f}~${retry_high:.2f} 추가. "
             f"일반 주소가 페이지 없음이라 꼬리 주소로 다시 여는 건 최대 {reopen}건 추가(건수는 열어 봐야 앎). 성공 응답만 과금. "
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
    """구조화 데이터(JSON-LD)의 BreadcrumbList 이름을 ' > '로 잇는다. 그 경로가 한 칸 이하이고 화면의 분류 경로(class="breadcrumbs" 목록)가
    더 길면 화면 경로를 쓴다(11-18 Electroplanet: JSON-LD에는 상품명 한 칸만, 화면에는 Accueil > Gros electroménager > Machine à laver). 없으면 빈칸."""
    structured = structured_path_of(html)
    if structured.count(" > ") >= 1:
        return structured
    visible = visible_path_of(html)
    return visible if visible.count(" > ") > structured.count(" > ") else structured


def visible_path_of(html):
    match = re.search(r'<(ul|ol|div|nav)[^>]*class="[^"]*\bbreadcrumbs?\b[^"]*"[^>]*>(.*?)</\1>', html, re.I | re.S)
    if not match:
        return ""
    names = [re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", item))).strip() for item in re.findall(r"<li[^>]*>(.*?)</li>", match.group(2), re.I | re.S)]
    names = [name.strip(" ›>/|»").strip() for name in names]  # 화면 경로의 구분 기호(›, /)는 이름이 아니다
    return " > ".join(name for name in names if name)


def structured_path_of(html):
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
    # 2026-11-23 사용자 결정: HTML 방식도 브라우저 방식처럼 리테일러 나라에서 접속한다(10월~11월 연습 회차는 HTML 방식에 나라 지정 없음).
    payload = {"url": item["url"], **fetch["methods"][method], "geolocation": item["geolocation"]}
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


def check_url(item, rules, fetch, key, html_folder, post=None, sleep=None, fallback_from_status=""):
    """주소 하나를 확인해 기록 한 줄을 만든다. 차단이 아닌 결과가 나오면 바로 멈춰 돈을 아낀다.
    꼬리 주소를 다시 여는 경우(D158) fallback_from_status에 일반 주소 상태를 받아, 기록의 fallback_url(이 꼬리 주소)과 fallback_from_status에 남긴다."""
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
    base = {"url": item["url"], "country": item["country"], "retailer": item["retailer"], "geolocation": item["geolocation"], "tries": tries, "fetched_at": now_text()}
    if fallback_from_status:
        base.update(fallback_url=item["url"], fallback_from_status=fallback_from_status)
    if best is None:
        return {**base, "ok": False, "status": FAILED, "final_url": "", "title": "", "canonical": "", "html_file": "", "category_path": "", "method": "", "http_status": None, "note": "", "problem": tries[-1]["problem"]}
    name = html_filename(item["url"])
    (html_folder / name).write_bytes(gzip.compress(best["html"].encode("utf-8")))
    html = best["html"]
    return {**base, "ok": True, "status": best["status"], "final_url": best["final_url"], "title": title_of(html), "canonical": canonical_of(html), "html_file": name,
            "category_path": category_path_of(html), "method": best["method"], "http_status": best["http_status"], "note": best["note"], "problem": ""}


def is_missing(record):
    return bool(record) and record.get("ok", True) and record["status"].startswith(MISSING_PREFIX)


def tails_to_open(item, plain):
    """일반 주소 기록이 페이지 없음일 때만 다시 열 꼬리 주소 목록. 외부 판매자, 차단, 품절이면 열지 않는다(06 문서 2-7a: 일반 주소 기준)."""
    return item.get("fallback_urls", []) if is_missing(plain) else []


def check_item(item, rules, fetch, key, html_folder, done=None, post=None, sleep=None):
    """계획 한 건을 확인해 새로 만든 기록들을 돌려준다. done(이미 끝난 기록)에 있는 주소는 다시 부르지 않는다.
    일반 주소가 페이지 없음이면 꼬리 주소를 모두 하나씩 열어 각자 기록한다(D158). 꼬리 주소가 차단이나 수집실패여도 그대로 남겨 사람 확인 목록으로 보낸다."""
    done = done or {}
    plain = done.get(item["url"]) or check_url(item, rules, fetch, key, html_folder, post, sleep)
    records = [] if item["url"] in done else [plain]
    for tail in tails_to_open(item, plain):
        if tail not in done:
            records.append(check_url({**item, "url": tail}, rules, fetch, key, html_folder, post, sleep, fallback_from_status=plain["status"]))
    return records


def run_checks(planned, rules, fetch, log, key, html_folder, logger, post=None, sleep=None):
    """곳별 동시 수를 제한하며 받는다. 끝난 주소는 다시 부르지 않는다."""
    finished_records = lambda item: {url: log.records[url] for url in [item["url"], *item.get("fallback_urls", [])] if log.done(url)}
    todo = [item for item in planned if not log.done(item["url"]) or any(not log.done(tail) for tail in tails_to_open(item, log.records[item["url"]]))]
    random.Random(1).shuffle(todo)
    # 곳별 줄을 따로 두고, 그 곳의 동시 수에 자리가 있을 때만 작업자에게 넘긴다. 섞은 한 줄을 그대로 넘기면 차단돼 느린 곳(11-18 Magalu)의
    # 자리를 기다리는 작업자가 쌓여 전체가 그 곳 속도로 떨어졌다.
    queues = defaultdict(list)
    for item in todo:
        queues[item["retailer"]].append(item)
    running = Counter()
    write_lock = threading.Lock()
    finished = 0

    def work(item):
        records = check_item(item, rules, fetch, key, html_folder, finished_records(item), post, sleep)
        with write_lock:
            for record in records:
                log.append(record)
        return item

    with ThreadPoolExecutor(max_workers=fetch["workers"]) as pool:
        pending = set()
        while pending or any(queues.values()):
            while len(pending) < fetch["workers"]:
                ready = [name for name in queues if queues[name] and running[name] < fetch["workers_per_retailer"]]
                if not ready:
                    break
                retailer = min(ready, key=lambda name: running[name])  # 지금 덜 돌고 있는 곳부터. 앞 곳이 자리를 독차지하지 않게(11-18)
                pending.add(pool.submit(work, queues[retailer].pop()))
                running[retailer] += 1
            done, pending = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                running[future.result()["retailer"]] -= 1
                finished += 1
                if finished % fetch["log_every"] == 0 or finished == len(todo):
                    logger.info("%d/%d 끝", finished, len(todo))


def apply_manual(pages, manual):
    """사람이 직접 연 결과로 덮어쓴다(리테일러 접속이 끝내 안 된 주소용)."""
    known = {page["url"]: page for page in pages}
    for entry in manual:
        if entry["요청URL"] not in known:
            raise ConfigError(f"{MANUAL_NAME}의 주소가 이번 대상에 없습니다: {entry['요청URL']}")
        known[entry["요청URL"]].update(status=entry["상태"], title=entry["제목"], final_url=entry["실제URL"] or entry["요청URL"], method=METHOD_MANUAL, html_file=entry.get("HTML파일", ""), ok=True, problem="")
    return pages


def build_pages(planned, log):
    """이어받기 기록에서 계획 순서대로 최종 기록을 만든다. 다시 연 꼬리 주소 기록은 그 일반 주소 기록 바로 뒤에 둔다. 내부 시도 기록은 뺀다."""
    pages = []
    for item in planned:
        plain = log.records.get(item["url"])
        for url in [item["url"], *tails_to_open(item, plain)]:
            record = log.records.get(url)
            if record is None:
                raise ConfigError(f"받지 못한 주소가 있습니다: {url}")
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
    reopened = [page for page in pages if page.get("fallback_from_status")]
    if reopened:
        lines += ["", f"일반 주소가 페이지 없음이라 원래 꼬리 주소로 다시 연 페이지 {len(reopened)}건(D158). 위 표에도 들어 있다. 다시 연 뒤 상태: {dict(Counter(page['status'] for page in reopened))}", "",
                  "| 국가 | 리테일러 | 다시 연 꼬리 주소 | 일반 주소 상태 | 다시 연 뒤 상태 |", "| --- | --- | --- | --- | --- |"]
        lines += [f"| {page['country']} | {page['retailer']} | {page['fallback_url']} | {page['fallback_from_status']} | {page['status']} |" for page in reopened]
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
    planned = plan_pages(read_csv(step1)[1], load_config(run, "targets")["targets"], rules, fetch, fallback_shops(load_config(run, "osm_query")))
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
