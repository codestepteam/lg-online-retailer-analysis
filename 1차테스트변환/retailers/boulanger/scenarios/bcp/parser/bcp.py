"""Self-contained BCP adapter for lg-crawling's parse(bundle) observation contract.

The legacy extraction code is packaged beside this entrypoint. It extracts
candidates only; no candidate is converted into a Y/N verdict here.
"""

from __future__ import annotations

import hashlib
import json
import re
import runpy
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit


class _BodyText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.body = False
        self.omit = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.body = True
        if tag in {"script", "style", "template", "noscript"}:
            self.omit += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "template", "noscript"}:
            self.omit = max(self.omit - 1, 0)
        if tag == "body":
            self.body = False

    def handle_data(self, data):
        if self.body and not self.omit and data.strip():
            self.parts.append(data)


class _Canonical(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag.casefold() != "link":
            return
        values = {key.casefold(): value for key, value in attrs}
        if "canonical" in (values.get("rel") or "").casefold().split():
            self.hrefs.append(values.get("href"))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def _state(html):
    match = re.search(r"(?is)<script[^>]+id=[\"']lg-capture-state[\"'][^>]*>(.*?)</script\s*>", html)
    if not match:
        raise ValueError("BCP capture state is missing from browser HTML")
    result = json.loads(match.group(1))
    if not isinstance(result, dict):
        raise ValueError("BCP capture state is not an object")
    return result


def parse(bundle):
    html = bundle.get("html")
    target = bundle.get("target")
    if not isinstance(html, str) or not isinstance(target, dict):
        raise ValueError("BCP parser requires html and target")
    if target.get("page_type") not in {"bcp", "brand-category"}:
        raise ValueError("BCP parser received another page type")
    retailer, url = target.get("retailer"), target.get("url")
    if not isinstance(retailer, str) or not isinstance(url, str) or not url:
        raise ValueError("BCP target identity is incomplete")
    state = _state(html)
    if state.get("ready") is not True:
        raise ValueError("BCP browser state is not ready")
    response = bundle.get("response") if isinstance(bundle.get("response"), dict) else {}
    final_url = response.get("url") or state.get("url") or url
    source_sha = bundle.get("raw_sha256") or hashlib.sha256(html.encode("utf-8")).hexdigest()
    with TemporaryDirectory(prefix="bcp-parse-") as directory:
        root = Path(directory)
        page = root / "batch" / "pages" / retailer / "brand-category"
        page.mkdir(parents=True)
        (page / "raw.html").write_text(html, encoding="utf-8")
        (page / "capture-state.json").write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        (page / "response.json").write_text(json.dumps({"ok": True, "retailer": retailer,
            "page_type": "brand-category", "requested_url": url, "final_url": final_url}), encoding="utf-8")
        legacy = runpy.run_path(str(Path(__file__).with_name("legacy_bcp_evidence.py")))
        extracted, _ = legacy["parse_page"](page, root / "extracted")
    text = _BodyText()
    text.feed(html)
    canonical = _Canonical()
    canonical.feed(html)
    full_text = " ".join(" ".join(text.parts).split())
    page_text = full_text[:80000]
    metrics = extracted["metrics"]
    initial = state.get("initialMetadata")
    final = state.get("metadata")
    changed = bool(final_url and url.rstrip("/") != str(final_url).rstrip("/"))
    initial_url = str(initial.get("url") or "") if isinstance(initial, dict) else ""
    requested_path, final_path = urlsplit(url).path, urlsplit(str(final_url)).path
    brand = str(target.get("brand") or "")
    alza_alias = (retailer == "alza" and requested_path.split("/")[-1] == final_path.split("/")[-1]
                  and re.search(r"(?<![A-Za-z])" + re.escape(brand) + r"(?![A-Za-z])", final_path, re.I))
    datart_alias = retailer == "datart" and requested_path.replace("/filter/", ".html/filter/") == final_path
    preserved = initial_url.rstrip("/") == url.rstrip("/")
    landing_alias = (initial_url.rstrip("/") == str(final_url).rstrip("/")
                     and (alza_alias or datart_alias))
    selected = initial if changed and (preserved or landing_alias) else final if not changed else None
    selected_canonical = (selected.get("canonical") if changed else canonical.hrefs) if isinstance(selected, dict) else None
    raw_uri = bundle.get("raw_uri")
    screenshot_uri = bundle.get("screenshot_uri")
    refs = [uri for uri in (raw_uri, screenshot_uri) if isinstance(uri, str) and uri]
    copied = {key: target.get(key, "") for key in
              ("url", "retailer", "page_type", "brand", "product_category", "product_name")}
    return {"schema_version": "lg-diagnostic-observation-v1", "target": copied,
            "facts": {"bcp_evidence": {key: value["evidence"] for key, value in metrics.items()},
                      "page_text": page_text, "page_text_truncated": len(full_text) > len(page_text),
                      "initial_metadata": initial,
                      "final_metadata": final, "selected_metadata": selected,
                      "selected_canonical_hrefs": selected_canonical,
                      "source_sha256": source_sha,
                      "screenshot_uri": screenshot_uri, "capture_ready": True},
            "completeness": {"capture": True, "html": True,
                             "initial_metadata": isinstance(state.get("initialMetadata"), dict),
                             "hero_snapshots": bool(state.get("heroEvidence", {}).get("snapshots"))},
            "evidence": refs}
