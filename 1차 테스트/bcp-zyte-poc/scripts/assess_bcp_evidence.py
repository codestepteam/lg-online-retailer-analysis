#!/usr/bin/env python3
"""Apply the confirmed BCP rules to a saved evidence batch.

ID9 and ID10 use automatic checks. ID8 uses a source-locked image review when
one is present. Other metrics remain REVIEW; candidate counts are never treated
as proof of presence or absence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / "results"
RULE_VERSION = "bcp-first-assessment-D019-2026-09-28"
METRIC_IDS = ("ID8", "ID9", "ID10", "ID18", "ID19", "ID20", "ID21", "ID22", "ID23")
REVIEW_REASONS = {
    "ID8": "제품 카드 포함·CSS 배경 및 순수 장식 제외 기준의 이미지별 범위·문구 검수가 필요",
    "ID18": "상단 대표 배너의 브랜드·제품군 관련성과 화면 배치를 사람 확인해야 함",
    "ID19": "브랜드 선택 이유를 설명하는 독립된 본문 영역인지 사람 확인해야 함",
    "ID20": "제품군 기술·기능·효익을 설명하는 영역인지 사람 확인해야 함",
    "ID21": "카테고리 탐색 블록의 전체 링크를 클릭하고 도착 페이지를 확인해야 함",
    "ID22": "제품 카드와 같은 제품의 상세 페이지로 실제 이동하는지 확인해야 함",
    "ID23": "화면에 보이는 브랜드·제품군 질문과 답변인지 사람 확인해야 함",
}
CSV_FIELDS = ("리테일러", "항목", "판정", "이유", "근거", "주의", "요청 URL", "수집 최종 URL", "상세 파일")


class CanonicalTags(HTMLParser):
    """Read actual link elements; an empty href must not erase tag presence."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str | None] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() != "link":
            return
        values = {name.casefold(): value for name, value in attrs}
        if "canonical" in (values.get("rel") or "").casefold().split():
            self.hrefs.append(values.get("href"))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def values(metadata: dict[str, object], key: str) -> list[str]:
    raw = metadata.get(key)
    if isinstance(raw, list):
        return [str(item or "").strip() for item in raw]
    return [str(raw).strip()] if raw is not None else []


def assess_id9(metadata: dict[str, object]) -> dict[str, object]:
    fields = {
        "Title": values(metadata, "title"),
        "Meta Description": values(metadata, "metaDescription"),
        "H1": values(metadata, "h1"),
        "Robots Meta": values(metadata, "robots"),
    }
    missing = [name for name, items in fields.items() if not any(items)]
    robots = [item.casefold().replace(" ", "") for item in fields["Robots Meta"] if item]
    invalid_robots = [item for item in robots if not {"index", "follow"}.issubset(set(item.split(","))) or {"noindex", "nofollow"} & set(item.split(","))]
    conflicts = [name for name, items in fields.items() if len(set(item for item in items if item)) > 1]
    evidence = {**fields, "missing": missing, "invalidRobots": invalid_robots, "conflictingFields": conflicts}
    if missing or invalid_robots:
        parts = []
        if missing:
            parts.append("누락 또는 빈값: " + ", ".join(missing))
        if invalid_robots:
            parts.append("Robots Meta가 index, follow 조건에 맞지 않음: " + "; ".join(fields["Robots Meta"]))
        return {"status": "N", "reason": "; ".join(parts), "evidence": evidence, "warnings": []}
    if conflicts:
        return {"status": "REVIEW", "reason": "서로 다른 값의 중복 태그: " + ", ".join(conflicts), "evidence": evidence, "warnings": []}
    warnings = ["H1이 여러 개이므로 대표 제목은 추가 확인 필요"] if len(fields["H1"]) > 1 else []
    return {"status": "Y", "reason": "Title·Meta Description·H1·Robots Meta가 모두 있고 Robots가 index, follow", "evidence": evidence, "warnings": warnings}


def assess_id10(html: str) -> dict[str, object]:
    parser = CanonicalTags()
    parser.feed(html)
    return assess_id10_hrefs(parser.hrefs)


def assess_id10_hrefs(hrefs: list[str | None]) -> dict[str, object]:
    warnings: list[str] = []
    if any(not (href or "").strip() for href in hrefs):
        warnings.append("Canonical 태그에 주소가 비어 있음")
    if len(hrefs) > 1:
        warnings.append("Canonical 태그가 여러 개 있음")
    return {
        "status": "Y" if hrefs else "N",
        "reason": "Canonical 태그가 있음" if hrefs else "Canonical 태그가 없음",
        "evidence": {"tagCount": len(hrefs), "hrefs": hrefs},
        "warnings": warnings,
    }


def candidate_summary(metric_id: str, evidence: dict[str, object]) -> dict[str, int]:
    keys = {
        "ID8": ("top10ByRenderedArea",),
        "ID18": ("attributeCandidates", "largeVisibleImages"),
        "ID19": ("headingOrAttributeCandidates",),
        "ID20": ("headingOrAttributeCandidates",),
        "ID21": ("attributeCandidates", "linkCandidates"),
        "ID22": ("attributeCandidates", "productLinkCandidates"),
        "ID23": ("headingOrAttributeCandidates", "detailsElements", "faqPageJsonLd"),
    }[metric_id]
    return {key: len(evidence.get(key, [])) for key in keys}


