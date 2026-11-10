"""Prepare/verify v7; replace Sharaf DG only and preserve all other 26-column rows."""
import collections
import csv
import hashlib
import html
import json
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FINAL = ROOT / 'pdp 모수 추출/최종_20261029'
SOURCE = next(p for p in FINAL.glob('*.csv') if unicodedata.normalize('NFC',p.name).startswith('PDP모수_공유용_v6_'))
FRESH = ROOT / 'outputs/sharaf-157-filtered-20261110-e4651deb/Sharaf DG 두레이 157 적용_필터결과.csv'
RAW_DIR = ROOT / 'outputs/sharaf-157-raw-toggle-20261110-267a8cbc'
NAME = 'PDP모수_공유용_v7_SharafDG직판재조사교체_25개국_35개리테일러_전체판정_54443행_20261110.csv'


def read(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames), list(reader)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(url):
    return urlsplit(url).path.rstrip('/').lower()


def prepare():
    columns, base = read(SOURCE)
    _, fresh = read(FRESH)
    sharaf = [r for r in base if r['리테일러']=='Sharaf DG']
    preserved = [r for r in base if r['리테일러']!='Sharaf DG']
    assert (len(base),len(columns),len(sharaf),len(fresh)) == (55997,26,2793,1239)
    metadata = {}
    for line in (RAW_DIR/'raw-pages.jsonl').read_text().splitlines():
        for card in json.loads(line)['cards']:
            metadata[card['url']] = card['attributes']
    codes = collections.defaultdict(set)
    for row in sharaf:
        if row['제품코드']:
            codes[key(row['확인 요청 URL'])].add(row['제품코드'])
    start = max(int(r['행번호']) for r in base)
    changed = []
    for index,row in enumerate(fresh,1):
        assert int(row['원본행번호'])==index
        new_id = start + index
        code = codes[key(row['카드PDP링크'])]
        product_code = next(iter(code)) if len(code)==1 else ''
        notes = [row['메모'], '두레이 #157 직판 토글 재조사(2026-11-10)',f'재조사 원본행 {index}']
        if row['기존16개비교']:
            notes.append(row['기존16개비교'])
        if row['기존행번호']:
            notes.append('v6 기존 포함행 '+row['기존행번호'])
        if row['모수 포함 여부']=='포함':
            notes.append(row['판정사유'])
        reason = row['판정사유'] if row['모수 포함 여부']=='제외' else ''
        if row['대표원본행번호']:
            reason += f"(대표 행 {start+int(row['대표원본행번호'])})"
        brand = row['브랜드'] or html.unescape(metadata[row['카드PDP링크']].get('data-brand','')).upper()
        evidence = ('본 상품 판매 영역의 Sold by(판매자): Sharaf DG; '+row['상세확인시각']+'; '+row['상세확인근거']) if row['상세확인근거'] else ''
        mapped = {'행번호':str(new_id),'흐름':'검색','국가':'UAE','리테일러':'Sharaf DG',
            '제품군':row['판정제품군'],'브랜드':brand,'제품코드':product_code,'OSM브랜드':'',
            '상품명':row['상품명'],'확인 요청 URL':row['카드PDP링크'],'원본 상품 URL':row['카드PDP링크'],
            '기준일':row['수집시각'][:10],'검색어':row['J열검색어'],'엑셀행번호':row['엑셀행번호'],
            '광고여부':row['광고여부'],'출처파일':str((RAW_DIR/'상품카드.csv').relative_to(ROOT)),
            '모수 포함 여부':row['모수 포함 여부'],'제외단계':row['제외단계'],'제외사유':reason,
            '메모':'; '.join(n for n in notes if n),
            '페이지확인규칙':'본 상품 Sold by(판매자)가 Sharaf DG 이외면 제외; 추천·다른 판매자 목록 제외',
            '페이지 접속 확인 결과':'정상' if row['상세확인근거'] else '',
            '접속 후 URL':row['실제도착URL'],'판매자':row['판매자'],
            '판매자구분':'직판' if row['판매자']=='Sharaf DG' else '', '판매자근거':evidence}
        assert set(mapped)==set(columns)
        changed.append([mapped[c] for c in columns])
    expected = [[r[c] for c in columns] for r in preserved]+changed
    assert len(expected)==54443
    assert len({r[0] for r in expected})==54443
    package = {'columns':columns,'preserved':[[r[c] for c in columns] for r in preserved],'changed':changed,
        'name':NAME,'output_paths':[str(FINAL/NAME),str(Path('/Users/codestepseunghee/Downloads')/NAME)],
        'source':str(SOURCE),'source_sha256':digest(SOURCE),'fresh':str(FRESH),'fresh_sha256':digest(FRESH),
        'new_row_id_range':[start+1,start+len(fresh)]}
    (OUT/'prepared.json').write_text(json.dumps(package,ensure_ascii=False))
    print(json.dumps({'preserved':len(preserved),'replacement':len(changed),'new_row_id_range':package['new_row_id_range'],'output':NAME},ensure_ascii=False))


