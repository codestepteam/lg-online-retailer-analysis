"""EY '25개국 분석' 엑셀 사본에 값을 채운다. 원본 파일은 건드리지 않는다.

사용: python -I fill_workbook.py <원본.xlsx> <자료 폴더> <결과.xlsx> <계산값.json>

2026-11-16 EY 추가 요청 반영
1. 경쟁사: 이집트 Cairo Sales = TOSHIBA, 호주 Appliance Online = HAIER, 대만 Momoshop = PANASONIC.
   나머지 리테일러는 삼성. 엑셀의 '경쟁사_S사' 칸에 넣고, 합계와 평균 줄에도 포함한다. 칸 메모는 달지 않는다(사용자 요청).
2. 리테일러와 국가 값은 '평균의 평균'이 아니라 아래 카테고리 칸들의 분자 합 ÷ 분모 합으로 다시 구한다.
   - 상품 상세 7개 항목: 통과 수 합 ÷ 판정 수 합 × 100
   - ID4: 검색어별 점수 합 ÷ 점수가 있는 검색어 수 합
   - Category SOV: 검색어별 값 합 ÷ 검색어 수 합
   - ID1~3 (순위 점수 합이라 분모가 없음): EY 답변(2026-11-16)대로 1번 방식.
     리테일러 = 카테고리 칸 단순 평균, 국가 = 그 나라 리테일러×카테고리 칸 전체의 단순 평균.
3. PDP Readiness, Visibility, 합계와 평균 줄, Summary의 Index는 엑셀 함수로 적는다.
   11월은 국가 시트가 없어 Summary의 11월 Index는 숫자로 적는다.
4. (EY 추가 요청 2026-11-16) Visibility 옆에 Search SOV와 Category SOV를 모든 탭에 넣는다.
   - Summary 외 탭: Visibility 바로 뒤에 'Search SOV', 'Category SOV' 두 열을 끼워 넣는다.
     값은 같은 줄의 ID4 칸, Dashboard Only 칸을 그대로 가리키는 함수다 (대시보드의 Search SOV = ID4,
     Category SOV = Dashboard Only). 그래서 한 묶음이 14칸에서 16칸이 된다.
   - Summary: 국가 표와 국가X리테일러 표의 Visibility 뒤에 'Search SOV', 'Category SOV' Index(8월, 10월, 11월)를 넣는다.
   원본 양식에는 이 열이 없으므로, 원본을 읽은 직후 add_sov_columns()가 열을 끼워 넣고 서식을 옆 Visibility 열에서 복사한다.
"""
import copy
import json
import math
import re
import sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter as L, column_index_from_string
from openpyxl.worksheet.cell_range import CellRange

SRC, DATA, OUT, OUT_JSON = sys.argv[1:5]

COLS = ["readiness", "34", "39", "47", "37", "38", "42", "43", "vis", "ssov", "csov", "1", "2", "3", "4", "catsov"]
W = len(COLS)                     # 한 묶음 칸 수 (16)
FORMULA_COLS = ("readiness", "vis", "ssov", "csov")   # 함수로 적는 칸
OFF = {c: i for i, c in enumerate(COLS)}
SUMMARY_METRICS = [("readiness", "readiness"), ("vis", "vis"), ("ssov", "4"), ("csov", "catsov")]   # (Summary 열, 값 키)
PDP5 = ["34", "39", "47", "37", "38"]
PDP7 = ["34", "39", "47", "37", "38", "42", "43"]
RANK = ["1", "2", "3"]            # 분모 없는 순위 점수 합
POOLED = PDP7 + ["4", "catsov"]   # 분자 합 ÷ 분모 합
CATS = ["REF", "WM", "DW"]
SIDES = ["LG", "COMP"]            # COMP = 엑셀의 '경쟁사_S사' 칸

