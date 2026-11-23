"""브라우저가 넘겨준 페이지 원본을 raw2/ 에 그대로 저장하고, 다음에 열 주소를 알려 주는 로컬 도우미.

흐름
1. 브라우저가 http://127.0.0.1:8765/next 를 연다. 이 페이지는 queue.txt 에서 아직 저장되지 않은
   첫 작업 이름을 찾아, 그 주소(jobs.json 의 v8.1 접속 후 URL 그대로)로 이동한다.
   이동하기 전에 창 이름(window.name)에 {name, url} 을 적어 둔다.
2. 상품 페이지에서 collector.js 가 원본을 window.__payload 에 담고, 창 이름에 그 내용을 적은 뒤
   http://127.0.0.1:8765/recv?name=<작업 이름> 으로 돌아온다.
3. /recv 페이지가 창 이름에 든 내용을 꺼내 /save 로 보내면, 받은 글자를 바꾸지 않고
   raw2/<작업 이름>.json 으로 쓴다. 같은 이름이 이미 있으면 덮어쓰지 않는다. 그리고 1로 돌아간다.

작업 이름: <종류>-<v8.1 행번호>. 종류 s 는 주소 글자 실험의 바꾼 주소, 나머지는 그 행의 접속 후 URL.
"""

import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

HERE = Path(__file__).resolve().parent
OUT = HERE / "raw2"
OUT.mkdir(exist_ok=True)

PAGE = """<!doctype html><meta charset=utf-8><title>working</title><body><script>
(async()=>{
  const n=new URLSearchParams(location.search).get('name');
  if(n){
    const d=window.name; window.name='';
    if(!d||d.length<1000){document.title='EMPTY '+n;document.body.textContent='EMPTY';return}
    const r=await fetch('/save?name='+n,{method:'POST',body:d}); const t=await r.text();
    if(r.status!==200){document.title='SAVE FAILED '+n+' '+r.status+' '+t;document.body.textContent=document.title;return}
    document.title='saved '+n+' '+t;
  }
  const j=await (await fetch('/nextjob')).json();
  if(!j.name){document.title=(document.title+' | QUEUE DONE');document.body.textContent=document.title;return}
  document.title=document.title+' | next '+j.name;
  window.name=JSON.stringify(j);
  location.href=j.url;
})()
</script>"""


def job_url(name):
    jobs = json.loads((HERE / "jobs.json").read_text(encoding="utf-8"))
    kind, row = name.split("-", 1)
    if kind == "s":
        return next(s["alt"] for s in jobs["slug"] if s["row"] == row)
    return jobs["urls"][row]


def next_job():
    q = [x.strip() for x in (HERE / "queue.txt").read_text(encoding="utf-8").split() if x.strip()]
    for name in q:
        if not (OUT / f"{name}.json").exists():
            return {"name": name, "url": job_url(name)}
    return {}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path in ("/next", "/recv"):
            self._send(200, PAGE.encode(), "text/html; charset=utf-8")
        elif path == "/install":
            # 수집 스크립트(collector.js)와 짧은 호출문을 창 이름에 담아 대상 사이트로 넘긴다.
            to = parse_qs(urlsplit(self.path).query)["to"][0]
            d = json.loads((HERE / "wrappers.json").read_text(encoding="utf-8"))
            d["c"] = (HERE / "collector.js").read_text(encoding="utf-8")
            page = "<!doctype html><meta charset=utf-8><script>window.name=JSON.stringify(%s);location.href=%s</script>" % (
                json.dumps(d).replace("</", "<\\/"), json.dumps(to))
            self._send(200, page.encode(), "text/html; charset=utf-8")
        elif path == "/nextjob":
            self._send(200, json.dumps(next_job()).encode(), "application/json")
        else:
            self._send(200, "\n".join(sorted(p.name for p in OUT.glob("*.json"))).encode())

    def do_POST(self):
        name = parse_qs(urlsplit(self.path).query).get("name", [""])[0]
        data = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", name):
            self._send(400, b"bad name")
        elif (OUT / f"{name}.json").exists():
            self._send(409, b"exists")
        else:
            (OUT / f"{name}.json").write_bytes(data)
            self._send(200, str(len(data)).encode())

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
