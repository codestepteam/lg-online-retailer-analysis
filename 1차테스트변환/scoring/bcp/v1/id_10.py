"""BCP ID10: canonical tag presence, including empty href as in the first test."""

def score(observation):
    facts = observation.get("facts", {})
    hrefs = facts.get("selected_canonical_hrefs")
    evidence = observation.get("evidence", [])
    if not isinstance(hrefs, list):
        return {"state": "indeterminate", "reason": "requested_page_canonical_missing", "evidence": evidence}
    return {"state": "completed", "value": bool(hrefs), "evidence": evidence}
