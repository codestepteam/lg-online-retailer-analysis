# 공통 도구: 브랜드 사전, 상품명 모델 토큰 추출, 페이지(JSON-LD) 읽기. 표준 라이브러리만 사용.
import csv, gzip, json, re, os, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENERIC_BRANDS = """LG SAMSUNG BOSCH SIEMENS HISENSE HAIER ELECTROLUX AEG ZANUSSI BEKO GRUNDIG GORENJE WHIRLPOOL INDESIT HOTPOINT
CANDY HOOVER AMICA MIELE LIEBHERR SMEG SHARP TOSHIBA PANASONIC MIDEA CECOTEC INFINITON BALAY BECKEN KUNFT BELTAX VOX
MPM SENCOR PHILIPS REMINGTON BABYLISS BRAUN ETA TEFAL ROWENTA DYSON XIAOMI MELISSA REVLON FAURE ARISTON CONTINENTAL EDISON
BRANDT DE-DIETRICH DEDIETRICH ESSENTIEL FAGOR TEKA PITSOS NEFF CONSTRUCTA GAGGENAU VESTEL FINLUX ORION TCL ARCELIK ALTUS
DAEWOO ZEROWATT ROSIERES SCHOLTES SAUTER VIVAX SMITH&BROWN KLEIN MEDIA-TECH PROFICARE MESKO COSHARE LIN BERG ZELMER
WHITE-WESTINGHOUSE WESTINGHOUSE KENWOOD MORPHY RICHARDS RUSSELL HOBBS ADLER CAMRY CLATRONIC SEVERIN BOMANN PRIVILEG
QUADRO FRIGIDAIRE HITACHI SANYO MAXWELL ESPERANZA TELESTAR NORDMENDE NEO TECHWOOD MIDEA COMFEE HYUNDAI KONCEPT EZIO
SILVERCREST AMSTRAD OK. OK GENERAL-ELECTRIC GE SALORA TELEFUNKEN HANSEATIC BAUKNECHT KÜPPERSBUSCH GORENJE-ASKO ASKO
SAMSUNG-ELECTRONICS FOSTER HOMA RECAMANIA ZANKER JUNO PRIVILEG HOTPOINT-ARISTON CAPLE NODOR LOGIK HAIER-HOON HOON
SENCOR CONCEPT EVVO BLAUPUNKT TEESA JVC SMEGO ELEKTRA-BREGENZ ELEKTRABREGENZ BERTAZZONI SIMFER AMICA-DOMOWA SEVERIN
MOULINEX KRUPS BLACK+DECKER VALERA PARLUX GAMA-ITALY GAMA BOSCH-BALAY TRISTAR MAGNUM WPRO WHIRLPOOL-WPRO THOMSON
UFESA DOMO ZELMER BEKO-GRUNDIG GRUNDIG-BEKO ELEKTRA ORAVA ECG FIRST AUSTRIA NOVEEN BLOMBERG ARDO ELICA CATA
""".split()
GENERIC_BRANDS = [b.replace('-', ' ') if b in ('DE-DIETRICH','WHITE-WESTINGHOUSE','MEDIA-TECH') else b for b in GENERIC_BRANDS]
# 이름 안에 우연히 같은 글자가 나오기 쉬운 짧은 단어는 사전에서 제외
DROP = {'OK', 'OK.', 'GE', 'NEO', 'LIN', 'FIRST', 'GAMA', 'DOMO', 'ELEKTRA', 'CATA', 'CONCEPT', 'FOSTER', 'HOON', 'LOGIK', 'JUNO'}
KEEP_IF_UPPER = {'LIN', 'NEO', 'FIRST', 'GAMA', 'DOMO', 'ELEKTRA', 'CATA', 'CONCEPT', 'FOSTER', 'LOGIK', 'JUNO'}  # 전부 대문자로 적힌 경우만 인정

ARABIC = {'ال جى': 'LG', 'سامسونج': 'SAMSUNG'}

def norm_brand(b):
    return re.sub(r'\s+', ' ', b.strip()).upper()

def read_rows(fname):
    with open(os.path.join(BASE, 'inputs', fname), encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def read_html(path):
    with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as f:
        return f.read()

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

def build_brand_matcher(extra=()):
    names = set(norm_brand(b) for b in list(GENERIC_BRANDS) + list(extra) if b)
    names = {n for n in names if n and n not in ('S/MARCA',)}
    pats = []
    for n in sorted(names, key=len, reverse=True):
        pats.append((n, re.compile(r'(?<![\w&])' + re.escape(n).replace(r'\ ', r'[\s\-]') + r'(?![\w&])', re.I)))
    def find(name):
        best = None
        for n, p in pats:
            for m in p.finditer(name):
                if n in KEEP_IF_UPPER or n in DROP:
                    if m.group(0) != m.group(0).upper():
                        continue
                if best is None or m.start() < best[0]:
                    best = (m.start(), n)
                break
        return best[1] if best else ''
    return find

def write_part(fname, out_rows):
    d = os.path.join(BASE, 'parts')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, fname), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['행번호', '확인 요청 URL', '브랜드명', '제품코드', '브랜드 찾은곳', '제품코드 찾은곳'])
        w.writerows(out_rows)

def report(rows, out_rows):
    assert len(rows) == len(out_rows)
    for a, b in zip(rows, out_rows):
        assert a['행번호'] == b[0]
    t = collections.Counter()
    for a, b in zip(rows, out_rows):
        t[(a['모수 포함 여부'], 'B:' + b[4], 'C:' + b[5])] += 1
    print('rows', len(rows))
    for k, v in sorted(t.items()):
        print(k, v)
    for grp in ('포함', '검토 필요', '제외'):
        sub = [b for a, b in zip(rows, out_rows) if a['모수 포함 여부'] == grp]
        if sub:
            print(grp, len(sub), '브랜드채움 %.1f%%' % (100 * sum(1 for b in sub if b[2]) / len(sub)), '코드채움 %.1f%%' % (100 * sum(1 for b in sub if b[3]) / len(sub)))

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
