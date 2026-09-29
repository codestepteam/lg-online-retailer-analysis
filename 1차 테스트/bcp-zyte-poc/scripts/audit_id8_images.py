#!/usr/bin/env python3
"""Build an ID8 image review list from saved browser state and HTML.

The requested rule covers BCP content <img> elements, including product cards.
CSS background images are outside this metric. This script excludes clearly
unrelated page chrome and ads, but leaves uncertain decoration for review.
"""

from __future__ import annotations

import argparse
import csv
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin


ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / "results"
CSV_FIELDS = (
    "리테일러", "전체 크기 순위", "비제외 순위", "화면 이미지 번호", "화면 면적", "Alt 원문",
    "범위 제안", "범위 근거", "제품 카드 근거", "장식 신호", "이미지 주소", "HTML 위치",
)


class ImageContexts(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict[str, str]]] = []
        self.images: list[tuple[dict[str, str], list[tuple[str, dict[str, str]]]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "img":
            self.images.append((data, list(self.stack)))
        if tag not in self.VOID:
            self.stack.append((tag, data))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                return


def html_path(ancestors: list[tuple[str, dict[str, str]]]) -> str:
    parts = []
    for tag, attrs in ancestors[-8:]:
        identifier = "#" + attrs["id"] if attrs.get("id") else ""
        classes = "." + ".".join(attrs["class"].split()[:2]) if attrs.get("class") else ""
        parts.append(tag + identifier + classes)
    return " > ".join(parts)


def classify(attrs: dict[str, str], ancestors: list[tuple[str, dict[str, str]]], src: str) -> tuple[str, str, str, str]:
    tags = [tag for tag, _ in ancestors]
    context = " ".join(" ".join((item.get("id", ""), item.get("class", ""))) for _, item in ancestors).casefold()
    image_class = attrs.get("class", "").casefold()
    source = src.casefold()
    product_signals = [term for term in (
        "productgriditem", "product-list__product-image", "product-card-image", "product-box",
        "browsingitem", "product-card", "product__image",
    ) if term in context or term in image_class]
    if "article" in tags and "assets.mmsrg.com/isr/" in source:
        product_signals.append("상품 카드 안의 상품 이미지")
    decorative_signal = ""
    if attrs.get("role", "").casefold() in {"presentation", "none"}:
        decorative_signal = "role=" + attrs["role"]
    elif attrs.get("aria-hidden", "").casefold() == "true":
        decorative_signal = "aria-hidden=true"
    if "footer" in tags or "header" in tags:
        return "제외", "리테일러 공통 머리말·꼬리말", "", decorative_signal
    if any(term in context for term in ("brandingears", "amp-banner", "category-banner", "ems--pl_", "ems__full-link")):
        return "제외", "브랜드 제품군 밖의 광고·마케팅 영역", "", decorative_signal
    if any(term in source for term in ("retailmedia-static.criteo.com", "retail_media_sba_skeleton")):
        return "제외", "외부 광고 또는 로딩용 임시 이미지", "", decorative_signal
    if product_signals:
        return "포함", "제품 카드 이미지", ", ".join(product_signals), decorative_signal
    if "aside" in tags or ("nav" in tags and "main" not in tags):
        return "제외", "본문 밖 보조 영역·공통 탐색", "", decorative_signal
    if decorative_signal:
        return "검토", "장식 표시가 있으나 순수 장식 여부는 이미지 확인 필요", "", decorative_signal
    if "main" in tags or any(term in context for term in ("brandpage", "maincontent", "categoryanotationblock", "product-category-koncova", "hero__hero__")):
        return "포함", "브랜드 카테고리 본문 이미지", "", decorative_signal
    return "검토", "본문 소속 또는 순수 장식 여부 확인 필요", "", decorative_signal


def match_contexts(state: dict[str, object], raw_html: str) -> list[dict[str, object]]:
    parser = ImageContexts()
    parser.feed(raw_html)
    base_url = str(state.get("url") or "")
    records = parser.images
    result: list[dict[str, object]] = []
    for image in state.get("images", []):
        if not isinstance(image, dict):
            continue
        index = image.get("index")
        src = str(image.get("src") or "")
        if not isinstance(index, int):
            continue
        candidates = [position for position in range(max(0, index - 4), min(len(records), index + 5))
                      if urljoin(base_url, records[position][0].get("src", "")) == src]
        if not candidates:
            candidates = [position for position, (attrs, _) in enumerate(records)
                          if urljoin(base_url, attrs.get("src", "")) == src]
        if not candidates:
            scope, reason, product_signal, decorative_signal = "검토", "화면 이미지와 HTML 위치를 대응하지 못함", "", ""
            path = ""
        else:
            match = min(candidates, key=lambda position: abs(position - index))
            attrs, ancestors = records[match]
            scope, reason, product_signal, decorative_signal = classify(attrs, ancestors, src)
            path = html_path(ancestors)
        result.append({**image, "scopeSuggestion": scope, "scopeReason": reason,
                       "productCardSignal": product_signal, "decorativeSignal": decorative_signal,
                       "htmlPath": path})
    return result


def audit_page(batch: Path, retailer: str, page_type: str = "brand-category") -> tuple[dict[str, object], list[dict[str, object]]]:
    page = batch / "pages" / retailer / page_type
    state = json.loads((page / "capture-state.json").read_text(encoding="utf-8"))
    raw_html = (page / "raw.html").read_text(encoding="utf-8", errors="replace")
    records = match_contexts(state, raw_html)
    eligible = [item for item in records if item.get("visible") is True and item.get("loaded") is True and float(item.get("renderedArea") or 0) > 0]
    eligible.sort(key=lambda item: (-float(item.get("renderedArea") or 0), int(item["index"])))
    non_excluded = [item for item in eligible if item["scopeSuggestion"] != "제외"]
    selected = non_excluded[:10]
    if not selected:
        status, reason = "REVIEW", "대상 이미지가 0개일 때의 처리 기준이 미정"
    elif any(item["scopeSuggestion"] == "검토" for item in selected):
        status, reason = "REVIEW", "상위 후보에 본문 소속·장식 여부 확인이 필요한 이미지가 있음"
    elif any(not str(item.get("alt") or "").strip() for item in selected):
        status, reason = "N", "선정된 본문 이미지 또는 제품 카드 이미지 중 alt가 빈 이미지가 있음"
    else:
        status, reason = "REVIEW", "상위 이미지의 alt는 모두 있으나 문구가 실제 이미지와 맞는지 확인 필요"
    summary = {
        "retailer": retailer,
        "status": status,
        "reason": reason,
        "eligibleImageCount": len(eligible),
        "excludedCount": sum(item["scopeSuggestion"] == "제외" for item in eligible),
        "selectedCount": len(selected),
        "reviewCountInTop10": sum(item["scopeSuggestion"] == "검토" for item in selected),
        "emptyAltCountInTop10": sum(not str(item.get("alt") or "").strip() for item in selected),
        "top10": selected,
        "scopeRule": f"{page_type} 본문 <img> 및 제품 카드 포함; CSS 배경·순수 장식 제외; 화면 표시 면적 순",
    }
    rows: list[dict[str, object]] = []
    non_excluded_rank = 0
    for global_rank, item in enumerate(eligible, start=1):
        if item["scopeSuggestion"] != "제외":
            non_excluded_rank += 1
        if non_excluded_rank > 30 and global_rank > 50:
            break
        rows.append({
            "리테일러": retailer,
            "전체 크기 순위": global_rank,
            "비제외 순위": non_excluded_rank if item["scopeSuggestion"] != "제외" else "",
            "화면 이미지 번호": item.get("index"),
            "화면 면적": round(float(item.get("renderedArea") or 0)),
            "Alt 원문": item.get("alt"),
            "범위 제안": item["scopeSuggestion"],
            "범위 근거": item["scopeReason"],
            "제품 카드 근거": item["productCardSignal"],
            "장식 신호": item["decorativeSignal"],
            "이미지 주소": item.get("src"),
            "HTML 위치": item["htmlPath"],
        })
    return summary, rows


def latest_batch() -> Path:
    batches = sorted(path for path in RESULTS_ROOT.iterdir() if path.is_dir() and (path / "pages").is_dir())
    if not batches:
        raise ValueError("No saved BCP batch found")
    return batches[-1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", nargs="?", type=Path)
    args = parser.parse_args()
    batch = args.batch.resolve() if args.batch else latest_batch()
    retailers = sorted(path.name for path in (batch / "pages").iterdir() if (path / "brand-category" / "capture-state.json").is_file())
    summaries: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []
    target = batch / "id8-audit"
    target.mkdir(exist_ok=True)
    for retailer in retailers:
        summary, page_rows = audit_page(batch, retailer)
        summaries.append(summary)
        rows.extend(page_rows)
        (target / f"{retailer}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (batch / "ID8_이미지_검토.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# ID8 이미지 설명 문구 1차 검토",
        "",
        "2026-09-28 사용자 결정: 본문 HTML 이미지와 제품 카드 이미지 포함, CSS 배경·순수 장식 이미지 제외. 크기는 화면 표시 면적 기준이다.",
        "이 파일은 저장된 HTML의 이미지 위치와 화면 크기를 대조한 1차 결과다. `N`은 상위 대상 이미지에서 빈 alt가 확인된 경우이며, `REVIEW`는 대상 범위 또는 alt 문구 의미를 더 확인해야 한다는 뜻이다.",
        "",
        "| 리테일러 | 1차 상태 | 대상 후보 수 | 빈 alt 수 | 확인 필요 수 | 이유 |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for item in summaries:
        lines.append(f"| {item['retailer']} | {item['status']} | {item['selectedCount']} | {item['emptyAltCountInTop10']} | {item['reviewCountInTop10']} | {item['reason']} |")
    lines.extend(["", "이미지별 크기·alt·포함/제외 이유는 `ID8_이미지_검토.csv`와 `id8-audit/<리테일러>.json`에서 확인한다.", "`aria-hidden=true`여도 제품 카드의 상품 이미지라면 포함한다. 빈 alt만으로 장식 이미지라고 판단하지 않는다."])
    (batch / "ID8_이미지_검토_요약.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(batch / "ID8_이미지_검토_요약.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
