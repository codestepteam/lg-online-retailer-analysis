import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mix_common import *
O = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'Australia_Appliance_Online'
EXTRA = {'FISHER & PAYKEL', 'MITSUBISHI ELECTRIC', 'CHIQ', 'MYKIN', 'ARTUSI', 'ASKO', 'FHIABA', 'SEIKI', 'LINARIE',
         'HUSKY', 'TELEFUNKEN', 'KINGSBOTTLE', 'ESATTO', 'EUROTECH', 'RINNAI', 'ONIX', 'NEFF', 'ILVE', 'BROMIC',
         'RHINO', 'INALTO', 'AIRFLO', 'DOMETIC', 'EUROMAID', 'SPEED QUEEN', 'SMART', 'LG', 'SMEG'}
ALIAS = {'MITSUBISHI': 'MITSUBISHI ELECTRIC', 'FISHER': 'FISHER & PAYKEL', 'SPEED': 'SPEED QUEEN'}


def page_info(h):
    """JSON-LD Product 의 brand.name 과 sku (이 리테일러는 sku 가 곧 제조사 모델)."""
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        for x in (d if isinstance(d, list) else [d]):
            if isinstance(x, dict) and x.get('@type') == 'Product':
                b = x.get('brand')
                b = b.get('name') if isinstance(b, dict) else b
                return norm_brand(b or ''), clean(str(x.get('mpn') or x.get('sku') or '')).upper()
    return '', ''


def main():
    inp = rd(f'{O}/inputs/{NAME}.csv')
    pages, brands = {}, set()
    for r in inp:
        h = load(r['HTML경로'])
        if h:
            pages[r['행번호']] = (h,) + page_info(h)
            if pages[r['행번호']][1]: brands.add(pages[r['행번호']][1])
    print('page brands', sorted(brands))
    rows = []
    for r in inp:
        name = r['상품명']; p = pages.get(r['행번호'])
        b = c = ''; bs = cs = '없음'
        if p:
            if p[1]: b, bs = p[1], '페이지'
            if p[2]: c, cs = p[2], '페이지'
        if not b:
            b = brand_from_text(name, brands | EXTRA, ALIAS)
            if b: bs = '상품명'
        if not c:
            c = tail_code(name, p[0] if p else None) or pick_code(name, p[0] if p else None) or spaced_tail(name, p[0] if p else None)
            if c: cs = '상품명'
        rows.append([r['행번호'], r['확인 요청 URL'], b, c, bs, cs])
    write(f'{O}/parts/{NAME}.csv', rows)
    report(inp, rows)


main()
