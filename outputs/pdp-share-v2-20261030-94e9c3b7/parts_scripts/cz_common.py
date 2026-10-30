import csv, gzip, re, json, html as H

GENERIC = ['LG','SAMSUNG','HISENSE','GORENJE','BOSCH','SIEMENS','BEKO','ELECTROLUX','AEG','WHIRLPOOL','CANDY','HAIER',
 'PHILCO','ZANUSSI','MIELE','SHARP','TOSHIBA','PANASONIC','SMEG','HOTPOINT','INDESIT','AMICA','MPM','CONCEPT','GUZZANTI',
 'ROMO','ETA','ARDO','LIEBHERR','FRIGIDAIRE','MIDEA','HYUNDAI','TESLA','SENCOR','ECG','ARISTON','NEOLUX','BAUKNECHT',
 'HITACHI','HAIER','CATA','FAGOR','TEKA','MORA','PHILIPS','GRUNDIG','KRUPS','DE\'LONGHI','POLAROID','NORDFROST','ROLLER']
UNIT = re.compile(r'^\d+(KG|OBR|RPM|CM|L|T|W|KW|MM|HZ|V|LITR|LITRU|MIN|DB|BAR|M|G|ML|KWH|\"|L/MIN|X\d+)$', re.I)
STOP = {'3DSCAN','DOORCOOLING','INSTAVIEW','WIFI','NOFROST','AIRWASH'}

def rd(path):
    return list(csv.DictReader(open(path, encoding='utf-8-sig')))

def load(p):
    try:
        return gzip.open(p, 'rt', encoding='utf-8', errors='replace').read()
    except Exception:
        return None

def tokens(name):
    out = []
    for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9\-/\.]*[A-Za-z0-9]", name):
        u = t.upper()
        if len(u) < 5 or u in STOP: continue
        if not (re.search(r'[A-Z]', u) and re.search(r'\d', u)): continue
        if UNIT.match(u) or re.fullmatch(r'\d{3,5}[A-Z]?', u): continue
        if re.fullmatch(r'\d+[,.]?\d*(KG|CM|L|W|MM)', u): continue
        out.append(u)
    return out

def brand_from_name(name, extra):
    up = ' ' + name.upper() + ' '
    for b in sorted(set(extra) | set(GENERIC), key=len, reverse=True):
        if re.search(r'(?<![A-Z0-9])' + re.escape(b) + r'(?![A-Z0-9])', up):
            return b
    return ''

def write(path, out):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['행번호','확인 요청 URL','브랜드명','제품코드','브랜드 찾은곳','제품코드 찾은곳'])
        w.writerows(out)

def report(rows, out):
    from collections import Counter
    assert len(rows) == len(out)
    c = Counter()
    for r, o in zip(rows, out):
        c[(r['모수 포함 여부'], 'B:' + o[4], 'P:' + o[5])] += 1
    for k in sorted(c): print(k, c[k])

def clean_tokens(name):
    """페이지 없는 행용: 후보가 1개이고, 모델이 공백으로 쪼개진 모양(앞뒤에 짧은 코드 조각)이 아니면 채택."""
    toks = tokens(name)
    if len(set(toks)) != 1: return ''
    t = toks[0]
    words = re.split(r'[\s,;()]+', name)
    idx = [i for i, w in enumerate(words) if w.upper().strip('.') == t]
    if not idx: return ''
    i = idx[0]
    def shortcode(w):
        u = w.upper()
        return bool(re.fullmatch(r'[A-Z0-9]{1,5}', u)) and u not in GENERIC and u not in ('SERIE','LED','TYP','PRO','MAX','PLUS','NO','FROST','XL') and not w.lower() in ('na','po','ze','za','do','pro','bez','let','kg','cm','v')
    for j in (i-1, i+1):
        if not (0 <= j < len(words)): continue
        w = words[j]
        if re.fullmatch(r'\d+', w): continue
        nxt = words[j+1].upper() if j+1 < len(words) else ''
        if shortcode(w) and re.search(r'\d', w): return ''
        if j == i+1 and re.fullmatch(r'[A-Z]{1,2}', w) and nxt != 'SERIES': return ''
        if re.fullmatch(r'[A-Z]{2,6}', w) and w not in GENERIC and w not in ('NO','FROST','SERIES','LED','PRO','MAX','PLUS','XL','ECO','WIFI','SLIM','NOFROST'): return ''
        if re.fullmatch(r'[A-Z]{2,}[a-z]+[A-Za-z]*', w) and w.upper() not in GENERIC: return ''  # 예: KGNsf
    return t

def set_code(name, page_upper=None, strict=False):
    """'A + B' 세트 상품이면 'A + B', 아니면 ''. 각 부분(' + ' 기준)에서 모델 토큰을 하나씩 뽑는다."""
    parts = re.split(r'\s+\+\s+', name)
    codes = []
    for part in parts:
        if strict:
            c = clean_tokens(part)
            if c: codes.append(c)
            elif tokens(part): return ''
            continue
        t = tokens(part)
        if t: codes.append(max(t, key=len))
    codes = list(dict.fromkeys(codes))
    if len(codes) < 2: return ''
    if page_upper is not None and not all(c in page_upper for c in codes): return ''
    return ' + '.join(codes)
