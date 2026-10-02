"""BCP ID9: first-test Title, description, H1, and robots rule."""

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
