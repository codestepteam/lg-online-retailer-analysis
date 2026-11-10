"""Cairo Sales·Sharaf DG·Appliance Online·Falabella 공용. 10월 mix_common.py에서 사전 값만 인자로 뺐다."""
import html as H
import re


UNIT = re.compile(r'^\d+([.,]\d+)?(KG|OBR|RPM|CM|L|LT|LTS|T|W|KW|MM|HZ|V|LITR|LITRU|LITROS|MIN|DB|BAR|M|G|ML|KWH|'
                  r'BTU|FT|PIES|P|PULG|INCH|IN|KGS|CC|A|AH|WH|GB|TB|HP)$', re.I)


def clean(s):
    return re.sub(r'\s+', ' ', H.unescape(s or '')).strip()


def norm_brand(b):
    b = clean(b).upper()
    b = re.sub(r'\s*\.$', '', b)
    return b


def name_tokens(name, stop):
    """상품명에서 모델 번호처럼 생긴 토큰 후보(문장 속 순서대로)."""
    name = re.sub(r'([\u0600-\u06FF])([A-Za-z0-9])', r'\1 \2', name)
    out = []
    for m in re.finditer(r"(?<![A-Za-z0-9])[A-Za-z0-9][A-Za-z0-9\-/\.\(\)]*[A-Za-z0-9\)]", name):
        t = m.group(0)
        u = t.upper().rstrip('.')
        u = re.sub(r'\)$', '', u) if u.count(')') > u.count('(') else u
        if len(u) < 5 or u in stop:
            continue
        if not (re.search(r'[A-Z]', u) and re.search(r'\d', u)):
            continue
        if UNIT.match(u) or re.fullmatch(r'\d+X\d+(X\d+)?(CM|MM)?', u):
            continue
        if re.fullmatch(r'\d+[A-Z]{1,3}', u):  # 450L, 9KG 같은 숫자+짧은 단위
            continue
        if re.fullmatch(r'[\d.,/\-]+(KG|G|W|WATTS?|M2|M3|HZ|LTS?|L|CM|MM|V|RPM|OBR)?([/\-][\d.,]*(KG|L|LT)?)?', u):
            continue
        if re.fullmatch(r'[A-Z]{1,3}\d+(HZ|KG|WATTS?|RPM)', u):
            continue
        if re.fullmatch(r'\d+(/\d+)+', u):
            continue
        if re.fullmatch(r'(A|B|C|D|E|F|G)\++', u):
            continue
        out.append((m.start(), u))
    return out


def pick_code(name, stop, page=None):
    """상품명에서 코드 한 개(또는 'A + B') 고르기. 확실하지 않으면 ''."""
    toks = name_tokens(name, stop)
    if page is not None:
        pu = page.upper()
        toks = [(p, t) for p, t in toks if t in pu]
    toks = [(p, t) for p, t in toks]
    # 중복 제거(순서 유지)
    seen, uniq = set(), []
    for p, t in toks:
        if t not in seen:
            seen.add(t); uniq.append((p, t))
    toks = uniq
    if not toks:
        return ''
    if len(toks) == 1:
        return toks[0][1]
    # 두 개: 사이에 '+' 또는 '&' 가 있으면 세트
    if len(toks) == 2:
        between = name[toks[0][0] + len(toks[0][1]) - 1: toks[1][0]]
        if re.search(r'[+&]', between) and len(between) < 8:
            return toks[0][1] + ' + ' + toks[1][1]
    # 여러 개가 모두 '+' 로 이어진 묶음 상품
    if len(toks) >= 3 or len(toks) == 2:
        ok = True
        for a, b in zip(toks, toks[1:]):
            between = name[a[0] + len(a[1]) - 1: b[0]]
            if not (re.search(r'[+&]', between) and len(between) < 45):
                ok = False; break
        if ok:
            return ' + '.join(t for _, t in toks)
    # 여러 개: 상품명 맨 끝 토큰이면 그것, 아니면 모호 -> 빈칸
    last_p, last_t = toks[-1]
    tail = name[last_p + len(last_t):]
    if len(tail.strip(' -)')) <= 2:
        return last_t
    return ''


def tail_code(name, page=None):
    """'... - MODEL' 꼴(마지막 ' - ' 뒤)이 모델처럼 생겼으면 그 값(공백 포함)."""
    parts = re.split(r'\s[-\u2013\u2014]\s', name)
    if len(parts) < 2:
        return ''
    t = parts[-1].strip().rstrip('.')
    words = t.split()
    if not words or len(words) > 4 or len(t) < 5 or len(t) > 30:
        return ''
    if not (re.search(r'[A-Za-z]', t) and re.search(r'\d', t)):
        return ''
    for w in words:
        if not (re.search(r'\d', w) or (w.isupper() and len(w) >= 2)):
            return ''
    if UNIT.match(t.replace(' ', '')):
        return ''
    u = t.upper()
    if page is not None and u not in clean(page).upper():
        return ''
    return u


def spaced_tail(name, page=None):
    """상품명 맨 끝의 띄어쓴 모델(예: 'WWI 860 WPS', 'RFD 75850 GBK')."""
    if '+' in name:
        return ''
    name = re.sub(r'([\u0600-\u06FF])([A-Za-z0-9])', r'\1 \2', name)
    words = re.split(r'[\s]+', name.strip().rstrip('.'))
    got = []
    for w in reversed(words):
        w2 = w.strip(',')
        if UNIT.match(w2) or not w2:
            break
        if re.search(r'\d', w2) and re.fullmatch(r'[A-Za-z0-9\-/\.]+', w2) and not w2.islower():
            got.append(w2.upper())
        elif w2.isupper() and w2.isalpha() and len(w2) >= 1:
            got.append(w2)
        else:
            break
    got.reverse()
    t = ' '.join(got)
    if got and got[-1] in {'LT', 'LTS', 'L', 'KG', 'W', 'CM', 'MM', 'HZ', 'V', 'RPM'}:
        return ''
    if len(got) < 2 or len(t) < 6 or len(t) > 30:
        return ''
    if not (re.search(r'\d', t) and any(g.isalpha() and len(g) >= 2 for g in got) and re.search(r'[A-Z]{2}', t)):
        return ''
    if page is not None and t not in clean(page).upper():
        return ''
    return t


AR_MAP = str.maketrans({'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي', 'ـ': ''})


AR_RE = re.compile(r'[\u0600-\u06FF]')


def ar_norm(s):
    return re.sub(r'[\u064B-\u065F]', '', s.translate(AR_MAP))


def brand_from_text(text, brands, generic, alias=None):
    """text 안에서 가장 먼저 나오는 브랜드(같은 위치면 긴 이름 우선). 아랍어 키는 단어 앞 경계만 확인."""
    alias = alias or {}
    up = ' ' + ar_norm(clean(text).upper()) + ' '
    best = None
    cands = {b: b for b in set(brands) | set(generic)}
    for a, b in alias.items():
        cands[a.upper()] = b
    for key, val in cands.items():
        if not key or len(key) < 2:
            continue
        k = ar_norm(key)
        if AR_RE.search(k):
            pat = r'(?<![A-Z0-9\u0600-\u06FF])' + re.escape(k)
        else:
            pat = r'(?<![A-Z0-9\u0600-\u06FF])' + re.escape(k) + r'(?![A-Z0-9\u0600-\u06FF])'
        m = re.search(pat, up)
        if m:
            kk = (m.start(), -len(k))
            if best is None or kk < best[0]:
                best = (kk, val)
    return best[1] if best else ''
