#!/usr/bin/env python3
"""MediaMarkt (NL, HU): 입력 -> parts. 브랜드=JSON-LD brand, 제품코드=사양 'MPN' 칸(상품명과 맞을 때), 아니면 상품명 토큰."""
import csv, gzip, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_tokens import valid, norm, title_models
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ['Netherlands_MEDIAMARKT', 'Hungary_Mediamarkt']
MPN_NAMES = ['Manufacturer Part Number (MPN)', 'Model-ID', 'Gyártói cikkszám (MPN)', 'Modell azonosító']
GENERIC = ['LG','SAMSUNG','BOSCH','SIEMENS','MIELE','AEG','ELECTROLUX','WHIRLPOOL','BEKO','HISENSE','HAIER','CANDY','HOOVER','GORENJE','SMEG','PANASONIC','SHARP','TOSHIBA','SONY','PHILIPS','INDESIT','ZANUSSI','LIEBHERR','BAUKNECHT','NEFF','GRUNDIG','ARÇELIK','ARCELIK','AMICA','INDESIT','HOTPOINT','DE DIETRICH','TEKA','FRANKE','OK.','OK','KOENIC','HYUNDAI','MIDEA','TCL','XIAOMI','DYSON','SEVERIN','EXQUISIT','PKM','NABO','INVENTUM','ETNA','PELGRIM','ATAG','VIVAX','SIMFER','KONCEPT','ZOWIE']

def load(p):
    return gzip.open(p, 'rt', encoding='utf-8', errors='replace').read()
def page_brand(h):
    m = re.search(r'"brand":\{"@type":"Brand","name":"([^"]*)"', h)
    return m.group(1).strip().upper() if m else ''
def page_cands(h):
    out = []
    for n in MPN_NAMES:
        for v in re.findall(r'"name":"' + re.escape(n) + r'","type":null,"unit":null,"value":"([^"]*)"', h):
            v = v.replace('\\u002F', '/').replace('\\\\u002F', '/').strip()
            if v and v not in out: out.append(v)
    return out
def brand_from_title(title, brands):
    t = title.upper()
    for b in sorted(brands, key=len, reverse=True):
        if re.match(re.escape(b) + r'(?![A-Z0-9])', t):
            return b
    return ''
def run(name):
    rows = list(csv.DictReader(open(f'{BASE}/inputs/{name}.csv', encoding='utf-8-sig')))
    pages = {}
    brands = set(GENERIC)
    for r in rows:
        if r['HTML경로']:
            h = load(r['HTML경로']); pages[r['행번호']] = h
            b = page_brand(h)
            if b: brands.add(b)
    out = []
    for r in rows:
        h = pages.get(r['행번호']); title = r['상품명']
        brand = bsrc = code = csrc = ''
        tm = []
        if h is not None:
            b = page_brand(h)
            if b: brand, bsrc = b, '페이지'
        if not brand:
            b = brand_from_title(title, brands)
            if b: brand, bsrc = b, '상품명'
            else:  # 사전에 없는 브랜드: MediaMarkt 제목은 브랜드로 시작 -> 첫 단어가 3자 이상 대문자 글자뿐이면 브랜드로 본다
                w = title.split()[0] if title.split() else ''
                if re.fullmatch(r'[A-ZÀ-Ý&]{3,}', w): brand, bsrc = w, '상품명'
        brand = brand.rstrip('.') if brand else brand
        skip = len(brand.split()) if brand and brand_from_title(title, [brand, brand + '.']) else 0
        tm = title_models(title, skip)
        tm_ok = [m for m in tm if h is None or m in h.upper()]
        if h is not None:
            nt = norm(title + ' ' + r['확인 요청 URL'].replace('-', ''))
            tn = [norm(m) for m in tm_ok]
            hit = ''
            for c in page_cands(h):
                nc = norm(c)
                if nc and (nc in nt or any(nc.startswith(t) and len(nc) - len(t) <= 4 for t in tn)):
                    hit = c.upper(); break
            if hit: code, csrc = hit, '페이지'
        if not code and tm_ok:
            code, csrc = ' + '.join(tm_ok), '상품명'
        out.append([r['행번호'], r['확인 요청 URL'], brand, code, bsrc or '없음', csrc or '없음'])
    os.makedirs(f'{BASE}/parts', exist_ok=True)
    with open(f'{BASE}/parts/{name}.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(['행번호','확인 요청 URL','브랜드명','제품코드','브랜드 찾은곳','제품코드 찾은곳']); w.writerows(out)
    print(name, len(rows), len(out))
if __name__ == '__main__':
    for n in FILES: run(n)