def assess_id8(batch: Path, retailer: str, source_dir: Path) -> dict[str, object]:
    review_path = batch / "ID8_판정_검수.json"
    audit_path = batch / "id8-audit" / f"{retailer}.json"
    if not review_path.is_file() or not audit_path.is_file():
        return {"status": "REVIEW", "reason": REVIEW_REASONS["ID8"], "evidence": {}, "warnings": []}
    review = json.loads(review_path.read_text(encoding="utf-8"))
    entry = review.get("pages", {}).get(retailer)
    if not isinstance(entry, dict):
        return {"status": "REVIEW", "reason": "이 페이지의 ID8 이미지별 검수 기록이 없음", "evidence": {}, "warnings": []}
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    selected = audit.get("top10", [])
    selected_indices = [item.get("index") for item in selected]
    source_hashes = {
        "captureStateSha256": hashlib.sha256((source_dir / "capture-state.json").read_bytes()).hexdigest(),
        "rawHtmlSha256": hashlib.sha256((source_dir / "raw.html").read_bytes()).hexdigest(),
    }
    if (any(entry.get(key) != value for key, value in source_hashes.items())
            or entry.get("selectedImageIndices") != selected_indices):
        return {"status": "REVIEW", "reason": "검수 이후 수집본 또는 상위 10개 이미지가 달라져 재검수 필요",
                "evidence": {"selectedImageIndices": selected_indices}, "warnings": []}
    decision = entry.get("decision")
    if decision not in {"Y", "N"} or (decision == "Y" and any(not str(item.get("alt") or "").strip() for item in selected)):
        return {"status": "REVIEW", "reason": "ID8 검수 기록과 실제 alt 값이 일치하지 않아 재검수 필요",
                "evidence": {"selectedImageIndices": selected_indices}, "warnings": []}
    return {
        "status": decision,
        "reason": entry.get("reason") or "ID8 이미지별 검수 결과",
        "evidence": {"selectedImages": [{key: item.get(key) for key in (
            "index", "src", "alt", "renderedArea", "scopeSuggestion", "scopeReason", "htmlPath"
        )} for item in selected], "sourceHashes": source_hashes, "reviewMethod": entry.get("reviewMethod")},
        "warnings": [str(review.get("reviewStatus") or "AI 이미지별 검수")],
    }


def assess_page(batch: Path, evidence_path: Path) -> tuple[dict[str, object], list[dict[str, str]]]:
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    page = evidence["page"]
    retailer = page["retailer"]
    source_dir = batch / "pages" / retailer / "brand-category"
    state = json.loads((source_dir / "capture-state.json").read_text(encoding="utf-8"))
    html = (source_dir / "raw.html").read_text(encoding="utf-8", errors="replace")
    metadata = state.get("metadata") if isinstance(state.get("metadata"), dict) else {}
    initial_metadata = state.get("initialMetadata") if isinstance(state.get("initialMetadata"), dict) else None
    requested_url = page.get("requestedUrl") or ""
    final_url = page.get("finalUrl") or ""
    url_warning = "스크롤·더보기 후 수집 최종 URL이 요청 URL과 달라짐. ID9·ID10은 최종 화면 기준" if requested_url != final_url else ""
    use_initial_metadata = bool(
        requested_url != final_url and initial_metadata and initial_metadata.get("url") == requested_url
    )
    results: dict[str, dict[str, object]] = {}
    rows: list[dict[str, str]] = []
    for metric_id in METRIC_IDS:
        if page.get("collectionOk") is not True:
            result = {"status": "COLLECTION_ERROR", "reason": "정상 수집이 확인되지 않음", "evidence": {}, "warnings": []}
        elif metric_id == "ID8":
            result = assess_id8(batch, retailer, source_dir)
        elif metric_id == "ID9":
            result = assess_id9(initial_metadata if use_initial_metadata else metadata)
            result["evidence"]["metadataMoment"] = "before_scroll" if use_initial_metadata else "captured_final_page"
        elif metric_id == "ID10":
            result = assess_id10_hrefs(initial_metadata.get("canonical", [])) if use_initial_metadata else assess_id10(html)
            result["evidence"]["metadataMoment"] = "before_scroll" if use_initial_metadata else "captured_final_page"
        else:
            result = {
                "status": "REVIEW",
                "reason": REVIEW_REASONS[metric_id],
                "evidence": {"candidateCounts": candidate_summary(metric_id, evidence["metrics"][metric_id]["evidence"])},
                "warnings": [],
            }
        if url_warning and not use_initial_metadata and metric_id in {"ID9", "ID10"} and result["status"] in {"Y", "N"}:
            observed_status = result["status"]
            result["evidence"]["capturedFinalPageStatus"] = observed_status
            result["status"] = "REVIEW"
            result["reason"] = f"요청 URL의 {metric_id}는 미확인. 수집 최종 화면에서는 {observed_status}: {result['reason']}"
        if url_warning:
            result["warnings"].append("스크롤·더보기 후 수집 최종 URL이 요청 URL과 달라짐; ID9·ID10은 스크롤 전 보존값 기준" if use_initial_metadata else url_warning)
        results[metric_id] = result
        rows.append({
            "리테일러": retailer,
            "항목": metric_id,
            "판정": result["status"],
            "이유": result["reason"],
            "근거": json.dumps(result["evidence"], ensure_ascii=False),
            "주의": "; ".join(result["warnings"]),
            "요청 URL": requested_url,
            "수집 최종 URL": final_url,
            "상세 파일": str(Path("assessed") / retailer / "bcp-assessment.json"),
        })
    output = {
        "ruleVersion": RULE_VERSION,
        "sourceEvidence": str(evidence_path.relative_to(batch)),
        "retailer": retailer,
        "requestedUrl": requested_url,
        "capturedFinalUrl": final_url,
        "results": results,
    }
    return output, rows


