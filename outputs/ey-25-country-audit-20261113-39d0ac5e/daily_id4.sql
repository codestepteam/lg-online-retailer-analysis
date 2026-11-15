SELECT r.collected_on, r.page_id, p.retailer, p.country, p.category, p.kind, p.search_keyword, p.representative, r.assessment_id, r.brand, r.score, r.verdict_status, r.source_kind
FROM lg_registry.plp_daily_sets s
JOIN lg_registry.plp_daily_pages p ON p.request_id=s.request_id AND p.collected_on=s.collected_on
JOIN lg_registry.plp_daily_results r ON r.request_id=s.request_id AND r.collected_on=p.collected_on AND r.page_id=p.page_id
WHERE s.superseded_at IS NULL AND p.kind='search' AND r.assessment_id='4'
AND r.collected_on >= '2026-10-01' AND r.collected_on <= '2026-11-13';
