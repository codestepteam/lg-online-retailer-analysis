"""10월 seller_g3의 체코·폴란드·스웨덴·영국 리테일러 함수."""
import html as H
import re

from .base import DIRECT, EXTERNAL, REFURB, UNKNOWN, condition_of, main_product, seller_of

USED = ("UsedCondition", "RefurbishedCondition", "DamagedCondition")


def alza(item, html, rules):
    product, name = main_product(html), rules["names"][item["retailer"]]
    if not product:
        return "", UNKNOWN, "ld+json Product 없음"
    condition = condition_of(product)
    if condition in USED:
        return name, REFURB, f"ld+json offers.itemCondition={condition} (판매자 필드 없음, 운영사 Alza로 추정)"
    return name, DIRECT, f"추정: 판매자 표시 없음. ld+json itemCondition={condition}, 마켓플레이스 문구 없음"


def datart(item, html, rules):
    product, name, bazaar = main_product(html), rules["names"][item["retailer"]], "/bazar/" in item["url"]
    if product:
        seller, condition = seller_of(product), condition_of(product)
        evidence = f"ld+json offers.seller.name={seller}; itemCondition={condition}"
        if bazaar or condition in USED:
            return seller or name, REFURB, evidence + "; URL /bazar/"
        return seller or name, DIRECT, evidence
    if bazaar and "product-detail-title" in html:
        return name, REFURB, "URL /bazar/ + product-detail-title (ld+json 없음, 판매자는 운영사 DATART로 추정)"
    return "", UNKNOWN, "ld+json Product 없음, 본문이 빈 껍데기 페이지"


def media_expert(item, html, rules):
    start = html.find("<h1")
    found = re.search(r'seller-label[^>]*>\s*Sprzedawca:\s*</span>\s*<span class="seller-name[^"]*"[^>]*>(.*?)</span>', html[start:] if start >= 0 else html, re.S)
    if not found:
        return "", UNKNOWN, "Sprzedawca 표시 없음"
    seller = H.unescape(found.group(1)).strip()
    if "/outlet/" in item["url"]:
        state = re.search(r"Stan produktu:\s*([^<]{0,40})", html)
        return seller, REFURB, f"Sprzedawca: {seller}; URL /outlet/; Stan produktu 표시" + (f" ({H.unescape(state.group(1)).strip()})" if state and state.group(1).strip() else "")
    if seller.lower().replace(" ", "") == rules["media_expert_direct"]:
        return seller, DIRECT, f"Sprzedawca: {seller}"
    return seller, EXTERNAL, f"Sprzedawca: {seller} (Media Expert 아님)"


def rtv_euro_agd(item, html, rules):
    product, name = main_product(html), rules["names"][item["retailer"]]
    if not product:
        return "", UNKNOWN, "ld+json Product 없음"
    condition = condition_of(product)
    if condition != "NewCondition":
        return name, REFURB, f"ld+json itemCondition={condition}"
    return name, DIRECT, f"추정: ld+json offers.seller.name이 빈 문자열, itemCondition={condition}, 외부 판매자 표시 없음"


def elgiganten(item, html, rules):
    product, name = main_product(html), rules["names"][item["retailer"]]
    if not product:
        return "", UNKNOWN, "ld+json Product 없음"
    flags = {key: re.findall(r'\\"' + key + r'\\":(true|false)', html) for key in ("isMarketplaceProduct", "isMarketPlaceProduct", "isOutletProduct", "isOutlet", "isDropship")}
    text = ",".join(f"{key}={'/'.join(sorted(set(values)))}" for key, values in flags.items() if values)
    if "true" in flags["isMarketplaceProduct"] + flags["isMarketPlaceProduct"]:
        return "", EXTERNAL, text
    if "true" in flags["isOutletProduct"] + flags["isOutlet"]:
        return name, REFURB, text
    return name, DIRECT, f"페이지 내 플래그: {text or '플래그 없음'} (판매자 이름 필드는 없음, 운영사로 추정)"


def currys(item, html, rules):
    product = main_product(html)
    if not product:
        return "", UNKNOWN, "ld+json Product 없음: 상품이 아닌 목록(카테고리) 페이지가 저장됨"
    return rules["names"][item["retailer"]], DIRECT, f"추정: 판매자 표시 없음. ld+json itemCondition={condition_of(product)}, 마켓플레이스 문구 없음"


def ao(item, html, rules):
    product, name = main_product(html), rules["names"][item["retailer"]]
    if not product:
        return "", UNKNOWN, "ld+json Product 없음"
    seller, condition = seller_of(product), condition_of(product)
    if condition != "NewCondition":
        return seller or name, REFURB, f"itemCondition={condition}"
    if seller.lower() in rules["ao_direct"]:
        return seller, DIRECT, f"ld+json offers.seller.name={seller}; itemCondition={condition}"
    return seller, EXTERNAL if seller else UNKNOWN, f"ld+json offers.seller.name={seller}"
