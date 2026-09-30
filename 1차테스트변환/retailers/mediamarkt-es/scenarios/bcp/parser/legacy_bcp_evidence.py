#!/usr/bin/env python3
"""Extract reviewable evidence for the nine BCP metrics from a saved capture batch.

This script does not assign Y/N. It preserves observed values and marks heuristic
content matches as candidates so that assessment rules can be reviewed separately.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / "results"
SCHEMA_VERSION = "bcp-evidence-v1"

METRICS = {
    "ID8": "Alt text 적용 여부",
    "ID9": "메타데이터 최적화",
    "ID10": "Canonical URL",
    "ID18": "Hero Banner 존재 여부",
    "ID19": "Why LG 블록 존재 여부",
    "ID20": "USP 블록 존재 여부",
    "ID21": "Category Navigator 존재 및 탐색 가능 여부",
    "ID22": "Product List와 PDP 이동 수단 존재 여부",
    "ID23": "FAQ 존재 여부",
}

TERM_GROUPS = {
    "why_lg": [
        "why lg", "why choose lg", "pourquoi lg", "waarom lg", "perche lg",
        "por que lg", "varfor lg", "proč lg", "proc lg", "dlaczego lg",
    ],
    "faq": [
        "faq", "frequently asked", "questions frequentes", "veelgestelde vragen",
        "domande frequenti", "preguntas frecuentes", "vanliga fragor",
        "nejcastejsi dotazy", "casto kladene otazky",
    ],
    "usp": [
        "technology", "technologies", "technologie", "tecnologia", "tecnologias",
        "innovazione", "innovation", "innovacion", "advantages", "benefits",
        "avantages", "vantaggi", "voordelen", "fordelar", "vyhody",
        "doorcooling", "instaview", "fresh balancer", "freshconverter", "thinq",
    ],
}

ATTRIBUTE_TERMS = {
    "hero": ["hero", "brand-banner", "brand_banner", "brandbanner"],
    "why_lg": ["why-lg", "why_lg", "whylg"],
    "usp": ["usp", "feature", "benefit", "technology", "technologie"],
    "faq": ["faq", "frequently-asked", "accordion"],
    "navigator": ["category-nav", "category_nav", "categorynav", "navigator", "category-tile"],
    "product_list": ["product-list", "product_list", "productlist", "product-grid", "product_grid"],
}

PRODUCT_URL_TERMS = [
    "/product/", "/products/", "/produkt/", "/produit/", "/prodotto/",
    "/p/", "/dp/", "productdetail", "product-detail",
]

CSV_FIELDS = [
    "리테일러", "요청 URL", "최종 URL", "수집 상태", "페이지 제목",
    "ID8 표시·로딩 이미지 수", "ID8 상위 이미지 수", "ID9 Title 수",
    "ID9 Meta Description 수", "ID9 H1 수", "ID9 Robots 수", "ID10 Canonical 수",
    "ID18 HTML 속성 후보 수", "ID18 큰 이미지 후보 수", "ID19 후보 수", "ID20 후보 수", "ID21 후보 수",
    "ID22 후보 수", "ID23 후보 수", "판정 상태", "상세 결과",
]


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object expected: {path}")
    return value


def normalized(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", text).strip().casefold()


def unique_text(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = re.sub(r"\s+", " ", str(value or "")).strip()
        if item and item not in seen:
            result.append(item)
            seen.add(item)
    return result


def unique_candidates(values: list[dict[str, object]], limit: int) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    seen: set[tuple[str, str, str]] = set()
    for value in values:
        key = (
            str(value.get("path") or ""),
            str(value.get("text") or "")[:500],
            json.dumps(value.get("matchedBy") or value.get("matchedTerms") or [], ensure_ascii=False, sort_keys=True),
        )
        if key in seen:
            continue
        result.append(value)
        seen.add(key)
        if len(result) >= limit:
            break
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def css_hint(tag: str, attrs: dict[str, str]) -> str:
    value = tag
    if attrs.get("id"):
        return f"{value}#{attrs['id']}"
    classes = [part for part in attrs.get("class", "").split() if part][:3]
    if classes:
        value += "".join(f".{part}" for part in classes)
    return value


@dataclass
class CaptureFrame:
    tag: str
    depth: int
    path: str
    groups: list[str]
    attrs: dict[str, str]
    parts: list[str] = field(default_factory=list)

    def add(self, value: str) -> None:
        if sum(len(part) for part in self.parts) < 4000:
            self.parts.append(value)

    def result(self) -> dict[str, object]:
        text = re.sub(r"\s+", " ", " ".join(self.parts)).strip()
        return {
            "tag": self.tag,
            "path": self.path,
            "matchedBy": self.groups,
            "text": text[:4000],
            "attributes": {key: value for key, value in self.attrs.items() if key in {
                "id", "class", "role", "aria-label", "data-testid", "data-component", "itemtype"
            }},
        }


class RawHtmlEvidenceParser(HTMLParser):
    """Collect headings, semantic candidates and FAQ structured data."""

    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    NON_CONTENT_TAGS = {"script", "style", "link", "meta", "use", "path", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, str]] = []
        self.frames: list[CaptureFrame] = []
        self.script_frames: list[CaptureFrame] = []
        self.headings: list[dict[str, object]] = []
        self.components: dict[str, list[dict[str, object]]] = {key: [] for key in ATTRIBUTE_TERMS}
        self.details: list[dict[str, object]] = []
        self.images: list[dict[str, str]] = []
        self.json_ld: list[object] = []

    def path(self, current: str) -> str:
        return " > ".join([item[1] for item in self.stack[-5:]] + [current])

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        hint = css_hint(tag, attrs)
        path = self.path(hint)
        depth = len(self.stack)
        semantic_attrs = [
            attrs.get(key, "") for key in (
                "id", "class", "role", "aria-label", "data-testid", "data-component", "itemtype"
            )
        ]
        attr_blob = normalized(" ".join([tag, *semantic_attrs]))
        groups = [
            group for group, terms in ATTRIBUTE_TERMS.items()
            if any(term in attr_blob for term in terms)
        ]
        if tag in self.NON_CONTENT_TAGS:
            groups = []
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.frames.append(CaptureFrame(tag, depth, path, ["heading"], attrs))
        if tag == "details":
            self.frames.append(CaptureFrame(tag, depth, path, ["details"], attrs))
        if groups:
            self.frames.append(CaptureFrame(tag, depth, path, groups, attrs))
        if tag == "script" and "ld+json" in attrs.get("type", "").casefold():
            frame = CaptureFrame(tag, depth, path, ["json_ld"], attrs)
            self.frames.append(frame)
            self.script_frames.append(frame)
        if tag == "img":
            self.images.append({
                "path": path,
                "src": attrs.get("src") or attrs.get("data-src") or attrs.get("data-lazy-src") or "",
                "alt": attrs.get("alt", ""),
                "class": attrs.get("class", ""),
                "width": attrs.get("width", ""),
                "height": attrs.get("height", ""),
            })
        if tag not in self.VOID_TAGS:
            self.stack.append((tag, hint))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID_TAGS:
            self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        value = data.strip()
        if not value:
            return
        for frame in self.frames:
            frame.add(value)

    def handle_endtag(self, tag: str) -> None:
        matching_index = next((index for index in range(len(self.stack) - 1, -1, -1) if self.stack[index][0] == tag), None)
        if matching_index is None:
            return
        ending_depth = matching_index
        closing = [frame for frame in self.frames if frame.depth >= ending_depth]
        self.frames = [frame for frame in self.frames if frame.depth < ending_depth]
        for frame in closing:
            result = frame.result()
            if "heading" in frame.groups:
                self.headings.append(result)
            if "details" in frame.groups:
                self.details.append(result)
            for group in frame.groups:
                if group in self.components:
                    self.components[group].append(result)
            if "json_ld" in frame.groups:
                try:
                    self.json_ld.append(json.loads(" ".join(frame.parts)))
                except (json.JSONDecodeError, TypeError):
                    pass
        del self.stack[matching_index:]

    def close(self) -> None:
        super().close()
        for frame in list(self.frames):
            result = frame.result()
            if "heading" in frame.groups:
                self.headings.append(result)
            if "details" in frame.groups:
                self.details.append(result)
            for group in frame.groups:
                if group in self.components:
                    self.components[group].append(result)
        self.frames.clear()


def keyword_matches(headings: list[dict[str, object]], group: str) -> list[dict[str, object]]:
    terms = TERM_GROUPS[group]
    matches: list[dict[str, object]] = []
    for heading in headings:
        text = normalized(heading.get("text"))
        path = normalized(heading.get("path"))
        if group == "usp" and any(term in path for term in ("product-list", "product_list", "product-card", "product_card")):
            continue
        matched = [term for term in terms if term in text]
        if matched:
            matches.append({**heading, "matchedTerms": matched})
    return matches


def faq_json_ld(values: list[object]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []

    def visit(value: object) -> None:
        if isinstance(value, list):
            for item in value:
                visit(item)
            return
        if not isinstance(value, dict):
            return
        kinds = value.get("@type")
        kinds = kinds if isinstance(kinds, list) else [kinds]
        if any(str(kind).casefold() == "faqpage" for kind in kinds):
            questions = []
            for item in value.get("mainEntity", []) if isinstance(value.get("mainEntity"), list) else []:
                if not isinstance(item, dict):
                    continue
                answer = item.get("acceptedAnswer") if isinstance(item.get("acceptedAnswer"), dict) else {}
                questions.append({"question": item.get("name", ""), "answer": answer.get("text", "")})
            results.append({"type": "FAQPage", "questions": questions})
        for child in value.values():
            if isinstance(child, (dict, list)):
                visit(child)

    for value in values:
        visit(value)
    return results


def top_images(state: dict[str, object], key: str) -> tuple[list[dict[str, object]], int]:
    images = [image for image in state.get("images", []) if isinstance(image, dict)]
    eligible = [image for image in images if image.get("visible") is True and image.get("loaded") is True]
    ordered = sorted(eligible, key=lambda image: float(image.get(key) or 0), reverse=True)
    return ordered[:10], len(eligible)


def topic_tokens(metadata: dict[str, object]) -> set[str]:
    values = [metadata.get("title", ""), *unique_text(metadata.get("h1"))]
    stop = {
        "with", "from", "pour", "avec", "voor", "alle", "tutti", "todos", "brand", "category", "page", "online",
        "coolblue", "amazon", "alza", "datart", "boulanger", "mediamarkt", "mediaworld", "elgiganten",
    }
    return {
        token for token in re.findall(r"[a-z0-9]+", normalized(" ".join(str(value) for value in values)))
        if len(token) >= 4 and token not in stop and token != "lg"
    }


def link_candidates(state: dict[str, object], final_url: str, metadata: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    clickables = [item for item in state.get("clickables", []) if isinstance(item, dict)]
    page_host = urlparse(final_url).netloc
    topics = topic_tokens(metadata)
    navigation: list[dict[str, object]] = []
    products: list[dict[str, object]] = []
    seen_nav: set[tuple[str, str]] = set()
    seen_product: set[tuple[str, str]] = set()
    model_pattern = re.compile(r"\b(?=[A-Z0-9-]{5,}\b)(?=[A-Z0-9-]*[A-Z])(?=[A-Z0-9-]*\d)[A-Z0-9-]+\b")

    for item in clickables:
        text = re.sub(r"\s+", " ", str(item.get("text") or item.get("ariaLabel") or "")).strip()
        href = urljoin(final_url, str(item.get("href") or ""))
        if not href or not text:
            continue
        lowered_href = href.casefold()
        product_signals = []
        if any(term in lowered_href for term in PRODUCT_URL_TERMS):
            product_signals.append("product-like URL")
        if "lg" in normalized(text) and model_pattern.search(text):
            product_signals.append("LG와 모델명 형태의 문구")
        if product_signals:
            key = (href, text[:200])
            if key not in seen_product and len(products) < 100:
                products.append({"text": text[:500], "href": href, "signals": product_signals})
                seen_product.add(key)
            continue

        text_tokens = set(re.findall(r"[a-z0-9]+", normalized(text)))
        same_host = not urlparse(href).netloc or urlparse(href).netloc == page_host
        shared = sorted(topics & text_tokens)
        if same_host and 1 <= len(text) <= 120 and shared:
            key = (href, text)
            if key not in seen_nav and len(navigation) < 100:
                navigation.append({"text": text, "href": href, "signals": [f"페이지 주제어와 일치: {', '.join(shared)}"]})
                seen_nav.add(key)
    return navigation, products


def metric(metric_id: str, evidence: dict[str, object], notes: list[str] | None = None) -> dict[str, object]:
    return {
        "metricId": metric_id,
        "metricName": METRICS[metric_id],
        "extractionStatus": "evidence_extracted",
        "assessment": {"status": "not_assessed", "value": None, "reason": "판정 규칙 적용 전"},
        "evidence": evidence,
        "notes": notes or [],
    }


def parse_page(page: Path, output_root: Path) -> tuple[dict[str, object], dict[str, object]]:
    retailer = page.parent.name
    raw_path = page / "raw.html"
    state_path = page / "capture-state.json"
    response_path = page / "response.json"
    state = read_json(state_path)
    response = read_json(response_path)
    metadata = state.get("metadata") if isinstance(state.get("metadata"), dict) else {}
    html = raw_path.read_text(encoding="utf-8", errors="replace")
    parser = RawHtmlEvidenceParser()
    parser.feed(html)
    parser.close()

    final_url = str(response.get("final_url") or state.get("url") or "")
    top_rendered, eligible_count = top_images(state, "renderedArea")
    top_natural, _ = top_images(state, "naturalArea")
    navigation_links, product_links = link_candidates(state, final_url, metadata)
    faq_structured = faq_json_ld(parser.json_ld)

    hero_candidates = unique_candidates(parser.components["hero"], 50)
    why_candidates = unique_candidates(keyword_matches(parser.headings, "why_lg") + parser.components["why_lg"], 50)
    usp_candidates = unique_candidates(keyword_matches(parser.headings, "usp") + parser.components["usp"], 100)
    faq_candidates = unique_candidates(keyword_matches(parser.headings, "faq") + parser.components["faq"], 100)
    navigator_candidates = unique_candidates(parser.components["navigator"], 50)
    product_list_candidates = unique_candidates(parser.components["product_list"], 50)
    faq_details = unique_candidates([
        item for item in parser.details
        if "?" in str(item.get("text") or "")
        or any(term in normalized(item.get("text")) for term in TERM_GROUPS["faq"])
    ], 100)

    metrics = {
        "ID8": metric("ID8", {
            "imageSelection": "원시 후보: visible=true와 loaded=true인 전체 이미지를 화면 표시 면적(renderedArea) 순으로 최대 10개 정렬. ID8 최종 대상은 별도 이미지 범위 검토에서 선정",
            "eligibleImageCount": eligible_count,
            "top10ByRenderedArea": top_rendered,
            "comparisonOnlyTop10ByNaturalArea": top_natural,
        }, ["D017~D019: 화면 표시 면적 순위, 본문 및 제품 카드 포함, CSS 배경·순수 장식 제외. 이 단계의 전체 이미지 상위 10개는 ID8 최종 대상이 아님"]),
        "ID9": metric("ID9", {
            "title": [str(metadata.get("title"))] if metadata.get("title") else [],
            "metaDescription": unique_text(metadata.get("metaDescription")),
            "h1": unique_text(metadata.get("h1")),
            "robots": unique_text(metadata.get("robots")),
        }),
        "ID10": metric("ID10", {"canonical": unique_text(metadata.get("canonical"))}),
        "ID18": metric("ID18", {
            "attributeCandidates": hero_candidates,
            "largeVisibleImages": top_rendered[:10],
            "renderedCandidateSnapshots": state.get("heroEvidence", {}).get("snapshots", {}),
        }, ["화면 위치·크기는 새 수집본에서만 제공되며, 상단 범위와 영상 인정 기준은 아직 미확정"]),
        "ID19": metric("ID19", {"headingOrAttributeCandidates": why_candidates}, ["Why LG 인정 문구와 USP 중복 처리 기준은 아직 미확정"]),
        "ID20": metric("ID20", {"headingOrAttributeCandidates": usp_candidates}, ["검색어 일치 후보이며 승인된 USP 기준자료와 대조하지 않음"]),
        "ID21": metric("ID21", {
            "attributeCandidates": navigator_candidates,
            "linkCandidates": navigation_links,
        }, ["후보 링크의 실제 도착 페이지와 작동 여부는 아직 검사하지 않음"]),
        "ID22": metric("ID22", {
            "attributeCandidates": product_list_candidates,
            "productLinkCandidates": product_links,
        }, ["제품 상세 페이지 도착 여부는 아직 검사하지 않음"]),
        "ID23": metric("ID23", {
            "headingOrAttributeCandidates": faq_candidates,
            "detailsElements": faq_details,
            "faqPageJsonLd": faq_structured,
        }, ["브랜드·제품군 관련 질문답변인지와 실제 화면 표시 여부는 아직 판정하지 않음"]),
    }

    output = {
        "schemaVersion": SCHEMA_VERSION,
        "page": {
            "retailer": retailer,
            "pageType": state.get("pageType") or response.get("page_type"),
            "requestedUrl": response.get("requested_url"),
            "finalUrl": final_url,
            "capturedAt": response.get("captured_at"),
            "collectionOk": response.get("ok") is True,
            "title": metadata.get("title") or state.get("title"),
        },
        "sources": {
            "rawHtml": {"path": str(raw_path.relative_to(page.parents[3])), "sha256": sha256(raw_path)},
            "captureState": {"path": str(state_path.relative_to(page.parents[3])), "sha256": sha256(state_path)},
            "response": {"path": str(response_path.relative_to(page.parents[3])), "sha256": sha256(response_path)},
            "screenshotRole": "페이지 상태를 사람이 참고하는 보조자료",
        },
        "parser": {
            "assessmentPerformed": False,
            "candidateRules": {
                "contentTerms": TERM_GROUPS,
                "attributeTerms": ATTRIBUTE_TERMS,
                "productUrlTerms": PRODUCT_URL_TERMS,
            },
        },
        "documentOutline": {"headings": parser.headings[:500]},
        "metrics": metrics,
    }

    target = output_root / retailer
    target.mkdir(parents=True, exist_ok=True)
    detail_path = target / "bcp-evidence.json"
    detail_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    row = {
        "리테일러": retailer,
        "요청 URL": response.get("requested_url", ""),
        "최종 URL": final_url,
        "수집 상태": "성공" if response.get("ok") is True else "실패",
        "페이지 제목": metadata.get("title") or state.get("title") or "",
        "ID8 표시·로딩 이미지 수": eligible_count,
        "ID8 상위 이미지 수": len(top_rendered),
        "ID9 Title 수": len(metrics["ID9"]["evidence"]["title"]),
        "ID9 Meta Description 수": len(metrics["ID9"]["evidence"]["metaDescription"]),
        "ID9 H1 수": len(metrics["ID9"]["evidence"]["h1"]),
        "ID9 Robots 수": len(metrics["ID9"]["evidence"]["robots"]),
        "ID10 Canonical 수": len(metrics["ID10"]["evidence"]["canonical"]),
        "ID18 HTML 속성 후보 수": len(hero_candidates),
        "ID18 큰 이미지 후보 수": len(top_rendered),
        "ID19 후보 수": len(why_candidates),
        "ID20 후보 수": len(usp_candidates),
        "ID21 후보 수": len(navigator_candidates) + len(navigation_links),
        "ID22 후보 수": len(product_list_candidates) + len(product_links),
        "ID23 후보 수": len(faq_candidates) + len(faq_details) + len(faq_structured),
        "판정 상태": "미판정",
        "상세 결과": str(detail_path.relative_to(output_root.parent)),
    }
    return output, row


def latest_batch() -> Path:
    batches = sorted(path for path in RESULTS_ROOT.iterdir() if path.is_dir() and (path / "pages").is_dir())
    if not batches:
        raise ValueError(f"No saved result batch: {RESULTS_ROOT}")
    return batches[-1]


def write_readme(batch: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Brand Category Page 1차 파서 결과",
        "",
        f"- 입력 수집 묶음: `{batch.name}`",
        f"- 처리 페이지: {len(rows)}개",
        "- 현재 단계: 9개 항목의 근거와 후보 추출",
        "- 판정 상태: 미판정",
        "- `screenshot.jpg` 역할: 페이지 상태를 사람이 참고하는 보조자료",
        "",
        "후보 수는 최종 Y/N 결과가 아니다. HTML 속성이나 다국어 검색어와 일치한 검토 대상을 뜻한다.",
        "",
        "| 리테일러 | ID18 Hero 속성 후보 | ID18 큰 이미지 후보 | ID19 Why LG 후보 | ID20 USP 후보 | ID21 Navigator 후보 | ID22 Product 후보 | ID23 FAQ 후보 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['리테일러']} | {row['ID18 HTML 속성 후보 수']} | {row['ID18 큰 이미지 후보 수']} | {row['ID19 후보 수']} | "
            f"{row['ID20 후보 수']} | {row['ID21 후보 수']} | {row['ID22 후보 수']} | {row['ID23 후보 수']} |"
        )
    lines.extend([
        "",
        "각 후보의 원문·HTML 위치·후보 선정 이유는 `parsed/<리테일러>/bcp-evidence.json`에서 확인한다.",
        "ID21과 ID22의 링크가 실제 목적지로 정상 이동하는지는 다음 링크 검사 단계에서 확인한다.",
    ])
    (batch / "파서_근거_요약.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("batch", nargs="?", type=Path, help="saved batch directory; defaults to latest")
    args = argument_parser.parse_args()
    batch = args.batch.resolve() if args.batch else latest_batch()
    pages = sorted((batch / "pages").glob("*/brand-category"))
    if not pages:
        raise ValueError(f"No BCP pages in batch: {batch}")

    output_root = batch / "parsed"
    rows: list[dict[str, object]] = []
    for page in pages:
        _, row = parse_page(page, output_root)
        rows.append(row)

    with (batch / "파서_근거_요약.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    write_readme(batch, rows)

    manifest_path = batch / "manifest.json"
    manifest = read_json(manifest_path)
    manifest["parser"] = {
        "schema_version": SCHEMA_VERSION,
        "page_count": len(rows),
        "assessment_status": "not performed",
        "details_directory": "parsed",
        "summary_csv": "파서_근거_요약.csv",
        "summary_markdown": "파서_근거_요약.md",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(batch / "파서_근거_요약.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
