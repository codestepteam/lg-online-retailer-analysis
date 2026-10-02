"""BCP ID22: selected same-brand product cards must open product detail pages."""

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
