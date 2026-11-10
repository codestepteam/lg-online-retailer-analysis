"""10월 seller_g2의 MediaMarktSaturn(독일·헝가리·이탈리아)·Amazon·OTTO·Unieuro 함수와 독일 MediaMarkt 화면 판정(K6)."""
import html as H
import re

from .base import DIRECT, EXTERNAL, BRAND, REFURB, UNKNOWN, MARKETPLACE_ONLY, main_heading, pipe_text, text_of, visible_html


def mediamarkt_saturn(item, html, rules):
    found = re.search(r"-(\d+)(?:\.html)?(?:\?.*)?$", item["url"])
    if not found:
        return "", UNKNOWN, "URL에 상품 id 없음(상품 페이지 아님)"
    product = found.group(1)
    data = html if '"isProductOfTypeMarketplace"' in html else html.replace('\\"', '"')
    main, match_text = product, ""
    for match in re.finditer(r'"productId":"(\d+)","retailProductId":"?(\d*)"?,"marketplaceProductId":"?(\d*)"?,"preferredProductId":"?(\d+)"?', data):
        if product in match.group(1, 2, 3):
            main, match_text = match.group(4), data[match.start():match.start() + 3000]
            break
    flag = None
    for candidate in (main, product):
        flag = re.search(r'"id":"[A-Za-z]+:[a-z]{2}:%s","currency":[^,]*,"isProductOfTypeMarketplace":(true|false)' % candidate, data)
        if flag:
            main = candidate
            break
    if not flag:
        return "", UNKNOWN, f"가격 정보 블록 없음(id {product})"
    if flag.group(1) == "false":
        return rules["names"][item["retailer"]], DIRECT, f"isProductOfTypeMarketplace=false(id {main})"
    segment = data[flag.end():flag.end() + 700]
    seller = re.search(r'"marketplaceSeller":(\{[^}]*\}|null)', segment)
    name = re.search(r'"sellerName":"([^"]*)"', seller.group(1)) if seller else None
    if not name:
        return "", EXTERNAL, f"{MARKETPLACE_ONLY}: isProductOfTypeMarketplace=true, marketplaceSeller=null, id {main}"
    name = H.unescape(name.group(1))
    condition = re.search(r'"bestMarketplaceOffers":\[\{[^\]]*?"offerCondition":"(\w+)"', match_text)
    condition = condition.group(1) if condition else None
    evidence = f"isProductOfTypeMarketplace=true; marketplaceSeller.sellerName={name}"
    if condition and condition != "NEW":
        return name, REFURB, evidence + f"; offerCondition={condition}"
    if name in rules["mediamarkt_de"]["refurb_sellers"]:
        return name, REFURB, evidence + "; (그룹 자체 리퍼 판매자, 조건값 미확인)"
    return name, BRAND if re.match(rules["brand_official_mms"], name, re.I) else EXTERNAL, evidence


def mediamarkt_de(item, html, rules):
    """본 상품 제목과 판매 영역 문구를 먼저 보고, 문구가 없을 때만 구조값으로 판단한다(D103)."""
    settings = rules["mediamarkt_de"]
    title, heading_end = main_heading(html)
    if heading_end is None:
        return "", UNKNOWN, "본 상품 제목(h1) 없음"
    title_hit = re.search(settings["refurb_title"], title, re.I)
    segment = visible_html(html)[heading_end:heading_end + 180_000]
    for stop in settings["section_stops"]:
        found = re.search(stop, segment, re.I)
        if found:
            segment = segment[:found.start()]
    phrase = re.search(settings["seller_phrase"], segment, re.I)
    seller = ""
    if phrase:
        anchor = re.search(r"(?is)<a\b[^>]*>(.*?)</a>", segment[phrase.end():phrase.end() + 2200])
        seller = text_of(anchor.group(1)) if anchor else ""
    if title_hit:
        return seller, REFURB, f"본 상품 제목 리퍼·중고 표현: {title_hit.group()}" + (f"; 판매자 {seller}" if seller else "")
    if phrase and not seller:
        return "", UNKNOWN, "판매 문구는 있으나 판매자 이름을 읽지 못함"
    if seller:
        evidence = f"본 상품 판매 영역: {phrase.group()} {seller}"
        if seller in settings["refurb_sellers"]:
            return seller, REFURB, evidence
        if seller.casefold() in settings["direct"]:
            return seller, DIRECT, evidence
        return seller, BRAND if re.match(rules["brand_official_mms"], seller, re.I) else EXTERNAL, evidence
    return mediamarkt_saturn(item, html, rules)


def _block(html, name):
    start = html.find(f'id="{name}"')
    if start < 0:
        return None
    following = re.search(r'<div id="\w+_feature_div"', html[start + 30:])
    return html[start:start + 30 + following.start()] if following else html[start:start + 3000]


