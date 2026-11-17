"""검사 D: v0.3의 기존 칸이 v0.2와 같은지 (열만 밀렸는지), 새 칸이 약속대로인지."""
import re, sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter as L, column_index_from_string as CI
A = load_workbook(sys.argv[1]); B = load_workbook(sys.argv[2])   # A = v0.2, B = v0.3
def ins_map(inserts):   # inserts: [(v0.2 열 번호 앞에, 칸 수)]  -> v0.2 열 -> v0.3 열
    return lambda c: c + sum(n for at, n in inserts if c >= at)
maps = {}
for t in ("8월_국가", "10월_국가"): maps[t] = ins_map([(12, 2), (26, 2)])
for t in ("8월_국가x리테일러", "10월_국가x리테일러"): maps[t] = ins_map([(13, 2), (27, 2)])
for m in "8", "10", "11": maps[f"{m}월_국가x리테일러x카테고리"] = ins_map([(13 + 14 * k, 2) for k in range(6)])
maps["※ 25개국 Summary"] = ins_map([(9, 6)])
REF = re.compile(r"(?:'([^']+)'!)?(\$?[A-Z]{1,3}\$?\d+)(?::(\$?[A-Z]{1,3}\$?\d+))?")
ONE = re.compile(r"(\$?)([A-Z]{1,3})(\$?)(\d+)")
def remap(f, here):
    def one(ref, sh):
        m = ONE.fullmatch(ref)
        return m.group(1) + L(maps[sh](CI(m.group(2)))) + m.group(3) + m.group(4)
    def sub(m):
        sh = m.group(1) or here
        out = (f"'{m.group(1)}'!" if m.group(1) else "") + one(m.group(2), sh)
        return out + (":" + one(m.group(3), sh) if m.group(3) else "")
    return REF.sub(sub, f)
n = bad = 0; mapped = {}; fmt_bad = []
for ws in A:
    if ws.title not in maps: continue
    wb = B[ws.title]; f = maps[ws.title]
    for row in ws.iter_rows():
        for c in row:
            nc = f(c.column); mapped.setdefault(ws.title, set()).add((c.row, nc))
            v = c.value; w = wb.cell(row=c.row, column=nc).value
            if isinstance(v, str) and v.startswith("="): v = remap(v, ws.title)
            n += 1
            if v != w:
                bad += 1
                if bad <= 10: print("  다름", ws.title, c.coordinate, "->", L(nc), repr(v)[:90], "|", repr(w)[:90])
            if c.style_id != wb.cell(row=c.row, column=nc).style_id and c.number_format != wb.cell(row=c.row, column=nc).number_format:
                fmt_bad.append((ws.title, c.coordinate))
    mc = sorted(str(x) for x in ws.merged_cells.ranges)
print(f"기존 칸 대조: {n}칸, 다름 {bad}, 숫자 서식 다름 {len(fmt_bad)}", fmt_bad[:5])
# 새 칸
new_ok = new_n = 0
def chk(cond, msg):
    global new_ok, new_n
    new_n += 1
    if cond: new_ok += 1
    elif new_n - new_ok <= 10: print("  새 칸 문제", msg)
for t, f in maps.items():
    ws = B[t]
    for r in range(1, ws.max_row + 1):
        for c in range(1, ws.max_column + 1):
            if (r, c) in mapped.get(t, set()): continue
            v = ws.cell(row=r, column=c).value
            if v is None: continue
            if t.startswith("※"):
                continue
            head = 3 if "카테고리" not in t else 4
            if r == head: chk(v in ("Search SOV", "Category SOV"), (t, r, c, v)); continue
            name = ws.cell(row=head, column=c).value
            # 같은 묶음의 ID4 / Dashboard Only 칸: 둘 다 +5
            tgt = c + 5
            exp_head = "ID4" if name == "Search SOV" else "Dashboard Only"
            chk(ws.cell(row=head, column=tgt).value == exp_head, (t, c, "옆 칸 이름"))
            first_agg = 5 if head == 3 else 6
            if r < first_agg + 6:
                chk(isinstance(v, str) and (v.startswith('=IF(COUNT(' + L(c)) ), (t, r, c, v))
            else:
                ref = f"{L(tgt)}{r}"
                chk(v == f'=IF(ISNUMBER({ref}),{ref},"")', (t, r, c, v))
print(f"새 칸(Summary 외) 검사: {new_n}칸 중 맞음 {new_ok}")
S = B["※ 25개국 Summary"]
print("Summary 4줄:", [ (L(c), S.cell(row=4, column=c).value) for c in range(2, 30) if S.cell(row=4, column=c).value])
print("Summary 5줄:", "".join(f"{L(c)}={S.cell(row=5, column=c).value} " for c in range(3, 30) if S.cell(row=5, column=c).value))
print("Summary 병합:", sorted(str(x) for x in S.merged_cells.ranges))
for c in ("I12", "L12", "K12", "N12", "X12", "AA12", "I6", "X11", "Z12", "AC12"):
    print("  ", c, S[c].value)
