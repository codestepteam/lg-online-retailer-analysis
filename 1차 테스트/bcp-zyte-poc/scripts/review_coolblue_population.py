#!/usr/bin/env python3
"""Review current Coolblue competitor BCP content and image descriptions."""

from __future__ import annotations

import hashlib
import json

from lxml import html as lxml_html

from capture_bcp_population import RESULTS


BATCH = RESULTS / "20260928-all-159"
ROWS = {103, 104, 105, 106, 107, 108, 109, 110, 111, 115, 116, 117}
SIMPLE_PLP = {103, 108}
NO_QA = {107}
GENERIC_ALTS = {"Veelgestelde vragen", "Vraag", "Vragen", "Bewaar extra veel boodschappen", "Energieklasse C",
                "Bezorging en installatie van je droger", "Energiezuinig drogen", "Extra zuinig drogen met energieklasse A"}


def verdict(status: str, reason: str, evidence: dict | None = None) -> dict:
    return {"status": status, "reason": reason, "evidence": evidence or {}}


def main() -> None:
    records = json.loads((BATCH / "manifest.json").read_text())["records"]
    content_path = BATCH / "본문_항목_AI검수.json"
    image_path = BATCH / "ID8_전체검수.json"
    content = json.loads(content_path.read_text()) if content_path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    images = json.loads(image_path.read_text()) if image_path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    digest = {int(item["sourceWorkbookRow"]): item for item in json.loads((BATCH / "본문_검토용_압축자료.json").read_text())}
    for record in records:
        row = int(record["sourceRow"])
        if row not in ROWS:
            continue
        if record["retailerSlug"] != "coolblue" or record["pageType"] != "Brand Category Page":
            raise ValueError(f"wrong source identity at row {row}")
        page = BATCH / "pages" / record["pageKey"] / "brand-category"
        raw = (page / "raw.html").read_bytes()
        state = (page / "capture-state.json").read_bytes()
        tree = lxml_html.fromstring(raw)
        brand = str(record["brand"])
        heading_text = [" ".join(" ".join(node.itertext()).split()) for node in tree.xpath("//h2")]
        feature = [item for item in heading_text if brand.casefold() in item.casefold() and any(
            word in item.casefold() for word in ("voordelen", "droogt", "wast", "fresh", "vitafresh", "energ", "bespaar", "care", "iron", "ruimte", "cooling", "max"))]
        if row not in SIMPLE_PLP and not feature and row not in {106, 107, 111}:
            raise ValueError(f"separate product-benefit blocks not found at row {row}")
        question = next((item["text"] for item in digest[row]["contentCandidates"]
                         if "?" in item["text"] and brand.casefold() in item["text"].casefold()
                         and not item["text"].startswith("1 We bezorgen")), "")
        if row not in NO_QA and not question:
            raise ValueError(f"question-answer text not located at row {row}")
        benefit_text = next((item["text"] for item in digest[row]["contentCandidates"]
                             if brand.casefold() in item["text"].casefold()
                             and not item["text"].startswith("1 We bezorgen")
                             and any(word in item["text"].casefold() for word in
                                     ("bespaar", "energie", "droog", "was", "koel", "fresh", "care", "ruimte"))), "")
        if not benefit_text:
            raise ValueError(f"brand/category benefit text not located at row {row}")
        results = {
            "ID18": verdict("N" if row in SIMPLE_PLP else "Y",
                            "상단은 제목·제품 목록이고 이미지형 대표 영역이 없음" if row in SIMPLE_PLP else "상단 브랜드 제품군 소개에 이미지형 대표 영역과 제품군 카드가 있음",
                            {"screenshot": str((page / "screenshot.jpg").relative_to(BATCH))}),
            "ID19": verdict("Y", "본문에서 해당 브랜드 제품군의 성능·절약·관리 편익을 설명함", {"excerpt": benefit_text[:500]}),
            "ID20": verdict("N" if row in SIMPLE_PLP else "Y",
                            "제품군 소개는 있지만 독립된 기술·효익 블록이 없음" if row in SIMPLE_PLP else "브랜드 제품군의 기술 또는 효익을 별도 비교·카드 영역에서 설명함",
                            {"headings": feature[:8]}),
            "ID23": verdict("N" if row in NO_QA else "Y",
                            "본문에서 해당 브랜드 제품군의 질문과 이어지는 답변을 확인하지 못함" if row in NO_QA else "브랜드 제품군 관련 질문과 대응 설명이 본문 또는 FAQ에 있음",
                            {"excerpt": question[:600]}),
        }
        content["pages"][record["pageKey"]] = {"sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(), "results": results}
        audit = json.loads((BATCH / "id8-audit" / f"{record['pageKey']}.json").read_text())
        if audit["status"] == "REVIEW":
            selected = audit["top10"]
            bad = next((item for item in selected if str(item.get("alt") or "").strip() in GENERIC_ALTS), None)
            if not bad:
                raise ValueError(f"row {row} ID8 review needs image-by-image inspection")
            images["pages"][record["pageKey"]] = {
                "sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(),
                "sourceCaptureStateSha256": hashlib.sha256(state).hexdigest(),
                "result": verdict("N", "상위 본문 이미지 중 브랜드·제품군과 연결하여 이미지를 설명하지 않는 일반 문구가 있음",
                                  {"exampleAlt": bad["alt"], "imageUrl": bad["src"], "renderedArea": bad["renderedArea"]}),
            }
    content_path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n")
    image_path.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n")
    print(f"Coolblue reviewed: {len(ROWS)} current BCP rows")


if __name__ == "__main__":
    main()
