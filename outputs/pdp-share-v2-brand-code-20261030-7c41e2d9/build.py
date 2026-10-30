# 공유용 CSV에 브랜드·제품코드 열을 붙여 공유용 v2를 만든다(2026-10-30 최하은 피드백).
# - 브랜드: OSM 행은 OSM이 준 BRAND, 검색 행은 1단계 판정(step1_filter.py)과 같은 방법으로 상품명·주소에서 찾은 대상 브랜드.
# - 제품코드: OSM 행은 OSM이 준 MPC(대문자로 통일), 검색 행은 상품명(없으면 주소)에서 뽑은 추정값.
# 행 순서·URL·판정 등 기존 열 값은 바꾸지 않는다. 실행: PYTHONPATH=<openpyxl 경로> /usr/bin/python3 build.py
import csv, json, os, sys, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from model_code import model_code

ROOT = '/Users/codestepseunghee/codestep/lg-online-retailer-analysis'
PDP = ROOT + '/pdp 모수 추출'
FIN = PDP + '/최종_20261029'
SRC = FIN + '/PDP모수_공유용_25개국_35개리테일러_전체판정_55997행_20261029.csv'
DST = FIN + '/PDP모수_공유용_25개국_35개리테일러_전체판정_55997행_20261029_v2.csv'

# 1단계 판정 코드의 브랜드 목록·찾기 함수를 그대로 쓴다(입력 읽기 앞부분만 실행)
code = open(FIN + '/판정근거/스크립트/step1_filter.py', encoding='utf-8').read()
code = code.split('# ---------- 입력 읽기')[0].replace('OUT = sys.argv[1]', "OUT = ''")
g = {}
exec(code, g)
BRANDS, brands_in, slug = g['BRANDS'], g['brands_in'], g['slug']
CAT_KEY = {'REF': 'REF', 'W/M': 'W/M', 'DRY': 'W/M', 'D/W': 'DW'}  # step1_filter.cat_key와 같음

# OSM 원본 행: step1_filter.py와 같은 순서로 읽으면 공유용 행번호 1~12126과 1:1로 맞는다
osm = []
for f, keep in [('OSM_유럽13개리테일러_PDP후보_8160건_20261026.csv', lambda x: x['CNTRY'] not in ('Germany', 'UK')),
                ('OSM_독일영국5개리테일러_PDP후보_1889건_20261029.csv', lambda x: True),
                ('OSM_추가9개리테일러_PDP후보_4942건_20261028.csv', lambda x: True)]:
    osm += [x for x in csv.DictReader(open(PDP + '/' + f, encoding='utf-8-sig')) if keep(x)]

rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
cols = list(rows[0].keys())
assert cols[5] == 'OSM브랜드'
out = []
for i, r in enumerate(rows):
    if r['흐름'] == 'OSM':
        x = osm[i]
        assert (x['PRODUCT_DESC'], x['RAW_URL'], x['BRAND']) == (r['상품명'], r['원본 상품 URL'], r['OSM브랜드']), r['행번호']
        brand = x['BRAND'].strip().upper()
        mpc = x['MPC'].strip()
        mc, src = (mpc.upper(), 'OSM 제공') if mpc not in ('', '\\N') else ('', '')
    else:
        assert r['흐름'] == '검색' and not r['OSM브랜드']
        target = BRANDS.get((r['국가'], CAT_KEY.get(r['제품군'], r['제품군'])), set())
        brand = ', '.join(sorted(brands_in(r['상품명'] + ' ' + slug(r['확인 요청 URL']), target)))
        mc, src = model_code(r['상품명'], r['확인 요청 URL'])
    o = {}
    for c in cols:
        if c == 'OSM브랜드':
            o['브랜드'] = brand; o['제품코드'] = mc; o['제품코드 출처'] = src
        else:
            o[c] = r[c]
    out.append(o)

with open(DST, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()), quoting=csv.QUOTE_MINIMAL)
    w.writeheader(); w.writerows(out)

# ---------- 검증 ----------
back = list(csv.DictReader(open(DST, encoding='utf-8-sig')))
assert len(back) == len(rows)
for a, b in zip(rows, back):
    for c in cols:
        if c != 'OSM브랜드':
            assert a[c] == b[c], (a['행번호'], c)
# 1단계 판정과 일관성: 검색 행에서 브랜드를 못 찾은 행 == ①브랜드 제외 행
srch = [b for b in back if b['흐름'] == '검색']
assert all((not b['브랜드']) == (b['제외단계'] == '①브랜드') for b in srch)
cnt = collections.Counter
stat = {
    'source_sha256': hashlib.sha256(open(SRC, 'rb').read()).hexdigest(),
    'output_sha256': hashlib.sha256(open(DST, 'rb').read()).hexdigest(),
    'rows': len(back), 'columns': list(back[0].keys()),
    '모수 포함 여부': cnt(b['모수 포함 여부'] for b in back),
    '브랜드 빈칸(흐름별)': cnt(b['흐름'] for b in back if not b['브랜드']),
    '브랜드 여러 개': sum(',' in b['브랜드'] for b in back),
    'LG 포함 행(흐름×판정)': {f'{k[0]}|{k[1]}': v for k, v in cnt((b['흐름'], b['모수 포함 여부']) for b in back if 'LG' in b['브랜드'].split(', ')).items()},
    '제품코드 출처(판정별)': {f'{k[0]}|{k[1] or "빈칸"}': v for k, v in cnt((b['모수 포함 여부'], b['제품코드 출처']) for b in back).items()},
}
json.dump(stat, open(HERE + '/verification.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(stat, ensure_ascii=False, indent=1))
