"""검색 리테일러별 브랜드·제품코드 추출. 판단 순서는 10월 parts_scripts 그대로이고, 사전 값은 product_codes.json에서 받는다.

각 함수는 (행 목록, read, words)를 받아 {행번호: (브랜드, 제품코드, 브랜드 찾은곳, 제품코드 찾은곳)}을 돌려준다.
read(행)은 그 행의 저장 HTML 글자, 페이지가 없으면 None이다. 페이지에서 나온 브랜드를 리테일러 전체의 사전으로 쓰므로 한 곳의 행을 한꺼번에 받는다.
"""
import html as H
import json
import re
import urllib.parse

from . import cz, mix, pl_pt, title_tokens

PAGE, NAME, URL, NOTHING = "페이지", "상품명", "URL", "없음"


def read_all(rows, read):
    return {row["행번호"]: html for row in rows if (html := read(row)) is not None}


def result(brand, code, brand_from, code_from):
    return brand, code, brand_from or NOTHING, code_from or NOTHING


def alza(rows, read, words):
    shared, pages, brands, out = words["cz"], read_all(rows, read), set(), {}
    for h in pages.values():
        if h:
            m = re.search(r'"brand":\{"@type":"Brand","name":"([^"]+)"', h)
            if m:
                brands.add(m.group(1).upper())
    for r in rows:
        name, h = r["상품명"], pages.get(r["행번호"])
        b = bf = p = pf = ""
        if h:
            m = re.search(r'"brand":\{"@type":"Brand","name":"([^"]+)"', h)
            if m:
                b, bf = H.unescape(m.group(1)).strip().upper(), PAGE
            m = re.search(r'"mpn":"([^"]*)"', h)
            mpn = H.unescape(m.group(1)).strip().upper() if m else ""
            toks = cz.tokens(name, shared["stop"])
            sc = cz.set_code(name, shared, h.upper())
            if sc:
                p, pf = sc, NAME
            elif mpn and not re.fullmatch(r"\d+", mpn):
                base = mpn.split(".")[0] if (b == "LG" and "." in mpn) else mpn  # LG: 'GBBS322APY.APYQEUZ' → 상품명과 같은 앞부분
                p, pf = base, PAGE
            else:
                c = [t for t in toks if t in h.upper()]  # mpn이 없거나 숫자뿐이면 상품명 단어 중 페이지에 있는 것
                if c:
                    p, pf = max(c, key=len), NAME
        if not b:
            b = cz.brand_from_name(name, brands, shared["generic"])
            bf = NAME if b else NOTHING
        if not p and not h:
            t = cz.set_code(name, shared, strict=True) or cz.clean_tokens(name, shared)
            if t:
                p, pf = t, NAME
        out[r["행번호"]] = result(b, p, bf, pf)
    return out


def datart_brand(h):
    m = re.search(r'"@type":\s*"Brand",\s*"name":\s*"([^"]+)"', h) or re.search(r"item_brand&quot;:\s*&quot;([^&]+)&quot;", h) or re.search(r'"brand":\s*"([^"]+)"', h)
    return H.unescape(m.group(1)).strip().upper() if m else ""


def datart(rows, read, words):
    shared, pages, brands, out = words["cz"], read_all(rows, read), set(), {}
    for h in pages.values():
        if h and (b := datart_brand(h)):
            brands.add(b)
    for r in rows:
        name, h = r["상품명"], pages.get(r["행번호"])
        b = bf = p = pf = ""
        if h:
            b = datart_brand(h)
            if b:
                bf = PAGE
            hu = h.upper()
            ms = re.search(r'"sku":\s*"([^"]+)"', h)
            sku = ms.group(1).upper() if ms else ""
            sc = cz.set_code(name, shared, hu)
            toks = list(dict.fromkeys(cz.tokens(name, shared["stop"])))
            if sc:
                p, pf = sc, NAME
            else:
                c = [t for t in toks if t in hu]
                s = [t for t in c if sku.endswith(t.replace(" ", ""))]  # 매장 sku 끝부분과 맞는 후보가 가장 확실
                if s:
                    p, pf = max(s, key=len), NAME
                elif len(c) == 1:
                    p, pf = c[0], NAME
                elif c:
                    t = cz.clean_tokens(name, shared)
                    if t and t in hu:
                        p, pf = t, NAME
            if not p:  # 짧은 모델(4자)은 매장 sku 끝부분과 맞을 때만
                w = [x.upper() for x in re.findall(r"[A-Za-z0-9]{4,}", name) if re.search(r"\d", x) and re.search(r"[A-Za-z]", x) and sku.endswith(x.upper())]
                if w:
                    p, pf = max(w, key=len), NAME
        if not b:
            b = cz.brand_from_name(name, brands, shared["generic"])
            bf = NAME if b else NOTHING
        if not p and not h:
            t = cz.set_code(name, shared, strict=True) or cz.clean_tokens(name, shared)
            if t:
                p, pf = t, NAME
        out[r["행번호"]] = result(b, p, bf, pf)
    return out


