#!/usr/bin/env python3
"""Review current Dutch MediaMarkt BCP content against the agreed rubric."""

from __future__ import annotations

import hashlib
import json

from lxml import html as lxml_html

from capture_bcp_population import RESULTS


BATCH = RESULTS / "20260928-all-159"
ROWS = set(range(120, 126)) | set(range(128, 132))
NO_USP = {120, 123, 131}
NO_FAQ = {120, 123}


def verdict(status: str, reason: str, evidence: dict | None = None) -> dict:
    return {"status": status, "reason": reason, "evidence": evidence or {}}


def main() -> None:
    records = json.loads((BATCH / "manifest.json").read_text())["records"]
    path = BATCH / "본문_항목_AI검수.json"
    reviews = json.loads(path.read_text()) if path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    for record in records:
        row = int(record["sourceRow"])
        if row not in ROWS:
            continue
        if record["retailerSlug"] != "mediamarkt-nl" or record["pageType"] != "Brand Category Page":
            raise ValueError(f"wrong source identity at row {row}")
        page = BATCH / "pages" / record["pageKey"] / "brand-category"
        raw = (page / "raw.html").read_bytes()
        tree = lxml_html.fromstring(raw)
        brand = str(record["brand"])
        sections = []
        for node in tree.xpath("//h2"):
            heading = " ".join(" ".join(node.itertext()).split())
            if not heading or heading in {"Bekijk ook eens", "Download de app"}:
                continue
            next_node = node.getnext()
            body = " ".join(" ".join(next_node.itertext()).split()) if next_node is not None else ""
            sections.append({"heading": heading, "excerpt": body[:500]})
        if not any(brand.casefold() in item["heading"].casefold() for item in sections):
            raise ValueError(f"brand editorial heading missing at row {row}")
        if row not in NO_USP and len(sections) < 3:
            raise ValueError(f"separate product-benefit section missing at row {row}")
        qa = next((item for item in sections if "?" in item["heading"] and brand.casefold() in item["heading"].casefold()
                   and len(item["excerpt"]) > 50), None)
        if row not in NO_FAQ and not qa:
            raise ValueError(f"brand/category Q&A not found at row {row}")
        results = {
            "ID18": verdict("N", "상단은 제품 목록·일반 판촉이며 해당 브랜드 제품군의 이미지형 대표 배너가 없음", {"screenshot": str((page / "screenshot.jpg").relative_to(BATCH))}),
            "ID19": verdict("Y", "본문에서 해당 브랜드 제품군을 선택할 구체적인 기능·효익을 설명함", {"section": sections[0]}),
            "ID20": verdict("N" if row in NO_USP else "Y",
                            "기술·효익이 소개 문장에는 있으나 독립된 핵심 USP 영역으로 구분되지 않음" if row in NO_USP else "기술·효익 또는 사용 사례를 별도 제목의 본문 영역에서 설명함",
                            {"sections": sections[:5]}),
            "ID21": verdict("N", "상단의 일반 탐색·필터·상품 추천을 제외하면 해당 브랜드 제품군의 전용 하위 카테고리 탐색 블록이 없음",
                            {"screenshot": str((page / "screenshot.jpg").relative_to(BATCH))}),
            "ID23": verdict("N" if row in NO_FAQ else "Y",
                            "질문형 문장은 구매·배송 안내에 관한 것으로 브랜드 제품군 설명의 질문답변이 아님" if row in NO_FAQ else "브랜드 제품군에 대한 질문형 제목과 이어지는 설명이 있음",
                            {"questionSection": qa}),
        }
        reviews["pages"][record["pageKey"]] = {"sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(), "results": results}
    path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n")
    print(f"MediaMarkt Netherlands reviewed: {len(ROWS)} current BCP rows")


if __name__ == "__main__":
    main()
