"""Rejudge only BCP ID8 from the second Temporal capture, using archived file bytes.

The GCS batch is read-only. All new observations and AI responses stay under
this third-test directory. Missing image byte counts remain unassessed.
"""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import hashlib
import json
import re
import runpy
from pathlib import Path
from urllib.parse import unquote, unquote_to_bytes, urlparse

from google.cloud import storage

from ai_observe import BCPReviewer


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
RESULTS = ROOT / "results" / "id8-file-bytes-20261001"
BUCKET = "lg-content-capture-20260909-assets"
BATCH = "bcp-local-retry-20260929T172142Z"
PREFIX = f"pipeline/batches/{BATCH}/"
STATE_PATTERN = re.compile(r'''(?is)<script[^>]+id=["']lg-capture-state["'][^>]*>(.*?)</script\s*>''')
SCORE = runpy.run_path(str(ROOT / "scoring" / "bcp" / "v1" / "id_8.py"))["score"]


def key_from_env() -> str:
    for line in (PROJECT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("OPENAI_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"\'')
    raise ValueError("OPENAI_API_KEY is absent from the project .env")


def gcs_json(bucket, key: str):
    return json.loads(bucket.blob(key).download_as_bytes())


def inline_bytes(source: str) -> int | None:
    if not source.startswith("data:"):
        return None
    try:
        header, payload = source.split(",", 1)
        return len(base64.b64decode(payload)) if header.endswith(";base64") else len(unquote_to_bytes(payload))
    except (ValueError, base64.binascii.Error):
        return None


def prepare(bucket, old):
    result = {"url_id": old["url_id"], "retailer": old["retailer"], "url": old["url"],
              "previous_state": old["state"], "previous_value": old.get("value"),
              "previous_reason": old.get("reason"), "source_batch": BATCH}
    attempt = old.get("attempt_id")
    if not attempt:
        result["status"] = "NO_CAPTURE_ATTEMPT"
        return result, None
    stem = f"{PREFIX}runs/{old['retailer']}/attempts/{attempt}/"
    try:
        raw = bucket.blob(stem + "raw.html").download_as_bytes()
        state_match = STATE_PATTERN.search(raw.decode("utf-8", errors="replace"))
        if not state_match:
            result["status"] = "CAPTURE_STATE_MISSING"
            return result, None
        state = json.loads(state_match.group(1))
        artifact = gcs_json(bucket, stem + f"observations/{old['url_id']}/parser.json")
        observation = artifact["observation"]
        if observation["facts"]["source_sha256"] != hashlib.sha256(raw).hexdigest():
            result["status"] = "SOURCE_HASH_MISMATCH"
            return result, None
        manifest = gcs_json(bucket, stem + "assets/manifest.json")
    except Exception as exc:
        result["status"] = "SOURCE_UNAVAILABLE"
        result["error_type"] = type(exc).__name__
        return result, None

    asset_sizes = {asset.get("url"): asset["bytes"] for asset in manifest.get("assets", [])
                   if asset.get("kind") == "image" and type(asset.get("bytes")) is int}
    visible = [image for image in state.get("images", [])
               if image.get("visible") is True and image.get("loaded") is True]
    area_top10 = sorted(visible, key=lambda image: float(image.get("renderedArea") or 0),
                        reverse=True)[:10]
    images = []
    missing = []
    for image in visible:
        source = str(image.get("src") or "")
        size = asset_sizes.get(source)
        if size is None:
            size = inline_bytes(source)
        if size is None:
            missing.append({"index": image.get("index"), "src": source[:300]})
            continue
        images.append({"index": image["index"], "fileBytes": size,
                       "src": source[:300] if not source.startswith("data:") else "inline data image",
                       "alt": image.get("alt")})
    result.update({"visible_loaded_images": len(images) + len(missing),
                   "measured_images": len(images), "missing_image_bytes": len(missing),
                   "missing_examples": missing[:10],
                   "raw_area_top10_indices": [image["index"] for image in area_top10]})
    if missing:
        result["status"] = "BYTE_SIZE_MISSING"
        return result, None
    if not images:
        result["status"] = "NO_ELIGIBLE_IMAGES"
        return result, None
    ordered = sorted(images, key=lambda image: (-image["fileBytes"], image["index"]))
    result["raw_byte_top10_indices"] = [image["index"] for image in ordered[:10]]
    result["raw_candidate_set_changed"] = (
        set(result["raw_area_top10_indices"]) != set(result["raw_byte_top10_indices"]))
    evidence = {"selectionRule": "visible, loaded, in-scope HTML images; descending archived file bytes",
                "eligibleImageCount": len(ordered), "unknownFileByteCount": 0,
                "candidatesByFileBytes": ordered}
    observation["facts"]["bcp_evidence"]["ID8"] = evidence
    screenshot_uri = observation["facts"].get("screenshot_uri")
    if not isinstance(screenshot_uri, str) or not screenshot_uri.startswith(f"gs://{BUCKET}/"):
        result["status"] = "SCREENSHOT_URI_INVALID"
        return result, None
    result["status"] = "READY"
    result["source_sha256"] = observation["facts"]["source_sha256"]
    return result, (observation, screenshot_uri)


class FileStore:
    def __init__(self, root: Path):
        self.root = root

    def uri(self, key: str) -> str:
        return (self.root / key).resolve().as_uri()

    def read_json(self, uri: str):
        return json.loads(Path(unquote(urlparse(uri).path)).read_text(encoding="utf-8"))

    def put_immutable(self, key: str, body: bytes, content_type: str):
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            if path.read_bytes() != body:
                raise ValueError("immutable AI review content changed")
        else:
            path.write_bytes(body)
        return path.resolve().as_uri()


def review(bucket, record, observation, screenshot_uri, reviewer):
    try:
        screen = bucket.blob(screenshot_uri.removeprefix(f"gs://{BUCKET}/")).download_as_bytes()
        enriched = reviewer.review(observation, screen, ids=["8"])
        ai = enriched["facts"]["ai_reviews"]["ID8"]
        verdict = SCORE(enriched)
        record.update({"status": "REVIEWED", "third_state": verdict["state"],
                       "third_value": verdict.get("value"), "third_reason": ai["reason"],
                       "selected_indices": ai["selected_indices"],
                       "review_uri": ai["observation_uri"],
                       "prompt_version": ai["prompt_version"],
                       "changed": (verdict.get("value") != record["previous_value"]
                                   if verdict["state"] == record["previous_state"] == "completed"
                                   else None)})
    except Exception as exc:
        record["status"] = "REVIEW_ERROR"
        record["error_type"] = type(exc).__name__
        record["error_detail"] = str(exc)[:400]
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", help="Comma-separated source row numbers; omit for all 139")
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    selected = {f"row-{int(number):04d}" for number in args.rows.split(",")} if args.rows else None
    client = storage.Client(project="lg-content-capture-20260909")
    bucket = client.bucket(BUCKET)
    old_scores = [score for score in gcs_json(bucket, PREFIX + "score-index.json")["scores"]
                  if score["assessment_id"] == "8" and (selected is None or score["url_id"] in selected)]
    if selected is not None and len(old_scores) != len(selected):
        raise ValueError("some requested source rows are absent from the second batch")
    print(f"Preparing {len(old_scores)} ID8 rows from {BATCH}", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        prepared = list(pool.map(lambda score: prepare(bucket, score), old_scores))
    records = [record for record, _ in prepared]
    ready = [(record, data) for record, data in prepared if data is not None]
    print(f"Ready for AI review: {len(ready)}; missing byte sizes: "
          f"{sum(record['status'] == 'BYTE_SIZE_MISSING' for record in records)}", flush=True)
    if not args.prepare_only:
        reviewer = BCPReviewer(FileStore(RESULTS), key_from_env())
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(review, bucket, record, data[0], data[1], reviewer)
                       for record, data in ready]
            for number, future in enumerate(concurrent.futures.as_completed(futures), 1):
                record = future.result()
                print(f"{number}/{len(ready)} {record['url_id']} {record['status']} "
                      f"{record.get('third_value')}", flush=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    suffix = "-" + args.rows.replace(",", "-") if args.rows else ""
    output = RESULTS / f"comparison{suffix}.json"
    output.write_text(json.dumps({"source_batch": BATCH, "criterion": "archived_image_file_bytes",
                                  "rows": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {output}", flush=True)


if __name__ == "__main__":
    main()
