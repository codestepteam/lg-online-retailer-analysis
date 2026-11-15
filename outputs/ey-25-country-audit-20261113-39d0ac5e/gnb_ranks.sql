SELECT r.collected_on, r.page_id, r.rank, r.brand, r.brand_raw, NULL::text AS name, NULL::text AS url, r.is_ad
FROM lg_registry.plp_daily_sets s
JOIN lg_registry.plp_daily_pages p ON p.request_id=s.request_id AND p.collected_on=s.collected_on AND p.kind='gnb'
JOIN lg_registry.plp_daily_ranks r ON r.collected_on=s.collected_on AND r.request_id=s.request_id AND r.page_id=p.page_id
WHERE s.superseded_at IS NULL AND r.rank <= 10 AND r.collected_on >= '2026-10-01' AND r.collected_on <= '2026-11-13';