def matcher(words, keep_case_rules=True):
    shared = words["pl_pt"]
    return pl_pt.build_brand_matcher(words["extra"], shared["generic"], shared["drop"] if keep_case_rules else (), shared["keep_if_upper"] if keep_case_rules else ())


def worten(rows, read, words):
    find, out = matcher(words), {}
    for r in rows:
        b = c = ""
        bs = cs = NOTHING
        name, h = r["상품명"], read(r) or ""
        if h:
            ps = pl_pt.ld_products(h)
            if ps:
                b = pl_pt.ld_brand(ps[0])
                if b in ("S/MARCA", "SEM MARCA"):
                    b = ""
            if b:
                bs = PAGE
            m = re.search(r"Especificações.{0,40}?Marca.{0,80}?Referência([A-Za-z0-9][A-Za-z0-9\-/._]{3,29}?)EAN", h)
            if m and pl_pt.is_model_token(m.group(1)):
                c, cs = m.group(1).upper(), PAGE
        if not b:
            b = find(name)
            bs = NAME if b else NOTHING
        if not c:
            t = pl_pt.name_model(name, cut_paren=True)
            if t and (not h or all(x.lower() in h.lower() for x in t.split(" + "))):
                c, cs = t, NAME
        out[r["행번호"]] = (b, c, bs, cs)
    return out


def polish_page_values(r, h, name):
    """Media Expert·RTV 공통: JSON-LD 브랜드·모델, 없으면 페이지에 있는 상품명 단어."""
    b = c = ""
    bs = cs = NOTHING
    ps = pl_pt.ld_products(h)
    if ps:
        b = pl_pt.ld_brand(ps[0])
        m = ps[0].get("model")
        if isinstance(m, str) and m.strip():
            c = pl_pt.clean_ld_model(m)
    if b:
        bs = PAGE
    if c:
        cs = PAGE
    else:
        t = pl_pt.name_model(name)
        if t and t.split(" + ")[0].lower() in h.lower():
            c, cs = t, NAME
    return b, c, bs, cs


def polish_rows(rows, read, find):
    out = {}
    for r in rows:
        b = c = ""
        bs = cs = NOTHING
        name, h = r["상품명"], read(r)
        if h is not None:
            b, c, bs, cs = polish_page_values(r, h, name)
        if not b:
            b = find(name)
            bs = NAME if b else NOTHING
        if not c and h is None:
            c = pl_pt.name_model(name)
            cs = NAME if c else NOTHING
        out[r["행번호"]] = (b, c, bs, cs)
    return out


def rtv_euro_agd(rows, read, words):
    find0, stop = matcher(words, keep_case_rules=False), set(words["first_word_stop"])  # RTV는 브랜드를 'Samsung'처럼 첫 글자만 대문자로 적는다

    def find(name):
        b = find0(name)
        if b:
            return b
        for t in pl_pt.tokens(name)[:6]:
            if t.lower() in stop:
                continue
            if re.fullmatch(r"[A-ZĄĆĘŁŃÓŚŹŻÜÖ][A-Za-ząćęłńóśźżüö&\-]{2,}", t) and not re.search(r"\d", t):
                return t.upper()
        return ""

    return polish_rows(rows, read, find)


def media_expert(rows, read, words):
    find0, stop = matcher(words), set(words["upper_word_stop"])

    def find(name):
        b = find0(name)
        if b:
            return b
        for t in pl_pt.tokens(name)[1:6]:
            if re.fullmatch(r"[A-ZĄĆĘŁŃÓŚŹŻÜÖ][A-ZĄĆĘŁŃÓŚŹŻÜÖ&\-]{2,}", t) and t not in stop:
                return t
        return ""

    return polish_rows(rows, read, find)


