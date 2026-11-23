"""S2 1차 거르기: 상품명·주소만으로 브랜드 → 제품군 → 리리부 순서로 판정한다. 중복은 여기서 빼지 않고 S5가 접속 후 URL로 본다(2026-11-23).

제품군 단계에는 리테일러별 상품명 약어(Electroplanet), 주소 분류(RTV), OSM 상품명의 제외 단어 검사가 들어 있다(D143).

페이지를 열어야 아는 판단(판매자, 실제 도착 주소)은 S3 이후에 한다. 규칙 값은 회차 폴더의 config에서 읽는다.
"""
import re
from collections import Counter
from urllib.parse import urlparse

from common import ConfigError, RunPaths, get_logger, load_config, load_output_spec, new_parser, outputs_ready, read_csv, write_csv

BRAND_STAGE, CATEGORY_STAGE, KEYWORD_STAGE, DUPLICATE_STAGE = "①브랜드", "②제품군", "③리리부", "④중복"
KEEP, EXCLUDE, CHECK = "남김", "제외", "확인 필요"
# 묶음 상품 판정(D052)에서 대상 제품군 단어를 찾는 상품명 앞부분 단어 수. AI가 정한 값이다(사용자·EY 결정 아님, 2026-11-23).
# 왜 전체가 아니라 앞부분만 보나: 전체에서 찾으면 단품 설명의 기능 목록 단어가 대상 단어로 맞아 단품이 묶음으로 남는다.
#   실제 사례(10월 폴란드 MEDIAEXPERT): 'Kuchenka mikrofalowa HISENSE H28SO1 Speed Oven 7w1 Air Fry Grill Pizza Toster Suszarka …'
#   (Hisense 전자레인지 단품). 12번째 단어 Suszarka(여기서는 '식품 건조 기능')가 건조기 단어 suszark에 맞아, 전체에서 찾으면 남는다.
# 왜 8인가: 묶음은 본 상품을 상품명 맨 앞에 쓰고 끼워 주는 물건을 '+' 뒤에 붙인다. 확인한 진짜 묶음 92행(11월 연습 68 + 10월 24)은
#   대상 단어가 모두 1~6번째 단어에 있었다(가장 뒤: Sharaf DG 'Samsung Series 8 Front Load Washing Machine'의 Washing, 6번째).
#   12 이상으로 늘리면 위 전자레인지가 다시 묶음으로 남는다.
BUNDLE_HEAD_WORDS = 8
OSM_FLOW, SEARCH_FLOW = "OSM", "검색"
SUMMARY_COLUMNS = ["흐름", "국가", "리테일러", "전체", BRAND_STAGE, CATEGORY_STAGE, KEYWORD_STAGE, DUPLICATE_STAGE, KEEP, CHECK]
JUDGED_ELSEWHERE = ("브랜드", "제품코드", "페이지상태", "실제URL", "판매자", "판매자구분", "판매자근거")


def brand_regex(brand):
    parts = [re.escape(part) for part in brand.lower().replace("&", " ").split()]
    return re.compile(r"(?<![a-z0-9])" + r"[\s\-_&+]*".join(parts) + r"(?![a-z0-9])")


CJK = re.compile(r"[\u2e80-\u9fff\uf900-\ufaff\uff00-\uffef]")


def keyword_regex(word):
    """제외 키워드 정규식. 한자·가나로 시작하는 단어는 띄어쓰기가 없어 앞 글자 경계를 보지 않는다(D144: 福利品이 문장 중간에 붙어도 잡는다)."""
    return re.compile(("" if CJK.match(word) else r"(?<![\w])") + re.escape(word))


def brand_prefix(brand, retailer, prefix):
    """osm_brand_prefix 리테일러면 대문자 브랜드의 맨 앞 영문 단어만 돌려준다(D142·D144). 아니면 대문자 브랜드 그대로."""
    brand = (brand or "").strip().upper()
    if prefix and retailer in prefix.get("retailers", []):
        found = re.match(prefix["pattern"], brand)
        if found:
            return found.group(1)
    return brand


