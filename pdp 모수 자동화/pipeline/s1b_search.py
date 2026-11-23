"""S1b 검색 후보 수집(OSM에 없는 12곳).

세 가지 실행이 있다. 모두 --dry-run이 기본이고 --run을 줘야 Zyte를 부른다.
- 인자 없음: 본 수집. candidates/search_cards.csv(14열), search_reconcile.csv(27열)를 만든다.
- --retailer '국가|리테일러': 본 수집을 한 곳만 한다. 두 후보 파일에서 그 곳 행만 새로 바꾸고 다른 곳 행은 둔다(2026-11-23 사용자 요청).
- --sample: 시험 수집. 곳마다 검색어 1개 × 앞 2페이지만 받아 10월과 비교한다. 후보 파일은 만들지 않는다.
- --probe: WP1-1 방식 실험(12곳 × 3방식 × 1페이지, 재시도 없음).
"""
import base64
import hashlib
import json
import math
import re
import threading
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import parse_qs, parse_qsl, quote, quote_plus, urlencode, urljoin, urlparse, urlsplit, urlunsplit

from bs4 import BeautifulSoup

from common import REPO_ROOT, ConfigError, ResumeLog, RunPaths, call_preview, get_logger, load_config, new_parser, outputs_ready, read_csv, read_secret, write_csv

ENCODERS = {"percent": lambda text: quote(text, safe=""), "plus": quote_plus, "lower_plus": lambda text: quote_plus(text.lower())}
HTML_FIELDS = ("httpResponseBody", "browserHtml")
REPORT_NAME, RECORD_NAME, HTML_FOLDER = "zyte_search_probe.md", "zyte_search_probe.jsonl", "search_probe"
COMMAND = "uv run --python 3.12 --with-requirements pipeline/requirements.txt python pipeline/run.py s1b --month {month} --probe --run"
COLLECT_COMMAND = "uv run --python 3.12 --with-requirements pipeline/requirements.txt python pipeline/run.py s1b --month {month}{flag} --run"
PAGES_NAME, SAMPLE_PAGES_NAME, SAMPLE_REPORT = "search_pages.jsonl", "search_sample_pages.jsonl", "search_sample.md"
CARDS_NAME, RECONCILE_NAME = "search_cards.csv", "search_reconcile.csv"
CARD_COLUMNS = ("엑셀행번호", "국가", "리테일러", "F열제품군", "J열검색어", "최종검색결과URL", "페이지번호", "카드순번", "상품명", "카드PDP링크", "광고여부", "표시된전체수", "수집시각", "접속국가")
RECONCILE_COLUMNS = ("엑셀행번호", "국가", "리테일러", "F열제품군", "J열검색어", "최초표시전체수", "최종표시전체수", "페이지별표시수변화", "상한", "최종저장카드수", "광고카드수", "광고표시없음카드수", "수집원본카드수",
                     "확인페이지수", "최종출력마지막페이지", "완료구분", "대조결과", "최종검색결과URL", "접속국가", "접속근거", "비고", "근거", "재시도확인시각", "재시도접속근거", "재시도확인주소", "재시도범위", "재시도시_개별검색어제출")
MANUAL = "manual"


def start_url(retailer, keyword):
    encoding = retailer["query_encoding"]
    if encoding not in ENCODERS:
        raise ConfigError(f"모르는 검색어 인코딩입니다: {encoding}")
    url = retailer["start_url_template"].replace("{" + encoding + "}", ENCODERS[encoding](keyword))
    return apply_query_filters(url, retailer)


def query_filters_match(url, retailer):
    query = parse_qs(urlsplit(url).query, keep_blank_values=True)
    return all(query.get(name) == [value] for name, value in retailer.get("required_query_params", {}).items())


def apply_query_filters(url, retailer):
    """설정된 필수 검색 조건만 보강한다. 상품 카드의 PDP URL에는 적용하지 않는다."""
    required = retailer.get("required_query_params", {})
    if not required or query_filters_match(url, retailer):
        return url
    parts = urlsplit(url)
    pairs = [(name, value) for name, value in parse_qsl(parts.query, keep_blank_values=True) if name not in required]
    return urlunsplit(parts._replace(query=urlencode(pairs + list(required.items()), quote_via=quote)))


def request_cache_key(base, retailer, start):
    """필수 검색 조건을 쓰는 곳은 이전 무필터 기록과 이어받기 키를 분리한다."""
    if not retailer.get("required_query_params"):
        return base
    return base + "|" + hashlib.sha256(start.encode()).hexdigest()[:16]


def validate_existing_cards(path, settings):
    """과거 무필터 후보 CSV를 완료된 새 수집으로 건너뛰지 않는다. 원본은 보존한다."""
    _, rows = read_csv(path)
    for row in rows:
        retailer = settings["retailers"].get(f"{row['국가']}|{row['리테일러']}", {})
        if not query_filters_match(row["최종검색결과URL"], retailer):
            raise ConfigError("기존 검색 후보에 필수 직판 조건이 없습니다. 기존 파일을 보존하고 새 회차 또는 승인된 --force 재수집을 사용하세요.")


def october_samples(probe):
    """10월 기록: 엑셀행번호별 표시 전체 수·저장 카드 수와 1페이지 카드 링크."""
    _, reconcile = read_csv(REPO_ROOT / probe["october_reconcile"])
    _, cards = read_csv(REPO_ROOT / probe["october_cards"])
    links = {}
    for card in cards:
        if card["페이지번호"] == "1":
            links.setdefault(card["엑셀행번호"], []).append(card["카드PDP링크"])
    return {row["엑셀행번호"]: {"total": row["최종표시전체수"], "cards": int(row["최종저장카드수"] or 0), "links": links.get(row["엑셀행번호"], [])} for row in reconcile}


