#!/usr/bin/env python3
"""Record source-locked manual reviews of the 24 LG category captures."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from lxml import html

from capture_bcp_population import ROOT


BATCH = ROOT / "results_population" / "20260928-all-159"
# Order: hero, Why LG, separate USP, on-page question/answer.
DECISIONS = {
    14: "YYYN", 15: "YYYY", 16: "YYYY",
    38: "NYNN", 39: "NNNN",
    50: "NYNY", 51: "YYNY",
    74: "YNNN", 75: "YNNN", 76: "YNNN", 77: "YNNN",
    92: "NYNN", 93: "NYNN", 94: "NYNN",
    112: "YYYN", 113: "NYNN", 114: "NYNN",
    126: "NYYN", 127: "NYYY",
    141: "NYNY", 142: "NYNY", 143: "NYNY",
    155: "NYNN", 156: "YYYN",
}
IMAGE_Y = {14, 15, 16, 38, 39, 74, 75, 76, 77}
IMAGE_N = {112, 114}
NAV_N = {50, 51, 74, 75, 76, 77, 92, 93, 113, 114, 126, 141, 155}
INTRO_BLOCK = {14: "block-00011", 15: "block-00011", 16: "block-00011",
               38: "block-00005", 112: "block-00005", 113: "block-00009",
               114: "block-00009", 126: "block-00008", 127: "block-00011",
               155: "block-00020", 156: "block-00018"}
USP_BLOCK = {14: "block-00012", 15: "block-00012", 16: "block-00012",
             112: "block-00011", 126: "block-00108", 127: "block-00071",
             156: "block-00020"}
FAQ_BLOCK = {15: "block-00018", 16: "block-00017"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verdict(status: str, reason: str, evidence: dict | None = None) -> dict:
    return {"status": status, "reason": reason, "evidence": evidence or {}}


def main() -> None:
    records = {int(r["sourceRow"]): r for r in json.loads((BATCH / "manifest.json").read_text())["records"]}
    compact = {int(r["sourceWorkbookRow"]): r for r in json.loads((BATCH / "본문_검토용_압축자료.json").read_text())}
    review_path = BATCH / "본문_항목_AI검수.json"
    image_path = BATCH / "ID8_전체검수.json"
    reviews = json.loads(review_path.read_text())
    images = json.loads(image_path.read_text())
    for row, flags in DECISIONS.items():
        record = records[row]
        assert record["brand"] == "LG" and record["pageType"] == "Brand Category Page", row
        key = record["pageKey"]
        page = BATCH / "pages" / key / "brand-category"
        raw = page / "raw.html"
        screenshot = page / "screenshot.jpg"
        tree = html.fromstring(raw.read_bytes())
        body = " ".join(" ".join(tree.xpath("//body")[0].itertext()).split())
        assert "LG" in body, row
        candidates = {b["blockId"]: b["text"] for b in compact[row]["contentCandidates"]}
        rendered = {"screenshot": str(screenshot.relative_to(BATCH))}
        if row in INTRO_BLOCK:
            assert INTRO_BLOCK[row] in candidates, (row, "intro")
        if row in USP_BLOCK:
            assert USP_BLOCK[row] in candidates, (row, "USP")
        if row in FAQ_BLOCK:
            assert FAQ_BLOCK[row] in candidates, (row, "FAQ")
        intro = {"blockId": INTRO_BLOCK[row], "excerpt": candidates[INTRO_BLOCK[row]][:450]} if row in INTRO_BLOCK else {}
        usp = {"blockId": USP_BLOCK[row], "excerpt": candidates[USP_BLOCK[row]][:450]} if row in USP_BLOCK else {}
        qa = {"blockId": FAQ_BLOCK[row], "excerpt": candidates[FAQ_BLOCK[row]][:450]} if row in FAQ_BLOCK else {}
        if row in {50, 51}:
            # The Boulanger header asks a brand/category question and answers it in the same section.
            heading = tree.xpath('//*[@id="product-list__header"]')
            assert heading, row
            for hidden in heading[0].xpath('.//script|.//style'):
                hidden.drop_tree()
            clean = " ".join(" ".join(heading[0].itertext()).split())
            assert "LG" in clean, row
            qa = {"section": "product-list__header", "excerpt": clean[:600]}
            assert "?" in qa["excerpt"], row
            intro = qa
        elif row in {92, 93, 94}:
            headings = [" ".join(node.itertext()).strip() for node in tree.xpath("//h2")]
            brand_headings = [s for s in headings if "LG" in s]
            assert brand_headings, (row, "brand editorial heading")
            intro = {"headings": brand_headings[:5]}
        elif row in {141, 142, 143}:
            faq = []
            for node in tree.xpath("//li[.//h3]"):
                heading = " ".join(node.xpath(".//h3")[0].itertext()).strip()
                answer = " ".join(" ".join(node.itertext()).split())[len(heading):].strip()
                if "?" in heading and "LG" in (heading + answer) and len(answer) > 25:
                    faq.append({"question": heading, "answer": answer[:350]})
            assert faq, (row, "LG FAQ")
            qa = faq[0]
            intro = {"faqExample": faq[0]}
        elif row == 127:
            questions = [" ".join(node.itertext()).strip() for node in tree.xpath("//h2")]
            assert any("?" in q and "LG" in q for q in questions), row
            qa = {"questionHeadings": [q for q in questions if "?" in q and "LG" in q][:3]}
        elif row in {38, 39}:
            # Generic Datart promotion images in the top area do not advertise LG.
            assert "LG" in body
        elif row in {74, 75, 76, 77}:
            # Amazon brand-store images are the top large images in the capture.
            assert "LG" in str(compact[row]["topImages"][0]["alt"])

        status18, status19, status20, status23 = flags
        results = {
            "ID18": verdict(status18,
                "상단에 LG와 해당 제품군을 소개하는 큰 이미지형 대표 영역이 있음" if status18 == "Y" else
                "상단에는 해당 LG 제품군을 대표하는 이미지 배너가 없음; 일반 매장 판촉·제품 카드·로고는 제외",
                rendered),
            "ID19": verdict(status19,
                "본문에서 LG 제품군을 선택할 이유나 사용상 이점을 설명함" if status19 == "Y" else
                "제품 목록·일반 안내 외에 LG 제품군을 선택할 이유를 설명하는 영역이 없음",
                intro),
            "ID20": verdict(status20,
                "LG 제품군의 기술·기능·효익을 별도 제목이나 콘텐츠 영역에서 설명함" if status20 == "Y" else
                "기술명은 상품 카드 또는 일반 설명에만 있으며 별도의 핵심 기술·효익 블록이 없음",
                usp),
            "ID23": verdict(status23,
                "LG 제품군에 관한 질문과 이어지는 답변이 같은 페이지에 있음" if status23 == "Y" else
                "LG 제품군에 관한 질문·답변 쌍이 페이지에 없음; 단순 도움말 링크와 고객 평가 질문은 제외",
                qa),
        }
        if row in NAV_N:
            results["ID21"] = verdict("N", "LG 하위 제품군으로 이동하는 전용 탐색 블록이 없거나, 표시된 카테고리 카드가 일반 브랜드 혼합 목록으로 이동함", rendered)
        reviews["pages"][key] = {"sourceRawHtmlSha256": sha(raw),
                                 "sourceScreenshotSha256": sha(screenshot), "results": results}
        if row in IMAGE_Y | IMAGE_N:
            audit = json.loads((BATCH / "id8-audit" / f"{key}.json").read_text())
            assert audit["status"] == "REVIEW", row
            top = audit["top10"]
            assert top, row
            if row in IMAGE_Y:
                assert all("LG" in str(item.get("alt") or "") for item in top), row
                image_result = verdict("Y", "화면 크기 상위 본문 이미지 10개의 설명 문구가 LG 제품군·모델·기능을 설명함",
                                       {"imageIndices": [item["index"] for item in top], "alts": [item["alt"] for item in top]})
            else:
                generic = [item for item in top if str(item.get("alt") or "").strip() in {"Uitgelicht product", "LG wasmachines"}]
                assert generic, row
                image_result = verdict("N", "상위 이미지 중 사진 내용을 설명하지 않는 일반 문구가 있음",
                                       {"genericImages": [{"index": item["index"], "alt": item["alt"], "src": item["src"]} for item in generic]})
            images["pages"][key] = {"sourceRawHtmlSha256": sha(raw),
                                     "sourceCaptureStateSha256": sha(page / "capture-state.json"),
                                     "result": image_result}
    review_path.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n")
    image_path.write_text(json.dumps(images, ensure_ascii=False, indent=2) + "\n")
    print(f"reviewed {len(DECISIONS)} LG pages; {len(IMAGE_Y | IMAGE_N)} image assessments")


if __name__ == "__main__":
    main()
