"""Falabella 시험 3쌍(6개 주소)을 유료 수집 서비스로 두 번씩, 합계 12회 호출한다. 자동 재시도 없음.
요청 내용은 앞서 미리 보기(raw/paid-pilot-request-preview.json)에 저장된 것과 글자까지 같다.
--run 을 붙여야 실제로 호출한다. 차단 응답이 나오면 그 자리에서 멈춘다.
결과: raw2/z<회차>-<행번호>.json (본 수집과 같은 형식), raw2/z<회차>-<행번호>.response.json (응답 전체), screenshots2/z<회차>-<행번호>.jpg
"""
import base64, json, os, re, sys, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw2"

def key():
    if os.getenv("ZYTE_API_KEY"): return os.environ["ZYTE_API_KEY"]
    for line in (HERE.parents[1] / ".env").read_text().splitlines():
        m = re.fullmatch(r"\s*(?:export\s+)?ZYTE_API_KEY\s*=\s*(.+?)\s*", line)
        if m: return m[1].strip("'\x22")
    raise RuntimeError("키 없음")

def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

preview = [p for p in json.loads((HERE / "raw/paid-pilot-request-preview.json").read_text()) if "falabella" in p["request"]["url"]]
jobs = json.loads((HERE / "jobs.json").read_text(encoding="utf-8"))
assert len(preview) == 12
for p in preview:
    assert p["request"]["url"] == jobs["urls"][p["row"]]
    assert set(p["request"]) == {"url", "browserHtml", "screenshot", "screenshotOptions", "session"}
order = []
for p in preview:
    if p["row"] not in order: order.append(p["row"])
preview = sorted(preview, key=lambda p: (p["attempt"], order.index(p["row"])))
if "--run" not in sys.argv:
    for p in preview: print("미리 보기", p["attempt"], p["row"], p["request"]["url"][-60:])
    print("호출 예정", len(preview), "회. 실제 호출 없음"); sys.exit()
token = base64.b64encode((key() + ":").encode()).decode()
for p in preview:
    name = f"z{p['attempt']}-{p['row']}"
    if (RAW / f"{name}.response.json").exists():
        print(name, "이미 있음"); continue
    started = now()
    req = urllib.request.Request("https://api.zyte.com/v1/extract", data=json.dumps(p["request"]).encode(),
                                 headers={"Authorization": "Basic " + token, "Content-Type": "application/json"})
    try: resp = urllib.request.urlopen(req, timeout=150)
    except urllib.error.HTTPError as e: resp = e
    with resp:
        data = resp.read(); api_status = resp.status
    (RAW / f"{name}.response.json").write_bytes(data)
    obj = json.loads(data)
    html = obj.get("browserHtml") or ""
    if obj.get("screenshot"):
        (HERE / "screenshots2" / f"{name}.jpg").write_bytes(base64.b64decode(obj["screenshot"]))
    title = (re.search(r"<title[^>]*>([^<]*)", html) or [None, ""])[1]
    payload = {"name": name, "requested_url": p["request"]["url"], "final_url": obj.get("url") or p["request"]["url"], "title": title,
               "http_status": obj.get("statusCode"), "started_utc": started, "collected_utc": now(), "viewport": None, "scroll_height": None,
               "user_agent": "", "notes": [f"api_status {api_status}", "tool zyte"], "html": html, "shadows": [], "frames": []}
    (RAW / f"{name}.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    blocked = api_status != 200 or obj.get("statusCode") in (401, 403, 429) or re.search("bloqueado|captcha|Un paso m|Just a moment|Cloudflare", title or "", re.I)
    print(name, "api", api_status, "page", obj.get("statusCode"), "html", len(html), "|", (title or "")[:60], "| 차단" if blocked else "")
    if blocked:
        print("차단 또는 오류 응답. 여기서 멈춤."); sys.exit(1)
