"""v5의 HU/NL 포함 546주소를 재검사해 v6를 준비한다. 기본 실행은 무료 미리보기다.

--execute: 승인 후 주소별 Zyte browserHtml 1회(재시도 없음).
--build: 저장 HTML만 재판정하고 검증 완료 시 v6를 생성한다(외부 호출 없음).
"""
import argparse
import base64
import csv
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.parse import urlparse
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PIPELINE = ROOT / "pdp 모수 자동화/pipeline"
sys.path.insert(0, str(PIPELINE))
from s4_sellers import judge_page
from rules.sellers.base import main_heading

FINAL = ROOT / "pdp 모수 추출/최종_20261029"
SOURCE = FINAL / "PDP모수_공유용_v5_독일MediaMarkt13건제외반영_25개국_35개리테일러_전체판정_55997행_20261106.csv"
V6 = FINAL / "PDP모수_공유용_v6_헝가리네덜란드MediaMarkt규칙반영_25개국_35개리테일러_전체판정_55997행_20261110.csv"
CONFIG = ROOT / "pdp 모수 자동화/runs/2026-11/config/retailer_rules.json"
SCOPE = {("Hungary", "Mediamarkt"), ("Netherlands", "MEDIAMARKT")}
PLAN, SNAPSHOT, LOG = HERE / "plan.json", HERE / "rules_snapshot.json", HERE / "requests.jsonl"
AUDIT, CHANGES, FAILURES = HERE / "PDP재확인.csv", HERE / "변경대상.csv", HERE / "실패목록.csv"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def write_csv(path, columns, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def source_rows():
    columns, rows = read_csv(SOURCE)
    selected = [r for r in rows if (r["국가"], r["리테일러"]) in SCOPE and r["모수 포함 여부"] == "포함"]
    assert len(rows) == 55_997 and len(columns) == 26
    assert Counter(r["국가"] for r in selected) == {"Hungary": 268, "Netherlands": 278}
    assert len({r["확인 요청 URL"] for r in selected}) == len(selected) == 546
    return columns, rows, selected


def prepare():
    _, _, selected = source_rows()
    if PLAN.exists():
        validate_plan()
        return json.loads(PLAN.read_text())
    SNAPSHOT.write_text(CONFIG.read_text())
    plan = {"source": str(SOURCE.relative_to(ROOT)), "source_sha256": digest(SOURCE),
            "rules_sha256": digest(SNAPSHOT), "code_sha256": code_digest(),
            "calls": 546, "counts": dict(Counter(r["국가"] for r in selected)),
            "payload_example": {"url": selected[0]["확인 요청 URL"], "browserHtml": True},
            "retries": 0, "cost_usd_base_range": [0.55146, 8.77968],
            "pricing_source": "https://www.zyte.com/pricing/", "pricing_checked_on": "2026-11-10",
            "targets": [{"row": r["행번호"], "country": r["국가"], "retailer": r["리테일러"], "url": r["확인 요청 URL"]} for r in selected]}
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    return plan


def code_digest():
    files = [PIPELINE / "s4_sellers.py", *sorted((PIPELINE / "rules/sellers").glob("*.py"))]
    return hashlib.sha256("\n".join(f"{p.name}:{digest(p)}" for p in files).encode()).hexdigest()


def validate_plan():
    plan = json.loads(PLAN.read_text())
    assert digest(SOURCE) == plan["source_sha256"], "v5 source changed"
    assert digest(SNAPSHOT) == plan["rules_sha256"], "rule snapshot changed"
    assert code_digest() == plan["code_sha256"], "parser code changed; review plan before proceeding"
    _, _, selected = source_rows()
    assert [r["확인 요청 URL"] for r in selected] == [t["url"] for t in plan["targets"]]
    return plan


def api_key():
    key = os.environ.get("ZYTE_API_KEY", "").strip()
    if not key:
        env = ROOT / ".env"
        if env.exists():
            found = re.search(r"^ZYTE_API_KEY\s*=\s*(.*)$", env.read_text(), re.M)
            key = found.group(1).strip().strip("\"'") if found else ""
    if not key:
        raise RuntimeError("ZYTE_API_KEY is not configured")
    return key


def html_path(url):
    return HERE / "html" / (hashlib.sha256(url.encode()).hexdigest()[:20] + ".html.gz")


def fetch(target, key):
    record = dict(target, checked_at=datetime.now(timezone.utc).isoformat(), ok=False)
    auth = base64.b64encode((key + ":").encode()).decode()
    request = Request("https://api.zyte.com/v1/extract", data=json.dumps({"url": target["url"], "browserHtml": True}).encode(),
                      headers={"Content-Type": "application/json", "Authorization": "Basic " + auth})
    try:
        with urlopen(request, timeout=150) as response:
            result = json.load(response)
        page = result.get("browserHtml", "")
        record["final_url"] = result.get("url", "")
        if not page:
            raise ValueError("empty browserHtml")
        html_path(target["url"]).write_bytes(gzip.compress(page.encode()))
        record.update(ok=True, html_sha256=hashlib.sha256(page.encode()).hexdigest(), bytes=len(page.encode()))
    except Exception as error:
        # API 인증 헤더·키·응답 본문은 로그에 보관하지 않는다.
        record["error"] = f"{type(error).__name__}: {str(error)[:160]}"
    return record


def execute():
    plan = validate_plan()
    records = [json.loads(line) for line in LOG.read_text().splitlines()] if LOG.exists() else []
    assert len({r["row"] for r in records}) == len(records), "duplicate attempts"
    assert {r["row"] for r in records} <= {r["row"] for r in plan["targets"]}
    attempted = {r["row"] for r in records}
    pending = [t for t in plan["targets"] if t["row"] not in attempted]
    if not pending:
        print("No additional calls; every URL already attempted.")
        return
    key = api_key()
    (HERE / "html").mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool, LOG.open("a") as stream:
        jobs = [pool.submit(fetch, target, key) for target in pending]
        for number, future in enumerate(as_completed(jobs), 1):
            record = future.result()
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            stream.flush()
            if number % 25 == 0 or number == len(jobs):
                print(f"attempted {len(attempted) + number}/546", flush=True)


def evaluate(target, record, rules):
    result = dict(target, checked_at=record.get("checked_at", ""), final_url=record.get("final_url", ""), title="", seller="", kind="", status="확인불가", reason="")
    if not record.get("ok"):
        result["reason"] = record.get("error", "수집 기록 없음")
        return result
    page = gzip.decompress(html_path(target["url"]).read_bytes()).decode()
    assert hashlib.sha256(page.encode()).hexdigest() == record["html_sha256"]
    result["title"] = main_heading(page)[0]
    if not result["title"] or re.search(r"captcha|access denied|just a moment", result["title"], re.I):
        result["reason"] = "본 상품 제목 없음 또는 차단 화면"
        return result
    if urlparse(record["final_url"]).hostname != urlparse(target["url"]).hostname:
        result["reason"] = "다른 사이트로 이동"
        return result
    item = {"country": target["country"], "retailer": target["retailer"], "url": target["url"], "title": result["title"]}
    seller, kind, evidence = judge_page(item, page, rules, {})
    result.update(seller=seller, kind=kind, reason=evidence)
    if kind == "직판":
        result["status"] = "유지"
    elif kind in ("외부판매자", "브랜드공식점", "리퍼·중고"):
        result["status"] = "제외"
    return result


def apply_results(columns, source, reviews):
    """검증된 두 나라 포함 행만 바꾸고 원본 행·열·나머지 값은 보존한다."""
    assert len({r["row"] for r in reviews}) == len(reviews)
    by_id = {r["row"]: r for r in reviews}
    assert set(by_id) == {r["행번호"] for r in source if (r["국가"], r["리테일러"]) in SCOPE and r["모수 포함 여부"] == "포함"}
    assert all(r["status"] in ("유지", "제외") for r in reviews), "unverified review prevents v6"
    output = [dict(r) for r in source]
    for row in output:
        review = by_id.get(row["행번호"])
        if review is None or review["status"] != "제외":
            continue
        assert (row["국가"], row["리테일러"]) in SCOPE and row["모수 포함 여부"] == "포함"
        row.update({"모수 포함 여부": "제외", "제외단계": "③리리부", "제외사유": review["reason"],
                    "판매자": review["seller"] or row["판매자"], "판매자구분": review["kind"], "판매자근거": review["reason"], "접속 후 URL": review["final_url"]})
        row["메모"] = "; ".join(x for x in (row["메모"], f'D124: {review["checked_at"]} PDP 제목·본 상품 판매자 재확인; 원본 기준일·상품명 보존') if x)
    assert len(output) == len(source) and all(list(r) == columns for r in output)
    assert sum(a != b for a, b in zip(source, output)) == sum(r["status"] == "제외" for r in reviews)
    return output


def build():
    plan = validate_plan()
    if not LOG.exists():
        raise RuntimeError("수집 전이므로 v6를 만들 수 없습니다")
    records = [json.loads(line) for line in LOG.read_text().splitlines()]
    assert len(records) == len({r["row"] for r in records}), "duplicate attempts"
    by_id = {r["row"]: r for r in records}
    assert set(by_id) <= {t["row"] for t in plan["targets"]}
    rules = json.loads(SNAPSHOT.read_text())["sellers"]
    reviews = [evaluate(t, by_id.get(t["row"], {}), rules) for t in plan["targets"]]
    columns = list(reviews[0])
    write_csv(AUDIT, columns, reviews)
    write_csv(CHANGES, columns, [r for r in reviews if r["status"] == "제외"])
    failed = [r for r in reviews if r["status"] == "확인불가"]
    write_csv(FAILURES, columns, failed)
    if failed:
        raise RuntimeError(f"미확인 {len(failed)}건; 실패목록을 확인해야 하므로 v6 미생성")
    columns, source, _ = source_rows()
    output = apply_results(columns, source, reviews)
    assert not V6.exists(), "v6 already exists; refusing to overwrite"
    write_csv(V6, columns, output)
    saved_columns, saved = read_csv(V6)
    assert saved_columns == columns and saved == output
    summary = {"total": len(output), "before": dict(Counter(r["모수 포함 여부"] for r in source)),
               "after": dict(Counter(r["모수 포함 여부"] for r in output)),
               "changed": sum(a != b for a, b in zip(source, output)), "failures": 0, "source_sha256": digest(SOURCE), "v6_sha256": digest(V6)}
    (HERE / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true", help="승인 후: 유료 546회, 재시도 없음")
    mode.add_argument("--build", action="store_true", help="저장 HTML 판정·v6 생성(유료 호출 없음)")
    args = parser.parse_args()
    if args.execute:
        execute()
    elif args.build:
        build()
    else:
        plan = prepare()
        print(json.dumps({k: v for k, v in plan.items() if k != "targets"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
