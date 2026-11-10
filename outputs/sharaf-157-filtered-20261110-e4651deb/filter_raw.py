"""Apply existing Sharaf DG rules to frozen raw rows; preserve every input row."""
import collections
import csv
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RAW = ROOT / 'outputs/sharaf-157-raw-toggle-20261110-267a8cbc/상품카드.csv'
PRIOR = ROOT / 'outputs/sharaf-157-october-filter-20261110'


def load_rules():
    spec = importlib.util.spec_from_file_location('prior_audit', PRIOR / 'audit_filter.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.original_rules()


def product_key(url):
    """Historical comparison only; never used to exclude current duplicate rows."""
    return urlsplit(url).path.rstrip('/').lower()


def page_judgement(obs, rules):
    if not obs or obs['status'] != 'observed' or not obs.get('title'):
        return '검토 필요', '', '본 상품 상세 화면 확인 필요'
    if obs['seller'] != 'Sharaf DG' or obs['sellerHref'] != '/store/sdg':
        return '제외', '③리리부', '본 상품 외부 판매자: ' + obs['seller']
    hit = rules['kw_hit']('UAE', obs['title'])
    if hit:
        return '제외', '③리리부', f'본 상품 제목의 {hit[0]} 키워드: {hit[1]}'
    state, why = rules['category_check']('REF', obs['title'])
    if state == '제외':
        return '제외', '②제품군', '본 상품 상세 제목의 대상 외 제품군: ' + why
    if re.search(r'\bpermanently (?:unavailable|out of stock)\b|\bdiscontinued\b|no longer available', obs['deliveryText'], re.I):
        return '제외', '④영구품절', '본 상품 판매 영역에 영구 판매 불가 표시'
    return '포함', '', '상품명 기준 통과; 본 상품 Sharaf DG 직판·정상 상품 화면 확인'


def main():
    rules = load_rules()
    with RAW.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        original_columns = list(reader.fieldnames)
        inputs = list(reader)
    assert len(inputs) == 1239
    original_hash = hashlib.sha256(RAW.read_bytes()).hexdigest()
    old_file = next((ROOT / 'pdp 모수 추출/최종_20261029').glob('PDP모수_공유용_v5_*.csv'))
    with old_file.open(encoding='utf-8-sig', newline='') as f:
        old = [r for r in csv.DictReader(f) if r['리테일러'] == 'Sharaf DG' and r['모수 포함 여부'] == '포함']
    assert len(old) == 16
    old_by_path = {product_key(r['확인 요청 URL']): r for r in old}
    observations = {}
    for directory in [PRIOR, OUT]:
        for line in (directory / 'pdp-observations.jsonl').read_text().splitlines():
            obs = json.loads(line)
            obs['evidence'] = str(directory.relative_to(ROOT) / 'pdp-snapshots' / (f"{obs['id']:03d}.txt" if directory == PRIOR else f"{obs['id']}.txt"))
            assert (ROOT / obs['evidence']).is_file()
            observations[obs['requestedURL']] = obs
    fixture = {'status':'observed','title':'LG Upright Freezer','seller':'Sharaf DG','sellerHref':'/store/sdg','deliveryText':'Out of Stock'}
    assert page_judgement(fixture, rules)[0] == '포함'
    assert page_judgement({**fixture,'seller':'Marketplace'}, rules)[1] == '③리리부'
    assert page_judgement({**fixture,'deliveryText':'Permanently unavailable'}, rules)[1] == '④영구품절'
    assert page_judgement(None, rules)[0] == '검토 필요'
    assert page_judgement({**fixture,'title':'LG Styler'}, rules)[1] == '②제품군'
    results, exact_first, actual_first = [], {}, {}
    for index, row in enumerate(inputs, 1):
        div = 'REF' if row['F열제품군'] == 'Refrigerator' else 'W/M'
        url = row['카드PDP링크']
        inp = {'국가':'UAE','리테일러':'Sharaf DG','제품군':div,'상품명':row['상품명'],'URL':url,'흐름':'검색','OSM브랜드':''}
        state, stage, reason, memo = rules['judge'](inp, 'B')
        brands = sorted(rules['brands_in'](row['상품명']+' '+rules['slug'](url), rules['BRANDS'][('UAE',div)]))
        obs = observations.get(url) if state != '제외' else None
        representative = ''
        if state != '제외':
            if url in exact_first:
                state, stage, reason = '제외', '④중복', '같은 요청 URL 중복'
                representative = exact_first[url]
            else:
                exact_first[url] = index
                state, stage, reason = page_judgement(obs, rules)
                if state == '포함' and memo.startswith('부품 의심'):
                    state, reason = '검토 필요', '부품 의심: 실제 상품 종류 확인 필요'
                if state == '포함':
                    actual = obs['actualURL']
                    if actual in actual_first:
                        state, stage, reason = '제외', '④중복', '실제 도착 URL 중복'
                        representative = actual_first[actual]
                    else:
                        actual_first[actual] = index
        old_match = old_by_path.get(product_key(url))
        comparison = ''
        if state != '제외':
            comparison = '기존 포함 상품' if old_match else ('추가 대상' if state == '포함' else '추가 후보(검토 필요)')
        results.append({**row, '원본행번호':index,'브랜드':','.join(brands),'판정제품군':div,
            '모수 포함 여부':state,'제외단계':stage,'판정사유':reason,'메모':memo,'대표원본행번호':representative,
            '판매자':obs['seller'] if obs else '', '실제도착URL':obs['actualURL'] if obs else '',
            '상세확인시각':obs['checkedAt'] if obs else '', '상세확인근거':obs['evidence'] if obs else '',
            '재고참고':'단순 품절(제외하지 않음)' if obs and 'out of stock' in obs['deliveryText'].lower() else '',
            '기존16개비교':comparison,'기존행번호':old_match['행번호'] if old_match else '',
            '기존URL':old_match['확인 요청 URL'] if old_match else '',
            '기존상품URL변경':'Y' if old_match and old_match['확인 요청 URL']!=url else ''})
    included = [r for r in results if r['모수 포함 여부']=='포함']
    assert len(included) == len({r['카드PDP링크'] for r in included}) == len({r['실제도착URL'] for r in included})
    assert all(r['판매자']=='Sharaf DG' and r['상세확인근거'] for r in included)
    assert all({k:r[k] for k in original_columns} == inputs[i] for i,r in enumerate(results))
    assert hashlib.sha256(RAW.read_bytes()).hexdigest() == original_hash
    columns = list(results[0])
    matrix = [columns] + [[r[k] for k in columns] for r in results]
    (OUT/'result-matrix.json').write_text(json.dumps(matrix, ensure_ascii=False))
    seen_paths = {product_key(r['카드PDP링크']) for r in included}
    missing_old = [r for r in old if product_key(r['확인 요청 URL']) not in seen_paths]
    (OUT/'existing16-not-found.json').write_text(json.dumps(missing_old,ensure_ascii=False,indent=2))
    summary = {'raw_rows':len(inputs),'states':dict(collections.Counter(r['모수 포함 여부'] for r in results)),
        'exclusion_stages':dict(collections.Counter(r['제외단계'] for r in results if r['모수 포함 여부']=='제외')),
        'old_included':16,'overlap':sum(r['기존16개비교']=='기존 포함 상품' for r in included),
        'additional':sum(r['기존16개비교']=='추가 대상' for r in included),'old_not_found':len(missing_old),
        'pdp_reused':sum(r['상세확인근거'].startswith(str(PRIOR.relative_to(ROOT))) for r in included),
        'pdp_new':sum(r['상세확인근거'].startswith(str(OUT.relative_to(ROOT))) for r in included),
        'temporary_out_of_stock_kept':sum(bool(r['재고참고']) for r in included),
        'per_brand':[{'brand':b,'REF':sum(r['브랜드']==b and r['판정제품군']=='REF' for r in included),
            'W/M':sum(r['브랜드']==b and r['판정제품군']=='W/M' for r in included),
            'additional':sum(r['브랜드']==b and r['기존16개비교']=='추가 대상' for r in included)} for b in ['LG','SAMSUNG','BOSCH','HISENSE']],
        'validation':'All 1239 original rows and 14 original columns unchanged; unique included request/actual URLs; main seller and evidence present; five policy fixtures passed',
        'source_raw_sha256':original_hash,'source_old_file':str(old_file.relative_to(ROOT)),
        'failures':[],'unresolved':[r['원본행번호'] for r in results if r['모수 포함 여부']=='검토 필요']}
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
