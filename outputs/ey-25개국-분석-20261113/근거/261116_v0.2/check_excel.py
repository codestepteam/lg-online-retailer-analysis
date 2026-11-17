"""검사 C: 엑셀이 실제로 계산한 값(함수 칸)이 파이썬 계산값과 같은지."""
import json, sys, re
from openpyxl import load_workbook
TSV, XLSX, CJ = sys.argv[1:4]
C = json.load(open(CJ))
grid, cur = {}, None
for line in open(TSV, encoding="utf-8").read().rstrip("\n").split("@@ROW@@"):
    if line.startswith("@@SHEET@@"):
        cur = line[9:]; grid[cur] = []; continue
    if cur: grid[cur].append(line.split("@@C@@"))
def xv(sh, r, c):
    try: s = grid[sh][r-1][c-1]
    except IndexError: return None
    if s == "": return None
    try: return float(s)
    except ValueError: return s
wb = load_workbook(XLSX)
exec(open(sys.argv[4]).read().split("# ---------- 1)")[0].split("SRC, DATA")[0])  # 이름표 사전만 가져옴
exec("COUNTRY_CODE=" + re.search(r"COUNTRY_CODE = (\{.*?\n\})", open(sys.argv[4]).read(), re.S).group(1))
exec("RETAILER_KEY=" + re.search(r"RETAILER_KEY = (\{.*?\n\})", open(sys.argv[4]).read(), re.S).group(1))
SEVEN = {"ES","FR","IT","SE","NL","PL","CZ"}; TWO = {"UK","DE"}
grp = lambda cc: "7" if cc in SEVEN else ("2" if cc in TWO else "16")
COLS = ["readiness","34","39","47","37","38","42","43","vis","1","2","3","4","catsov"]
bad = []; n = 0
def cmp(tag, got, exp, tol=1e-8):
    global n; n += 1
    if exp is None and got in (None, ""): return
    if exp is None or got is None or isinstance(got, str) or abs(got - exp) > tol: bad.append((tag, got, exp))
def avg(xs): xs=[x for x in xs if x is not None]; return sum(xs)/len(xs) if xs else None
def sm(xs): xs=[x for x in xs if x is not None]; return sum(xs) if xs else None
from decimal import Decimal, ROUND_HALF_UP
def idx(a, b): return None if a is None or b is None or b == 0 else int(Decimal(repr(a/b*100)).quantize(Decimal(1), ROUND_HALF_UP))
def check_sheet(sh, month, level, first, last, aggrow, lab, bases):
    ws = wb[sh]
    keys = {r: lab(ws, r) for r in range(first, last+1)}
    for r, key in keys.items():
        for side, cat_, base in bases:
            k = key if level == "country" else "|".join(key) + (f"|{cat_}" if cat_ else "")
            d = C[level][month][side].get(k, {})
            for col, off in (("readiness",0),("vis",8)):
                cmp(f"{sh}!{r},{base+off}", xv(sh, r, base+off), d.get(col))
            for i, col in enumerate(COLS):
                if col not in ("readiness","vis"):
                    cmp(f"{sh}!{r},{base+i} 숫자", xv(sh, r, base+i), d.get(col), 1e-9 * 100)
    groups = ["7"] if month == "8" else ["7","16","25"]
    for side, cat_, base in bases:
        for ci in range(14):
            col = base + ci
            for gi, g in enumerate(["7","16","25"]):
                rows = [r for r, k in keys.items() if g == "25" or grp(k if level=="country" else k[0]) == g]
                vals = [xv(sh, r, col) for r in rows]; vals = [v if isinstance(v, float) else None for v in vals]
                es, ea = (sm(vals), avg(vals)) if g in groups else (None, None)
                cmp(f"{sh}!합계{g},{col}", xv(sh, aggrow+gi, col), es)
                cmp(f"{sh}!평균{g},{col}", xv(sh, aggrow+3+gi, col), ea)
def lc(ws, r, c=2): return COUNTRY_CODE[str(ws.cell(row=r, column=c).value).strip()]
def lr(ws, r, c=3, cc=2):
    k = lc(ws, r, cc); return (k, RETAILER_KEY[(k, str(ws.cell(row=r, column=c).value).strip())])
for m in ("8","10"):
    check_sheet(f"{m}월_국가", m, "country", 11, 35, 5, lc, [("LG",None,3),("COMP",None,17)])
    check_sheet(f"{m}월_국가x리테일러", m, "retailer", 11, 45, 5, lr, [("LG",None,4),("COMP",None,18)])
for m in ("8","10","11"):
    check_sheet(f"{m}월_국가x리테일러x카테고리", m, "category", 12, 46, 6, lr,
                [(s, c, 4+si*42+ki*14) for si, s in enumerate(("LG","COMP")) for ki, c in enumerate(("REF","WM","DW"))])
# Summary
sh = "※ 25개국 Summary"; ws = wb[sh]
for level, first, last, lab, colf in (("country",12,36,lc,lambda si,mi:3+si*3+mi),
                                      ("retailer",12,46,lambda w,r: lr(w,r,11,10),lambda si,mi:12+si*3+mi)):
    keys = {r: lab(ws, r) for r in range(first, last+1)}
    for mi, m in enumerate(("8","10","11")):
        for si, col in enumerate(("readiness","vis")):
            xc = colf(si, mi); pairs = {}
            for r, key in keys.items():
                k = key if level == "country" else "|".join(key)
                a, b = C[level][m]["LG"].get(k,{}).get(col), C[level][m]["COMP"].get(k,{}).get(col)
                pairs[r] = (a, b)
                cmp(f"Summary!{r},{xc}", xv(sh, r, xc), idx(a, b), 0)
            for gi, g in enumerate(["7","16","25"]):
                if m == "8" and g != "7": e = None
                else:
                    ps = [pairs[r] for r, k in keys.items() if (g == "25" or grp(k if level=="country" else k[0]) == g) and None not in pairs[r]]
                    e = idx(sum(a for a,_ in ps), sum(b for _,b in ps)) if ps else None
                cmp(f"Summary!합계{g},{xc}", xv(sh, 6+gi, xc), e, 0)
                cmp(f"Summary!평균{g},{xc}", xv(sh, 9+gi, xc), e, 0)
# 엑셀 오류 값(#DIV/0! 등)이 하나라도 있는지
errs = [(s, i+1, j+1, v) for s, rows in grid.items() for i, row in enumerate(rows) for j, v in enumerate(row) if v.startswith("#") and v[:2] != "##"]
print(f"비교한 칸 {n}, 다름 {len(bad)}, 엑셀 오류 값 {len(errs)}")
for b in bad[:30]: print("  다름", b)
for e in errs[:10]: print("  오류", e)
