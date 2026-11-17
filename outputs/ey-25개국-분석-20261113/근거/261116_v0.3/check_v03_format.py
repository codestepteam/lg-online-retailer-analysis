"""v0.3 파일의 칸 겉모양(바탕색, 테두리)이 v0.2와 같은지 검사한다.
보이는 서식 = 칸이 있으면 칸 서식, 없으면 열 전체 서식, 그것도 없으면 기본 서식.
기존 열은 v0.2의 같은 열과, 새 열은 원본 열(Visibility)과 비교한다. 제목 줄 글자는 보지 않는다.
사용법: python check_v03_format.py v0.2.xlsx v0.3.xlsx
"""
import sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter as L
A = load_workbook(sys.argv[1]); B = load_workbook(sys.argv[2])

def look(wb, ws, r, c):
    if (r, c) in ws._cells:
        xf = ws._cells[(r, c)]._style
        fill, border = xf.fillId, xf.borderId
    else:
        xf = None
        for d in ws.column_dimensions.values():   # 열 설정은 여러 열을 한 범위로 묶기도 한다
            if d.min is not None and d.max is not None and d.min <= c <= d.max:
                xf = d._style; break
        fill, border = (xf.fillId, xf.borderId) if xf is not None else (0, 0)
    return (repr(wb._fills[fill]), repr(wb._borders[border]))

def colmap(title, maxc):
    # v0.3 열 -> ("old", v0.2 열) 또는 ("new", 같은 모양이어야 할 v0.3 열)
    if title.endswith("Summary"):
        m = {c: ("old", c) for c in range(1, 9)}
        for k in range(6): m[9 + k] = ("new", 6 + k % 3)
        for c in range(15, maxc + 1): m[c] = ("old", c - 6)
        for k in range(6): m[24 + k] = ("new", 21 + k % 3)
        return m
    if "카테고리" in title: inserts = [(13 + 14 * k, 2) for k in range(6)]
    elif "리테일러" in title: inserts = [(13, 2), (27, 2)]
    else: inserts = [(12, 2), (26, 2)]
    m = {}; c3 = 1; c2 = 1
    pts = dict(inserts)
    while c3 <= maxc:
        if c2 in pts:
            for _ in range(pts.pop(c2)): m[c3] = ("new", None); c3 += 1
            continue
        m[c3] = ("old", c2); c3 += 1; c2 += 1
    # 새 열의 원본 = 바로 앞의 기존 열(Visibility)
    last_old = None
    for c in sorted(m):
        if m[c][0] == "old": last_old = c
        else: m[c] = ("new", last_old)
    return m

bad = 0; total = 0; samples = []
for wa in A.worksheets:
    wb_ = B[wa.title]
    maxc = wb_.max_column + 10; maxr = max(wa.max_row, wb_.max_row) + 60
    m = colmap(wa.title, maxc)
    for r in range(1, maxr + 1):
        for c in range(1, maxc + 1):
            kind, src = m[c]
            got = look(B, wb_, r, c)
            exp = look(A, wa, r, src) if kind == "old" else look(B, wb_, r, src)
            total += 1
            if got != exp:
                bad += 1
                if len(samples) < 10: samples.append((wa.title, f"{L(c)}{r}", kind, L(src)))
    print(wa.title, "열 설정 수", len(wb_.column_dimensions))
print(f"겉모양 비교 {total}칸, 다름 {bad}")
for s in samples: print("  ", s)
