# -*- coding: utf-8 -*-
"""그룹1 리테일러 7곳의 '메인 상품 판매자'를 HTML에서 읽어 seller_g1.csv 로 저장.
실행: python3 -I seller_g1.py   (로컬 HTML만 읽음, 외부 접속 없음)
"""
import csv, gzip, html as H, json, re, os, collections

Z = '/private/tmp/claude-501/-Users-codestepseunghee-codestep-lg-online-retailer-analysis/253f8734-8060-4ddc-8899-4a7f6bf91733/scratchpad/zyte_full'
OUT = Z + '/seller/seller_g1.csv'
TARGET = {('France', 'BOULANGER'), ('France', 'DARTY'), ('Spain', 'ELCORTEINGLES_ELECTRONICA'),
          ('Spain', 'MEDIAMARKT'), ('Portugal', 'Worten'), ('Netherlands', 'COOLBLUE'),
          ('Netherlands', 'MEDIAMARKT')}


def load(d):
    p = f"{Z}/{d.get('_dir') or 'html'}/{d['HTML파일']}"
    return gzip.open(p, 'rt', encoding='utf-8', errors='replace').read()


def clean(s):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


# 결과 = (판매자, 구분, 근거)
def boulanger(d, h):
    m = re.search(r'id="product-merchant__condition">(.*?)</p>', h, re.S)
    if not m:
        return ('', '확인불가', '판매자 문구 블록(product-merchant__condition) 없음 - 상품 페이지가 아닌 목록 페이지로 보임')
    blk = m.group(1)
    t = re.search(r'title="([^"]*)"', blk)
    name = H.unescape(t.group(1)).strip() if t else clean(blk)
    cond = clean(re.split(r'(?i)vendu', clean(blk))[0])
    ev = f'{cond} / vendu & expédié par {name}'
    low = name.lower()
    if low == 'boulanger':
        kind = '직판'
    elif low == 'haier - candy - hoover':
        kind = '브랜드공식점'
        ev += ' (Haier 그룹 브랜드 입점 - 브랜드 공식 판매로 판단, 추정)'
    elif re.search(r'(?i)reconditionn|occasion', cond):
        kind = '리퍼·중고'
    else:
        kind = '외부판매자'
    if kind != '리퍼·중고' and re.search(r'(?i)reconditionn', cond):
        kind = '리퍼·중고'
    return (name, kind, ev)


def darty(d, h):
    mk = re.search(r'product-mkp-seller-info.*?class="mkp-seller-name[^"]*">([^<]*)<', h, re.S)
    sch = re.findall(r'itemprop="seller"\s+content="([^"]*)"', h)
    cond = re.search(r'itemprop="itemCondition"\s+content="https://schema.org/(\w+)"', h)
    cond = cond.group(1) if cond else ''
    avail = re.search(r'itemprop="availability"\s+href="https://schema.org/(\w+)"', h)
    avail = avail.group(1) if avail else ''
    if mk:
        name = H.unescape(mk.group(1)).strip()
        ev = f'화면 판매자 블록 "Vendu et expédié par {name}" / 상태 {cond}'
        if sch and H.unescape(sch[0]) != name:
            ev += f' (메타 seller={sch[0]}와 다름 - 화면 블록 우선)'
    elif sch:
        name = H.unescape(sch[0]).strip()
        ev = f'메타 itemprop=seller "{name}" / 상태 {cond} / {avail}'
    else:
        return ('', '확인불가', '판매자 블록과 메타 seller 모두 없음 (오퍼 정보 없는 페이지)')
    low = name.lower()
    if re.search(r'seconde vie|occasion', low) or cond == 'UsedCondition':
        kind = '리퍼·중고'
    elif low == 'darty':
        kind = '직판'
    else:
        kind = '외부판매자'
    return (name, kind, ev)


def eci(d, h):
    ss = re.findall(r'"_single_sku":\{([^{}]*)\}', h)
    if not ss:
        return ('', '확인불가', '_single_sku 없음')
    s = ss[0]
    prov = re.search(r'"provider":"([^"]*)"', s)
    pn = re.search(r'"provider_name":"([^"]*)"', s)
    mp = re.search(r'"marketplace":(\w+)', s)
    prov = prov.group(1) if prov else ''
    pn = pn.group(1) if pn else ''
    mp = mp.group(1) if mp else ''
    ev = f'_single_sku provider={prov}, provider_name={pn}, marketplace={mp}'
    if prov == 'eci' and mp == 'false':
        return ('El Corte Inglés', '직판', ev)
    return (pn, '외부판매자', ev)


