#!/usr/bin/env python3
"""Record source-locked manual review of saved Elgiganten BCP captures."""

from __future__ import annotations

import hashlib
import json

from lxml import html

from capture_bcp_population import RESULTS


BATCH = RESULTS / "20260928-all-159"
ROWS = {149, 150, 151, 152, 153, 154, 157, 158}
HERO = {152, 153, 154, 157, 158}
NO_HERO = {151}


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
        if record["retailerSlug"] != "elgiganten" or record["pageType"] != "Brand Category Page":
            raise ValueError(f"wrong source identity at row {row}")
        page = BATCH / "pages" / record["pageKey"] / "brand-category"
        raw = (page / "raw.html").read_bytes()
        tree = html.fromstring(raw)
        main = tree.xpath("//main")
        if not main:
            raise ValueError(f"main content missing at row {row}")
        headings = [" ".join(" ".join(node.itertext()).split()) for node in main[0].xpath(".//h1|.//h2")]
        headings = [heading for heading in headings if heading and "Cookies:" not in heading]
        if not headings:
            raise ValueError(f"editorial headings missing at row {row}")
        screenshot = str((page / "screenshot.jpg").relative_to(BATCH))
        evidence = {"headings": headings[:12], "screenshot": screenshot}
        results = {
            "ID19": verdict("Y", "본문에서 해당 브랜드 제품군의 구체적인 기술·편익을 선택 이유로 설명함", evidence),
            "ID20": verdict("Y", "본문의 별도 영역에서 해당 제품군의 기술·기능과 효익을 설명함", evidence),
            "ID23": verdict("N", "본문에서 해당 브랜드 제품군의 실질적인 질문과 대응 답변을 확인하지 못함", evidence),
        }
        if row in HERO:
            results["ID18"] = verdict("Y", "상단에 해당 브랜드 제품군을 소개하는 이미지형 대표 영역이 있음", evidence)
        elif row in NO_HERO:
            results["ID18"] = verdict("N", "상단은 제목·상품 목록이며 제품군 대표 배너가 없음", evidence)
        else:
            results["ID18"] = verdict("REVIEW", "본문 상단에 큰 제품 영상과 설명이 있으나 영상도 대표 배너로 인정할지는 현재 판정 기준에 명시되지 않음", evidence)
        reviews["pages"][record["pageKey"]] = {
            "sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(), "results": results,
        }
    path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n")
    print(f"Elgiganten content reviewed: {len(ROWS)} rows; video hero remains undecided for 2 rows")


if __name__ == "__main__":
    main()
