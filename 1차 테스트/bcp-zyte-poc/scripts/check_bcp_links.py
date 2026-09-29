#!/usr/bin/env python3
"""Check selected BCP category and product destinations in a Zyte browser session.

The result records exactly which links were checked. A successful HTTP response
alone is not a content verdict; destination title and H1 are retained for review.
"""

from __future__ import annotations

import argparse
from html import unescape
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from capture_bcp_population import ROOT, prepared_recipe
import zyte_capture as zyte


PRODUCT_PATHS = ("/product/", "/products/", "/produkt/", "/produit/", "/prodotto/", "/ref/", "/dp/")
NAV_HREFS = {
    14: ["/kombinovane-lednicky/lg/", "/lednicky-s-mrazakem-dole-kombinovane/lg/", "/lednice-s-mrazakem-nahore/lg/", "/americke-lednice-side-by-side/lg/", "/americke-lednice-s-vyrobnikem-ledu/lg/", "/americke-dvoudverove-lednice/lg/", "/americke-ctyrdverove-lednice/lg/"],
    15: ["/pracky-s-prednim-plnenim/lg/", "/uzke-pracky-slim-45cm/lg/", "/parni-pracky/lg/", "/pracky-se-susickou/lg/", "/set-pracka-a-susicka/lg/"],
    16: ["/susicky-s-tepelnym-cerpadlem/lg/", "/chytre-susicky/lg/", "/pracky-se-susickou/lg/", "/set-pracka-a-susicka/lg/", "/kondenzacni-susicky/lg/"],
    38: ["/kombinovane-lednice-lg.html", "/americke-chladnicky-51579/lg", "/no-frost-lednice-lg.html", "/chytre-lednice-lg.html", "/usporne-lednicky-lg.html", "/lednice-lg-s-vyrobnikem-ledu.html", "/lednice-lg-s-pripojenim-na-vodu.html", "/lednice-lg-s-davkovacem-vody.html", "/lednice-lg-s-displejem.html", "/velke-lednice-lg.html", "/tiche-lednice-lg.html"],
    39: ["/volne-stojici-susicky-lg.html", "/susicky-pro-alergiky-lg.html", "/chytre-susicky-lg.html", "/kondenzacni-susicky-lg.html", "/susicky-s-tepelnym-cerpadlem-lg.html", "/usporne-susicky-lg.html", "/susicky-s-ceskym-panelem-lg.html", "/pracka-a-susicka-61385/lg"],
    94: ["/it/brand/lg/lavatrici/carico-8-kg", "/it/brand/lg/lavatrici/carico-9-kg"],
    112: ["/koelkasten/vrijstaand/amerikaanse-koelkasten/lg", "/koelkasten/vrijstaand/koel-vriescombinaties/lg"],
    126: ["/nl/category/lg-amerikaanse-koelkasten-963.html"],
    127: ["/nl/category/lg-wasmachines-11-kg-3792.html", "/nl/category/lg-wasmachines-8-kg-3790.html", "/nl/category/lg-wasmachines-9-kg-3791.html"],
    142: ["/es/brand/lg-electronics/frigorificos/frigorificos-americanos", "/es/brand/lg-electronics/frigorificos/frigorificos-combinados"],
    143: ["/es/brand/lg-electronics/lavado/lavadoras-secadoras", "/es/brand/lg-electronics/lavado/lavadora-lg-8kg", "/es/brand/lg-electronics/lavado/lavadora-lg-9kg"],
    156: ["/brand/lg/lg-kombinerad-tvattmaskin-torktumlare", "/brand/lg/lg-torktumlare"],
}


