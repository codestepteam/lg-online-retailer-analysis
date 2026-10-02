"""Normalize source-bound first-test product destination checks for BCP ID22."""

from __future__ import annotations

import re
from urllib.parse import urlsplit


PRODUCT_PATHS = ("/product/", "/products/", "/produkt/", "/produit/", "/prodotto/", "/ref/", "/dp/")


def _product_url(url, retailer):
    path = urlsplit(str(url)).path.casefold()
    return (any(part in path for part in PRODUCT_PATHS)
            or retailer == "alza" and bool(re.search(r"-d\d+\.htm$", path))
            or retailer == "datart" and bool(re.search(
                r"/(?:automaticka-|pracka-|susicka-|chladnicka-|lednice-|americka-lednice-|mrazak-|mraznicka-|mycka-|mycka-nadobi-)[^/]+", path)))


def attach_product_checks(observation, checked, *, evidence_uri):
    """Only accept results tied to this HTML; unverified destinations stay unknown."""
    target = observation.get("target", {})
    facts = observation.get("facts", {})
    if (not isinstance(checked, dict) or
            checked.get("sourceRawHtmlSha256") != facts.get("source_sha256") or
            checked.get("sourceUrl") != target.get("url") or
            checked.get("verificationMethod") != "zyte_same_origin_product_fetch" or
            not isinstance(evidence_uri, str) or not evidence_uri):
        raise ValueError("product destination check is not bound to this BCP capture")
    targets = checked.get("targets")
    results = checked.get("results")
    if (not isinstance(targets, list) or not 1 <= len(targets) <= 2 or
            not isinstance(results, list) or any(not isinstance(item, dict) for item in targets + results)):
        raise ValueError("product check targets or results are invalid")
    by_url = {item.get("url"): item for item in results}
    brand = str(target.get("brand") or "")
    if not brand:
        raise ValueError("target brand is missing")
    normalized = []
    for item in targets:
        url = item.get("url")
        result = by_url.get(url, {})
        title = str(result.get("title") or "")
        h1 = str(result.get("h1") or "")
        final_url = str(result.get("finalUrl") or url or "")
        valid = result.get("status") == 200
        normalized.append({"url": url, "capture_valid": valid,
                           "brand_matches": bool(re.search(r"(?<![A-Za-z])" + re.escape(brand) +
                               r"(?![A-Za-z])", title + " " + h1, re.I)) if valid else None,
                           "product_detail": _product_url(final_url, target.get("retailer")) if valid else None,
                           "evidence_uri": evidence_uri})
    return {**observation,
            "facts": {**facts, "product_destination_checks": normalized},
            "evidence": list(dict.fromkeys([*observation.get("evidence", []), evidence_uri]))}
