"""10월 seller_g1의 프랑스·스페인·포르투갈·네덜란드 리테일러 함수."""
import html as H
import json
import re

from .base import DIRECT, EXTERNAL, BRAND, REFURB, UNKNOWN, clean


def boulanger(item, html, rules):
    found = re.search(r'id="product-merchant__condition">(.*?)</p>', html, re.S)
    # 11-24 화면 일부: <p class="merchant__header"><span class="merchant__condition">Produit neuf</span> vendu et expédié par <span class="merchant__name">Boulanger</span>
    found = found or re.search(r'<p class="merchant__header"[^>]*>(.*?)</p>', html, re.S)
    if not found:
        return "", UNKNOWN, "판매자 문구 블록(product-merchant__condition) 없음 - 상품 페이지가 아닌 목록 페이지로 보임"
    block = found.group(1)
    title = re.search(r'title="([^"]*)"', block) or re.search(r'class="merchant__name[^"]*"[^>]*>(.*?)</(?:span|a)>', block, re.S)
    name = clean(title.group(1)) if title else clean(block)
    condition = clean(re.split(r"(?i)vendu", clean(block))[0])
    evidence = f"{condition} / vendu & expédié par {name}"
    settings = rules["boulanger"]
    if re.search(settings["refurb_condition"], condition, re.I):
        return name, REFURB, evidence
    if name.lower() == settings["direct"]:
        return name, DIRECT, evidence
    if name.lower() in settings["brand_group"]:
        return name, BRAND, evidence + " (브랜드 그룹 입점 - 브랜드 공식 판매로 판단, 추정)"
    return name, REFURB if re.search(settings["refurb_external"], condition, re.I) else EXTERNAL, evidence


def darty(item, html, rules):
    settings = rules["darty"]
    screen = re.search(r'product-mkp-seller-info.*?class="mkp-seller-name[^"]*">([^<]*)<', html, re.S)
    meta = re.findall(r'itemprop="seller"\s+content="([^"]*)"', html)
    condition = re.search(r'itemprop="itemCondition"\s+content="https://schema.org/(\w+)"', html)
    condition = condition.group(1) if condition else ""
    availability = re.search(r'itemprop="availability"\s+href="https://schema.org/(\w+)"', html)
    availability = availability.group(1) if availability else ""
    if screen:
        name = H.unescape(screen.group(1)).strip()
        evidence = f'화면 판매자 블록 "Vendu et expédié par {name}" / 상태 {condition}'
        if meta and H.unescape(meta[0]) != name:
            evidence += f" (메타 seller={meta[0]}와 다름 - 화면 블록 우선)"
    elif meta:
        name = H.unescape(meta[0]).strip()
        if name.lower() == settings["direct"] and settings["marketplace_url_tag"] in item["url"]:
            return "", UNKNOWN, f'주소에 {settings["marketplace_url_tag"]} 꼬리표(마켓플레이스 상품 표시)가 있는데 화면 판매자 블록이 없고 메타만 {name}'
        evidence = f'메타 itemprop=seller "{name}" / 상태 {condition} / {availability}'
    else:
        return "", UNKNOWN, "판매자 블록과 메타 seller 모두 없음 (오퍼 정보 없는 페이지)"
    low = name.lower()
    if re.search(settings["refurb_seller"], low) or condition == "UsedCondition":
        return name, REFURB, evidence
    return name, DIRECT if low == settings["direct"] else EXTERNAL, evidence


def el_corte_ingles(item, html, rules):
    blocks = re.findall(r'"_single_sku":\{([^{}]*)\}', html)
    if not blocks:
        return "", UNKNOWN, "_single_sku 없음"
    value = lambda pattern: (re.search(pattern, blocks[0]) or [None, ""])[1]
    provider, provider_name, marketplace = value(r'"provider":"([^"]*)"'), value(r'"provider_name":"([^"]*)"'), value(r'"marketplace":(\w+)')
    evidence = f"_single_sku provider={provider}, provider_name={provider_name}, marketplace={marketplace}"
    if provider == "eci" and marketplace == "false":
        return rules["names"][item["retailer"]], DIRECT, evidence
    return provider_name, EXTERNAL, evidence


