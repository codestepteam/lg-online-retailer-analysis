"""EY '25개국 분석' 엑셀 사본에 값을 채운다. 원본 파일은 건드리지 않는다.

사용: python -I fill_workbook.py <원본.xlsx> <자료 폴더> <결과.xlsx> <계산값.json>
"""
import json
import re
import sys
from openpyxl import load_workbook

SRC, DATA, OUT, OUT_JSON = sys.argv[1:5]

COLS = ["readiness", "34", "39", "47", "37", "38", "42", "43", "vis", "1", "2", "3", "4", "catsov"]
PDP5 = ["34", "39", "47", "37", "38"]
CATS = ["REF", "WM", "DW"]
BRANDS = ["LG", "SAMSUNG"]

COUNTRY_CODE = {
    "United Kingdom": "UK", "Germany": "DE", "Czech": "CZ", "France": "FR", "Italy": "IT",
    "Netherlands": "NL", "Poland": "PL", "Spain": "ES", "Sweden": "SE", "Canada": "CA",
    "Chile": "CL", "Mexico": "MX", "Peru": "PE", "Brazil": "BR", "Hungary": "HU",
    "Portugal": "PT", "Egypt": "EG", "UAE": "AE", "Morocco": "MA", "Saudi Arabia": "SA",
    "Australia": "AU", "Singapore": "SG", "Thailand": "TH", "Taiwan": "TW", "Vietnam": "VN",
}
RETAILER_KEY = {
    ("UK", "AO"): "ao", ("UK", "Currys"): "currys",
    ("DE", "MediaMarkt"): "mediamarkt-de", ("DE", "Amazon"): "amazon-de", ("DE", "Otto"): "otto",
    ("CZ", "Alza"): "alza", ("CZ", "Datart"): "datart",
    ("FR", "Boulanger"): "boulanger", ("FR", "Darty"): "darty",
    ("IT", "Amazon"): "amazon-it", ("IT", "Mediaworld"): "mediaworld", ("IT", "Unieuro"): "unieuro",
    ("NL", "Coolblue"): "coolblue", ("NL", "MediaMarkt"): "mediamarkt-nl",
    ("PL", "MediaExpert"): "media-expert", ("PL", "RtvEuroAgd"): "rtv-euro-agd",
    ("ES", "ECI"): "eci", ("ES", "MediaMarkt"): "mediamarkt-es",
    ("SE", "Elgiganten"): "elgiganten", ("CA", "Costco"): "costco-ca",
    ("CL", "FALABELLA"): "falabella-cl", ("MX", "Liverpool"): "liverpool",
    ("PE", "FALABELLA"): "falabella-pe", ("BR", "Magazine Luiza (MAGALU)"): "magalu",
    ("HU", "MediaMarkt"): "mediamarkt-hu", ("PT", "Worten"): "worten",
    ("EG", "Cairo Sales"): "cairo-sales", ("AE", "Sharaf DG"): "sharaf-dg",
    ("MA", "electroplanet"): "electroplanet", ("SA", "eXtra"): "extra-sa",
    ("AU", "Appliance Online"): "appliance-online", ("SG", "Lazada"): "lazada-sg",
    ("TH", "Lazada"): "lazada-th", ("TW", "Momoshop"): "momoshop", ("VN", "DIENMAYXANH"): "dienmayxanh",
}
SEVEN = {"ES", "FR", "IT", "SE", "NL", "PL", "CZ"}
TWO = {"UK", "DE"}


def group_of(cc):
    return "7" if cc in SEVEN else ("2" if cc in TWO else "16")


