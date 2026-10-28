# -*- coding: utf-8 -*-
"""그룹2 리테일러(DE MediaMarkt/OTTO/Amazon, IT Amazon/MediaWorld/Unieuro, HU MediaMarkt) 판매자 추출.
실행: python3 -I seller_g2.py   (로컬 HTML만 읽음, 외부 호출 없음)
출력: 같은 폴더의 seller_g2.csv (utf-8-sig)
"""
import json, gzip, re, csv, os, base64, html as H, collections

Z = '/private/tmp/claude-501/-Users-codestepseunghee-codestep-lg-online-retailer-analysis/253f8734-8060-4ddc-8899-4a7f6bf91733/scratchpad/zyte_full'
OUT = os.path.join(Z, 'seller', 'seller_g2.csv')
TARGET = {('Germany', 'MEDIAMARKT'), ('Germany', 'OTTO'), ('Germany', 'AMAZON'), ('Italy', 'AMAZON'),
          ('Italy', 'MEDIAWORLD'), ('Italy', 'UNIEURO'), ('Hungary', 'Mediamarkt')}

# 직판 / 외부판매자 / 브랜드공식점 / 리퍼·중고 / 확인불가
D, X, B, R, U = '직판', '외부판매자', '브랜드공식점', '리퍼·중고', '확인불가'
BRAND_RE = re.compile(r'^(samsung (deutschland|italia|electronics.*)|lg electronics.*|bosch.*home.*|miele.*|hisense.*|haier.*|candy.*)$', re.I)


def load(d):
    p = f"{Z}/{d.get('_dir') or 'html'}/{d['HTML파일']}"
    return gzip.open(p, 'rt', encoding='utf-8', errors='replace').read()


def clean(s):
    s = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '|', s)
    s = H.unescape(s.replace('&nbsp;', ' '))
    return re.sub(r'\s+', ' ', re.sub(r'(\|\s*)+', '|', s))


# ---------------------------------------------------------------- MediaMarktSaturn (MediaMarkt DE/HU, MediaWorld IT)
def mms(d, h):
    m = re.search(r'-(\d+)(?:\.html)?(?:\?.*)?$', d['요청URL'])
    if not m:
        return '', U, 'URL에 상품 id 없음(상품 페이지 아님)'
    pid = m.group(1)
    hh = h if '"isProductOfTypeMarketplace"' in h else h.replace('\\"', '"')
    # 1) 화면에 실제로 보여 주는 상품 id: URL의 id가 들어 있는 GraphqlProductMatch의 preferredProductId
    main = pid
    match_txt = ''
    for mm in re.finditer(r'"productId":"(\d+)","retailProductId":"?(\d*)"?,"marketplaceProductId":"?(\d*)"?,"preferredProductId":"?(\d+)"?', hh):
        if pid in mm.group(1, 2, 3):
            main = mm.group(4)
            match_txt = hh[mm.start():mm.start() + 3000]
            break
    pf = None
    for cand in (main, pid):
        pf = re.search(r'"id":"[A-Za-z]+:[a-z]{2}:%s","currency":[^,]*,"isProductOfTypeMarketplace":(true|false)' % cand, hh)
        if pf:
            main = cand
            break
    if not pf:
        return '', U, f'가격 정보 블록 없음(id {pid})'
    is_mp = pf.group(1) == 'true'
    seg = hh[pf.end():pf.end() + 700]
    brand = {'Germany': 'MediaMarkt', 'Hungary': 'MediaMarkt', 'Italy': 'MediaWorld'}[d['국가']]
    if not is_mp:
        return brand, D, f'isProductOfTypeMarketplace=false(id {main})'
    ms = re.search(r'"marketplaceSeller":(\{[^}]*\}|null)', seg)
    nm = re.search(r'"sellerName":"([^"]*)"', ms.group(1)) if ms else None
    if not nm:
        return '', U, f'마켓플레이스 상품이나 유효 판매 제안 없음(marketplaceSeller=null, id {main})'
    name = H.unescape(nm.group(1))
    cond = re.search(r'"bestMarketplaceOffers":\[\{[^\]]*?"offerCondition":"(\w+)"', match_txt)
    cond = cond.group(1) if cond else None
    ev = f'isProductOfTypeMarketplace=true; marketplaceSeller.sellerName={name}'
    if cond and cond != 'NEW':
        return name, R, ev + f'; offerCondition={cond}'
    if name == 'MediaMarktSaturn geprüft':
        return name, R, ev + '; (그룹 자체 리퍼 판매자, 조건값 미확인)'
    if BRAND_RE.match(name):
        return name, B, ev
    return name, X, ev


# ---------------------------------------------------------------- Amazon DE/IT
def block(h, name):
    i = h.find('id="%s"' % name)
    if i < 0:
        return None
    m = re.search(r'<div id="\w+_feature_div"', h[i + 30:])
    return h[i:i + 30 + m.start()] if m else h[i:i + 3000]


def toks(b):
    if not b:
        return None
    t = [x for x in clean(b).split('|') if x.strip()]
    return t[1:] if t and t[0].startswith('id=') else t


COND_RE = re.compile(r'^(Gebraucht|Kaufen Gebraucht|Generalüberholt|Renewed|Usato|Acquista Usato|Ricondizionat|Refurbished)', re.I)


