"""screenshots2/<작업 이름>.partNN.jpg 조각(화면을 한 칸씩 내리며 찍은 것)을 찍힌 위치대로 이어
screenshots2/<작업 이름>.jpg (전체 페이지 한 장)로 만든다. 조각은 지운다."""
import json, sys
from pathlib import Path
from PIL import Image
D = Path(__file__).resolve().parent / (sys.argv[1] if len(sys.argv) > 1 else "screenshots2")
n = 0
for meta in sorted(D.glob("*.full.json")):
    info = json.loads(meta.read_text())
    out = D / f"{info['name']}.jpg"
    if "segs" not in info:
        continue
    segs = info["segs"]
    if out.exists() or not all((D / s["file"]).exists() for s in segs):
        continue
    sheet = Image.new("RGB", (info["width"], info["height"]), "white")
    for s in segs:  # 마지막 조각은 앞 조각과 겹칠 수 있다. 위치대로 덮어 붙이면 된다.
        sheet.paste(Image.open(D / s["file"]).convert("RGB"), (0, s["y"]))
    sheet.save(out, quality=84)
    for s in segs:
        (D / s["file"]).unlink()
    n += 1
print("stitched", n)
