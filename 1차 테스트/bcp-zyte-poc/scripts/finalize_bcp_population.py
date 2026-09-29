#!/usr/bin/env python3
"""Combine source-locked automated checks with reviewed content and link evidence."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

METRICS = ("ID8", "ID9", "ID10", "ID18", "ID19", "ID20", "ID21", "ID22", "ID23")

# Each note identifies the visible/HTML passage reviewed; None means the required
# block was absent in the captured page. These are AI review findings, not source
# workbook outcomes and not user-approved labels.
CONTENT: dict[int, dict[str, str | None]] = {
    14: {"ID18": "상단 LG 냉장고 가로 이미지(screenshot.jpg)", "ID19": "LG 냉장고 혁신·절전·InstaView 선택 이유(본문 block-00011)", "ID20": "Total No Frost·NatureFresh·컴프레서 장점(본문 block-00012)", "ID23": "외출 중 냉장고 온도 조절 질문과 LG ThinQ 원격 조절 답(본문 block-00011)", "ID21": "냉장고 하위 제품군 이미지·텍스트 링크 7개(본문 block-00012)"},
    15: {"ID18": "상단 LG 세탁기 가로 이미지(screenshot.jpg)", "ID19": "LG 세탁기의 세탁력·절전·AI DD 선택 이유(본문 block-00011)", "ID20": "TurboWash·6 Motion·ThinQ 기능과 효익(본문 block-00012~15)", "ID23": "LG 세탁기의 차별점 질문과 설명(본문 block-00017~18)", "ID21": "세탁기 하위 제품군 이미지·텍스트 링크 5개(본문 block-00012~15)"},
    16: {"ID18": "상단 LG 건조기 가로 이미지(screenshot.jpg)", "ID19": "LG 건조기의 절전·자동 세척·친환경 선택 이유(본문 block-00011)", "ID20": "듀얼 인버터 히트펌프·Eco Hybrid 장점(본문 block-00012~15)", "ID23": "'왜 LG 건조기인가' 질문과 장점 설명(본문 block-00016~17)", "ID21": "건조기 관련 하위 제품군 이미지·텍스트 링크 5개(본문 block-00012~15)"},
    38: {"ID18": None, "ID19": "LG 냉장고의 저소음·저전력·실용성 선택 이유(본문 block-00005)", "ID20": None, "ID23": None, "ID21": "상단 LG 냉장고 하위 제품군 타일 11개(raw.html의 subcategory-box-list)"},
    39: {"ID18": None, "ID19": None, "ID20": None, "ID23": None, "ID21": "상단 LG 건조기 하위 제품군 타일 8개(raw.html의 subcategory-box-list; 액세서리 링크는 별도)"},
    50: {"ID18": None, "ID19": "LG 냉장고 보관·편의성의 브랜드 선택 이유(본문 block-00007, block-00515)", "ID20": "InstaView·Multi Air Flow·Door Cooling+ 효익 설명(본문 block-00515)", "ID23": "LG 냉장고 품질·온도 설정 질문과 답변(본문 block-00515)", "ID21": None},
    51: {"ID18": "상단 LG 세탁기 판촉 가로 배너(screenshot.jpg)", "ID19": "Direct Drive의 내구성·저소음 선택 이유(본문 block-00498)", "ID20": "Direct Drive·Steam·TurboWash 효익 설명(본문 block-00498)", "ID23": "LG 세탁기 품질·수명 질문과 답변(본문 block-00498)", "ID21": None},
    74: {"ID18": "상단 LG 냉장고 브랜드·제품군 배너(screenshot.jpg)", "ID19": None, "ID20": None, "ID23": None, "ID21": None},
    75: {"ID18": "상단 LG 세탁기 브랜드·제품군 배너(screenshot.jpg)", "ID19": None, "ID20": None, "ID23": None, "ID21": None},
    76: {"ID18": "상단 LG 건조기 브랜드·제품군 배너(screenshot.jpg)", "ID19": None, "ID20": None, "ID23": None, "ID21": None},
    77: {"ID18": "상단 LG 세탁건조기 브랜드·제품군 배너(screenshot.jpg)", "ID19": None, "ID20": None, "ID23": None, "ID21": None},
    92: {"ID18": None, "ID19": "LG 냉장고 보존성·신뢰성 소개(본문 block-00217)", "ID20": None, "ID23": None, "ID21": None},
    93: {"ID18": None, "ID19": "LG 건조기 효율·성능 소개(본문 block-00114)", "ID20": None, "ID23": None, "ID21": None},
    94: {"ID18": None, "ID19": "LG 세탁기 효율·성능 소개(본문 block-00217)", "ID20": None, "ID23": None, "ID21": "상단 LG 세탁기 8kg·9kg 카테고리 타일(raw.html)"},
    112: {"ID18": "상단 냉장고 이미지와 LG 하위 제품군 카드(screenshot.jpg)", "ID19": "Fresh Converter를 통한 신선 보관과 절전 선택 이유(본문 block-00005)", "ID20": "절전량과 LG 냉장고 기능을 설명하는 별도 영역(본문 block-00011)", "ID23": "절전 희망 질문과 LG 고효율 냉장고 답(본문 block-00005)", "ID21": "상단 LG 냉장고 하위 제품군 카드 2개(본문 block-00005)"},
    113: {"ID18": None, "ID19": "LG Direct Drive 저소음 선택 이유(본문 block-00009)", "ID20": None, "ID23": None, "ID21": None},
    114: {"ID18": None, "ID19": "Direct Drive 저소음·Steam+ 위생 세탁 선택 이유(본문 block-00009)", "ID20": None, "ID23": "빠른 세탁 질문과 TurboWash 39분 세탁 답(본문 block-00009)", "ID21": None},
    126: {"ID18": None, "ID19": "LG 냉장고의 혁신·품질·절전 선택 이유(본문 block-00108)", "ID20": "DoorCooling+·ThinQ·InstaView·NoFrost별 효익 설명(본문 block-00108)", "ID23": None, "ID21": None},
    127: {"ID18": None, "ID19": "LG 세탁기의 품질·혁신·저소음 선택 이유(본문 block-00060, block-00071)", "ID20": "AI·TurboWash·Steam+·자동 투입의 효익(본문 block-00063~69)", "ID23": "적합한 LG 세탁기 질문과 선택 기준 답(본문 block-00072~73)", "ID21": None},
    141: {"ID18": None, "ID19": "LG 식기세척기 적재·세척 장점(본문 block-00143~46)", "ID20": None, "ID23": "QuadWash·TrueSteam 질문과 펼친 답변(본문 block-00143~46; capture-state.json faqExpansion)", "ID21": None},
    142: {"ID18": None, "ID19": "LG 냉장고의 혁신·효율·보관 선택 이유(본문 block-00225)", "ID20": None, "ID23": "LG 냉장고 기술 질문과 펼친 답변(본문 block-00225~27; capture-state.json faqExpansion)", "ID21": "상단 LG 냉장고 두 하위 제품군 원형 카드(screenshot.jpg)"},
    143: {"ID18": None, "ID19": "LG 세탁기의 TurboWash·6Motion·ThinQ 선택 이유(본문 block-00211)", "ID20": None, "ID23": "LG 세탁기 효율·기술 질문과 펼친 답변(본문 block-00212~19; capture-state.json faqExpansion)", "ID21": "상단 LG 세탁기 하위 제품군 원형 카드 3개(screenshot.jpg)"},
    155: {"ID18": None, "ID19": "LG 냉장고 디자인·온도 관리로 신선도 향상(본문 block-00020)", "ID20": None, "ID23": None, "ID21": None},
    156: {"ID18": None, "ID19": "LG 세탁기의 저소음·내구성 선택 이유(본문 block-00021)", "ID20": "Direct Drive·AI Wash·6 Motion 효익 영역(본문 block-00021)", "ID23": None, "ID21": "상단 LG 세탁기·건조기 하위 제품군 카드 2개(본문 block-00019)"},
}

ABSENT_REASON = {
    "ID18": "상단에 해당 LG 제품군의 이미지형 대표 배너가 없음",
    "ID19": "브랜드를 선택할 이유·차별성을 설명하는 본문 영역이 없음",
    "ID20": "독립된 제품군 핵심 기술·효익 블록이 확인되지 않음(제품명·일반 소개·FAQ만으로는 인정하지 않음)",
    "ID23": "이 페이지 본문에서 해당 LG 제품군의 텍스트 질문과 대응 답변을 확인하지 못함",
    "ID21": "LG 제품군을 나누어 보여주는 전용 탐색 블록이 없음(일반 탐색·필터·본문 링크는 제외)",
}


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def valid_destination(item: dict[str, object]) -> bool:
    if item.get("status") != 200:
        return False
    title = str(item.get("title") or "")
    h1 = str(item.get("h1") or "")
    if re.search(r"captcha|confirm you are human|verify you are human", title + h1, re.I):
        return False
    return bool(re.search(r"\bLG\b", title + " " + h1, re.I))


def link_verdict(batch: Path, key: str, kind: str) -> tuple[str, str, list[dict[str, object]]]:
    path = batch / "link-check" / f"{key}.json"
    if not path.is_file():
        return "REVIEW", "이동 주소의 도착 페이지를 검사하지 못함", []
    primary = read_json(path)
    direct_path = batch / "link-check-direct" / f"{key}.json"
    direct = read_json(direct_path).get("results", []) if direct_path.is_file() else []
    direct_by_url = {str(x.get("url")): x for x in direct}
    checks = []
    for item in primary.get("results", []):
        if item.get("kind") != kind:
            continue
        selected = item if valid_destination(item) else direct_by_url.get(str(item.get("url")), item)
        checks.append({"url": item.get("url"), "label": item.get("label"), "status": selected.get("status"),
                       "finalUrl": selected.get("finalUrl"), "title": selected.get("title"),
                       "h1": selected.get("h1"), "error": selected.get("error"),
                       "method": "direct visit" if selected is not item else "same-origin fetch"})
    if not checks:
        return "REVIEW", "확인 대상 링크가 선택되지 않음", checks
    failures = [x for x in checks if not valid_destination(x)]
    if not failures:
        return "Y", f"검사한 {len(checks)}개 링크가 LG 관련 도착 페이지로 열림", checks
    broken = [x for x in failures if x.get("status") in (404, 410)]
    if broken:
        return "N", f"링크 {len(broken)}개가 404/410 응답: " + ", ".join(str(x["url"]) for x in broken), checks
    wrong_landing = [x for x in failures if x.get("status") == 200 and
                     not re.search(r"\bLG\b", str(x.get("title") or "") + " " + str(x.get("h1") or ""), re.I)]
    if wrong_landing:
        return "N", "LG 제품군이 아닌 페이지로 이동한 링크: " + "; ".join(
            f"{x['url']} → {x.get('finalUrl')} ({x.get('title')})" for x in wrong_landing), checks
    return "REVIEW", f"검사한 {len(checks)}개 중 {len(failures)}개 도착을 확인하지 못함(차단·오류·내용 불일치)", checks


def main(batch: Path) -> None:
    manifest = read_json(batch / "manifest.json")
    rows = []
    details = []
    for record in manifest["records"]:
        row = int(record["sourceRow"])
        key = str(record["pageKey"])
        base = read_json(batch / "assessed" / key / "bcp-assessment.json")
        results = {metric: base["results"][metric] for metric in ("ID8", "ID9", "ID10")}
        notes = CONTENT[row]
        for metric in ("ID18", "ID19", "ID20", "ID23"):
            note = notes[metric]
            reason = note if note else ABSENT_REASON[metric]
            if row == 50 and metric == "ID18":
                reason = "상단 가로 광고는 Whirlpool 제품으로 LG 냉장고 배너가 아님"
            if metric == "ID20" and row in (141, 142, 143):
                reason = "LG 기술 설명은 FAQ에 있으나 별도의 핵심 USP 블록은 확인되지 않음"
            if metric == "ID23" and row in (113,):
                reason = "관련 조언 링크는 있으나 이 페이지 본문에 질문·답변 쌍이 없음"
            results[metric] = {"status": "Y" if note else "N", "reason": reason,
                               "evidence": {"capture": f"pages/{key}/brand-category/raw.html",
                                            "visual": f"pages/{key}/brand-category/screenshot.jpg"}}
        nav_note = notes["ID21"]
        if nav_note:
            status, reason, checks = link_verdict(batch, key, "navigator")
            results["ID21"] = {"status": status, "reason": f"{nav_note}; {reason}", "evidence": {"linkChecks": checks}}
        else:
            results["ID21"] = {"status": "N", "reason": ABSENT_REASON["ID21"], "evidence": {"capture": f"pages/{key}/brand-category/raw.html"}}
        status, reason, checks = link_verdict(batch, key, "product")
        results["ID22"] = {"status": status, "reason": f"LG 제품 카드가 있음; {reason}; 검사 범위는 서로 다른 첫 2개 제품 카드",
                           "evidence": {"linkChecks": checks, "coverage": "first two distinct LG product cards; remaining cards not destination-tested"}}
        details.append({"pageKey": key, "sourceWorkbookRow": row, "country": record["country"],
                        "retailer": record["retailer"], "brand": record["brand"],
                        "categoryCode": record["categoryCode"], "subcategory": record["subcategory"],
                        "url": record["url"], "results": results,
                        "reviewStatus": "2026-09-28 AI review; user approval not implied"})
        rows.append({"엑셀 행": row, "국가": record["country"], "리테일러": record["retailer"],
                     "제품군": record["subcategory"], "URL": record["url"],
                     **{metric: results[metric]["status"] for metric in METRICS}})
    (batch / "판정_최종_상세.json").write_text(json.dumps(details, ensure_ascii=False, indent=2) + "\n")
    with (batch / "판정_최종_전체URL.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    counts = {metric: Counter(d["results"][metric]["status"] for d in details) for metric in METRICS}
    lines = ["# LG Brand Category Page 24개 URL 판정", "",
             "대상: `Brand_BCP_1차_테스트_URL_목록.xlsx`의 LG Brand Category Page 24개. 2026-09-28 Zyte 수집본 기준 AI 판정이다.",
             "ID8~10은 자동 검사와 이미지별 검수를 반영했다. ID18~20·23은 저장된 화면과 본문을 읽고 판정했다.",
             "ID21은 해당 LG 제품군의 탐색 블록 링크 전부, ID22는 서로 다른 첫 두 제품 카드 링크를 검사했다. 따라서 ID22 Y는 페이지의 모든 제품 카드 검증을 뜻하지 않는다.", "",
             "| 항목 | Y | N | 확인 필요 |", "| --- | ---: | ---: | ---: |"]
    for metric in METRICS:
        c = counts[metric]
        lines.append(f"| {metric} | {c['Y']} | {c['N']} | {c['REVIEW']} |")
    lines += ["", "| 국가 | 리테일러 | 제품군 | URL | " + " | ".join(METRICS) + " |",
              "| --- | --- | --- | --- | " + " | ".join("---" for _ in METRICS) + " |"]
    for d in details:
        vals = [d["country"], d["retailer"], d["subcategory"], f"[열기]({d['url']})"]
        vals += [d["results"][metric]["status"] for metric in METRICS]
        lines.append("| " + " | ".join(vals) + " |")
    lines += ["", "각 URL의 항목별 이유와 검사한 링크·도착 페이지는 `판정_최종_상세.json`에 있다. 원본은 `pages/<페이지>/brand-category/raw.html`, 화면 참고는 같은 폴더의 `screenshot.jpg`다.",
              "판정은 제공된 Concentrix 결과를 복사하지 않고 이번 수집본에서 독립적으로 했다. 과거 결과와의 차이는 수집 시점과 기준 차이를 구분해 비교해야 한다."]
    (batch / "판정_최종_전체URL.md").write_text("\n".join(lines) + "\n")
    print(batch / "판정_최종_전체URL.md")
    print(json.dumps({m: dict(c) for m, c in counts.items()}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main(Path(sys.argv[1]).resolve())
    except (IndexError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"BCP final assessment failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
