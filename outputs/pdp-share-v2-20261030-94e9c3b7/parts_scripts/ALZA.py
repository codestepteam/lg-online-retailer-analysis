import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cz_common import *
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = rd(f'{BASE}/inputs/Czech_Republic_ALZA.csv')
pages = {}
brands = set()
for r in rows:
    if r['HTML경로']:
        h = load(r['HTML경로']); pages[r['행번호']] = h
        if h:
            m = re.search(r'"brand":\{"@type":"Brand","name":"([^"]+)"', h)
            if m: brands.add(m.group(1).upper())
out = []
for r in rows:
    name = r['상품명']; h = pages.get(r['행번호'])
    b = bf = p = pf = ''
    if h:
        m = re.search(r'"brand":\{"@type":"Brand","name":"([^"]+)"', h)
        if m: b, bf = H.unescape(m.group(1)).strip().upper(), '페이지'
        m = re.search(r'"mpn":"([^"]*)"', h)
        mpn = H.unescape(m.group(1)).strip().upper() if m else ''
        toks = tokens(name)
        sc = set_code(name, h.upper())
        if sc:
            p, pf = sc, '상품명'
        elif mpn and not re.fullmatch(r'\d+', mpn):
            # LG: 'GBBS322APY.APYQEUZ' -> 상품명과 같은 앞부분 사용
            base = mpn.split('.')[0] if (b == 'LG' and '.' in mpn) else mpn
            p, pf = base, '페이지'
        else:
            # mpn 이 없거나 숫자뿐(매장/제조사 내부 번호) -> 상품명 토큰 중 페이지에 있는 것
            c = [t for t in toks if t in h.upper()]
            if c: p, pf = max(c, key=len), '상품명'
    if not b:
        b = brand_from_name(name, brands)
        bf = '상품명' if b else '없음'
    if not p:
        if not h:
            t = set_code(name, strict=True) or clean_tokens(name)
            if t: p, pf = t, '상품명'
    out.append([r['행번호'], r['확인 요청 URL'], b, p, bf or '없음', pf or '없음'])
write(f'{BASE}/parts/Czech_Republic_ALZA.csv', out)
report(rows, out)
