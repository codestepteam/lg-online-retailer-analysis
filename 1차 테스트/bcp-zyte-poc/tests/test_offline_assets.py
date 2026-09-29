#!/usr/bin/env python3
"""One stdlib-only smoke test for the offline asset bundle."""

from __future__ import annotations

import sys
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import offline_assets  # noqa: E402
from offline_assets import FetchResult, _same_document_fragment, capture  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        pages = {
            "/index.html": (
                "text/html",
                b"""<!doctype html><html><head><base href='/'>
                <link rel='stylesheet' href='/styles/main.css'>
                <link rel='stylesheet' href='/fallback.css'>
                <link rel='preload' as='image' imagesrcset='https://remote.invalid/only-preload.png 1x'>
                <meta http-equiv='refresh' content='0;url=/bad'>
                <style>.inline { background: url('/inline.png') }</style></head><body>
                <img class='hero' src='/placeholder.gif' data-src='/hero.png'
                     data-srcset='/hero.png 1x, /hero@2x.png 2x'>
                <img class='scene7' srcset='/scene7/a?op=usm=1.75,0.3,2,0 1x'>
                <svg><use href='/icons.svg#ok'></use></svg>
                <iframe src='/frame.html'></iframe>
                <script src='/hydrate.js'>location='/captcha'</script>
                <template shadowrootmode='open'><img src='/shadow.png'></template>
                <img src='/missing.png'><img src='/html-as-image'><img src='/space name.png'><img src='file:///etc/passwd'></body></html>""",
            ),
            "/styles/main.css": ("text/css", b"@import 'nested.css'; body { background:url('../bg.png') } @font-face { src:url('/font.woff2') }"),
            "/fallback.css": ("text/html", b"<html>direct block</html>"),
            "/styles/nested.css": ("text/css", b"h1 { background: url('/nested.png') }") ,
            "/frame.html": ("text/html", b"<html><head><base href='file:///'></head><body><img src='/frame.png'><style>body{background:url('/frame-bg.png')}</style></body></html>"),
            "/hero.png": ("image/png", b"hero"),
            "/hero@2x.png": ("image/png", b"hero2"),
            "/shadow.png": ("image/png", b"shadow"),
            "/inline.png": ("image/png", b"inline"),
            "/bg.png": ("image/png", b"bg"),
            "/nested.png": ("image/png", b"nested"),
            "/frame.png": ("image/png", b"frame"),
            "/frame-bg.png": ("image/png", b"frame-bg"),
            "/font.woff2": ("font/woff2", b"font"),
            "/scene7/a": ("image/jpeg", b"scene7"),
            "/html-as-image": ("text/html", b"<html>blocked</html>"),
            "/space name.png": ("image/png", b"space"),
            "/icons.svg": ("image/svg+xml", b"<svg><symbol id='ok'><path d='M0 0'/></symbol></svg>"),
        }
        content = pages.get(unquote(self.path.split("?", 1)[0]))
        if content is None:
            self.send_response(404)
            self.end_headers()
            return
        content_type, body = content
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args: object) -> None:
        return


def main() -> None:
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        original_zyte = offline_assets.Fetcher._get_via_zyte

        def stub_zyte(self, url: str) -> FetchResult:
            if url.endswith("/fallback.css"):
                return FetchResult(b"body { color: red }", url, 200, "text/css", 1, source="zyte-http")
            return FetchResult(b"<html>still blocked</html>", url, 200, "text/html", 1, source="zyte-http")

        offline_assets.Fetcher._get_via_zyte = stub_zyte
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "bundle"
            manifest = capture(
                f"http://127.0.0.1:{server.server_port}/index.html",
                output,
                base_url=f"http://127.0.0.1:{server.server_port}/public/source.html",
                timeout=2,
                retries=1,
                zyte_api_key="stub",
            )
            html = (output / "index.html").read_text(encoding="utf-8")
            css = "\n".join(p.read_text(encoding="utf-8") for p in (output / "assets").glob("*.css"))
            assert (output / "page.raw.html").is_file()
            assert (output / "manifest.json").is_file()
            assert "<base" not in html.lower()
            assert "http-equiv=\"refresh\"" not in html.lower()
            assert "<script src=" not in html.lower()
            assert "remote.invalid" not in html
            assert "template shadowrootmode=\"open\"" in html
            assert "frames/iframe-001.html" in html
            assert "url(http" not in css.lower()
            assert manifest["stats"]["asset_count"] >= 10
            assert any(item["kind"] == "image" and item["error"] == "HTTP 404" for item in manifest["failures"])
            assert any("unexpected content-type text/html" in item["error"] for item in manifest["failures"])
            assert sum(item["error"] == "file URL disallowed for remote source" for item in manifest["failures"]) >= 2
            assert not any("/scene7/0.3" in item["url"] or "/scene7/2" in item["url"] for item in manifest["failures"])
            assert any(item["url"].endswith("/fallback.css") and item["source"] == "zyte-http" for item in manifest["assets"])
            assert _same_document_fragment("http://example.test/public/source.html#icon", "http://example.test/public/source.html") == "#icon"
            assert (output / "frames/iframe-001.html").is_file()
    finally:
        if 'original_zyte' in locals():
            offline_assets.Fetcher._get_via_zyte = original_zyte
        server.shutdown()
        thread.join(timeout=2)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "remote-snapshot.html"
        source.write_text('<base href="file:///"><img src="private-never-read"><style>body{background:url(file:///private-style-never-read)}</style>')
        mirror = offline_assets.OfflineCapture(root / "safe-view", base_url="https://example.test/page")
        def deny_prefetch(url):
            raise AssertionError("Remote snapshot attempted a local asset read: " + url)
        mirror.fetcher.get = deny_prefetch
        result = mirror.capture(str(source))
        assert len(result["failures"]) >= 2
    print("offline asset smoke test: ok")


if __name__ == "__main__":
    main()
