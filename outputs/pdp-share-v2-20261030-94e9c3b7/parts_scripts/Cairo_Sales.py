import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mix_common import *
O = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = 'Egypt_Cairo_Sales'

# 아랍어 표기 -> 영문 브랜드 (같은 브랜드의 철자 변형 포함)
AR = {
    'ال جى': 'LG', 'ال جي': 'LG', 'إل جي': 'LG', 'ال جى': 'LG',
    'سامسونج': 'SAMSUNG', 'سامسونغ': 'SAMSUNG', 'توشيبا': 'TOSHIBA', 'شارب': 'SHARP', 'زانوسى': 'ZANUSSI',
    'زانوسي': 'ZANUSSI', 'بيكو': 'BEKO', 'وايت بوينت': 'WHITE POINT', 'وايت ويل': 'WHITE WHALE',
    'تورنيدو': 'TORNADO', 'فريش': 'FRESH', 'هوفر': 'HOOVER', 'يونيون اير': 'UNIONAIRE', 'يونيون إير': 'UNIONAIRE',
    'يونيون أير': 'UNIONAIRE', 'يونيون تك': 'UNION TECH', 'هاير': 'HAIER', 'اريستون': 'ARISTON', 'أريستون': 'ARISTON',
    'جورينيا': 'GORENJE', 'جورنيا': 'GORENJE', 'اوشن': 'OCEAN', 'أوشن': 'OCEAN', 'وايرلبول': 'WHIRLPOOL',
    'ويرلبول': 'WHIRLPOOL', 'سميج': 'SMEG', 'كاندي': 'CANDY', 'ميديا': 'MIDEA', 'بوش': 'BOSCH',
    'كريازى': 'KIRIAZI', 'كريازي': 'KIRIAZI', 'هامبورج': 'HAMBURG', 'هايسنس': 'HISENSE', 'ميلا': 'MIELE',
    'مابي': 'MABE', 'ال جي': 'LG', 'الكتروستار': 'ELECTROSTAR', 'ايديال': 'IDEAL', 'سيمنس': 'SIEMENS',
    'اريستون': 'ARISTON', 'هيتاشي': 'HITACHI', 'باناسونيك': 'PANASONIC', 'اي جي': 'AEG', 'ايه إي جي': 'AEG',
    'هيتاشي': 'HITACHI', 'هيتاشى': 'HITACHI', 'انديست': 'INDESIT', 'كلفنيتور': 'KELVINATOR', 'كلفينيتور': 'KELVINATOR',
    'باساب': 'PASSAP', 'بنجوين': 'PENGUIN', 'فاجور': 'FAGOR', 'هيونداي': 'HYUNDAI', 'تورنادو': 'TORNADO',
    'جورينيه': 'GORENJE', 'فرانكي': 'FRANKE', 'بيرغهوف': 'BERGHOFF', 'سوكاني': 'SOKANY', 'يونيون اير': 'UNIONAIRE',
    'ديهولد': 'DAEWOO', 'دايو': 'DAEWOO', 'ديوو': 'DAEWOO', 'كونتننتال': 'CONTINENTAL',
}


def page_info(h):
    """(브랜드, 사양표 모델 칸, 'الموديل' 상품 참조번호)"""
    b = tb = rf = ''
    x = re.search(r'itemprop="brand"[^>]*>\s*<meta itemprop="name" content="([^"]*)"', h)
    if x: b = norm_brand(x.group(1))
    x = re.search(r'<td>\s*(?:الموديل|موديل)\s*</td>\s*<td>([^<]*)</td>', h)
    if x: tb = clean(x.group(1)).upper()
    if tb and tb.count('(') != tb.count(')'):
        tb = ''  # 괄호가 깨진 값은 버림
    x = re.search(r'<p id="product_reference">.*?<span[^>]*content="([^"]*)"', h, re.S)
    if x: rf = clean(x.group(1)).upper()
    return b, tb, rf


def N(s):
    return re.sub(r'[^A-Z0-9]', '', s.upper())


def page_code(h, name, tb, rf):
    tt = pick_code(name, h)
    if tb and rf and N(tb) != N(rf) and tt and N(tt) == N(rf):
        return tt  # 사양표 값이 짧게/다르게 적힌 경우: 제목·참조번호가 일치하는 쪽
    if tb:
        return tb
    return tt if (tt and (not rf or N(tt) == N(rf))) else rf


def main():
    inp = rd(f'{O}/inputs/{NAME}.csv')
    pages, brands = {}, set()
    for r in inp:
        h = load(r['HTML경로'])
        if h:
            bb, tb, rf = page_info(h)
            pages[r['행번호']] = (h, bb, page_code(h, r['상품명'], tb, rf))
            if pages[r['행번호']][1]: brands.add(pages[r['행번호']][1])
    print('page brands', sorted(brands))
    rows = []
    for r in inp:
        name = r['상품명']; p = pages.get(r['행번호'])
        b = c = ''; bs = cs = '없음'
        if p:
            if p[1]: b, bs = p[1], '페이지'
            if p[2]: c, cs = p[2], '페이지'
        if not b:
            b = brand_from_text(name, brands, AR)
            if b: bs = '상품명'
        if not c:
            trunc = name.rstrip().endswith(('...', '…'))  # 제목이 잘렸으면 끝 토큰은 믿지 않음
            nm = name.rstrip().rstrip('.…').rstrip()
            c = pick_code(nm, p[0] if p else None) or spaced_tail(nm, p[0] if p else None)
            if trunc and c and nm.upper().endswith(c.split(' + ')[-1].split(' ')[-1]):
                c = ''
            if c: cs = '상품명'
        rows.append([r['행번호'], r['확인 요청 URL'], b, c, bs, cs])
    write(f'{O}/parts/{NAME}.csv', rows)
    report(inp, rows)


main()
