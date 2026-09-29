#!/usr/bin/env python3
"""Retry failed product-card visits directly through Zyte, preserving original checks."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from capture_bcp_population import ROOT
from check_failed_links_direct import check
import zyte_capture as zyte


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    batch = args.batch.resolve()
    api_key = zyte._load_env(ROOT)
    if not api_key:
        raise RuntimeError("ZYTE_API_KEY is missing")
    output = batch / "product-link-check-direct"
    output.mkdir(exist_ok=True)
    jobs = []
    for path in sorted((batch / "product-link-check").glob("*.json")):
        data = json.loads(path.read_text())
        already = json.loads((output / path.name).read_text()).get("results", []) if (output / path.name).is_file() else []
        successful = {item["url"] for item in already if item.get("status") == 200}
        for index, target in enumerate(data.get("targets", [])):
            result = data.get("results", [])[index] if index < len(data.get("results", [])) else {}
            if result.get("status") != 200 and target["url"] not in successful:
                jobs.append((path.stem, target))
    print(f"direct retry targets={len(jobs)}", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = {pool.submit(check, target, api_key): key for key, target in jobs}
        for future in as_completed(pending):
            key = pending[future]
            result = future.result()
            path = output / f"{key}.json"
            previous = json.loads(path.read_text()) if path.is_file() else {"pageKey": key, "results": []}
            previous["results"] = [item for item in previous["results"] if item.get("url") != result.get("url")] + [result]
            previous["source"] = "Zyte browser direct navigation"
            path.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + "\n")
            print(key, result.get("status", result.get("error")), result.get("title", "")[:80], flush=True)


if __name__ == "__main__":
    main()