def mix_rows(rows, pages, words, brands, code_of, alias=None):
    """페이지 값 → 상품명 사전 순서. pages[행번호] = (html, 브랜드, 코드)."""
    generic, out = words["mix"]["generic"], {}
    for r in rows:
        name, p = r["상품명"], pages.get(r["행번호"])
        b = c = ""
        bs = cs = NOTHING
        if p:
            if p[1]:
                b, bs = p[1], PAGE
            if p[2]:
                c, cs = p[2], PAGE
        if not b:
            b = mix.brand_from_text(name, brands, generic, alias)
            if b:
                bs = NAME
        if not c:
            c = code_of(name, p[0] if p else None)
            if c:
                cs = NAME
        out[r["행번호"]] = (b, c, bs, cs)
    return out


def sharaf_page(h):
    b = m = ""
    x = re.search(r'<meta property="brand" content="([^"]*)"', h) or re.search(r'var flixConfig = \{[^}]*?"brand":"([^"]*)"', h) or re.search(r'itemprop="brand"[^>]*>\s*<meta itemprop="name" content="([^"]*)"', h)
    if x:
        b = mix.norm_brand(x.group(1))
    x = re.search(r'<meta itemprop="mpn" content="([^"]*)"', h) or re.search(r'"mpn":"([^"]*)"', h)
    if x:
        m = mix.clean(x.group(1)).upper()
    return b, m


def tail_or_pick(stop):
    def code_of(name, page):
        return mix.tail_code(name, page) or mix.pick_code(name, stop, page) or mix.spaced_tail(name, page)
    return code_of


def sharaf(rows, read, words):
    pages, brands = {}, set()
    for number, h in read_all(rows, read).items():
        if h:
            b, model = sharaf_page(h)
            pages[number] = (h, b, re.sub(r"\s*\+\s*", " + ", model) if model and model not in ("NULL", "N/A", "-") else "")
            if b:
                brands.add(b)
    return mix_rows(rows, pages, words, brands | set(words["extra"]), tail_or_pick(words["mix"]["stop"]), words["alias"])


def appliance_online_page(h):
    """JSON-LD Product의 brand.name과 mpn 또는 sku(이 리테일러는 sku가 곧 제조사 모델)."""
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except ValueError:
            continue
        for x in d if isinstance(d, list) else [d]:
            if isinstance(x, dict) and x.get("@type") == "Product":
                b = x.get("brand")
                b = b.get("name") if isinstance(b, dict) else b
                return mix.norm_brand(b or ""), mix.clean(str(x.get("mpn") or x.get("sku") or "")).upper()
    return "", ""


def appliance_online(rows, read, words):
    pages, brands = {}, set()
    for number, h in read_all(rows, read).items():
        if h:
            pages[number] = (h, *appliance_online_page(h))
            if pages[number][1]:
                brands.add(pages[number][1])
    return mix_rows(rows, pages, words, brands | set(words["extra"]), tail_or_pick(words["mix"]["stop"]), words["alias"])


def falabella_page(h, bad_model):
    """상품 페이지면 (브랜드, 모델), 카테고리 목록 등 상품이 아니면 None."""
    x = re.search(r'"brandName":"([^"]*)"', h) or re.search(r'"brand":\{"@type":"Brand","name":"([^"]*)"\}', h)
    if not x:
        return None
    ms = re.findall(r'"name":"Modelo","value":"([^"]*)"', h)
    m = mix.clean(ms[0]).upper() if ms else ""
    return mix.norm_brand(x.group(1)), "" if m in bad_model else m


def url_slug(url):
    m = re.search(r"/product/\d+/([^/?]+)", url)
    return urllib.parse.unquote(m.group(1)).replace("-", " ") if m else ""


def falabella(rows, read, words):
    generic, stop, bad_model, pages, brands, out = words["mix"]["generic"], words["mix"]["stop"], set(words["bad_model"]), {}, set(words["extra"]), {}
    for number, h in read_all(rows, read).items():
        info = falabella_page(h, bad_model) if h else None
        if info is not None:
            pages[number] = (h, *info)
            if info[0]:
                brands.add(info[0])
    for r in rows:
        name, p = r["상품명"], pages.get(r["행번호"])
        b = c = ""
        bs = cs = NOTHING
        if p:
            if p[1]:
                b, bs = p[1], PAGE
            if p[2]:
                c, cs = p[2], PAGE
        if not b:
            b = mix.brand_from_text(name, brands, generic)
            if b:
                bs = NAME
        if not b:
            b = mix.brand_from_text(url_slug(r["URL"]), brands, generic)
            if b:
                bs = URL
        if not c:
            c = mix.pick_code(name, stop, p[0] if p else None)
            if c:
                cs = NAME
        out[r["행번호"]] = (b, c, bs, cs)
    return out


