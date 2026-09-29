#!/usr/bin/env python3
"""Record reviewed ID8 image decisions for remaining brand pages and one BCP."""

from __future__ import annotations

import hashlib
import json

from audit_id8_images import audit_page
from capture_bcp_population import RESULTS


BATCH = RESULTS / "20260928-all-159"
DECISIONS = {
    21: ("N", "가장 큰 LG 브랜드 이미지의 alt가 'LG'라는 브랜드명뿐이어서 이미지를 설명하지 않음", 28),
    22: ("Y", "상위 이미지의 실제 alt가 Samsung 제품 종류·모델을 설명함", None),
    56: ("Y", "상위 상품 이미지의 실제 alt가 Darty의 LG 제품 종류·모델을 설명함", None),
    57: ("Y", "상위 상품 이미지의 실제 alt가 Darty의 Samsung 제품 종류·모델을 설명함", None),
    82: ("N", "상위 LG 가전제품 종류 이미지 중 alt가 비어 있는 본문 이미지가 있음", 13),
    83: ("Y", "상위 Samsung 제품·제품군 이미지의 실제 alt가 표시된 기기와 기능을 설명함; 로고는 순수 장식으로 제외", None),
    101: ("Y", "상위 LG 상품 이미지의 실제 alt가 제품 종류·모델과 기능을 설명함", None),
    102: ("N", "본문 상위 이미지의 alt가 비어 있음", 14),
    152: ("N", "상위 이미지의 alt 중 'wash dry VC'는 이미지를 설명하지 않는 내부식 약어임", 20),
    160: ("Y", "상위 Samsung 제품군 이미지의 실제 alt가 해당 제품 종류·서비스를 설명함", None),
}


def main() -> None:
    records = {int(x["sourceRow"]): x for x in json.loads((BATCH / "manifest.json").read_text())["records"]}
    path = BATCH / "ID8_전체검수.json"
    data = json.loads(path.read_text()) if path.is_file() else {"reviewer": "AI, current saved capture", "pages": {}}
    for row, (status, reason, bad_index) in DECISIONS.items():
        record = records[row]
        page_type = "brand-category" if record["pageType"] == "Brand Category Page" else "brand"
        page = BATCH / "pages" / record["pageKey"] / page_type
        audit, _ = audit_page(BATCH, record["pageKey"], page_type)
        top = audit["top10"]
        if bad_index is not None and bad_index not in {x["index"] for x in top}:
            raise ValueError(f"expected image {bad_index} not in top 10 at row {row}")
        if status == "Y" and any(not str(x.get("alt") or "").strip() for x in top):
            raise ValueError(f"top images have blank alt at row {row}")
        data["pages"][record["pageKey"]] = {
            "sourceRawHtmlSha256": hashlib.sha256((page / "raw.html").read_bytes()).hexdigest(),
            "sourceCaptureStateSha256": hashlib.sha256((page / "capture-state.json").read_bytes()).hexdigest(),
            "result": {"status": status, "reason": reason,
                       "evidence": {"selectedImages": [{"index": x["index"], "alt": x.get("alt"), "renderedArea": x["renderedArea"]} for x in top],
                                    "exceptionIndex": bad_index}},
        }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"reviewed {len(DECISIONS)} additional ID8 rows")


if __name__ == "__main__":
    main()
