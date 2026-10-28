# 사용: python3 -I seller_g3.py   (외부 호출 없음, 로컬 HTML만 읽음)
import json, gzip, re, csv, html as H, os
Z = '/private/tmp/claude-501/-Users-codestepseunghee-codestep-lg-online-retailer-analysis/253f8734-8060-4ddc-8899-4a7f6bf91733/scratchpad/zyte_full'
TARGET = {'ALZA', 'DATART', 'MEDIAEXPERT', 'RTV_EURO_AGD', 'ELGIGANTEN', 'CURRYS', 'AO'}
NAME = {'ALZA': 'Alza.cz', 'DATART': 'DATART', 'RTV_EURO_AGD': 'RTV EURO AGD', 'ELGIGANTEN': 'Elgiganten',
        'CURRYS': 'Currys', 'AO': 'AO.com', 'MEDIAEXPERT': 'Media Expert'}

def read_html(d):
    p = f"{Z}/{d.get('_dir') or 'html'}/{d['HTML파일']}"
    return gzip.open(p, 'rt', encoding='utf-8', errors='replace').read()

def ldblocks(h):
    out = []
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
        s = m.group(1).strip()
        for t in (s, re.sub(r'[\x00-\x1f]+', ' ', s)):
            try:
                out.append(json.loads(t)); break
            except Exception:
                pass
    return out

def is_type(o, t):
    x = o.get('@type')
    return x == t or (isinstance(x, list) and t in x)

def main_product(h):
    """페이지 맨 위 단계의 Product (다른 상품 안에 끼어 있는 isRelatedTo 등은 제외)"""
    for b in ldblocks(h):
        for o in (b if isinstance(b, list) else [b]):
            if isinstance(o, dict):
                if is_type(o, 'Product'):
                    return o
                g = o.get('@graph')
                if isinstance(g, list):
                    for x in g:
                        if isinstance(x, dict) and is_type(x, 'Product'):
                            return x
    return None

def first_offer(p):
    o = p.get('offers')
    if isinstance(o, dict):
        if isinstance(o.get('offers'), list) and o['offers']:
            return o['offers'][0]
        return o
    if isinstance(o, list) and o and isinstance(o[0], dict):
        return o[0]
    return {}

def cond_of(p):
    return str(first_offer(p).get('itemCondition', '')).split('/')[-1]

def seller_of(p):
    s = first_offer(p).get('seller')
    return (s.get('name') if isinstance(s, dict) else s) or ''

DIRECT, EXT, REF, UNK = '직판', '외부판매자', '리퍼·중고', '확인불가'

def judge(r, d, h):
    u = d['요청URL']
    p = main_product(h)
    if r == 'ALZA':
        if not p: return None, UNK, 'ld+json Product 없음'
        c = cond_of(p)
        if c in ('UsedCondition', 'RefurbishedCondition', 'DamagedCondition'):
            return NAME[r], REF, f'ld+json offers.itemCondition={c} (판매자 필드 없음, 운영사 Alza로 추정)'
        return NAME[r], DIRECT, f'추정: 판매자 표시 없음. ld+json itemCondition={c}, 마켓플레이스 문구 없음'
    if r == 'DATART':
        bazar = '/bazar/' in u
        if p:
            s = seller_of(p); c = cond_of(p)
            if bazar or c in ('UsedCondition', 'DamagedCondition', 'RefurbishedCondition'):
                return s or NAME[r], REF, f'ld+json offers.seller.name={s}; itemCondition={c}; URL /bazar/'
            return s or NAME[r], DIRECT, f'ld+json offers.seller.name={s}; itemCondition={c}'
        if bazar and 'product-detail-title' in h:
            return NAME[r], REF, 'URL /bazar/ + product-detail-title (ld+json 없음, 판매자는 운영사 DATART로 추정)'
        return None, UNK, 'ld+json Product 없음, 본문이 빈 껍데기 페이지'
    if r == 'MEDIAEXPERT':
        i = h.find('<h1')
        m = re.search(r'seller-label[^>]*>\s*Sprzedawca:\s*</span>\s*<span class="seller-name[^"]*"[^>]*>(.*?)</span>', h[i:] if i >= 0 else h, re.S)
        if not m: return None, UNK, 'Sprzedawca 표시 없음'
        s = H.unescape(m.group(1)).strip()
        outlet = '/outlet/' in u
        if outlet:
            st = re.search(r'Stan produktu:\s*([^<]{0,40})', h)
            return s, REF, f'Sprzedawca: {s}; URL /outlet/; Stan produktu 표시' + (f' ({H.unescape(st.group(1)).strip()})' if st and st.group(1).strip() else '')
        if s.lower().replace(' ', '') == 'mediaexpert':
            return s, DIRECT, f'Sprzedawca: {s}'
        return s, EXT, f'Sprzedawca: {s} (Media Expert 아님)'
    if r == 'RTV_EURO_AGD':
        if not p: return None, UNK, 'ld+json Product 없음'
        c = cond_of(p)
        if c != 'NewCondition':
            return NAME[r], REF, f'ld+json itemCondition={c}'
        return NAME[r], DIRECT, f'추정: ld+json offers.seller.name이 빈 문자열, itemCondition={c}, 외부 판매자 표시 없음'
    if r == 'ELGIGANTEN':
        if not p: return None, UNK, 'ld+json Product 없음'
        flags = {}
        for k in ('isMarketplaceProduct', 'isMarketPlaceProduct', 'isOutletProduct', 'isOutlet', 'isDropship'):
            flags[k] = re.findall(r'\\"' + k + r'\\":(true|false)', h)
        txt = ','.join(f"{k}={'/'.join(sorted(set(v)))}" for k, v in flags.items() if v)
        if 'true' in flags['isMarketplaceProduct'] + flags['isMarketPlaceProduct']:
            return None, EXT, txt
        if 'true' in flags['isOutletProduct'] + flags['isOutlet']:
            return NAME[r], REF, txt
        if not txt: txt = '플래그 없음'
        return NAME[r], DIRECT, '페이지 내 플래그: ' + txt + ' (판매자 이름 필드는 없음, 운영사로 추정)'
    if r == 'CURRYS':
        if not p: return None, UNK, 'ld+json Product 없음: 상품이 아닌 목록(카테고리) 페이지가 저장됨'
        return NAME[r], DIRECT, f'추정: 판매자 표시 없음. ld+json itemCondition={cond_of(p)}, 마켓플레이스 문구 없음'
    if r == 'AO':
        if not p: return None, UNK, 'ld+json Product 없음'
        s = seller_of(p)
        c = cond_of(p)
        if c != 'NewCondition': return s or NAME[r], REF, f'itemCondition={c}'
        if s.lower() in ('ao.com', 'ao'):
            return s, DIRECT, f'ld+json offers.seller.name={s}; itemCondition={c}'
        return s or None, (EXT if s else UNK), f'ld+json offers.seller.name={s}'
    return None, UNK, ''

def main():
    out = []
    for l in open(Z + '/pages_best.jsonl'):
        d = json.loads(l)
        if d['페이지상태'] != '정상' or d['리테일러'] not in TARGET: continue
        h = read_html(d)
        s, k, e = judge(d['리테일러'], d, h)
        out.append([d['요청URL'], d['국가'], d['리테일러'], s or '', k, e])
    with open(Z + '/seller/seller_g3.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(['요청URL', '국가', '리테일러', '판매자', '판매자구분', '근거']); w.writerows(out)
    print(len(out), 'rows')

if __name__ == '__main__':
    main()
