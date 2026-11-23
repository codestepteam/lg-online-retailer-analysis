"""values.csv 로 엑셀 파일과 두레이 글 초안을 만든다.

엑셀의 값은 모두 values.csv(= raw 원본에서 스크립트로 뽑은 값)와 v8.1 원본에서 온다. 손으로 적는 값은 없다.
"""
import csv
import json
import sys
from pathlib import Path

from openpyxl import Workbook
from PIL import Image as PILImage
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.hyperlink import Hyperlink

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from extract_values import FIELDS, NONE  # noqa: E402
import judge as J  # noqa: E402

XLSX = HERE / "Costco_Falabella_주소글자만다른_62쌍_124행_PDP대조_20261121.xlsx"
DRAFT = HERE / "두레이_글_초안.md"
SHOTS = HERE / "screenshots"
if not (SHOTS / "m-7975.jpg").exists():
    SHOTS = HERE / "screenshots2"  # 정리 전 임시 위치
TEXTS = json.loads((HERE / "texts.json").read_text(encoding="utf-8"))

MAIN_COLS = (["쌍 번호", "리테일러", "국가", "브랜드", "제품코드", "v8.1 행번호", "모수 포함 여부", "제외사유", "접속 후 URL",
              "주소에서 서로 다른 부분", "주소 끝 PDP 식별자"] + [l for _, l in FIELDS]
             + ["수집 시각(한국 시각)", "쌍 판정", "다른 항목", "스크린샷"])

HEAD_FILL = PatternFill("solid", fgColor="1F3864")
HEAD_FONT = Font(bold=True, color="FFFFFF")
BAND = [PatternFill("solid", fgColor="FFFFFF"), PatternFill("solid", fgColor="EEF3FA")]
RED = PatternFill("solid", fgColor="F8CBAD")
YELLOW = PatternFill("solid", fgColor="FFE699")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
IMG_W = 800      # 엑셀에 넣는 그림 폭(픽셀). 원본 크기 그림은 screenshots 폴더에 있다
CHUNK = 2000     # 긴 그림은 이 높이로 잘라 위에서 아래로 이어 붙여 넣는다
ROW_PX = 20      # 스크린샷 시트의 한 줄 높이(픽셀)
EMBED = HERE / "_embed"  # 엑셀에 넣을 축소 그림(900x600)을 두는 임시 폴더


def header(ws, cols, row=1):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.fill, cell.font, cell.border = HEAD_FILL, HEAD_FONT, BORDER
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[row].height = 34


