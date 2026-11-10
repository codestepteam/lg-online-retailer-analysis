"""Replay Sharaf DG's October name filters, then join current PDP evidence.

Reads frozen search observations and the October v5 file. Never modifies inputs.
The original step1 definitions are executed without its input/output sections.
"""
import ast
import collections
import csv
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'pdp 모수 추출/최종_20261029/판정근거/스크립트/step1_filter.py'
SEARCH = ROOT / 'outputs/sharaf-157-live-toggle-20261109/search-terms/all-search-results.json'
OCTOBER = next((ROOT / 'pdp 모수 추출/최종_20261029').glob('PDP모수_공유용_v5_*.csv'))


def key(url):
    return urlsplit(url).path.rstrip('/').lower()


def original_rules():
    source = SOURCE.read_text()
    # The prefix only reads the reference workbook and defines original helpers.
    prefix = source.split('# ---------- 입력 읽기 ----------')[0]
    scope = {'__name__': 'october_rules'}
    prefix_tree = ast.parse(prefix)
    prefix_tree.body = [n for n in prefix_tree.body if not (
        isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'OUT' for t in n.targets)
    )]
    exec(compile(prefix_tree, str(SOURCE), 'exec'), scope)
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in {'cat_key', 'judge'}:
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(SOURCE), 'exec'), scope)
    scope['FR58'] = set()
    return scope


