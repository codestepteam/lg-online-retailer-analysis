#!/usr/bin/env python3
"""Adapt one inspected retailer BCP recipe to another BCP URL on that retailer."""

from __future__ import annotations

import copy
import json
from urllib.parse import urlsplit


CONFIG_PREFIX = "window.__lgConfig = "


def _replace_url_contains(evidence: object, old_url: str, new_url: str) -> None:
    if not isinstance(evidence, dict):
        return
    terms = evidence.get("url_contains")
    if not isinstance(terms, list):
        return
    old_tail = urlsplit(old_url).path.rstrip("/").split("/")[-1]
    new_tail = urlsplit(new_url).path.rstrip("/").split("/")[-1]
    evidence["url_contains"] = [
        term.replace(old_url, new_url).replace(old_tail, new_tail)
        if isinstance(term, str) else term for term in terms
    ]


def adapt_recipe(base: dict[str, object], new_url: str) -> dict[str, object]:
    """Return a copy with URL-bearing request actions and checks updated."""
    recipe = copy.deepcopy(base)
    request = recipe.get("request")
    if not isinstance(request, dict) or not isinstance(request.get("actions"), list):
        raise ValueError("BCP recipe has no request actions")
    old_url = str(recipe.get("target_url") or request.get("url") or "")
    if not old_url or not new_url.startswith("https://"):
        raise ValueError("old and new BCP URLs must be valid HTTPS URLs")
    if urlsplit(old_url).hostname != urlsplit(new_url).hostname:
        raise ValueError("new URL must use the same retailer host as the inspected recipe")
    if old_url == new_url:
        return recipe

    found_config = False
    for action in request["actions"]:
        if not isinstance(action, dict):
            continue
        if action.get("action") == "goto" and action.get("url") == old_url:
            action["url"] = new_url
        source = action.get("source")
        if not isinstance(source, str) or not source.startswith(CONFIG_PREFIX):
            continue
        config = json.loads(source[len(CONFIG_PREFIX):].rstrip().removesuffix(";"))
        if config.get("url") is not None and config.get("url") != old_url:
            raise ValueError("embedded BCP config URL differs from recipe target URL")
        if config.get("url") is not None:
            config["url"] = new_url
        _replace_url_contains(config.get("evidence"), old_url, new_url)
        action["source"] = CONFIG_PREFIX + json.dumps(config, ensure_ascii=False) + ";"
        found_config = True
    if not found_config:
        raise ValueError("embedded BCP config was not found")
    if recipe.get("target_url"):
        recipe["target_url"] = new_url
        if not any(isinstance(action, dict) and action.get("action") == "goto" and action.get("url") == new_url
                   for action in request["actions"]):
            raise ValueError("entry-page recipe did not navigate to the new target URL")
    else:
        if request.get("url") != old_url:
            raise ValueError("request URL differs from recipe target URL")
        request["url"] = new_url
    _replace_url_contains(recipe.get("evidence"), old_url, new_url)
    return recipe