def url_words(url):
    return urlparse(url).path.replace("/", " ").replace("-", " ").replace("_", " ")


class Rules:
    """설정 파일을 판정에 바로 쓸 수 있는 형태로 묶는다."""

    def __init__(self, brands, keywords, categories, retailer_rules, s0_input):
        self.brands, self.category_fallback, self.alias = brands["brands"], s0_input["category_fallback"], s0_input["country_alias"]
        self.categories, self.retailer_rules = categories, retailer_rules
        self.common = retailer_rules["common"]
        self.keywords = {country: [(item["type"], item["keyword"], keyword_regex(item["keyword"])) for item in items]
                         for country, items in keywords["keywords"].items()}
        self.brand_regexes = {}
        self.page_rule_text = {(rule["country"], rule["retailer"]): rule["text"] for rule in retailer_rules["page_rule_text"]}
        self.name_codes = {retailer: [(item["name"], item["stage"], re.compile(item["pattern"]), re.compile(item["unless"]) if item.get("unless") else None) for item in items]
                           for retailer, items in categories.get("retailer_name_codes", {}).items() if not retailer.startswith("_")}
        self.url_categories = [{**rule, "allow": re.compile(rule["allow"]), "parts": re.compile(rule["parts"])} for rule in retailer_rules.get("url_categories", [])]
        osm_names = set(categories.get("osm_negative", {}).get("names", []))
        self.osm_negative = [(item["name"], re.compile(item["pattern"])) for item in categories["negative"] if item["name"] in osm_names]
        self.positive = [re.compile(pattern) for pattern in categories["positive"].values()]

    def country(self, name):
        name = (name or "").strip()
        return self.alias.get(name, name)

    def target_brands(self, country, div):
        category = {"D/W": "DW"}.get(div) or self.category_fallback.get(div, div)
        return self.brands.get(country, {}).get(category, [])

    def brands_in(self, text, targets):
        lowered = text.lower()
        found = []
        for brand in targets:
            regex = self.brand_regexes.setdefault(brand, brand_regex(brand))
            arabic = self.common["arabic_brand_patterns"].get(brand.lower())
            if regex.search(lowered) or (arabic and re.search(arabic, " ".join(lowered.split()[:3]))):
                found.append(brand)
        return found

    def head(self, name):
        return " ".join(re.split(r"\s+", name.strip().lower())[:self.categories["head_words"]])

    def search_category(self, value):
        lowered = value.lower()
        return next((div for word, div in self.categories["search_category_map"].items() if word in lowered), "?")

    def check_search_category(self, text):
        """(결과, 이름). 결과는 제외·묶음·냉동고·통과·단어없음 중 하나다.

        제외 단어가 있어도, 그 단어를 지운 나머지에 대상 제품군 단어가 있으면 묶음 상품으로 보고 남긴다(D052: 대상 제품이 하나라도 들어
        있으면 유지). 예: 'Lavadora WT19BVTB + Tendedero'(세탁기 + 빨래 건조대). 지우고 보는 이유는 'dishwasher' 안의 'washer'처럼
        제외 단어 속 글자가 대상 단어로 잘못 맞지 않게 하려는 것이다(2026-11-23).
        대상 단어는 앞 8단어 안에서만 찾는다. 묶음은 본 상품이 상품명 앞에 오고, 'Kuchenka mikrofalowa … grill pizza toster suszarka'
        (전자레인지 기능 목록의 '건조')처럼 단품 설명 뒤쪽에 나오는 단어는 묶음이 아니다(10월 MEDIAEXPERT 실제 상품명).
        """
        lowered = text.lower()
        hit, rest = None, " ".join(lowered.split()[:BUNDLE_HEAD_WORDS])
        for item in self.categories["negative"]:
            if re.search(item["pattern"], lowered):
                hit = hit or item["name"]
                rest = re.sub(item["pattern"], " ", rest)
        if hit:
            if any(re.search(pattern, rest) for pattern in self.categories["positive"].values()):
                return "묶음", hit
            return "제외", hit
        if re.search(self.categories["freezer_head"], self.head(lowered)) and not re.search(self.categories["freezer_combo_search"], lowered):
            return "냉동고", ""
        if any(re.search(pattern, lowered) for pattern in self.categories["positive"].values()):
            return "통과", ""
        return "단어없음", ""

    def keyword_hit(self, country, name):
        lowered = name.lower()
        return next(((kind, word) for kind, word, regex in self.keywords.get(country, []) if regex.search(lowered)), None)

    def name_code(self, row):
        """상품명 맨 앞 종류 약어로 조사 제품군 밖 상품이면 (제외단계, 제외사유). 아니면 None."""
        lowered = " ".join((row["상품명"] or "").lower().split())
        for name, stage, regex, unless in self.name_codes.get(row["리테일러"], []):
            if regex.search(lowered) and not (unless and unless.search(lowered)):
                return stage, (f"부품({name}, 상품명 약어)" if stage == KEYWORD_STAGE else f"대상 제품군 아님({name}, 상품명 약어)")
        return None

    def lead_brand(self, row):
        """상품명이 【브랜드 …】로 시작하는 리테일러(name_lead_brand)면 그 맨 앞 브랜드(대문자). 아니면 None."""
        pattern = self.common.get("name_lead_brand", {}).get(row["리테일러"])
        found = re.match(pattern, (row["상품명"] or "").strip()) if pattern else None
        return found.group(1).upper() if found else None

    def url_category(self, row):
        """주소 경로 첫 칸(리테일러 상품 분류)으로 판정한다. 대상 분류면 None, 아니면 (제외단계, 제외사유)."""
        for rule in self.url_categories:
            if rule["country"] != row["국가"] or rule["retailer"] != row["리테일러"]:
                continue
            segment = (urlparse(row["URL"]).path.strip("/").split("/") or [""])[0].lower()
            if rule["parts"].search(segment):
                return KEYWORD_STAGE, rule["parts_reason"].format(segment=segment)
            if rule["allow"].search(segment):
                return None
            return CATEGORY_STAGE, rule["other_reason"].format(segment=segment)
        return None

    def osm_negative_hit(self, name):
        """OSM 상품명에 제외 단어(osm_negative 이름만)가 있고 대상 제품군 단어가 없으면 그 이름. 아니면 None."""
        lowered = name.lower()
        hit = next((label for label, regex in self.osm_negative if regex.search(lowered)), None)
        if hit and not any(regex.search(lowered) for regex in self.positive):
            return hit
        return None

    def url_exclusion(self, row):
        for rule in self.retailer_rules["url_exclusions"]:
            if rule["country"] != row["국가"] or rule.get("retailer", row["리테일러"]) != row["리테일러"]:
                continue
            url = row["URL"].lower() if rule["ignore_case"] else row["URL"]
            hit = next((word for word in rule["contains"] if word in url), None)
            if hit:
                return rule["reason"].format(hit=hit)
        return None


