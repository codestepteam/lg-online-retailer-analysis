#!/usr/bin/env python3
"""Record current MediaWorld BCP content review with saved-page evidence."""

from __future__ import annotations

import hashlib
import json

from lxml import html as lxml_html

from capture_bcp_population import RESULTS


BATCH = RESULTS / "20260928-all-159"
ROWS = set(range(84, 92)) | set(range(95, 99))


def verdict(status: str, reason: str, evidence: dict | None = None) -> dict:
    return {"status": status, "reason": reason, "evidence": evidence or {}}


def main() -> None:
    manifest = json.loads((BATCH / "manifest.json").read_text())
    path = BATCH / "본문_항목_AI검수.json"
    reviews = json.loads(path.read_text()) if path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    for record in manifest["records"]:
        row = int(record["sourceRow"])
        if row not in ROWS:
            continue
        if record["retailerSlug"] != "mediaworld" or record["pageType"] != "Brand Category Page":
            raise ValueError(f"wrong source identity at row {row}")
        page = BATCH / "pages" / record["pageKey"] / "brand-category"
        raw = (page / "raw.html").read_bytes()
        tree = lxml_html.fromstring(raw)
        brand = str(record["brand"])
        editorial = []
        for node in tree.xpath("//h2"):
            heading = " ".join(" ".join(node.itertext()).split())
            if brand.casefold() in heading.casefold():
                text = " ".join(" ".join(node.getparent().itertext()).split())
                editorial.append({"heading": heading, "excerpt": text[:600]})
        # Samsung freezer content uses category benefit headings without its
        # brand name, but the paragraphs explicitly describe Samsung features.
        if row == 95:
            for node in tree.xpath("//h2"):
                text = " ".join(" ".join(node.getparent().itertext()).split())
                if "Samsung" in text and "No Frost" in text:
                    editorial.append({"heading": " ".join(node.itertext()).strip(), "excerpt": text[:600]})
                    break
        if row != 91 and not editorial:
            raise ValueError(f"brand benefit text not located at row {row}")
        if row == 91 and editorial:
            raise ValueError("Hisense washer page unexpectedly gained an editorial block")
        headings = [" ".join(" ".join(node.itertext()).split()) for node in tree.xpath("//h2|//h3")]
        if any("?" in item and brand.casefold() in item.casefold() for item in headings):
            raise ValueError(f"row {row} has a brand question; ID23 requires re-review")
        results = {
            "ID18": verdict("N", "상단은 브랜드명·로고·제품군 타일 및 상품 목록이고 브랜드 제품군의 이미지형 대표 배너가 없음", {"screenshot": str((page / "screenshot.jpg").relative_to(BATCH))}),
            "ID19": verdict("Y" if editorial else "N", "하단 설명에서 해당 브랜드 제품군의 기술·성능상 이점을 설명함" if editorial else "브랜드 제품군을 선택할 이유를 설명하는 독립 본문을 확인하지 못함", {"editorial": editorial[:2]}),
            "ID20": verdict("N", "기술 이름은 하단 서술형 설명에 있으나 별도 기술·효익 카드나 블록은 없음", {"editorial": editorial[:2]}),
            "ID23": verdict("N", "본문에 해당 브랜드 제품군의 질문과 그에 대응하는 답변 블록이 없음", {"editorialHeadings": [item["heading"] for item in editorial]}),
        }
        reviews["pages"][record["pageKey"]] = {"sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(), "results": results}
    path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n")
    print(f"MediaWorld reviewed: {len(ROWS)} current BCP rows")


if __name__ == "__main__":
    main()