def cairo_page(h):
    """(브랜드, 사양표 모델 칸, 'الموديل'(모델) 상품 참조번호)."""
    b = tb = rf = ""
    x = re.search(r'itemprop="brand"[^>]*>\s*<meta itemprop="name" content="([^"]*)"', h)
    if x:
        b = mix.norm_brand(x.group(1))
    x = re.search(r"<td>\s*(?:الموديل|موديل)\s*</td>\s*<td>([^<]*)</td>", h)
    if x:
        tb = mix.clean(x.group(1)).upper()
    if tb and tb.count("(") != tb.count(")"):
        tb = ""  # 괄호가 깨진 값은 버린다
    x = re.search(r'<p id="product_reference">.*?<span[^>]*content="([^"]*)"', h, re.S)
    if x:
        rf = mix.clean(x.group(1)).upper()
    return b, tb, rf


def letters_digits(text):
    return re.sub(r"[^A-Z0-9]", "", text.upper())


def cairo_code(h, name, tb, rf, stop):
    tt = mix.pick_code(name, stop, h)
    if tb and rf and letters_digits(tb) != letters_digits(rf) and tt and letters_digits(tt) == letters_digits(rf):
        return tt  # 사양표 값이 짧게·다르게 적힌 경우 제목·참조번호가 맞는 쪽
    if tb:
        return tb
    return tt if (tt and (not rf or letters_digits(tt) == letters_digits(rf))) else rf


def cairo_sales(rows, read, words):
    stop, pages, brands = words["mix"]["stop"], {}, set()
    names = {row["행번호"]: row["상품명"] for row in rows}
    for number, h in read_all(rows, read).items():
        if h:
            b, tb, rf = cairo_page(h)
            pages[number] = (h, b, cairo_code(h, names[number], tb, rf, stop))
            if b:
                brands.add(b)

    def code_of(name, page):
        truncated = name.rstrip().endswith(("...", "…"))  # 제목이 잘렸으면 끝 단어는 믿지 않는다
        short = name.rstrip().rstrip(".…").rstrip()
        c = mix.pick_code(short, stop, page) or mix.spaced_tail(short, page)
        if truncated and c and short.upper().endswith(c.split(" + ")[-1].split(" ")[-1]):
            c = ""
        return c

    return mix_rows(rows, pages, words, brands, code_of, words["alias"])


def electroplanet_brand(h):
    m = re.search(r'<a class="manufacturer" href="[^"]*/marques/[^"]*">\s*([^<]*?)\s*</a>', h)
    return H.unescape(m.group(1)).strip().upper() if m else ""


def title_brand(title, brands):
    t = " " + re.sub(r"[^A-Z0-9À-Ý&]+", " ", title.upper()) + " "
    best = ("", -1)
    for b in sorted(brands):
        i = t.rfind(" " + b + " ")
        if i >= 0 and (i + len(b), len(b)) > (best[1], len(best[0])):
            best = (b, i + len(b))
    return best[0]


def title_words(title):
    return re.sub(r"[^A-Z0-9À-Ý& ]+", " ", title.upper()).split()


def electroplanet_title_brand(title, brands, known, alias):
    b = title_brand(title, brands)
    ws = title_words(title)
    if not b and len(ws) >= 2 and " ".join(ws[-2:]) == "A M":
        b = alias["A M"]  # 'A,M' = Arthur Martin 약어
    if not b and ws:
        last = ws[-1]
        if last in alias:
            b = last
        elif len(last) >= 3 and last.isalpha():  # 상품명 끝 단어가 잘린 경우
            c = [x for x in known if x.startswith(last) and x != last]
            if len(c) == 1:
                b = c[0]
    if b in alias:
        b = alias[b]
    elif b and b not in known:  # 끝이 잘린 표기(MOULINE, BEK 등)는 알려진 브랜드 하나로 이어지면 고친다
        c = [x for x in known if x.startswith(b) and x != b]
        if len(c) == 1:
            b = c[0]
    return b