def osm_rows(path, source_name, rules, keep=lambda row: True):
    _, rows = read_csv(path)
    for row in rows:
        if not keep(row):
            continue
        crawl = row.get("CRAWL_URL")
        yield {"흐름": OSM_FLOW, "출처파일": source_name, "국가": rules.country(row["CNTRY"]), "리테일러": row["RTLR_NAME"].strip(), "제품군": row["DIV"],
               "OSM브랜드": row["BRAND"], "상품명": row["PRODUCT_DESC"], "URL": crawl if crawl not in (None, "", "\\N") else row["RAW_URL"],
               "원본URL": row["RAW_URL"], "기준일": row["RPT_DATE"], "검색어": "", "엑셀행번호": "", "광고여부": "", "OSM_RK": row["RK"], "OSM_SOURCE_TYPE": row["SOURCE_TYPE"]}


def search_rows(path, source_name, rules):
    _, rows = read_csv(path)
    for row in rows:
        yield {"흐름": SEARCH_FLOW, "출처파일": source_name, "국가": rules.country(row["국가"]), "리테일러": row["리테일러"].strip(), "제품군": rules.search_category(row["F열제품군"]),
               "OSM브랜드": "", "상품명": row["상품명"], "URL": row["카드PDP링크"], "원본URL": row["카드PDP링크"], "기준일": row["수집시각"][:10],
               "검색어": row["J열검색어"], "엑셀행번호": row["엑셀행번호"], "광고여부": row["광고여부"], "OSM_RK": "", "OSM_SOURCE_TYPE": ""}


