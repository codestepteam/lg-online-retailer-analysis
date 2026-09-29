#!/usr/bin/env python3
"""Record AI review of Alza BCP images and editorial blocks in saved captures."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from parse_bcp_for_jev import parse_page


FREEZER_ROWS = {4, 9, 13, 18}
EDITORIAL_ROWS = {2: (13, 23), 3: (13, 14), 5: (12, 15), 6: (13, 17),
                  7: (13, 29), 8: (12, None), 10: (15, 17), 11: (12, 17),
                  12: (13, 11), 17: (12, None), 19: (12, 21), 20: (12, 19)}
ROWS = FREEZER_ROWS | set(EDITORIAL_ROWS)
HERO_ONLY_ROWS = {14}


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
        if record["retailerSlug"] != "alza" or record["pageType"] != "Brand Category Page":
            raise ValueError(f"unexpected Alza identity in row {row}")
        key = record["pageKey"]
        page = batch / "pages" / key / "brand-category"
        data, _ = parse_page(page, str(record["brand"]), str(record["subcategory"] or ""))
        blocks = {block["block_id"]: block for block in data["blocks"]}
        audit = json.loads((batch / "id8-audit" / f"{key}.json").read_text())
        selected = [item for item in audit["top10"] if str(item.get("alt") or "").strip() not in {"Sleva", "AlzaPlus"}]
        if not selected or any(not str(item.get("alt") or "").strip() for item in selected):
            raise ValueError(f"row {row} image alt needs further review")
        if any(item["scopeSuggestion"] == "검토" for item in selected):
            raise ValueError(f"row {row} image scope needs further review")
        images["pages"][key] = {"sourceRawHtmlSha256": digest(page / "raw.html"),
                                 "sourceCaptureStateSha256": digest(page / "capture-state.json"),
                                 "result": result("Y", f"화면 표시 면적 상위 본문 이미지 {len(selected)}개의 alt가 {record['brand']} 제품군·기능 또는 상품 모델을 설명함; 할인·회원 배지는 순수 장식으로 제외",
                                                  {"selectedImageIndices": [item["index"] for item in selected],
                                                   "selectedAlts": [item["alt"] for item in selected]})}
        if row in FREEZER_ROWS:
            decisions = {
                "ID18": result("N", "상단에 해당 브랜드 냉동고의 이미지형 대표 배너가 없음", {"screenshot": str((page / "screenshot.jpg").relative_to(batch))}),
                "ID19": result("N", "본문은 주문·배송 안내와 제품 목록이며 브랜드 선택 이유를 설명하는 영역이 없음", {"contentBlockId": "block-00011"}),
                "ID20": result("N", "브랜드 냉동고의 기술·효익을 설명하는 별도 영역이 없음"),
                "ID23": result("N", "해당 브랜드 냉동고에 대한 질문과 대응 답변이 없음"),
            }
        else:
            usp_number, faq_number = EDITORIAL_ROWS[row]
            usp_id = f"block-{usp_number:05d}"
            faq_id = f"block-{faq_number:05d}" if faq_number else None
            if usp_id not in blocks or len(blocks[usp_id]["text"]) < 100:
                raise ValueError(f"row {row} USP source block changed")
            hero = selected[0]
            if hero["renderedArea"] < 100000:
                raise ValueError(f"row {row} image hero needs visual inspection")
            decisions = {
                "ID18": result("Y", "상단에 해당 브랜드 제품군의 큰 이미지형 대표 영역이 있음", {"topImageIndex": hero["index"], "topImageAlt": hero["alt"], "screenshot": str((page / "screenshot.jpg").relative_to(batch))}),
                "ID19": result("Y", "본문이 해당 브랜드 제품군을 선택할 이유·차별적 편익을 설명함", {"introBlockId": "block-00011", "excerpt": blocks["block-00011"]["text"][:400]}),
                "ID20": result("Y", "별도 본문 영역에서 제품군 기술·기능과 사용자 효익을 설명함", {"blockId": usp_id, "excerpt": blocks[usp_id]["text"][:600]}),
                "ID23": result("Y" if faq_id else "N",
                               "브랜드·제품군 관련 질문과 이어지는 답변이 본문에 있음" if faq_id else "본문에서 해당 브랜드 제품군의 질문·답변 쌍이 확인되지 않음",
                               {"blockId": faq_id, "excerpt": blocks[faq_id]["text"][:450]} if faq_id else {}),
            }
            if faq_id and faq_id not in blocks:
                raise ValueError(f"row {row} FAQ block changed")
        reviews["pages"][key] = {"sourceRawHtmlSha256": digest(page / "raw.html"), "results": decisions}
    # The LG refrigerator page was excluded from the broader Alza editorial
    # review, but its top hero is directly visible in the saved screenshot.
    for record in manifest["records"]:
        row = int(record["sourceRow"])
        if row not in HERO_ONLY_ROWS:
            continue
        if (record["retailerSlug"], record["pageType"], record["brand"], record["subcategory"]) != (
            "alza", "Brand Category Page", "LG", "냉장고"
        ):
            raise ValueError(f"unexpected Alza LG hero identity in row {row}")
        key = record["pageKey"]
        page = batch / "pages" / key / "brand-category"
        audit = json.loads((batch / "id8-audit" / f"{key}.json").read_text())
        hero = next((item for item in audit["top10"] if "LG%20lednice%20BP.jpg" in str(item.get("src"))), None)
        if not hero or not hero.get("visible") or hero.get("renderedArea", 0) < 100000:
            raise ValueError(f"row {row} LG hero evidence changed")
        reviews["pages"][key] = {
            "sourceRawHtmlSha256": digest(page / "raw.html"),
            "sourceScreenshotSha256": digest(page / "screenshot.jpg"),
            "results": {
                "ID18": result(
                    "Y",
                    "저장된 화면의 본문 상단에 LG 냉장고를 소개하는 큰 이미지형 대표 배너가 있음",
                    {
                        "topImageIndex": hero["index"],
                        "topImageAlt": hero["alt"],
                        "screenshot": str((page / "screenshot.jpg").relative_to(batch)),
                    },
                )
            },
        }
    review_path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n")
    image_path.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n")
    print(f"Alza reviewed: {len(ROWS)} BCP rows plus {len(HERO_ONLY_ROWS)} LG hero row; {review_path}; {image_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    args = parser.parse_args()
    run(args.batch.resolve())


if __name__ == "__main__":
    main()