def electroplanet_codes(title, h):
    """첫 번째 모델 모양 단어(또는 'A/B' 세트). 'X + Y'로 이어진 두 번째 상품도 허용."""
    found, ws = [], title.upper().split()
    for k, w in enumerate(ws):
        m = title_tokens.models_from_word(w)
        if m:
            found = list(dict.fromkeys(m))
            if k + 2 < len(ws) and ws[k + 1] == "+":
                found += [x for x in title_tokens.models_from_word(ws[k + 2]) if x not in found]
            break
    if h:
        found = [m for m in found if m.split("/")[0] in h.upper()]
    return " + ".join(found)


def electroplanet(rows, read, words):
    pages, brands = read_all(rows, read), set(words["generic"])
    for h in pages.values():
        b = electroplanet_brand(h)
        if b:
            brands.add(b)
        for x in re.findall(r'<span class="brand">([^<]+)</span>', h):
            brands.add(H.unescape(x).strip().upper())
    brands -= {"", *words["not_brands"]}  # 색·약어가 브랜드 칸에 섞인 것
    known, stop, last_counts = set(brands), set(words["last_word_stop"]), {}
    for r in rows:  # 사전에 없는 브랜드: 상품명 맨 끝 글자 단어가 3번 이상 반복되면 브랜드로 본다
        ws = title_words(r["상품명"])
        if ws and re.fullmatch(r"[A-Z]{3,}", ws[-1]) and ws[-1] not in stop:
            last_counts[ws[-1]] = last_counts.get(ws[-1], 0) + 1
    brands |= {word for word, count in last_counts.items() if count >= 3}
    out = {}
    for r in rows:
        h, title = pages.get(r["행번호"]), r["상품명"]
        brand = bsrc = ""
        if h:
            b = electroplanet_brand(h)
            if b:
                brand, bsrc = b, PAGE
        if not brand:
            b = electroplanet_title_brand(title, brands, known, words["alias"])
            if b:
                brand, bsrc = b, NAME
        code = electroplanet_codes(title, h)
        out[r["행번호"]] = result(brand, code, bsrc, NAME if code else "")
    return out


def mediamarkt_brand(h):
    m = re.search(r'"brand":\{"@type":"Brand","name":"([^"]*)"', h)
    return m.group(1).strip().upper() if m else ""


def mediamarkt_candidates(h, mpn_names):
    out = []
    for n in mpn_names:
        for v in re.findall(r'"name":"' + re.escape(n) + r'","type":null,"unit":null,"value":"([^"]*)"', h):
            v = v.replace("\\u002F", "/").replace("\\\\u002F", "/").strip()
            if v and v not in out:
                out.append(v)
    return out


def brand_from_title(title, brands):
    t = title.upper()
    for b in sorted(brands, key=lambda name: (-len(name), name)):
        if re.match(re.escape(b) + r"(?![A-Z0-9])", t):
            return b
    return ""


def mediamarkt(rows, read, words):
    shared, pages = words["mediamarkt"], read_all(rows, read)
    brands = set(shared["generic"]) | {b for h in pages.values() if (b := mediamarkt_brand(h))}
    out = {}
    for r in rows:
        h, title = pages.get(r["행번호"]), r["상품명"]
        brand = bsrc = code = csrc = ""
        if h is not None:
            b = mediamarkt_brand(h)
            if b:
                brand, bsrc = b, PAGE
        if not brand:
            b = brand_from_title(title, brands)
            if b:
                brand, bsrc = b, NAME
            else:  # 사전에 없는 브랜드: MediaMarkt 제목은 브랜드로 시작한다
                w = title.split()[0] if title.split() else ""
                if re.fullmatch(r"[A-ZÀ-Ý&]{3,}", w):
                    brand, bsrc = w, NAME
        brand = brand.rstrip(".") if brand else brand
        skip = len(brand.split()) if brand and brand_from_title(title, [brand, brand + "."]) else 0
        models = title_tokens.title_models(title, skip)
        models_ok = [m for m in models if h is None or m in h.upper()]
        if h is not None:
            joined = title_tokens.norm(title + " " + r["URL"].replace("-", ""))
            short = [title_tokens.norm(m) for m in models_ok]
            for candidate in mediamarkt_candidates(h, shared["mpn_names"]):
                value = title_tokens.norm(candidate)
                if value and (value in joined or any(value.startswith(t) and len(value) - len(t) <= 4 for t in short)):
                    code, csrc = candidate.upper(), PAGE
                    break
        if not code and models_ok:
            code, csrc = " + ".join(models_ok), NAME
        out[r["행번호"]] = result(brand, code, bsrc, csrc)
    return out
