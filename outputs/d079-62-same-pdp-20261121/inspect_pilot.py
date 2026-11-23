"""Audit saved trial pages. A trial observation does not assign a final pair verdict."""

import json
import re
from pathlib import Path

from lxml import html
from PIL import Image


OUT = Path(__file__).resolve().parent
RAW = OUT / "raw"


def text(node):
    return node.text_content().strip()


def texts(doc, path):
    return [text(e) for e in doc.xpath(path)]


def payloads(doc):
    parts = []
    for content in doc.xpath("//script/text()"):
        if content.startswith("self.__next_f.push("):
            args = json.loads(content[content.index("(") + 1:content.rindex(")")])
            if len(args) == 2 and isinstance(args[1], str):
                parts.append(args[1])
    return "".join(parts)


def source_objects(stream, key):
    decoder = json.JSONDecoder()
    return [decoder.raw_decode(stream[m.end():])[0] for m in re.finditer(re.escape(f'"{key}":') + r'(?=[\[{])', stream)]


def costco(doc):
    stream = payloads(doc)
    identifier = texts(doc, '//*[@id="productDescriptionDesktop"]//*[@data-testid="Text_item-number"]')
    product = json.loads(doc.xpath('string(//script[@id="ProductSchema"])'))
    crumbs = json.loads(doc.xpath('string(//script[@id="BreadcrumbListSchema"])'))
    details = doc.xpath('//*[@aria-labelledby="product_details"]')[0]
    title_area = '//*[@id="productDescriptionDesktop"]'
    specs = [texts(tr, './th|./td') for tr in doc.xpath('//*[@id="ProductSpecifications"]//tr')]
    selectors = doc.xpath('//*[@id="product-data-card-right-column"]//*[starts-with(@data-testid,"variants-accordion")]')
    selection = [[text(e), e.xpath('.//button/@aria-label')] for e in selectors]
    media = source_objects(stream, "brandfolderAsset")
    # The UI can hold other products' galleries. Match assets to the displayed gallery.
    visible_ids = set(doc.xpath('//*[@data-testid="image-carousel"]//img/@id'))
    candidates = [assets for assets in media if any(a.get('id') in visible_ids for a in assets)]
    file_lists = []
    for assets in candidates:
        files = [(a.get('customFields', {}).get('Asset Type'), a.get('attributes', {}).get('cdn_url'),
                  [v.get('attributes', {}).get('url') for v in a.get('attachments', {}).get('data', [])])
                 for a in assets]
        if files not in file_lists:
            file_lists.append(files)
    for e in details.xpath('.//script|.//style|.//button|.//noscript'):
        e.drop_tree()
    description = text(details)
    pictures = [e.get('src') for e in details.xpath('.//img')]
    data_sources = source_objects(stream, "productDetailsData")
    selected_product = [j['productData']['id'] for j in data_sources if j.get('productData', {}).get('itemType') == 'Product']
    return {
        "사이트 상품 번호 후보": list(dict.fromkeys(selected_product)),
        "화면 품목 번호와 모델": identifier,
        "대표 주소": doc.xpath('//link[@rel="canonical"]/@href'),
        "브랜드": product.get('brand'),
        "상품명": texts(doc, title_area + '//h1'),
        "갤러리 자료": file_lists,
        "갤러리 영상 버튼": doc.xpath('//*[@data-testid="image-carousel"]//button[contains(@aria-label,"Video")]/@aria-label'),
        "핵심 특징": texts(doc, '//*[@data-testid="features-list"]//*[starts-with(@data-testid,"Text_feature-")]'),
        "상세 설명": description, "상세 설명 그림": pictures,
        "사양표": specs,
        "상단 평점과 리뷰": doc.xpath(title_area + '//button[starts-with(@aria-label,"average rating") or starts-with(@aria-label,"Read ")]/@aria-label'),
        "본품 표시 가격": texts(doc, '//*[@data-testid="pricing-card"]//*[@data-testid="Text_single-price-whole-value"]'),
        "판매자": None,
        "배송지 구매 상태": texts(doc, '//*[@data-testid="Text_zipcode-status"]'),
        "선택 옵션 후보": selection,
        "카테고리 경로": [v["name"] for v in crumbs["itemListElement"]],
        "배송 우편번호": texts(doc, '//*[@data-testid="Button_zipcodeSelector"]'),
    }


def inspect():
    manifest = json.loads((RAW / "selection.json").read_text())
    rows = []
    for pair in (p for p in manifest["pairs"] if p["pilot"]):
        for source in pair["rows"]:
            row_id = source["행번호"]
            for meta_file in sorted(RAW.glob(f"iab-*-{row_id}.json")):
                meta = json.loads(meta_file.read_text())
                assert meta["row"] == row_id and meta["url"] == source["접속 후 URL"]
                stem = meta_file.stem
                top = html.fromstring((RAW / f"{stem}.html").read_text())
                blocked = "su acceso ha sido bloqueado" in top.text_content().lower()
                shot = OUT / "screenshots" / (f"{stem}.jpg" if blocked else f"{stem}-product.jpg")
                with Image.open(shot) as picture:
                    picture.verify()
                meta.update({"pair": pair["pair"], "blocked": blocked, "screenshot": shot.name})
                if not blocked:
                    detail = html.fromstring((RAW / f"{stem}-detail.html").read_text())
                    meta["observations"] = costco(detail)
                rows.append(meta)
    assert len({r["row"] for r in rows}) == 12
    path = RAW / "iab-pilot-observations.json"
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"{len(rows)} captures, {sum(r['blocked'] for r in rows)} blocked, {len(rows)} readable image files")
    return rows


if __name__ == "__main__":
    inspect()
