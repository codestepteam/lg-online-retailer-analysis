import sys,pathlib,gzip,json,csv,collections
import pandas as pd
ROOT=pathlib.Path('/Users/codestepseunghee/codestep')
sys.path.insert(0,str(ROOT/'lge-hs-clinic-dashboard/backend'))
from app.data import adapters,first_report,scores
from app.domain import roster,metrics
OUT=ROOT/'lg-online-retailer-analysis/outputs/ey-25-country-audit-20261113-39d0ac5e'
source=ROOT/'lge-hs-clinic-dashboard/var/reporting/v03-20261026/v03.report-records.json.gz'
rows=[json.loads(l) for l in gzip.decompress(source.read_bytes()).decode().splitlines()]
_,mart=first_report.build_first_report(pd.DataFrame(rows).assign(operation_id='op-20261026-01'),'2026-08-31')
mart['readiness']=metrics.build_conversion_score(mart)
mine=json.load(open(ROOT/'lg-online-retailer-analysis/outputs/ey-25개국-분석-20261113/근거/computed.json'))['category']['8']
inv={v:k for k,v in roster.RETAILER_MAP.items()}; div={'REF':'REF','W/M':'WM','D/W':'DW'}
records=[];refs={}
for aid,(key,prefix) in {**scores.SCORE_METRICS,'readiness':('readiness','CONVERSION')}.items():
    pc=prefix+('_SCORE' if aid=='readiness' else '_PCT')
    for _,r in mart[key].iterrows():
        brand=r['BRAND']
        if brand not in ['LG','SAMSUNG']:continue
        k='|'.join([r['CNTRY_CODE'],inv[r['CNTRY_CODE'],r['SITE_NAME']],div[r['DIV']]])
        val=float(r[pc]) if pd.notna(r[pc]) else None
        refs[brand,k,aid]=val
        old=mine.get(brand,{}).get(k,{}).get(aid)
        records.append({'brand':brand,'key':k,'metric':aid,'workbook':old,'dashboard_august_code':val,'different':(old is None)!=(val is None) or old is not None and val is not None and abs(old-val)>.011})
for brand,cells in mine.items():
    for k,vals in cells.items():
        for aid,v in vals.items():
            if aid not in [*scores.SCORE_METRICS,'readiness'] or (brand,k,aid) in refs:continue
            records.append({'brand':brand,'key':k,'metric':aid,'workbook':v,'dashboard_august_code':None,'different':True})
with open(OUT/'8월_실제대시보드경로_대조.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
print('8월 실제경로',len(records),'차이',sum(r['different'] for r in records))
for aid in [*scores.SCORE_METRICS,'readiness']:
    subset=[r for r in records if r['metric']==aid];print(aid,len(subset),sum(r['different'] for r in subset),'numeric',sum(r['different'] and r['workbook'] is not None and r['dashboard_august_code'] is not None for r in subset))
print('examples',json.dumps([r for r in records if r['different'] and r['key'] in ['FR|darty|REF','IT|mediaworld|REF','PL|media-expert|REF','SE|elgiganten|REF']],ensure_ascii=False))
print('first report keys',[(k,len(v)) for k,v in mart.items()])
cs=json.load(open(ROOT/'lg-online-retailer-analysis/outputs/ey-25개국-분석-20261113/근거/computed.json'))
retailers={};countries={}
for brand in ['LG','SAMSUNG']:
    for cr in {k.rsplit('|',1)[0] for b,k,a in refs if b==brand and a=='readiness'}:
        vs=[v for (b,k,a),v in refs.items() if b==brand and a=='readiness' and k.rsplit('|',1)[0]==cr and v is not None]
        if vs:retailers[brand,cr]=sum(vs)/len(vs)
    for cc in {k.split('|')[0] for b,k in retailers if b==brand}:
        vs=[v for (b,k),v in retailers.items() if b==brand and k.split('|')[0]==cc]
        countries[brand,cc]=sum(vs)/len(vs)
print('8월 country Index',[(cc,round(cs['country']['8']['LG'][cc]['readiness']/cs['country']['8']['SAMSUNG'][cc]['readiness']*100),round(countries['LG',cc]/countries['SAMSUNG',cc]*100)) for b,cc in countries if b=='LG'])
print('8월 7국 aggregate index',round(sum(v for (b,k),v in countries.items() if b=='LG')/sum(v for (b,k),v in countries.items() if b=='SAMSUNG')*100))
