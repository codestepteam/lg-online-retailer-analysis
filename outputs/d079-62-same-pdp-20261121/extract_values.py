"""raw/<작업 이름>.json.gz (브라우저가 저장한 페이지 원본을 압축한 것)에서 검사 항목 1~15의 값을 뽑는다.

- 값은 모두 저장된 원본에서만 읽는다. 사람이 적어 넣는 값은 없다.
- 글자 정리: 연속된 공백과 줄바꿈을 한 칸으로 줄이고 앞뒤 공백을 지운다. 그 밖의 글자는 바꾸지 않는다.
- 결과: extracted/<작업 이름>.json
"""

import copy
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

import lxml.html as LH

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
EXT = HERE / "extracted"

NONE = "없음"  # 그 페이지에 해당 값이 없을 때 적는 말

FIELDS = [
    # f01(페이지 원본의 상품 번호)은 값을 읽은 120행 모두 주소 끝 번호와 같아 판정과 엑셀에서 뺐다(11-21 사용자 결정). 값은 여전히 뽑아 extracted에 남는다.
    ("f02", "1. 화면에 보이는 제품 번호"),
    ("f03", "2. canonical"),
    ("f04", "3. 브랜드와 모델"),
    ("f05", "4. 상품명"),
    ("f06", "5. 갤러리"),
    ("f07", "6. Feature"),
    ("f08", "7. 상세 설명 본문"),
    ("f09", "8. 사양표"),
    ("f10", "9. 평점과 리뷰 수"),
    ("f11", "10. 표시 가격"),
    ("f12", "11. 판매자"),
    ("f13", "12. 구매 가능 상태"),
    ("f14", "13. 선택 옵션"),
    ("f15", "14. 카테고리 경로"),
]


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def clean(el):
    """글자만 읽기 위해 스크립트, 스타일, 아이콘 그림을 뺀 복사본을 만든다."""
    c = copy.deepcopy(el)
    for bad in c.xpath(".//script|.//style|.//noscript|.//template|.//svg"):
        bad.drop_tree()
    return c


def tc(el):
    """요소 안 글자를 그대로 이어 붙인다(한 줄 값용)."""
    return norm(clean(el).text_content()) if el is not None else ""


def tj(el):
    """요소 안 글자 조각 사이에 한 칸을 넣어 잇는다(여러 줄 본문용)."""
    if el is None:
        return ""
    return norm(" ".join(t for t in clean(el).itertext()))


def first(lst):
    return lst[0] if lst else None


def img_path(src):
    return (src or "").split("?")[0]


def imgs_of(el):
    """그림 목록. 늦게 뜨는 그림은 src 에 임시 그림이 들어 있으므로, 실제 경로가 적힌 속성(data-flixsrcset, data-src)을 먼저 읽는다."""
    out = []
    for im in el.xpath(".//img"):
        v = im.get("data-flixsrcset") or im.get("data-src") or im.get("src") or ""
        v = v.strip().split(" ")[0].split(",")[0]
        if v:
            out.append(img_path(v))
    return out


def frame_doc(src):
    f = RAW / "frames" / (hashlib.sha1(src.encode("utf-8")).hexdigest() + ".json")
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def frag(html):
    return LH.fromstring("<div>" + html + "</div>")


# ───────────────────────── Costco ─────────────────────────

def costco_product_data(html):
    chunks = re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)', html)
    rsc = "".join(json.loads(c) for c in chunks)
    key = '"productDetailsData":{"productData":{"id"'
    i = rsc.find(key)
    if i < 0:
        return None, rsc
    obj, _ = json.JSONDecoder().raw_decode(rsc[rsc.find("{", i + len('"productDetailsData":')):])
    return obj, rsc