# 리테일러별 경쟁사 (EY 요청 2026-11-16). 나머지는 SAMSUNG.
COMPETITOR = {("EG", "cairo-sales"): "TOSHIBA", ("AU", "appliance-online"): "HAIER", ("TW", "momoshop"): "PANASONIC"}

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
    return None if v is None else float(v)


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def side_of(brand, cc, ret):
    """이 브랜드 값이 그 리테일러의 'LG' 칸인지 '경쟁사' 칸인지. 어느 쪽도 아니면 None."""
    brand = brand.upper()
    if brand == "LG":
        return "LG"
    comp = COMPETITOR.get((cc.upper(), rkey(ret)), "SAMSUNG")
    return "COMP" if brand == comp else None


# ---------- 1) 카테고리 칸: cat[월][쪽][(국가, 리테일러, 카테고리)][칸] = 값, frac[...][칸] = (분자, 분모) ----------
cat = {m: {s: {} for s in SIDES} for m in ("8", "10", "11")}
frac = {m: {s: {} for s in SIDES} for m in ("8", "10", "11")}
brand_of = {m: {} for m in cat}   # (국가, 리테일러) -> 경쟁사 칸에 들어간 실제 브랜드


# 건조기(DRY)는 세탁기(WM) 칸에 합친다 (사용자 2026-11-17: "세탁기에 건조기도 포함").
# 같은 칸에 두 번째 값이 오면: 분자 분모가 있으면 분자 합 ÷ 분모 합, 없으면(ID1~3 점수 합) 그냥 더한다.
MERGE_INTO = {"DRY": "WM"}
seen = set()   # (월, 쪽, 칸 키, 항목, 원래 카테고리): 같은 원래 카테고리가 두 번 오면 자료 중복이라 멈춘다.


def put(month, brand, cc, ret, category, col, value, nd=None):
    side = side_of(brand, cc, ret)
    if side is None or value is None:
        return
    orig = category.upper()
    key = (cc.upper(), rkey(ret), MERGE_INTO.get(orig, orig))
    tag = (month, side, key, col, orig)
    assert tag not in seen, tag
    seen.add(tag)
    if side == "COMP":
        brand_of[month][key[:2]] = brand.upper()
    cell = cat[month][side].setdefault(key, {})
    fr = frac[month][side].setdefault(key, {})
    if col in cell:
        old_nd = fr.get(col)
        assert (old_nd is None) == (nd is None), tag
        if nd is None:
            cell[col] += value
        else:
            n, d = old_nd[0] + nd[0], old_nd[1] + nd[1]
            fr[col] = (n, d)
            assert d > 0, tag
            cell[col] = n / d
        return
    cell[col] = value
    if nd is not None:
        fr[col] = nd


# 8월 상품 상세: EY 8월 엑셀과 같은 조건의 대시보드 8월 전용 계산(first_report) — 통과 수 ÷ 대상 수.
# 대상 0건이면 EY 엑셀과 같이 0, ID43만 빈칸.
for r in load("aug_first_report.jsonl"):
    n, tot_ = int(r["n"]), int(r["total"])
    aid = str(r["assessment_id"])
    if tot_ > 0:
        v = n / tot_ * 100
    else:
        v = None if aid == "43" else 0.0
    put("8", r["brand"], r["country"], r["retailer"], r["category"], aid, v, (n * 100, tot_))

# 10월 상품 상세: operation_scores. value = pass_count ÷ completed.
oct_pdp = load("oct_lg.jsonl") + load("oct_brand_SAMSUNG.jsonl") + load("oct_comp.jsonl")
for r in oct_pdp:
    brand = "LG" if r["brand_scope"] == "lg" else r["brand_scope"].split(":", 1)[1].split()[0]
    v = num(r["value"])
    p, c = float(r["pass_count"] or 0), int(r["completed"] or 0)
    if v is None:
        assert c == 0, r
    else:
        assert c > 0 and abs(v - p / c) < 1e-9, r
    put("10", brand, r["country"], r["retailer"], r["category"], str(r["assessment_id"]),
        None if v is None else v * 100, (p * 100, c))

