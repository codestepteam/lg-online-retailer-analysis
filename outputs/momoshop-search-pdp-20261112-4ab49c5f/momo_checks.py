"""Check main product seller, condition, and stock evidence for this MomoShop snapshot."""

import gzip
import json
import re
from pathlib import Path

from lxml import html


OUT = Path(__file__).resolve().parent
RULES = OUT.parents[1] / "pdp 모수 자동화/runs/2026-11/config/retailer_rules.json"
REFURB = re.compile(json.loads(RULES.read_text())["sellers"]["momo_refurb_title"], re.I)
SHOP = re.compile(r'"shop":\{"name":"([^"]*)".*?"entpCode":"(\w+)"')
BUY = {"直接購買", "放入購物車", "加入購物車"}
SOLD_OUT = "已售完"
RESTOCK = "補貨中"


def label(element):
    return " ".join((element.get("aria-label") or element.text_content()).split())


def html_signals(path):
    source = gzip.decompress(path.read_bytes()).decode("utf-8", "replace")
    document = html.fromstring(source)
    data = "\n".join(document.xpath("//script/text()")).replace(r'\"', '"')
    supplier = re.search(r'"entpCode":"(\w*)"', data)
    stock = re.search(r'"goodsStock":"([^"]*)"', data)
    offers = {label(button) for button in document.xpath("//button[not(@disabled)]")}
    offers.update(label(button) for button in document.xpath("//button[@disabled]") if RESTOCK in label(button))
    options = []
    for select in document.xpath('//select[option[contains(text(), "請選擇商品規格")]]'):
        values = [label(option) for option in select.xpath('option[@value!="" and not(@disabled)]')]
        if values and all(SOLD_OUT in value for value in values):
            options.extend(values)
    return {
        "shops": SHOP.findall(data), "entp": supplier[1] if supplier else "",
        "stock": stock[1] if stock else "", "offers": offers, "options": options,
    }


def inspect(identity, title):
    raw = OUT / "pdp_evidence" / f"goods-{identity}.html.gz"
    browser = OUT / "audit_evidence" / f"goods-{identity}.json"
    source = "상세 페이지 HTML"
    details = html_signals(raw) if raw.exists() else {}
    if not details and browser.exists():
        checked = json.loads(browser.read_text())
        if checked["verified"]:
            details = checked
            title = checked["pdp_title"] or title
            source = "내부 브라우저 재확인"
    if not details:
        source = "최초 브라우저 관찰 요약"
    offers = set(details.get("offers", []))
    restock = any(RESTOCK in offer for offer in offers)
    options = details.get("options", [])
    refurb = REFURB.search(title)
    return {
        "source": source, "supplier_code": details.get("entp", ""),
        "shop_names": [shop[0] for shop in details.get("shops", []) if shop[0]],
        "refurb_match": refurb.group() if refurb else "",
        "stock_code": details.get("stock", ""), "restock_label": restock,
        "sold_out_options": options,
        "stock_review": details.get("stock") == "0" and bool(options) and not restock and not offers & BUY,
    }


def apply(result, signals):
    if signals["supplier_code"] and not signals["shop_names"]:
        result["seller_basis"] = (
            "원래 상품 링크는 GoodsDetail.jsp, 본 상품에 입점 상점 표시 없음. "
            f"공급사 코드 {signals['supplier_code']} ({signals['source']})"
        )
    elif signals["source"] == "최초 브라우저 관찰 요약":
        result["seller_basis"] = "일반 상품 화면과 원래 상품 링크(GoodsDetail.jsp) 확인. 상세 판매자 데이터 미보존"
    if signals["shop_names"]:
        name = signals["shop_names"][0]
        result.update(decision="제외", exclusion_stage="③리리부", reason=f"본 상품 외부 판매자 ({name})",
                      seller=name, seller_basis=f"상세 상품 데이터의 상점명 ({signals['source']})")
    elif signals["refurb_match"]:
        result.update(decision="제외", exclusion_stage="③리리부",
                      reason=f"MomoShop 상세 상품명의 리퍼·중고 표현 {signals['refurb_match']}")
    elif signals["stock_review"]:
        result.update(decision="검토 필요", exclusion_stage="④품절",
                      reason="본 상품 선택 옵션에 無(已售完)(옵션 없음·품절) 표시. 재입고·판매 종료 여부 미확인")
