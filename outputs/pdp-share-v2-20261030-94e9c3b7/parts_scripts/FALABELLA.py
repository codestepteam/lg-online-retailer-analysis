import os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mix_common import *
O = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'Peru_FALABELLA'
EXTRA = {'INDURAMA', 'VENTUS', 'MABE', 'COLDEX', 'OSTER', 'DAEWOO', 'SANKEY', 'FRIGIDAIRE', 'ELECTROLUX', 'HISENSE',
         'WINIA', 'PHILCO', 'WHIRLPOOL', 'CONSUL', 'BRASTEMP', 'SOLE', 'IMACO', 'RECCO', 'KALLEY', 'KIRKLAND',
         'NEX', 'MIRAY', 'INNOVA', 'MIDEA', 'KOBLENZ', 'SAMSUNG', 'LG', 'BOSCH', 'HAIER', 'TCL', 'XIAOMI', 'KENMORE', 'BLACKLINE', 'AGHASO', 'TAURUS', 'REMINGTON', 'BABYLISS', 'GAMA'}
BAD_MODEL = {'', 'N/A', 'NA', 'NO APLICA', 'NO TIENE', 'SIN MODELO', 'GENERICO', 'GENÉRICO', 'NULL', '-', '.', 'S/M', 'NONE'}


def page_info(h):
    """상품 페이지면 (브랜드, 모델) 반환, 카테고리 목록 등 상품이 아니면 None."""
    x = re.search(r'"brandName":"([^"]*)"', h) or re.search(r'"brand":\{"@type":"Brand","name":"([^"]*)"\}', h)
    if not x:
        return None
    b = norm_brand(x.group(1))
    ms = re.findall(r'"name":"Modelo","value":"([^"]*)"', h)
    m = clean(ms[0]).upper() if ms else ''
    if m in BAD_MODEL:
        m = ''
    return b, m


def url_slug(u):
    m = re.search(r'/product/\d+/([^/?]+)', u)
    return urllib.parse.unquote(m.group(1)).replace('-', ' ') if m else ''


def main():
    inp = rd(f'{O}/inputs/{NAME}.csv')
    pages, brands = {}, set()
    nonprod = 0
    for r in inp:
        h = load(r['HTML경로'])
        if h:
            pi = page_info(h)
            if pi is None:
                nonprod += 1
                continue
            pages[r['행번호']] = (h,) + pi
            if pi[0]: brands.add(pi[0])
    print('product pages', len(pages), 'non-product (category) pages ignored', nonprod, 'brands', len(brands))
    rows = []
    for r in inp:
        name = r['상품명']; p = pages.get(r['행번호'])
        b = c = ''; bs = cs = '없음'
        if p:
            if p[1]: b, bs = p[1], '페이지'
            if p[2]: c, cs = p[2], '페이지'
        if not b:
            b = brand_from_text(name, brands | EXTRA)
            if b: bs = '상품명'
        if not b:
            b = brand_from_text(url_slug(r['확인 요청 URL']), brands | EXTRA)
            if b: bs = 'URL'
        if not c:
            c = pick_code(name, p[0] if p else None)
            if c: cs = '상품명'
        rows.append([r['행번호'], r['확인 요청 URL'], b, c, bs, cs])
    write(f'{O}/parts/{NAME}.csv', rows)
    report(inp, rows)


main()
