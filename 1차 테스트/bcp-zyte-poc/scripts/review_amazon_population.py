#!/usr/bin/env python3
"""Review saved Amazon Italy competitor BCP screens and the ten largest images."""

from __future__ import annotations

import hashlib
import json

from capture_bcp_population import RESULTS


BATCH = RESULTS / "20260928-all-159"
ROWS = set(range(58, 74)) | {78, 79, 81}
NO_WHY = {58, 60}
NO_USP = {58, 60}
TEXT_ONLY_HERO = {78, 79, 81}
SPECIAL_ID8_Y = {58, 66, 67}


def verdict(status: str, reason: str, evidence: dict | None = None) -> dict:
    return {"status": status, "reason": reason, "evidence": evidence or {}}


def main() -> None:
    records = json.loads((BATCH / "manifest.json").read_text())["records"]
    content_path, images_path = BATCH / "본문_항목_AI검수.json", BATCH / "ID8_전체검수.json"
    content = json.loads(content_path.read_text()) if content_path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    images = json.loads(images_path.read_text()) if images_path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    for record in records:
        row = int(record["sourceRow"])
        if row not in ROWS:
            continue
        if record["retailerSlug"] != "amazon-it" or record["pageType"] != "Brand Category Page":
            raise ValueError(f"wrong source identity at row {row}")
        page = BATCH / "pages" / record["pageKey"] / "brand-category"
        raw, state = (page / "raw.html").read_bytes(), (page / "capture-state.json").read_bytes()
        audit = json.loads((BATCH / "id8-audit" / f"{record['pageKey']}.json").read_text())
        top = audit["top10"]
        screenshot = str((page / "screenshot.jpg").relative_to(BATCH))
        evidence = {"screenshot": screenshot, "topImages": [{"index": i["index"], "alt": i.get("alt"), "renderedArea": i["renderedArea"]} for i in top[:5]]}
        results = {
            "ID18": verdict("N" if row in TEXT_ONLY_HERO else "Y",
                            "상단 대표 영역은 제품군 이름만 적힌 단색 이미지여서 제품군 대표 시각 자료가 아님" if row in TEXT_ONLY_HERO else "본문 상단에 해당 브랜드 제품군을 나타내는 큰 시각 영역이 있음", evidence),
            "ID19": verdict("N" if row in NO_WHY else "Y",
                            "상품 목록·개별 모델 설명뿐이며 브랜드 제품군을 선택할 이유를 설명하지 않음" if row in NO_WHY else "브랜드 제품군의 기술·편익을 설명하는 별도 시각·본문 영역이 있음", evidence),
            "ID20": verdict("N" if row in NO_USP else "Y",
                            "상품 카드의 개별 모델 사양 외에 제품군 기술·효익 블록이 없음" if row in NO_USP else "제품군 기술·기능 또는 사용 이점을 소개하는 별도 시각·본문 블록이 있음", evidence),
            "ID23": verdict("N", "브랜드 제품군에 관한 질문과 대응 답변이 본문에 없음", {"screenshot": screenshot}),
        }
        if row not in {66, 67}:
            results["ID21"] = verdict("N", "공통 브랜드 상단 메뉴를 제외하면 본문에 제품 종류별 탐색 블록이 없음", {"screenshot": screenshot})
        content["pages"][record["pageKey"]] = {"sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(), "results": results}
        if row in SPECIAL_ID8_Y:
            # The tiny Prime badges, brand logo, and 1px sprite in Bosch row 58
            # are decoration rather than the page's product imagery.
            selected = [i for i in top if row != 58 or i["index"] in {2, 5, 7, 8, 9, 10}]
            if not selected or any(not str(i.get("alt") or "").strip() for i in selected):
                raise ValueError(f"ID8 target-image selection changed at row {row}")
            id8 = verdict("Y", "본문 대표·기능·상품 이미지의 실제 alt가 해당 이미지와 제품군을 설명함; 순수 로고·배지·1픽셀 장식은 제외", {"selectedIndices": [i["index"] for i in selected], "selectedAlts": [i["alt"] for i in selected]})
        else:
            bad = next((i for i in top if not str(i.get("alt") or "").strip()), None)
            if bad is None:
                # Image present, but the description says only generic people rather than
                # the shown Candy dryer/washer benefits.
                bad = next((i for i in top if str(i.get("alt") or "").startswith(("a man", "a woman", "a child"))), None)
            if bad is None:
                raise ValueError(f"ID8 negative evidence missing at row {row}")
            id8 = verdict("N", "화면 표시 면적 상위 본문 이미지에 빈 alt 또는 브랜드·제품과 무관한 일반 인물 설명이 있음",
                          {"index": bad["index"], "alt": bad.get("alt"), "imageUrl": bad.get("src"), "renderedArea": bad["renderedArea"]})
        images["pages"][record["pageKey"]] = {
            "sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(),
            "sourceCaptureStateSha256": hashlib.sha256(state).hexdigest(), "result": id8,
        }
    content_path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    images_path.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n")
    print(f"Amazon Italy reviewed: {len(ROWS)} competitor BCP rows")


if __name__ == "__main__":
    main()
