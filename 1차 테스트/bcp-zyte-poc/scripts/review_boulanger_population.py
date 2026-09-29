#!/usr/bin/env python3
"""Record AI review of current Boulanger brand-category captures."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from parse_bcp_for_jev import parse_page


ROWS = {45, 46, 47, 48, 49, 52, 53}
VERIFIED_GENERIC_DESTINATIONS = {
    "https://www.boulanger.com/c/seche-linge-pompe-a-chaleur": {
        "checkedFromRow": 45, "title": "Sèche-linge pompe à chaleur | efficacité et économie", "h1": "Sèche-linge pompe à chaleur"},
    "https://www.boulanger.com/c/lave-linge-hublot": {
        "checkedFromRow": 46, "title": "Lave-linge Hublot & Frontal : Large Choix au Meilleur Prix | Boulanger", "h1": "Lave linge Hublot"},
    "https://www.boulanger.com/c/petit-refrigerateur": {
        "checkedFromRow": 47, "title": "Mini Frigo - Petit réfrigérateur - Livraison 24h Offerte* | Boulanger", "h1": "Petit Frigo - Mini Frigo"},
}


def result(status: str, reason: str, evidence: dict | None = None) -> dict:
    return {"status": status, "reason": reason, "evidence": evidence or {}}


def run(batch: Path) -> None:
    manifest = json.loads((batch / "manifest.json").read_text())
    path = batch / "본문_항목_AI검수.json"
    reviews = json.loads(path.read_text()) if path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    for record in manifest["records"]:
        row = int(record["sourceRow"])
        if row not in ROWS:
            continue
        if record["retailerSlug"] != "boulanger" or record["pageType"] != "Brand Category Page":
            raise ValueError(f"unexpected Boulanger identity in row {row}")
        key = record["pageKey"]
        page = batch / "pages" / key / "brand-category"
        data, _ = parse_page(page, str(record["brand"]), str(record["subcategory"] or ""))
        brand = str(record["brand"])
        texts = [block for block in data["blocks"] if brand.casefold() in block["text"].casefold()
                 and len(block["text"]) > 180 and len(block["links"]) < 5]
        editorial = [block for block in texts if block["attributes"].get("id") == "product-list__header"
                     or block["source_order"] > max(0, data["blocks"][-1]["source_order"] - 200)]
        if not editorial:
            raise ValueError(f"row {row} brand editorial block not located")
        qa = next((block for block in editorial if "?" in block["text"] and len(block["text"].split("?", 1)[1].strip()) > 30), None)
        if not qa:
            raise ValueError(f"row {row} question-answer wording needs manual review")
        nav = next((block for block in data["blocks"] if block["attributes"].get("id") == "child-categories"), None)
        if not nav or not nav["links"]:
            raise ValueError(f"row {row} child categories not found")
        first = nav["links"][0]
        destination = VERIFIED_GENERIC_DESTINATIONS.get(first["url"])
        if not destination:
            raise ValueError(f"row {row} first category URL is not one of the checked generic destinations")
        results = {
            "ID18": result("N", "상단의 가로 마케팅 이미지는 Boulanger 공통 판촉이며 해당 브랜드·제품군 대표 배너가 아님", {"captureScreenshot": str((page / "screenshot.jpg").relative_to(batch))}),
            "ID19": result("Y", "브랜드를 선택할 이유와 제품군 장점이 본문 소개·하단 설명에 적혀 있음", {"editorialBlockIds": [block["block_id"] for block in editorial[:3]], "excerpt": editorial[0]["text"][:450]}),
            "ID20": result("N", "기술 이름이 소개·질문답변 문장에는 있으나 별도의 제품군 핵심 USP 블록은 확인되지 않음", {"editorialBlockIds": [block["block_id"] for block in editorial[:3]]}),
            "ID21": result("N", f"카테고리 카드 '{first['text']}' 클릭 주소가 {brand} 제품군이 아닌 일반 카테고리로 열림", {"sourceBlockId": nav["block_id"], "checkedUrl": first["url"], "destination": destination}),
            "ID23": result("Y", "브랜드·제품군에 관한 질문형 문장과 이어지는 답변이 같은 본문 영역에 있음", {"blockId": qa["block_id"], "excerpt": qa["text"][:600]}),
        }
        reviews["pages"][key] = {"sourceRawHtmlSha256": hashlib.sha256((page / "raw.html").read_bytes()).hexdigest(), "results": results}
    path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n")
    print(f"Boulanger reviewed: {len(ROWS)} BCP rows; {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    args = parser.parse_args()
    run(args.batch.resolve())


if __name__ == "__main__":
    main()
