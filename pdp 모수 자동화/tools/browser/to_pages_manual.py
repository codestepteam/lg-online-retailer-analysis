"""magalu_pages.js 결과(receiver.py가 저장한 JSON)를 S3 수동 보완표로 바꾸고, Zyte를 부르지 않고 S3 결과 파일을 다시 만든다.

실행(pdp 모수 자동화 폴더에서):
  python3 tools/browser/to_pages_manual.py --month 2026-11 --results <작업 폴더>/magalu.json

- 페이지마다 상품명, 판매자 문구, 판매 불가 표시만 담은 작은 HTML(runs/<월>/html/manual_magalu_<해시>.html.gz)을 만든다.
  S4 magalu 규칙은 이 HTML의 'Vendido por …' 문구로 판매자를 읽는다.
- 정가 없는 화면은 판매자 뒤에 'Preço'(가격) 표가 붙어 판매자 이름에 섞이므로 떼어 낸다.
- 상태: 사이트 404/410은 없음(404), 나머지는 정상. Magalu는 품절 표시 규칙이 없어 Produto indisponível도 정상으로 둔다(11월과 같음).
- runs/<월>/judgments/pages_manual.csv를 새로 쓴다(기존 행은 지워지므로 다른 리테일러 수동 행이 있으면 먼저 합쳐 둔다).
"""
import argparse
import csv
import gzip
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
import s3_pages as s3  # noqa: E402
from common import ResumeLog, RunPaths, load_config, read_csv  # noqa: E402

COLUMNS = ["요청URL", "상태", "제목", "실제URL", "HTML파일"]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--month", required=True)
    parser.add_argument("--results", required=True, help="magalu_pages.js 결과 JSON(receiver.py 저장본)")
    args = parser.parse_args()
    run = RunPaths(args.month)
    records = {r["url"]: r for r in json.loads(Path(args.results).read_text(encoding="utf-8")) if r.get("ok")}
    rows = []
    for url, r in records.items():
        name = "manual_magalu_" + hashlib.sha1(url.encode()).hexdigest()[:16] + ".html.gz"
        sold = re.sub(r"\s+Preço(?=\s+R\$)", "", r["sold"])
        body = (f"<html><head><title>{html.escape(r['title'])}</title></head><body><p>{html.escape(sold)}</p>"
                + ("<p>Produto indisponível</p>" if r.get("unavail") else "") + "</body></html>")
        (run.sub("html") / name).write_bytes(gzip.compress(body.encode("utf-8")))
        status = f"없음({r['code']})" if r["code"] in (404, 410) else s3.NORMAL
        final = (r.get("final") or url).replace("://www.magazineluiza.com.br", "://magazineluiza.com.br")
        rows.append({"요청URL": url, "상태": status, "제목": r["title"], "실제URL": final, "HTML파일": name})
    path = run.sub("judgments") / s3.MANUAL_NAME
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    common = load_config(run, "retailer_rules")["common"]
    planned = s3.plan_pages(read_csv(run.sub("judgments") / "step1.csv")[1], load_config(run, "targets")["targets"],
                            common["page_status"], common["page_fetch"], s3.fallback_shops(load_config(run, "osm_query")))
    log = ResumeLog(run.sub("logs") / s3.LOG_NAME, "url")
    pending = s3.write_outputs(run, s3.apply_manual(s3.build_pages(planned, log), rows))
    print(f"수동 행 {len(rows)}건 → {path}, S3 수동 확인 남은 것 {len(pending)}건")


if __name__ == "__main__":
    main()
