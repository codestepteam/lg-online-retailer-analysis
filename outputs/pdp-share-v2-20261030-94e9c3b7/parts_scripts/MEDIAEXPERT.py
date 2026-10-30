# Poland_MEDIAEXPERT: JSON-LD Product.brand / Product.model 우선, 없으면 상품명
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pl_pt_common import *
F = 'Poland_MEDIAEXPERT.csv'
rows = read_rows(F)
EXTRA = ['HUMANAS','DREAME','LAIFEN','INOLY','MANTA','UWANT','NICEBOY','BEAUTIFLY','MOVA','SKINVIBE','AENO','RAVANSON','VESTFROST','ELECTRO-LINE','LUMINEO','LAFE','ELITEHOFF','KINGHOFF','LEIFHEIT','VILEDA','SAM COOK','GÖTZE','TROSKOMANIA','BIZON']
find0 = build_brand_matcher(EXTRA)
STOP = {'LED','USB','XXL','XL','NFC','LCD','PRO','MAX','MINI','AGD','PLUS','ECO','SET','TURBO','INOX','IONIC','AIR','SMART','DIGITAL','TOUCH','NEW','NO','FROST','PL','EU'}
UP = r'[A-ZĄĆĘŁŃÓŚŹŻÜÖ]'
def find(name):
    b = find0(name)
    if b: return b
    for t in tokens(name)[1:6]:
        if re.fullmatch(UP + r'[A-ZĄĆĘŁŃÓŚŹŻÜÖ&\-]{2,}', t) and t not in STOP:
            return t
    return ''
out = []
for r in rows:
    b = c = ''; bs = cs = '없음'
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
