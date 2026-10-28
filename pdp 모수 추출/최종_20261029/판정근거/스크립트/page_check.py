"""받은 페이지 전체를 검사해 주소마다 쓸 기록 하나를 고른다 -> zyte_full/pages_best.jsonl"""
import json,gzip,re,sys,collections
d=sys.argv[1]
BLOCK=re.compile(r'sec-if-cpt|window\["bobcmn"\]|captcha|cf-chl|Just a moment|Access Denied|Não é possível acessar|px-captcha|Pardon Our Interruption|Request unsuccessful',re.I)
def load(f, sub='html'):
    try:
        for l in open(f'{d}/{f}',encoding='utf-8'):
            x=json.loads(l); x['_dir']=sub; yield x
    except FileNotFoundError: return
cands=collections.defaultdict(list)
for f,sub,pri in [('results.jsonl','html',1),('results_browser.jsonl','html',2),('results_codex_magalu.jsonl','html_codex',3)]:
    for x in load(f,sub):
        x['_pri']=pri; cands[x['요청URL']].append(x)
out=[]; stat=collections.Counter()
for u,xs in cands.items():
    best=None
    for x in sorted(xs,key=lambda x:-x['_pri']):
        if not x.get('ok'): continue
        h=gzip.decompress(open(f"{d}/{x['_dir']}/{x['HTML파일']}",'rb').read()).decode('utf-8','replace')
        # 차단 문구는 페이지가 작을 때만 차단으로 본다(정상 페이지 스크립트에도 captcha 단어가 있을 수 있음)
        blocked = x['HTML크기']<60000 and (BLOCK.search(h) or not x.get('제목'))
        x['페이지상태']='차단화면' if blocked else ('없음(%s)'%x['상태코드'] if x.get('상태코드') in (404,410) else ('없음(제목)' if re.match(r'(page not found|404\b)',(x.get('제목') or '').strip(),re.I) else '정상'))
        # 410이어도 상품 페이지가 뜨고 품절 표시만 있는 경우(MediaMarkt "dauerhaft ausverkauft", ECI "AGOTADO")는 영구품절로 따로 둔다
        if x['페이지상태']=='없음(410)' and x.get('제목') and re.search(r'ausverkauft|AGOTADO|nem elérhető|niet meer|"availability":"[^"]*OutOfStock|ONLINE_NOT_AVAILABLE|PERMANENTLY',h,re.I):
            x['페이지상태']='영구품절'
        if not blocked: best=x; break
        if best is None: best=x
    if best is None: best=dict(xs[-1],페이지상태='수집실패')
    stat[(best['리테일러'],best['페이지상태'][:6])]+=1
    best.pop('_pri',None); out.append(best)
with open(f'{d}/pages_best.jsonl','w',encoding='utf-8') as f:
    for x in out: f.write(json.dumps(x,ensure_ascii=False)+'\n')
agg=collections.defaultdict(dict)
for (r,s),n in stat.items(): agg[r][s]=n
for r,v in sorted(agg.items()):
    if set(v)!={'정상'}: print(r,v)
print('전체',len(out),collections.Counter(x['페이지상태'][:6] for x in out))
