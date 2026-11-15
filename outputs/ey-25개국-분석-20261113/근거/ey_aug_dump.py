import sys, json
from openpyxl import load_workbook
wb = load_workbook(sys.argv[1], read_only=True, data_only=True)
print(wb.sheetnames)
ws = wb["Summary Detail"]
rows = []
for r in ws.iter_rows(min_row=1, max_row=160, max_col=90, values_only=True):
    rows.append(list(r))
json.dump(rows, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, default=str)
print(ws.max_row, ws.max_column)
