import re
from urllib.parse import urlparse
# 단위·수치 표기(12KG, 1400RPM, 12/8KG, 635L, 1400OBR/MIN, 60X85CM)는 제품코드가 아니다
UNIT = re.compile(r'^\d+([.,/X-]\d+)*[A-Z]{0,7}(/[A-Z]{1,4})?\+?$')
def cands(text, split_hyphen=False):
    out = []
    for t in re.split(r'[\s,;:()\[\]{}|"“”«»+™®¿!?_]+' + (r'|-' if split_hyphen else ''), text):
        t = t.strip('.-/*').upper()
        if len(t) < 5 or not re.fullmatch(r'[A-Z0-9][A-Z0-9\-/.]*[A-Z0-9]', t): continue
        if sum(ch.isdigit() for ch in t) < 1 or sum(ch.isalpha() for ch in t) < 2: continue
        if UNIT.match(t) or re.fullmatch(r'\d+[A-Z]*[-/]\d+[A-Z]*', t): continue
        out.append(t)
    return out
def pick(c):
    # 숫자 2개 이상인 첫 후보(묶음 상품은 앞쪽이 본 상품). 없으면 첫 후보
    return next((t for t in c if sum(ch.isdigit() for ch in t) >= 2), c[0])
def model_code(name, url):
    c = cands(name)
    if c: return pick(c), '상품명에서 추출(추정)'
    path = re.sub(r'\.(b?html?|aspx?|php)$', '', urlparse(url).path, flags=re.I)
    c = [x for x in cands(path.replace('/', ' '), split_hyphen=True) if not re.fullmatch(r'[A-Z]{0,4}\d{5,}', x)]
    if c: return pick(c), '주소에서 추출(추정)'
    return '', ''
