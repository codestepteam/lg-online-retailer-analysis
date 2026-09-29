#!/usr/bin/env python3
"""Audit saved BCP capture batches without changing their raw capture files."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / "results"
CSV_FIELDS = [
    "리테일러",
    "응답 정상",
    "페이지 끝 도달",
    "필수 영역 검사",
    "쿠키 창 남음",
    "페이지 높이(px)",
    "화면 이미지 높이(px)",
    "화면 이미지 저장 상태",
    "현재 확인 결과",
]


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object expected: {path}")
    return value


def latest_batch() -> Path:
    batches = sorted(path for path in RESULTS_ROOT.iterdir() if path.is_dir())
    if not batches:
        raise ValueError(f"No saved result batch: {RESULTS_ROOT}")
    return batches[-1]


def audit_page(page: Path) -> dict[str, object]:
    retailer = page.parent.name
    response = read_json(page / "response.json")
    state = read_json(page / "capture-state.json")
    scroll = state.get("scroll") if isinstance(state.get("scroll"), dict) else {}
    required = state.get("required") if isinstance(state.get("required"), list) else []
    required_ok = all(not isinstance(item, dict) or item.get("present") is not False for item in required)
    cookie_remaining = bool(state.get("cookieRemaining"))
    page_height = int(scroll.get("height") or 0)
    with Image.open(page / "screenshot.jpg") as image:
        screenshot_height = image.height
    screenshot_full = page_height > 0 and screenshot_height >= page_height
    response_ok = response.get("ok") is True
    scroll_ok = scroll.get("reachedBottom") is True
    capture_ok = response_ok and scroll_ok and required_ok and not cookie_remaining and not state.get("error")
    if not capture_ok:
        result = "수집기 완료 조건 미통과"
    elif screenshot_full:
        result = "본문 수집 조건 통과·화면 전체 저장"
    else:
        result = "본문 수집 조건 통과·화면 10,000px까지 저장"
    return {
        "리테일러": retailer,
        "응답 정상": response_ok,
        "페이지 끝 도달": scroll_ok,
        "필수 영역 검사": required_ok,
        "쿠키 창 남음": cookie_remaining,
        "페이지 높이(px)": page_height,
        "화면 이미지 높이(px)": screenshot_height,
        "화면 이미지 저장 상태": "전체" if screenshot_full else "일부",
        "현재 확인 결과": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", nargs="?", type=Path)
    args = parser.parse_args()
    batch = args.batch.resolve() if args.batch else latest_batch()
    pages = sorted((batch / "pages").glob("*/brand-category"))
    if not pages:
        raise ValueError(f"No BCP pages in batch: {batch}")
    rows = [audit_page(page) for page in pages]

    csv_path = batch / "수집_완전성_점검.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    full_count = sum(row["화면 이미지 저장 상태"] == "전체" for row in rows)
    partial = [str(row["리테일러"]) for row in rows if row["화면 이미지 저장 상태"] == "일부"]
    lines = [
        "# Brand Category Page 수집 완전성 점검",
        "",
        f"- 점검 대상: `{batch.name}`",
        f"- 수집기 완료 조건 통과: {sum(' 통과' in str(row['현재 확인 결과']) for row in rows)}/{len(rows)}",
        f"- 화면 전체 저장: {full_count}/{len(rows)}",
        f"- 화면 10,000픽셀 제한으로 일부만 저장: {', '.join(partial) if partial else '없음'}",
        "",
        "`raw.html`은 이미지를 HTML로 변환한 파일이 아니다. 브라우저 동작이 끝난 시점의 페이지 구조와 텍스트를 저장한 파일이다. 외부 이미지·폰트·스크립트 파일 자체를 모두 포함하는 완전한 오프라인 복제본은 아니다.",
        "",
        "| 리테일러 | 본문 수집 조건 | 페이지 높이 | 화면 이미지 높이 | 화면 저장 |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in rows:
        capture = "통과" if "통과" in str(row["현재 확인 결과"]) else "미통과"
        lines.append(
            f"| {row['리테일러']} | {capture} | {row['페이지 높이(px)']}px | "
            f"{row['화면 이미지 높이(px)']}px | {row['화면 이미지 저장 상태']} |"
        )
    report_path = batch / "수집_완전성_점검.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest_path = batch / "manifest.json"
    manifest = read_json(manifest_path)
    manifest["completeness_audit"] = {
        "capture_contract_passed": len(rows),
        "screenshot_full": full_count,
        "screenshot_partial": len(partial),
        "screenshot_partial_retailers": partial,
        "report": report_path.name,
        "csv": csv_path.name,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
