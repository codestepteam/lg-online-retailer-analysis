"""스크린샷을 12장씩 한 장에 모아(쌍이 위아래로 오게) 눈으로 훑어보기 쉽게 만든다. 각 그림 위에 행번호와 values.csv의 상품명, 가격을 적는다."""
import csv, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
vals = list(csv.DictReader((HERE / "values.csv").open(encoding="utf-8-sig", newline="")))
shots = HERE / "screenshots"
if not (shots / "m-7975.jpg").exists(): shots = HERE / "screenshots2"
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
W, H, LAB = 480, 324, 34
per = 12  # 6쌍
for s in range(0, len(vals), per):
    chunk = vals[s:s + per]
    sheet = Image.new("RGB", (W * 6, (H + LAB) * 2), "white")
    d = ImageDraw.Draw(sheet)
    for i, v in enumerate(chunk):
        col, row = i // 2, i % 2
        x, y = col * W, row * (H + LAB)
        d.text((x + 4, y + 2), f"pair {v['쌍 번호']} row {v['v8.1 행번호']} | {v['11. 표시 가격'][:40]}", fill="black", font=font)
        d.text((x + 4, y + 17), v["5. 상품명"][:74], fill=(0, 0, 160), font=font)
        f = shots / Path(v["스크린샷 파일"]).name if v["스크린샷 파일"] else None
        if f and f.exists():
            im = Image.open(f).convert("RGB"); im = im.crop((0, 0, im.size[0], min(im.size[1], int(im.size[0] * H / W)))); sheet.paste(im.resize((W, H)), (x, y + LAB))  # 전체 페이지 그림의 맨 윗부분
        d.rectangle([x, y, x + W - 1, y + H + LAB - 1], outline=(150, 150, 150))
    sheet.save(out / f"sheet_{s // per + 1:02d}.jpg", quality=80)
print("sheets", (len(vals) + per - 1) // per)