def payload_for(url, geolocation, mode):
    return {"url": url, "geolocation": geolocation, **mode}


def plan_requests(terms, settings):
    """리테일러마다 10월에 카드가 있었던 첫 검색어를 골라 방식별 요청 목록을 만든다."""
    probe = settings["probe"]
    samples = october_samples(probe)
    planned = []
    for retailer in settings["retailers"].values():
        candidates = [term for term in terms if (term["country"], term["retailer"]) == (retailer["country"], retailer["retailer"])
                      and samples.get(str(term["excel_row"]), {}).get("cards", 0) > 0 and samples[str(term["excel_row"])]["links"]]
        if not candidates:
            raise ConfigError(f"실험할 검색어가 없습니다: {retailer['country']} {retailer['retailer']}")
        term = min(candidates, key=lambda item: item["excel_row"])
        sample = samples[str(term["excel_row"])]
        url = start_url(retailer, term["keyword"])
        for name, mode in probe["modes"].items():
            cache_key = request_cache_key(re.sub(r"\W+", "_", f"{retailer['country']}_{retailer['retailer']}_{name}"), retailer, url)
            planned.append({"key": cache_key, "country": retailer["country"], "retailer": retailer["retailer"], "mode": name,
                            "excel_row": term["excel_row"], "keyword": term["keyword"], "english": term["english"], "geolocation_group": retailer["zyte_geolocation_group"],
                            "october_total": sample["total"], "october_first_page_cards": len(sample["links"]), "october_links": sample["links"],
                            "payload": payload_for(url, retailer["zyte_geolocation"], mode)})
    if len(planned) > probe["max_requests"]:
        raise ConfigError(f"실험 요청이 승인 상한을 넘습니다: {len(planned)} > {probe['max_requests']}")
    return planned


def estimate(planned, pricing):
    """종량제 공개 단가 기준 (HTML 요청 수, 브라우저 요청 수, 최저액, 최고액). 사이트 묶음을 몰라 1묶음~5묶음 범위로 낸다."""
    http = sum("httpResponseBody" in item["payload"] for item in planned)
    browser = len(planned) - http
    tiers = pricing["tiers"]
    low, high = tiers[min(tiers, key=int)], tiers[max(tiers, key=int)]
    amount = lambda tier: (http * tier["http"] + browser * tier["browser"]) / 1000
    return http, browser, amount(low), amount(high)