# 10·11월 검색 노출: ID1~3 = 검색어별 점수 합, ID4 = 검색어별 점수 평균(= 합 ÷ 점수가 있는 검색어 수)
for month, fn in {"10": "oct_plp_lg.jsonl", "11": "nov_plp_dev.jsonl"}.items():
    for r in load(fn):
        scored = int(r["scored"])
        if scored == 0:
            continue
        s = num(r["sum_score"])
        if r["assessment_id"] == "4":
            assert abs(num(r["avg_score"]) - s / scored) < 1e-9, r
            put(month, r["brand"], r["country"], r["retailer"], r["category"], "4", s / scored, (s, scored))
        else:
            put(month, r["brand"], r["country"], r["retailer"], r["category"], r["assessment_id"], s)

# 8월 검색 노출 (기준 자료의 검색어별 값)
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
for (brand, cc, ret_, category, aid), vals in aug.items():
    if aid == "4":
        put("8", brand, cc, ret_, category, aid, sum(vals) / len(vals), (sum(vals), len(vals)))
    else:
        put("8", brand, cc, ret_, category, aid, sum(vals))

# Category SOV: 검색어별 값의 평균 = 검색어별 값 합 ÷ 검색어 수
sov = []
for fn, ym, month in (("catsov_lg.jsonl", "2026-10", "10"), ("catsov_dev.jsonl", "2026-11", "11")):
    for r in load(fn):
        if r["ym"] == ym:
            v, k = num(r["category_sov"]), int(r["keywords"])
            sov.append((month, r["brand"], r["country"], r["retailer"], r["category"], v, (v * k, k)))
augsov = {}
for r in load("aug_catsov_lg.jsonl"):
    augsov.setdefault((r["brand"], r["country"], r["retailer"], r["category"]), []).append(int(r["top10_count"]) * 10.0)
for (brand, cc, ret_, category), vals in augsov.items():
    sov.append(("8", brand, cc, ret_, category, sum(vals) / len(vals), (sum(vals), len(vals))))
skipped_sov = []
for month, brand, cc, ret_, category, v, nd in sov:
    side = side_of(brand, cc, ret_)
    if side is None:
        continue
    key = (cc.upper(), rkey(ret_), category.upper())
    # 대시보드와 같은 기준: 그 칸에 검색 노출 결과가 있는 브랜드이거나, 상위 10개에 한 번이라도 보인 브랜드만 적는다.
    if not any(c in cat[month][side].get(key, {}) for c in ("1", "2", "3", "4")) and not (v and v > 0):
        skipped_sov.append((month, brand.upper()) + key)
        continue
    put(month, brand, cc, ret_, category, "catsov", v, nd)

# 카테고리 칸의 묶음 점수 (엑셀에서는 함수로 적지만, 검사와 11월 Summary 숫자에 쓰려고 같이 계산)
def bundle(d):
    if all(c in d for c in PDP5):
        d["readiness"] = sum(d[c] for c in PDP5) / 5
    if "4" in d and "catsov" in d:
        d["vis"] = (d["4"] + d["catsov"]) / 2


for month in cat:
    for side in SIDES:
        for d in cat[month][side].values():
            bundle(d)


# ---------- 2) 카테고리 칸 → 리테일러, 국가 ----------
def pool(keys, month, side):
    """keys: 합칠 카테고리 칸들. 분자 합 ÷ 분모 합, ID1~3은 칸 단순 평균."""
    d = {}
    for col in POOLED:
        nds = [frac[month][side].get(k, {}).get(col) for k in keys]
        nds = [x for x in nds if x is not None]
        if not nds:
            continue
        nsum, dsum = sum(x[0] for x in nds), sum(x[1] for x in nds)
        if dsum > 0:
            d[col] = nsum / dsum
        elif month == "8" and col in PDP7 and col != "43":
            d[col] = 0.0   # 8월 대상 0건 = 0 (EY 8월 엑셀 표기와 같게)
    for col in RANK:
        v = mean([cat[month][side].get(k, {}).get(col) for k in keys])
        if v is not None:
            d[col] = v
    bundle(d)
    return d


