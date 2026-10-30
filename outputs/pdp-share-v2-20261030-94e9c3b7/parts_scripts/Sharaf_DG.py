import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mix_common import *
O = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'UAE_Sharaf_DG'
EXTRA = {'BAUMATIC', 'SANMICA', 'BERTAZZONI', 'MILLEN', 'AFRA', 'ECOFLOW', 'STARGOLD', 'EVVOLI', 'MILTON', 'KONKA',
         'YAMADA', 'VESTFROST', 'WOLF', 'WITFORMS', 'NINJA', 'KENWOOD', 'EMELCOLD', 'STAR TRACK', 'IMPEX', 'GRATUS',
         'EGNRL', 'VIDAXL', 'KARCHER', 'UWANT', 'JIMMY', 'BLACK+DECKER', 'SUPER GENERAL', 'SPJ'}
ALIAS = {'BLACK AND DECKER': 'BLACK+DECKER', 'BLACK & DECKER': 'BLACK+DECKER', 'HISESNE': 'HISENSE', 'AKAI420': 'AKAI'}


def page_info(h):
    b = m = ''
    x = re.search(r'<meta property="brand" content="([^"]*)"', h) or re.search(r'var flixConfig = \{[^}]*?"brand":"([^"]*)"', h) \
        or re.search(r'itemprop="brand"[^>]*>\s*<meta itemprop="name" content="([^"]*)"', h)
    if x: b = norm_brand(x.group(1))
    x = re.search(r'<meta itemprop="mpn" content="([^"]*)"', h) or re.search(r'"mpn":"([^"]*)"', h)
    if x: m = clean(x.group(1)).upper()
    return b, m


def main():
    inp = rd(f'{O}/inputs/{NAME}.csv')
    pages = {}
    brands = set()
    for r in inp:
        h = load(r['HTML경로'])
        if h:
            pages[r['행번호']] = (h,) + page_info(h)
            if pages[r['행번호']][1]: brands.add(pages[r['행번호']][1])
    rows = []
    for r in inp:
        name = r['상품명']; p = pages.get(r['행번호'])
        b = c = ''; bs = cs = '없음'
        if p:
            h, pb, pm = p
            if pb: b, bs = pb, '페이지'
            if pm and pm not in ('NULL', 'N/A', '-'): c, cs = re.sub(r'\s*\+\s*', ' + ', pm), '페이지'
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
