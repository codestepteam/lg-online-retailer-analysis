# 공유용 v2 + EY 검토(D086) + 사용자 결정(D087) -> 공유용 v3
# 실행: python3 -I make_v3.py <rows.pkl> <v2.csv> <v3.csv>
# rows.pkl: EY 검토 엑셀(관련문서) `3. PDP모수` 탭을 openpyxl로 읽어 (행 목록, 기타) 형태로 저장한 임시 파일.
#           rows[0]은 머리글, 열 0 행번호 · 9 확인 요청 URL · 16 우리 판정(Q) · 17 EY 판정(R) · 18 EY 비고(S). 세션 임시 폴더에만 있었다.
import csv, pickle, sys, collections

PKL, V2, V3 = sys.argv[1:4]
rows, _ = pickle.load(open(PKL, 'rb'))
ey = {r[0]: r for r in rows[1:]}
R = list(csv.DictReader(open(V2, encoding='utf-8-sig')))
cols = list(R[0].keys())
assert len(R) == 55997 and len(ey) == 55997

TAG = ' 10-31 EY 검토 반영'
log = collections.Counter()


def memo(r, s):
    r['메모'] = (r['메모'] + ';' if r['메모'] else '') + TAG + ': ' + s
    r['메모'] = r['메모'].lstrip()


def inc(r, why):
    r['모수 포함 여부'], r['제외단계'], r['제외사유'] = '포함', '', ''
    memo(r, why); log[('포함', why)] += 1


def exc(r, step, reason, why):
    r['모수 포함 여부'], r['제외단계'], r['제외사유'] = '제외', step, reason
    memo(r, why); log[('제외', why)] += 1


# EY 비고(S열)·근거 -> 제외 단계
def ey_exclude(r, e):
    note, basis = e[18] or '', r['판매자근거']
    if note == 'PDP 아님':
        return '④페이지없음', '상품 페이지 아님'
    if note == 'OOS':
        return '④영구품절', '품절'
    if note.startswith('Marketplace'):
        return '③리리부', '외부 판매자(Vendu et installé par Darty 없음)'
    if note == '리퍼 제품':
        return '③리리부', '리퍼·중고'
    if '현재 구매 불가' in basis:
        return '④영구품절', '현재 구매 불가'
    if '상품 페이지 내용 없음' in basis:
        return '④페이지없음', '상품 페이지 내용 없음'
    if '열지 못함' in basis:
        return '④페이지없음', '상품 페이지를 열지 못함'
    raise SystemExit(f"분류 못함 {r['행번호']} {note} {basis}")


BRAND_NAME_SELLER = {'Electrolux', 'Brastemp', 'Midea Store', 'Samsung', 'LG'}
OWN = {'2054': ('제외', '④페이지없음', '상품 페이지 아님(첫 화면 주소)'),
       '2950': ('포함',), '7937': ('포함',),
       '8138': ('제외', '②제품군', '대상 제품군 아님(TV)')}

for r in R:
    n = int(r['행번호']); e = ey[n]
    assert e[9] == r['확인 요청 URL'] and e[16] == r['모수 포함 여부'], n
    q, ev, lg = r['모수 포함 여부'], e[17], r['브랜드'] == 'LG'
    ret, seller, kind = r['리테일러'], r['판매자'], r['판매자구분']
    # 1) EY R열이 우리 판정과 다르면 그대로 따름
    if ev is not None and ev != q and ev != '검토 필요':
        if ev == '포함':
            inc(r, 'EY 판정 포함(D086)')
        else:
            exc(r, *ey_exclude(r, e), 'EY 판정 제외(D086)')
        continue
    if r['행번호'] in OWN:
        o = OWN[r['행번호']]
        if o[0] == '포함': inc(r, '규칙 없던 행, 사용자 결정 포함(D087)')
        else: exc(r, o[1], o[2], '규칙 없던 행, 사용자 결정 제외(D087)')
        continue
    if q == '포함':
        continue
    # 2) 경쟁사에 EY 규칙 넓혀 적용(D087)
    if not lg and ret == 'FALABELLA' and q == '제외' and seller in ('TOTTUS', 'SODIMAC'):
        inc(r, 'E1 TOTTUS·SODIMAC 판매 포함(경쟁사, D087)')
    elif not lg and ret == 'FALABELLA' and q == '제외' and seller == 'SAMSUNG TIENDA OFICIAL':
        inc(r, 'E2 브랜드 공식점 포함(경쟁사, D087)')
    elif not lg and ret == 'LAZADA' and q == '제외' and kind == '브랜드공식점':
        inc(r, 'E4 브랜드 공식점 포함(경쟁사, D087)')
    elif ret == 'MAGAZINELUIZA' and q == '제외' and kind == '외부판매자' and seller in BRAND_NAME_SELLER:
        inc(r, 'E12 판매자 이름이 브랜드 이름인 외부 판매자 포함(D087)')
    elif q == '검토 필요' and not lg and ret == 'AMAZON':
        if '현재 구매 불가' in r['판매자근거']:
            exc(r, '④영구품절', '현재 구매 불가', 'E6 현재 구매 불가 제외(경쟁사, D087)')
        else:
            inc(r, 'E6 판매자 확인 불가 포함(경쟁사, D087)')
    elif q == '검토 필요' and not lg and ret == 'DATART':
        if '/bazar/' in r['확인 요청 URL']:
            exc(r, '③리리부', '리퍼·중고(주소 /bazar/)', 'E8 리퍼 제외(경쟁사, D087)')
        else:
            inc(r, 'E8 정상 상품 페이지 포함(경쟁사, D087)')
    elif q == '검토 필요' and ret == 'MAGAZINELUIZA' and lg:
        inc(r, 'E12 판매자 확인 불가 포함(D087)')

# 3) 같은 주소 중복: 포함 행끼리 (국가, 리테일러, 주소)가 같으면 v2에서 이미 포함이던 행 또는 행번호가 가장 작은 행만 남김
groups = collections.defaultdict(list)
for r in R:
    if r['모수 포함 여부'] == '포함':
        groups[(r['국가'], r['리테일러'], r['확인 요청 URL'])].append(r)
v2inc = {r['행번호'] for r in csv.DictReader(open(V2, encoding='utf-8-sig')) if r['모수 포함 여부'] == '포함'}
for g in groups.values():
    if len(g) < 2: continue
    g.sort(key=lambda r: (r['행번호'] not in v2inc, int(r['행번호'])))
    assert sum(r['행번호'] in v2inc for r in g) <= 1, [r['행번호'] for r in g]
    for r in g[1:]:
        exc(r, '④중복', f"같은 주소(대표 행 {g[0]['행번호']})", f"같은 주소 중복 정리(대표 행 {g[0]['행번호']})")

with open(V3, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL)
    w.writeheader(); w.writerows(R)

for k, v in sorted(log.items()): print(v, k)
print(collections.Counter(r['모수 포함 여부'] for r in R))
