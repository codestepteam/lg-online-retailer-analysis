#!/usr/bin/env python3
"""Compress saved BCP text and image evidence into a page-by-page review aid."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from parse_bcp_for_jev import parse_page


CHROME = re.compile(r"breadcrumb|filter|sort|footer|header|menu|basket|cart|rating|review|product-card|product_item|productgrid|product-list|product_list|top-10", re.I)
TOPIC = re.compile(r"technolog|innov|avantage|benefit|v[ýy]hod|why|warum|waarom|por qu|perch[ée]|pourquoi|faq|questions|preguntas|vraag|domande|fr[åa]gor|\?", re.I)


def content_candidates(blocks: list[dict], brand: str) -> list[dict]:
    scored = []
    seen = set()
    for block in blocks:
        value = re.sub(r"\s+", " ", str(block.get("text") or "")).strip()
        if not 80 <= len(value) <= 4000 or block.get("hidden_hint") or len(block.get("links", [])) > 8:
            continue
        context = " ".join(str(part.get("attributes") or "") for part in block.get("ancestor_context", []))
        context += " " + str(block.get("attributes") or "")
        if CHROME.search(context):
            continue
        key = value[:250]
        if key in seen:
            continue
        seen.add(key)
        score = int(bool(re.search(r"(?<![A-Za-z])" + re.escape(brand) + r"(?![A-Za-z])", value, re.I))) * 3
        score += int(bool(TOPIC.search(value))) * 2
        score += int(len(block.get("links", [])) == 0)
        score += int(bool(block.get("heading_texts")))
        scored.append((score, block["source_order"], {"blockId": block["block_id"], "line": block["source_line"],
                                                        "path": block["source_path"], "text": value[:1800],
                                                        "imageAlts": [image.get("alt_raw") for image in block.get("images", [])[:4]],
                                                        "linkCount": len(block.get("links", []))}))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in scored[:30]]


def run(batch: Path) -> None:
    manifest = json.loads((batch / "manifest.json").read_text())
    historical_path = batch / "과거_판정_비교자료.json"
    historical = {int(item["sourceWorkbookRow"]): item["earlierResults"] for item in
                  json.loads(historical_path.read_text())["pages"]} if historical_path.is_file() else {}
    output = []
    for record in manifest["records"]:
        if record["pageType"] != "Brand Category Page" or record["collectionStatus"] not in ("captured", "seeded", "reused"):
            continue
        page = batch / "pages" / record["pageKey"] / "brand-category"
        data, _ = parse_page(page, str(record["brand"]), str(record["subcategory"] or ""))
        images = [item for item in data["image_evidence"]["captured_images"]
                  if item.get("visible") is True and item.get("loaded") is True]
        images.sort(key=lambda item: float(item.get("renderedArea") or 0), reverse=True)
        output.append({"sourceWorkbookRow": record["sourceRow"], "pageKey": record["pageKey"],
                       "retailer": record["retailerSlug"], "brand": record["brand"],
                       "category": record["subcategory"], "url": record["url"],
                       "title": data["page"]["title"], "blockCount": len(data["blocks"]),
                       "quality": data["quality"]["capture_issues"],
                       "topImages": [{key: item.get(key) for key in ("src", "alt", "renderedArea", "index")} for item in images[:15]],
                       "contentCandidates": content_candidates(data["blocks"], str(record["brand"])),
                       "historicalComparison": [{key: entry.get(key) for key in ("metricId", "recordedLabel", "recordedReason", "sourceSheetRow")}
                                                for entry in historical.get(int(record["sourceRow"]), [])]})
    path = batch / "본문_검토용_압축자료.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path, len(output))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    args = parser.parse_args()
    run(args.batch.resolve())


if __name__ == "__main__":
    main()
