"""엑셀 파일만 읽어서(채우는 코드와 무관하게) 묶음 점수·리테일러 평균·국가 평균·합계/평균 줄·Summary Index를 다시 계산해 대조."""
import sys
from openpyxl import load_workbook
wb = load_workbook(sys.argv[1], data_only=True)
G7 = {"Spain", "France", "Italy", "Sweden", "Netherlands", "Poland", "Czech"}; G2 = {"United Kingdom", "Germany"}
def grp(country): return "7" if country in G7 else "2" if country in G2 else "16"
def val(ws, r, c):
    v = ws.cell(r, c).value
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None
def mean(xs):
    xs = [x for x in xs if x is not None]; return sum(xs) / len(xs) if xs else None
def tot(xs):
    xs = [x for x in xs if x is not None]; return sum(xs) if xs else None
res = {}
def chk(name, got, exp, where):
    s = res.setdefault(name, [0, 0, []]); s[0] += 1
    if (got is None) != (exp is None) or (got is not None and abs(got - exp) > 1e-9):
        s[1] += 1; s[2].append((where, got, exp))
def lab(ws, r, c): 
    v = ws.cell(r, c).value; return v.strip() if isinstance(v, str) else v
def aggregates(ws, name, first_agg, rows, labels, cols):
    for c in cols:
        for i, (g, f) in enumerate([("7", tot), ("16", tot), ("25", tot), ("7", mean), ("16", mean), ("25", mean)]):
            xs = [val(ws, r, c) for r in rows if g == "25" or grp(labels[r]) == g]
            chk(name + " 합계·평균 줄", val(ws, first_agg + i, c), f(xs), f"{ws.title}!{ws.cell(first_agg + i, c).coordinate}")
store = {}   # (월, 단위) -> {라벨: {(브랜드, 지표번호): 값}}
for m in ("8", "10", "11"):
    ws = wb[f"{m}월_국가x리테일러x카테고리"]; rows = range(12, 47)
    country = {r: lab(ws, r, 2) for r in rows}; rname = {r: (lab(ws, r, 2), lab(ws, r, 3)) for r in rows}
    for b in (0, 1):
        for c in (0, 1, 2):
            base = 4 + b * 42 + c * 14
            for r in rows:
                five = [val(ws, r, base + k) for k in range(1, 6)]
                chk(f"{m}월 제품군 PDP Readiness", val(ws, r, base), sum(five) / 5 if all(x is not None for x in five) else None, f"{ws.title}!{ws.cell(r, base).coordinate}")
                a, s = val(ws, r, base + 12), val(ws, r, base + 13)
                chk(f"{m}월 제품군 Visibility", val(ws, r, base + 8), (a + s) / 2 if a is not None and s is not None else None, f"{ws.title}!{ws.cell(r, base + 8).coordinate}")
    aggregates(ws, f"{m}월 제품군", 6, rows, country, range(4, 4 + 84))
    rv = {rname[r]: {(b, k): mean([val(ws, r, 4 + b * 42 + c * 14 + k) for c in (0, 1, 2)]) for b in (0, 1) for k in range(14)} for r in rows}
    store[(m, "ret")] = rv
    cv = {}
    for cn in dict.fromkeys(country.values()):
        cv[cn] = {(b, k): mean([rv[rn][(b, k)] for rn in rv if rn[0] == cn]) for b in (0, 1) for k in range(14)}
    store[(m, "cty")] = cv
    if m == "11": continue
    wr = wb[f"{m}월_국가x리테일러"]; rr = range(11, 46)
    for r in rr:
        key = (lab(wr, r, 2), lab(wr, r, 3)); assert key == rname[r + 1], (key, rname[r + 1])
        for b in (0, 1):
            for k in range(14):
                chk(f"{m}월 리테일러 = 제품군 평균", val(wr, r, 4 + b * 14 + k), rv[key][(b, k)], f"{wr.title}!{wr.cell(r, 4 + b * 14 + k).coordinate}")
    aggregates(wr, f"{m}월 리테일러", 5, rr, {r: lab(wr, r, 2) for r in rr}, range(4, 32))
    wc = wb[f"{m}월_국가"]; cr = range(11, 36)
    for r in cr:
        cn = lab(wc, r, 2); assert cn in cv, cn
        for b in (0, 1):
            for k in range(14):
                chk(f"{m}월 국가 = 리테일러 평균", val(wc, r, 3 + b * 14 + k), cv[cn][(b, k)], f"{wc.title}!{wc.cell(r, 3 + b * 14 + k).coordinate}")
    aggregates(wc, f"{m}월 국가", 5, cr, {r: lab(wc, r, 2) for r in cr}, range(3, 31))
ws = wb["※ 25개국 Summary"]
def index(l, s): return None if l is None or not s else float(int(round(l / s * 100)))
for unit, lcol, c0, rows, keyf in (("cty", 2, 3, range(12, 37), lambda r: lab(ws, r, 2)), ("ret", 11, 12, range(12, 47), None)):
    keys = {}; last = None
    for r in rows:
        if unit == "ret":
            if lab(ws, r, 10): last = lab(ws, r, 10)
            keys[r] = (last, lab(ws, r, 11))
        else: keys[r] = keyf(r)
        assert keys[r] in store[("10", unit)], keys[r]
    for si, k in enumerate((0, 8)):
        for mi, m in enumerate(("8", "10", "11")):
            col = c0 + si * 3 + mi
            pairs = {r: (store[(m, unit)][keys[r]][(0, k)], store[(m, unit)][keys[r]][(1, k)]) for r in rows}
            for r in rows:
                chk("Summary Index(국가·리테일러 줄)", val(ws, r, col), index(*pairs[r]), f"Summary!{ws.cell(r, col).coordinate}")
            for i, g in enumerate(["7", "16", "25", "7", "16", "25"]):
                ok = [p for r, p in pairs.items() if (g == "25" or grp(keys[r] if unit == "cty" else keys[r][0]) == g) and p[0] is not None and p[1]]
                exp = index(sum(p[0] for p in ok), sum(p[1] for p in ok)) if ok else None
                chk("Summary 합계·평균 줄", val(ws, 6 + i, col), exp, f"Summary!{ws.cell(6 + i, col).coordinate}")
filled = sum(1 for w in wb.worksheets for row in w.iter_rows() for c in row if isinstance(c.value, (int, float)) and not isinstance(c.value, bool))
print("숫자가 들어 있는 칸(머리글 숫자 포함 가능):", filled)
for name, (n, bad, ex) in res.items():
    import re; print(f"{name}: 검사 {n} / 불일치 {bad}", sorted({re.sub(r"[A-Z]+", "", w.split("!")[1]) for w, _g, _e in ex}) if bad else "", "파일 쪽이 전부 빈칸" if bad and all(g is None for _w, g, _e in ex) else "")
# 범위 검사
bad = []
for w in wb.worksheets:
    if "월_" not in w.title: continue
    for row in w.iter_rows(min_row=5):
        for c in row:
            if isinstance(c.value, (int, float)) and not isinstance(c.value, bool) and c.value < 0: bad.append((w.title, c.coordinate, c.value))
print("음수 칸:", len(bad), bad[:5])
