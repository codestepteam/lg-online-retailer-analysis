"""헝가리·네덜란드 MediaMarkt의 본 상품 제목·판매자 문구 우선 검사(D124)."""
import re

from .base import DIRECT, EXTERNAL, REFURB, UNKNOWN, main_heading, text_of, visible_html


def mediamarkt_screen(item, html, rules):
    settings = rules["mediamarkt_screen"][item["country"]]
    title, heading_end = main_heading(html)
    if heading_end is not None:
        hit = re.search(settings["refurb_title"], title, re.I)
        if hit:
            return "", REFURB, f"본 상품 제목 리퍼·중고 표현: {hit.group()}"
        segment = visible_html(html)[heading_end:heading_end + 180_000]
        for stop in settings["section_stops"]:
            found = re.search(stop, segment, re.I)
            if found:
                segment = segment[:found.start()]
        # HTML 태그로 나뉜 문구도 읽되, 숨은 script/style 및 추천·설명 영역은 읽지 않는다.
        phrase = re.search(settings["seller_phrase"], segment, re.I)
        if phrase:
            following = segment[phrase.end():phrase.end() + 2200]
            anchor = re.search(r'(?is)<a\b([^>]*)>(.*?)</a>', following)
            # 관계없는 링크의 이름을 판매자로 삼지 않는다.
            if not anchor or not re.search(r'marketplace/seller/|third-party-provider', anchor.group(1), re.I):
                return "", UNKNOWN, "본 상품 판매 문구는 있으나 판매자 링크를 확인하지 못함"
            seller = text_of(anchor.group(2))
            if not seller:
                return "", UNKNOWN, "본 상품 판매 문구는 있으나 판매자 이름을 읽지 못함"
            evidence = f"본 상품 판매 영역: {text_of(phrase.group())} {seller}"
            if seller.casefold() in settings["direct"]:
                return seller, DIRECT, evidence
            return seller, EXTERNAL, evidence
    # 화면 문구가 없으면 기존 본 상품 ID의 내부 판매자 검사를 유지한다.
    from . import group1, group2
    fallback = {"mediamarkt_es_nl": group1.mediamarkt_es_nl,
                "mediamarkt_saturn": group2.mediamarkt_saturn}[settings["fallback"]]
    return fallback(item, html, rules)