def amazon(d, h, idname):
    ai = h.find('id="buybox"')
    bb = clean(h[ai:ai + 9000]) if ai >= 0 else ''
    hm = re.match(r'[^>]*>\s*\|?\s*(.*)', bb)
    head = hm.group(1)[:80] if hm else ''
    mids = re.findall(r'id="merchantID" name="merchantID" value="([A-Z0-9]+)"', h)
    first_mid = mids[0] if mids else None
    cm = COND_RE.match(head)
    wb = block(h, 'merchantInfoFeature_feature_div')
    ft = toks(block(h, 'fulfillerInfoFeature_feature_div'))
    mt = toks(wb)
    if cm:
        s = re.search(r'(?:Verkauft von|Venduto da)\s*\|\s*([^|]+)', bb)
        name = s.group(1).strip() if s else idname.get(first_mid, f'(판매자ID {first_mid})')
        return name, R, f'구매상자 제목 "{head[:30]}"' + (f'; 판매자 문구 "{name}"' if s else f'; merchantID={first_mid}')
    if mt and len(mt) > 1:
        label = mt[0]
        link = re.search(r"<a [^>]*seller=([A-Z0-9]+)[^>]*>([^<]*)</a>", wb)
        name = H.unescape(link.group(2)).strip() if link else mt[1]
        fba = ft and len(ft) > 1 and ft[1].startswith('Amazon')
        if not link and name == 'Amazon':
            return 'Amazon', D, f'"{label}: Amazon"'
        if BRAND_RE.match(name):
            return name, B, f'"{label}: {name}"' + ('; Amazon 배송(FBA)' if fba else '')
        return name, X, f'"{label}: {name}"' + ('; 배송은 Amazon(FBA): "%s: %s"' % (ft[0], ft[1]) if fba else '; 판매자가 직접 배송')
    if re.search(r'Derzeit nicht verfügbar|Non disponibile|Al momento non disponibile', bb[:400]):
        return '', U, '구매상자에 "현재 구매 불가" 문구(판매자 표시 없음)'
    return '', U, '구매상자에 판매자 표시 없음(제안 없음)'


# ---------------------------------------------------------------- OTTO
def otto(d, h):
    ms = re.search(r'<div class="retailer__info[^"]*"><span>Verkäufer:</span>(.*?)</oc-interactive-overlay-v2>', h, re.S)
    if not ms:
        return '', U, '"Verkäufer:" 블록 없음'
    b = ms.group(1)
    link = re.search(r'<oc-link-v2[^>]*>(.*?)</oc-link-v2>', b, re.S)
    if link:
        name = H.unescape(re.sub(r'<[^>]+>', '', link.group(1)).strip())
        return name, X, f'retailer__info "Verkäufer: {name}"'
    if 'logo="otto"' in b:
        return 'OTTO', D, 'retailer__info "Verkäufer:" + otto 로고(partner/1000000)'
    return '', U, '"Verkäufer:" 블록 형식 불명'


# ---------------------------------------------------------------- Unieuro
def unieuro(d, h):
    if re.search(r'-pid[A-Z0-9]+$', d['요청URL']) and 'venduti e spediti da Unieuro' in h:
        return 'Unieuro', D, '[추정] 판매자 표시 자체가 HTML에 없음; "venduti e spediti da Unieuro" 일반 안내문만 있고 마켓플레이스 표지 없음'
    return '', U, '상품 페이지 내용 없음(홈/빈 페이지)'


def main():
    rows = [json.loads(l) for l in open(Z + '/pages_best.jsonl', encoding='utf-8')]
    rows = [r for r in rows if r['페이지상태'] == '정상' and (r['국가'], r['리테일러']) in TARGET]
    # Amazon 판매자ID -> 이름 (판매자 링크가 있는 페이지에서 수집)
    idname = {'A3JWKAKR8XB7XF': 'Amazon', 'A11IL2PNWYJU7H': 'Amazon'}
    cache = {}
    for r in rows:
        if r['리테일러'] == 'AMAZON':
            h = load(r)
            cache[r['요청URL']] = h
            wb = block(h, 'merchantInfoFeature_feature_div')
            if wb:
                for sid, nm in re.findall(r"seller=([A-Z0-9]+)[^>]*>([^<]*)</a>", wb):
                    idname.setdefault(sid, H.unescape(nm).strip())
            # 중고 구매상자: "Verkauft von X"/"Venduto da X" 문구에서도 ID->이름 수집
            ai = h.find('id="buybox"')
            bb = clean(h[ai:ai + 9000]) if ai >= 0 else ''
            s2 = re.search(r'(?:Verkauft von|Venduto da)\s*\|\s*([^|]+)', bb)
            m2 = re.findall(r'id="merchantID" name="merchantID" value="([A-Z0-9]+)"', h)
            if s2 and m2:
                idname.setdefault(m2[0], s2.group(1).strip())
    out = []
    for r in rows:
        h = cache.pop(r['요청URL'], None) or load(r)
        k = (r['국가'], r['리테일러'])
        if k[1] == 'AMAZON':
            res = amazon(r, h, idname)
        elif k[1] == 'OTTO':
            res = otto(r, h)
        elif k[1] == 'UNIEURO':
            res = unieuro(r, h)
        else:
            res = mms(r, h)
        out.append([r['요청URL'], r['국가'], r['리테일러'], *res])
    with open(OUT, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['요청URL', '국가', '리테일러', '판매자', '판매자구분', '근거'])
        w.writerows(out)
    print(len(out), 'rows ->', OUT)


if __name__ == '__main__':
    main()