def latest_batch() -> Path:
    batches = sorted(path for path in RESULTS_ROOT.iterdir() if path.is_dir() and (path / "parsed").is_dir())
    if not batches:
        raise ValueError("No parsed BCP batch found")
    return batches[-1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", nargs="?", type=Path, help="saved batch directory; defaults to latest parsed batch")
    args = parser.parse_args()
    batch = args.batch.resolve() if args.batch else latest_batch()
    evidence_paths = sorted((batch / "parsed").glob("*/bcp-evidence.json"))
    if not evidence_paths:
        raise ValueError(f"No parsed BCP evidence in {batch}")
    rows: list[dict[str, str]] = []
    for evidence_path in evidence_paths:
        assessment, page_rows = assess_page(batch, evidence_path)
        target = batch / "assessed" / assessment["retailer"]
        target.mkdir(parents=True, exist_ok=True)
        (target / "bcp-assessment.json").write_text(json.dumps(assessment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        rows.extend(page_rows)
    summary = batch / "판정_1차_요약.csv"
    with summary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter((row["항목"], row["판정"]) for row in rows)
    lines = [
        "# BCP 9개 항목 1차 판정",
        "",
        f"- 입력 수집 묶음: `{batch.name}` ({len(evidence_paths)}개 페이지)",
        "- ID9·ID10은 자동 검사했다. ID8은 원본 수집본과 일치하는 이미지별 검수 기록이 있을 때만 Y/N을 반영한다. 다른 항목은 후보 개수로 Y/N을 추정하지 않는다.",
        "- 요청 URL과 수집 최종 URL이 다르면 스크롤 전 저장값으로 ID9·ID10을 검사한다. 저장값이 없는 예전 수집본은 REVIEW로 둔다.",
        "",
        "| 리테일러 | ID8 이미지 설명 | ID9 메타데이터 | ID10 대표 주소 태그 | URL 변경 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for evidence_path in evidence_paths:
        retailer = evidence_path.parent.name
        page_rows = {row["항목"]: row for row in rows if row["리테일러"] == retailer}
        changed = "예" if page_rows["ID9"]["요청 URL"] != page_rows["ID9"]["수집 최종 URL"] else "아니요"
        lines.append(f"| {retailer} | {page_rows['ID8']['판정']} | {page_rows['ID9']['판정']} | {page_rows['ID10']['판정']} | {changed} |")
    lines.extend(["", "## 항목별 상태", "", "| 항목 | Y | N | 검토 필요 |", "| --- | ---: | ---: | ---: |"])
    for metric_id in METRIC_IDS:
        lines.append(f"| {metric_id} | {counts[metric_id, 'Y']} | {counts[metric_id, 'N']} | {counts[metric_id, 'REVIEW']} |")
    lines.extend([
        "", "각 판정의 실제 값과 이유는 `판정_1차_요약.csv` 또는 `assessed/<리테일러>/bcp-assessment.json`에서 본다.",
        "ID18·19·20·23 콘텐츠 의미와 ID21·22 링크 도착 검증이 다음 작업이다. ID8의 Y/N은 이번 수집본의 AI 이미지별 검수 결과이며 과거 결과표의 판정을 복사한 값이 아니다.",
    ])
    (batch / "판정_1차_요약.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest_path = batch / "manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        id8_reviewed = all(row["판정"] in {"Y", "N"} for row in rows if row["항목"] == "ID8")
        manifest["assessment_status"] = "partial: ID8 reviewed, ID9 and ID10 automated; six metrics need review" if id8_reviewed else "partial: ID9 and ID10 assessed; seven metrics need review"
        manifest["assessment"] = {
            "rule_version": RULE_VERSION,
            "page_count": len(evidence_paths),
            "automated_metrics": ["ID9", "ID10"],
            "manually_reviewed_metrics": ["ID8"] if id8_reviewed else [],
            "review_metrics": [metric_id for metric_id in METRIC_IDS if metric_id not in ({"ID8", "ID9", "ID10"} if id8_reviewed else {"ID9", "ID10"})],
            "summary_csv": "판정_1차_요약.csv",
            "summary_markdown": "판정_1차_요약.md",
            "details_directory": "assessed",
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(batch / "판정_1차_요약.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
