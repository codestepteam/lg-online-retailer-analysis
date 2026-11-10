"""ALZA·DATART 공용. 10월 cz_common.py에서 사전 값만 인자로 뺐다."""
import re


UNIT = re.compile(r'^\d+(KG|OBR|RPM|CM|L|T|W|KW|MM|HZ|V|LITR|LITRU|MIN|DB|BAR|M|G|ML|KWH|\"|L/MIN|X\d+)$', re.I)


def tokens(name, stop):
    out = []
    for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9\-/\.]*[A-Za-z0-9]", name):
        u = t.upper()
        if len(u) < 5 or u in stop: continue
        if not (re.search(r'[A-Z]', u) and re.search(r'\d', u)): continue
        if UNIT.match(u) or re.fullmatch(r'\d{3,5}[A-Z]?', u): continue
        if re.fullmatch(r'\d+[,.]?\d*(KG|CM|L|W|MM)', u): continue
        out.append(u)
    return out


def brand_from_name(name, extra, generic):
    up = ' ' + name.upper() + ' '
    for b in sorted(set(extra) | set(generic), key=lambda b: (-len(b), b)):
        if re.search(r'(?<![A-Z0-9])' + re.escape(b) + r'(?![A-Z0-9])', up):
            return b
    return ''


def clean_tokens(name, words):
    """페이지 없는 행용: 후보가 1개이고, 모델이 공백으로 쪼개진 모양(앞뒤에 짧은 코드 조각)이 아니면 채택."""
    generic = words["generic"]
    toks = tokens(name, words["stop"])
    if len(set(toks)) != 1: return ''
    t = toks[0]
    words = re.split(r'[\s,;()]+', name)
    idx = [i for i, w in enumerate(words) if w.upper().strip('.') == t]
    if not idx: return ''
    i = idx[0]
    def shortcode(w):
        u = w.upper()
        return bool(re.fullmatch(r'[A-Z0-9]{1,5}', u)) and u not in generic and u not in ('SERIE','LED','TYP','PRO','MAX','PLUS','NO','FROST','XL') and not w.lower() in ('na','po','ze','za','do','pro','bez','let','kg','cm','v')
    for j in (i-1, i+1):
        if not (0 <= j < len(words)): continue
        w = words[j]
        if re.fullmatch(r'\d+', w): continue
        nxt = words[j+1].upper() if j+1 < len(words) else ''
        if shortcode(w) and re.search(r'\d', w): return ''
        if j == i+1 and re.fullmatch(r'[A-Z]{1,2}', w) and nxt != 'SERIES': return ''
        if re.fullmatch(r'[A-Z]{2,6}', w) and w not in generic and w not in ('NO','FROST','SERIES','LED','PRO','MAX','PLUS','XL','ECO','WIFI','SLIM','NOFROST'): return ''
        if re.fullmatch(r'[A-Z]{2,}[a-z]+[A-Za-z]*', w) and w.upper() not in generic: return ''  # 예: KGNsf
    return t


def set_code(name, words, page_upper=None, strict=False):
    """'A + B' 세트 상품이면 'A + B', 아니면 ''. 각 부분(' + ' 기준)에서 모델 토큰을 하나씩 뽑는다."""
    parts = re.split(r'\s+\+\s+', name)
    codes = []
    for part in parts:
        if strict:
            c = clean_tokens(part, words)
            if c: codes.append(c)
            elif tokens(part, words["stop"]): return ''
            continue
        t = tokens(part, words["stop"])
        if t: codes.append(max(t, key=len))
    codes = list(dict.fromkeys(codes))
    if len(codes) < 2: return ''
    if page_upper is not None and not all(c in page_upper for c in codes): return ''
    return ' + '.join(codes)
