# 판매자 판독 스크립트 (그룹4: 11개 리퍼러/국가). 로컬 HTML만 사용, 외부 호출 없음.
# 실행: python3 -I seller_g4.py
import json, gzip, re, csv, os, collections

Z = '/private/tmp/claude-501/-Users-codestepseunghee-codestep-lg-online-retailer-analysis/253f8734-8060-4ddc-8899-4a7f6bf91733/scratchpad/zyte_full'
OUT = Z + '/seller/seller_g4.csv'
TARGETS = [('Appliance Online', None), ('COSTCO', None), ('Cairo Sales', None), ('Electroplanet', None),
           ('EXTRA', None), ('Sharaf DG', None), ('LIVERPOOL', None), ('LAZADA', 'Singapore'),
           ('LAZADA', 'Thailand'), ('MOMOSHOP', None), ('DIENMAYXANH', None)]

DIRECT, EXT, BRAND, REFURB, UNK = '직판', '외부판매자', '브랜드공식점', '리퍼·중고', '확인불가'
BRAND_RE = re.compile(r'(?i)^(lg|samsung|sony|mabe|whirlpool|electrolux|bosch|panasonic|hisense|tcl|midea|haier|hitachi|sharp)\b.*(store|oficial|official|tienda)')
REFURB_TITLE = re.compile(r'(?i)refurb|reconditionn|renewed|open.?box|pre-?owned|\bused\b|福利品|整新|展示品|二手|trưng bày|مجدد|مستعمل|reacondicion|seminuev|usado|มือสอง')


def load(d):
    p = f"{Z}/{d.get('_dir') or 'html'}/{d['HTML파일']}"
    return gzip.open(p, 'rt', encoding='utf-8', errors='replace').read()


def unesc(h):
    return h.replace('\\"', '"')


def g(pat, s, flags=0, grp=1):
    m = re.search(pat, s, flags)
    return m.group(grp) if m else None


# ---------- 리테일러별 규칙: (판매자, 구분, 근거) 반환 ----------
def appliance_online(d, h):
    # 282건 모두 홈페이지 빈 껍데기(상품 정보 없음)
    if '<link id="canonicalLink" rel="canonical" href="https://www.appliancesonline.com.au/">' in h and 'Product' not in h:
        return '', UNK, 'HTML이 상품 정보 없는 홈페이지 빈 껍데기(자바스크립트로 나중에 그리는 화면)'
    return '', UNK, '판매자 표시 못 찾음'


def costco(d, h):
    u = unesc(h)
    tp = g(r'"isThirdPartyIncluded":(\w+)', u)
    car = g(r'"carrier":"([^"]+)"', u)
    sku = g(r'"sku":"(\d+)"', h)
    if tp == 'true':
        return '', UNK, 'isThirdPartyIncluded=true (의미 미확인, 외부 판매자 가능성 배제 못함)'
    return 'Costco', DIRECT, f'[추정] 판매자 칸 없음; Costco 품목번호 sku={sku}, 배송방식 {car}, isThirdPartyIncluded=false'


def cairo(d, h):
    if 'itemprop="offers"' in h and 'NewCondition' in h:
        return 'Cairo Sales', DIRECT, '[추정] 판매자 칸 없음; 단일 상점(ld+json LocalBusiness=Cairo Sales Stores), offers에 seller 없음, itemCondition=New'
    return '', UNK, '상품 offers 정보 없음'


def electroplanet(d, h):
    if '"@type":"Product"' in h and '"offers"' in h:
        return 'Electroplanet', DIRECT, '[추정] 판매자 칸 없음; Product ld+json offers에 seller 없음, 단일 상점'
    return '', UNK, 'Product ld+json 없음'