def mediamarkt(d, h):
    cty = 'es' if d['국가'] == 'Spain' else 'nl'
    m = re.search(r'-(\d+)\.html', d['요청URL'])
    if not m:
        return ('', '확인불가', '상품 페이지 주소가 아님(메인 상품 id 없음)')
    pid = m.group(1)
    # 메인 상품 id 에 붙은 가격 정보(추천상품은 다른 id)
    ms = re.findall(r'"id":"Media:%s:%s(?:\[\d+\])?","currency":"[A-Z]+","isProductOfTypeMarketplace":(\w+)[^{}]*?"marketplaceSeller":(null|\{[^{}]*\})' % (cty, pid), h)
    flag = 'true' if any(a == 'true' for a, b in ms) else ('false' if ms else 'none')
    sn = ''
    for a, b in ms:
        if b != 'null':
            x = re.search(r'"sellerName":"((?:[^"\\]|\\.)*)"', b)
            if x:
                sn = json.loads('"%s"' % x.group(1)) if '\\' in x.group(1) else x.group(1)
                break
    st = re.search(r'"id":"Media:%s:%s","isAvailableForDelivery":\w+,"isAvailableForPickup":\w+,"isAvailableAndBuyable":\w+,"isInAssortment":\w+,"onlineStatus":"(\w+)"' % (cty, pid), h)
    st = st.group(1) if st else '없음'
    link = re.search(r'data-test="additional-info-normal"[^>]*>(?:Vendido y enviado por|Verkoop en verzending door|Verzonden en verkocht door) <a[^>]*mms-third-party-provider-link[^>]*><span[^>]*>([^<]*)<', h)
    link = H.unescape(link.group(1)).strip() if link else ''
    cond = re.search(r'"id":"Media:%s:%s\[\d+\]","categoryIds":\[[^\]]*\],"locale":"[^"]*","offer":\{[^{}]*"conditionType":"(\w+)"' % (cty, pid), h)
    cond = cond.group(1) if cond else ''
    if flag == 'true':
        name = sn or link
        ev = f'메인id {pid}: isProductOfTypeMarketplace=true, marketplaceSeller.sellerName={name}, conditionType={cond or "-"}, onlineStatus={st}'
        kind = '리퍼·중고' if cond and cond != 'NEW' else '외부판매자'
        return (name, kind, ev)
    if link:
        ev = (f'메인id {pid}: 구조값 isProductOfTypeMarketplace={flag}(onlineStatus={st})이나 화면 구매박스에 '
              f'마켓플레이스 판매자 "{link}" 표시 (애매 - 화면 기준 외부판매자)')
        return (link, '외부판매자', ev)
    if flag == 'false':
        ev = f'메인id {pid}: isProductOfTypeMarketplace=false, marketplaceSeller=null, onlineStatus={st}'
        return ('MediaMarkt', '직판', ev)
    return ('', '확인불가', f'메인id {pid}의 가격/판매자 정보가 HTML에 없음(onlineStatus={st})')


def worten(d, h):
    m = re.search(r'<div class="neu-02-bg seller-info".*?(?=<!--\]-->)', h, re.S)
    if not m:
        return ('', '확인불가', 'seller-info 블록 없음')
    blk = m.group(0)
    sc = ''
    cm = re.search(r'id="sellerConditions"[^>]*>(.*?)</div>', h, re.S)
    if cm:
        sc = clean(cm.group(1))
    used = bool(re.search(r'(?i)unidade de exposi|recondicionad[oa]\b|COM DEFEITO', sc))
    if 'seller-info__seller-link' in blk:
        name = clean(re.search(r'<b class="h-underline"[^>]*>(.*?)</b>', blk, re.S).group(1))
        ev = f'seller-info "Vendido por {name}" (marketplace 클래스)'
        kind = '외부판매자'
        if name == 'Worten Peças':
            ev += ' - 이름상 Worten 부품 채널로 보이나(추정) 화면 구조는 마켓플레이스 판매자'
    else:
        name = 'Worten'
        ev = 'seller-info "Vendido por" + Worten 로고'
        kind = '직판'
    if used:
        kind = '리퍼·중고'
        ev += f' / 판매조건 문구: {sc[:80]}'
    return (name, kind, ev)


def coolblue(d, h):
    cond = re.search(r'schema.org/(\w+Condition)', h)
    cond = cond.group(1) if cond else '-'
    av = re.search(r'schema.org/(InStock|SoldOut|OutOfStock|PreOrder)', h)
    return ('Coolblue', '직판',
            f'(추정) HTML 어디에도 판매자(seller) 표시가 없음 - 직판으로 간주. 오퍼 상태 {cond}, 재고 {av.group(1) if av else "-"}')


FUNCS = {'BOULANGER': boulanger, 'DARTY': darty, 'ELCORTEINGLES_ELECTRONICA': eci,
         'MEDIAMARKT': mediamarkt, 'Worten': worten, 'COOLBLUE': coolblue}


def main():
    rows = []
    for l in open(Z + '/pages_best.jsonl', encoding='utf-8'):
        d = json.loads(l)
        if d.get('페이지상태') != '정상' or (d['국가'], d['리테일러']) not in TARGET:
            continue
        h = load(d)
        name, kind, ev = FUNCS[d['리테일러']](d, h)
        rows.append([d['요청URL'], d['국가'], d['리테일러'], name, kind, ev])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['요청URL', '국가', '리테일러', '판매자', '판매자구분', '근거'])
        w.writerows(rows)
    c = collections.Counter((r[1], r[2], r[4]) for r in rows)
    for k, v in sorted(c.items()):
        print(v, k)


if __name__ == '__main__':
    main()