def render_preview(month, planned, settings, pricing):
    http, browser, low, high = estimate(planned, pricing)
    modes = "; ".join(f"{name} = {json.dumps(mode, ensure_ascii=False)}" for name, mode in settings["probe"]["modes"].items())
    extended = sum(item["geolocation_group"] == "extended" for item in planned)
    actions = sum("actions" in item["payload"] for item in planned)
    sends = [("주소(url)", "12곳의 검색 결과 1페이지. 아래 표 전체"), ("지역(geolocation)", "리테일러 국가 코드. 아래 표 전체"), ("방식", modes),
             ("인증", "`.env`의 Zyte 키를 인증 머리글로만 보냄. 파일·로그에는 안 남김")]
    scale = (f"최대 {len(planned)}요청(HTML {http}, 브라우저 {browser}), 재시도 없음. 공개 단가로 약 ${low:.3f} ~ ${high:.3f}. 묶음은 사이트별로 정해져 모름. "
             f"확장 지역 {extended}요청·브라우저 동작 {actions}요청의 추가 금액은 공개 문서에 없어 이 금액은 최소치. 성공 응답만 과금")
    text = call_preview("Zyte (검색 수집 실험, WP1-1)", "OSM에 없는 12곳을 사람 손 없이 수집할 수 있는지, 곳별로 어느 방식이 되는지 확인한다", sends, scale, [COMMAND.format(month=month)])
    rows = ["", "| 국가 | 리테일러 | 엑셀행 | 검색어 | 영어 뜻 | 지역 | 10월 1페이지 카드 | 10월 표시 전체 수 | 주소 |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for item in planned[::len(settings["probe"]["modes"])]:
        rows.append(f"| {item['country']} | {item['retailer']} | {item['excel_row']} | {item['keyword']} | {item['english']} | {item['payload']['geolocation']} | {item['october_first_page_cards']} | {item['october_total']} | {item['payload']['url']} |")
    return text + "\n".join(rows) + "\n"


def zyte_post(payload, key, api_url, timeout):
    """(HTTP 상태, 응답 JSON)을 돌려준다. 실패도 예외 없이 돌려줘 표에 남긴다."""
    token = base64.b64encode(f"{key}:".encode()).decode()
    request = urllib.request.Request(api_url, data=json.dumps(payload).encode(), headers={"Authorization": f"Basic {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        try:
            return error.code, json.loads(error.read())
        except ValueError:
            return error.code, {}
    except (urllib.error.URLError, TimeoutError) as error:
        return 0, {"title": type(error).__name__}


def page_html(body):
    if "browserHtml" in body:
        return body["browserHtml"]
    if "httpResponseBody" in body:
        return base64.b64decode(body["httpResponseBody"]).decode("utf-8", "replace")
    return None


def tidy(text):
    return " ".join(text.split())


def text_of(element):
    return tidy(element.get_text(" "))


def card_name(card, parser):
    for selector in parser["name"]:
        found = card.select_one(selector)
        if found and text_of(found):
            return text_of(found), found
    return tidy(card.get(parser.get("name_attr", ""), "") or ""), None


def card_link(card, name_element, parser, base_url):
    for rule in parser["link"]:
        if rule == "self":
            href = card.get("href")
        elif isinstance(rule, dict):
            parent = name_element.find_parent(rule["parent_of_name"]) if name_element else None
            href = parent.get("href") if parent else None
        else:
            found = card.select_one(rule)
            href = found.get("href") if found else None
        if href:
            return urljoin(base_url, href)
    return ""


def card_ad(card, rule):
    """10월과 같은 세 값: 예 / 아니오(사이트가 광고 아님을 밝힘) / 표시 없음."""
    if "attr" in rule:
        return {rule["yes"]: "예", rule["no"]: "아니오"}.get(card.get(rule["attr"]), "표시 없음")
    return "예" if re.search(rule["text"], text_of(card), re.I) else "표시 없음"


def read_total(soup, rules):
    """(화면에 적힌 전체 수 글자, 숫자). 1000+처럼 정확한 수가 아니면 숫자는 None."""
    for rule in rules:
        for element in soup.select(rule["css"]):
            match = re.search(rule["regex"], text_of(element.parent if rule.get("parent") else element))
            if match and re.search(r"\d", match.group(1)):
                display = match.group(1).strip()
                return display, None if "+" in display else int(re.sub(r"\D", "", display))
    return "", None


def has_next(soup, rule, page):
    next_page = str(page + 1)
    text = rule.get("text", "").replace("{next}", next_page)
    for element in soup.select(rule["css"].replace("{next}", next_page)):
        if not text or re.fullmatch(text, text_of(element)):
            return True
    return False


def parse_page(html, parser, base_url, page):
    """받은 HTML 한 장에서 본 목록 카드·전체 수·다음 페이지 여부를 읽는다. 추천 구역은 선택자로 뺀다."""
    soup = BeautifulSoup(html, "lxml")
    cards = []
    for card in soup.select(parser["cards"]):
        name, name_element = card_name(card, parser)
        cards.append({"name": name, "link": card_link(card, name_element, parser, base_url), "ad": card_ad(card, parser["ad"])})
    display, total = read_total(soup, parser["total"])
    zero = parser.get("zero")
    is_zero = bool(zero) and not cards and any(re.search(zero["regex"], text_of(element)) for element in soup.select(zero["css"]))
    return {"cards": cards, "total_display": display, "total": total, "has_next": has_next(soup, parser["next"], page), "zero": is_zero, "loading": len(soup.select(parser["loading"])) if parser.get("loading") else 0}


def set_param(url, param, value):
    """주소의 나머지 글자는 건드리지 않고 param만 바꾼다. value가 None이면 뺀다."""
    base, mark, fragment = url.partition("#")
    base = re.sub(rf"([?&]){re.escape(param)}=[^&]*(&|$)", lambda match: match.group(1) if match.group(2) else "", base).rstrip("?&")
    if value is not None:
        base += ("&" if "?" in base else "?") + f"{param}={value}"
    return base + mark + fragment


def term_start(retailer, term):
    """시작 주소. start_from_arrival인 곳은 주소로 직접 들어가면 검색창 제출과 다른 화면이 나와, 10월 도착 주소의 1페이지에서 시작한다."""
    arrival = retailer.get("october_arrivals", {}).get(str(term["excel_row"]))
    if retailer.get("start_from_arrival") and arrival:
        pagination = retailer["pagination"]
        return apply_query_filters(set_param(arrival, pagination["param"], 1 if pagination.get("first_page_explicit") else None), retailer)
    return start_url(retailer, term["keyword"])


def page_url(retailer, term, page, start, arrival):
    if page == 1:
        return apply_query_filters(start, retailer)
    pagination = retailer["pagination"]
    base = apply_query_filters(arrival if pagination["applies_to"] == "arrival_url" else start, retailer)
    if pagination["kind"] == "query_param":
        return set_param(base, pagination["param"], page)
    if pagination["kind"] == "path_suffix":
        head, mark, tail = base.partition("?")
        return re.sub(r"(-p\d+)?\.htm$", "", head) + pagination["pattern"].replace("{page}", str(page)) + mark + tail
    if pagination["kind"] == "url_template":
        return start_url({**retailer, "start_url_template": pagination["pattern"].replace("{page}", str(page))}, term["keyword"])
    raise ConfigError(f"이 방식은 다음 페이지 주소가 없습니다: {pagination['kind']}")


def now_text():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def page_problem(status, body, html, block):
    """받은 응답이 쓸 수 없으면 이유를, 쓸 수 있으면 None을 돌려준다."""
    if html is None:
        return f"응답 없음(API {status} {body.get('title', '')})".strip()
    site = body.get("statusCode")
    if site and site >= 400:
        return f"사이트 상태 {site}"
    if len(html) < block["block_max_size"] and re.search(block["block_pattern"], html, re.I):
        return "차단 화면"
    return None


def fetch_page(url, retailer, page, settings, key, post=None):
    """한 페이지를 받아 읽는다. 차단·오류·1페이지 카드 없음은 설정 횟수만큼 다시 시도하고, 끝내 안 되면 ok=False."""
    post = post or zyte_post  # 기본값으로 묶으면 테스트의 가짜 호출이 먹히지 않아 실제로 나간다
    collection, probe = settings["collection"], settings["probe"]
    url = apply_query_filters(url, retailer)
    payload = payload_for(url, retailer["zyte_geolocation"], collection["methods"][retailer["search_method"]])
    problem, empty_later, partial = "", None, None
    for attempt in range(1, collection["retries"] + 2):
        status, body = post(payload, key, probe["api_url"], probe["timeout_seconds"])
        html = page_html(body)
        problem = page_problem(status, body, html, probe)
        if problem is None:
            final_url = body.get("url", url)
            if not query_filters_match(final_url, retailer):
                problem = "응답 도착 URL에서 필수 직판 검색 조건이 사라짐"
                continue
            parsed = parse_page(html, retailer["parser"], final_url, page)
            if parsed["cards"] and parsed.get("loading"):
                # 로딩 자리(아직 안 그려진 카드 칸)가 남은 화면은 다시 받는다(11-18 MEDIAEXPERT: 같은 주소가 카드 2장+로딩 28칸 또는 30장).
                # 끝내 남으면 카드가 가장 많았던 화면을 쓴다.
                record = {"ok": True, "url": url, "final_url": final_url, "attempts": attempt, "problem": "", "collected_at": now_text(), **parsed}
                if partial is None or len(parsed["cards"]) > len(partial["cards"]):
                    partial = record
                problem = f"로딩 자리 {parsed['loading']}개"
                continue
            if parsed["cards"] or parsed["zero"]:
                return {"ok": True, "url": url, "final_url": final_url, "attempts": attempt, "problem": "", "collected_at": now_text(), **parsed}
            # 2페이지 이후 빈 화면은 덜 그려진 화면일 수 있어 다시 받는다(11-18 RTV: 같은 2페이지가 0장, 다시 받으니 20장).
            # 끝내 비면 예전처럼 목록 끝으로 본다.
            if page > 1:
                empty_later = {"ok": True, "url": url, "final_url": final_url, "attempts": attempt, "problem": "", "collected_at": now_text(), **parsed}
            problem = f"카드 없음(화면 표시 전체 수 {parsed['total_display'] or '없음'})"
    if partial:
        return {**partial, "attempts": collection["retries"] + 1}
    if empty_later:
        return empty_later
    return {"ok": False, "url": url, "final_url": "", "attempts": collection["retries"] + 1, "problem": problem, "collected_at": now_text(), "cards": [], "total_display": "", "total": None, "has_next": False, "zero": False, "loading": 0}


def without_repeated_front(saved_links, cards):
    """더 보기형 사이트는 페이지 N에 앞 카드까지 다시 준다. 앞부분이 이미 저장한 목록과 똑같을 때만 잘라 낸다."""
    size = len(saved_links)
    if size and [card["link"] for card in cards[:size]] == saved_links:
        return cards[size:]
    return cards


def collect_term(retailer, term, settings, fetch, log, max_pages=None, write_lock=None):
    """검색어 하나를 끝까지 받는다. 받은 페이지는 log에 남겨, 다시 실행하면 돈을 또 쓰지 않는다."""
    lock = write_lock or threading.Lock()
    limit = settings["card_limit"]
    start = arrival = term_start(retailer, term)
    saved, pages, stop, last_links, raw_count = [], [], "max_pages", None, 0
    scroll_only = retailer["pagination"]["kind"] == "infinite_scroll"
    last_page = 1 if scroll_only else (max_pages or settings["collection"]["max_pages_per_term"])
    for page in range(1, last_page + 1):
        key = request_cache_key(f"{term['excel_row']}|{page}", retailer, start)
        with lock:
            record = log.records[key] if log.done(key) else None
        if record is None:
            record = {"page_key": key, **fetch(page_url(retailer, term, page, start, arrival), retailer, page)}
            with lock:
                log.append(record)
        pages.append(record)
        if not record["ok"]:
            stop = "failed"
            break
        if page == 1:
            arrival = record["final_url"] or start
        links = [card["link"] for card in record["cards"]]
        if links and links == last_links:
            stop = "repeat"
            break
        last_links = links
        fresh = without_repeated_front([card["link"] for card in saved], record["cards"])
        raw_count += len(fresh)
        saved += [{**card, "page": page, "final_url": record["final_url"], "total_display": record["total_display"], "collected_at": record["collected_at"]} for card in fresh]
        if len(saved) >= limit:
            saved, stop = saved[:limit], "limit"
            break
        if record["zero"]:
            stop = "zero"
            break
        if not record["cards"] or not fresh or not (record["has_next"] or continue_to_total(retailer, record, page)):
            stop = "end"
            break
    return {"term": term, "retailer": retailer, "cards": saved, "pages": pages, "stop": stop, "raw_count": raw_count}


def continue_to_total(retailer, record, page):
    """다음 단추가 없어도 화면 표시 전체 수에 닿는 쪽까지는 이어 받는다(D153, 헝가리 MediaMarkt처럼 설정한 곳만).

    헝가리 MediaMarkt는 Zyte로 받은 화면에서 다음 단추가 일찍 사라지지만, 실제 사이트는 그 뒤 쪽에도 상품이 있었다(2026-11-23 크롬 확인).
    빈 쪽, 같은 쪽 반복, 상한, 페이지 안전 한도에서는 다른 끝 조건이 그대로 멈춘다.
    """
    pagination = retailer["pagination"]
    if not pagination.get("continue_to_total") or record["total"] is None:
        return False
    return page < -(-record["total"] // pagination["per_page"])


def judge_outcome(outcome, limit):
    """(완료구분, 대조결과). 표시 수와 달라도 다시 받지 않고 적어 둔다(D060). 문구는 10월 검색어별_건수대조.csv와 같다."""
    stop, saved = outcome["stop"], len(outcome["cards"])
    good = [page for page in outcome["pages"] if page["ok"]]
    total = next((page["total"] for page in reversed(good) if page["total"] is not None), None)
    display = next((page["total_display"] for page in reversed(good) if page["total_display"]), "")
    if stop == "failed":
        return "수집 실패", f"자동 수집 실패: {outcome['pages'][-1]['problem']}. 10월 방식 수동 수집 필요(search_cards_manual.csv)"
    if stop == "zero":
        return "원문 0건", "사이트 0건 표시 확인"
    if stop == "limit":
        return "상한 적용", f"상위 {limit:,}개 저장: D056에 따른 정상 상한 적용"
    if total is None and "+" in display:
        return "끝 도달", "표시 전체 수가 정확한 숫자가 아니어서 대조하지 않음"
    if total == saved:
        return "끝 도달", "표시 수와 실제 카드 수 일치"
    if outcome["retailer"].get("total_excludes_ads") and total == sum(1 for card in outcome["cards"] if card["ad"] != "예"):
        # D154(2026-11-23): FALABELLA는 화면 표시 수에 광고 카드가 빠진다. ALZA처럼 광고가 표시 수에 들어가는 곳은 이 설정을 켜지 않는다.
        return "끝 도달", "광고 카드를 뺀 수가 표시 수와 일치"
    return "수 불일치", "화면 표시 전체 수와 실제 카드 수 불일치"


def card_rows(outcome):
    term, retailer = outcome["term"], outcome["retailer"]
    return [{"엑셀행번호": term["excel_row"], "국가": term["country"], "리테일러": term["retailer"], "F열제품군": term["category"], "J열검색어": term["keyword"], "최종검색결과URL": card["final_url"], "페이지번호": card["page"],
             "카드순번": number, "상품명": card["name"], "카드PDP링크": card["link"], "광고여부": card["ad"], "표시된전체수": card["total_display"], "수집시각": card["collected_at"], "접속국가": retailer["country"]}
            for number, card in enumerate(outcome["cards"], 1)]


def reconcile_row(outcome, limit):
    term, retailer, pages, cards = outcome["term"], outcome["retailer"], outcome["pages"], outcome["cards"]
    good = [page for page in pages if page["ok"]]
    shown = [page["total_display"] for page in good if page["total_display"]]
    changes = [value for index, value in enumerate(shown) if index == 0 or value != shown[index - 1]]
    finished, result = judge_outcome(outcome, limit)
    notes = {"repeat": "다음 페이지가 앞 페이지와 같아 멈춤", "max_pages": "페이지 안전 한도에 닿아 멈춤"}
    note = [notes[outcome["stop"]]] if outcome["stop"] in notes else []
    loading = sum(page["loading"] for page in good)
    if loading:
        note.append(f"로딩 자리 {loading}개가 남은 화면 있음")
    passed = sum(1 for page in good[:-1] if not page["has_next"])
    if passed:
        note.append(f"다음 단추가 없는 쪽 {passed}개를 지나 표시 수까지 이어 받음(D153)")
    ads = Counter(card["ad"] for card in cards)
    row = {column: "" for column in RECONCILE_COLUMNS}
    row.update({"엑셀행번호": term["excel_row"], "국가": term["country"], "리테일러": term["retailer"], "F열제품군": term["category"], "J열검색어": term["keyword"], "최초표시전체수": shown[0] if shown else "", "최종표시전체수": shown[-1] if shown else "",
                "페이지별표시수변화": " → ".join(changes), "상한": limit, "최종저장카드수": len(cards), "광고카드수": ads["예"], "광고표시없음카드수": len(cards) - ads["예"], "수집원본카드수": outcome["raw_count"], "확인페이지수": len(good),
                "최종출력마지막페이지": cards[-1]["page"] if cards else "", "완료구분": finished, "대조결과": result, "최종검색결과URL": good[-1]["final_url"] if good else "", "접속국가": retailer["country"],
                "접속근거": f"Zyte geolocation={retailer['zyte_geolocation']}", "비고": "; ".join(note), "근거": f"Zyte 자동 수집({retailer['search_method']})"})
    return row


def retailer_of(term, settings):
    return settings["retailers"][f"{term['country']}|{term['retailer']}"]


def october_pages(probe):
    """10월 엑셀행번호별 (페이지 수, 카드 수). 요청 수 예상에 쓴다."""
    _, cards = read_csv(REPO_ROOT / probe["october_cards"])
    pages, counts = defaultdict(set), Counter()
    for card in cards:
        pages[card["엑셀행번호"]].add(card["페이지번호"])
        counts[card["엑셀행번호"]] += 1
    return {row: (len(seen), counts[row]) for row, seen in pages.items()}


def expected_pages(term, retailer, october, limit):
    pagination = retailer["pagination"]
    seen, cards = october.get(str(term["excel_row"]), (1, 0))
    if pagination["kind"] == "infinite_scroll":
        return 1
    return max(1, math.ceil(min(cards, limit) / pagination["per_page"]) if pagination.get("per_page") else seen)


def plan_collection(terms, settings, sample):
    """검색어별 예상 페이지 수를 붙인다. 수동으로 정한 곳은 호출 계획에서 빼고 따로 돌려준다."""
    collection = settings["collection"]
    october = october_pages(settings["probe"])
    planned, manual = [], []
    for term in terms:
        retailer = retailer_of(term, settings)
        method = retailer.get("search_method")
        if method is None:
            raise ConfigError(f"search_method가 비어 있습니다: {term['country']} {term['retailer']}")
        if method == MANUAL:
            manual.append(term)
            continue
        if method not in collection["methods"]:
            raise ConfigError(f"모르는 search_method입니다: {method}")
        pages = expected_pages(term, retailer, october, settings["card_limit"])
        planned.append({"term": term, "retailer": retailer, "pages": 1 if retailer["pagination"]["kind"] == "infinite_scroll" else min(pages, collection["sample_pages"]) if sample else pages})
    return planned, manual


def sample_terms(terms, settings):
    """곳마다 10월에 카드가 있었던 첫 검색어(방식 실험과 같은 검색어) 하나."""
    samples = october_samples(settings["probe"])
    chosen = []
    for retailer in settings["retailers"].values():
        candidates = [term for term in terms if (term["country"], term["retailer"]) == (retailer["country"], retailer["retailer"]) and samples.get(str(term["excel_row"]), {}).get("links")]
        if not candidates:
            raise ConfigError(f"시험할 검색어가 없습니다: {retailer['country']} {retailer['retailer']}")
        chosen.append(min(candidates, key=lambda item: item["excel_row"]))
    return chosen


def render_collection_preview(month, planned, manual, settings, pricing, sample, key=None):
    collection = settings["collection"]
    expanded = [{"payload": collection["methods"][item["retailer"]["search_method"]]} for item in planned for _ in range(item["pages"])]
    http, browser, low, high = estimate(expanded, pricing)
    methods = "; ".join(f"{name} = {json.dumps(mode, ensure_ascii=False)}" for name, mode in collection["methods"].items())
    purpose = ("곳마다 검색어 1개·앞 2페이지만 받아, 고친 시작 주소·카드 규칙·페이지 넘김이 실제로 되는지 10월과 비교한다" if sample
               else f"{key}의 검색 결과 카드를 검색어별 상위 1,000개까지 모아 11월 후보로 쓴다(D056). 후보 파일에서 이 곳 행만 바꾼다" if key
               else "OSM에 없는 12곳의 검색 결과 카드를 검색어별 상위 1,000개까지 모아 11월 후보로 쓴다(D056)")
    sends = [("주소(url)", "검색어별 검색 결과 주소. 아래 표에 곳별 첫 주소 예시"), ("지역(geolocation)", "리테일러 국가 코드"), ("방식", methods), ("인증", "`.env`의 Zyte 키를 인증 머리글로만 보냄. 파일·로그에는 안 남김")]
    scale = (f"예상 {len(expanded):,}요청(HTML {http:,}, 브라우저 {browser:,}). 요청 수는 10월 페이지 수 기준 예상이며 실제는 달라질 수 있음. 페이지마다 최대 {collection['retries']}회 재시도. 공개 단가로 약 ${low:.2f} ~ ${high:.2f}. 묶음은 사이트별로 정해져 모름. "
             "확장 지역·브라우저 동작의 추가 금액은 공개 문서에 없어 이 금액은 최소치. 성공 응답만 과금")
    flag = " --sample" if sample else f" --retailer '{key}'" if key else ""
    text = call_preview("Zyte (검색 " + ("시험 수집" if sample else "본 수집") + ", WP1-3)", purpose, sends, scale, [COLLECT_COMMAND.format(month=month, flag=flag)])
    rows = ["", "| 국가 | 리테일러 | 검색어 수 | 예상 페이지 | 방식 | 지역 | 첫 주소 예시 |", "| --- | --- | --- | --- | --- | --- | --- |"]
    grouped = defaultdict(list)
    for item in planned:
        grouped[(item["term"]["country"], item["term"]["retailer"])].append(item)
    for (country, name), items in grouped.items():
        retailer = items[0]["retailer"]
        rows.append(f"| {country} | {name} | {len(items)} | {sum(item['pages'] for item in items):,} | {retailer['search_method']} | {retailer['zyte_geolocation']} | {term_start(retailer, items[0]['term'])} |")
    if manual:
        rows += ["", "수동 수집(호출 없음): " + ", ".join(sorted({f"{term['country']} {term['retailer']}" for term in manual}))]
    return text + "\n".join(rows) + "\n"


def run_collection(planned, settings, log, key, logger, max_pages=None):
    """검색어를 동시에 처리하되 한 곳에 몰리지 않게 곳별 동시 수를 제한한다. 결과는 계획 순서대로 돌려준다."""
    collection = settings["collection"]
    gates = defaultdict(lambda: threading.Semaphore(collection["workers_per_retailer"]))
    for item in planned:
        gates[item["retailer"]["retailer"]]
    write_lock = threading.Lock()

    def work(item):
        retailer = item["retailer"]
        with gates[retailer["retailer"]]:
            outcome = collect_term(retailer, item["term"], settings, lambda url, shop, page: fetch_page(url, shop, page, settings, key), log, max_pages, write_lock)
        logger.info("%s %s행: 카드 %d, 페이지 %d, 멈춘 이유 %s", retailer["retailer"], item["term"]["excel_row"], len(outcome["cards"]), len(outcome["pages"]), outcome["stop"])
        return outcome

    with ThreadPoolExecutor(max_workers=collection["workers"]) as pool:
        futures = {index: pool.submit(work, planned[index]) for index in interleaved_order(planned)}
        return [futures[index].result() for index in range(len(planned))]


def interleaved_order(planned):
    """검색어를 곳별로 번갈아 넣을 순서(계획 위치 목록). 계획 순서대로 넣으면 앞 곳의 동시 수 제한에 작업자가 모두 묶여 다른 곳이 놀았다(11-18 실행)."""
    queues = defaultdict(list)
    for index, item in enumerate(planned):
        queues[item["retailer"]["retailer"]].append(index)
    order, lists = [], list(queues.values())
    for round_ in range(max((len(x) for x in lists), default=0)):
        order += [indexes[round_] for indexes in lists if round_ < len(indexes)]
    return order


def render_sample(outcomes, settings):
    """곳별로 시험 결과를 10월과 나란히 놓는다. 자동/수동 분류(04 문서 3-4)의 근거 표."""
    samples = october_samples(settings["probe"])
    _, cards = read_csv(REPO_ROOT / settings["probe"]["october_cards"])
    october_ads = Counter(card["엑셀행번호"] for card in cards if card["페이지번호"] == "1" and card["광고여부"] == "예")
    tolerance = settings["collection"]["total_tolerance"]
    rows = ["## 시험 수집 결과", "", "| 국가 | 리테일러 | 방식 | 받은 페이지 | 1페이지 카드 | 10월 1페이지 | 같은 상품 | 광고(지금/10월) | 표시 전체 수 | 10월 표시 | ±10% 안 | 2페이지 새 카드 | 멈춘 이유 | 문제 |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for outcome in outcomes:
        term, retailer, pages = outcome["term"], outcome["retailer"], outcome["pages"]
        row = str(term["excel_row"])
        sample, first = samples[row], pages[0]
        first_cards = first["cards"]
        october_paths = {urlparse(link).path for link in sample["links"]}
        same = sum(urlparse(card["link"]).path in october_paths for card in first_cards)
        october_digits = re.sub(r"\D", "", sample["total"])
        within = ""
        if first["total"] is not None and october_digits:
            within = "예" if abs(first["total"] - int(october_digits)) <= int(october_digits) * tolerance else "아니오"
        second = sum(card["page"] == 2 for card in outcome["cards"])
        rows.append(f"| {term['country']} | {term['retailer']} | {retailer['search_method']} | {sum(page['ok'] for page in pages)}/{len(pages)} | {len(first_cards)} | {len(sample['links'])} | {same} | {sum(card['ad'] == '예' for card in first_cards)}/{october_ads[row]} | {first['total_display']} | {sample['total']} | {within} | {second if len(pages) > 1 else ''} | {outcome['stop']} | {pages[-1]['problem']} |")
    return "\n".join(rows) + "\n"


def links_seen(html, links):
    """10월 1페이지 상품 주소 중 받은 HTML에 경로가 그대로 있는 개수. 상품이 바뀌면 줄 수 있어 참고값이다."""
    return sum(urlparse(link).path in html for link in links if urlparse(link).path)


def probe_one(item, key, settings, folder):
    status, body = zyte_post(item["payload"], key, settings["api_url"], settings["timeout_seconds"])
    html = page_html(body)
    record = {"key": item["key"], "ok": html is not None, "country": item["country"], "retailer": item["retailer"], "mode": item["mode"], "api_status": status, "site_status": body.get("statusCode"),
              "final_url": body.get("url", ""), "error": body.get("title", ""), "size": len(html or ""), "blocked": False, "links_seen": 0, "links_total": len(item["october_links"])}
    if html is not None:
        (folder / f"{item['key']}.html").write_text(html, encoding="utf-8")
        record["blocked"] = record["size"] < settings["block_max_size"] and bool(re.search(settings["block_pattern"], html, re.I))
        record["links_seen"] = links_seen(html, item["october_links"])
    return record


def render_results(records):
    if not records:
        return ""
    rows = ["", "## 실험 결과", "", "| 국가 | 리테일러 | 방식 | 받음 | API 상태 | 사이트 상태 | HTML 크기 | 차단 문구 | 10월 링크 보임 | 오류 |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for record in records:
        rows.append(f"| {record['country']} | {record['retailer']} | {record['mode']} | {'예' if record['ok'] else '아니오'} | {record['api_status']} | {record['site_status'] or ''} | {record['size']:,} | {'있음' if record['blocked'] else ''} | {record['links_seen']}/{record['links_total']} | {record['error']} |")
    return "\n".join(rows) + "\n"


def run_probe(planned, settings, run, force, logger):
    folder = run.sub("html") / HTML_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    log = ResumeLog(run.sub("logs") / RECORD_NAME, "key", is_done=lambda record: True)
    key = read_secret("ZYTE_API_KEY")
    for item in planned:
        if log.done(item["key"]) and not force:
            continue
        record = probe_one(item, key, settings, folder)
        log.append(record)
        logger.info("%s: 받음=%s API=%s 사이트=%s 크기=%d", item["key"], record["ok"], record["api_status"], record["site_status"], record["size"])
    return log


def probe_main(args, run, logger, settings, pricing):
    planned = plan_requests(load_config(run, "search_terms")["terms"], settings)
    preview = render_preview(args.month, planned, settings, pricing)
    records_path = run.sub("logs") / RECORD_NAME
    if args.live:
        log = run_probe(planned, settings["probe"], run, args.force, logger)
        records = [log.records[item["key"]] for item in planned if item["key"] in log.records]
        logger.info("실험 끝: 요청 기록 %d건, 받음 %s", len(records), dict(Counter(record["ok"] for record in records)))
    else:
        records = list(ResumeLog(records_path, "key").records.values()) if records_path.exists() else []
        print(preview)
    (run.sub("logs") / REPORT_NAME).write_text(preview + render_results(records), encoding="utf-8")
    return 0


def retailer_key(name, settings):
    """--retailer 값을 search_urls.json의 '국가|리테일러' 키로 바꾼다. 리테일러 이름만 줘도 한 곳으로 정해지면 받는다(대소문자 무시)."""
    keys = list(settings["retailers"])
    if name in keys:
        return name
    matches = [key for key in keys if key.split("|", 1)[1].lower() == name.lower()]
    if len(matches) != 1:
        raise ConfigError(f"--retailer는 다음 중 하나여야 합니다('국가|리테일러'): {', '.join(keys)}")
    return matches[0]


def terms_of(terms, key):
    country, retailer = key.split("|", 1)
    chosen = [term for term in terms if (term["country"], term["retailer"]) == (country, retailer)]
    if not chosen:
        raise ConfigError(f"검색어가 없는 리테일러입니다: {key}")
    return chosen


def merge_rows(path, columns, new_rows, key, overwrite):
    """한 곳만 수집했을 때: 기존 파일에서 그 곳 행만 새 행으로 바꾸고 다른 곳 행은 그대로 둔다."""
    country, retailer = key.split("|", 1)
    old = read_csv(path)[1] if path.exists() else []
    if any((row["국가"], row["리테일러"]) == (country, retailer) for row in old) and not overwrite:
        raise FileExistsError(f"{path}에 이미 {key} 행이 있습니다. 다시 받으려면 --force")
    kept = [row for row in old if (row["국가"], row["리테일러"]) != (country, retailer)]
    write_csv(path, columns, kept + new_rows, overwrite=True)


def retailer_done(path, key):
    if not path.exists():
        return False
    country, retailer = key.split("|", 1)
    return any((row["국가"], row["리테일러"]) == (country, retailer) for row in read_csv(path)[1])


def main(argv):
    parser = new_parser("S1b 검색 수집", paid=True)
    parser.add_argument("--probe", action="store_true", help="WP1-1 방식 실험(12곳 × 3방식)")
    parser.add_argument("--sample", action="store_true", help="곳마다 검색어 1개 × 앞 2페이지 시험 수집(후보 파일은 만들지 않음)")
    parser.add_argument("--retailer", help="본 수집을 한 곳만 한다. '국가|리테일러'(예: 'Netherlands|MEDIAMARKT') 또는 한 곳으로 정해지는 리테일러 이름. 결과는 후보 파일의 그 곳 행만 바꾼다")
    args = parser.parse_args(argv)
    if args.probe and args.sample:
        raise ConfigError("--probe와 --sample은 함께 쓸 수 없습니다")
    if args.retailer and (args.probe or args.sample):
        raise ConfigError("--retailer는 본 수집에만 씁니다(--probe, --sample과 함께 쓸 수 없음)")
    run = RunPaths(args.month).create()
    logger = get_logger(run, "s1b")
    settings = load_config(run, "search_urls")
    pricing = load_config(run, "zyte_pricing")
    if args.probe:
        return probe_main(args, run, logger, settings, pricing)
    terms = load_config(run, "search_terms")["terms"]
    key = retailer_key(args.retailer, settings) if args.retailer else None
    selected = sample_terms(terms, settings) if args.sample else terms_of(terms, key) if key else terms
    planned, manual = plan_collection(selected, settings, args.sample)
    preview = render_collection_preview(args.month, planned, manual, settings, pricing, args.sample, key)
    if not args.live:
        print(preview)
        return 0
    folder = run.sub("candidates")
    outputs = [folder / CARDS_NAME, folder / RECONCILE_NAME]
    if key and not args.force and retailer_done(outputs[1], key):
        validate_existing_cards(outputs[0], settings)
        logger.info("이미 있어 건너뜁니다: %s (%s)", key, outputs[1])
        return 0
    if not key and not args.sample and outputs_ready(outputs, args.force):
        validate_existing_cards(outputs[0], settings)
        logger.info("이미 있어 건너뜁니다: %s", ", ".join(map(str, outputs)))
        return 0
    log = ResumeLog(run.sub("logs") / (SAMPLE_PAGES_NAME if args.sample else PAGES_NAME), "page_key")
    outcomes = run_collection(planned, settings, log, read_secret("ZYTE_API_KEY"), logger, settings["collection"]["sample_pages"] if args.sample else None)
    if args.sample:
        report = render_sample(outcomes, settings)
        (run.sub("logs") / SAMPLE_REPORT).write_text(preview + "\n" + report, encoding="utf-8")
        print(report)
        return 0
    limit = settings["card_limit"]
    cards = [row for outcome in outcomes for row in card_rows(outcome)]
    reconcile = [reconcile_row(outcome, limit) for outcome in outcomes]
    if key:
        merge_rows(outputs[0], list(CARD_COLUMNS), cards, key, args.force)
        merge_rows(outputs[1], list(RECONCILE_COLUMNS), reconcile, key, args.force)
    else:
        write_csv(outputs[0], list(CARD_COLUMNS), cards, overwrite=args.force)
        write_csv(outputs[1], list(RECONCILE_COLUMNS), reconcile, overwrite=args.force)
    finished = Counter(row["완료구분"] for row in reconcile)
    logger.info("본 수집 끝: 검색어 %d개, 카드 %d장, 완료구분 %s", len(reconcile), sum(int(row["최종저장카드수"]) for row in reconcile), dict(finished))
    failed = [row for row in reconcile if row["완료구분"] == "수집 실패"]
    for row in failed:
        logger.warning("수동 수집 필요: %s %s %s행 %s — %s", row["국가"], row["리테일러"], row["엑셀행번호"], row["J열검색어"], row["대조결과"])
    return 1 if failed else 0
