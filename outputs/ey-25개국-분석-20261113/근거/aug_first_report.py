"""8월: 대시보드의 8월 전용 계산(first_report)을 개발 DB 원문 행에 돌려, 채운 값(computed.json)과 비교한다. 읽기 전용."""
import json, os, sys
D = '/Users/codestepseunghee/codestep/lge-hs-clinic-dashboard/backend'
S = sys.argv[1]
for line in open(D + '/.env', encoding='utf-8'):
    line = line.strip()
    if line and not line.startswith('#') and '=' in line:
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'").strip('"') if not v.strip().startswith('{') else v.strip())
sys.path.insert(0, D)
import pandas as pd
from app.data import db, adapters, first_report, scores
from app.domain import metrics, roster

OP = adapters.FIRST_REPORT_OPERATION_ID
print("8월 회차:", OP)
with db.read_only_session() as cur:
    records = db.fetch_baseline_records(cur, OP, first_report.ASSESSMENT_IDS, url_only=True)
print("원문 행:", len(records), "진단별:", records["assessment_id"].astype(str).value_counts().to_dict())
conv, mart = first_report.build_first_report(records, "2026-08-31")
full = {m: scores.mart_from_scores([], "")[m] for _a, (m, _p) in scores.SCORE_METRICS.items()}
for k, f in mart.items():
    full[k] = f
score = metrics.build_conversion_score(full)

inv = {v: k for k, v in roster.RETAILER_MAP.items()}
DIV2CAT = {"REF": "REF", "W/M": "WM", "D/W": "DW", "WM": "WM", "DW": "DW"}
AID = {m: a for a, (m, _p) in scores.SCORE_METRICS.items()}
PREFIX = {m: p for a, (m, p) in scores.SCORE_METRICS.items()}
out = {}   # brand -> key -> col -> (value, n, total)
for m, f in mart.items():
    p = PREFIX[m]
    for _, r in f.iterrows():
        key = "|".join([r["CNTRY_CODE"], inv[(r["CNTRY_CODE"], r["SITE_NAME"])], DIV2CAT[r["DIV"]]])
        pct = r[f"{p}_PCT"]
        out.setdefault(str(r["BRAND"]).upper(), {}).setdefault(key, {})[AID[m]] = (
            None if pd.isna(pct) else float(pct), int(r[f"{p}_N"]), int(r[f"{p}_TOTAL"]))
for _, r in score.iterrows():
    key = "|".join([r["CNTRY_CODE"], inv[(r["CNTRY_CODE"], r["SITE_NAME"])], DIV2CAT[r["DIV"]]])
    v = r["CONVERSION_SCORE"]
    out.setdefault(str(r["BRAND"]).upper(), {}).setdefault(key, {})["readiness"] = (None if pd.isna(v) else float(v), None, None)
json.dump(out, open(f"{S}/data/aug_first_report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("브랜드:", {b: len(v) for b, v in out.items()})
with open(f"{S}/data/aug_first_report.jsonl", "w", encoding="utf-8") as fh:
    for brand in ("LG", "SAMSUNG"):
        for key in sorted(out.get(brand, {})):
            cc, ret, category = key.split("|")
            for aid, (pct, n, tot_) in sorted(out[brand][key].items()):
                if aid == "readiness":
                    continue
                fh.write(json.dumps({"brand": brand, "country": cc, "retailer": ret, "category": category, "assessment_id": aid,
                                     "n": n, "total": tot_, "dashboard_pct": pct}, ensure_ascii=False) + "\n")

mine = json.load(open(f"{S}/data/computed.json", encoding="utf-8"))["category"]["8"]
norm = roster.normalize_pipeline_key
tot = {}
for brand in ("LG", "SAMSUNG"):
    mb = {}
    for k, d in mine[brand].items():
        cc, r, c = k.split("|"); mb["|".join([cc, norm(r), c])] = d
    for key in sorted(set(mb) | set(out.get(brand, {}))):
        for col in ("34", "39", "47", "37", "38", "42", "43", "readiness"):
            a = mb.get(key, {}).get(col)
            b = out.get(brand, {}).get(key, {}).get(col, (None,))[0]
            t = tot.setdefault(col, {"둘다": 0, "수치차이": 0, "한쪽만": 0, "ex": []})
            if a is None and b is None: continue
            if a is None or b is None:
                t["한쪽만"] += 1; t["ex"].append((brand, key, a, b)); continue
            t["둘다"] += 1
            if abs(a - b) > 0.011:
                t["수치차이"] += 1; t["ex"].append((brand, key, round(a, 2), b))
for col, t in tot.items():
    print(col, {k: v for k, v in t.items() if k != "ex"}, t["ex"][:4])
