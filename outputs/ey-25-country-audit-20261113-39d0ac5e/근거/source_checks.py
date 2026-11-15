import pathlib,json,csv
from openpyxl import load_workbook
ROOT=pathlib.Path('/Users/codestepseunghee/codestep/lg-online-retailer-analysis')
OUT=ROOT/'outputs/ey-25-country-audit-20261113-39d0ac5e'
criteria=ROOT/'관련문서/EY_LGE HS 온라인 리테일 클리닉 진단 항목_v2.2_20261023(송부본).xlsx'
w=load_workbook(criteria,read_only=True,data_only=True)
print('CRITERIA',w.sheetnames)
for sh in w:
    if '진단 항목' not in sh.title:continue
    for row in sh.iter_rows(min_row=1,max_row=25):
        if any(c.value in ['ID1','ID2','ID3',1,2,3] for c in row[:14]) or any(c.value and '평균' in str(c.value) for c in row):
            print(sh.title,[(c.coordinate,str(c.value)) for c in row if c.value is not None])
w.close()
import unicodedata
source=next(p for p in pathlib.Path('/Users/codestepseunghee/Downloads').glob('*.xlsx') if unicodedata.normalize('NFC',p.name)=='★EY_LGE_Clinic_Assessment Summary_Improvement Tracker_V0.3_20260825 (업데이트).xlsx')
w=load_workbook(source,read_only=True,data_only=True)
fixture=json.load(open(ROOT.parent/'lge-hs-clinic-dashboard/backend/tests/fixtures/august_ey_v03_expected.json'))
data=json.load(open(ROOT/'outputs/ey-25개국-분석-20261113/근거/computed.json'))['category']['8']['LG']
ret={'ELCORTEINGLES_ELECTRONICA':'eci','DARTY':'darty','MEDIAWORLD':'mediaworld','MEDIAMARKT':'mediamarkt-nl','MEDIAEXPERT':'media-expert','ALZA':'alza','ELGIGANTEN':'elgiganten'}
aid={'video':'34','warranty':'39','dimension':'47','reviews_rating':'37','reviews_qty':'38','flix_coverage':'42','flix_rendering':'43'}
results=[]
for metric,addr,cc,retailer,cat,brand,n,d,pct in fixture['rows']:
    key='|'.join([cc,ret.get(retailer,retailer.lower()),{'W/M':'WM','D/W':'DW'}.get(cat,cat)])
    original=w['Summary Detail'][addr].value
    current=data.get(key,{}).get(aid[metric])
    results.append({'source_file':str(source),'sheet':'Summary Detail','cell':addr,'key':key,'metric':aid[metric],'original_cached':original,'original_percent':original*100 if isinstance(original,(float,int)) else None,'workbook_percent':current})
print('EY_SAMPLES',json.dumps(results,ensure_ascii=False))
with open(OUT/'EY_8월_원본_표본대조.csv','w',encoding='utf-8-sig',newline='') as f:
    z=csv.DictWriter(f,fieldnames=results[0]);z.writeheader();z.writerows(results)
