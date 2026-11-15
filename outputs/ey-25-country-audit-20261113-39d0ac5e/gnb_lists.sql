SELECT l.collected_on, l.page_id, p.retailer, p.country, p.category, p.kind, p.search_keyword, p.gnb_keyword, l.source_key, l.source_kind, l.complete, l.end_reached, l.total, l.product_count, l.short_complete, l.reason
FROM lg_registry.plp_daily_sets s
JOIN lg_registry.plp_daily_pages p ON p.request_id=s.request_id AND p.collected_on=s.collected_on
JOIN lg_registry.plp_daily_rank_lists l ON l.collected_on=p.collected_on AND l.page_id=p.page_id AND l.request_id=s.request_id
WHERE s.superseded_at IS NULL AND p.kind='gnb' AND l.collected_on >= '2026-10-01' AND l.collected_on <= '2026-11-13';