def widths(ws, spec):
    for i, w in enumerate(spec, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def text_sheet(ws, lines, width=120):
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = width
    r = 1
    for line in lines:
        if isinstance(line, str):
            line = [line]
        if len(line) == 1:
            c = ws.cell(row=r, column=1, value=line[0])
            if line[0] and not line[0].startswith(" "):
                c.font = Font(bold=True, size=12)
        else:
            ws.cell(row=r, column=1, value=line[0]).font = Font(bold=True)
            c = ws.cell(row=r, column=2, value=line[1])
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(row=r, column=1).alignment = Alignment(vertical="top", wrap_text=True)
        r += 1
    return r


def verdict_fill(v, band):
    return RED if v == "다름" else YELLOW if v in ("확인 못 함", J.NA) else band


def pair_rows(ws, records, cols, shot_anchor=None, start=2):
    """한 줄이 한 행. 쌍마다 번갈아 배경색, 다름과 확인 못 함은 색으로 표시."""
    r = start
    for i, rec in enumerate(records):
        band = BAND[(i // 2) % 2]
        fill = verdict_fill(rec["쌍 판정"], band)
        for c, name in enumerate(cols, 1):
            if name == "스크린샷":
                cell = ws.cell(row=r, column=c, value="전체 페이지 보기")
                if shot_anchor and rec["v8.1 행번호"] in shot_anchor:
                    # 같은 파일 안의 다른 시트로 가는 링크는 "위치(location)"로 적어야 Excel이 이동한다.
                    cell.hyperlink = Hyperlink(ref=cell.coordinate, location=f"'스크린샷'!{shot_anchor[rec['v8.1 행번호']]}", display="전체 페이지 보기")
                    cell.font = Font(color="0563C1", underline="single")
                else:
                    cell.value = "그림 없음"
            else:
                val = rec[name]
                cell = ws.cell(row=r, column=c, value=val)
                if name == "접속 후 URL":
                    cell.hyperlink = val
                    cell.font = Font(color="0563C1", underline="single")
            cell.fill, cell.border = fill, BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=False)
        r += 1
    return r


def build(records, summary):
    wb = Workbook()
    # 1 요약
    ws = wb.active
    ws.title = "요약"
    text_sheet(ws, summary)

    # 3 스크린샷 (먼저 자리 계산)
    wsS = wb.create_sheet("스크린샷")
    wsS.column_dimensions["A"].width = 3
    wsS.column_dimensions["B"].width = 116
    wsS.column_dimensions["C"].width = 3
    wsS.column_dimensions["D"].width = 116
    anchor = {}
    r = 1
    wsS.cell(row=r, column=2, value=TEXTS["shots_note"]).alignment = Alignment(wrap_text=True, vertical="top")
    wsS.row_dimensions[r].height = 48
    r += 2
    for i in range(0, len(records), 2):
        a, b = records[i], records[i + 1]
        t = wsS.cell(row=r, column=2, value=f"쌍 {a['쌍 번호']} | {a['리테일러']} | 판정: {a['쌍 판정']}")
        t.font = Font(bold=True, size=12)
        t.fill = verdict_fill(a["쌍 판정"], PatternFill("solid", fgColor="D9E1F2"))
        tallest = 0
        for col, rec in ((2, a), (4, b)):
            anchor[rec["v8.1 행번호"]] = f"{get_column_letter(col)}{r + 1}"
            wsS.cell(row=r + 1, column=col, value=f"v8.1 행번호 {rec['v8.1 행번호']} ({rec['역할']}, {rec['모수 포함 여부']})").font = Font(bold=True)
            u = wsS.cell(row=r + 2, column=col, value=rec["접속 후 URL"])
            u.hyperlink = rec["접속 후 URL"]
            u.font = Font(color="0563C1", underline="single", size=9)
            wsS.cell(row=r + 3, column=col, value=f"수집 시각(한국 시각): {rec['수집 시각(한국 시각)'].split(' / ')[0]}")
            f = SHOTS / Path(rec["스크린샷 파일"]).name if rec["스크린샷 파일"] else None
            if f and f.exists():
                EMBED.mkdir(exist_ok=True)
                full = PILImage.open(f).convert("RGB")
                w, h = full.size
                H = int(h * IMG_W / w)
                small = full.resize((IMG_W, H))
                tallest = max(tallest, H)
                for ci, y in enumerate(range(0, H, CHUNK)):
                    part = EMBED / f"{f.stem}.{ci:02d}.jpg"
                    small.crop((0, y, IMG_W, min(H, y + CHUNK))).save(part, quality=65)
                    img = XLImage(str(part))
                    wsS.add_image(img, f"{get_column_letter(col)}{r + 4 + y // ROW_PX}")
            else:
                wsS.cell(row=r + 4, column=col, value="그림 없음 (화면을 읽지 못함)")
        rows_needed = tallest // ROW_PX + 2
        for rr in range(r + 4, r + 4 + rows_needed):
            wsS.row_dimensions[rr].height = ROW_PX * 0.75
        r += 4 + rows_needed + 1

    # 2 124행
    ws2 = wb.create_sheet("124행", 1)
    header(ws2, MAIN_COLS)
    pair_rows(ws2, records, MAIN_COLS, anchor)
    ws2.freeze_panes = "A2"
    ws2.auto_filter.ref = f"A1:{get_column_letter(len(MAIN_COLS))}{len(records) + 1}"
    widths(ws2, [7, 11, 8, 12, 16, 9, 9, 30, 60, 30, 13] + [22, 14, 40, 30, 40, 34, 40, 38, 34, 20, 18, 40, 50, 36, 34] + [20, 10, 40, 11])

    # 4 검사 방법
    ws4 = wb.create_sheet("검사 방법")
    r = text_sheet(ws4, TEXTS["method_intro"])
    cols = ["번호", "검사 항목", "뜻", "Costco에서 값을 읽은 위치", "Falabella에서 값을 읽은 위치"]
    r += 1
    header(ws4, cols, r)
    for row in TEXTS["method_items"]:
        r += 1
        for c, v in enumerate(row, 1):
            cell = ws4.cell(row=r, column=c, value=v)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = BORDER
    widths(ws4, [24, 28, 46, 60, 60])  # A열은 위쪽 설명 줄의 제목 칸도 겸한다
    r += 2
    for line in TEXTS["method_rules"]:
        if len(line) == 1:
            ws4.cell(row=r, column=1, value=line[0]).font = Font(bold=True, size=12)
        else:
            ws4.cell(row=r, column=1, value=line[0]).font = Font(bold=True)
            ws4.cell(row=r, column=1).alignment = Alignment(vertical="top", wrap_text=True)
            ws4.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
            c = ws4.cell(row=r, column=2, value=line[1])
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws4.row_dimensions[r].height = max(18, 16 * (1 + len(line[1]) // 95))
        r += 1

    wb.save(XLSX)
    return anchor


if __name__ == "__main__":
    print("이 파일은 make_all.py 에서 부른다.")
