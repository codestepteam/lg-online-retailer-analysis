SELECT to_char(r.collected_on, 'YYYY-MM') AS ym, upper(p.country) AS country, p.retailer, upper(p.category) AS category, upper(r.brand) AS brand, count(*) AS rank_rows
FROM lg_registry.plp_daily_sets s
JOIN lg_registry.plp_daily_pages p ON p.request_id = s.request_id AND p.collected_on = s.collected_on
JOIN lg_registry.plp_daily_ranks r ON r.collected_on = p.collected_on AND r.request_id = s.request_id AND r.page_id = p.page_id
WHERE s.superseded_at IS NULL AND upper(r.brand) IN ('LG','SAMSUNG')
GROUP BY 1,2,3,4,5 ORDER BY 1,2,3,4,5
