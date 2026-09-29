#!/usr/bin/env python3
"""Run the ECI Zyte proof of concept.

The script selects one ECI PLP URL and one LG PDP URL from
``retailer-urls-14/eci/urls.csv`` and makes three Zyte API requests:

1. PDP as an HTTP response body.
2. PDP as browser HTML, screenshot, and structured product data.
3. PLP as browser HTML, screenshot, and structured product-list data.

The API key is read from the ``ZYTE_API_KEY`` environment variable or, when
that is not set, from ``ZYTE_API_KEY`` in the project-root ``.env`` file. It is
never written to an output file.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT_ROOT / "retailer-urls-14" / "eci" / "urls.csv"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "data" / "zyte" / "runs"
DEFAULT_ENV_FILE = PROJECT_ROOT / ".env"
ZYTE_ENDPOINT = "https://api.zyte.com/v1/extract"
REQUIRED_COLUMNS = {
    "url",
    "page_type",
    "brand",
    "product_category",
    "product_name",
    "assessment_ids",
    "canonical_url",
}


class PocError(RuntimeError):
    """Raised when the PoC cannot continue safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect one ECI PLP and one LG PDP through Zyte API."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Input CSV (default: {DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=f"Run output parent directory (default: {DEFAULT_OUTPUT_ROOT})",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=DEFAULT_ENV_FILE,
        help=f"File containing ZYTE_API_KEY (default: {DEFAULT_ENV_FILE})",
    )
    parser.add_argument(
        "--geolocation",
        default="ES",
        help="Two-letter request geolocation (default: ES)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=180.0,
        help="Timeout in seconds for each Zyte request (default: 180)",
    )
    parser.add_argument(
        "--run-id",
        help="Optional output directory name; defaults to the current UTC timestamp",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the selected rows and request payloads without calling Zyte or writing files",
    )
    return parser.parse_args()


def read_source_rows(source: Path) -> list[dict[str, str]]:
    if not source.is_file():
        raise PocError(f"Input CSV does not exist: {source}")

    with source.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise PocError(
                "Input CSV is missing required columns: " + ", ".join(sorted(missing))
            )
        return [dict(row) for row in reader]


def select_source_rows(
    rows: list[dict[str, str]],
) -> tuple[dict[str, str], dict[str, str]]:
    plp = next(
        (row for row in rows if row["page_type"].strip().upper() == "PLP"),
        None,
    )
    pdp = next(
        (
            row
            for row in rows
            if row["page_type"].strip().upper() == "PDP"
            and row["brand"].strip().upper() == "LG"
        ),
        None,
    )

    if plp is None:
        raise PocError("No PLP row was found in the input CSV.")
    if pdp is None:
        raise PocError("No LG PDP row was found in the input CSV.")
    return plp, pdp


def read_zyte_api_key(env_file: Path) -> str:
    environment_value = os.environ.get("ZYTE_API_KEY", "").strip()
    if environment_value:
        return environment_value

    if not env_file.is_file():
        raise PocError(
            f"ZYTE_API_KEY is not set and the .env file does not exist: {env_file}"
        )

    for line_number, raw_line in enumerate(
        env_file.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").lstrip()
        name, separator, value = line.partition("=")
        if not separator or name.strip() != "ZYTE_API_KEY":
            continue

        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if not value:
            raise PocError(
                f"ZYTE_API_KEY is empty in {env_file} at line {line_number}."
            )
        return value

    raise PocError(f"ZYTE_API_KEY was not found in {env_file}.")


def build_jobs(
    plp: dict[str, str],
    pdp: dict[str, str],
    geolocation: str,
) -> list[dict[str, Any]]:
    common = {"geolocation": geolocation.upper()}
    return [
        {
            "name": "pdp-http",
            "source_row": pdp,
            "payload": {
                "url": pdp["url"],
                "httpResponseBody": True,
                "httpResponseHeaders": True,
                **common,
            },
            "outputs": {"httpResponseBody": "pdp-http.html"},
        },
        {
            "name": "pdp-browser",
            "source_row": pdp,
            "payload": {
                "url": pdp["url"],
                "browserHtml": True,
                "screenshot": True,
                "product": True,
                "productOptions": {"extractFrom": "browserHtml"},
                **common,
            },
            "outputs": {
                "browserHtml": "pdp-browser.html",
                "screenshot": "pdp-screenshot.jpg",
                "product": "pdp-product.json",
            },
        },
        {
            "name": "plp-browser",
            "source_row": plp,
            "payload": {
                "url": plp["url"],
                "browserHtml": True,
                "screenshot": True,
                "productList": True,
                "productListOptions": {"extractFrom": "browserHtml"},
                **common,
            },
            "outputs": {
                "browserHtml": "plp-browser.html",
                "screenshot": "plp-screenshot.jpg",
                "productList": "plp-products.json",
            },
        },
    ]


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def decode_base64_field(value: Any, field: str) -> bytes:
    if not isinstance(value, str):
        raise PocError(f"Zyte response field {field!r} is missing or is not text.")
    try:
        return base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error) as error:
        raise PocError(f"Zyte response field {field!r} is not valid Base64.") from error


