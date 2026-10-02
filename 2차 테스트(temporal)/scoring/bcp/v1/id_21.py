"""BCP ID21: all category cards must be clicked and their landing lineups checked."""

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
