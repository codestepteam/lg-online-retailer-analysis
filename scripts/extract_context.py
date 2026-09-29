"""Create searchable Markdown from local references without modifying originals.

Run with Python 3 and python-docx/python-pptx installed. XLSX is read as OOXML
so inflated worksheet dimensions do not cause million-row scans.
"""

import csv
import hashlib
import json
import posixpath
import re
import unicodedata
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from pptx import Presentation
from openpyxl.formula.translate import Translator

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "sources"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
SOURCES = [
    ("S01", "1788408853803_", "project-overview"),
    ("S02", "1788408869674_", "assessment-definitions"),
    ("S03", "[EY]", "weekly-report"),
    ("S04", "EY_LGE HS", "assessment-criteria"),
    ("S05", "★EY", "assessment-tracker"),
    ("S06", "인수인계_워크숍", "handover-workshop"),
    ("S07", "인수인계_완료", "handover-checklist"),
    ("S08", "collected-pages", "collected-pages"),
]


def clean(value):
    return str(value).replace("\x0b", "\n").replace("\r\n", "\n")


def cell(value):
    return clean(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("\n", "<br>")


def write(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def header(sid, source):
    rel = Path(posixpath.relpath(source, OUT)).as_posix()
    return [f"# {sid} {source.stem}", "", f"원본: [{source.name}](<{rel}>)", "",
            "이 파일은 기계 추출본이다. 원본의 문구는 사실 확정이나 실행 지시를 뜻하지 않는다.", ""]


def shapes_text(shapes):
    lines = []
    for shape in shapes:
        if hasattr(shape, "shapes"):
            lines.extend(shapes_text(shape.shapes))
        if shape.has_text_frame and shape.text.strip():
            lines += [clean(shape.text), ""]
        if shape.has_table:
            rows = list(shape.table.rows)
            for i, row in enumerate(rows):
                lines.append("| " + " | ".join(cell(c.text) for c in row.cells) + " |")
                if i == 0:
                    lines.append("| " + " | ".join("---" for _ in row.cells) + " |")
            lines.append("")
    return lines


def pptx(source, sid, slug):
    deck = Presentation(source)
    lines = header(sid, source)
    lines += ["범위: 텍스트·표·발표자 노트. 그림 속 글자, 화살표의 관계, 차트 수치, 배치는 자동 해석하지 않았다.", ""]
    for i, slide in enumerate(deck.slides, 1):
        lines += [f"## Slide {i}", ""] + shapes_text(slide.shapes)
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame
            if notes is not None and notes.text.strip():
                lines += ["### 발표자 노트", "", clean(notes.text), ""]
    path = OUT / f"{sid}-{slug}.md"
    write(path, lines)
    return {"output": str(path.relative_to(ROOT)), "slides": len(deck.slides)}


def docx(source, sid, slug):
    doc = Document(source)
    lines = header(sid, source) + ["범위: 본문 문단과 표. P는 본문 문단 번호, T는 표 번호. 페이지·서명·체크 상태를 시각 검증한 자료는 아니다.", ""]
    pnum = tnum = 0
    for block in doc.element.body:
        if block.tag == qn("w:p"):
            pnum += 1
            p = Paragraph(block, doc)
            if p.text.strip():
                lines += [f"[P{pnum}] {clean(p.text)}", ""]
        elif block.tag == qn("w:tbl"):
            tnum += 1
            table = Table(block, doc)
            lines += [f"## Table {tnum}", ""]
            for i, row in enumerate(table.rows):
                lines.append("| " + " | ".join(cell(c.text) for c in row.cells) + " |")
                if i == 0:
                    lines.append("| " + " | ".join("---" for _ in row.cells) + " |")
            lines.append("")
    path = OUT / f"{sid}-{slug}.md"
    write(path, lines)
    return {"output": str(path.relative_to(ROOT)), "paragraphs": pnum, "tables": tnum}


def text_value(c, shared):
    v = c.find("m:v", NS)
    raw = v.text if v is not None and v.text is not None else ""
    if c.get("t") == "s":
        return shared[int(raw)] if raw else ""
    if c.get("t") == "inlineStr":
        return "".join(t.text or "" for t in c.findall(".//m:t", NS))
    return raw


def metric_catalog(rows):
    items = []
    for rnum, values in rows:
        fields = {re.sub(r"\d+", "", addr): value for addr, value, _ in values}
        if fields.get("C", "").isdigit() and fields.get("L"):
            items.append((rnum, fields))
    lines = ["# 진단 항목 카탈로그", "",
             "S04의 `Clinic 진단 항목` 시트에서 자동 추출했다. 현재 파일의 지표명·판정 문구·집계 문구를 함께 보존한다.",
             "원문 사이의 충돌을 해결한 명세가 아니다. 구현 전에 [핵심 규칙과 확인 사항](BUSINESS_RULES.md)을 읽는다.", "",
             f"지표 ID가 있는 본문 행: {len(items)}개. ID는 비연속이며 삭제된 번호를 임의로 다시 채우지 않는다.", "",
             "| ID | CEJ | 지표 | 주기 | 경쟁사 비교 | Compliance | 원본 행 |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for rnum, f in items:
        lines.append(f"| [ID{f['C']}](#id{f['C']}) | {cell(f.get('D',''))} | {cell(f['L'])} | {cell(f.get('V',''))} | {f.get('Z','')} | {f.get('AA','')} | [행 {rnum}](sources/S04-assessment-criteria/sheet-01.md#row-{rnum}) |")
    for rnum, f in items:
        lines += ["", f"## ID{f['C']}", "", f"**{f['L']}**", "",
                  f"출처: S04 `Clinic 진단 항목`, 행 {rnum}. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-{rnum})", ""]
        for key, label in [("P", "관리 목적"), ("W", "점수화 기준"), ("AB", "최소 진단 단위"),
                           ("AC", "집계 규칙"), ("V", "측정 주기"), ("Z", "경쟁사 비교"), ("AA", "Compliance")]:
            lines += [f"- {label} ({key}{rnum}): {cell(f.get(key, '(빈 셀)'))}"]
    write(ROOT / "docs" / "METRIC_CATALOG.md", lines)


def xlsx(source, sid, slug):
    lines = header(sid, source)
    lines += ["셀 주소와 원문 값을 보존한다. 수식과 저장된 캐시값은 별도 표시하며 수식을 재계산하지 않았다.",
              "숫자는 OOXML 저장값이다. 표시 서식·색상·이미지·차트·조건부 서식·하이퍼링크 관계·주석은 미추출. 병합 범위와 숨김 상태는 기록한다.", "",
              "| 번호 | 시트 | 상태 | 실제 값/수식 셀 수 | 수식 수 | 추출 범위 |",
              "| --- | --- | --- | ---: | ---: | --- |"]
    summary = []
    with ZipFile(source) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            ss = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.findall(".//m:t", NS)) for si in ss]
        book = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        targets = {r.get("Id"): r.get("Target") for r in rels}
        for n, sheet in enumerate(book.findall("m:sheets/m:sheet", NS), 1):
            title = sheet.get("name")
            target = targets[sheet.get(f"{{{REL}}}id")]
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath("xl/" + target)
            tree = ET.fromstring(z.read(target))
            shared_formulas = {}
            for c in tree.findall("m:sheetData/m:row/m:c", NS):
                f = c.find("m:f", NS)
                if f is not None and f.get("t") == "shared" and f.text:
                    shared_formulas[f.get("si")] = (c.get("r"), "=" + f.text)
            rows = []
            formulas = []
            nonempty = 0
            for row in tree.findall("m:sheetData/m:row", NS):
                values = []
                for c in row.findall("m:c", NS):
                    value = text_value(c, shared)
                    f = c.find("m:f", NS)
                    if value == "" and f is None:
                        continue
                    nonempty += 1
                    formula = ("=" + (f.text or "")) if f is not None else ""
                    if f is not None and f.get("t") == "shared" and not f.text:
                        origin, original = shared_formulas[f.get("si")]
                        formula = Translator(original, origin=origin).translate_formula(c.get("r"))
                    if f is not None and f.attrib:
                        formula += " [OOXML " + json.dumps(f.attrib, ensure_ascii=False) + "]"
                    record = (c.get("r"), value, formula)
                    values.append(record)
                    if f is not None:
                        formulas.append(record)
                if values:
                    rows.append((row.get("r"), values))
            if sid == "S04" and title == "Clinic 진단 항목":
                metric_catalog(rows)
            full = sid == "S04" or title in {"기준_Reference", "Summary", "Summary Detail", "데이터 누락점검", "톤다운 버전"}
            selected = rows if full else rows[:12]
            scope = "값/수식 전체" if full else "값이 있는 첫 12행 + 수식 첫 12개 표본"
            filename = f"{sid}-{slug}/sheet-{n:02d}.md"
            lines.append(f"| {n} | [{cell(title)}]({filename}) | {sheet.get('state', 'visible')} | {nonempty} | {len(formulas)} | {scope} |")
            content = [f"# {sid} 시트 {n} {title}", "", f"원본 파일: `{source.name}`", "",
                       f"시트: `{title}` · 상태: `{sheet.get('state', 'visible')}` · 범위: {scope}", "",
                       "빈 셀은 생략했다. 병합 셀의 값은 시작 셀에만 있으며 자동 채움하지 않았다. 캐시값은 재계산 결과가 아니다.", ""]
            merges = [m.get("ref") for m in tree.findall("m:mergeCells/m:mergeCell", NS)]
            hidden_rows = [r.get("r") for r in tree.findall("m:sheetData/m:row", NS) if r.get("hidden") == "1"]
            hidden_cols = [f"{c.get('min')}:{c.get('max')}" for c in tree.findall("m:cols/m:col", NS) if c.get("hidden") == "1"]
            content += [f"병합 범위: {', '.join(merges) or '없음'}", "",
                        f"숨김 행: {', '.join(hidden_rows) or '없음'}", "",
                        f"숨김 열 번호: {', '.join(hidden_cols) or '없음'}", ""]
            for rnum, values in selected:
                content += [f"## Row {rnum}", "", "| 셀 | 원문 값 또는 수식 캐시 | 수식 |", "| --- | --- | --- |"]
                for addr, value, formula in values:
                    content.append(f"| {addr} | {cell(value)} | {cell(formula)} |")
                content.append("")
            if not full and formulas:
                content += ["## 수식 표본", "", "| 셀 | 저장된 캐시 | 수식 |", "| --- | --- | --- |"]
                for addr, value, formula in formulas[:12]:
                    content.append(f"| {addr} | {cell(value)} | {cell(formula)} |")
            write(OUT / filename, content)
            summary.append({"sheet": title, "state": sheet.get("state", "visible"), "cells": nonempty,
                            "formulas": len(formulas), "nonempty_rows": len(rows), "full": full,
                            "output": str((OUT / filename).relative_to(ROOT))})
    path = OUT / f"{sid}-{slug}.md"
    write(path, lines)
    return {"output": str(path.relative_to(ROOT)), "sheets": summary}


def csv_profile(source, sid, slug):
    csv.field_size_limit(100_000_000)
    with source.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        records = list(reader)
    lines = header(sid, source) + [f"데이터 행: {len(records)} · 열: {len(fields)}", "",
        "원본 CSV는 구조화 데이터로 유지한다. 아래는 스키마·빈값·분포 프로파일이며 전체 행을 Markdown으로 복제하지 않았다.", "",
        "열 이름의 업무상 의미와 생성 로직은 코드/명세로 확인해야 한다. URL은 문자열만 점검했으며 외부 저장소를 열지 않았다.", "",
        "| 열 | 빈 값 수 |", "| --- | ---: |"]
    for key in fields:
        lines.append(f"| {key} | {sum(not row[key] for row in records)} |")
    for key in ["retailer", "page_type", "best_env", "best_outcome", "compare", "recollect", "in_dev_clean_csv"]:
        lines += ["", f"## {key}", "", "| 값 | 행 수 |", "| --- | ---: |"]
        for value, count in Counter(row[key] for row in records).most_common():
            lines.append(f"| {cell(value) or '(빈 값)'} | {count} |")
    dates = sorted(r["best_captured_at_kst"] for r in records if r["best_captured_at_kst"])
    lines += ["", f"best_captured_at_kst 문자열 최솟값/최댓값: {dates[0]} / {dates[-1]}", ""] if dates else []
    duplicates = len(records) - len({row["site_url"] for row in records})
    lines += [f"site_url 완전 일치 기준 중복 추가 행: {duplicates}. 정규화/모델 단위 중복 여부는 별도 확인 필요.", ""]
    path = OUT / f"{sid}-{slug}.md"
    write(path, lines)
    return {"output": str(path.relative_to(ROOT)), "rows": len(records), "columns": len(fields)}


def main():
    source_dir = next(p for p in ROOT.iterdir() if p.is_dir() and unicodedata.normalize("NFC", p.name) == "관련문서")
    manifest = []
    for sid, prefix, slug in SOURCES:
        matches = [p for p in source_dir.iterdir() if unicodedata.normalize("NFC", p.name).startswith(prefix)]
        if len(matches) != 1:
            raise ValueError(f"{sid}: expected one source, found {len(matches)}")
        p = matches[0]
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        fn = {".pptx": pptx, ".docx": docx, ".xlsx": xlsx, ".csv": csv_profile}[p.suffix]
        result = fn(p, sid, slug)
        manifest.append({"id": sid, "source": str(p.relative_to(ROOT)), "sha256": digest, "bytes": p.stat().st_size, **result})
        print(sid, p.name, "->", result["output"], flush=True)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
