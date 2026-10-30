import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cz_common import *
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = rd(f'{BASE}/inputs/Czech_Republic_DATART.csv')

def page_brand(h):
    m = re.search(r'"@type":\s*"Brand",\s*"name":\s*"([^"]+)"', h) or re.search(r'item_brand&quot;:\s*&quot;([^&]+)&quot;', h) \
        or re.search(r'"brand":\s*"([^"]+)"', h)
    return H.unescape(m.group(1)).strip().upper() if m else ''

pages, brands = {}, set()
for r in rows:
    if r['HTML경로']:
        h = load(r['HTML경로']); pages[r['행번호']] = h
        if h:
            b = page_brand(h)
            if b: brands.add(b)
out = []
for r in rows:
    name = r['상품명']; h = pages.get(r['행번호'])
    b = bf = p = pf = ''
    if h:
        b = page_brand(h)
        if b: bf = '페이지'
        hu = h.upper()
        ms = re.search(r'"sku":\s*"([^"]+)"', h)
        sku = ms.group(1).upper() if ms else ''
        # 세트(예: 'A + B') -> 각 모델
        sc = set_code(name, hu)
        toks = list(dict.fromkeys(tokens(name)))
        if sc:
            p, pf = sc, '상품명'
        else:
            c = [t for t in toks if t in hu]
            # 매장 sku(접두어+모델) 끝부분과 일치하는 후보가 있으면 가장 확실
            s = [t for t in c if sku.endswith(t.replace(' ', ''))]
            if s: p, pf = max(s, key=len), '상품명'
            elif len(c) == 1: p, pf = c[0], '상품명'
            elif c:
                t = clean_tokens(name)
                if t and t in hu: p, pf = t, '상품명'
        if not p:  # 짧은 모델(4자)은 매장 sku 끝부분과 일치할 때만 인정
            w = [x.upper() for x in re.findall(r'[A-Za-z0-9]{4,}', name) if re.search(r'\d', x) and re.search(r'[A-Za-z]', x) and sku.endswith(x.upper())]
            if w: p, pf = max(w, key=len), '상품명'
    if not b:
        b = brand_from_name(name, brands); bf = '상품명' if b else '없음'
    if not p and not h:
        t = set_code(name, strict=True) or clean_tokens(name)
        if t: p, pf = t, '상품명'
    out.append([r['행번호'], r['확인 요청 URL'], b, p, bf or '없음', pf or '없음'])
write(f'{BASE}/parts/Czech_Republic_DATART.csv', out)
report(rows, out)
