"""내장 브라우저와 주소 목록, 결과를 주고받는 로컬 수신기. 127.0.0.1에서만 열린다.

실행: python3 receiver.py <작업 폴더>
  - 작업 폴더에 list_<이름>.json(주소 또는 id 목록)을 넣어 둔다.
  - GET  /go?name=<이름>&to=<사이트 첫 화면 주소>
        남은 목록을 주소 # 뒤에 붙여 그 사이트로 보낸다(사이트 보안 설정 때문에 브라우저에서 이 수신기로 fetch를 보낼 수 없어서다).
        <이름>.json에 이미 받은 항목(ok 또는 name이 있는 것)은 빼고 보낸다.
  - POST /submit?name=<이름>   (form 필드 data에 JSON)
        브라우저가 form으로 보낸 결과를 <이름>.json에 덧붙여 저장한다. form 제출은 화면 이동이라 그 탭의 스크립트는 끝난다.
"""
import json
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

FOLDER = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8765


def saved(name):
    path = FOLDER / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def key_of(item):
    return item.get("url") or item.get("id") or item.get("path")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        name, target = query["name"][0], query["to"][0]
        done = {key_of(item) for item in saved(name) if item.get("ok") or item.get("name") or item.get("notfound")}
        # 목록은 경로나 id만 담고 결과는 전체 주소를 담으므로 끝부분이 같으면 받은 것으로 본다
        todo = [item for item in json.loads((FOLDER / f"list_{name}.json").read_text(encoding="utf-8"))
                if not any(str(key).endswith(str(item)) for key in done)]
        self.send_response(302)
        self.send_header("Location", target.rstrip("/") + "/#list=" + urllib.parse.quote(json.dumps(todo)))
        self.end_headers()

    def do_POST(self):
        name = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)["name"][0]
        raw = self.rfile.read(int(self.headers["Content-Length"])).decode("utf-8")
        data = json.loads(urllib.parse.parse_qs(raw)["data"][0])
        rows = saved(name) + (data if isinstance(data, list) else data.get("results", []))
        (FOLDER / f"{name}.json").write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        body = f"<html><body>{name}: 받은 {len(rows)}건 저장</body></html>".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"수신기: http://127.0.0.1:{PORT} 작업 폴더 {FOLDER.resolve()}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
