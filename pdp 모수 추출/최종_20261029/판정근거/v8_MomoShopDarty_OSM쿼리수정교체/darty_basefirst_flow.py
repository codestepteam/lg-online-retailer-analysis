"""Darty: 지금 규칙(v7) vs 원래 상품 주소 우선으로 골랐을 때 PDP 모수 흐름 비교."""
import collections
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
g = json.load(open(HERE / 'darty_groups.json'))
v7 = {}
for f in (ROOT / 'pdp 모수 추출').rglob('PDP모수_공유용_v7_*.csv'):
    for r in csv.DictReader(open(f, encoding='utf-8-sig')):
        if r['리테일러'].upper() == 'DARTY':
            v7[r['원본 상품 URL']] = r
print('v7 Darty', len(v7))
print('제외단계 x 판매자구분', collections.Counter((r['제외단계'], r['판매자구분']) for r in v7.values() if r['모수 포함 여부'] != '포함'))


def rk(r, null_first):
    s = r['RK_S']
    if s in (None, ''):
        return (0, 0) if null_first else (1, 0)
    return (1, float(s)) if null_first else (0, float(s))


def plain(u):
    return '?' not in u and '#' not in u


def pick(v, mode):
    if mode == 'now':
        key = lambda r: (r['PRIO'], rk(r, True), len(r['CUT']), r['CUT'], r['URL'])
    else:
        key = lambda r: (0 if plain(r['URL']) else 1, r['PRIO'], rk(r, False), len(r['CUT']), r['CUT'], r['URL'])
    return sorted(v, key=key)[0]['URL']


def reason(r):
    if r['모수 포함 여부'] == '포함':
        return '포함'
    s = r['판매자구분']
    if s == '외부판매자':
        return '외부 판매자'
    if '리퍼' in s:
        return '리퍼·중고'
    if s in ('확인불가', '영구품절') or '품절' in r['제외사유'] or '확인' in s:
        return '확인 불가·영구 품절'
    return '기타'


now = {k: pick(v, 'now') for k, v in g.items()}
base = {k: pick(v, 'base') for k, v in g.items()}
lg = {k: k.split('|')[1] == 'LG' for k in g}
miss = [u for u in now.values() if u not in v7]
print('now kept not in v7', len(miss))

tab = collections.Counter()
for k in g:
    for mode, ks in [('now', now), ('base', base)]:
        u = ks[k]
        kind = 'ofmp' if '?ofmp=' in u.lower() else '원래'
        tab[(mode, 'kind', kind, lg[k])] += 1
        if mode == 'now' or u == now[k]:
            res = reason(v7[u])
        else:
            res = '판정 필요'
        tab[(mode, 'res', res, lg[k])] += 1
for k, n in sorted(tab.items(), key=str):
    print(n, k)
# 바뀐 152개의 지금 판정
ch = [k for k in g if now[k] != base[k]]
print('changed', len(ch), 'LG', sum(lg[k] for k in ch),
      collections.Counter((reason(v7[now[k]]), lg[k]) for k in ch))
print('changed DIV', collections.Counter(k.split('|')[0] for k in ch))
