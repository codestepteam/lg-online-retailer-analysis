import csv,json,collections,unicodedata,hashlib
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
BASE=ROOT/'pdp 모수 추출/최종_20261029'
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def key(u):return urlsplit(u).path.rstrip('/')
v6=next(p for p in BASE.glob('*.csv') if unicodedata.normalize('NFC',p.name).startswith('PDP모수_공유용_v6_'))
old=[r for r in readcsv(v6) if r['리테일러']=='Sharaf DG']
newfile=ROOT/'outputs/sharaf-157-filtered-20261110-e4651deb/Sharaf DG 두레이 157 적용_필터결과.csv'
new=readcsv(newfile)
print('new fields',list(new[0]))
# The filtered audit CSV uses the same decision field as the shared v7 CSV.
state='모수 포함 여부' if '모수 포함 여부' in new[0] else '판정'
urlfield='확인 요청 URL' if '확인 요청 URL' in new[0] else '카드PDP링크'
included=[r for r in new if r[state] in ('포함','남김')]
by=collections.defaultdict(list)
for r in old:by[key(r['확인 요청 URL'])].append(r)
classifications=collections.Counter();matched=[]
for n in included:
 previous=by.get(key(n[urlfield]),[])
 if any(r['모수 포함 여부']=='포함' for r in previous):label='기존 포함'
 elif any(r['제외단계']=='③리리부' and r['제외사유'].startswith('외부 판매자') for r in previous):
  label='기존 외부 판매자 제외'
  p=next(r for r in previous if r['제외단계']=='③리리부' and r['제외사유'].startswith('외부 판매자'))
  matched.append({'상품명':n['상품명'],'기존행번호':p['행번호'],'기존URL':p['확인 요청 URL'],'기존판매자':p['판매자'],'기존제외사유':p['제외사유'],'재조사직판URL':n[urlfield]})
 elif not previous:label='기존 원본에 상품 경로 없음'
 else:label='그 외'
 classifications[label]+=1
assert classifications=={'기존 포함':12,'기존 외부 판매자 제외':93,'기존 원본에 상품 경로 없음':11}, classifications
assert all(m['기존URL']!=m['재조사직판URL'] for m in matched)
oldurlset={r['확인 요청 URL'] for r in old}
assert all(m['재조사직판URL'] not in oldurlset for m in matched)
assert len({key(r[urlfield]) for r in included})==116
stages=collections.Counter(r['제외단계'] or '포함' for r in old)
assert stages=={'①브랜드':2188,'②제품군':3,'④중복':336,'③리리부':250,'포함':16},stages
sellerfile=BASE/'판정근거/판매자판정/seller_g4.csv'
sellers=[r for r in readcsv(sellerfile) if r['리테일러']=='Sharaf DG']
assert collections.Counter(r['판매자구분'] for r in sellers)=={'외부판매자':241,'직판':25}
pages=[json.loads(l) for l in (BASE/'판정근거/페이지확인/pages_best.jsonl').open() if 'Sharaf DG' in l]
assert len(pages)==266 and all(r['페이지상태']=='정상' and r['요청URL']==r['실제URL'] for r in pages)
oldpages=[json.loads(l) for l in (ROOT/'pdp 모수 추출/검색결과_20261028_734afcdd/상품카드_페이지원본.jsonl').open()]
oldpages=[p for p in oldpages if p.get('retailer','').strip()=='Sharaf DG' and p.get('valid_collection') is not False]
assert len(oldpages)==63 and sum(len(p['cards']) for p in oldpages)==2793
assert all(not any('seller' in k for k in parse_qs(urlsplit(p['final_url']).query)) for p in oldpages)
assert all(set(c)=={'position','name','pdp_link','ad'} for p in oldpages for c in p['cards'])
functions=json.loads((ROOT/'pdp 모수 추출/검색결과_20261028_734afcdd/브라우저수집_함수기록.json').read_text())
modules=[s for s in functions.values() if isinstance(s,str) and 'export function sharaf(ctx,tab,control)' in s]
assert modules
sharafcode=modules[-1].split('export function sharaf(ctx,tab,control)',1)[1]
assert 'seller' not in sharafcode.lower() and 'a.product-link' in sharafcode
(OUT/'original-sharaf-collection.txt').write_text('export function sharaf(ctx,tab,control)'+sharafcode)
obs=json.loads((ROOT/'outputs/sharaf-toggle-causality-20261110-5972e8b2/search-observations.json').read_text())
off,on=obs; onby={key(c['url']):c for c in on['cards']};pairs=[]
for c in off['cards']:
 n=onby.get(key(c['url']))
 if n and c['seller']!='Sharaf DG' and any(b in c['title'].lower() for b in ('lg ','bosch','samsung','hisense')):
  assert c['sku']==n['sku'] and n['seller']=='Sharaf DG' and c['url']!=n['url']
  oldmatch=[r for r in old if r['확인 요청 URL']==c['url'] and r['제외사유'].startswith('외부 판매자')]
  pairs.append({'title':c['title'],'sku':c['sku'],'off_seller':c['seller'],'off_url':c['url'],'on_seller':n['seller'],'on_url':n['url'],'same_external_url_found_in_october_exclusions':bool(oldmatch),'old_rows':[r['행번호'] for r in oldmatch]})
assert len(pairs)==3 and all(p['same_external_url_found_in_october_exclusions'] for p in pairs)
with (OUT/'93개_외부판매자제외에서직판포함_대조.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(matched[0]));w.writeheader();w.writerows(matched)
report={'source_v6':str(v6.relative_to(ROOT)),'source_v6_sha256':hashlib.sha256(v6.read_bytes()).hexdigest(),'old_raw_pages':len(oldpages),'old_raw_rows':2793,'old_decision_stages':dict(stages),'historical_unique_pdp_checks':len(pages),'historical_request_vs_actual_url_differences':0,'historical_parsed_sellers':dict(collections.Counter(r['판매자구분'] for r in sellers)),'original_direct25_later_removed':9,'new_included_vs_old':dict(classifications),'same_day_search_pairs':pairs,'observed_off_at':off['checkedAt'],'observed_on_at':on['checkedAt']}
report['interpretation']='기존 코드는 목록의 대표 판매 제안 URL만 수집하고 외부 판매자 제외 뒤 같은 제품의 직판 URL을 추가로 찾지 않는다. 93개 제품의 기존 제외와 현재 직판 포함을 대조했다.'
report['limits']=['당시 상세 페이지 HTML을 현재 확인할 수 없어 기존 첫 seller_name 파서의 외부 판매자 241건 판정 전체를 재검증할 수 없다.','10월 28일에 현재 직판 판매 제안이 존재했는지, 93건 모두 토글만으로 바뀐 것인지는 확정하지 않았다.','동일 시점 토글 비교는 검색어 1개의 첫 48개 카드이며 전체 9개 검색어 비교가 아니다.']
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:report[k] for k in ['old_decision_stages','historical_parsed_sellers','new_included_vs_old','same_day_search_pairs']},ensure_ascii=False,indent=2))
