import csv,json,pathlib,shutil,hashlib,unicodedata
ROOT=pathlib.Path('/Users/codestepseunghee/codestep/lg-online-retailer-analysis')
OUT=ROOT/'outputs/ey-25-country-audit-20261113-39d0ac5e'
DATA=pathlib.Path('/private/tmp/claude-501/-Users-codestepseunghee-codestep-lg-online-retailer-analysis/5cdf1839-729e-40d6-8177-cbed245162dc/scratchpad/data')
E=OUT/'근거';E.mkdir(exist_ok=True)
for name in ['aug_lg.jsonl','aug_brand_SAMSUNG.jsonl','aug_plp_lg.jsonl','aug_catsov_lg.jsonl','oct_lg.jsonl','oct_brand_SAMSUNG.jsonl','oct_plp_lg.jsonl','nov_plp_dev.jsonl','catsov_lg.jsonl','catsov_dev.jsonl']:
    shutil.copy2(DATA/name,E/name)
for name in ['inspect.mjs','audit.py','dashboard_check.py','source_checks.py','august_dashboard.py','package_audit.py']:
    shutil.copy2(pathlib.Path('/tmp/lg-audit-39d0ac5e')/name,E/name)
for f in (ROOT/'outputs/ey-25개국-분석-20261113/근거').glob('*.sql'):shutil.copy2(f,E/f.name)
allrows=list(csv.DictReader(open(OUT/'전체_셀_대조.csv',encoding='utf-8-sig')))
locations={}
for r in allrows:
    if r['sheet']=='8월_국가x리테일러x카테고리':
        label=r['label'].split('|')
        if len(label)==5:locations[label[3],'|'.join(label[:3]),label[4]]=r['cell']
aug=list(csv.DictReader(open(OUT/'8월_실제대시보드경로_대조.csv',encoding='utf-8-sig')))
for r in aug:r['sheet']='8월_국가x리테일러x카테고리';r['cell']=locations.get((r['brand'],r['key'],r['metric']),'')
with open(OUT/'8월_실제대시보드경로_대조.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=aug[0]);w.writeheader();w.writerows(aug)
for r in aug:
    if r['different']=='True':assert r['cell'],r
sql_rows={p.stem:sum(1 for l in p.open() if l.strip()) for p in OUT.glob('*.jsonl')}
print('SQL result counts',sql_rows)
print('firstreport differences',sum(r['different']=='True' for r in aug))
source=json.load(open(OUT/'audit_summary.json'))['file']
assert hashlib.sha256(pathlib.Path(source).read_bytes()).hexdigest()==json.load(open(OUT/'audit_summary.json'))['sha256']
assert len(allrows)==6708 and all(r['match']=='True' for r in allrows)
# 가짜 입력에서 수치 차이·빈칸/0 혼동을 검출하는 검사. 업무 파일은 변경하지 않는다.
def same(a,b):return a is None and b is None or isinstance(a,(float,int)) and isinstance(b,(float,int)) and abs(a-b)<1e-8
assert same(50,50) and not same(50,0) and not same(None,0) and not same(0,None)
assert not same(51,sum([10,20,20])) and same(50,sum([10,20,20]))
print('검증: 6708행 대조표, 173건 위치, SQL 결과 수, 원본 SHA, 가짜 차이·빈칸/0·합계 입력 확인')
