"""Falabella 주소를 유료 수집 서비스로 수집한다. 자동 재시도 없음. --run 이 있어야 실제로 호출한다.

사용: python zyte_falabella.py [--run] <작업 이름> <작업 이름> ...   (예: m-8616 m-8627)
- 인자로 준 순서대로 호출한다. 두 개씩 한 쌍으로 보고 같은 접속 묶음(session)을 쓴다.
- 요청: 화면 크기 1200x800, 페이지 안에서 zyte_page_script.js 실행(끝까지 내리기, 접힌 영역 펼치기, 별도 영역 담기), 그 뒤의 페이지 원본과 화면 그림.
- 결과: raw2/<작업 이름>.json (본 수집과 같은 형식), raw2/<작업 이름>.response.json (응답 전체), screenshots2/<작업 이름>.jpg
"""
import base64, json, os, re, sys, uuid, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw2"
JOBS = json.loads((HERE / "jobs.json").read_text(encoding="utf-8"))
SCRIPT = (HERE / "zyte_page_script.js").read_text(encoding="utf-8")
assert len(SCRIPT) <= 6000
LOG = HERE / "zyte_calls.log"
FULL = "--full" in sys.argv

def key():
    if os.getenv("ZYTE_API_KEY"): return os.environ["ZYTE_API_KEY"]
    for line in (HERE.parents[1] / ".env").read_text().splitlines():
        m = re.fullmatch(r"\s*(?:export\s+)?ZYTE_API_KEY\s*=\s*(.+?)\s*", line)
        if m: return m[1].strip("'\x22")
    raise RuntimeError("키 없음")

def now(): return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def url_of(name):
    kind, row = name.split("-", 1)
    if kind in ("s", "s2"): return next(s["alt"] for s in JOBS["slug"] if s["row"] == row)
    return JOBS["urls"][row]

def request_for(name, session, extra=None):
    req = {"url": url_of(name), "browserHtml": True, "screenshot": True, "screenshotOptions": {"fullPage": False},
           "viewport": {"width": 1200, "height": 800}, "session": {"id": session},
           "actions": [{"action": "evaluate", "source": SCRIPT}]}
    if FULL:  # 전체 페이지 그림: 화면 크기 지정을 빼고(페이지가 그려진 폭 그대로) 페이지 전체를 찍는다
        req["screenshotOptions"] = {"fullPage": True}
        req.pop("viewport")
    req.update(extra or {})
    return req

def call(name, session, token, extra=None):
    if (RAW / f"{name}.response.json").exists():
        print(name, "이미 있음"); return True
    req = request_for(name, session, extra)
    started = now()
    r = urllib.request.Request("https://api.zyte.com/v1/extract", data=json.dumps(req).encode(),
                               headers={"Authorization": "Basic " + token, "Content-Type": "application/json"})
    try: resp = urllib.request.urlopen(r, timeout=200)
    except urllib.error.HTTPError as e: resp = e
    with resp:
        data = resp.read(); api_status = resp.status
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"name": name, "at": started, "api_status": api_status, "bytes": len(data), "session": session}) + "\n")
    obj = json.loads(data)
    if api_status != 200:
        (RAW / f"{name}.error.json").write_bytes(data)
        print(name, "api", api_status, str(obj)[:300]); return False
    (RAW / f"{name}.response.json").write_bytes(data)
    html = obj.get("browserHtml") or ""
    if obj.get("screenshot"):
        (HERE / "screenshots2" / f"{name}.jpg").write_bytes(base64.b64decode(obj["screenshot"]))
    m = re.search(r'<script type="application/json" id="lg-capture">(.*?)</script>', html, re.S)
    cap = json.loads(m.group(1)) if m else {}
    acts = obj.get("actions")
    payload = {"name": name, "requested_url": req["url"], "final_url": cap.get("final_url") or obj.get("url") or req["url"],
               "title": cap.get("title") or "", "http_status": obj.get("statusCode"), "started_utc": cap.get("started_utc") or started,
               "collected_utc": cap.get("collected_utc") or now(), "viewport": cap.get("viewport"), "scroll_height": cap.get("scroll_height"),
               "user_agent": cap.get("user_agent", ""), "notes": (cap.get("notes") or ["page script did not finish"]) + ["imgs_pending 0", "tool paid-service", f"actions {json.dumps(acts)[:200]}"],
               "html": html, "shadows": cap.get("shadows") or [], "frames": cap.get("frames") or []}
    (RAW / f"{name}.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    title = (re.search(r"<title[^>]*>([^<]*)", html) or [None, ""])[1]
    blocked = obj.get("statusCode") in (401, 403, 429) or re.search("bloqueado|captcha|Un paso m|Just a moment|^Cloudflare", title or "", re.I)
    print(name, "page", obj.get("statusCode"), "html", len(html), "cap", bool(cap), cap.get("viewport"), "|", (title or "")[:50], "|", "; ".join(cap.get("notes") or [])[:120], "| 차단" if blocked else "")
    return not blocked

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    extra = json.loads(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--extra=")), "{}"))
    plan = [(n, str(uuid.uuid5(uuid.NAMESPACE_URL, "d079-pair-" + args[i - i % 2] + "-v2"))) for i, n in enumerate(args)]
    if "--run" not in sys.argv:
        for n, s in plan: print("미리 보기", n, s[:8], url_of(n)[-70:])
        print("호출 예정", len(plan), "회. 실제 호출 없음"); sys.exit()
    token = base64.b64encode((key() + ":").encode()).decode()
    for n, s in plan:
        if not call(n, s, token, extra):
            print("차단 또는 오류. 여기서 멈춤."); sys.exit(1)
