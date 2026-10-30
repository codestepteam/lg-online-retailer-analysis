# Poland_RTV_EURO_AGD: JSON-LD Product.model 우선(전 행 존재), 브랜드는 페이지에 brand가 있으면 사용, 없으면 상품명
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pl_pt_common as common
from pl_pt_common import *
F = 'Poland_RTV_EURO_AGD.csv'
rows = read_rows(F)
common.KEEP_IF_UPPER.clear(); common.DROP.clear()   # RTV는 브랜드를 'Samsung'처럼 첫 글자만 대문자로 적음
EXTRA = ['TROSKOMANIA','BIZON','DREAME','LAIFEN','XIAOMI','CONCEPT','ELDOM','BRABANTIA','LEIFHEIT','VILEDA','ARTWEGER','VESTFROST','KINGHOFF','ZELMER','MAESTRO','GOCKOWIAK','HUMANAS','NICEBOY','UWANT','TEESA','LUND','SHARK','WEBBER','BEAUTYME','ELITEHOFF','RAVANSON','AENO']
find0 = build_brand_matcher(EXTRA)
STOP_WORDS = set("""lodówka pralka suszarka pralko-suszarka suszarko-lokówka zamrażarka kostkarka chłodziarka lokówka piekarnik zmywarka zestaw łącznik mata wirówka ociekacz szafa
środek kule wąż torba podkładki zapach pojemnik pojemniki kruszarka półka syfon proszek żel płyn wkłady pełny pelny pełen funkcje komora szuflada elektryczna mocna duża składany kosz tabletki odkurzacz urządzenie listki do na pod dla""".split())
def find(name):
    b = find0(name)
    if b: return b
    for t in tokens(name)[:6]:
        if t.lower() in STOP_WORDS: continue
        if re.fullmatch(r'[A-ZĄĆĘŁŃÓŚŹŻÜÖ][A-Za-ząćęłńóśźżüö&\-]{2,}', t) and not re.search(r'\d', t):
            return t.upper()
    return ''
out = []
for r in rows:
    b = c = ''; bs = cs = '없음'
    h = ''
    if r['HTML경로']:
        h = read_html(r['HTML경로'])
        ps = ld_products(h)
        if ps:
            p = ps[0]
            b = ld_brand(p)
            m = p.get('model')
            if isinstance(m, str) and m.strip():
                c = clean_ld_model(m)
        if b: bs = '페이지'
        if c:
            cs = '페이지'
        else:
            t = name_model(r['상품명'])
            if t and t.split(' + ')[0].lower() in h.lower():
                c, cs = t, '상품명'
    if not b:
        b = find(r['상품명'])
        bs = '상품명' if b else '없음'
    if not c and not r['HTML경로']:
        c = name_model(r['상품명'])
        cs = '상품명' if c else '없음'
    out.append([r['행번호'], r['확인 요청 URL'], b, c, bs, cs])
write_part(F, out)
report(rows, out)