def main():
    rules = original_rules()
    with OCTOBER.open(encoding='utf-8-sig', newline='') as f:
        old = [r for r in csv.DictReader(f) if r['리테일러'] == 'Sharaf DG']
    old_by_path = collections.defaultdict(list)
    for r in old:
        old_by_path[key(r['확인 요청 URL'])].append(r)
    old_included = {key(r['확인 요청 URL']): r for r in old if r['모수 포함 여부'] == '포함'}
    assert len(old_included) == 16
    current = {}
    search = json.loads(SEARCH.read_text())
    for result in search['results']:
        for page in result['pages']:
            for card in page['cards']:
                k = key(card['url'])
                if k not in current:
                    current[k] = {
                        'id': len(current) + 1,
                        'product_path': k,
                        'title': card['title'],
                        'url': card['url'],
                        'group': result['group'],
                        'terms': [],
                        'observed_offer_urls': [],
                    }
                item = current[k]
                if result['term'] not in item['terms']:
                    item['terms'].append(result['term'])
                if card['url'] not in item['observed_offer_urls']:
                    item['observed_offer_urls'].append(card['url'])
    assert len(current) == 120
    rows = []
    for k, item in current.items():
        div = 'REF' if item['group'] == 'fridges_freezers' else 'W/M'
        original_input = {
            '국가': 'UAE', '리테일러': 'Sharaf DG',
            '제품군': div, '상품명': item['title'], 'URL': item['url'],
            '흐름': '검색', 'OSM브랜드': '',
        }
        state, stage, reason, memo = rules['judge'](original_input, 'B')
        found = rules['brands_in'](item['title'] + ' ' + rules['slug'](item['url']), rules['BRANDS'][('UAE', div)])
        # The filter selection identifies Hisense even when the source title is misspelled.
        brand = found[0] if len(found) == 1 else ('HISENSE' if item['title'].lower().startswith('hisesne ') else '')
        rows.append({
            **item, 'brand': brand, 'division': div,
            'name_filter_state': state, 'name_filter_stage': stage,
            'name_filter_reason': reason, 'name_filter_memo': memo,
            'october_included_same_product': k in old_included,
            'october_rows': [
                {c: r[c] for c in ['행번호','브랜드','상품명','확인 요청 URL','모수 포함 여부','제외단계','제외사유','판매자','판매자구분']}
                for r in old_by_path.get(k, [])
            ],
        })
    # Policy fixtures protect the distinction between freezer and clothing Styler.
    fixture = {'국가':'UAE','리테일러':'Sharaf DG','제품군':'REF','흐름':'검색','OSM브랜드':''}
    def judge_title(title):
        return rules['judge']({**fixture,'상품명':title,'URL':'https://uae.sharafdg.com/product/sample/'},'B')
    assert judge_title('LG Upright Freezer 324 Litres')[0] == '통과'
    assert judge_title('LG Styler with TrueSteam')[0] == '제외'
    assert judge_title('LG Refurbished Refrigerator')[0] == '제외'
    assert judge_title('Hisesne Side By Side Refrigerator')[0] == '제외'
    payload = {
        'sources': {'search':str(SEARCH.relative_to(ROOT)), 'october':str(OCTOBER.relative_to(ROOT)),
                    'name_rules':str(SOURCE.relative_to(ROOT)), 'name_rules_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()},
        'search_checked_at':search['checkedAt'],
        'comparison_key':'Product URL path; ignore promo offer ID for existing-product comparison only. Retain exact offer URL for seller verification.',
        'rows':rows,
        'october_included_not_in_search':[r for k,r in old_included.items() if k not in current],
    }
    (OUT / 'name-filter-and-october-match.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
    tasks = [{c:r[c] for c in ['id','title','url','product_path','brand','division']} for r in rows if r['name_filter_state'] != '제외']
    (OUT / 'pdp-check-tasks.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2))
    print(json.dumps({'input':len(rows),'name_filter':dict(collections.Counter(r['name_filter_state'] for r in rows)),
                      'excluded':[{c:r[c] for c in ['id','title','name_filter_reason']} for r in rows if r['name_filter_state']=='제외'],
                      'pdp_checks_needed':len(tasks),'old_included_overlap':sum(r['october_included_same_product'] for r in rows),
                      'old_included_not_in_search':len(payload['october_included_not_in_search']),
                      'fixtures':'4 assertions passed'},ensure_ascii=False,indent=2))


def finalize():
    data = json.loads((OUT / 'name-filter-and-october-match.json').read_text())
    observations = [json.loads(line) for line in (OUT / 'pdp-observations.jsonl').read_text().splitlines() if line.strip()]
    by_id = {r['id']:r for r in observations}
    expected = {r['id'] for r in data['rows'] if r['name_filter_state'] != '제외'}
    assert len(observations) == len(by_id) == 119
    assert set(by_id) == expected
    canonical_first = {}
    for row in data['rows']:
        if row['name_filter_state'] == '제외':
            row.update(final_state='제외',final_reason=row['name_filter_reason'])
            continue
        obs = by_id[row['id']]
        row['pdp_observation'] = obs
        row['pdp_snapshot'] = 'pdp-snapshots/' + f"{row['id']:03d}.txt"
        assert obs['status'] == 'observed', obs
        assert key(obs['actualURL']) == key(row['url'])
        assert obs['canonical'], obs['id']
        row['stock_note'] = '현재 품절 표시(10월 Sharaf 기준상 단순 품절만으로 제외하지 않음)' if 'out of stock' in obs['deliveryText'].lower() else ''
        if obs['seller'] != 'Sharaf DG' or obs['sellerHref'] != '/store/sdg':
            row.update(final_state='제외',final_reason='본 상품의 외부 판매자: ' + obs['seller'])
            continue
        ck = key(obs['canonical'])
        if ck in canonical_first:
            row.update(final_state='제외',final_reason=f'대표 주소 중복: {canonical_first[ck]}번')
            continue
        canonical_first[ck] = row['id']
        # A visible normal PDP and main seller were checked. No permanent-closure
        # wording was found in the main offer. Historical HTTP status is not reused.
        assert not any(w in obs['priceText'].lower() for w in ('permanently','discontinued','refurbished','pre-owned','open-box'))
        row.update(final_state='포함',final_reason='10월 상품명 기준 통과; 본 상품 Sharaf DG 직판·정상 상품 화면·대표 주소 중복 없음')
    included = [r for r in data['rows'] if r['final_state']=='포함']
    overlap = [r for r in included if r['october_included_same_product']]
    additional = [r for r in included if not r['october_included_same_product']]
    offer_updates = [r for r in overlap if not any(o['모수 포함 여부']=='포함' and o['확인 요청 URL']==r['url'] for o in r['october_rows'])]
    summary = []
    for b in ['LG','SAMSUNG','BOSCH','HISENSE']:
        total = [r for r in included if r['brand']==b]
        new = [r for r in additional if r['brand']==b]
        overlap_rows = [r for r in overlap if r['brand']==b]
        old_missing = [r for r in data['october_included_not_in_search'] if r['브랜드']==b]
        summary.append({'brand':b,'october_count':len(overlap_rows)+len(old_missing),
                        'current_filtered_ref':sum(r['division']=='REF' for r in total),
                        'current_filtered_wm':sum(r['division']=='W/M' for r in total),
                        'current_filtered_total':len(total),'overlap':len(overlap_rows),
                        'additional_ref':sum(r['division']=='REF' for r in new),
                        'additional_wm':sum(r['division']=='W/M' for r in new),
                        'additional_total':len(new),'existing_offer_url_updates':sum(r['brand']==b for r in offer_updates)})
    assert len(included)==119 and len(overlap)==13 and len(additional)==106
    assert len(data['october_included_not_in_search'])==3 and len(offer_updates)==3
    assert len({key(r['url']) for r in additional})==106
    assert sum(r['additional_total'] for r in summary)==106
    totals = {'raw_search_products':120,'filtered_included':len(included),'excluded':120-len(included),
              'pdp_checked':119,'pdp_unresolved':0,'october_included':16,'overlap_products':len(overlap),
              'additional_products':len(additional),'additional_previously_excluded_in_october':sum(bool(r['october_rows']) for r in additional),
              'additional_not_in_october_input':sum(not r['october_rows'] for r in additional),
              'existing_products_with_offer_url_update':len(offer_updates),
              'october_products_not_found_in_current_search':3,
              'temporary_out_of_stock_kept':sum(bool(r['stock_note']) for r in included),
              'union_if_old16_retained_and_additions_applied':16+len(additional)}
    report = {**data,'pdp_checked_from':min(r['checkedAt'] for r in observations),
              'pdp_checked_to':max(r['checkedAt'] for r in observations),'summary':summary,'totals':totals,
              'policy_notes':['D065: standalone freezers are included in REF. Previous chat excluded one incorrectly; corrected here.',
                              'UAE name/brand/refurbishment/parts criteria replay original step1_filter.py definitions and v2.2 workbook.',
                              'Main seller verified from visible delivery offer; recommendations and Other Sellers ignored.',
                              'Generic Out of Stock alone was not an exclusion in the October Sharaf logic; 37 observations retained.',
                              'The Hisesne spelling error is excluded to reproduce the October name filter exactly; no new correction rule invented.',
                              'Count additional products by product path; promo differences for existing products are URL updates, not new products.',
                              'Current November observations do not prove October availability. No source CSV, database, or Dooray post was changed.'],
              'additional_ids':[r['id'] for r in additional], 'existing_offer_update_ids':[r['id'] for r in offer_updates]}
    (OUT/'filtered-comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    (OUT/'additional-products.json').write_text(json.dumps(additional,ensure_ascii=False,indent=2))
    (OUT/'additional-106-urls.txt').write_text(''.join(r['url']+'\n' for r in additional))
    (OUT/'existing-product-offer-url-updates-3.json').write_text(json.dumps(offer_updates,ensure_ascii=False,indent=2))
    (OUT/'october-products-not-in-current-search-3.json').write_text(json.dumps(data['october_included_not_in_search'],ensure_ascii=False,indent=2))
    print(json.dumps({'summary':summary,'totals':totals},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
    if '--finalize' in sys.argv:
        finalize()
