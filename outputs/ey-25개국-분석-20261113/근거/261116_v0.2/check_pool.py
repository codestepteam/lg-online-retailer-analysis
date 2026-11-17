"""검사 B: 원천 jsonl에서 바로 리테일러, 국가 값을 다시 계산해 채우기 코드의 값과 비교 (채우기 코드를 쓰지 않음)."""
import json, sys
from collections import defaultdict
D, NEW = sys.argv[1], json.load(open(sys.argv[2]))
COMP = {("EG","cairo-sales"):"TOSHIBA",("AU","appliance-online"):"HAIER",("TW","momoshop"):"PANASONIC"}
def rows(f): return [json.loads(l) for l in open(f"{D}/{f}") if l.strip()]
def side(b, cc, r):
    b = b.upper().split()[0].replace("BRAND:","")
    if b in ("LG",): return "LG"
    return "COMP" if b == COMP.get((cc, r.replace("_","-")), "SAMSUNG") else None
N = defaultdict(float); Dn = defaultdict(float)   # (월, 쪽, 단위, 키, 칸)
R = defaultdict(list)
def add(m, s, cc, r, col, n, d):
    for lvl, key in (("retailer", f"{cc}|{r}"), ("country", cc)):
        N[(m,s,lvl,key,col)] += n; Dn[(m,s,lvl,key,col)] += d
# 10월 PDP
for f in ("oct_lg.jsonl","oct_brand_SAMSUNG.jsonl","oct_comp.jsonl"):
    for x in rows(f):
        if x["category"] not in ("REF","WM","DW"): continue
        s = side(x["brand_scope"].replace("brand:","") if x["brand_scope"]!="lg" else "LG", x["country"], x["retailer"])
        if s: add("10", s, x["country"], x["retailer"].replace("_","-"), str(x["assessment_id"]), float(x["pass_count"] or 0)*100, int(x["completed"] or 0))
# 8월 PDP: 통과 수 x 100 / 대상 수 (대상 0건 합이면 0, ID43만 빈칸)
zero8 = set()
for x in rows("aug_first_report.jsonl"):
    if x["category"] not in ("REF","WM","DW"): continue
    s = side(x["brand"], x["country"], x["retailer"])
    if s: add("8", s, x["country"], x["retailer"].replace("_","-"), str(x["assessment_id"]), int(x["n"])*100, int(x["total"]))
# 8월 ID4: 검색어별 % 합 / 검색어 수
for x in rows("aug_plp_lg.jsonl"):
    if x["category"] not in ("REF","WM","DW") or x["assessment_id"] != "4": continue
    s = side(x["brand"], x["country"], x["retailer"])
    if s: add("8", s, x["country"], x["retailer"].replace("_","-"), "4", float(str(x["raw"]).strip().strip('"').strip().rstrip("%")), 1)
# 10, 11월 ID4 + ID1~3 칸값
cellrank = defaultdict(list)
for m, f in (("10","oct_plp_lg.jsonl"),("11","nov_plp_dev.jsonl")):
    for x in rows(f):
        if x["category"] not in ("REF","WM","DW") or int(x["scored"]) == 0: continue
        s = side(x["brand"], x["country"], x["retailer"])
        if not s: continue
        r = x["retailer"].replace("_","-")
        if x["assessment_id"] == "4": add(m, s, x["country"], r, "4", float(x["sum_score"]), int(x["scored"]))
        else:
            for lvl, key in (("retailer", f"{x['country']}|{r}"), ("country", x["country"])):
                cellrank[(m,s,lvl,key,x["assessment_id"])].append(float(x["sum_score"]))
res = {k: N[k]/Dn[k] for k in N if Dn[k] > 0}
res.update({k: 0.0 for k in N if Dn[k] == 0 and k[0] == "8" and k[4] != "43"})
res.update({k: sum(v)/len(v) for k, v in cellrank.items()})
cnt = bad = 0; seen = set()
for (m,s,lvl,key,col), v in res.items():
    w = NEW[lvl][m][s].get(key, {}).get(col)
    cnt += 1; seen.add((m,s,lvl,key,col))
    if w is None or abs(w - v) > 1e-9:
        bad += 1; print("다름", m, s, lvl, key, col, v, w)
# 반대 방향: 채우기 코드에만 있는 값 (PDP7, ID1~4, 10/11월)
extra = 0
for lvl in ("retailer","country"):
    for m in ("10","11"):
        for s in ("LG","COMP"):
            for key, d in NEW[lvl][m][s].items():
                for col in d:
                    if col in ("34","39","47","37","38","42","43","1","2","3","4") and (m,s,lvl,key,col) not in seen:
                        if m == "11" and col not in ("1","2","3","4"): continue
                        extra += 1; print("코드에만 있음", m, s, lvl, key, col, d[col])
print(f"비교한 값 {cnt}, 다름 {bad}, 코드에만 있음 {extra}")
