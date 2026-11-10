"""Worten·Media Expert·RTV 공용. 10월 pl_pt_common.py에서 사전 값만 인자로 뺐다."""
import json
import re


def norm_brand(b):
    return re.sub(r'\s+', ' ', b.strip()).upper()


def ld_products(h):
    out = []
    for m in re.finditer(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        items = d if isinstance(d, list) else [d]
        for it in items:
            if not isinstance(it, dict):
                continue
            for o in (it.get('@graph') or [it]):
                if isinstance(o, dict) and o.get('@type') == 'Product':
                    out.append(o)
    return out


def ld_brand(p):
    b = p.get('brand')
    if isinstance(b, dict):
        b = b.get('name')
    if isinstance(b, list) and b:
        b = b[0].get('name') if isinstance(b[0], dict) else b[0]
    return norm_brand(b) if isinstance(b, str) and b.strip() else ''


UNITS = ['kg', 'cm', 'mm', 'obr/min', 'obr', 'rpm', 'kwh', 'min', 'litr', 'db', 'hz', 'ghz', 'wat', 'w', 'l', 't', 'v', 'x', 'dni', 'rok', 'lat', 'pcs', 'szt', 'gb', 'mb', 'bar', 'm', 'a', 'pc']


UNIT_RE = re.compile('|'.join(sorted(map(re.escape, UNITS), key=len, reverse=True)))


def is_unit_like(t):
    s = UNIT_RE.sub('', t.lower())
    s = re.sub(r'[\d.,/+\-_()°*:]', '', s)
    return s == ''


def tokens(text):
    out = []
    for t in re.split(r'[\s,;()\[\]=]+', text):
        t = t.strip(".,;:!?\"'*°")
        if t:
            out.append(t)
    return out


def is_model_token(t):
    if len(t) < 5:
        return False
    if not (re.search(r'\d', t) and re.search(r'[A-Za-z]', t)):
        return False
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9\-/._]*[A-Za-z0-9]', t):
        return False
    if is_unit_like(t):
        return False
    if re.fullmatch(r'\d+(?:[.,]\d+)?[A-Za-z]{1,4}', t):   # 60cm, 1400T 같은 숫자+짧은 단위
        return False
    if re.fullmatch(r'\d+/\d+[A-Za-z]*', t):
        return False
    if re.fullmatch(r'(?i)(?:\d+x\d+.*|a\+*\d*|\d+w|wi-?fi\d*|usb.*|\d+(?:[.,]\d+)?(?:kg|cm|l|w|t|obr|rpm|min)+)', t):
        return False
    return True


def best_token(text):
    c = [t for t in tokens(text) if is_model_token(t)]
    if not c:
        return ''
    return max(c, key=len)   # 길이가 같으면 먼저 나온 것


def name_model(name, cut_paren=False):
    """상품명에서 모델 번호 추정. 세트('A + B')면 앞의 두 부분에서 각각 하나씩."""
    if cut_paren:
        name = name.split('(')[0]
    parts = re.split(r'\s\+\s', name)
    if len(parts) > 1:
        found = []
        for p in parts:
            t = best_token(p)
            if t and t.upper() not in [f.upper() for f in found]:
                found.append(t)
        if len(found) >= 2:
            return ' + '.join(x.upper() for x in found[:2])
        if found:
            return found[0].upper()
        return ''
    return best_token(name).upper()


def build_brand_matcher(extra, generic, drop, keep_if_upper):
    names = set(norm_brand(b) for b in list(generic) + list(extra) if b)
    names = {n for n in names if n and n not in ('S/MARCA',)}
    pats = []
    for n in sorted(names, key=lambda n: (-len(n), n)):
        pats.append((n, re.compile(r'(?<![\w&])' + re.escape(n).replace(r'\ ', r'[\s\-]') + r'(?![\w&])', re.I)))
    def find(name):
        best = None
        for n, p in pats:
            for m in p.finditer(name):
                if n in keep_if_upper or n in drop:
                    if m.group(0) != m.group(0).upper():
                        continue
                if best is None or m.start() < best[0]:
                    best = (m.start(), n)
                break
        return best[1] if best else ''
    return find


def clean_ld_model(m):
    """JSON-LD model 정리: 'RB38C607AB1 EF' 처럼 짧은 꼬리는 유지, 'SBS HCKR7819DWGB' 같은 설명 단어가 섞이면 모델 토큰만 남김."""
    c = re.sub(r'\s+', ' ', m.strip()).upper()
    w = c.split(' ')
    if len(w) == 1:
        return c
    if len(w) == 2 and re.fullmatch(r'[A-Z]{2}', w[1]) and is_model_token(w[0]):
        return c
    t = best_token(c)
    return t.upper() if t else c