ret = {m: {s: {} for s in SIDES} for m in cat}
country = {m: {s: {} for s in SIDES} for m in cat}
for month in cat:
    for side in SIDES:
        keys = [k for k in cat[month][side] if k[2] in CATS]
        for cc, r in {k[:2] for k in keys}:
            ret[month][side][(cc, r)] = pool([k for k in keys if k[:2] == (cc, r)], month, side)
        for cc in {k[0] for k in keys}:
            country[month][side][cc] = pool([k for k in keys if k[0] == cc], month, side)


def index(lg, ss):
    if lg is None or ss is None or ss == 0:
        return None
    # 엑셀 ROUND와 같게 .5는 올림 (파이썬 round는 짝수 쪽으로 감).
    # 87.49999999999999처럼 계산 오차로 .5 바로 아래가 된 값은 엑셀처럼 87.5로 보고 올림하도록 소수 10자리에서 먼저 정리한다.
    return math.floor(round(lg / ss * 100, 10) + 0.5)


# ---------- 3) 엑셀 채우기 ----------
wb = load_workbook(SRC)


def insert_cols_keep(ws, idx, amount):
    """idx 칸 앞에 amount 칸을 끼워 넣는다. 병합 칸과 열 너비도 같이 민다 (openpyxl은 칸 값과 서식만 민다)."""
    merges = [CellRange(str(m)) for m in ws.merged_cells.ranges]
    for m in merges:
        ws.unmerge_cells(str(m))
    # 열 너비: 범위로 묶인 정보(예: AE~XFD)를 200열까지는 한 칸씩 풀고, 그 뒤는 꼬리 범위로 둔다.
    # 범위째로 밀면 다른 열 정보와 겹쳐 엑셀이 파일 복구 창을 띄운다.
    LIMIT = 200
    per, tail = {}, []
    for key, dim in list(ws.column_dimensions.items()):
        lo = dim.min or column_index_from_string(key)
        hi = dim.max or lo
        for c in range(lo, min(hi, LIMIT) + 1):
            per[c] = dim
        if hi > LIMIT:
            tail.append((max(lo, LIMIT + 1), hi, dim))
        del ws.column_dimensions[key]
    ws.insert_cols(idx, amount)

    def put(lo, hi, dim):
        d = copy.copy(dim)
        d.min, d.max, d.index = lo, hi, L(lo)
        ws.column_dimensions[L(lo)] = d

    for c, dim in sorted(per.items()):
        nc = c + amount if c >= idx else c
        put(nc, nc, dim)
    for lo, hi, dim in tail:
        if lo + amount <= 16384:
            put(lo + amount, min(hi + amount, 16384), dim)
    for m in merges:
        if m.min_col >= idx:
            m.shift(col_shift=amount)
        elif m.max_col >= idx:
            m.expand(right=amount)
        ws.merge_cells(str(m))


def copy_col_style(ws, src_col, dst_col, max_row):
    # 열 전체 서식(양식은 모든 열을 흰 바탕으로 칠해 둠)과 너비를 함께 옮긴다. 너비만 옮기면 새 열에 눈금선이 보인다.
    src_dim = ws.column_dimensions[L(src_col)]
    dst_dim = ws.column_dimensions[L(dst_col)]
    dst_dim.width = src_dim.width
    dst_dim._style = copy.copy(src_dim._style)
    # 원래 열에 칸이 있는 줄만 옮긴다. 없는 줄에 빈 칸을 만들면 그 칸이 열 서식을 덮어 눈금선이 보인다.
    for r in range(1, max_row + 1):
        if (r, src_col) in ws._cells:
            ws.cell(row=r, column=dst_col)._style = copy.copy(ws._cells[(r, src_col)]._style)


