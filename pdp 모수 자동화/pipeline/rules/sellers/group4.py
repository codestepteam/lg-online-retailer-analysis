"""10월 seller_g4의 나머지 리테일러 함수, Sharaf 화면 판정(K1), Lazada 상품별 연결(K2), step2의 Falabella·보완표였던 Magalu·Appliance Online."""
import re

from .base import BRAND, DIRECT, EXTERNAL, MARKETPLACE_ONLY, REFURB, UNKNOWN, first, main_heading, text_of, unescape_json, visible_html


def appliance_online(item, html, rules):
    if re.search(rules["appliance_shell"], html):
        return "", UNKNOWN, "HTML이 상품 정보 없는 홈페이지 빈 껍데기(자바스크립트로 나중에 그리는 화면)"
    return rules["names"][item["retailer"]], DIRECT, "추정: 판매자 표시 없음, 외부 판매자·리퍼 표시 없음"


def costco(item, html, rules):
    data = unescape_json(html)
    third_party = first(r'"isThirdPartyIncluded":(\w+)', data)
    if third_party == "true":
        return "", UNKNOWN, "isThirdPartyIncluded=true (의미 미확인, 외부 판매자 가능성 배제 못함)"
    return rules["names"][item["retailer"]], DIRECT, f'[추정] 판매자 칸 없음; Costco 품목번호 sku={first(r"\"sku\":\"(\d+)\"", html)}, 배송방식 {first(r"\"carrier\":\"([^\"]+)\"", data)}, isThirdPartyIncluded=false'


def cairo_sales(item, html, rules):
    if 'itemprop="offers"' in html and "NewCondition" in html:
        return rules["names"][item["retailer"]], DIRECT, "[추정] 판매자 칸 없음; 단일 상점(ld+json LocalBusiness=Cairo Sales Stores), offers에 seller 없음, itemCondition=New"
    return "", UNKNOWN, "상품 offers 정보 없음"


def electroplanet(item, html, rules):
    if '"@type":"Product"' in html and '"offers"' in html:
        return rules["names"][item["retailer"]], DIRECT, "[추정] 판매자 칸 없음; Product ld+json offers에 seller 없음, 단일 상점"
    return "", UNKNOWN, "Product ld+json 없음"


def extra(item, html, rules):
    market = first(r'"marketPlaceProduct":(\w+)', html)
    if market == "true":
        name = first(r'"marketPlaceOfferData":\{.{0,3000}?"shopName":"([^"]*)"', html, re.S) or first(r'"marketPlaceShopDetails":\{"id":"\d+","name":"([^"]*)"', html) or ""
        condition = first(r'"marketPlaceOfferData":\{.{0,3000}?"conditionCode":"(\w+)"', html, re.S)
        if condition and condition != "NEW":
            return name, REFURB, f"marketPlaceProduct=true, offer conditionCode={condition}"
        return name, EXTERNAL, f'pdpDetails.marketPlaceProduct=true, marketPlaceOfferData.shopName={name}, condition={condition}, ld+json price={first(r"\"price\"\s*:\s*\"?([\d.]+)", html)}'
    if market == "false":
        return rules["names"][item["retailer"]], DIRECT, "pdpDetails.marketPlaceProduct=false (ld+json seller=Extra Stores는 마켓 상품에도 똑같이 들어가 근거로 안 씀)"
    return "", UNKNOWN, "marketPlaceProduct 못 찾음"


def sharaf(item, html, rules):
    """본 상품 판매 영역의 Sold by만 본다. HTML 첫 seller_name과 Fulfilled by는 쓰지 않는다(K1, D100)."""
    settings = rules["sharaf"]
    _, heading_end = main_heading(html)
    if heading_end is None:
        return "", UNKNOWN, "본 상품 제목(h1) 없음"
    segment = visible_html(html)[heading_end:heading_end + 180_000]
    for stop in settings["section_stops"]:
        found = re.search(stop, segment, re.I)
        if found:
            segment = segment[:found.start()]
    phrase = re.search(settings["sold_by"], segment, re.I)
    if not phrase:
        return "", UNKNOWN, "본 상품 판매 영역에 Sold by 없음"
    following = segment[phrase.end():phrase.end() + 2200]
    nodes = [text_of(part).strip(" :") for part in re.split(r"<[^>]+>", following)]
    name = next((node for node in nodes if node), "")
    name = re.split(settings["sold_by_end"], name, flags=re.I)[0].strip()
    if not name:
        return "", UNKNOWN, "Sold by 문구는 있으나 판매자 이름을 읽지 못함"
    return name, DIRECT if name.casefold() == settings["direct"] else EXTERNAL, f"본 상품 판매 영역: Sold by {name}"


