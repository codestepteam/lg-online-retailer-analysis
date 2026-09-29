#!/usr/bin/env python3
"""Keep the earlier assessment beside current captures for comparison, never as current labels."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

import openpyxl


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "관련문서" / "★EY_LGE_Clinic_Assessment Summary_Improvement Tracker_V0.1_20260911 (1).xlsx"
SHEET = "ID18_19_20_21_22_23"


def url_key(value: str) -> tuple[str, str]:
    url = urlsplit(str(value).strip().splitlines()[0])
    return url.hostname or "", url.path.rstrip("/")


def run(batch: Path) -> dict:
    manifest = json.loads((batch / "manifest.json").read_text())
    book = openpyxl.load_workbook(SOURCE, read_only=True, data_only=True)
    sheet = book[SHEET]
    earlier: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row_number, row in enumerate(sheet.iter_rows(min_row=7, max_col=12, values_only=True), start=7):
        metric = row[1]
        if metric not in (18, 19, 20, 21, 22, 23) or not row[7]:
            continue
        earlier[url_key(str(row[7]))].append({
            "metricId": f"ID{metric}", "sourceSheetRow": row_number, "country": row[2],
            "brand": row[3], "retailer": row[4], "category": row[5],
            "recordedLabel": row[10], "recordedReason": row[11], "recordedUrl": row[7],
        })
    result = {"role": "historical comparison only, not current assessment", "sourceWorkbook": str(SOURCE.relative_to(ROOT)),
              "sheet": SHEET, "sheetUpdateLabel": "2026-08-26", "pages": []}
    for record in manifest["records"]:
        if record["pageType"] != "Brand Category Page":
            continue
        matched = [entry for entry in earlier.get(url_key(record["url"]), [])
                   if str(entry["brand"]).casefold() == str(record["brand"]).casefold()]
        result["pages"].append({"sourceWorkbookRow": record["sourceRow"], "pageKey": record["pageKey"],
                                "url": record["url"], "earlierResults": matched})
    output = batch / "과거_판정_비교자료.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)
    print(dict(Counter(len(item["earlierResults"]) for item in result["pages"])))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    args = parser.parse_args()
    run(args.batch.resolve())


if __name__ == "__main__":
    main()
