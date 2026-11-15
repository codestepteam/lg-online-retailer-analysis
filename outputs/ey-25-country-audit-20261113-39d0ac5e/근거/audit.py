import json, ast, csv, hashlib, statistics, collections, pathlib, re
ROOT=pathlib.Path('/Users/codestepseunghee/codestep/lg-online-retailer-analysis')
OUT=ROOT/'outputs/ey-25-country-audit-20261113-39d0ac5e'
OUT.mkdir(exist_ok=True)
DATA=pathlib.Path('/private/tmp/claude-501/-Users-codestepseunghee-codestep-lg-online-retailer-analysis/5cdf1839-729e-40d6-8177-cbed245162dc/scratchpad/data')
wb=json.load(open('/tmp/lg-audit-39d0ac5e/workbook.json'))
computed=json.load(open(ROOT/'outputs/ey-25개국-분석-20261113/근거/computed.json'))
constants={}
for n in ast.parse((ROOT/'outputs/ey-25개국-분석-20261113/근거/fill_workbook.py').read_text()).body:
    if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['COUNTRY_CODE','RETAILER_KEY','COLS','CATS','BRANDS','SEVEN','TWO']:
        constants[n.targets[0].id]=ast.literal_eval(n.value)
globals().update(constants)
def load(n):return [json.loads(x) for x in (DATA/n).read_text().splitlines()]
def avg(xs):
    xs=[x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None
def same(a,b):return a is None and b is None or isinstance(a,(int,float)) and isinstance(b,(int,float)) and abs(a-b)<1e-8
def col(n):
    out=''
    while n:n,r=divmod(n-1,26);out=chr(65+r)+out
    return out
def cell(sh,r,c):return wb['sheets'][sh]['values'][r-1][c-1]
def grp(cc):return '7' if cc in SEVEN else '2' if cc in TWO else '16'
source=collections.defaultdict(list)
raw_checks=[]
for mo,prefix in [('8','aug'),('10','oct')]:
    for brand,suffix in [('LG','lg'),('SAMSUNG','brand_SAMSUNG')]:
        for x in load(f'{prefix}_{suffix}.jsonl'):
            if x['assessment_id'] not in COLS:continue
            key=(mo,brand,x['country'],x['retailer'].replace('_','-'),x['category'],x['assessment_id'])
            if x['value'] is not None:
                source[key].append(float(x['value'])*100)
                if x['completed']:
                    raw_checks.append({'file':f'{prefix}_{suffix}.jsonl','key':str(key),'value':x['value'],'numerator':x['pass_count'],'denominator':x['completed'],'match':same(x['value'],x['pass_count']/x['completed'])})
for mo,fn in [('10','oct_plp_lg.jsonl'),('11','nov_plp_dev.jsonl')]:
    for x in load(fn):
        if not x['scored']:continue
        key=(mo,x['brand'],x['country'],x['retailer'],x['category'],x['assessment_id'])
        source[key].append(float(x['avg_score'] if x['assessment_id']=='4' else x['sum_score']))
for x in load('aug_plp_lg.jsonl'):
    source[('8',x['brand'],x['country'],x['retailer'],x['category'],x['assessment_id'])].append(float(x['raw'].strip('"% ')))
cat={k:(sum(v) if k[0]=='8' and k[-1] in ['1','2','3'] else avg(v)) for k,v in source.items()}
for mo,fn in [('8','aug_catsov_lg.jsonl'),('10','catsov_lg.jsonl'),('11','catsov_dev.jsonl')]:
    vals=collections.defaultdict(list)
    for x in load(fn):
        if mo!='8' and x['ym']!=f'2026-{int(mo):02d}':continue
        key=(mo,x['brand'],x['country'],x['retailer'],x['category'])
        vals[key].append(float(x['top10_count'])*10 if mo=='8' else float(x['category_sov']))
    for k,v in vals.items():
        a=avg(v)
        if a>0 or any(k+(aid,) in cat for aid in ['1','2','3','4']):cat[k+('catsov',)]=a
for k in list({k[:-1] for k in cat}):
    if all(k+(a,) in cat for a in ['34','39','47','37','38']):cat[k+('readiness',)]=avg([cat[k+(a,)] for a in ['34','39','47','37','38']])
    if k+('4',) in cat and k+('catsov',) in cat:cat[k+('vis',)]=(cat[k+('4',)]+cat[k+('catsov',)])/2
ret={};country={}
for mo,brand,cc,retailer in {k[:4] for k in cat if k[4] in CATS}:
    for metric in COLS:ret[mo,brand,cc,retailer,metric]=avg([cat.get((mo,brand,cc,retailer,c,metric)) for c in CATS])
for mo,brand,cc in {k[:3] for k in ret}:
    for metric in COLS:country[mo,brand,cc,metric]=avg([v for k,v in ret.items() if k[:3]==(mo,brand,cc) and k[-1]==metric])
checks=[]
def check(sh,r,c,expected,basis,label=''):
    actual=cell(sh,r,c)
    if actual is not None or expected is not None:
        checks.append({'sheet':sh,'cell':col(c)+str(r),'label':label,'actual':actual,'expected':expected,'difference':actual-expected if isinstance(actual,(float,int)) and isinstance(expected,(float,int)) else None,'match':same(actual,expected),'basis':basis})
for sh in wb['sheets']:
    if '월_' not in sh:continue
    mo=sh.split('월')[0];level=sh.count('x');first=12 if level==2 else 11;end=47 if level==2 else 46 if level==1 else 36;startcol=4 if level else 3
    columns=[(startcol+bi*14*(3 if level==2 else 1)+ci*14+mi,b,c,m) for bi,b in enumerate(BRANDS) for ci,c in enumerate(CATS if level==2 else ['']) for mi,m in enumerate(COLS)]
    for xc,brand,category,metric in columns:
        row_values=[]
        for r in range(first,end):
            cc=COUNTRY_CODE[cell(sh,r,2).strip()];retailer=RETAILER_KEY[cc,cell(sh,r,3).strip()] if level else ''
            exp=cat.get((mo,brand,cc,retailer,category,metric)) if level==2 else ret.get((mo,brand,cc,retailer,metric)) if level==1 else country.get((mo,brand,cc,metric))
            check(sh,r,xc,exp,'saved source aggregation' if level==2 else 'category mean' if level==1 else 'retailer mean',f'{cc}|{retailer}|{category}|{brand}|{metric}')
            row_values.append((cc,exp))
        for i,g in enumerate(['7','16','25']):
            xs=[v for cc,v in row_values if v is not None and (g=='25' or grp(cc)==g)] if mo!='8' or g=='7' else []
            for delta,exp in [(0,sum(xs) if xs else None),(3,avg(xs))]:check(sh,first-6+i+delta,xc,exp,'sum of detail rows' if not delta else 'mean of nonblank detail rows',g+'|'+brand+'|'+category+'|'+metric)
def idx(a,b):return round(a/b*100) if a is not None and b not in [None,0] else None
sh='※ 25개국 Summary'
for level in [0,1]:
    for mi,mo in enumerate(['8','10','11']):
        for ti,metric in enumerate(['readiness','vis']):
            xc=(3 if level==0 else 12)+ti*3+mi;rows=[]
            for r in range(12,37 if level==0 else 47):
                cc=COUNTRY_CODE[cell(sh,r,2 if level==0 else 10).strip()]
                retkey=RETAILER_KEY[cc,cell(sh,r,11).strip()] if level else ''
                vals=[ret.get((mo,b,cc,retkey,metric)) if level else country.get((mo,b,cc,metric)) for b in BRANDS]
                check(sh,r,xc,idx(*vals),'round(LG / Samsung * 100)',cc+'|'+retkey+'|'+mo+'|'+metric);rows.append((cc,*vals))
            for i,g in enumerate(['7','16','25']):
                ps=[(a,b) for cc,a,b in rows if a is not None and b is not None and (g=='25' or grp(cc)==g)] if mo!='8' or g=='7' else []
                exp=idx(sum(a for a,b in ps),sum(b for a,b in ps)) if ps else None
                for r in [6+i,9+i]:check(sh,r,xc,exp,'paired LG sum / Samsung sum * 100',g+'|'+mo+'|'+metric)
with open(OUT/'전체_셀_대조.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=checks[0]);w.writeheader();w.writerows(checks)
formula_count=sum(bool(x) for s in wb['sheets'].values() for row in s['formulas'] for x in row)
old=ROOT/'outputs/ey-25개국-분석-20261113/25개국 분석_261113_v0.1_수정.xlsx'
summary={'file':wb['path'],'sha256':hashlib.sha256(pathlib.Path(wb['path']).read_bytes()).hexdigest(),'same_as_generated':pathlib.Path(wb['path']).read_bytes()==old.read_bytes(),'cell_checks':len(checks),'mismatches':[x for x in checks if not x['match']],'by_sheet':dict(collections.Counter(x['sheet'] for x in checks)),'formulas':formula_count,'pdp_ratio_checks':len(raw_checks),'pdp_ratio_mismatch':[x for x in raw_checks if not x['match']]}
(OUT/'audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
for sh in ['※ 25개국 Summary','11월_국가x리테일러x카테고리']:
    print(sh)
    for r in [1,2,3,4,5,6,7,8,9,10,11,12,14,19,22,28]:print(r,[(col(i+1),v) for i,v in enumerate(wb['sheets'][sh]['values'][r-1]) if v is not None][:30])
