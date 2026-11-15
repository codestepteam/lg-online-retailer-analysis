import os,sys,json,pathlib,csv
import pandas as pd
D=pathlib.Path('/Users/codestepseunghee/codestep/lge-hs-clinic-dashboard/backend')
sys.path.insert(0,str(D))
from dotenv import load_dotenv
load_dotenv(D/'.env')
from app.data import db,adapters
from app.domain import metrics,roster
from app.data.scores import mart_from_scores,SCORE_COLUMNS
OUT=pathlib.Path('/Users/codestepseunghee/codestep/lg-online-retailer-analysis/outputs/ey-25-country-audit-20261113-39d0ac5e')
DATA=pathlib.Path('/private/tmp/claude-501/-Users-codestepseunghee-codestep-lg-online-retailer-analysis/5cdf1839-729e-40d6-8177-cbed245162dc/scratchpad/data')
sqls={
'daily_id4':"""SELECT r.collected_on, r.page_id, p.retailer, p.country, p.category, p.kind, p.search_keyword, p.representative, r.assessment_id, r.brand, r.score, r.verdict_status, r.source_kind
FROM lg_registry.plp_daily_sets s
JOIN lg_registry.plp_daily_pages p ON p.request_id=s.request_id AND p.collected_on=s.collected_on
JOIN lg_registry.plp_daily_results r ON r.request_id=s.request_id AND r.collected_on=p.collected_on AND r.page_id=p.page_id
WHERE s.superseded_at IS NULL AND p.kind='search' AND r.assessment_id='4'
AND r.collected_on >= '2026-10-01' AND r.collected_on <= '2026-11-13'""",
'gnb_lists':"""SELECT l.collected_on, l.page_id, p.retailer, p.country, p.category, p.kind, p.search_keyword, p.gnb_keyword, l.source_key, l.source_kind, l.complete, l.end_reached, l.total, l.product_count, l.short_complete, l.reason
FROM lg_registry.plp_daily_sets s
JOIN lg_registry.plp_daily_pages p ON p.request_id=s.request_id AND p.collected_on=s.collected_on
JOIN lg_registry.plp_daily_rank_lists l ON l.collected_on=p.collected_on AND l.page_id=p.page_id AND l.request_id=s.request_id
WHERE s.superseded_at IS NULL AND p.kind='gnb' AND l.collected_on >= '2026-10-01' AND l.collected_on <= '2026-11-13'""",
'gnb_ranks':"""SELECT r.collected_on, r.page_id, r.rank, r.brand, r.brand_raw, NULL::text AS name, NULL::text AS url, r.is_ad
FROM lg_registry.plp_daily_sets s
JOIN lg_registry.plp_daily_pages p ON p.request_id=s.request_id AND p.collected_on=s.collected_on AND p.kind='gnb'
JOIN lg_registry.plp_daily_ranks r ON r.collected_on=s.collected_on AND r.request_id=s.request_id AND r.page_id=p.page_id
WHERE s.superseded_at IS NULL AND r.rank <= 10 AND r.collected_on >= '2026-10-01' AND r.collected_on <= '2026-11-13'""",
'operation_period':"""SELECT r.assessment_id, min(d->>'collected_on') AS first_day, max(d->>'collected_on') AS last_day, count(*) AS day_entries
FROM lg_registry.plp_operation_state s
JOIN lg_registry.current_plp_results r ON r.operation_id=s.operation_id AND r.selected_snapshot_id=s.current_snapshot_id
CROSS JOIN LATERAL jsonb_array_elements(r.diagnostic_detail->'days') d
WHERE s.operation_id='op-20261101-01' AND r.assessment_id IN ('1','2','3','4') GROUP BY 1 ORDER BY 1"""
}
frames={}
with db.read_only_session() as cur:
    for name,sql in sqls.items():
        (OUT/(name+'.sql')).write_text(sql+';\n')
        frames[name]=db._fetch_df(cur,sql)
        frames[name].to_json(OUT/(name+'.jsonl'),orient='records',lines=True,force_ascii=False,date_format='iso')
        print(name,len(frames[name]),flush=True)
print(frames['operation_period'].to_dict('records'),flush=True)
mine=json.load(open(DATA/'computed.json'))['category']
inv={v:k for k,v in roster.RETAILER_MAP.items()}
div={'W/M':'WM','D/W':'DW','REF':'REF'}
comparisons=[]
def collect(df,col,metric,cutoff):
    for _,r in df.iterrows():
        mo=str(int(r['MONTH'].split('-')[1]));b=r['BRAND'];k='|'.join([r['CNTRY_CODE'],inv[r['CNTRY_CODE'],r['SITE_NAME']],div[r['DIV']]])
        if b not in ['LG','SAMSUNG']:continue
        original=mine.get(mo,{}).get(b,{}).get(k,{}).get(metric)
        reference=float(r[col]) if pd.notna(r[col]) else None
        comparisons.append({'month':mo,'brand':b,'key':k,'metric':metric,'cutoff':cutoff,'workbook':original,'dashboard_code':reference,'difference':original-reference if original is not None and reference is not None else None})
for cutoff in ['2026-11-13','2026-11-10']:
    s=adapters.search_sov_daily_from_plp_daily(frames['daily_id4'],cutoff=cutoff,months=['2026-10','2026-11'])
    c=adapters.category_sov_daily_from_rank_lists(frames['gnb_lists'],frames['gnb_ranks'],cutoff=cutoff,months=['2026-10','2026-11'])
    for metric,src in [('4',s),('catsov',c)]:
        monthly=adapters.search_sov_month_from_daily(src)
        monthly=monthly.assign(MONTH=pd.to_datetime(monthly.DATE).dt.strftime('%Y-%m'),DIV=monthly.PRODUCT.map(roster.CATEGORY_TO_DIV),BRAND=monthly.BRAND_NAME)
        value=metrics._vis_divide(monthly,['CNTRY_CODE','SITE_NAME','DIV','MONTH'])
        collect(value,'VALUE',metric,cutoff)
for mo,prefix in [('8','aug'),('10','oct')]:
    rows=[json.loads(l) for name in [prefix+'_lg.jsonl',prefix+'_brand_SAMSUNG.jsonl'] for l in (DATA/name).read_text().splitlines()]
    mart=mart_from_scores(pd.DataFrame(rows,columns=SCORE_COLUMNS),f'2026-{int(mo):02d}')
    collect(metrics.build_conversion_score(mart),'CONVERSION_SCORE','readiness','source_snapshot')
    for aid,(key,prefix2) in __import__('app.data.scores',fromlist=['SCORE_METRICS']).SCORE_METRICS.items():
        collect(mart[key],prefix2+'_PCT',aid,'source_snapshot')
with open(OUT/'대시보드_계산_대조.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=comparisons[0]);w.writeheader();w.writerows(comparisons)
df=pd.DataFrame(comparisons)
for k,g in df.groupby(['month','metric','cutoff']):
    print(k,'compared',g.difference.notna().sum(),'diff > .011',g.difference.abs().gt(.011).sum(),'max',g.difference.abs().max())
print(df[(df.month=='11') & (df.metric=='4') & (df.difference.abs()>.011)].sort_values('difference').to_string(index=False))
