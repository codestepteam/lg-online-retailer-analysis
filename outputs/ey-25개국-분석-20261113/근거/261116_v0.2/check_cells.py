"""검사 A: 카테고리 칸 값이 11/13 계산값과 같은지 (경쟁사 3곳과 10월 스냅샷 변경 칸 제외)."""
import json, sys
old = json.load(open(sys.argv[1])); new = json.load(open(sys.argv[2]))
COMP3 = {("EG","cairo-sales"),("AU","appliance-online"),("TW","momoshop")}
for m in ("8","10","11"):
    for oside, nside in (("LG","LG"),("SAMSUNG","COMP")):
        o = old["category"][m][oside]; n = new["category"][m][nside]
        same = diff = 0; diffs = []; comp_only = 0
        for k in sorted(set(o) | set(n)):
            cc, r, c = k.split("|")
            if nside == "COMP" and (cc, r) in COMP3:
                comp_only += 1; continue
            for col in sorted(set(o.get(k, {})) | set(n.get(k, {}))):
                a, b = o.get(k, {}).get(col), n.get(k, {}).get(col)
                if a is None and b is None: continue
                if a is not None and b is not None and abs(a - b) < 1e-9: same += 1
                else: diff += 1; diffs.append((k, col, a, b))
        print(f"{m}월 {nside}: 같음 {same}, 다름 {diff}, 경쟁사 3곳이라 따로 본 칸묶음 {comp_only}")
        for d in diffs[:40]: print("   ", d)