def add_sov_columns(wb):
    # Summary 외 탭: Visibility 열(묶음 시작 + 8) 뒤에 2칸. 오른쪽 묶음부터 넣어야 앞 번호가 안 바뀐다.
    layouts = [("8월_국가", 3, 2, 3), ("10월_국가", 3, 2, 3), ("8월_국가x리테일러", 4, 2, 3), ("10월_국가x리테일러", 4, 2, 3)]
    layouts += [(f"{m}월_국가x리테일러x카테고리", 4, 6, 4) for m in ("8", "10", "11")]
    for title, first_base, n_blocks, head_row in layouts:
        ws = wb[title]
        max_row = ws.max_row
        for b in reversed(range(n_blocks)):
            vis = first_base + b * 14 + 8
            assert ws.cell(row=head_row, column=vis).value == "Visibility", (title, vis)
            assert ws.cell(row=head_row, column=vis + 4).value == "ID4", (title, vis)
            insert_cols_keep(ws, vis + 1, 2)
            for k, name in enumerate(("Search SOV", "Category SOV")):
                c = vis + 1 + k
                copy_col_style(ws, vis, c, max_row)
                ws.cell(row=head_row, column=c).value = name
                ws.merge_cells(start_row=head_row, start_column=c, end_row=head_row + 1, end_column=c)
    # Summary: 국가 표 Visibility(F~H) 뒤에 6칸을 끼워 넣고, 국가X리테일러 표는 맨 끝(밀린 뒤 U~W 다음)에 6칸을 붙인다.
    ws = wb["※ 25개국 Summary"]
    max_row = ws.max_row
    assert ws["F4"].value == "Visibility" and ws["O4"].value == "Visibility"
    insert_cols_keep(ws, 9, 6)
    for vis_first in (6, 21):   # 국가 표 F, 국가X리테일러 표 U
        for k, name in enumerate(("Search SOV", "Category SOV")):
            first = vis_first + 3 + k * 3
            for mi in range(3):
                copy_col_style(ws, vis_first + mi, first + mi, max_row)
                ws.cell(row=5, column=first + mi).value = ws.cell(row=5, column=vis_first + mi).value
            ws.cell(row=4, column=first).value = name
            ws.merge_cells(start_row=4, start_column=first, end_row=4, end_column=first + 2)


add_sov_columns(wb)
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


def write_aggs(ws, first_agg_row, col, spans, month):
    """spans: {'7': (시작 줄, 끝 줄), '16': ..., '25': ...} — 합계 줄은 SUM, 평균 줄은 AVERAGE 함수."""
    assert [ws.cell(row=first_agg_row + i, column=2).value for i in range(6)] == AGG_LABELS, ws.title
    cl = L(col)
    for i, g in enumerate(["7", "16", "25"]):
        if g not in agg_groups(month):
            continue
        a, b = spans[g]
        rng = f"{cl}{a}:{cl}{b}"
        setv(ws, first_agg_row + i, col, f'=IF(COUNT({rng})=0,"",SUM({rng}))', "0.0")
        setv(ws, first_agg_row + 3 + i, col, f'=IF(COUNT({rng})=0,"",AVERAGE({rng}))', "0.0")


def spans_of(ws, first_row, last_row, cc_of):
    rows = {g: [r for r in range(first_row, last_row + 1) if g == "25" or group_of(cc_of(ws, r)) == g]
            for g in ("7", "16", "25")}
    out = {}
    for g, rs in rows.items():
        assert rs == list(range(rs[0], rs[-1] + 1)), (ws.title, g, rs)   # 묶음 줄이 붙어 있어야 범위 함수가 맞다
        out[g] = (rs[0], rs[-1])
    return out


def label_country(ws, row, col=2):
    return COUNTRY_CODE[str(ws.cell(row=row, column=col).value).strip()]


def label_retailer(ws, row, col=3, ccol=2):
    cc = COUNTRY_CODE[str(ws.cell(row=row, column=ccol).value).strip()]
    return cc, RETAILER_KEY[(cc, str(ws.cell(row=row, column=col).value).strip())]


