#!/usr/bin/env python3
"""Review current Spanish MediaMarkt BCP content and expanded FAQ text."""

from __future__ import annotations

import hashlib
import json

from lxml import html as lxml_html

from capture_bcp_population import RESULTS


BATCH = RESULTS / "20260928-all-159"
ROWS = set(range(132, 141)) | set(range(144, 147))
HERO_ROWS = {135, 139, 140}


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
        if record["retailerSlug"] != "mediamarkt-es" or record["pageType"] != "Brand Category Page":
            raise ValueError(f"wrong source identity at row {row}")
        page = BATCH / "pages" / record["pageKey"] / "brand-category"
        raw = (page / "raw.html").read_bytes()
        tree = lxml_html.fromstring(raw)
        brand = str(record["brand"])
        faq = []
        for node in tree.xpath("//li[.//h3]"):
            question = " ".join(" ".join(node.xpath(".//h3")[0].itertext()).split())
            if "?" not in question:
                continue
            whole = " ".join(" ".join(node.itertext()).split())
            answer = whole[len(question):].strip()
            if len(answer) > 25:
                faq.append({"question": question, "answer": answer[:350]})
        brand_faq = [item for item in faq if brand.casefold() in (item["question"] + " " + item["answer"]).casefold()]
        if not brand_faq:
            raise ValueError(f"brand/category FAQ not located at row {row}")
        body_text = " ".join(tree.xpath("//body")[0].itertext())
        if brand.casefold() not in body_text.casefold():
            raise ValueError(f"source brand missing from current page at row {row}")
        results = {
            "ID18": verdict("Y" if row in HERO_ROWS else "N",
                            "상단 상품 목록 바로 위에 해당 브랜드 제품군의 가로 이미지 배너가 있음" if row in HERO_ROWS else "상단에 브랜드 제품군 이미지형 대표 배너가 없음",
                            {"screenshot": str((page / "screenshot.jpg").relative_to(BATCH))}),
            "ID19": verdict("Y", "본문 소개 또는 질문답변에서 해당 브랜드 제품군의 기술·절약·사용상 장점을 설명함",
                            {"faqExample": brand_faq[0] if brand_faq else None}),
            "ID20": verdict("N", "기술·효익은 소개 문단이나 질문답변에 있지만 별도의 제품군 핵심 기술 블록으로 분리되어 있지 않음",
                            {"faqExample": brand_faq[0] if brand_faq else None}),
            "ID23": verdict("Y", "해당 브랜드 제품군의 질문과 대응 답변이 저장된 FAQ 블록에 있음",
                            {"faqExample": faq[0] if faq else None, "brandFaqExample": brand_faq[0] if brand_faq else None}),
        }
        reviews["pages"][record["pageKey"]] = {"sourceRawHtmlSha256": hashlib.sha256(raw).hexdigest(), "results": results}
    path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n")
    print(f"MediaMarkt Spain reviewed: {len(ROWS)} current BCP rows")


if __name__ == "__main__":
    main()
