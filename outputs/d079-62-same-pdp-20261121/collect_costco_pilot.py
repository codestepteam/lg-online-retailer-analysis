"""Run the approved Costco pilot, once per previewed request, without automatic retries."""

import argparse
import base64
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from lxml import html

from select_rows import OUT, select


RAW = OUT / "raw"


def now():
    return datetime.now(timezone.utc).isoformat()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def exact_requests():
    preview = json.loads((RAW / "paid-pilot-request-preview.json").read_text())
    source = {r["행번호"]: r for p in select()["pairs"] if p["pilot"] for r in p["rows"]}
    subset = [p for p in preview if source[p["row"]]["리테일러"] == "COSTCO"]
    assert len(subset) == 12 and len({(p["row"], p["attempt"]) for p in subset}) == 12
    for p in subset:
        req = p["request"]
        assert req["url"] == source[p["row"]]["접속 후 URL"]
        assert urlsplit(req["url"]).hostname == "www.costco.ca" and req["geolocation"] == "CA"
        assert set(req) == {"url", "browserHtml", "screenshot", "screenshotOptions", "geolocation", "session"}
        assert req["screenshot"] and req["browserHtml"] and req["screenshotOptions"] == {"fullPage": False}
    return subset


def key():
    if os.getenv("ZYTE_API_KEY"):
        return os.environ["ZYTE_API_KEY"]
    for line in (OUT.parents[1] / ".env").read_text().splitlines():
        m = re.fullmatch(r"\s*(?:export\s+)?ZYTE_API_KEY\s*=\s*(.+?)\s*", line)
        if m:
            return m[1].strip("'\x22")
    raise RuntimeError("Missing Zyte extract key")


def send(p, token):
    stem = f"zyte-{p['attempt']}-{p['row']}"
    path = RAW / f"{stem}.meta.json"
    if path.exists():
        old = json.loads(path.read_text())
        if old.get("state") == "received":
            return
        raise RuntimeError(f"{stem} has a prior attempt; inspect its evidence before continuing")
    meta = {"row": p["row"], "attempt": p["attempt"], "pair": p["pair"], "url": p["request"]["url"],
            "started": now(), "state": "attempted"}
    with path.open("x") as f:
        json.dump(meta, f)
    req = urllib.request.Request("https://api.zyte.com/v1/extract", data=json.dumps(p["request"]).encode(),
                                 headers={"Authorization": "Basic " + token, "Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(req, timeout=150)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        data = response.read()
        meta["api_status"] = response.status
        meta["service_headers"] = {k: v for k, v in response.headers.items()
                                   if k.lower().startswith(("zyte-", "x-zyte", "x-crawlera", "scrapy-"))
                                   or k.lower() in {"request-id", "x-request-id", "date"}}
    (RAW / f"{stem}.response.json").write_bytes(data)
    obj = json.loads(data)
    meta.update({"at": now(), "landed": obj.get("url"), "page_status": obj.get("statusCode")})
    document = obj.get("browserHtml")
    if document:
        (RAW / f"{stem}.html").write_text(document, encoding="utf-8")
    if obj.get("screenshot"):
        image = base64.b64decode(obj["screenshot"], validate=True)
        ext = "png" if image.startswith(b"\x89PNG") else "jpg"
        target = OUT / "screenshots" / f"{stem}.{ext}"
        target.write_bytes(image)
        meta["screenshot"] = target.name
    page = html.fromstring(document) if document else None
    heading = " ".join(page.xpath("//title/text()|//h1//text()")) if page is not None else ""
    blocked = (meta["page_status"] in (401, 403, 429)
               or re.search("captcha|verify (you are|that you are) human|access denied|just a moment|are you a robot|access has been blocked", heading, re.I))
    meta["state"] = "blocked" if blocked else ("received" if meta["api_status"] == 200 else "api-error")
    dump(path, meta)
    print(stem, meta["api_status"], meta["page_status"], meta["state"], flush=True)
    if meta["state"] != "received":
        raise SystemExit(f"Stopped after {stem}. See saved response.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    planned = exact_requests()
    if args.run:
        token = base64.b64encode((key() + ":").encode()).decode()
        for request in planned:
            send(request, token)
    else:
        print(f"Offline preview: {len(planned)} Costco requests, no requests sent")
