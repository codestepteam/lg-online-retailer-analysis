"""1단계에서 남은 주소(A·B 합집합)를 Zyte로 열어 실제 도착 주소와 HTML을 저장한다.
- 이미 결과가 있는 주소는 건너뛴다(중간에 멈춰도 다시 실행하면 이어서 함)
- HTML은 gzip으로 html/ 아래 저장, 요약은 results.jsonl 한 줄씩
- API 키는 .env에서 읽고 어디에도 출력·저장하지 않는다
"""
import asyncio, base64, csv, gzip, hashlib, json, re, sys, time
from pathlib import Path
import aiohttp

S = Path(sys.argv[1])
CONC = int(sys.argv[2]) if len(sys.argv) > 2 else 30
LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 0
OUT = S / 'zyte_full'
(OUT / 'html').mkdir(parents=True, exist_ok=True)
RES = OUT / 'results.jsonl'

env = Path('/Users/codestepseunghee/codestep/lg-online-retailer-analysis/.env').read_text()
KEY = re.search(r'^ZYTE_API_KEY=(.*)$', env, re.M).group(1).strip().strip('"\'')
AUTH = aiohttp.BasicAuth(KEY, '')

# 대상: A·B에서 제외 아닌 행의 주소 (중복 없이)
targets = {}
for v in 'AB':
    for r in csv.DictReader(open(S / f'step1_프랑스{v}.csv', encoding='utf-8-sig')):
        if r['판정'] != '제외' and r['URL'] not in targets:
            targets[r['URL']] = (r['국가'], r['리테일러'])
done = set()
if RES.exists():
    for line in RES.open(encoding='utf-8'):
        d = json.loads(line)
        if d.get('ok'):
            done.add(d['요청URL'])
SKIP = set(sys.argv[4].split(',')) if len(sys.argv) > 4 and sys.argv[4] else set()  # 이번에 빼고 돌릴 리테일러
todo = [u for u in targets if u not in done and targets[u][1] not in SKIP]
import random; random.Random(1).shuffle(todo)  # 한 사이트에 몰리지 않게 섞는다
if LIMIT:
    todo = todo[:LIMIT]
print(f'전체 {len(targets)} / 완료 {len(done)} / 이번 {len(todo)} / 동시 {CONC}', flush=True)

def canon(html):
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*>', html, re.I)
    if not m:
        return ''
    h = re.search(r'href=["\']([^"\']+)', m.group(0))
    return h.group(1) if h else ''

def title(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip()[:200] if m else ''

stat = {'ok': 0, 'fail': 0}
t0 = time.time()
lock = asyncio.Lock()

async def one(sess, sem, url, fh):
    country, rtl = targets[url]
    rec = {'요청URL': url, '국가': country, '리테일러': rtl}
    async with sem:
        for attempt in range(4):
            try:
                async with sess.post('https://api.zyte.com/v1/extract', auth=AUTH, timeout=aiohttp.ClientTimeout(total=180),
                                     json={'url': url, 'httpResponseBody': True}) as resp:
                    body = await resp.json(content_type=None)
                    if resp.status == 200:
                        html = base64.b64decode(body['httpResponseBody']).decode('utf-8', 'replace')
                        name = hashlib.sha1(url.encode()).hexdigest()[:16] + '.html.gz'
                        (OUT / 'html' / name).write_bytes(gzip.compress(html.encode('utf-8')))
                        rec.update(ok=True, 실제URL=body.get('url', ''), 상태코드=body.get('statusCode'), 대표주소=canon(html),
                                   제목=title(html), HTML크기=len(html), HTML파일=name, 시도=attempt + 1)
                        break
                    rec.update(ok=False, 오류코드=resp.status, 오류=str(body.get('title') or body.get('detail') or body)[:200], 시도=attempt + 1)
                    if resp.status in (429, 503, 520, 521, 500):
                        await asyncio.sleep(5 * (attempt + 1) ** 2)
                        continue
                    break
            except Exception as e:
                rec.update(ok=False, 오류코드='예외', 오류=repr(e)[:200], 시도=attempt + 1)
                await asyncio.sleep(5 * (attempt + 1))
    async with lock:
        fh.write(json.dumps(rec, ensure_ascii=False) + '\n'); fh.flush()
        stat['ok' if rec.get('ok') else 'fail'] += 1
        n = stat['ok'] + stat['fail']
        if n % 200 == 0 or n == len(todo):
            el = time.time() - t0
            print(f'{n}/{len(todo)} 성공 {stat["ok"]} 실패 {stat["fail"]} 경과 {el/60:.1f}분 예상남은 {el/n*(len(todo)-n)/60:.1f}분', flush=True)

async def main():
    sem = asyncio.Semaphore(CONC)
    async with aiohttp.ClientSession() as sess:
        with RES.open('a', encoding='utf-8') as fh:
            await asyncio.gather(*(one(sess, sem, u, fh) for u in todo))

asyncio.run(main())
print('끝', stat, flush=True)