def extract_costco(p):
    doc = LH.fromstring(p["html"])
    obj, rsc = costco_product_data(p["html"])
    pd = (obj or {}).get("productData") or {}
    v, extra = {}, {}

    h1 = first(doc.xpath("//h1"))
    card = first(doc.xpath('//*[@data-testid="product-description"]'))
    right = first(doc.xpath('//*[@id="product-data-card-right-column"]'))

    v["f01"] = pd.get("id") or NONE
    item_el = first(card.xpath('.//*[@data-testid="Text_item-number"]')) if card is not None else None
    item_text = tc(item_el)
    m = re.search(r"Item\s+(\S+)", item_text)
    v["f02"] = m.group(1) if m else NONE
    extra["화면의 품목 줄 원문"] = item_text or NONE
    v["f03"] = first(doc.xpath('//link[@rel="canonical"]/@href')) or NONE

    brand = NONE
    for s in doc.xpath('//script[@type="application/ld+json"][@id="ProductSchema"]/text()'):
        try:
            brand = (json.loads(s).get("brand") or {}).get("name") or NONE
        except Exception:
            pass
    m = re.search(r"Model\s+(.+)$", item_text)
    v["f04"] = f"브랜드: {brand} | 모델: {m.group(1).strip() if m else NONE}"
    v["f05"] = tc(h1) or NONE

    # 6 갤러리: 미리보기 단추(순서대로)에 걸린 원본 사진 경로
    gal = first(doc.xpath('//*[@id="image-gallery"]'))
    photos, videos = [], 0
    if gal is not None:
        for b in gal.xpath('.//*[@data-testid="image-gallery-thumbnail"]'):
            src = first(b.xpath(".//img/@src"))
            label = b.get("aria-label") or ""
            if src:
                photos.append(img_path(src))
            if re.search(r"video", label, re.I) or (not src):
                videos += 1
        if not photos:  # 미리보기 단추가 없는 화면(사진 1장 등)은 큰 사진 칸에서 읽는다
            for b in gal.xpath('.//*[@data-testid="product-hero"]//*[@data-testid="media-container"]'):
                src = first(b.xpath(".//img/@src"))
                if src and img_path(src) not in photos:
                    photos.append(img_path(src))
        videos += len(gal.xpath(".//video|.//iframe"))
    v["f06"] = "\n".join(photos) + f"\n[영상 {videos}개]" if photos else NONE
    extra["f06_photos"] = len(photos)
    extra["f06_videos"] = videos

    feats = []
    fl = first(doc.xpath('//*[@data-testid="features-list"]'))
    if fl is not None:
        feats = [tc(e) for e in fl.xpath('.//*[starts-with(@data-testid,"Text_feature-")]')]
    v["f07"] = "\n".join(feats) if feats else NONE
    extra["f07_items"] = len(feats)

    # 8 상세 설명: Product Details 영역의 글 + 제조사 제공 영역(Syndigo, 별도 영역)의 글과 그림
    acc = first(doc.xpath('//*[@data-testid="Accordion_product_details"]'))
    texts, imgs = [], []
    if acc is not None:
        acc2 = copy.deepcopy(acc)
        for b in acc2.xpath(".//button"):  # 펼치기 단추(Product Details, View More 등)의 글자는 본문이 아니라서 뺀다
            b.drop_tree()
        texts.append(tj(acc2))
        imgs += imgs_of(acc)
    for s in p.get("shadows", []):
        if s["tag"].startswith("syndigo") and s["tag"] != "syndigo-svg-icon":
            f = frag(s["html"])
            t = tj(f)
            if t:
                texts.append(t)
            imgs += imgs_of(f)
            extra["f08_videos"] = extra.get("f08_videos", 0) + len(f.xpath(".//video|.//syndigo-video"))
    body = norm(" ".join(texts))
    v["f08"] = (body + "\n[본문 속 그림]\n" + "\n".join(imgs)) if (body or imgs) else NONE
    extra["f08_chars"] = len(body)
    extra["f08_imgs"] = len(imgs)
    extra["f08_has_syndigo"] = any(s["tag"] == "syndigo-powerpage" and len(s["html"]) > 0 for s in p.get("shadows", []))
    extra["f08_expects_syndigo"] = "expects_syndigo true" in p.get("notes", [])
    extra["f08_vendor"] = next((n.split(" ", 1)[1] if " " in n else "" for n in p.get("notes", []) if n.startswith("vendor")), None)
    extra["f08_flix_chars"] = next((int(n.split(" ")[1]) for n in p.get("notes", []) if n.startswith("flix ")), None)
    extra["consent_banner_hidden"] = any(n.startswith("hid ") for n in p.get("notes", []))

    rows = []
    for r in doc.xpath('//*[@id="ProductSpecifications"]//tr'):
        th, td = first(r.xpath("./th")), first(r.xpath("./td"))
        rows.append(f"{tj(th)}: {tj(td)}")
    v["f09"] = "\n".join(rows) if rows else NONE
    extra["f09_rows"] = len(rows)

    rating = count = None
    if card is not None:
        for b in card.xpath(".//*[@aria-label]"):
            a = b.get("aria-label")
            m = re.search(r"average rating value is ([\d.]+) of 5", a)
            if m and rating is None:
                rating = m.group(1)
            m = re.search(r"Read ([\d,]+) reviews?", a)
            if m and count is None:
                count = m.group(1)
    v["f10"] = f"평점 {rating} | 리뷰 {count}" if (rating or count) else NONE

    pc = first(doc.xpath('//*[@data-testid="pricing-card"]'))
    price = tc(first(pc.xpath('.//*[@data-testid="price"]'))) if pc is not None else ""
    v["f11"] = price or NONE
    extra["price_unavailable_notice"] = "unable to display the price" in p["html"]

    sold = NONE
    if right is not None:
        m = re.search(r"((?:Shipped and )?Sold by[^|]{0,80}|Vendu par[^|]{0,80})", tj(right))
        if m:
            sold = m.group(1)
    third = sorted(set(re.findall(r'"isThirdPartyIncluded":(\w+)', rsc)))
    v["f12"] = (f"화면의 판매자 표시: {sold} | 원본 데이터의 공급사 번호: {pd.get('vendorNumber')}-{pd.get('vendorNumberSuffix')}"
                f" | 원본 데이터의 외부 판매자 포함 표시: {','.join(third) or NONE}")
    extra["f12_screen"] = sold

    zip_el = first(doc.xpath('//*[@data-testid="fulfillment-zipCode-and-warehouse-selector"]'))
    status = tc(first(doc.xpath('//*[@data-testid="Text_zipcode-status"]')))
    ful = tj(first(doc.xpath('//*[@data-testid="fulfillmentMolecule"]')))
    add = first(doc.xpath('//*[@data-testid="add-to-cart"]'))
    add_btn = ""
    if add is not None:
        add_btn = " / ".join(tc(b) for b in add.xpath(".//button") if tc(b))
    oos = "Out of Stock" if (right is not None and re.search(r"Out of Stock", tj(right))) else ""
    v["f13"] = (f"배송지와 상태: {tj(zip_el) or NONE} | 상태: {status or NONE} | 받는 방법: {ful or NONE}"
                f" | 담기 단추: {add_btn or NONE}" + (f" | {oos}" if oos else ""))
    extra["postal"] = tj(first(doc.xpath('//*[@data-testid="locationselector_DeliveryLocationSelector"]')))

    children = [c.get("id") for c in pd.get("childCatalogData") or []]
    opt_dom = []
    if right is not None:
        for e in right.xpath('.//*[@role="radiogroup"]|.//select|.//*[contains(@data-testid,"watch")]|.//*[contains(@data-testid,"ariant")]'):
            t = tj(e)
            if t:
                opt_dom.append(t)
    v["f14"] = f"화면의 선택 항목: {' / '.join(opt_dom) or NONE} | 원본 데이터의 하위 품목: {', '.join(children) or NONE}"
    extra["f14_screen"] = " / ".join(opt_dom) or NONE

    bc = first(doc.xpath('//*[@data-testid="Breadcrumbs"]'))
    crumbs = [tc(a) for a in bc.xpath(".//a")] if bc is not None else []
    v["f15"] = " > ".join(crumbs) if crumbs else NONE

    extra["is_product_page"] = bool(h1 is not None and pd.get("id"))
    if not extra["is_product_page"]:
        extra["page_notice"] = tc(h1)
    return v, extra