def mediamarkt_es_nl(item, html, rules, *, screen=True):
    country = rules["mediamarkt_country_codes"][item["country"]]
    found = re.search(r"-(\d+)\.html", item["url"])
    if not found:
        return "", UNKNOWN, "상품 페이지 주소가 아님(메인 상품 id 없음)"
    product = found.group(1)
    prices = re.findall(r'"id":"Media:%s:%s(?:\[\d+\])?","currency":"[A-Z]+","isProductOfTypeMarketplace":(\w+)[^{}]*?"marketplaceSeller":(null|\{[^{}]*\})' % (country, product), html)
    flag = "true" if any(market == "true" for market, _ in prices) else ("false" if prices else "none")
    seller = ""
    for _, block in prices:
        name = re.search(r'"sellerName":"((?:[^"\\]|\\.)*)"', block) if block != "null" else None
        if name:
            seller = json.loads(f'"{name.group(1)}"') if "\\" in name.group(1) else name.group(1)
            break
    status = re.search(r'"id":"Media:%s:%s","isAvailableForDelivery":\w+,"isAvailableForPickup":\w+,"isAvailableAndBuyable":\w+,"isInAssortment":\w+,"onlineStatus":"(\w+)"' % (country, product), html)
    status = status.group(1) if status else "없음"
    link = re.search(r'data-test="additional-info-normal"[^>]*>(?:%s) <a[^>]*mms-third-party-provider-link[^>]*><span[^>]*>([^<]*)<' % "|".join(rules["mediamarkt_sold_by"]), html) if screen else None
    link = H.unescape(link.group(1)).strip() if link else ""
    condition = re.search(r'"id":"Media:%s:%s\[\d+\]","categoryIds":\[[^\]]*\],"locale":"[^"]*","offer":\{[^{}]*"conditionType":"(\w+)"' % (country, product), html)
    condition = condition.group(1) if condition else ""
    if flag == "true":
        name = seller or link
        evidence = f'메인id {product}: isProductOfTypeMarketplace=true, marketplaceSeller.sellerName={name}, conditionType={condition or "-"}, onlineStatus={status}'
        return name, REFURB if condition and condition != "NEW" else EXTERNAL, evidence
    if link:
        return link, EXTERNAL, f'메인id {product}: 구조값 isProductOfTypeMarketplace={flag}(onlineStatus={status})이나 화면 구매박스에 마켓플레이스 판매자 "{link}" 표시 (애매 - 화면 기준 외부판매자)'
    if flag == "false":
        return rules["names"][item["retailer"]], DIRECT, f"메인id {product}: isProductOfTypeMarketplace=false, marketplaceSeller=null, onlineStatus={status}"
    return "", UNKNOWN, f"메인id {product}의 가격/판매자 정보가 HTML에 없음(onlineStatus={status})"


def worten(item, html, rules):
    block = re.search(r'<div class="neu-02-bg seller-info".*?(?=<!--\]-->)', html, re.S)
    if not block:
        return "", UNKNOWN, "seller-info 블록 없음"
    block = block.group(0)
    conditions = re.search(r'id="sellerConditions"[^>]*>(.*?)</div>', html, re.S)
    conditions = clean(conditions.group(1)) if conditions else ""
    if "seller-info__seller-link" in block:
        name = clean(re.search(r'<b class="h-underline"[^>]*>(.*?)</b>', block, re.S).group(1))
        kind, evidence = EXTERNAL, f'seller-info "Vendido por {name}" (marketplace 클래스)'
    else:
        name, kind, evidence = rules["names"][item["retailer"]], DIRECT, 'seller-info "Vendido por" + Worten 로고'
    if re.search(rules["worten_refurb"], conditions, re.I):
        return name, REFURB, evidence + f" / 판매조건 문구: {conditions[:80]}"
    return name, kind, evidence


def coolblue(item, html, rules):
    condition = re.search(r"schema.org/(\w+Condition)", html)
    stock = re.search(r"schema.org/(InStock|SoldOut|OutOfStock|PreOrder)", html)
    return rules["names"][item["retailer"]], DIRECT, f'(추정) HTML 어디에도 판매자(seller) 표시가 없음 - 직판으로 간주. 오퍼 상태 {condition.group(1) if condition else "-"}, 재고 {stock.group(1) if stock else "-"}'