def load(name):
    with open(f"{DATA}/{name}", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def rkey(r):
    return str(r).strip().lower().replace("_", "-")


def num(v):
    if v is None:
        return None
    return float(v)


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def total(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) if xs else None


# ---------- 1) 카테고리 단위 값 모으기: cat[월][브랜드][(국가, 리테일러, 카테고리)][칸] ----------
cat = {m: {b: {} for b in BRANDS} for m in ("8", "10", "11")}


def put(month, brand, cc, ret, category, col, value):
    if value is None:
        return
    cat[month][brand].setdefault((cc.upper(), rkey(ret), category.upper()), {})[col] = value


# 8월 상품 상세(PDP) 지표: EY 8월 엑셀의 집계 조건(유지 표식·프랑스 대상 표식·이탈리아 제외 표식·리뷰 평점 0 제외)을
# 그대로 적용한 대시보드 8월 전용 계산(first_report)의 통과 수 ÷ 대상 수. 대상이 0건이면 EY 엑셀과 같이 0으로 적고,
# ID43만 빈칸으로 둔다(EY 엑셀 표기 N/A). 만드는 코드: aug_first_report.py
for r in load("aug_first_report.jsonl"):
    n, tot_ = int(r["n"]), int(r["total"])
    if tot_ > 0:
        v = n / tot_ * 100
    else:
        v = None if str(r["assessment_id"]) == "43" else 0.0
    put("8", r["brand"], r["country"], r["retailer"], r["category"], str(r["assessment_id"]), v)

# 10월 상품 상세(PDP) 7개 지표: 0~1 비율 → 0~100
for month, files in {"10": ("oct_lg.jsonl", "oct_brand_SAMSUNG.jsonl")}.items():
    for brand, fn in zip(BRANDS, files):
        for r in load(fn):
            v = num(r["value"])
            put(month, brand, r["country"], r["retailer"], r["category"], str(r["assessment_id"]), None if v is None else v * 100)

# 10·11월 검색 노출(ID1~3 = 검색어별 점수 합, ID4 = 검색어별 평균)
for month, fn in {"10": "oct_plp_lg.jsonl", "11": "nov_plp_dev.jsonl"}.items():
    for r in load(fn):
        if int(r["scored"]) == 0:
            continue
        v = num(r["avg_score"]) if r["assessment_id"] == "4" else num(r["sum_score"])
        put(month, r["brand"], r["country"], r["retailer"], r["category"], r["assessment_id"], v)

# 8월 검색 노출(기준 자료의 검색어별 값)
aug = {}
for r in load("aug_plp_lg.jsonl"):
    raw = str(r["raw"]).strip().strip('"').strip()
    if r["assessment_id"] == "4":
        m = re.fullmatch(r"(\d+(?:\.\d+)?)%", raw)
        if not m:
            raise SystemExit(f"8월 ID4 값 형식이 예상과 다름: {r}")
        v = float(m.group(1))
    else:
        if not re.fullmatch(r"\d+(?:\.\d+)?", raw):
            raise SystemExit(f"8월 점수 값 형식이 예상과 다름: {r}")
        v = float(raw)
    aug.setdefault((r["brand"], r["country"], r["retailer"], r["category"], r["assessment_id"]), []).append(v)
for (brand, cc, ret, category, aid), vals in aug.items():
    put("8", brand, cc, ret, category, aid, mean(vals) if aid == "4" else sum(vals))

# Category SOV(카테고리 목록 상위 10개 중 브랜드 비중, %)
sov = []
for r in load("catsov_lg.jsonl"):
    if r["ym"] == "2026-10":
        sov.append(("10", r["brand"], r["country"], r["retailer"], r["category"], num(r["category_sov"])))
for r in load("catsov_dev.jsonl"):
    if r["ym"] == "2026-11":
        sov.append(("11", r["brand"], r["country"], r["retailer"], r["category"], num(r["category_sov"])))
augsov = {}
for r in load("aug_catsov_lg.jsonl"):
    augsov.setdefault((r["brand"], r["country"], r["retailer"], r["category"]), []).append(int(r["top10_count"]) * 10.0)
for (brand, cc, ret, category), vals in augsov.items():
    sov.append(("8", brand, cc, ret, category, mean(vals)))
skipped_sov = []
for month, brand, cc, ret, category, v in sov:
    key = (cc.upper(), rkey(ret), category.upper())
    # 대시보드와 같은 기준: 그 리테일러·카테고리의 비교 브랜드(검색 노출 결과가 있는 브랜드)이거나,
    # 그 달 카테고리 목록 상위 10개에 한 번이라도 보인 브랜드만 값을 적는다. 둘 다 아니면 비워 둔다.
    if not any(c in cat[month][brand].get(key, {}) for c in ("1", "2", "3", "4")) and not (v and v > 0):
        skipped_sov.append((month, brand) + key)
        continue
    put(month, brand, cc, ret, category, "catsov", v)

# 묶음 점수
for month in cat:
    for brand in BRANDS:
        for key, d in cat[month][brand].items():
            if all(c in d for c in PDP5):
                d["readiness"] = sum(d[c] for c in PDP5) / 5
            if "4" in d and "catsov" in d:
                d["vis"] = (d["4"] + d["catsov"]) / 2

# ---------- 2) 리테일러 → 국가 ----------
ret = {m: {b: {} for b in BRANDS} for m in cat}
for month in cat:
    for brand in BRANDS:
        keys = {(cc, r) for (cc, r, c) in cat[month][brand] if c in CATS}
        for cc, r in keys:
            d = {}
            for col in COLS:
                v = mean([cat[month][brand].get((cc, r, c), {}).get(col) for c in CATS])
                if v is not None:
                    d[col] = v
            ret[month][brand][(cc, r)] = d
country = {m: {b: {} for b in BRANDS} for m in cat}
for month in cat:
    for brand in BRANDS:
        for cc in {cc for (cc, r) in ret[month][brand]}:
            d = {}
            for col in COLS:
                v = mean([dd.get(col) for (c2, r), dd in ret[month][brand].items() if c2 == cc])
                if v is not None:
                    d[col] = v
            country[month][brand][cc] = d


def index(lg, ss):
    if lg is None or ss is None or ss == 0:
        return None
    return int(round(lg / ss * 100))


# ---------- 3) 엑셀 채우기 ----------
wb = load_workbook(SRC)
written = {}
AGG_LABELS = ["7개국 합계", "16개국 합계", "25개국 합계", "7개국 평균", "16개국 평균", "25개국 평균"]


def setv(ws, row, col, value, fmt=None):
    if value is None:
        return
    c = ws.cell(row=row, column=col)
    if c.value is not None:
        raise SystemExit(f"이미 값이 있는 칸: {ws.title}!{c.coordinate}")
    c.value = value
    if fmt:
        c.number_format = fmt
    written[f"{ws.title}!{c.coordinate}"] = value


def agg_groups(month):
    return ["7"] if month == "8" else ["7", "16", "25"]


def write_aggs(ws, first_agg_row, col, rows_by_group, month):
    """rows_by_group: [(국가 묶음, 값)] — 아래 표에 실제로 적힌 값들."""
    assert [ws.cell(row=first_agg_row + i, column=2).value for i in range(6)] == AGG_LABELS, ws.title
    for i, g in enumerate(["7", "16", "25"]):
        if g not in agg_groups(month):
            continue
        vals = [v for grp, v in rows_by_group if v is not None and (g == "25" or grp == g)]
        setv(ws, first_agg_row + i, col, total(vals))
        setv(ws, first_agg_row + 3 + i, col, mean(vals))


def label_country(ws, row):
    name = str(ws.cell(row=row, column=2).value).strip()
    return COUNTRY_CODE[name]


def label_retailer(ws, row, col=3, ccol=2):
    cc = COUNTRY_CODE[str(ws.cell(row=row, column=ccol).value).strip()]
    return cc, RETAILER_KEY[(cc, str(ws.cell(row=row, column=col).value).strip())]


for month in ("8", "10"):
    ws = wb[f"{month}월_국가"]
    for bi, brand in enumerate(BRANDS):
        for ci, col in enumerate(COLS):
            xc = 3 + bi * 14 + ci
            rows = []
            for row in range(11, 36):
                cc = label_country(ws, row)
                v = country[month][brand].get(cc, {}).get(col)
                setv(ws, row, xc, v, "0.0")
                rows.append((group_of(cc), v))
            write_aggs(ws, 5, xc, rows, month)
    ws = wb[f"{month}월_국가x리테일러"]
    for bi, brand in enumerate(BRANDS):
        for ci, col in enumerate(COLS):
            xc = 4 + bi * 14 + ci
            rows = []
            for row in range(11, 46):
                cc, r = label_retailer(ws, row)
                v = ret[month][brand].get((cc, r), {}).get(col)
                setv(ws, row, xc, v, "0.0")
                rows.append((group_of(cc), v))
            write_aggs(ws, 5, xc, rows, month)

for month in ("8", "10", "11"):
    ws = wb[f"{month}월_국가x리테일러x카테고리"]
    for bi, brand in enumerate(BRANDS):
        for ki, category in enumerate(CATS):
            for ci, col in enumerate(COLS):
                xc = 4 + bi * 42 + ki * 14 + ci
                rows = []
                for row in range(12, 47):
                    cc, r = label_retailer(ws, row)
                    v = cat[month][brand].get((cc, r, category), {}).get(col)
                    setv(ws, row, xc, v, "0.0")
                    rows.append((group_of(cc), v))
                write_aggs(ws, 6, xc, rows, month)

# Summary: 삼성 대비 지수 = LG ÷ 삼성 × 100 (정수)
# 합계·평균 줄: LG와 삼성 값이 둘 다 있는 줄만 모아 (LG 합 ÷ 삼성 합 × 100). 같은 줄끼리 나누므로 합계 줄과 평균 줄의 지수는 같다.
ws = wb["※ 25개국 Summary"]
assert [ws.cell(row=6 + i, column=2).value for i in range(6)] == AGG_LABELS


def summary_block(xc, rows, month):
    """rows: [(국가 묶음, LG 값, 삼성 값)]"""
    for i, g in enumerate(["7", "16", "25"]):
        if g not in agg_groups(month):
            continue
        pairs = [(a, b) for grp, a, b in rows if a is not None and b is not None and (g == "25" or grp == g)]
        if not pairs:
            continue
        v = index(sum(a for a, _ in pairs), sum(b for _, b in pairs))
        setv(ws, 6 + i, xc, v)
        setv(ws, 9 + i, xc, v)


for mi, month in enumerate(("8", "10", "11")):
    for si, col in enumerate(("readiness", "vis")):
        xc = 3 + si * 3 + mi  # 왼쪽 표: 국가
        rows = []
        for row in range(12, 37):
            cc = label_country(ws, row)
            a, b = country[month]["LG"].get(cc, {}).get(col), country[month]["SAMSUNG"].get(cc, {}).get(col)
            setv(ws, row, xc, index(a, b))
            rows.append((group_of(cc), a, b))
        summary_block(xc, rows, month)
        xc = 12 + si * 3 + mi  # 오른쪽 표: 국가×리테일러
        rows = []
        for row in range(12, 47):
            cc, r = label_retailer(ws, row, col=11, ccol=10)
            a, b = ret[month]["LG"].get((cc, r), {}).get(col), ret[month]["SAMSUNG"].get((cc, r), {}).get(col)
            setv(ws, row, xc, index(a, b))
            rows.append((group_of(cc), a, b))
        summary_block(xc, rows, month)

wb.save(OUT)


def dump(level):
    return {m: {b: {"|".join(k) if isinstance(k, tuple) else k: v for k, v in level[m][b].items()} for b in BRANDS} for m in level}


with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"category": dump(cat), "retailer": dump(ret), "country": dump(country), "written": written,
               "skipped_samsung_sov": ["|".join(x) for x in skipped_sov]}, f, ensure_ascii=False, indent=1)
print("채운 칸 수:", len(written))
by_sheet = {}
for k in written:
    by_sheet[k.split("!")[0]] = by_sheet.get(k.split("!")[0], 0) + 1
for k, v in by_sheet.items():
    print("  ", k, v)
print("비교 대상이 아니어서 비운 Category SOV:", sorted(set(skipped_sov)))