def fill_block(ws, row, base, d):
    """한 줄의 16칸 묶음. base = 'PDP Readiness Score' 칸 번호. d = 그 줄의 값."""
    ci = {c: base + i for i, c in enumerate(COLS)}
    for col in COLS:
        if col in FORMULA_COLS:
            continue
        setv(ws, row, ci[col], d.get(col), "0.0")
    a, b = L(ci["34"]), L(ci["38"])
    rng = f"{a}{row}:{b}{row}"
    setv(ws, row, ci["readiness"], f'=IF(COUNT({rng})=5,AVERAGE({rng}),"")', "0.0")
    i4, sv = f"{L(ci['4'])}{row}", f"{L(ci['catsov'])}{row}"
    setv(ws, row, ci["vis"], f'=IF(AND(ISNUMBER({i4}),ISNUMBER({sv})),({i4}+{sv})/2,"")', "0.0")
    setv(ws, row, ci["ssov"], f'=IF(ISNUMBER({i4}),{i4},"")', "0.0")   # Search SOV = ID4
    setv(ws, row, ci["csov"], f'=IF(ISNUMBER({sv}),{sv},"")', "0.0")   # Category SOV = Dashboard Only


ref_cells = {}   # Summary 함수가 가리킬 칸: (월, 'country'|'retailer', 키, Summary 열, 쪽) -> "시트!칸"

for month in ("8", "10"):
    ws = wb[f"{month}월_국가"]
    sp = spans_of(ws, 11, 35, label_country)
    for row in range(11, 36):
        cc = label_country(ws, row)
        for si, side in enumerate(SIDES):
            base = 3 + si * W
            d = country[month][side].get(cc, {})
            fill_block(ws, row, base, d)
            for col, _ in SUMMARY_METRICS:
                ref_cells[(month, "country", cc, col, side)] = f"'{ws.title}'!{L(base + OFF[col])}{row}"
    for si in range(2):
        for ci in range(W):
            write_aggs(ws, 5, 3 + si * W + ci, sp, month)

    ws = wb[f"{month}월_국가x리테일러"]
    sp = spans_of(ws, 11, 45, lambda w, r: label_retailer(w, r)[0])
    for row in range(11, 46):
        key = label_retailer(ws, row)
        for si, side in enumerate(SIDES):
            base = 4 + si * W
            d = ret[month][side].get(key, {})
            fill_block(ws, row, base, d)
            for col, _ in SUMMARY_METRICS:
                ref_cells[(month, "retailer", key, col, side)] = f"'{ws.title}'!{L(base + OFF[col])}{row}"
    for si in range(2):
        for ci in range(W):
            write_aggs(ws, 5, 4 + si * W + ci, sp, month)

for month in ("8", "10", "11"):
    ws = wb[f"{month}월_국가x리테일러x카테고리"]
    sp = spans_of(ws, 12, 46, lambda w, r: label_retailer(w, r)[0])
    for row in range(12, 47):
        cc, r = label_retailer(ws, row)
        for si, side in enumerate(SIDES):
            for ki, category in enumerate(CATS):
                base = 4 + si * 3 * W + ki * W
                d = cat[month][side].get((cc, r, category), {})
                fill_block(ws, row, base, d)
    for si in range(2):
        for ki in range(3):
            for ci in range(W):
                write_aggs(ws, 6, 4 + si * 3 * W + ki * W + ci, sp, month)

# Summary: Index = LG ÷ 경쟁사 × 100 (정수로 반올림)
# 8·10월: 국가 시트 / 국가x리테일러 시트의 PDP Readiness, Visibility 칸을 가리키는 함수.
# 11월: 국가 시트가 없으므로 숫자.
# 합계·평균 줄: LG와 경쟁사 값이 둘 다 있는 줄만 모아 (LG 합 ÷ 경쟁사 합 × 100). 합계 줄과 평균 줄은 같은 값.
ws = wb["※ 25개국 Summary"]
assert [ws.cell(row=6 + i, column=2).value for i in range(6)] == AGG_LABELS


def idx_formula(a, b):
    return f'=IF(AND(ISNUMBER({a}),ISNUMBER({b})),IFERROR(ROUND({a}/{b}*100,0),""),"")'


