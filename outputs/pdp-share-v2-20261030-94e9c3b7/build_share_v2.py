# 공유용 v2: 기존 공유용 CSV에 브랜드·제품코드 2열을 제품군 뒤에 넣는다(D082).
# OSM 행은 OSM 원본 CSV를 같은 순서로 맞춰 BRAND·MPC를 옮기고, 검색 행은 parts/*.csv(리테일러별 추출 결과)를 행번호로 붙인다.
# 행별로 값을 어디서 찾았는지는 공유 파일이 아니라 이 폴더의 근거 CSV에 남긴다.
import csv, glob, sys
from pathlib import Path

ROOT = Path('/Users/codestepseunghee/codestep/lg-online-retailer-analysis')
PDP = ROOT / 'pdp 모수 추출'
HERE = Path(__file__).resolve().parent
SRC = PDP / '최종_20261029/PDP모수_공유용_25개국_35개리테일러_전체판정_55997행_20261029.csv'
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else PDP / '최종_20261029/PDP모수_공유용_v2_25개국_35개리테일러_전체판정_55997행_20261030.csv'
NULL = ('', '\\N')

# 자동 추출로 제품코드가 비었거나 틀린 행을 사람이 확인해 넣은 값. (행번호 → 제품코드, 찾은곳)
# Whirlpool·Siera 모델은 제조사 표기대로 띄어쓰기가 있어 상품명·페이지에 적힌 그대로 둔다.
# 모델 번호가 없는 행(55304 정수기 필터, 55682 반자동 세탁기, 47252 Falabella)은 빈칸으로 둔다.
MANUAL = {
    '21370': ('00312474', '상품명(페이지 mpn 312474로 확인)'),
    '21380': ('00312111', '상품명(페이지 mpn 312111로 확인)'),
    '33609': ('WPNEI84SBSWIFI', '상품명'),
    '54990': ('WTMS 551251 XNA', '상품명'), '55005': ('WBMF 703563 XNA', '상품명'),
    '55039': ('DP 480 NV', '상품명'), '55042': ('DP 460', '상품명'), '55046': ('DP 390', '상품명'),
    '55064': ('WTMF 601312 BNA', '상품명'), '55092': ('DP 480 /NV', '상품명'),
    '55108': ('GOWL 928/NB', '페이지 Modèle'), '55112': ('GOWL 928/NB + MWP 101 W', '상품명'),
    '55117': ('GMAL 9522/IXL', '페이지 Modèle'), '55119': ('GMAL 7522/IXL', '페이지 Modèle'),
    '55121': ('GMWL 928', '상품명'), '55406': ('F2Y1VYP6J.AMBPEMC', '상품명(뒤 9KG는 용량)'),
    '55483': ('WMTA 7122 S NA', '상품명'), '55544': ('FFD 11469 SBSV MA', '상품명'),
    '55548': ('WMTA 6101 S NA', '상품명'), '55549': ('WMTE 8123', '상품명'),
    '55553': ('TDLR 6228 FR/N', '상품명'), '55554': ('FFWS 7235SB', '상품명'),
    '55555': ('FFWS 7235 WB NA', '상품명'), '55556': ('FFWB 8248 WBS V NA', '상품명'),
    '55557': ('FFWD 9248 WBS V NA', '상품명'), '55558': ('FFWD 9248 SBS V NA', '상품명'),
    '55663': ('SPICR 309W1', '상품명'), '55664': ('SPICR 312W1', '상품명'),
    '55678': ('TDLR7220SSFRN', '페이지 Modèle'), '55794': ('TGML 650 IX', '페이지 Modèle'),
    '55913': ('MWP 304 M', '페이지 Modèle'),
    # 자동 값이 틀려 사용자가 확인해 준 값으로 바꾼 행
    '55407': ('W4W8BVPKZHM', '사용자 확인(자동 값 QMCWT1212KGLG는 꼬리 글자)'),
    '33504': ('WW90FG3M05AWLE', '사용자 확인(페이지 MPN …WLF 대신 상품명 …WLE)'),
    '33922': ('WW90FG3M05AWLE', '사용자 확인(페이지 MPN …WLF 대신 상품명 …WLE)'),
    '33606': ('WW80FG3M05AWLE', '사용자 확인(페이지 MPN …WLF 대신 상품명 …WLE)'),
    '34182': ('WW80FG3M05AWLE', '사용자 확인(페이지 MPN …WLF 대신 상품명 …WLE)'),
}

rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
cols = list(rows[0])
assert len(rows) == 55997, len(rows)

# OSM 원본: step1_filter.py 의 osm_rows 와 같은 파일·같은 순서
osm_src = []
for fname, keep in [('OSM_유럽13개리테일러_PDP후보_8160건_20261026.csv', lambda y: y['CNTRY'] not in ('Germany', 'UK')),
                    ('OSM_독일영국5개리테일러_PDP후보_1889건_20261029.csv', lambda y: True),
                    ('OSM_추가9개리테일러_PDP후보_4942건_20261028.csv', lambda y: True)]:
    osm_src += [(fname, y) for y in csv.DictReader(open(PDP / fname, encoding='utf-8-sig')) if keep(y)]

parts = {}
for f in sorted(glob.glob(str(HERE / 'parts/*.csv'))):
    for p in csv.DictReader(open(f, encoding='utf-8-sig')):
        assert p['행번호'] not in parts, p['행번호']
        parts[p['행번호']] = p

out, basis = [], []
osm_i = 0
for r in rows:
    if r['흐름'] == 'OSM':
        fname, y = osm_src[osm_i]
        osm_i += 1
        assert (fname, y['RAW_URL'], y['PRODUCT_DESC'], y['BRAND']) == (r['출처파일'], r['원본 상품 URL'], r['상품명'], r['OSM브랜드']), r['행번호']
        brand = y['BRAND'].strip().upper()
        if y['MPC'] not in NULL:
            code, where = y['MPC'].strip().upper(), 'OSM MPC'
        elif y['MODEL_DEDUP_KEY'] not in NULL:
            code, where = y['MODEL_DEDUP_KEY'].strip().upper(), 'OSM MODEL_DEDUP_KEY(MPC 빈칸)'
        else:
            code, where = '', '없음'
        bwhere = 'OSM BRAND'
    else:
        p = parts[r['행번호']]
        assert p['확인 요청 URL'] == r['확인 요청 URL'], r['행번호']
        brand, code = p['브랜드명'].strip().upper(), p['제품코드'].strip().upper()
        bwhere, where = p['브랜드 찾은곳'], p['제품코드 찾은곳']
        if r['행번호'] in MANUAL:
            code, where = MANUAL[r['행번호']]
            where = '수동 확인: ' + where
    new = {}
    for c in cols:
        new[c] = r[c]
        if c == '제품군':
            new['브랜드'], new['제품코드'] = brand, code
    out.append(new)
    basis.append({'행번호': r['행번호'], '흐름': r['흐름'], '국가': r['국가'], '리테일러': r['리테일러'],
                  '모수 포함 여부': r['모수 포함 여부'], '브랜드명': brand, '브랜드 찾은곳': bwhere,
                  '제품코드': code, '제품코드 찾은곳': where})
assert osm_i == len(osm_src)

def write(path, data):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(data[0]), quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(data)
write(OUT, out)
write(HERE / '브랜드_제품코드_근거.csv', basis)
print(OUT, len(out))