def judge(row, rules):
    """(판정, 제외단계, 제외사유, 메모)를 돌려준다."""
    country, div, name, url = row["국가"], row["제품군"], row["상품명"] or "", row["URL"]
    memo, notes = [], []
    common = rules.common
    is_search = row["흐름"] == SEARCH_FLOW
    dishwasher_outside = div == common["dishwasher_div"] and country not in common["dishwasher_countries"]
    targets = rules.target_brands(country, div)
    if is_search:
        if div == "?":
            return CHECK, CATEGORY_STAGE, "검색어 제품군 해석 불가", ""
        found = rules.brands_in(f"{name} {url_words(url)}", targets)
        if not found:
            return EXCLUDE, BRAND_STAGE, "대상 브랜드 이름 없음(상품명·주소)", ""
        if len(found) > 1:
            memo.append("대상 브랜드 여러 개: " + ",".join(found))
    elif not dishwasher_outside:
        brand = brand_prefix(row["OSM브랜드"], row["리테일러"], rules.common.get("osm_brand_prefix"))
        if not targets:
            return CHECK, BRAND_STAGE, f"경쟁브랜드 목록 없음({country} {div})", ""
        if brand not in targets:
            return EXCLUDE, BRAND_STAGE, f"대상 브랜드 아님({brand})", ""
    lead = rules.lead_brand(row)
    if lead and targets and lead not in targets:
        return EXCLUDE, BRAND_STAGE, f"상품명 맨 앞 브랜드가 대상 아님({lead})", ""
    if dishwasher_outside:
        return EXCLUDE, CATEGORY_STAGE, common["dishwasher_reason"], ""
    for found in (rules.name_code(row), rules.url_category(row)):
        if found:
            return EXCLUDE, found[0], found[1], ""
    if not is_search:
        negative = rules.osm_negative_hit(name)
        if negative:
            return EXCLUDE, CATEGORY_STAGE, f"대상 제품군 아님({negative}, OSM 상품명에 대상 제품군 단어 없음)", ""
    categories = rules.categories
    if is_search:
        result, category_name = rules.check_search_category(f"{name} {url_words(url)}")
        if result == "제외":
            return EXCLUDE, CATEGORY_STAGE, f"대상 제품군 아님({category_name})", ""
        if result == "묶음":
            notes.append(f"묶음 상품({category_name} 함께 판매, 대상 제품이 있어 유지, D052)")
        elif result == "냉동고":
            notes.append(categories["freezer_note"])
        elif result == "단어없음":
            notes.append(categories["no_category_note"])
    elif re.search(categories["freezer_head"], rules.head(name)) and not re.search(categories["freezer_combo_osm"], name.lower()):
        notes.append(categories["freezer_note"])
    hit = rules.keyword_hit(country, name)
    if hit:
        return EXCLUDE, KEYWORD_STAGE, f'{hit[0]} 단어 "{hit[1]}"(제외키워드 시트)', ""
    excluded = rules.url_exclusion(row)
    if excluded:
        return EXCLUDE, KEYWORD_STAGE, excluded, ""
    if re.search(r"(?<![\w])(?:" + categories["part_suspect"] + ")", rules.head(name)):
        memo.append(categories["part_suspect_memo"])
    notes += [item["note"] for item in rules.retailer_rules["url_notes"] if item["retailer"] == row["리테일러"] and item["contains"] in url]
    return (CHECK if memo else KEEP), "", "", "; ".join(memo + notes)


