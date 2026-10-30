# Portugal_Worten: 페이지 JSON-LD brand(S/MARCA는 무시). 모델은 JSON-LD에 없고 사양표('Referência' 값)가 있는 극소수 페이지만 사용,
# 나머지는 상품명에서 '(' 앞 부분의 모델 토큰(페이지가 있으면 페이지 본문에도 있을 때만).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pl_pt_common import *
F = 'Portugal_Worten.csv'
rows = read_rows(F)
EXTRA = ['LURELIA','AQUAFORGE','EVVO','BECKEN','KUNFT','BELTAX','VOX','INFINITON','RECAMANIA','HOMA','TELEFUNKEN','NEWSTAR','TAURUS','ORBEGOZO','COMFEE','CLATRONIC','ELECTRO LINE','LORENZ','STRONG','HYUNDAI','CORBERO','OCEANIC','ENVIRO','FRAMEC','MILECTRIC']
find = build_brand_matcher(EXTRA)
out = []
for r in rows:
    b = c = ''; bs = cs = '없음'
    name = r['상품명']
    h = ''
    if r['HTML경로']:
        h = read_html(r['HTML경로'])
        ps = ld_products(h)
        if ps:
            b = ld_brand(ps[0])
            if b in ('S/MARCA', 'SEM MARCA'): b = ''
        if b: bs = '페이지'
        m = re.search(r'Especificações.{0,40}?Marca.{0,80}?Referência([A-Za-z0-9][A-Za-z0-9\-/._]{3,29}?)EAN', h)
        if m and is_model_token(m.group(1)):
            c, cs = m.group(1).upper(), '페이지'
    if not b:
        b = find(name)
        bs = '상품명' if b else '없음'
    if not c:
        t = name_model(name, cut_paren=True)
        if t and (not h or all(x.lower() in h.lower() for x in t.split(' + '))):
            c, cs = t, '상품명'
    out.append([r['행번호'], r['확인 요청 URL'], b, c, bs, cs])
write_part(F, out)
report(rows, out)
