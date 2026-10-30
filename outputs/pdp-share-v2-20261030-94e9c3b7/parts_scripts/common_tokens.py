"""MediaMarkt/Electroplanet 공용: 상품명에서 모델 번호 모양 토큰 뽑기."""
import re
UNIT = re.compile(r'^\d+([.,]\d+)?(KG|RPM|OBR|CM|MM|L|LT|LTR|LITR\w*|T|TR|TRS|W|KW|KWH|V|HZ|DB|MIN|GB|TB|INCH|P|K|M|OTACEK|U|FOT)$', re.I)
def valid(t):
    t = t.strip('.,;:()[]"\'')
    if len(t) < 5 or UNIT.match(t): return False
    if not (re.search(r'\d', t) and re.search(r'[A-Za-z]', t)): return False
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.\-_]*[A-Za-z0-9+]?', t): return False
    if re.fullmatch(r'[A-Za-z]\+*', t): return False
    if any(re.search(r'\d', seg) and re.search(r'[A-Za-z]{6,}', seg) for seg in re.split(r'[.\-_]', t)): return False  # 단어가 붙어 버린 설명(THERMOSTAT8POSIT 등). 글자만 있는 조각은 허용
    if re.fullmatch(r'(?i)SERIE\d+', t): return False
    if re.match(r'\d', t) and len(t) < 8: return False           # 숫자로 시작하는 짧은 토큰(6C2M1PX 등)은 불확실
    if re.fullmatch(r'(?i)\d+(KG|BAR|BARS|CV|C|PRG|PROG|P|PCS|ML|CL|TRANCHES|FEUX|F|BLADES|ACCES|ESENS|TR|T|W|L|COUV|POSIT|GB|TB|G|K)(\d+[A-Za-z]*)?\+?', t): return False
    if re.fullmatch(r'\d+-[A-Za-z]{1,3}-\d+', t): return False  # 10-EN-1 같은 '다기능' 표기
    return True
def norm(s): return re.sub(r'[^A-Z0-9]', '', s.upper())
def models_from_word(w):
    """한 단어(공백 없이 이어진 것)에서 모델 후보. 'A/B' 는 둘 다 모델이면 A + B, 뒤가 짧은 알파벳이면 꼬리로 유지."""
    w = w.strip('.,;:()[]"\'')
    parts = w.split('/')
    ok = [p for p in parts if valid(p)]
    if not ok: return []
    rest = [p for p in parts if p not in ok]
    if len(ok) == 1 and parts[0] == ok[0] and len(parts) == 2 and re.fullmatch(r'[A-Za-z0-9]{1,4}', parts[1]) and not re.fullmatch(r'\d+[A-Za-z]{0,2}', parts[1]):
        return [w]  # 리테일러 꼬리(/MA, /98S 등)는 상품명 표기 그대로 유지
    return ok
def title_models(title, skip_words=0, max_words=5):
    seg = re.split(r'\s+[-–]\s+', title)[0]
    words = seg.split()[skip_words:skip_words + max_words]
    for w in words:
        m = models_from_word(w)
        if m: return [x.upper() for x in dict.fromkeys(m)]
    return []
