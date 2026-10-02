"""Offline checks against the saved first-test BCP captures."""

from __future__ import annotations

import csv
import json
import runpy
import sys
from pathlib import Path

from compile_capture import compile_request


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "1차 테스트" / "bcp-zyte-poc" / "results_population" / "20260928-all-159"


def main():
    rows = json.loads((ROOT / "inputs" / "bcp-urls.json").read_text(encoding="utf-8"))["records"]
    if len(rows) != 139:
        raise AssertionError(f"expected 139 first-test BCP input rows, got {len(rows)}")
    sys.path.insert(0, str(ROOT.parent / "1차 테스트" / "bcp-zyte-poc" / "scripts"))
    from capture_bcp_population import prepared_recipe
    for row in rows:
        request = compile_request(row["retailerSlug"], row)
        if request.get("browserHtml") is not True or request.get("screenshot") is not True:
            raise AssertionError(f"capture request is incomplete: {row['sourceRow']}")
        if request != prepared_recipe(row)[1]:
            raise AssertionError(f"Zyte request changed during conversion: {row['sourceRow']}")
    with (SOURCE / "전체_URL_판정_진행상태.csv").open(encoding="utf-8-sig", newline="") as stream:
        first_scores = {int(row["엑셀 행"]): row for row in csv.DictReader(stream)
                        if row["엑셀 행"].isdigit()}
    checked = 0
    source_rows = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))["records"]
    for row in source_rows:
        retailer = row["retailerSlug"]
        if row["pageType"] != "Brand Category Page" or row.get("collectionStatus") not in {"captured", "seeded", "reused"}:
            continue
        page = SOURCE / "pages" / row["pageKey"] / "brand-category"
        if not (page / "raw.html").is_file():
            continue
        response = json.loads((page / "response.json").read_text(encoding="utf-8"))
        bundle = {"html": (page / "raw.html").read_text(encoding="utf-8"),
                  "raw_uri": "file:///saved/raw.html", "screenshot_uri": "file:///saved/screenshot.jpg",
                  "target": {"url": row["url"], "retailer": retailer, "page_type": "bcp",
                             "brand": row["brand"], "product_category": row["subcategory"] or "",
                             "product_name": ""},
                  "response": {"url": response["final_url"]}}
        parser = ROOT / "retailers" / retailer / "scenarios" / "bcp" / "parser" / "bcp.py"
        observation = runpy.run_path(str(parser))["parse"](bundle)
        if (observation.get("schema_version") != "lg-diagnostic-observation-v1" or
                set(observation.get("facts", {}).get("bcp_evidence", {})) !=
                {"ID8", "ID9", "ID10", "ID18", "ID19", "ID20", "ID21", "ID22", "ID23"} or
                len(json.dumps(observation, ensure_ascii=False).encode("utf-8")) > 2 * 1024 * 1024):
            raise AssertionError(f"invalid BCP observation: {retailer}")
        for mid in ("9", "10", "18"):
            scorer = ROOT / "scoring" / "bcp" / "v1" / f"id_{mid}.py"
            result = runpy.run_path(str(scorer))["score"](observation)
            if result.get("state") not in {"completed", "indeterminate"}:
                raise AssertionError(f"invalid score: {retailer}/ID{mid}")
            if mid in {"9", "10"}:
                label = "Y" if result.get("value") is True else "N" if result.get("value") is False else "REVIEW"
                original = first_scores[int(row["sourceRow"])][f"ID{mid}"]
                if original not in {label, "SOURCE_MISMATCH"}:
                    raise AssertionError(f"ID{mid} changed: {row['sourceRow']} {original} -> {label}")
            if mid == "18" and result["state"] != "indeterminate":
                raise AssertionError("ID18 must await a new visual AI review")
        checked += 1
    if checked != 139:
        raise AssertionError(f"expected 139 captured BCP rows, got {checked}")
    print(f"OK: {len(rows)} source-identical capture requests; {checked} parser/score rows; no external calls")


if __name__ == "__main__":
    main()