def judge_all(rows, rules, columns):
    """모든 행을 판정하고 내부판 열로 채운다.

    요청 URL이 같아도 여기서는 중복으로 빼지 않는다(2026-11-23 사용자 결정). 중복은 S5가 접속 후 URL로만 판정한다.
    S3는 겹치지 않는 요청 URL만 한 번씩 열므로 Zyte 호출 수는 늘지 않는다.
    """
    judged = []
    for number, row in enumerate(rows, start=1):
        status, stage, reason, memo = judge(row, rules)
        judged.append({**row, "행번호": str(number), "판정": status, "제외단계": stage, "제외사유": reason, "메모": memo,
                       "페이지확인규칙": rules.page_rule_text.get((row["국가"], row["리테일러"]), ""), **{name: "" for name in JUDGED_ELSEWHERE}})
    extra = set(judged[0]) ^ set(columns) if judged else set()
    if extra:
        raise ConfigError(f"S2 행의 열이 output.json과 다릅니다: {sorted(extra)}")
    return judged


def summarize(judged):
    counts = {}
    for row in judged:
        key = (row["흐름"], row["국가"], row["리테일러"])
        counter = counts.setdefault(key, Counter())
        counter["전체"] += 1
        counter[row["제외단계"] if row["판정"] == EXCLUDE else row["판정"]] += 1
    return [{"흐름": flow, "국가": country, "리테일러": retailer, **{name: str(counter[name]) for name in SUMMARY_COLUMNS[3:]}}
            for (flow, country, retailer), counter in sorted(counts.items())]


def load_rules(run, data_run=None):
    """data_run을 주면 브랜드·키워드만 그 회차 값을 쓴다(10월 대조용)."""
    source = data_run or run
    return Rules(load_config(source, "brands"), load_config(source, "keywords"), load_config(run, "categories"), load_config(run, "retailer_rules"), load_config(run, "s0_input"))


def input_rows(run, rules):
    folder = run.sub("candidates")
    required = [folder / "osm_candidates.csv", folder / "search_cards.csv"]
    missing = [path for path in required if not path.exists()]
    if missing:
        raise ConfigError("S2 입력이 없습니다: " + ", ".join(map(str, missing)))
    rows = list(osm_rows(required[0], required[0].name, rules))
    for path in (required[1], folder / "search_cards_manual.csv"):
        if path.exists():
            rows += search_rows(path, path.name, rules)
    return rows


def main(argv):
    args = new_parser("S2 1차 거르기: 브랜드·제품군·리리부(중복은 S5에서)").parse_args(argv)
    run = RunPaths(args.month).create()
    logger = get_logger(run, "s2")
    folder = run.sub("judgments")
    outputs = [folder / "step1.csv", folder / "step1_summary.csv"]
    if outputs_ready(outputs, args.force):
        logger.info("출력이 이미 있어 건너뜁니다(다시 하려면 --force)")
        return 0
    spec = load_output_spec(run)
    if not {BRAND_STAGE, CATEGORY_STAGE, KEYWORD_STAGE, DUPLICATE_STAGE} <= set(spec.exclusion_stages):
        raise ConfigError("output.json의 제외단계 값이 S2와 다릅니다")
    rules = load_rules(run)
    judged = judge_all(input_rows(run, rules), rules, spec.internal_columns)
    write_csv(outputs[0], list(spec.internal_columns), judged, overwrite=args.force)
    write_csv(outputs[1], SUMMARY_COLUMNS, summarize(judged), overwrite=args.force)
    logger.info("S2 끝: %d행, 판정 %s", len(judged), dict(Counter(row["판정"] for row in judged)))
    return 0