def liverpool(item, html, rules):
    data = unescape_json(html)
    product = item["url"].rstrip("/").split("/")[-1].split("?")[0]
    info = re.search(r'"productInfo":\{"title".{0,3000}?"productId":"(\d+)".*?"isMarketPlace":(\w+).*?"hasHybridSeller":(\w+)', data)
    if not info or info.group(1) != product:
        return "", UNKNOWN, "메인 상품 productInfo 못 찾음"
    marketplace, hybrid = info.group(2), info.group(3)
    price = re.search(r'"productInfo".{0,6000}?"priceInfo":\{"salePrice":([\d.]+),"listPrice":\{"price":([\d.]+)\},"promoPrice":\{"price":([\d.]+)', data, re.S)
    prices = {float(value) for value in price.groups()} if price else set()
    best = re.search(r'"offersInfo":\{"offers":\[.*?\],"bestOffer":\{[^{}]*?"sellerName":"([^"]*)"[^{}]*?"priceInfo":\{"salePrice":([\d.]+)', data, re.S)
    kind = lambda name: BRAND if re.match(rules["brand_official_liverpool"], name, re.I) else EXTERNAL
    direct = rules["names"][item["retailer"]]
    if marketplace == "true":
        if best:
            return best.group(1), kind(best.group(1)), f"productInfo.isMarketPlace=true, offersInfo.bestOffer.sellerName={best.group(1)}"
        return "", EXTERNAL, f"{MARKETPLACE_ONLY}: isMarketPlace=true인데 bestOffer 없음"
    if best:
        if float(best.group(2)) in prices:
            return best.group(1), kind(best.group(1)), f"hasHybridSeller={hybrid}, bestOffer({best.group(1)}) 가격={best.group(2)}이 메인 상품 가격과 같음"
        return direct, DIRECT, f"[애매] isMarketPlace=false, bestOffer({best.group(1)} {best.group(2)})는 메인 상품 가격과 달라 메인 아님으로 봄"
    return direct, DIRECT, f"isMarketPlace=false, hasHybridSeller={hybrid}, offersInfo 없음"


def lazada_item_id(url):
    found = re.search(r"-i(\d+)(?=[-.?/]|$)", url.split("___")[0])
    return found.group(1) if found else ""


def lazada(item, html, rules):
    """판매자 번호로 이름을 잇지 않는다(서로 다른 매장이 번호를 공유, K2). 국가+상품 번호가 표에 있을 때만 쓴다."""
    known = rules["lazada_items"].get(f"{item['country']}|{lazada_item_id(item['url'])}")
    if known:
        return known["seller"], known["kind"], f"10월 상품별 화면 확인값(11월 화면 아님): {known['evidence']}"
    seller_id = first(r'"sellerId":"(\d+)"', html)
    return f"sellerId={seller_id}" if seller_id else "", UNKNOWN, f"판매자 이름은 HTML에 없음; sellerId={seller_id}만 있음, 상품 번호가 연결표에 없음"


def momo_collect(item, html, rules, context):
    found = re.search(r'"shop":\{"name":"([^"]*)".*?"entpCode":"(\w+)"', unescape_json(html))
    if found:
        context.setdefault("momo_shops", {})[found.group(2)] = found.group(1)


def momo(item, html, rules, context):
    data = unescape_json(html)
    refurb = bool(re.search(rules["momo_refurb_title"], item["title"], re.I))
    shop = re.search(r'"shop":\{"name":"([^"]*)".*?"entpCode":"(\w+)"', data)
    if shop:
        evidence = f"goodsDetail 데이터의 shop.name={shop.group(1)}, entpCode={shop.group(2)}"
        return shop.group(1), REFURB if refurb else EXTERNAL, evidence + ("; 제목에 福利品(B급·전시 상품)" if refurb else "")
    code = first(r"/TP/(TP\d+)/goodsDetail/", item["url"])
    if code:
        name = context.get("momo_shops", {}).get(code)
        if name:
            return name, EXTERNAL, f'[추정] 페이지가 빈 껍데기; 주소 입점사코드 {code}가 다른 페이지에서 "{name}"로 확인됨'
        return f"입점 상점 {code}", EXTERNAL, f"[추정] 페이지가 빈 껍데기; 주소가 /TP/{code}/goodsDetail/ 꼴이라 mo店+ 입점 상점 상품(v8 /TP/ 규칙, D142·D144). 상점 이름은 모름"
    if "GoodsDetail.jsp" in item["url"]:
        evidence = f'[추정] 옛 형식 주소(GoodsDetail.jsp), shop(입점 상점) 블록 없음, 공급사코드 {first(r"\"entpCode\":\"(\w*)\"", data)}'
        return rules["names"][item["retailer"]], REFURB if refurb else DIRECT, evidence + ("; 제목에 福利品" if refurb else "")
    return "", UNKNOWN, "판매자 블록 못 찾음"


def dienmayxanh(item, html, rules):
    data = unescape_json(html)
    seller = re.search(r'"sellerId":(\d+),"sellerType":(\d+)', data)
    site = first(r'"seller":\{"@id":"([^"]+)"', data)
    if seller and seller.group(1) == "2" and site and site.endswith(rules["dienmayxanh_site"]):
        return rules["names"][item["retailer"]], DIRECT, "상품 데이터 sellerId=2, sellerType=0; ld+json offers.seller=사이트 본체(#organization)"
    return "", UNKNOWN, f"sellerId={seller.groups() if seller else None}"


def falabella(item, html, rules):
    name = first(r'"sellerName"\s*:\s*"([^"]+)"', html) or ""
    return name, DIRECT if name.upper() == rules["falabella_direct"] else (EXTERNAL if name else UNKNOWN), f'sellerName "{name}"'


def magalu(item, html, rules):
    found = re.search(rules["magalu_sold_by"], text_of(html))
    if not found:
        return "", UNKNOWN, "화면에 Vendido por 문구 없음"
    name = found.group(1).strip()
    return name, DIRECT if name.lower() == rules["magalu_direct"] else EXTERNAL, f"화면: {found.group(0)}"
