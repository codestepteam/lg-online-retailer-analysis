#!/usr/bin/env python3
"""Electroplanet (Morocco): 브랜드=페이지 a.manufacturer(/marques/..) 링크 글자, 없으면 상품명에서 사전 매칭.
제품코드=페이지에 별도 모델 칸이 없어(Reference fournisseur = 상품명 그대로) 상품명 토큰, 페이지가 있으면 본문 확인."""
import csv, gzip, re, sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_tokens import valid, models_from_word
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'Morocco_Electroplanet'
GENERIC = ['MOULINEX','TEFAL','KRUPS','ROWENTA','TAURUS','SAMSUNG','LG','SAMSUNG','BOSCH','SIEMENS','BEKO','HAIER','HISENSE','WHIRLPOOL','ARTHUR MARTIN','SIERA','TOSHIBA','SHARP','ZANUSSI','ELECTROLUX','MIELE','CANDY','HOOVER','INDESIT','ARISTON','ARCELIK','GRUNDIG','SMEG','TCL','MIDEA','HITACHI','PANASONIC','SONY','NASCO','VESTEL','CONDOR','BRANDT','DE DIETRICH','FAGOR','LIEBHERR','GORENJE','AMICA','TEKA','FRANKE','WESTPOINT','WHITE POINT','BEKO','AEG','HOTPOINT','OK','KENWOOD','TORNADO','DAEWOO']
def load(p): return gzip.open(p, 'rt', encoding='utf-8', errors='replace').read()
def page_brand(h):
    m = re.search(r'<a class="manufacturer" href="[^"]*/marques/[^"]*">\s*([^<]*?)\s*</a>', h)
    return html.unescape(m.group(1)).strip().upper() if m else ''
def title_brand(title, brands):
    t = ' ' + re.sub(r'[^A-Z0-9À-Ý&]+', ' ', title.upper()) + ' '
    best = ('', -1)
    for b in brands:
        i = t.rfind(' ' + b + ' ')
        if i >= 0 and (i + len(b), len(b)) > (best[1], len(best[0])) : best = (b, i + len(b))
    return best[0]
def main():
    rows = list(csv.DictReader(open(f'{BASE}/inputs/{NAME}.csv', encoding='utf-8-sig')))
    pages = {r['행번호']: load(r['HTML경로']) for r in rows if r['HTML경로']}
    brands = set(GENERIC)
    for h in pages.values():
        b = page_brand(h)
        if b: brands.add(b)
        for x in re.findall(r'<span class="brand">([^<]+)</span>', h): brands.add(html.unescape(x).strip().upper())
    for bad in ('', 'SILVER', 'SBS', 'LAV', 'INO', 'INOX'): brands.discard(bad)  # 색·약어가 브랜드 칸에 섞인 것 제외
    # 사전에 없는 브랜드: 상품명 맨 끝 글자 단어가 3번 이상 반복되면(색·형용어 제외) 브랜드로 본다
    known = set(brands)
    STOP = set('INOX SILVER BLANC NOIR BLACK WHITE GRIS GREY WIFI NF NOFROST FROST BLC SLV BLK BLEU ROUGE DARK GRAPHITE BEIGE TITANE ANTHRACITE CLASSE MODERNE DIGITAL INVERTER AUTOMATIQUE'.split())
    lastc = {}
    for r in rows:
        ws = re.sub(r'[^A-Z0-9À-Ý& ]+', ' ', r['상품명'].upper()).split()
        if ws and re.fullmatch(r'[A-Z]{3,}', ws[-1]) and ws[-1] not in STOP: lastc[ws[-1]] = lastc.get(ws[-1], 0) + 1
    STOP |= {'SILVER','SBS','INO','LAV','ARDOISE','MAL','REF','COMB','PLAQUE'}
    brands |= {w for w, n in lastc.items() if n >= 3 and w not in STOP}
    ALIAS = {'WH': 'WHIRLPOOL', 'WHP': 'WHIRLPOOL', 'A M': 'ARTHUR MARTIN', 'AM': 'ARTHUR MARTIN', 'FRK': 'FRANKE'}  # 상품명 끝의 약어/잘린 표기
    out = []
    for r in rows:
        h = pages.get(r['행번호']); title = r['상품명']
        brand = bsrc = code = csrc = ''
        if h:
            b = page_brand(h)
            if b: brand, bsrc = b, '페이지'
        if not brand:
            b = title_brand(title, brands)
            ws = re.sub(r'[^A-Z0-9À-Ý& ]+', ' ', title.upper()).split()
            if not b and len(ws) >= 2 and ' '.join(ws[-2:]) == 'A M': b = 'ARTHUR MARTIN'   # 'A,M' = Arthur Martin 약어
            if not b and ws:
                lw = ws[-1]
                if lw in ALIAS: b = lw
                elif len(lw) >= 3 and lw.isalpha():  # 상품명 끝 단어가 잘린 경우
                    c = [x for x in known if x.startswith(lw) and x != lw]
                    if len(c) == 1: b = c[0]
            if b in ALIAS: b = ALIAS[b]
            elif b and b not in known:  # 끝이 잘린 표기(MOULINE, BEK 등)는 알려진 브랜드 중 하나로 이어지면 보정
                c = [x for x in known if x.startswith(b) and x != b]
                if len(c) == 1: b = c[0]
            if b: brand, bsrc = b, '상품명'
        # 제품코드: 상품명 토큰(공백 단위). 브랜드·일반어 뒤쪽부터 첫 유효 토큰, 'A/B' 는 'A + B'
        # 첫 번째로 모델처럼 생긴 단어 하나(또는 'A/B'로 이어진 세트). 'X + Y' 로 이어진 두 번째 상품도 허용
        found = []
        ws = title.upper().split()
        for k, w in enumerate(ws):
            m = models_from_word(w)
            if m:
                found = list(dict.fromkeys(m))
                if k + 2 < len(ws) and ws[k + 1] == '+':
                    found += [x for x in models_from_word(ws[k + 2]) if x not in found]
                break
        if h: found = [m for m in found if m.split('/')[0] in h.upper()]
        # 용량 꼬리가 붙은 조각(예: 420L/GR-B392PLGB 에서 420L)은 models_from_word가 이미 제거함
        if found:
            code, csrc = ' + '.join(found), '상품명'
        out.append([r['행번호'], r['확인 요청 URL'], brand, code, bsrc or '없음', csrc or '없음'])
    os.makedirs(f'{BASE}/parts', exist_ok=True)
    with open(f'{BASE}/parts/{NAME}.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(['행번호','확인 요청 URL','브랜드명','제품코드','브랜드 찾은곳','제품코드 찾은곳']); w.writerows(out)
    print(NAME, len(rows), len(out))
if __name__ == '__main__': main()
