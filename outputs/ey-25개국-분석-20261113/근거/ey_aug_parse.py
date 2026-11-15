"""EY 8월 엑셀 Summary Detail(저장값) → {진단ID: {브랜드: {국가|리테일러|제품군: 값}}}"""
import json, sys
rows = json.load(open(sys.argv[1], encoding="utf-8"))
def col(i):
    s = ""; i += 1
    while i: i, r = divmod(i - 1, 26); s = chr(65 + r) + s
    return s
COUNTRY = {"Spain": "ES", "Italy": "IT", "Netherlands": "NL", "Sweden": "SE", "France": "FR", "Poland": "PL", "Czech": "CZ"}
RET = {("ES", "ECI"): "eci", ("ES", "Media Markt"): "mediamarkt-es", ("IT", "Media World"): "mediaworld", ("IT", "Amazon"): "amazon-it",
       ("IT", "Unieuro"): "unieuro", ("NL", "Coolblue"): "coolblue", ("NL", "Media Markt"): "mediamarkt-nl", ("SE", "ELGIGANTEN"): "elgiganten",
       ("FR", "Darty"): "darty", ("FR", "Boulanger"): "boulanger", ("PL", "Media Expert"): "media-expert", ("PL", "RTV EURO AGD"): "rtv-euro-agd",
       ("CZ", "Datart"): "datart", ("CZ", "Alza"): "alza"}
CAT = {"REF": "REF", "W/M": "WM", "DW": "DW"}
r5, r6, r7 = rows[4], rows[5], rows[6]
cols = {}; cc = ret = None
for ci in range(9, 69):
    if r5[ci]: cc = COUNTRY[r5[ci].strip()]
    if r6[ci]: ret = RET[(cc, r6[ci].strip())]
    if r7[ci]: cols[ci] = f"{cc}|{ret}|{CAT[r7[ci].strip()]}"
print(len(cols), "개 리테일러×제품군 열")
out = {}; meta = {}; cur = None
for ri in range(7, len(rows)):
    r = rows[ri]
    if r[3] is not None:
        cur = str(r[3]).strip(); meta[cur] = (ri + 1, r[7], r[8])
    if cur is None: continue
    for ci, key in cols.items():
        b = r[ci]
        if isinstance(b, str) and b.strip():
            out.setdefault(cur, {}).setdefault(b.strip().upper(), {})[key] = {"v": r[ci + 1], "cell": f"{col(ci + 1)}{ri + 1}"}
json.dump({"meta": meta, "values": out}, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
for k, m in meta.items():
    lg = out.get(k, {}).get("LG", {})
    print(k, m, "LG칸", len(lg), "예", [lg[x]["v"] for x in list(lg)[:3]])
