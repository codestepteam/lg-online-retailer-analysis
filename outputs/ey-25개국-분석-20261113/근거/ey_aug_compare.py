"""8월: 채운 값(파일) vs EY 8월 엑셀 Summary Detail 저장값 vs 대시보드 8월 전용 계산. 제품군 단위 전부."""
import json, sys, csv
S = sys.argv[1]
mine = json.load(open(f"{S}/data/computed.json", encoding="utf-8"))["category"]["8"]
ey = json.load(open(f"{S}/data/ey_aug_parsed.json", encoding="utf-8"))["values"]
fr = json.load(open(f"{S}/data/aug_first_report.json", encoding="utf-8"))
print("파일 값의 열 이름:", sorted({c for b in mine.values() for d in b.values() for c in d}))
def num(v, scale):
    if isinstance(v, (int, float)) and not isinstance(v, bool): return float(v) * scale
    if isinstance(v, str):
        import re
        m = re.fullmatch(r"(\d+(?:\.\d+)?) pt \(.*\)", v.strip())   # EY 표기 예: "25 pt (833%)" = 경쟁사 점수(괄호는 LG 대비 비율)
        if m: return float(m.group(1))
        t = v.strip().rstrip("`").rstrip("%")
        try: return float(t) * (1 if v.strip().rstrip("`").endswith("%") else scale)
        except ValueError: return None
    return None
rows = []
summary = {}
for col in ("34", "39", "47", "37", "38", "42", "43", "4", "1", "2", "3"):
    scale = 100 if col not in ("1", "2", "3") else 1
    for brand in ("LG", "SAMSUNG"):
        keys = sorted(set(mine[brand]) | set(ey.get(col, {}).get(brand, {})))
        for key in keys:
            a = mine[brand].get(key, {}).get(col)
            e = ey.get(col, {}).get(brand, {}).get(key)
            eraw = e["v"] if e else None
            ev = num(eraw, scale) if e else None
            d = fr.get(brand, {}).get(key, {}).get(col, [None])[0]
            s = summary.setdefault((col, brand), {"파일=EY": 0, "파일≠EY": 0, "파일만 값": 0, "EY만 값": 0, "둘다 없음": 0, "대시보드8월=EY": 0, "대시보드8월≠EY": 0})
            if a is None and ev is None: st = "둘다 없음"
            elif a is None: st = "EY만 값"
            elif ev is None: st = "파일만 값"
            else: st = "파일=EY" if abs(a - ev) <= 0.011 else "파일≠EY"
            s[st] += 1
            if col not in ("4", "1", "2", "3"):
                if d is not None and ev is not None: s["대시보드8월=EY" if abs(d - ev) <= 0.011 else "대시보드8월≠EY"] += 1
                elif (d is None) != (ev is None): s["대시보드8월≠EY"] += 1
            rows.append([col, brand, key, e["cell"] if e else "", eraw, None if ev is None else round(ev, 4), None if a is None else round(a, 4), d, st])
w = csv.writer(open(f"{S}/data/aug_3way.csv", "w", encoding="utf-8-sig", newline=""))
w.writerow(["진단ID", "브랜드", "국가|리테일러|제품군", "EY 원본 칸(Summary Detail)", "EY 원본 저장값", "EY 값(환산)", "파일 값", "대시보드 8월 전용 계산", "판정"])
w.writerows(rows)
for k, s in summary.items(): print(k, s)
