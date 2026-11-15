"""대조용: 대시보드(lge-hs-clinic-dashboard) 자체 계산 코드로 같은 값을 다시 구해 채운 값과 비교한다. 읽기 전용."""
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
from app.data import db, adapters
from app.data.scores import mart_from_scores, SCORE_COLUMNS
from app.domain import metrics, roster

SCHEMA = db.SCHEMA
mine = json.load(open(f"{S}/data/computed.json", encoding="utf-8"))["category"]
inv = {v: k for k, v in roster.RETAILER_MAP.items()}          # (국가, 사이트명) -> 파이프라인 키
norm = roster.normalize_pipeline_key
DIV2CAT = {"REF": "REF", "W/M": "WM", "D/W": "DW", "WM": "WM", "DW": "DW"}

def my(month, brand, col):
    out = {}
    for k, d in mine[month][brand].items():
        cc, r, c = k.split("|")
        if col in d:
            out[(cc, norm(r), c)] = d[col]
    return out

def compare(title, ref, mine_d, absent_zero=False):
    keys = sorted(set(ref) | set(mine_d))
    both = [k for k in keys if k in ref and k in mine_d]
    diffs = [(k, ref[k], mine_d[k]) for k in both if abs(ref[k] - mine_d[k]) > 0.011]
    only_ref = [k for k in keys if k not in mine_d and not (absent_zero and abs(ref[k]) < 1e-9)]
    only_mine = [k for k in keys if k not in ref and not (absent_zero and abs(mine_d[k]) < 1e-9)]
    mx = max((abs(ref[k] - mine_d[k]) for k in both), default=0)
    print(f"[{title}] 양쪽 다 있음 {len(both)} / 차이 0.01 초과 {len(diffs)} / 최대 차이 {mx:.4f} / 대시보드에만 {len(only_ref)} / 내 값에만 {len(only_mine)}")
    for x in diffs[:8]: print("    차이", x)
    for x in only_ref[:8]: print("    대시보드에만", x, ref[x])
    for x in only_mine[:8]: print("    내 값에만", x, mine_d[x])

# --- A. PDP Readiness: 같은 점수 행을 대시보드 코드(mart_from_scores → build_conversion_score)에 넣어 비교
# 8월은 여기서 대조하지 않는다 — 대시보드는 8월에 전용 계산(first_report)을 쓰므로 aug_first_report.py와 8월_EY원본_대조.csv를 본다.
for month, label, files in [("10", "2026-10", ("oct_lg.jsonl", "oct_brand_SAMSUNG.jsonl"))]:
    rows = [json.loads(l) for fn in files for l in open(f"{S}/data/{fn}", encoding="utf-8") if l.strip()]
    stats = {}
    mart = mart_from_scores(pd.DataFrame(rows, columns=SCORE_COLUMNS), label, stats)
    score = metrics.build_conversion_score(mart)
    print(month, "월 대시보드가 버린 행:", stats, "| 브랜드:", sorted(score["BRAND"].dropna().unique()))
    for brand in ("LG", "SAMSUNG"):
        ref = {}
        for _, r in score[score["BRAND"].astype(str).str.upper() == brand].iterrows():
            if pd.notna(r["CONVERSION_SCORE"]):
                ref[(r["CNTRY_CODE"], inv[(r["CNTRY_CODE"], r["SITE_NAME"])], DIV2CAT[r["DIV"]])] = float(r["CONVERSION_SCORE"])
        compare(f"PDP Readiness {month}월 {brand}", ref, my(month, brand, "readiness"))

# --- B/C. 노출 지표: 개발 DB에서 읽어 대시보드 코드로 계산
with db.read_only_session() as cur:
    lists = db._fetch_df(cur,
        f"SELECT l.collected_on, l.page_id, p.retailer, p.country, p.category, p.kind, p.search_keyword, p.gnb_keyword, "
        f"l.source_key, l.source_kind, l.complete, l.end_reached, l.total, l.product_count, l.short_complete, l.reason "
        f"FROM {SCHEMA}.plp_daily_sets s "
        f"JOIN {SCHEMA}.plp_daily_pages p ON p.request_id = s.request_id AND p.collected_on = s.collected_on "
        f"JOIN {SCHEMA}.plp_daily_rank_lists l ON l.collected_on = p.collected_on AND l.page_id = p.page_id AND l.request_id = s.request_id "
        f"WHERE s.superseded_at IS NULL AND p.kind = 'gnb'")
    ranks = db._fetch_df(cur,
        f"SELECT r.collected_on, r.page_id, r.rank, r.brand, r.brand_raw, NULL::text AS name, NULL::text AS url, r.is_ad "
        f"FROM {SCHEMA}.plp_daily_sets s "
        f"JOIN {SCHEMA}.plp_daily_pages p ON p.request_id = s.request_id AND p.collected_on = s.collected_on AND p.kind = 'gnb' "
        f"JOIN {SCHEMA}.plp_daily_ranks r ON r.collected_on = s.collected_on AND r.request_id = s.request_id AND r.page_id = p.page_id "
        f"WHERE s.superseded_at IS NULL AND r.rank <= 10")
    daily4 = db.fetch_plp_daily_search_results(cur, ["4"])
    base = db.fetch_baseline_records(cur, "op-20261026-01", ["4"])
a4 = adapters.search_sov_source_from_registry(base, "2026-08-31")
if len(a4):
    g = a4.groupby(["CNTRY_CODE", "SITE_NAME", "PRODUCT", "BRAND_NAME"], as_index=False)["VALUE"].mean()
    for brand in ("LG", "SAMSUNG"):
        ref = {(r["CNTRY_CODE"], inv[(r["CNTRY_CODE"], r["SITE_NAME"])], DIV2CAT[r["PRODUCT"]]): float(r["VALUE"]) for _, r in g[g["BRAND_NAME"] == brand].iterrows()}
        compare(f"ID4 검색 점유 8월 {brand}", ref, my("8", brand, "4"))
else:
    print("개발 DB에 8월 기준 자료 없음 — 8월 ID4 대조 생략")
print("읽은 행: 목록", len(lists), "순위", len(ranks), "ID4 일별", len(daily4))

def month_values(src):
    """대시보드 일별 원천 → (월, 국가, 사이트, 제품군, 브랜드)별 값: 검색어별 월 평균 → 검색어 평균."""
    d = src.assign(M=pd.to_datetime(src["DATE"]).dt.strftime("%m").str.lstrip("0"))
    kw = d.groupby(["M", "CNTRY_CODE", "SITE_NAME", "PRODUCT", "SRCH_KWD", "BRAND_NAME"], as_index=False)["VALUE"].mean()
    return kw.groupby(["M", "CNTRY_CODE", "SITE_NAME", "PRODUCT", "BRAND_NAME"], as_index=False)["VALUE"].mean()

cs = month_values(adapters.category_sov_daily_from_rank_lists(lists, ranks))
s4 = month_values(adapters.search_sov_daily_from_plp_daily(daily4))
for title, frame, col in [("Category SOV", cs, "catsov"), ("ID4 검색 점유", s4, "4")]:
    for month in ("10", "11"):
        for brand in ("LG", "SAMSUNG"):
            sub = frame[(frame["M"] == month) & (frame["BRAND_NAME"] == brand)]
            ref = {(r["CNTRY_CODE"], inv[(r["CNTRY_CODE"], r["SITE_NAME"])], DIV2CAT[r["PRODUCT"]]): float(r["VALUE"]) for _, r in sub.iterrows()}
            compare(f"{title} {month}월 {brand}", ref, my(month, brand, col), absent_zero=(col == "catsov"))
