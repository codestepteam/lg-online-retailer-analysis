"""Compile a source-locked BCP scenario tip into one Zyte request, without calling Zyte."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from adapt_bcp_recipe import adapt_recipe


ROOT = Path(__file__).resolve().parent
PREFIX = "window.__lgConfig = "


def _read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def compile_request(retailer: str, target: dict, *, root: Path = ROOT) -> dict:
    """Return the same style of request as the first test for a BCP target."""
    tip = root / "retailers" / retailer / "scenarios" / "bcp"
    manifest = _read_json(tip / "manifest.json")
    config_file = tip / "config.json"
    if hashlib.sha256(config_file.read_bytes()).hexdigest() != manifest.get("capture_template_sha256"):
        raise ValueError("capture config checksum mismatch")
    config = _read_json(config_file)
    if manifest.get("retailer") != retailer or config.get("retailer") != retailer:
        raise ValueError("retailer does not match scenario tip")
    action_meta = {item["name"]: item for item in manifest["action_files"]}
    recipe = copy.deepcopy(config["recipe"])
    for action in recipe["request"]["actions"]:
        name = action.pop("source_file", None)
        if name is None:
            continue
        if name not in action_meta or Path(name).name != name:
            raise ValueError(f"unlisted action source: {name}")
        source = (tip / "zyte" / name).read_bytes()
        expected = action_meta[name]
        if len(source) != expected["bytes"] or hashlib.sha256(source).hexdigest() != expected["sha256"]:
            raise ValueError(f"action checksum mismatch: {name}")
        action["source"] = source.decode("utf-8")

    url = target.get("url")
    if not isinstance(url, str):
        raise ValueError("target.url is required")
    recipe = adapt_recipe(recipe, url)
    brand = target.get("brand")
    category = target.get("subcategory", target.get("product_category"))
    category_code = target.get("categoryCode", "")
    if not isinstance(brand, str) or not brand:
        raise ValueError("target brand is required")
    if category is not None and not isinstance(category, str):
        raise ValueError("target product category must be a string or null")
    for action in recipe["request"]["actions"]:
        source = action.get("source", "")
        if not isinstance(source, str) or not source.startswith(PREFIX):
            continue
        settings = json.loads(source[len(PREFIX):].rstrip().removesuffix(";"))
        settings.update(target_brand=brand, target_category=category,
                        target_category_code=category_code)
        if retailer == "elgiganten" and brand.casefold() != "lg":
            settings["ready"], settings["required"] = "body", ["body"]
            recipe.setdefault("evidence", {})["title_contains"] = [brand]
        action["source"] = PREFIX + json.dumps(settings, ensure_ascii=False) + ";"
        break
    else:
        raise ValueError("BCP config action is missing")

    if retailer == "elgiganten" and brand.casefold() != "lg":
        for action in recipe["request"]["actions"]:
            if action.get("action") == "waitForTimeout" and float(action.get("timeout", 0)) < 5:
                action["timeout"] = 5
                break
        recipe["request"]["actions"].insert(-2, {"action": "evaluate", "source":
            "(async()=>{const until=Date.now()+18000;while(Date.now()<until){"
            "if(document.querySelector('a[href*=\"/product/\"]'))return;"
            "await new Promise(r=>setTimeout(r,500));}})();"})

    request = recipe["request"]
    for action in request["actions"]:
        if isinstance(action.get("source"), str) and len(action["source"].encode("utf-8")) > 6000:
            raise ValueError("Zyte evaluate action exceeds 6000 bytes")
    return request