def extra(d, h):
    mp = g(r'"marketPlaceProduct":(\w+)', h)
    ld_price = g(r'"price"\s*:\s*"?([\d.]+)', h)
    if mp == 'true':
        shop = g(r'"marketPlaceOfferData":\{.{0,3000}?"shopName":"([^"]*)"', h, re.S)
        shop_ar = g(r'"marketPlaceShopDetails":\{"id":"\d+","name":"([^"]*)"', h)
        cond = g(r'"marketPlaceOfferData":\{.{0,3000}?"conditionCode":"(\w+)"', h, re.S)
        name = shop or shop_ar or ''
        if cond and cond != 'NEW':
            return name, REFURB, f'marketPlaceProduct=true, offer conditionCode={cond}'
        return name, EXT, f'pdpDetails.marketPlaceProduct=true, marketPlaceOfferData.shopName={name}, condition={cond}, ld+json price={ld_price}'
    if mp == 'false':
        return 'Extra', DIRECT, 'pdpDetails.marketPlaceProduct=false (ld+json seller=Extra Stores는 마켓 상품에도 똑같이 들어가 근거로 안 씀)'
    return '', UNK, 'marketPlaceProduct 못 찾음'


def sharaf(d, h):
    name = g(r'"seller_name":"([^"]*)"', h)
    st = g(r'"seller_type":"(\w+)"', h)
    if not name:
        return '', UNK, 'seller_name 없음'
    if st == 'first_party':
        return name, DIRECT, f'dataLayer seller_name={name}, seller_type=first_party'
    if st == 'marketplace':
        return name, EXT, f'dataLayer seller_name={name}, seller_type=marketplace'
    return name, UNK, f'seller_type={st}'


def liverpool(d, h):
    u = unesc(h)
    pid = d['요청URL'].rstrip('/').split('/')[-1].split('?')[0]
    pm = re.search(r'"productInfo":\{"title".{0,3000}?"productId":"(\d+)".*?"isMarketPlace":(\w+).*?"hasHybridSeller":(\w+)', u)
    if not pm or pm.group(1) != pid:
        return '', UNK, '메인 상품 productInfo 못 찾음'
    ismp, hyb = pm.group(2), pm.group(3)
    pi = re.search(r'"productInfo".{0,6000}?"priceInfo":\{"salePrice":([\d.]+),"listPrice":\{"price":([\d.]+)\},"promoPrice":\{"price":([\d.]+)', u, re.S)
    prices = {float(x) for x in pi.groups()} if pi else set()
    bo = re.search(r'"offersInfo":\{"offers":\[.*?\],"bestOffer":\{[^{}]*?"sellerName":"([^"]*)"[^{}]*?"priceInfo":\{"salePrice":([\d.]+)', u, re.S)
    def cls(name):
        return BRAND if BRAND_RE.match(name) else EXT
    if ismp == 'true':
        if bo:
            return bo.group(1), cls(bo.group(1)), f'productInfo.isMarketPlace=true, offersInfo.bestOffer.sellerName={bo.group(1)}'
        return '', UNK, 'isMarketPlace=true인데 bestOffer 없음'
    if bo:
        if float(bo.group(2)) in prices:
            return bo.group(1), cls(bo.group(1)), f'hasHybridSeller={hyb}, bestOffer({bo.group(1)}) 가격={bo.group(2)}이 메인 상품 가격과 같음'
        return 'Liverpool', DIRECT, f'[애매] isMarketPlace=false, bestOffer({bo.group(1)} {bo.group(2)})는 메인 상품 가격과 달라 메인 아님으로 봄'
    return 'Liverpool', DIRECT, f'isMarketPlace=false, hasHybridSeller={hyb}, offersInfo 없음'


def lazada(d, h):
    sid = g(r'"sellerId":"(\d+)"', h)
    sn = g(r'"seller_name":"([^"]*)"', h)
    return (f'sellerId={sid}' if sid else ''), UNK, (
        f'판매자 이름은 HTML에 없음(seller_name="{sn}", ld+json seller.name 빈칸; "Sold by Lazada"는 번역 문구 목록일 뿐); '
        f'sellerId={sid}만 있음')


MOMO_ENTP = {}