def _tokens(block):
    if not block:
        return None
    tokens = [token for token in pipe_text(block).split("|") if token.strip()]
    return tokens[1:] if tokens and tokens[0].startswith("id=") else tokens


def _buybox(html):
    start = html.find('id="buybox"')
    return pipe_text(html[start:start + 9000]) if start >= 0 else ""


def _merchant_ids(html):
    return re.findall(r'id="merchantID" name="merchantID" value="([A-Z0-9]+)"', html)


def amazon_collect(item, html, rules, context):
    """다른 페이지에서 판매자 번호와 이름의 짝을 모은다. 중고 구매상자는 이름 문구가 없을 수 있어 이 표를 쓴다."""
    names = context.setdefault("amazon_ids", dict(rules["amazon"]["known_ids"]))
    block = _block(html, "merchantInfoFeature_feature_div")
    for seller, name in re.findall(r"seller=([A-Z0-9]+)[^>]*>([^<]*)</a>", block or ""):
        names.setdefault(seller, H.unescape(name).strip())
    sold = re.search(rules["amazon"]["sold_by"], _buybox(html))
    ids = _merchant_ids(html)
    if sold and ids:
        names.setdefault(ids[0], sold.group(1).strip())


def amazon(item, html, rules, context):
    settings = rules["amazon"]
    buybox = _buybox(html)
    head_match = re.match(r"[^>]*>\s*\|?\s*(.*)", buybox)
    head = head_match.group(1)[:80] if head_match else ""
    ids = _merchant_ids(html)
    first_id = ids[0] if ids else None
    names = context.get("amazon_ids", {})
    merchant = _block(html, "merchantInfoFeature_feature_div")
    fulfiller, merchant_tokens = _tokens(_block(html, "fulfillerInfoFeature_feature_div")), _tokens(merchant)
    if re.match(settings["used_heading"], head, re.I):
        sold = re.search(settings["sold_by"], buybox)
        name = sold.group(1).strip() if sold else names.get(first_id, f"(판매자ID {first_id})")
        return name, REFURB, f'구매상자 제목 "{head[:30]}"' + (f'; 판매자 문구 "{name}"' if sold else f"; merchantID={first_id}")
    if merchant_tokens and len(merchant_tokens) > 1:
        label = merchant_tokens[0]
        link = re.search(r"<a [^>]*seller=([A-Z0-9]+)[^>]*>([^<]*)</a>", merchant)
        name = H.unescape(link.group(2)).strip() if link else merchant_tokens[1]
        by_amazon = fulfiller and len(fulfiller) > 1 and fulfiller[1].startswith("Amazon")
        if not link and name == "Amazon":
            return "Amazon", DIRECT, f'"{label}: Amazon"'
        if re.match(rules["brand_official_mms"], name, re.I):
            return name, BRAND, f'"{label}: {name}"' + ("; Amazon 배송(FBA)" if by_amazon else "")
        return name, EXTERNAL, f'"{label}: {name}"' + (f'; 배송은 Amazon(FBA): "{fulfiller[0]}: {fulfiller[1]}"' if by_amazon else "; 판매자가 직접 배송")
    if re.search(settings["unavailable"], buybox[:400]):
        return "", UNKNOWN, settings["unavailable_evidence"]
    if re.search(settings["options_only"], buybox[:600], re.I):
        return "", UNKNOWN, settings["options_only_evidence"]
    return "", UNKNOWN, settings["no_seller_evidence"]


def otto(item, html, rules):
    found = re.search(r'<div class="retailer__info[^"]*"><span>Verkäufer:</span>(.*?)</oc-interactive-overlay-v2>', html, re.S)
    if not found:
        return "", UNKNOWN, '"Verkäufer:" 블록 없음'
    block = found.group(1)
    link = re.search(r"<oc-link-v2[^>]*>(.*?)</oc-link-v2>", block, re.S)
    if link:
        name = H.unescape(re.sub(r"<[^>]+>", "", link.group(1)).strip())
        return name, EXTERNAL, f'retailer__info "Verkäufer: {name}"'
    if 'logo="otto"' in block:
        return rules["names"][item["retailer"]], DIRECT, 'retailer__info "Verkäufer:" + otto 로고(partner/1000000)'
    return "", UNKNOWN, '"Verkäufer:" 블록 형식 불명'


def unieuro(item, html, rules):
    if re.search(r"-pid[A-Z0-9]+$", item["url"]) and rules["unieuro_direct_text"] in html:
        return rules["names"][item["retailer"]], DIRECT, f'[추정] 판매자 표시 자체가 HTML에 없음; "{rules["unieuro_direct_text"]}" 일반 안내문만 있고 마켓플레이스 표지 없음'
    return "", UNKNOWN, "상품 페이지 내용 없음(홈/빈 페이지)"
