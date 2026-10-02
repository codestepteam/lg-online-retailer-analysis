"""Create local BCP scenario tips from the first-test recipes; never contacts GCS."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from build_scorers import build as build_scorers

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
SOURCE = PROJECT / "1차 테스트" / "bcp-zyte-poc"
PEER_SCHEMA = (PROJECT.parent / "lg-crawling" / "pipeline" / "schemas" /
               "lg-diagnostic-observation-v1.schema.json")
IDS = ("8", "9", "10", "18", "19", "20", "21", "22", "23")


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _file_info(path: Path, name: str):
    content = path.read_bytes()
    return {"name": name, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}


def build():
    build_scorers()
    if not PEER_SCHEMA.is_file():
        raise FileNotFoundError(f"lg-crawling observation schema is missing: {PEER_SCHEMA}")
    inventory = _json(SOURCE / "population" / "source_urls.json")
    bcp_rows = [row for row in inventory["records"] if row.get("pageType") == "Brand Category Page"]
    _write(ROOT / "inputs" / "bcp-urls.json", {key: inventory[key] for key in
           ("sourceWorkbook", "sourceWorkbookSha256", "sourceSheet")} | {"records": bcp_rows})
    recipes = sorted((SOURCE / "capture" / "recipes").glob("*/brand-category.json"))
    for source_path in recipes:
        retailer = source_path.parent.name
        tip = ROOT / "retailers" / retailer / "scenarios" / "bcp"
        recipe = _json(source_path)
        actions = []
        for index, action in enumerate(recipe["request"]["actions"]):
            source = action.pop("source", None)
            if source is None:
                continue
            if not isinstance(source, str):
                raise ValueError(f"invalid action source: {source_path}")
            name = f"action-{index:02d}.js"
            path = tip / "zyte" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source, encoding="utf-8")
            action["source_file"] = name
            actions.append(_file_info(path, name))
        parser_dir = tip / "parser"
        parser_dir.mkdir(parents=True, exist_ok=True)
        for name in ("bcp.py", "legacy_bcp_evidence.py"):
            shutil.copyfile(ROOT / "parser" / name, parser_dir / name)
        schema_dir = tip / "observation"
        schema_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PEER_SCHEMA, schema_dir / PEER_SCHEMA.name)
        _write(tip / "config.json", {"retailer": retailer, "page_type": "bcp", "recipe": recipe})
        manifest = {
            "schema_version": "lg-bcp-scenario-draft-v1", "retailer": retailer,
            "page_type": "bcp", "assessment_ids": list(IDS),
            "score_set": "scoring/bcp/v1", "parser_present": True,
            "action_files": actions,
            "parser_files": [_file_info(parser_dir / name, name) for name in
                             ("bcp.py", "legacy_bcp_evidence.py")],
            "observation_files": [_file_info(schema_dir / PEER_SCHEMA.name, PEER_SCHEMA.name)],
            "capture_template_sha256": hashlib.sha256((tip / "config.json").read_bytes()).hexdigest(),
            "source_recipe": str(source_path.relative_to(PROJECT)),
            "source_recipe_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        }
        _write(tip / "manifest.json", manifest)
    return len(recipes), len(bcp_rows)


if __name__ == "__main__":
    retailers, rows = build()
    print(f"Prepared {retailers} BCP scenario tips and {rows} BCP input rows")