def call_zyte(
    api_key: str,
    payload: dict[str, Any],
    timeout: float,
) -> tuple[int, dict[str, str], dict[str, Any], float]:
    credentials = base64.b64encode(f"{api_key}:".encode("utf-8")).decode("ascii")
    request = Request(
        ZYTE_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "User-Agent": "lg-online-retailer-analysis-zyte-poc/1.0",
        },
        method="POST",
    )

    started = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.status
            headers = {key.lower(): value for key, value in response.headers.items()}
            response_bytes = response.read()
    except HTTPError as error:
        status = error.code
        headers = {key.lower(): value for key, value in error.headers.items()}
        response_bytes = error.read()
    except URLError as error:
        raise PocError(f"Zyte request could not be sent: {error.reason}") from error

    elapsed_seconds = time.perf_counter() - started
    try:
        response_data = json.loads(response_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PocError(
            f"Zyte returned a non-JSON response with HTTP status {status}."
        ) from error
    if not isinstance(response_data, dict):
        raise PocError("Zyte returned JSON, but the top-level value is not an object.")
    return status, headers, response_data, elapsed_seconds


def save_extracted_outputs(
    run_directory: Path,
    job: dict[str, Any],
    response_data: dict[str, Any],
) -> list[str]:
    written: list[str] = []
    for field, filename in job["outputs"].items():
        if field not in response_data:
            continue
        output_path = run_directory / filename
        value = response_data[field]
        if field in {"httpResponseBody", "screenshot"}:
            output_path.write_bytes(decode_base64_field(value, field))
        elif field == "browserHtml":
            if not isinstance(value, str):
                raise PocError("Zyte response field 'browserHtml' is not text.")
            output_path.write_text(value, encoding="utf-8")
        else:
            write_json(output_path, value)
        written.append(filename)
    return written


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> int:
    args = parse_args()
    try:
        rows = read_source_rows(args.source)
        plp, pdp = select_source_rows(rows)
        jobs = build_jobs(plp, pdp, args.geolocation)

        if args.dry_run:
            print(
                json.dumps(
                    {
                        "source": str(args.source.resolve()),
                        "selected": {"plp": plp, "pdp": pdp},
                        "requests": [
                            {"name": job["name"], "payload": job["payload"]}
                            for job in jobs
                        ],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        api_key = read_zyte_api_key(args.env_file)

        run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_directory = args.output_root.resolve() / run_id / "eci"
        if run_directory.exists():
            raise PocError(f"Output directory already exists: {run_directory}")
        run_directory.mkdir(parents=True)

        manifest: dict[str, Any] = {
            "run_id": run_id,
            "started_at": utc_now(),
            "finished_at": None,
            "source": str(args.source.resolve()),
            "zyte_endpoint": ZYTE_ENDPOINT,
            "api_key_stored": False,
            "requests": [],
        }
        manifest_path = run_directory / "manifest.json"
        write_json(manifest_path, manifest)

        failures = 0
        for job in jobs:
            print(f"Requesting {job['name']}: {job['payload']['url']}")
            entry: dict[str, Any] = {
                "name": job["name"],
                "source_row": job["source_row"],
                "request": job["payload"],
                "started_at": utc_now(),
            }
            response_path = run_directory / f"{job['name']}-response.json"
            try:
                status, headers, response_data, elapsed = call_zyte(
                    api_key, job["payload"], args.timeout
                )
                write_json(response_path, response_data)
                entry.update(
                    {
                        "finished_at": utc_now(),
                        "http_status": status,
                        "target_status_code": response_data.get("statusCode"),
                        "final_url": response_data.get("url"),
                        "zyte_request_id": headers.get("zyte-request-id"),
                        "elapsed_seconds": round(elapsed, 3),
                        "response_file": response_path.name,
                    }
                )
                if status == 200:
                    entry["outcome"] = "captured"
                    entry["output_files"] = save_extracted_outputs(
                        run_directory, job, response_data
                    )
                else:
                    failures += 1
                    entry["outcome"] = "zyte_error"
                    entry["error"] = {
                        "type": response_data.get("type"),
                        "title": response_data.get("title"),
                        "detail": response_data.get("detail"),
                    }
            except PocError as error:
                failures += 1
                entry.update(
                    {
                        "finished_at": utc_now(),
                        "outcome": "local_error",
                        "error": {"detail": str(error)},
                    }
                )
            manifest["requests"].append(entry)
            write_json(manifest_path, manifest)

        manifest["finished_at"] = utc_now()
        manifest["summary"] = {
            "requested": len(jobs),
            "captured": len(jobs) - failures,
            "failed": failures,
        }
        write_json(manifest_path, manifest)
        print(f"Saved run: {run_directory}")
        return 1 if failures else 0
    except PocError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
