#!/usr/bin/env python3
"""Freeze successful BCP captures into a timestamped batch with a collection summary."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "output" / "offline"
RESULTS_ROOT = ROOT / "results"
RETAILERS = [
    "alza",
    "datart",
    "boulanger",
    "amazon-it",
    "mediaworld",
    "coolblue",
    "mediamarkt-nl",
    "mediamarkt-es",
    "elgiganten",
]
CAPTURE_FILES = [
    "request.json",
    "response.json",
    "raw.html",
    "screenshot.jpg",
    "capture-state.json",
]
CSV_FIELDS = [
    "리테일러",
    "페이지 유형",
    "수집 상태",
    "판정 상태",
    "수집 시각",
    "요청 URL",
    "최종 URL",
    "HTTP 상태",
    "페이지 끝 도달",
    "페이지 제목",
    "페이지 설명 개수",
    "검색엔진 설정",
    "대표 URL",
    "최상위 제목",
    "이미지 개수",
    "클릭 가능 요소 개수",
    "HTML 크기(byte)",
    "화면 파일 크기(byte)",
]


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object expected: {path}")
    return value


def joined(values: object) -> str:
    if not isinstance(values, list):
        return ""
    return " | ".join(str(value) for value in values)


def main() -> int:
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    batch_id = now.strftime("%Y%m%dT%H%M%SKST")
    batch_root = RESULTS_ROOT / batch_id
    pages_root = batch_root / "pages"
    rows: list[dict[str, object]] = []

    for retailer in RETAILERS:
        source = SOURCE_ROOT / retailer / "brand-category"
        response = read_json(source / "response.json")
        state = read_json(source / "capture-state.json")
        if response.get("ok") is not True:
            raise ValueError(f"capture is not successful: {retailer}")
        missing = [name for name in CAPTURE_FILES if not (source / name).is_file()]
        if missing:
            raise ValueError(f"capture files missing for {retailer}: {missing}")

        target = pages_root / retailer / "brand-category"
        target.mkdir(parents=True, exist_ok=False)
        for name in CAPTURE_FILES:
            shutil.copy2(source / name, target / name)

        metadata = state.get("metadata") if isinstance(state.get("metadata"), dict) else {}
        scroll = state.get("scroll") if isinstance(state.get("scroll"), dict) else {}
        byte_counts = response.get("bytes") if isinstance(response.get("bytes"), dict) else {}
        rows.append(
            {
                "리테일러": retailer,
                "페이지 유형": "Brand Category Page",
                "수집 상태": "성공",
                "판정 상태": "미판정",
                "수집 시각": response.get("captured_at", ""),
                "요청 URL": response.get("requested_url", ""),
                "최종 URL": response.get("final_url", ""),
                "HTTP 상태": response.get("status_code", ""),
                "페이지 끝 도달": scroll.get("reachedBottom") is True,
                "페이지 제목": metadata.get("title", ""),
                "페이지 설명 개수": len(metadata.get("metaDescription", [])),
                "검색엔진 설정": joined(metadata.get("robots")),
                "대표 URL": joined(metadata.get("canonical")),
                "최상위 제목": joined(metadata.get("h1")),
                "이미지 개수": len(state.get("images", [])),
                "클릭 가능 요소 개수": len(state.get("clickables", [])),
                "HTML 크기(byte)": byte_counts.get("raw_html", ""),
                "화면 파일 크기(byte)": byte_counts.get("screenshot", ""),
            }
        )

    batch_root.mkdir(parents=True, exist_ok=True)
    with (batch_root / "수집_요약.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    manifest = {
        "batch_id": batch_id,
        "created_at": now.isoformat(),
        "scope": "LG refrigerator Brand Category Page representative capture",
        "collection_count": len(rows),
        "collection_status": "9 successful",
        "assessment_status": "not performed",
        "pages_directory": "pages",
        "summary_csv": "수집_요약.csv",
        "captures": rows,
    }
    (batch_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(batch_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