def pair_formula(la, sa):
    both = f"--ISNUMBER({la}),--ISNUMBER({sa})"
    return f'=IFERROR(ROUND(SUMPRODUCT({both},{la})/SUMPRODUCT({both},{sa})*100,0),"")'


def summary_part(level, label_fn, first, last, xc_of):
    sp = spans_of(ws, first, last, lambda w, r: label_fn(w, r) if level == "country" else label_fn(w, r)[0])
    for mi, month in enumerate(("8", "10", "11")):
        for si, (col, vkey) in enumerate(SUMMARY_METRICS):
            xc = xc_of(si, mi)
            src = country if level == "country" else ret
            pairs_by_row = {}
            for row in range(first, last + 1):
                key = label_fn(ws, row)
                a, b = src[month]["LG"].get(key, {}).get(vkey), src[month]["COMP"].get(key, {}).get(vkey)
                pairs_by_row[row] = (a, b)
                if month == "11":
                    setv(ws, row, xc, index(a, b))
                else:
                    ra, rb = ref_cells[(month, level, key, col, "LG")], ref_cells[(month, level, key, col, "COMP")]
                    sheet_row = int(re.search(r"(\d+)$", ra).group(1))
                    assert sheet_row == row - 1, (ra, row)   # Summary 줄과 시트 줄의 나라·리테일러가 같은지
                    setv(ws, row, xc, idx_formula(ra, rb))
            for i, g in enumerate(["7", "16", "25"]):
                if g not in agg_groups(month):
                    continue
                a0, b0 = sp[g]
                if month == "11":
                    pairs = [pairs_by_row[r] for r in range(a0, b0 + 1) if None not in pairs_by_row[r]]
                    v = index(sum(x for x, _ in pairs), sum(y for _, y in pairs)) if pairs else None
                    setv(ws, 6 + i, xc, v)
                    setv(ws, 9 + i, xc, v)
                else:
                    ra, rb = ref_cells[(month, level, label_fn(ws, a0), col, "LG")], ref_cells[(month, level, label_fn(ws, a0), col, "COMP")]
                    rz, sz = ref_cells[(month, level, label_fn(ws, b0), col, "LG")], ref_cells[(month, level, label_fn(ws, b0), col, "COMP")]
                    la = f"{ra}:{rz.split('!')[1]}"
                    sa = f"{rb}:{sz.split('!')[1]}"
                    setv(ws, 6 + i, xc, pair_formula(la, sa))
                    setv(ws, 9 + i, xc, pair_formula(la, sa))


summary_part("country", label_country, 12, 36, lambda si, mi: 3 + si * 3 + mi)
summary_part("retailer", lambda w, r: label_retailer(w, r, col=17, ccol=16), 12, 46, lambda si, mi: 18 + si * 3 + mi)

wb.calculation.fullCalcOnLoad = True   # 엑셀이 열 때 함수를 모두 다시 계산
wb.save(OUT)


def dump(level):
    return {m: {s: {"|".join(k) if isinstance(k, tuple) else k: v for k, v in level[m][s].items()} for s in SIDES} for m in level}


with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"category": dump(cat), "retailer": dump(ret), "country": dump(country),
               "competitor_brand": {m: {"|".join(k): v for k, v in brand_of[m].items()} for m in brand_of},
               "written": written, "skipped_sov": ["|".join(x) for x in skipped_sov]}, f, ensure_ascii=False, indent=1)
print("채운 칸 수:", len(written), "/ 그중 함수:", sum(1 for v in written.values() if isinstance(v, str) and v.startswith("=")))
by_sheet = {}
for k in written:
    by_sheet[k.split("!")[0]] = by_sheet.get(k.split("!")[0], 0) + 1
for k, v in by_sheet.items():
    print("  ", k, v)
print("경쟁사 칸에 들어간 삼성 외 브랜드:", {m: {k: v for k, v in brand_of[m].items() if v != "SAMSUNG"} for m in brand_of})
