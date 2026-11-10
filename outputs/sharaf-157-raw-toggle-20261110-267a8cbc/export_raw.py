"""Export observed search cards as raw data; preserve every row and exact URL."""
import csv
import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

OUT = Path(__file__).resolve().parent
TERMS = [
    (157, 'bottom freezer refrigerator', 'Refrigerator'),
    (158, 'french door refrigerator', 'Refrigerator'),
    (159, 'refrigerator', 'Refrigerator'),
    (160, 'side by side fridge', 'Refrigerator'),
    (161, 'top freezer refrigerator', 'Refrigerator'),
    (162, 'front load washer', 'Washing Machine'),
    (163, 'top load washer', 'Washing Machine'),
    (164, 'washer dryer', 'Washing Machine'),
    (165, 'washing machine', 'Washing Machine'),
]
COLS = ['엑셀행번호','국가','리테일러','F열제품군','J열검색어','최종검색결과URL',
        '페이지번호','카드순번','상품명','카드PDP링크','광고여부','표시된전체수','수집시각','접속국가']


def make_rows(pages):
    rows = []
    for page in pages:
        for i, card in enumerate(page['cards'], 1):
            rows.append(dict(zip(COLS, [page['excelRow'],'UAE','Sharaf DG',page['productGroup'],
                page['term'],page['url'],page['page'],i,card['title'],card['url'],
                '광고 표시' if card.get('sponsored') else '표시 없음',page['displayedTotal'],
                page['checkedAt'],'미확인'])))
    return rows


def self_test():
    page = {'excelRow':157,'term':TERMS[0][1],'productGroup':'Refrigerator','url':'https://example.test/',
            'page':1,'displayedTotal':2,'checkedAt':'2026-11-10T00:00:00Z',
            'cards':[{'title':'Test Brand Refrigerator','url':'https://example.test/p/?promo=1','sponsored':True},
                     {'title':'Test Brand Refrigerator','url':'https://example.test/p/?promo=1','sponsored':False}]}
    rows = make_rows([page,dict(page,excelRow=158,term=TERMS[1][1])])
    assert len(rows)==4  # Same-page and cross-term duplicate rows are preserved.
    assert all(r['카드PDP링크'].endswith('?promo=1') for r in rows)
    assert rows[0]['광고여부']=='광고 표시' and rows[1]['광고여부']=='표시 없음'
    assert list(rows[0])==COLS and rows[2]['J열검색어']==TERMS[1][1]
    print('self-test: duplicate rows, exact promo URL, ad label, and original column order preserved')


def export():
    pages = [json.loads(line) for line in (OUT/'raw-pages.jsonl').read_text().splitlines() if line.strip()]
    page_keys = [(p['term'],p['page']) for p in pages]
    assert len(page_keys)==len(set(page_keys)), 'Repeated page observation: resolve explicitly before export'
    order = {t[1]:i for i,t in enumerate(TERMS)}
    pages.sort(key=lambda p:(order[p['term']],p['page']))
    for p in pages:
        q = parse_qs(urlsplit(p['url']).query)
        assert q['q']==[p['term']]
        assert p['soldByChecked'] and p['selectedBrands']==[]
        assert q['dFR[promotion_offer_json.seller_code][0]']==['sdg']
        assert q['dFR[promotion_offer_json.seller_code][1]']==['sdg_online_excl']
        assert not any(k.startswith('dFR[taxonomies.attr.Brand]') for k in q)
        assert not any(k.startswith('hFR[') for k in q), 'Category restriction must not be applied'
        assert all(c['title'] and '/product/' in c['url'] for c in p['cards'])
    summaries = []
    for excel_row,term,group in TERMS:
        ps = [p for p in pages if p['term']==term]
        assert ps, term
        assert [p['page'] for p in ps]==list(range(1,len(ps)+1)), term
        cards = [c for p in ps for c in p['cards']]
        shown = [p['displayedTotal'] for p in ps]
        assert len(set(shown))==1, (term,shown)
        assert len(cards)==shown[0], (term,len(cards),shown[0])
        summaries.append({'엑셀행번호':excel_row,'검색어':term,'제품군':group,
            '사이트 표시 수':shown[0],'저장 카드 수':len(cards),'확인 페이지 수':len(ps),
            '고유 정확 URL 수':len({c['url'] for c in cards}),'직판 토글':'ON','브랜드 필터':'없음',
            '중복 행 처리':'보존','대조 결과':'표시 수와 저장 수 일치'})
    rows = make_rows(pages)
    with (OUT/'상품카드.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=COLS);writer.writeheader();writer.writerows(rows)
    with (OUT/'검색어별_건수대조.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(summaries[0]));writer.writeheader();writer.writerows(summaries)
    (OUT/'원본_URL_중복유지.txt').write_text(''.join(r['카드PDP링크']+'\n' for r in rows))
    result={'conditions':'Existing 9 Search Terms; Sold By Sharaf DG ON; no brand/category/refurbishment/parts/stock/other downstream filter; retain all repeated rows and exact promo URLs',
        'first_checked_at':min(p['checkedAt'] for p in pages),'last_checked_at':max(p['checkedAt'] for p in pages),
        'search_terms':9,'pages':len(pages),'raw_rows':len(rows),'unique_exact_urls':len({r['카드PDP링크'] for r in rows}),
        'unique_product_paths':len({urlsplit(r['카드PDP링크']).path.rstrip('/') for r in rows}),
        'sponsored_cards':sum(r['광고여부']=='광고 표시' for r in rows),'failures':[],
        'access_country':'Not verified; target website country is UAE, actual network country not asserted',
        'per_term':summaries}
    (OUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    with (OUT/'상품카드.csv').open(encoding='utf-8-sig',newline='') as f:
        saved=list(csv.DictReader(f))
    assert len(saved)==len(rows)
    assert [r['카드PDP링크'] for r in saved]==[r['카드PDP링크'] for r in rows]
    assert (OUT/'원본_URL_중복유지.txt').read_text().splitlines()==[r['카드PDP링크'] for r in rows]
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    self_test()
    if '--self-test' not in sys.argv:
        export()
