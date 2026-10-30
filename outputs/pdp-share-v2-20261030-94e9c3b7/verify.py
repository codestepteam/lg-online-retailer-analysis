# 공유용 v2 검증: 기존 24열은 모든 셀이 그대로인지, 새 2열이 제품군 뒤에 있는지, 건수표를 출력한다.
# 가짜 입력(열 하나 값 변경, 행 순서 뒤바꿈)에서도 차이를 잡는지 함께 확인한다.
import collections, copy, csv, sys
from pathlib import Path

PDP = Path('/Users/codestepseunghee/codestep/lg-online-retailer-analysis/pdp 모수 추출/최종_20261029')
OLD = PDP / 'PDP모수_공유용_25개국_35개리테일러_전체판정_55997행_20261029.csv'
NEW = Path(sys.argv[1]) if len(sys.argv) > 1 else PDP / 'PDP모수_공유용_v2_25개국_35개리테일러_전체판정_55997행_20261030.csv'
NEWCOLS = ['브랜드', '제품코드']

def check(old, new):
    errs = []
    oc, nc = list(old[0]), list(new[0])
    i = oc.index('제품군') + 1
    if nc != oc[:i] + NEWCOLS + oc[i:]:
        errs.append('열 구성 다름')
    if len(old) != len(new):
        errs.append(f'행 수 다름 {len(old)} {len(new)}')
    for a, b in zip(old, new):
        for c in oc:
            if a[c] != b.get(c):
                errs.append(f'행번호 {a["행번호"]} {c} 다름')
                break
    return errs

old = list(csv.DictReader(open(OLD, encoding='utf-8-sig')))
new = list(csv.DictReader(open(NEW, encoding='utf-8-sig')))
errs = check(old, new)
print('실제 파일 차이:', len(errs), errs[:5])

fake1 = copy.deepcopy(new); fake1[100]['상품명'] += 'x'
fake2 = new[:]; fake2[0], fake2[1] = fake2[1], fake2[0]
fake3 = [{k: v for k, v in r.items() if k != '제품코드'} for r in new[:10]]
print('가짜 입력 검출:', bool(check(old, fake1)), bool(check(old, fake2)), bool(check(old[:10], fake3)))

print('\n[흐름 × 모수 포함 여부] 브랜드 빈칸 / 제품코드 빈칸 / 전체')
t = collections.defaultdict(lambda: [0, 0, 0])
for r in new:
    k = (r['흐름'], r['모수 포함 여부'])
    t[k][0] += not r['브랜드']; t[k][1] += not r['제품코드']; t[k][2] += 1
for k in sorted(t):
    print(k, t[k])

print('\n[브랜드=LG] 흐름·국가별 (전체 / 포함)')
lg = collections.defaultdict(lambda: [0, 0])
for r in new:
    if r['브랜드'] == 'LG':
        lg[(r['흐름'], r['국가'])][0] += 1
        lg[(r['흐름'], r['국가'])][1] += r['모수 포함 여부'] == '포함'
for k in sorted(lg):
    print(k, lg[k])
sys.exit(1 if errs else 0)
