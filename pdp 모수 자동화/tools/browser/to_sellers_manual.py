"""lazada_sellers.js 결과(receiver.py가 저장한 JSON)를 S4 판매자 수동 보완표(sellers_manual.csv)로 바꾼다.

실행(pdp 모수 자동화 폴더에서, S4를 한 번 돌린 뒤):
  python3 tools/browser/to_sellers_manual.py --month 2026-11 --results <작업 폴더>/lazada_th.json <작업 폴더>/lazada_sg.json \
      --previous runs/2026-11_연습/judgments/sellers_manual.csv
  그다음 run.py s4 --month 2026-11 --force 로 S4를 다시 돌린다.

- 대상: sellers.csv에서 LAZADA이고 판매자구분이 확인불가인 행. 같은 나라와 페이지 id(주소의 -i숫자)로 결과를 잇는다.
- 판매자구분은 판매자 이름으로 정한다(판매자 번호로 잇지 않는다, K2): 10월 연결표(config/lazada_sellers.json)와
  --previous로 준 지난 sellers_manual.csv에서 사람이 판정한 같은 이름의 구분을 쓴다.
  처음 보는 이름은 외부판매자로 두고 근거에 '확인 필요'를 적는다. 끝나면 처음 보는 이름 목록을 출력한다.
- runs/<월>/judgments/sellers_manual.csv를 새로 쓴다(기존 행은 지워지므로 다른 리테일러 수동 행이 있으면 먼저 합쳐 둔다).
"""
import argparse
import collections
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COLUMNS = ["요청URL", "판매자", "판매자구분", "근거"]


def country_of(url):
    return "Singapore" if "lazada.sg" in url else "Thailand"


def known_kinds(run_dir, previous):
    kinds = collections.defaultdict(collections.Counter)
    for key, value in json.loads((run_dir / "config/lazada_sellers.json").read_text(encoding="utf-8"))["sellers"].items():
        kinds[(key.split("|")[0], value["seller"].strip().lower())][value["kind"]] += 1
    for path in previous:
        for row in csv.DictReader(open(path, encoding="utf-8-sig")):
            kinds[(country_of(row["요청URL"]), row["판매자"].strip().lower())][row["판매자구분"]] += 1
    return {key: counter.most_common(1)[0][0] for key, counter in kinds.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--month", required=True)
    parser.add_argument("--results", nargs="+", required=True, help="lazada_sellers.js 결과 JSON들(파일 이름에 sg가 있으면 싱가포르)")
    parser.add_argument("--previous", nargs="*", default=[], help="지난 회차 sellers_manual.csv(이름→구분을 빌려 옴)")
    parser.add_argument("--date", default="", help="근거에 적을 날짜(예: 11-24)")
    args = parser.parse_args()
    run_dir = ROOT / "runs" / args.month
    kinds = known_kinds(run_dir, args.previous)
    pages = {}
    for path in args.results:
        country = "Singapore" if "sg" in Path(path).name.lower() else "Thailand"
        for r in json.loads(Path(path).read_text(encoding="utf-8")):
            pages[(country, str(r["id"]))] = r
    sellers = list(csv.DictReader(open(run_dir / "judgments/sellers.csv", encoding="utf-8-sig")))
    rows, new_names, missing = [], collections.Counter(), []
    for s in sellers:
        if s["리테일러"] != "LAZADA" or s["판매자구분"] != "확인불가":
            continue
        page_id = re.search(r"-i(\d+)", s["요청URL"].split("___")[0]).group(1)
        r = pages.get((s["국가"], page_id))
        if not r:
            missing.append(s["요청URL"])
            continue
        if r.get("notfound"):
            rows.append({"요청URL": s["요청URL"], "판매자": "", "판매자구분": "확인불가",
                         "근거": f"{args.date} 내장 브라우저: 상품 화면 없음({r.get('title', '')[:40]})"})
            continue
        shop = (re.search(r"/shop/([^/?]+)", r.get("href") or "") or [None, ""])[1]
        kind = kinds.get((s["국가"], r["name"].strip().lower()))
        if kind:
            note = "; 지난 회차에 같은 이름을 사람이 판정한 구분"
        else:
            kind, note = "외부판매자", "; 처음 보는 판매자 이름이라 외부판매자로 둠(확인 필요)"
            new_names[(s["국가"], r["name"])] += 1
        rows.append({"요청URL": s["요청URL"], "판매자": r["name"], "판매자구분": kind,
                     "근거": f"{args.date} 내장 브라우저 상품 화면 판매자 칸: {r['name']} (상점 /shop/{shop}/)" + note})
    out = run_dir / "judgments/sellers_manual.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{out}: {len(rows)}행 {dict(collections.Counter(r['판매자구분'] for r in rows))}, 결과 없는 행 {len(missing)}")
    print("처음 보는 판매자:", new_names.most_common())


if __name__ == "__main__":
    main()
