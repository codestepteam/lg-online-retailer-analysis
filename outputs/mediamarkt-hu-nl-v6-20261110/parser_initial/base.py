"""판매자 함수가 같이 쓰는 도구. 모든 함수는 (item, html, rules)를 받아 (판매자, 구분, 근거)를 돌려준다.

item은 url·country·retailer·title을 가진 사전이다. rules는 retailer_rules.json의 sellers 절에 실행 중 값이 더해진 것이다.
"""
import html as H
import json
import re
from html.parser import HTMLParser

DIRECT, EXTERNAL, BRAND, REFURB, UNKNOWN = "직판", "외부판매자", "브랜드공식점", "리퍼·중고", "확인불가"
MARKETPLACE_ONLY = "마켓플레이스 표시만 있고 판매자 이름 없음(D070)"
HIDDEN_BLOCKS = re.compile(r"(?is)<(?:script|style|noscript)\b[^>]*>.*?</(?:script|style|noscript)\s*>")


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.hidden = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def text_of(fragment):
    parser = VisibleText()
    parser.feed(fragment)
    return re.sub(r"\s+", " ", H.unescape(" ".join(parser.parts))).strip()


def visible_html(html):
    """추천 상품 데이터나 스크립트 안 값이 본 상품 문구로 잡히지 않게 숨은 블록을 뺀다."""
    return HIDDEN_BLOCKS.sub("", html)


def main_heading(html):
    """(제목 글자, 제목이 끝나는 위치). 본 상품 제목(h1)이 없으면 ("", None)."""
    visible = visible_html(html)
    found = re.search(r"(?is)<h1\b[^>]*>(.*?)</h1>", visible)
    return (text_of(found.group(1)), found.end()) if found else ("", None)


def clean(fragment):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def pipe_text(fragment):
    fragment = re.sub(r"<script.*?</script>|<style.*?</style>", "", fragment, flags=re.S)
    fragment = re.sub(r"<[^>]+>", "|", fragment)
    fragment = H.unescape(fragment.replace("&nbsp;", " "))
    return re.sub(r"\s+", " ", re.sub(r"(\|\s*)+", "|", fragment))


def unescape_json(html):
    return html.replace('\\"', '"')


def first(pattern, text, flags=0, group=1):
    found = re.search(pattern, text, flags)
    return found.group(group) if found else None


def display_name(item, rules):
    return rules["names"][item["retailer"]]


def json_ld_blocks(html):
    blocks = []
    for found in re.finditer(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", html, re.S | re.I):
        source = found.group(1).strip()
        for text in (source, re.sub(r"[\x00-\x1f]+", " ", source)):
            try:
                blocks.append(json.loads(text))
                break
            except ValueError:
                pass
    return blocks


def is_type(value, name):
    kind = value.get("@type")
    return kind == name or (isinstance(kind, list) and name in kind)


def main_product(html):
    """페이지 맨 위 단계의 Product. 다른 상품 안에 끼어 있는 연관 상품은 보지 않는다."""
    for block in json_ld_blocks(html):
        for value in block if isinstance(block, list) else [block]:
            if not isinstance(value, dict):
                continue
            if is_type(value, "Product"):
                return value
            for node in value.get("@graph") or []:
                if isinstance(node, dict) and is_type(node, "Product"):
                    return node
    return None


def first_offer(product):
    offers = product.get("offers")
    if isinstance(offers, dict):
        return offers["offers"][0] if isinstance(offers.get("offers"), list) and offers["offers"] else offers
    return offers[0] if isinstance(offers, list) and offers and isinstance(offers[0], dict) else {}


def condition_of(product):
    return str(first_offer(product).get("itemCondition", "")).split("/")[-1]


def seller_of(product):
    seller = first_offer(product).get("seller")
    return (seller.get("name") if isinstance(seller, dict) else seller) or ""
