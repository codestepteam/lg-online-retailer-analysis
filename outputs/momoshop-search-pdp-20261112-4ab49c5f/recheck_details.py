"""Preview or recheck outstanding PDP details using one Zyte browser request per job."""

import argparse
import base64
import gzip
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from lxml import html

from population import EVIDENCE, OUT, ROOT, load_evidence, product_key, write_json
from inspect_pdp import parse


ATTEMPTS = OUT / "zyte_attempts"
MAX_CALLS = 335


def pending_jobs():
    jobs = json.loads((OUT / "jobs.json").read_text())
    return [job for job in jobs if not load_evidence(job[0], job[1])[0].get("verified")
            and not (ATTEMPTS / f"{job[0]}-{job[1]}.json").exists()]


def api_key():
    configured = os.environ.get("ZYTE_API_KEY")
    if configured:
        return configured
    for line in (ROOT / ".env").read_text().splitlines():
        name, separator, value = line.strip().removeprefix("export ").partition("=")
        if separator and name.strip() == "ZYTE_API_KEY":
            return value.strip().strip("'\042")
    raise RuntimeError("ZYTE_API_KEY is missing")


def fetch(url, key):
    authorization = base64.b64encode((key + ":").encode()).decode()
    request = Request("https://api.zyte.com/v1/extract",
                      data=json.dumps({"url": url, "browserHtml": True}).encode(),
                      headers={"Authorization": "Basic " + authorization, "Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=85) as response:
            return json.loads(response.read())
    except HTTPError as error:
        return {"error": f"Zyte HTTP {error.code}"}
    except (URLError, TimeoutError, ValueError) as error:
        return {"error": f"Zyte {type(error).__name__}"}


def read_detail(result, kind, identity):
    body = result.get("browserHtml", "").encode()
    if not body or not result.get("url"):
        return {"verified": False, "error": result.get("error", "Zyte 응답에 상세 HTML 없음")}, body
    page = parse(result.get("statusCode"), result["url"], body)
    text = html.fromstring(body).xpath("string(//body)")
    missing = re.search(r"網頁無法顯示|商品目前無展售|此商品已下架|找不到此商品|商品不存在", text)
    try:
        _, _, _, final_identity = product_key(result["url"])
    except ValueError:
        final_identity = ""
    status = result.get("statusCode")
    if kind == "goods":
        valid = status == 200 and page["schema_name"] and (not page["schema_sku"] or str(page["schema_sku"]) == identity)
        absent = not page["schema_name"] and bool(missing) and status in (200, 404, 410)
    else:
        valid = status == 200 and "," in page["meta_keywords"] and "商店" in text
        absent = False
    page["verified"] = bool(final_identity == identity and (valid or absent))
    page["page_missing"] = bool(missing)
    page["error"] = "" if page["verified"] else "상품 식별 또는 상세 화면 확인 실패"
    return page, body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--workers", type=int, default=5)
    args = parser.parse_args()
    sent = len(list(ATTEMPTS.glob("*.json")))
    jobs = pending_jobs()[:max(0, MAX_CALLS - sent)]
    if args.limit is not None:
        jobs = jobs[:max(0, args.limit)]
    print(json.dumps({"planned_requests": len(jobs), "live": args.live}), flush=True)
    if not args.live or not jobs:
        return
    key = api_key()
    ATTEMPTS.mkdir(exist_ok=True)

    def run(job):
        kind, identity, canonical_url, original_url = job
        url = original_url if kind == "goods" else canonical_url
        name = f"{kind}-{identity}"
        with (ATTEMPTS / f"{name}.json").open("x", encoding="utf-8") as attempt:
            json.dump({"url": url, "kind": kind, "key": identity}, attempt)
        try:
            detail, body = read_detail(fetch(url, key), kind, identity)
        except (ValueError, TypeError, KeyError) as error:
            detail, body = {"verified": False, "error": type(error).__name__}, b""
        if body:
            (EVIDENCE / f"{name}.html.gz").write_bytes(gzip.compress(body))
        write_json(EVIDENCE / f"{name}.json", {**detail, "request_url": url, "kind": kind,
                                              "key": identity, "transport": "zyte_browser"})
        return detail["verified"]

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for done, verified in enumerate(pool.map(run, jobs), 1):
            if done % 25 == 0 or not verified or done == len(jobs):
                print(json.dumps({"done": done, "verified": verified, "identity": jobs[done - 1][1]}), flush=True)


if __name__ == "__main__":
    main()
