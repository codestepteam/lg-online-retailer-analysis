"""BCP ID20: use a fresh, source-bound AI review; never replay workbook-row answers."""

def score(observation):
    facts = observation.get("facts", {})
    source = facts.get("source_sha256")
    review = facts.get("ai_reviews", {}).get("ID20")
    evidence = observation.get("evidence", [])
    if not isinstance(review, dict) or review.get("source_sha256") != source or not source:
        return {"state": "indeterminate", "reason": "ai_review_missing_or_stale", "evidence": evidence}
    if (review.get("choice") not in {"Y", "N", "REVIEW"}
            or review.get("prompt_version") != "bcp-first-test-20260929-v1"
            or not all(isinstance(review.get(key), str) and review[key] for key in
                       ("model", "prompt_version", "reason", "observation_uri",
                        "input_sha256", "response_id"))
            or (False and (not isinstance(facts.get("screenshot_uri"), str)
                              or not isinstance(review.get("screenshot_sha256"), str)
                              or len(review["screenshot_sha256"]) != 64))):
        return {"state": "indeterminate", "reason": "ai_review_invalid", "evidence": evidence}
    refs = list(dict.fromkeys([*evidence, review["observation_uri"]]))
    if review["choice"] == "REVIEW":
        return {"state": "indeterminate", "reason": "ai_evidence_ambiguous", "evidence": refs}
    return {"state": "completed", "value": review["choice"] == "Y", "evidence": refs}
