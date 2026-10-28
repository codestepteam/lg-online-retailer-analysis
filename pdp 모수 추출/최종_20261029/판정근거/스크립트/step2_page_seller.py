"""1단계 결과(step1_프랑스A/B.csv)에 페이지 확인 결과를 합친다 -> step2_프랑스A/B.csv, step2_집계.csv
- 페이지 상태: 없음(404/410/제목) -> 제외(④페이지없음), 영구품절 -> 제외(④영구품절)
- 판매자: 외부판매자·브랜드공식점·리퍼·중고 -> 제외(③리리부), 확인불가 -> 확인 필요
  (README 6장 "리셀은 직판이 아닌 외부 판매자 상품", D066, 10-29 사용자 결정 "외부 판매자 전부 제외")
- 같은 상품: 남은 행끼리 같은 리테일러 안에서 실제 도착 주소가 같으면 첫 행만 남긴다(④중복, #119)
행은 지우지 않는다(D036).
"""
import csv, gzip, json, re, sys, collections
from pathlib import Path
from urllib.parse import urljoin

S = Path(sys.argv[1]); Z = S / 'zyte_full'

page = {}
for l in open(Z / 'pages_best.jsonl', encoding='utf-8'):
    d = json.loads(l); page[d['요청URL']] = d

# 판매자: 뒤에 읽는 파일이 앞의 것을 덮어쓴다
seller = {}
for f in ['seller_g1.csv', 'seller_g2.csv', 'seller_g3.csv', 'seller_g4.csv',
          'seller_appliance_online.csv', 'seller_lazada.csv', 'seller_magalu.csv']:
    for r in csv.DictReader(open(Z / 'seller' / f, encoding='utf-8-sig')):
        seller[r['요청URL']] = r

# Falabella: 페이지의 sellerName이 FALABELLA인 것만 직판(D066)
for u, d in page.items():
    if d['리테일러'] != 'FALABELLA' or d['페이지상태'] != '정상':
        continue
    h = gzip.open(Z / (d.get('_dir') or 'html') / d['HTML파일'], 'rt', encoding='utf-8').read()
    m = re.search(r'"sellerName"\s*:\s*"([^"]+)"', h)
    s = m.group(1) if m else ''
    seller[u] = {'판매자': s, '판매자구분': '직판' if s.upper() == 'FALABELLA' else ('외부판매자' if s else '확인불가'),
                 '근거': f'sellerName "{s}"'}

def norm(u):
    u = u.split('#')[0].rstrip('/')
    u = re.sub(r'^https?://(www\.)?', '', u, flags=re.I).lower()
    m = re.search(r'(amazon\.[a-z.]+)/(?:.*/)?dp/([A-Z0-9]{10})', u, re.I)
    if m:
        return f'{m.group(1)}/dp/{m.group(2)}'.lower()
    return u

EXTRA_COLS = ['페이지상태', '실제URL', '판매자', '판매자구분', '판매자근거']
summary = []
for v in 'AB':
    rows = list(csv.DictReader(open(S / f'step1_프랑스{v}.csv', encoding='utf-8-sig')))
    stat = collections.Counter()
    for r in rows:
        for c in EXTRA_COLS:
            r[c] = ''
        if r['판정'] == '제외':
            continue
        p = page.get(r['URL'])
        if not p:
            r['판정'] = '확인 필요'; r['메모'] = '; '.join(x for x in [r['메모'], '페이지 확인 기록 없음'] if x); stat['기록없음'] += 1
            continue
        r['페이지상태'] = p['페이지상태']; r['실제URL'] = p.get('실제URL') or r['URL']
        s = seller.get(r['URL'])
        if s:
            r['판매자'] = s['판매자']; r['판매자구분'] = s['판매자구분']; r['판매자근거'] = s['근거'][:200]
        if re.search(r'/not-found\b', r['실제URL']):
            p = dict(p, 페이지상태='없음(not-found로 이동)')  # Unieuro: 없는 상품은 /online/not-found로 넘어감
        if p['페이지상태'].startswith('없음') or (p['페이지상태'] == '차단화면' and r['리테일러'] == 'MAGAZINELUIZA'):
            # Magalu 2건은 Codex에서도 "Oops!" 화면만 나옴 -> 페이지 없음
            r['판정'] = '제외'; r['제외단계'] = '④페이지없음'; r['제외사유'] = f"페이지 없음({p['페이지상태']}, {p.get('제목','')[:40]})"
        elif p['페이지상태'] == '영구품절':
            r['판정'] = '제외'; r['제외단계'] = '④영구품절'; r['제외사유'] = '영구 품절(단종) 표시'
        elif p['페이지상태'] != '정상':
            r['판정'] = '확인 필요'; r['메모'] = '; '.join(x for x in [r['메모'], f"페이지 {p['페이지상태']}"] if x)
        elif s and s['판매자구분'] in ('외부판매자', '브랜드공식점', '리퍼·중고'):
            r['판정'] = '제외'; r['제외단계'] = '③리리부'
            r['제외사유'] = {'외부판매자': '외부 판매자', '브랜드공식점': '브랜드 공식점(외부 판매자)', '리퍼·중고': '리퍼·중고'}[s['판매자구분']] + f" ({s['판매자']})"
        elif not s or s['판매자구분'] == '확인불가':
            r['판정'] = '확인 필요'; r['메모'] = '; '.join(x for x in [r['메모'], '판매자 확인 불가'] if x)
        stat[(r['판정'], r['제외단계'])] += 1
    # 같은 상품 하나로: 남김·확인 필요 행끼리 같은 (국가, 리테일러) 안에서
    # 실제 도착 주소가 같거나, 페이지가 적어 둔 대표 주소(canonical)가 같으면 첫 행만 남긴다.
    # 예외: AO는 대표 주소가 시리즈(8kg·12kg 등 다른 모델)를 가리킴, Coolblue 세트("A + B")는 대표 주소가 단품을 가리킴
    first = {}
    for r in rows:
        if r['판정'] == '제외':
            continue
        p = page.get(r['URL'], {})
        keys = [('실제 도착 주소', (r['국가'], r['리테일러'], 'u', norm(r['실제URL'] or r['URL'])))]
        c = p.get('대표주소', '')
        if c and r['리테일러'] != 'AO' and not (r['리테일러'] == 'COOLBLUE' and ' + ' in p.get('제목', '')):
            keys.append(('대표 주소', (r['국가'], r['리테일러'], 'c', norm(urljoin(r['실제URL'] or r['URL'], c)))))
        hit = next(((how, first[k]) for how, k in keys if k in first), None)
        if hit:
            r['판정'] = '제외'; r['제외단계'] = '④중복'; r['제외사유'] = f'같은 상품({hit[0]} 같음, 대표 행 {hit[1]})'
            stat[f'④중복({hit[0]})'] += 1
        for _, k in keys:
            first.setdefault(k, hit[1] if hit else r['행번호'])
    cols = list(rows[0].keys())
    with open(S / f'step2_프랑스{v}.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    agg = collections.defaultdict(collections.Counter)
    for r in rows:
        agg[(r['국가'], r['리테일러'])][r['판정']] += 1
        agg[(r['국가'], r['리테일러'])]['전체'] += 1
    for k, c in sorted(agg.items()):
        summary.append([v, k[0], k[1], c['전체'], c['남김'], c['확인 필요'], c['제외']])
    print(v, collections.Counter(r['판정'] for r in rows), dict(stat))
with open(S / 'step2_집계.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f); w.writerow(['판', '국가', '리테일러', '전체', '남김', '확인 필요', '제외']); w.writerows(summary)