def momo(d, h):
    u = unesc(h)
    title = d['제목']
    refurb = bool(REFURB_TITLE.search(title))
    m = re.search(r'"shop":\{"name":"([^"]*)".*?"entpCode":"(\w+)"', u)
    url_ent = g(r'/TP/(TP\d+)/goodsDetail/', d['요청URL'])
    if m:
        name = m.group(1)
        MOMO_ENTP[m.group(2)] = name
        why = f'goodsDetail 데이터의 shop.name={name}, entpCode={m.group(2)}'
        if refurb:
            return name, REFURB, why + '; 제목에 福利品(B급·전시 상품)'
        return name, EXT, why
    if url_ent:
        return ('@ENT:' + url_ent), '@ENT', '주소의 입점사코드'
    if 'GoodsDetail.jsp' in d['요청URL']:
        ent = g(r'"entpCode":"(\w*)"', u)
        why = f'[추정] 옛 형식 주소(GoodsDetail.jsp), shop(입점 상점) 블록 없음, 공급사코드 {ent}'
        if refurb:
            return 'momo', REFURB, why + '; 제목에 福利品'
        return 'momo', DIRECT, why
    return '', UNK, '판매자 블록 못 찾음'


def dmx(d, h):
    u = unesc(h)
    sid = g(r'"sellerId":(\d+),"sellerType":(\d+)', u, grp=0)
    mm = re.search(r'"sellerId":(\d+),"sellerType":(\d+)', u)
    ld = g(r'"seller":\{"@id":"([^"]+)"', u)
    if mm and mm.group(1) == '2' and ld and ld.endswith('dienmayxanh.com/#organization'):
        return 'Điện máy XANH', DIRECT, f'상품 데이터 sellerId=2, sellerType=0; ld+json offers.seller=사이트 본체(#organization)'
    return '', UNK, f'sellerId={mm.groups() if mm else None}'


RULES = {('Appliance Online', None): appliance_online, ('COSTCO', None): costco, ('Cairo Sales', None): cairo,
         ('Electroplanet', None): electroplanet, ('EXTRA', None): extra, ('Sharaf DG', None): sharaf,
         ('LIVERPOOL', None): liverpool, ('LAZADA', 'Singapore'): lazada, ('LAZADA', 'Thailand'): lazada,
         ('MOMOSHOP', None): momo, ('DIENMAYXANH', None): dmx}


def main():
    all_rows = [json.loads(l) for l in open(Z + '/pages_best.jsonl', encoding='utf-8')]
    res = []
    for (ret, cty), fn in RULES.items():
        rs = [d for d in all_rows if d['리테일러'] == ret and d['페이지상태'] == '정상' and (cty is None or d['국가'] == cty)]
        part = []
        for d in rs:
            h = load(d)
            seller, cls, why = fn(d, h)
            part.append([d['요청URL'], d['국가'], d['리테일러'], seller, cls, why])
        if ret == 'MOMOSHOP':  # 껍데기 페이지는 같은 입점사코드의 다른 페이지에서 이름을 가져옴
            for r in part:
                if r[4] == '@ENT':
                    ent = r[3][5:]
                    nm = MOMO_ENTP.get(ent)
                    if nm:
                        r[3], r[4], r[5] = nm, EXT, f'[추정] 페이지가 빈 껍데기; 주소 입점사코드 {ent}가 다른 페이지에서 "{nm}"로 확인됨'
                    else:
                        r[3], r[4], r[5] = '', UNK, f'페이지가 빈 껍데기, 입점사코드 {ent}의 이름을 모름'
        res += part
    with open(OUT, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['요청URL', '국가', '리테일러', '판매자', '판매자구분', '근거'])
        w.writerows(res)
    # 요약
    by = collections.defaultdict(list)
    for r in res:
        by[(r[2], r[1])].append(r)
    for k, rs in by.items():
        c = collections.Counter(r[4] for r in rs)
        print(k, len(rs), dict(c))
        top = collections.Counter((r[3], r[4]) for r in rs).most_common(6)
        print('   ', top)


if __name__ == '__main__':
    main()
