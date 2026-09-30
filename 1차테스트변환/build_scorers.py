"""Write standalone score(observation) programs for the nine BCP IDs."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "scoring" / "bcp" / "v1"

AI = '''"""BCP ID{mid}: use a fresh, source-bound AI review; never replay workbook-row answers."""

def score(observation):
    facts = observation.get("facts", {{}})
    source = facts.get("source_sha256")
    review = facts.get("ai_reviews", {{}}).get("ID{mid}")
    evidence = observation.get("evidence", [])
    if not isinstance(review, dict) or review.get("source_sha256") != source or not source:
        return {{"state": "indeterminate", "reason": "ai_review_missing_or_stale", "evidence": evidence}}
    if (review.get("choice") not in {{"Y", "N", "REVIEW"}}
            or review.get("prompt_version") != "bcp-first-test-20260929-v1"
            or not all(isinstance(review.get(key), str) and review[key] for key in
                       ("model", "prompt_version", "reason", "observation_uri",
                        "input_sha256", "response_id"))
            or ({visual} and (not isinstance(facts.get("screenshot_uri"), str)
                              or not isinstance(review.get("screenshot_sha256"), str)
                              or len(review["screenshot_sha256"]) != 64))):
        return {{"state": "indeterminate", "reason": "ai_review_invalid", "evidence": evidence}}
    refs = list(dict.fromkeys([*evidence, review["observation_uri"]]))
    if review["choice"] == "REVIEW":
        return {{"state": "indeterminate", "reason": "ai_evidence_ambiguous", "evidence": refs}}
    return {{"state": "completed", "value": review["choice"] == "Y", "evidence": refs}}
'''

ID9 = '''"""BCP ID9: first-test Title, description, H1, and robots rule."""

def _values(metadata, key):
    raw = metadata.get(key)
    return [str(item or "").strip() for item in raw] if isinstance(raw, list) else ([str(raw).strip()] if raw is not None else [])

def score(observation):
    facts = observation.get("facts", {})
    metadata = facts.get("selected_metadata")
    evidence = observation.get("evidence", [])
    if not isinstance(metadata, dict):
        return {"state": "indeterminate", "reason": "requested_page_metadata_missing", "evidence": evidence}
    fields = {key: _values(metadata, key) for key in ("title", "metaDescription", "h1", "robots")}
    if any(not any(values) for values in fields.values()):
        return {"state": "completed", "value": False, "evidence": evidence}
    robots = [item.casefold().replace(" ", "") for item in fields["robots"] if item]
    if any(not {"index", "follow"}.issubset(set(item.split(","))) or
           {"noindex", "nofollow"} & set(item.split(",")) for item in robots):
        return {"state": "completed", "value": False, "evidence": evidence}
    if any(len(set(item for item in values if item)) > 1 for values in fields.values()):
        return {"state": "indeterminate", "reason": "conflicting_metadata_tags", "evidence": evidence}
    return {"state": "completed", "value": True, "evidence": evidence}
'''

ID10 = '''"""BCP ID10: canonical tag presence, including empty href as in the first test."""

def score(observation):
    facts = observation.get("facts", {})
    hrefs = facts.get("selected_canonical_hrefs")
    evidence = observation.get("evidence", [])
    if not isinstance(hrefs, list):
        return {"state": "indeterminate", "reason": "requested_page_canonical_missing", "evidence": evidence}
    return {"state": "completed", "value": bool(hrefs), "evidence": evidence}
'''

ID21 = '''"""BCP ID21: all category cards must be clicked and their landing lineups checked."""

def score(observation):
    facts = observation.get("facts", {})
    checks = facts.get("navigator_click_checks")
    expected = facts.get("navigator_expected_count")
    evidence = observation.get("evidence", [])
    if not isinstance(checks, list) or type(expected) is not int or expected < 1:
        return {"state": "indeterminate", "reason": "navigator_click_checks_missing", "evidence": evidence}
    if any(item.get("capture_valid") is True and item.get("lineup_match") == "different_lineup"
           and isinstance(item.get("jev_response_uri"), str) and item["jev_response_uri"]
           for item in checks if isinstance(item, dict)):
        return {"state": "completed", "value": False, "evidence": evidence}
    if (len(checks) != expected or any(not isinstance(item, dict) or item.get("clicked") is not True
            or item.get("capture_valid") is not True or item.get("lineup_match") != "matching_lineup"
            or not isinstance(item.get("jev_response_uri"), str) or not item["jev_response_uri"]
            for item in checks)):
        return {"state": "indeterminate", "reason": "navigator_click_or_lineup_unverified", "evidence": evidence}
    return {"state": "completed", "value": True, "evidence": evidence}
'''

ID22 = '''"""BCP ID22: selected same-brand product cards must open product detail pages."""

def score(observation):
    facts = observation.get("facts", {})
    checks = facts.get("product_destination_checks")
    evidence = observation.get("evidence", [])
    if not isinstance(checks, list) or not checks:
        return {"state": "indeterminate", "reason": "product_destination_checks_missing", "evidence": evidence}
    if any(isinstance(item, dict) and item.get("capture_valid") is True and
           isinstance(item.get("evidence_uri"), str) and item["evidence_uri"] and
           (item.get("brand_matches") is False or item.get("product_detail") is False)
           for item in checks):
        return {"state": "completed", "value": False, "evidence": evidence}
    if any(not isinstance(item, dict) or item.get("capture_valid") is not True or
           item.get("brand_matches") is not True or item.get("product_detail") is not True or
           not isinstance(item.get("evidence_uri"), str) or not item["evidence_uri"]
           for item in checks):
        return {"state": "indeterminate", "reason": "product_destination_unverified", "evidence": evidence}
    return {"state": "completed", "value": True, "evidence": evidence}
'''


def build():
    ROOT.mkdir(parents=True, exist_ok=True)
    programs = {"9": ID9, "10": ID10, "21": ID21, "22": ID22}
    programs.update({mid: AI.format(mid=mid, visual=mid in {"8", "18"})
                     for mid in ("8", "18", "19", "20", "23")})
    for mid, source in programs.items():
        (ROOT / f"id_{mid}.py").write_text(source, encoding="utf-8")
    manifest = {"schema_version": "lg-bcp-score-set-draft-v1", "version": "bcp-first-test-v1",
                "scorers": {mid: {"version": f"bcp-id{mid}-first-test-v1",
                    "path": f"id_{mid}.py", "sha256": hashlib.sha256(source.encode()).hexdigest()}
                    for mid, source in sorted(programs.items(), key=lambda item: int(item[0]))}}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8")
    return len(programs)


if __name__ == "__main__":
    print(f"Wrote {build()} BCP scorers")
