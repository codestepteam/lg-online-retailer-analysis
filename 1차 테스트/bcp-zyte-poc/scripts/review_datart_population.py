#!/usr/bin/env python3
"""Record inspected Datart BCP judgments against immutable capture hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from parse_bcp_for_jev import parse_page


ROWS = {*range(23, 38), 42}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result(status: str, reason: str, evidence: dict | None = None) -> dict:
    return {"status": status, "reason": reason, "evidence": evidence or {}}


def run(batch: Path) -> None:
    manifest = json.loads((batch / "manifest.json").read_text())
    review_path, image_path = batch / "본문_항목_AI검수.json", batch / "ID8_전체검수.json"
    reviews = json.loads(review_path.read_text()) if review_path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    images = json.loads(image_path.read_text()) if image_path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    for record in manifest["records"]:
        row = int(record["sourceRow"])
        if row not in ROWS:
            continue
        if record["retailerSlug"] != "datart" or record["pageType"] != "Brand Category Page":
            raise ValueError(f"unexpected source identity in row {row}")
        key = record["pageKey"]
        page = batch / "pages" / key / "brand-category"
        raw = page / "raw.html"
        data, _ = parse_page(page, str(record["brand"]), str(record["subcategory"] or ""))
        body_blocks = [block for block in data["blocks"] if "category-description" in str(block.get("attributes"))]
        if any(str(record["brand"]).casefold() in block["text"].casefold() for block in body_blocks):
            raise ValueError(f"row {row} has brand-specific category description; manual review required")
        nav_blocks = [block for block in data["blocks"] if "subcategory-box-list" in str(block.get("attributes"))]
        if nav_blocks and row != 42:
            raise ValueError(f"row {row} has a subcategory box; manual review required")
        if row == 42 and any("Samsung" in block["text"] for block in nav_blocks):
            raise ValueError("Samsung dryer subcategory links require manual destination review")
        audit = json.loads((batch / "id8-audit" / f"{key}.json").read_text())
        selected = [item for item in audit["top10"] if item["scopeSuggestion"] == "포함"
                    and item["scopeReason"] == "제품 카드 이미지"]
        if not selected or any(str(record["brand"]).casefold() not in str(item.get("alt") or "").casefold() for item in selected):
            raise ValueError(f"row {row} ID8 product alt is not clearly brand-related")
        # Rows with fewer than ten product images show shared footer/app images
        # after the product cards. Those are outside this brand-category metric.
        images["pages"][key] = {"sourceRawHtmlSha256": digest(raw),
                                 "sourceCaptureStateSha256": digest(page / "capture-state.json"),
                                 "result": result("Y", f"화면 면적 상위 본문 상품 이미지 {len(selected)}개에 {record['brand']} 제품명·모델 설명 alt가 있음; 공통 사이트 배너·꼬리말 이미지는 제외",
                                                  {"selectedImageIndices": [item["index"] for item in selected],
                                                   "selectedAlts": [item["alt"] for item in selected],
                                                   "excludedSharedFooterOrPromo": audit["selectedCount"] - len(selected)})}
        generic_note = ("제품군 일반 설명은 있으나 브랜드를 언급하지 않음" if body_blocks else "브랜드별 본문 설명 영역이 없음")
        reviews["pages"][key] = {"sourceRawHtmlSha256": digest(raw), "results": {
            "ID18": result("N", "상단 브랜드·제품군 대표 이미지 배너가 없음; 보이는 큰 배너는 Datart 공통 판촉 영역", {"reviewedScreenshot": str((page / "screenshot.jpg").relative_to(batch))}),
            "ID19": result("N", f"브랜드 선택 이유를 설명하는 독립 영역이 없음; {generic_note}", {"descriptionBlockIds": [block["block_id"] for block in body_blocks]}),
            "ID20": result("N", "브랜드 제품군의 기술·효익을 설명하는 별도 영역이 없음; 상품 카드의 모델별 설명은 제외"),
            "ID21": result("N", "브랜드 제품군 하위 카테고리 탐색 블록이 없음; 일반 필터·사이트 메뉴는 제외", {"subcategoryBlockIds": [block["block_id"] for block in nav_blocks]}),
            "ID23": result("N", "현재 본문에서 해당 브랜드·제품군의 질문과 대응 답변을 확인하지 못함"),
        }}
    review_path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n")
    image_path.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n")
    print(f"Datart reviewed: {len(ROWS)} BCP rows; {review_path}; {image_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    args = parser.parse_args()
    run(args.batch.resolve())


if __name__ == "__main__":
    main()
