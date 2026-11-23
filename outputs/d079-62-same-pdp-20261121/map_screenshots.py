"""브라우저가 저장한 스크린샷 파일을 수집 시각으로 각 작업에 이어 screenshots2/<작업 이름>.jpg 로 복사한다.

규칙: 한 번에 한 주소만 수집하고 그때 스크린샷을 한 장 찍었다. 스크린샷 파일 이름에는 찍은 시각(1/1000초)이 들어 있다.
작업 A의 스크린샷은 "A의 원본을 담은 시각" 이후, "그다음 작업이 시작된 시각" 이전에 찍힌 원래 크기(가로 800) 그림이다.
그 구간에 그림이 없으면 잇지 않고 알린다. 여러 장이면(같은 화면을 다시 찍은 경우) 먼저 찍힌 그림을 쓰고 알린다.
"""
import json, re, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
RAW, OUT = HERE / "raw2", HERE / "screenshots2"
SHOTS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / ".claude/projects/-Users-codestepseunghee-codestep-lg-online-retailer-analysis/e642cf82-9a93-463c-94a2-bc0c4287c9ee/tool-results"

def ms(iso):
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() * 1000)

def main():
    OUT.mkdir(exist_ok=True)
    jobs = []
    for f in RAW.glob("*.json"):
        with f.open(encoding="utf-8") as fh:
            head = fh.read(3000)
        s = re.search(r'"started_utc":"([^"]+)"', head).group(1)
        c = re.search(r'"collected_utc":"([^"]+)"', head).group(1)
        jobs.append((ms(s), ms(c), f.stem))
    jobs.sort()
    shots = []
    for f in SHOTS.glob("mcp-Claude_Browser-blob-*.jpg"):
        t = int(re.search(r"blob-(\d+)-", f.name).group(1))
        shots.append((t, f))
    shots.sort()
    bad, multi, done = [], [], 0
    mapping = {}
    for i, (s, c, name) in enumerate(jobs):
        end = jobs[i + 1][0] if i + 1 < len(jobs) else c + 120000
        cand = [f for t, f in shots if c <= t < end and Image.open(f).size[0] >= 800]
        if len(cand) == 0:
            bad.append((name, 0))
            continue
        if len(cand) > 1:  # 같은 화면을 두 번 찍은 경우(호출을 다시 한 경우)는 먼저 찍힌 그림을 쓴다
            multi.append((name, len(cand)))
        dst = OUT / f"{name}.jpg"
        if not dst.exists():
            shutil.copyfile(cand[0], dst)
        mapping[name] = {"source": cand[0].name, "shot_ms": int(re.search(r"blob-(\d+)-", cand[0].name).group(1)), "collected_ms": c, "next_started_ms": end}
        done += 1
    (OUT / "_mapping.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")
    print("이은 스크린샷", done, "| 잇지 못한 작업", bad, "| 그림이 여러 장이라 첫 장을 쓴 작업", multi)

if __name__ == "__main__":
    main()