# ───────────────────────── Falabella ─────────────────────────

def extract_falabella(p):
    doc = LH.fromstring(p["html"])
    v, extra = {}, {}
    nd_txt = first(doc.xpath('//script[@id="__NEXT_DATA__"]/text()'))
    pp = (json.loads(nd_txt)["props"]["pageProps"] if nd_txt else {}) or {}
    pd = pp.get("productData") or {}
    cur = pd.get("currentVariant")
    variants = pd.get("variants") or []
    var = next((x for x in variants if x.get("id") == cur), variants[0] if variants else {})
    h1 = first(doc.xpath("//h1"))

    v["f01"] = f"상품 번호: {pd.get('id') or NONE} | 현재 선택된 세부 상품 번호: {cur or NONE}" if pd else NONE
    codes = []
    for e in doc.iter():
        if isinstance(e.tag, str) and e.tag not in ("script", "style") and e.text and re.search(r"Código del producto|C[oó]d\. tienda", e.text):
            t = tj(e)
            if t not in codes:
                codes.append(t)
    v["f02"] = " | ".join(codes) if codes else NONE
    v["f03"] = first(doc.xpath('//link[@rel="canonical"]/@href')) or NONE

    brand = tc(first(doc.xpath('//*[@id="pdp-product-brand-link"]|//*[contains(@class,"pdp-basic-info__brand-link")]'))) or NONE
    specs = (pd.get("attributes") or {}).get("specifications") or []
    model = next((x.get("value") for x in specs if (x.get("name") or "").strip().lower() == "modelo"), NONE)
    v["f04"] = f"브랜드: {brand} | 원본 데이터의 브랜드: {pd.get('brandName') or NONE} | 모델: {model}"
    v["f05"] = tc(h1) or NONE

    medias = var.get("medias") or []
    photos = [m.get("url") for m in medias if m.get("mediaType") == "image"]
    vids = [m.get("url") for m in medias if m.get("mediaType") != "image"]
    v["f06"] = ("\n".join(f"{m.get('mediaType')}: {m.get('url')}" for m in medias)) if medias else NONE
    extra["f06_photos"], extra["f06_videos"] = len(photos), len(vids)

    top = (pd.get("attributes") or {}).get("topSpecifications") or []
    v["f07"] = "\n".join(f"{x.get('name')}: {x.get('value')}" for x in top) if top else NONE
    extra["f07_items"] = len(top)

    # 8 상세 설명: 원본 데이터의 설명 글 + 화면의 "Información adicional (추가 정보)" 영역 글과 그림 + 제조사 제공 영역
    texts, imgs = [], []
    ld = pd.get("longDescription") or ""
    if ld:
        f = frag(ld)
        texts.append(tj(f))
        imgs += [x for x in f.xpath(".//img/@src")]
        extra["f08_source_scripts"] = f.xpath(".//script/@src")
    for t in doc.xpath('//*[contains(@class,"accordion__title")]'):
        if tc(t) in ("Información adicional", "Información Adicional"):
            item = t
            for _ in range(4):
                item = item.getparent()
                if item is None or len(item.xpath('.//*[starts-with(@id,"accordion-panel")]')):
                    break
            if item is not None:
                for pnl in item.xpath('.//*[starts-with(@id,"accordion-panel")]')[:1]:
                    pnl2 = copy.deepcopy(pnl)
                    for fr in pnl2.xpath(".//iframe|.//button"):  # 별도 문서는 아래에서 따로 읽는다. 펼치기 단추 글자(Mostrar menos 등)는 본문이 아니라서 뺀다
                        fr.drop_tree()
                    texts.append(tj(pnl2))
                    imgs += [x for x in pnl2.xpath(".//img/@src")]
    for s in p.get("shadows", []):
        f = frag(s["html"])
        if tj(f) and not s["tag"].startswith(("next-", "modal")):
            extra.setdefault("shadow_tags", []).append(s["tag"])
    # 제조사가 제공한 설명은 별도 주소의 문서(iframe)로 들어온다. 수집 서비스 안에서는 이 문서가 열리지 않아,
    # 같은 문서 주소를 브라우저로 따로 열어 저장해 둔 것(raw2/frames/<주소의 sha1>.json)에서 글과 그림을 읽는다.
    frame_srcs, frame_read = [], []
    for fr in doc.xpath("//iframe"):
        src = fr.get("src") or ""
        if not re.search(r"indexado|omnitok|flixmedia", src + (fr.get("id") or "")):
            continue
        frame_srcs.append(src)
        fd = frame_doc(src)
        if fd is not None:
            f = LH.fromstring(fd["html"])
            body_el = first(f.xpath("//body"))
            texts.append(tj(body_el if body_el is not None else f))
            imgs += imgs_of(f)
            frame_read.append(True)
        else:
            frame_read.append(False)
    extra["f08_frames"] = frame_srcs
    extra["f08_frame_read"] = all(frame_read) if frame_srcs else None
    body = norm(" ".join(t for t in texts if t))
    v["f08"] = (body + "\n[제조사 설명 문서 주소]\n" + "\n".join(frame_srcs) + "\n[본문 속 그림]\n" + "\n".join(imgs)) if (body or imgs or frame_srcs) else NONE
    extra["f08_chars"], extra["f08_imgs"] = len(body), len(imgs)

    v["f09"] = "\n".join(f"{x.get('name')}: {x.get('value')}" for x in specs) if specs else NONE
    extra["f09_rows"] = len(specs)

    rr = pp.get("ratingAndReviewsSeo") or {}
    stars = first(doc.xpath('//*[@data-testid="rr-rating-stars"]'))
    screen_rating = tj(stars.getparent()) if stars is not None else NONE
    v["f10"] = (f"화면: {screen_rating or NONE} | 원본 데이터: 평점 {rr.get('ratingValue') or NONE}, 리뷰 {rr.get('reviewCount') or NONE}")

    prices = var.get("prices") or []
    kinds = {"internetPrice": "인터넷 가격", "normalPrice": "정상 가격", "cmrPrice": "CMR 카드 가격", "eventPrice": "행사 가격"}

    def one(x):
        t = x.get("type")
        return f"{kinds.get(t, t)}({t}){' 줄 그은 가격' if x.get('crossed') else ''}: {x.get('symbol') or ''}{' '.join(x.get('price') or [])}"
    v["f11"] = " | ".join(one(x) for x in prices) if prices else NONE

    sold = NONE
    lab = first(doc.xpath('//*[contains(@class,"seller-info__label")]'))
    name_el = first(doc.xpath('//*[@id="testId-SellerInfo-sellerName"]'))
    if lab is not None or name_el is not None:
        sold = norm(f"{tj(lab)} {tj(name_el)}")
    si = pd.get("sellerInfo") or {}
    v["f12"] = f"화면: {sold} | 원본 데이터: {si.get('sellerName') or NONE} ({si.get('sellerId') or NONE})"

    add = [tc(e) for e in doc.xpath('//*[@id="add-to-cart-button"]')] or [tc(e) for e in doc.xpath('//*[contains(@class,"add-to-cart-text")]')]
    yn = lambda b: "예" if b is True else "아니오" if b is False else NONE
    v["f13"] = (f"담기 단추: {' / '.join(add) or NONE} | 원본 데이터: 품절 {yn(pd.get('isOutOfStock'))}, 구매 가능 {yn(var.get('isPurchaseable'))}"
                f", 온라인 판매 {yn(var.get('isOnlineSellable'))}")

    def vline(x):
        a = x.get("attributes") or {}
        opts = {k: a.get(k) for k in ("colorName", "size", "colorCode") if a.get(k)}
        return f"{x.get('id')}: {x.get('name')}" + (f" {json.dumps(opts, ensure_ascii=False)}" if opts else "")
    v["f14"] = (f"세부 상품 {len(variants)}개\n" + "\n".join(vline(x) for x in variants)) if variants else NONE
    extra["f14_variants"] = len(variants)

    bc = first(doc.xpath('//*[@id="breadcrumb"]|//*[@data-testid="breadcrumbs"]'))
    crumbs = [tc(a) for a in bc.xpath(".//a")] if bc is not None else []
    crumbs = [c for c in crumbs if c]
    v["f15"] = " > ".join(crumbs) if crumbs else NONE

    extra["is_product_page"] = bool(h1 is not None and pd.get("id"))
    return v, extra


def extract(p):
    host = re.sub(r"^https?://([^/]+)/.*$", r"\1", p["final_url"])
    if host.endswith("costco.ca"):
        v, extra = extract_costco(p)
    else:
        v, extra = extract_falabella(p)
    for k in ["f01"] + [k for k, _ in FIELDS]:
        v[k] = v.get(k) or NONE
    meta = {k: p.get(k) for k in ("name", "requested_url", "final_url", "title", "http_status", "started_utc",
                                  "collected_utc", "viewport", "scroll_height", "notes")}
    return {"meta": meta, "values": v, "extra": extra}


if __name__ == "__main__":
    EXT.mkdir(exist_ok=True)
    names = sys.argv[1:] or sorted(f.name[:-8] for f in RAW.glob("*.json.gz") if not f.name.endswith(".response.json.gz"))
    for n in names:
        gz = RAW / f"{n}.json.gz"
        p = json.loads(gzip.open(gz, "rt", encoding="utf-8").read()) if gz.exists() else json.loads((HERE / "raw2" / f"{n}.json").read_text(encoding="utf-8"))
        out = extract(p)
        (EXT / f"{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("extracted", len(names))