def verify():
    package=json.loads((OUT/'prepared.json').read_text())
    columns,base=read(SOURCE)
    new_columns,rows=read(FINAL/NAME)
    _,fresh=read(FRESH)
    assert columns==new_columns and len(columns)==26
    assert len(rows)==54443 and len({r['행번호'] for r in rows})==54443
    old_other=[r for r in base if r['리테일러']!='Sharaf DG']
    new_other=[r for r in rows if r['리테일러']!='Sharaf DG']
    assert new_other==old_other  # All 53,204 x 26 cells, row IDs and order unchanged.
    sha=[r for r in rows if r['리테일러']=='Sharaf DG']
    assert len(sha)==len(fresh)==1239
    for index,(original,converted) in enumerate(zip(fresh,sha),1):
        for a,b in [('상품명','상품명'),('카드PDP링크','확인 요청 URL'),('카드PDP링크','원본 상품 URL'),
                    ('모수 포함 여부','모수 포함 여부'),('제외단계','제외단계'),('J열검색어','검색어'),('엑셀행번호','엑셀행번호')]:
            assert original[a]==converted[b], (index,a)
        assert converted['기준일']=='2026-11-10'
        assert int(converted['행번호'])==55997+index
    states=collections.Counter(r['모수 포함 여부'] for r in rows)
    assert states=={'포함':10311,'제외':44132}
    assert collections.Counter(r['모수 포함 여부'] for r in sha)=={'포함':116,'제외':1123}
    inc=[r for r in sha if r['모수 포함 여부']=='포함']
    assert len({r['확인 요청 URL'] for r in inc})==len({r['접속 후 URL'] for r in inc})==116
    assert all(r['판매자']=='Sharaf DG' and r['판매자근거'] for r in inc)
    assert digest(SOURCE)==package['source_sha256'] and digest(FRESH)==package['fresh_sha256']
    targets=[Path(p) for p in package['output_paths']]
    assert targets[0].read_bytes()==targets[1].read_bytes()
    oldinc={key(r['확인 요청 URL']) for r in base if r['리테일러']=='Sharaf DG' and r['모수 포함 여부']=='포함'}
    newinc={key(r['확인 요청 URL']) for r in inc}
    assert (len(oldinc&newinc),len(newinc-oldinc),len(oldinc-newinc))==(12,104,4)
    result={'rows':len(rows),'columns':len(columns),'v6':dict(collections.Counter(r['모수 포함 여부'] for r in base)),
        'v7':dict(states),'included_increase':100,'other_rows_unchanged':len(old_other),
        'sharaf':{'rows':len(sha),'included':116,'excluded':1123,'overlap':12,'additional':104,'old_not_found':4},
        'brand_included':dict(collections.Counter(r['브랜드'] for r in inc)),
        'countries':len({r['국가'] for r in rows}),'retailer_country_pairs':len({(r['국가'],r['리테일러']) for r in rows}),
        'new_row_id_range':package['new_row_id_range'],'all_original_source_hashes_unchanged':True,
        'copies_identical':True,'v7_sha256':digest(targets[0]),'csv_failures':[],
        'commands':['python3 build_v7.py','node export_v7.mjs','python3 build_v7.py --verify'],
        'output_paths':package['output_paths']}
    (OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    verify() if '--verify' in sys.argv else prepare()