def selected_links(batch: Path, record: dict[str, object]) -> list[dict[str, str]]:
    key = record["pageKey"]
    evidence = json.loads((batch / "parsed" / key / "bcp-evidence.json").read_text())
    metrics = evidence["metrics"]
    source_host = urlsplit(str(record["url"])).hostname
    selected: list[dict[str, str]] = []
    raw_html = (batch / "pages" / key / "brand-category" / "raw.html").read_text(errors="replace")
    for path in NAV_HREFS.get(int(record["sourceRow"]), []):
        matches = [x for x in metrics["ID21"]["evidence"]["linkCandidates"] if path in x.get("href", "")]
        if matches:
            selected.append({"kind": "navigator", "label": str(matches[0].get("text") or ""), "url": str(matches[0]["href"])})
        elif path in raw_html:
            raw_links = [unescape(value) for value in re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)', raw_html, re.I)]
            actual = next((urljoin(str(record["url"]), value) for value in raw_links if path in value), None)
            if actual:
                selected.append({"kind": "navigator", "label": path, "url": actual})
    seen: set[str] = set()
    for x in metrics["ID22"]["evidence"]["productLinkCandidates"]:
        url = str(x.get("href") or "")
        label = str(x.get("text") or "")
        parsed = urlsplit(url)
        alza_product = source_host == "www.alza.cz" and bool(re.search(r"/lg-[^/]+-d\d+\.htm$", parsed.path))
        datart_product = source_host == "www.datart.cz" and "-lg-" in parsed.path and not parsed.path.endswith("-lg.html")
        if parsed.hostname != source_host or not (alza_product or datart_product or any(part in parsed.path for part in PRODUCT_PATHS)):
            continue
        if not re.search(r"\bLG\b", label, re.I):
            continue
        base = url.split("?", 1)[0].split("#", 1)[0]
        if base in seen:
            continue
        seen.add(base)
        selected.append({"kind": "product", "label": label[:180], "url": url})
        if len(seen) >= 2:
            break
    return selected


def browser_script(links: list[dict[str, str]]) -> str:
    payload = json.dumps(links, ensure_ascii=False)
    return f"""(async () => {{
      const links = {payload};
      const results = [];
      for (const link of links) {{
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 15000);
        try {{
          const response = await fetch(link.url, {{credentials:'include',redirect:'follow',signal:controller.signal}});
          const html = await response.text();
          const doc = new DOMParser().parseFromString(html,'text/html');
          results.push({{...link,status:response.status,finalUrl:response.url,
            title:(doc.head.querySelector('title')?.textContent||'').trim().slice(0,250),
            h1:(doc.querySelector('h1')?.textContent||'').trim().slice(0,250),
            bodyLength:(doc.body?.textContent||'').length}});
        }} catch (error) {{ results.push({{...link,error:String(error)}}); }}
        clearTimeout(timer);
      }}
      const node = document.createElement('script');node.id='lg-link-check';node.type='application/json';
      node.textContent=JSON.stringify(results);document.body.appendChild(node);
    }})()"""


def check_page(batch: Path, record: dict[str, object], api_key: str) -> tuple[str, dict[str, object]]:
    key = str(record["pageKey"])
    selected = selected_links(batch, record)
    if not selected:
        return key, {"pageKey": key, "requestedUrl": record["url"], "targets": [], "results": [], "error": "no targets selected"}
    _, request = prepared_recipe(record)
    request["screenshot"] = False
    request.pop("screenshotOptions", None)
    script = browser_script(selected)
    if len(script.encode()) > 6000:
        raise ValueError(f"link-check script exceeds Zyte limit: {key}")
    request["actions"].append({"action": "evaluate", "source": script})
    try:
        response = zyte._post_json(api_key, request, 180, 1)
        html = str(response.get("browserHtml") or "")
        match = re.search(r'<script id="lg-link-check" type="application/json">(.*?)</script>', html, re.S)
        if not match:
            raise ValueError("link-check result missing from browser HTML")
        results = json.loads(match.group(1))
        return key, {"pageKey": key, "requestedUrl": record["url"], "targets": selected, "results": results,
                     "source": "Zyte browser same-origin fetch", "sourcePageStatus": response.get("statusCode")}
    except Exception as exc:
        return key, {"pageKey": key, "requestedUrl": record["url"], "targets": selected, "results": [], "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--only-row", type=int, action="append")
    args = parser.parse_args()
    batch = args.batch.resolve()
    manifest = json.loads((batch / "manifest.json").read_text())
    records = [r for r in manifest["records"] if not args.only_row or int(r["sourceRow"]) in args.only_row]
    api_key = zyte._load_env(ROOT)
    if not api_key:
        raise RuntimeError("ZYTE_API_KEY is missing")
    target = batch / "link-check"
    target.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(check_page, batch, record, api_key) for record in records]
        for future in as_completed(futures):
            key, result = future.result()
            (target / f"{key}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            statuses = [x.get("status", x.get("error")) for x in result["results"]]
            print(key, len(result["targets"]), statuses, result.get("error", ""), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"BCP link check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
