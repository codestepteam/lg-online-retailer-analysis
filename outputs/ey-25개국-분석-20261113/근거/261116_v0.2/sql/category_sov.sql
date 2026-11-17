WITH pg AS (
  SELECT l.collected_on, l.page_id, s.request_id, upper(p.country) AS country, p.retailer, upper(p.category) AS category,
         COALESCE(NULLIF(btrim(p.gnb_keyword), ''), l.page_id::text) AS kw
  FROM lg_registry.plp_daily_sets s
  JOIN lg_registry.plp_daily_pages p ON p.request_id = s.request_id AND p.collected_on = s.collected_on
  JOIN lg_registry.plp_daily_rank_lists l ON l.collected_on = p.collected_on AND l.page_id = p.page_id AND l.request_id = s.request_id
  WHERE s.superseded_at IS NULL AND p.kind = 'gnb' AND l.source_key::text = '3'
    AND COALESCE(l.complete, false) AND (COALESCE(l.product_count, 0) >= 10 OR COALESCE(l.short_complete, false))
), cnt AS (
  SELECT r.collected_on, r.request_id, r.page_id, upper(r.brand) AS brand, count(*) AS n
  FROM lg_registry.plp_daily_ranks r WHERE r.rank <= 10 AND upper(r.brand) IN ('LG','SAMSUNG','TOSHIBA','HAIER','PANASONIC') GROUP BY 1,2,3,4
), cell AS (
  SELECT pg.*, b.brand, COALESCE(c.n, 0) * 10.0 AS v
  FROM pg CROSS JOIN (VALUES ('LG'), ('SAMSUNG'), ('TOSHIBA'), ('HAIER'), ('PANASONIC')) AS b(brand)
  LEFT JOIN cnt c ON c.collected_on = pg.collected_on AND c.request_id = pg.request_id AND c.page_id = pg.page_id AND c.brand = b.brand
), daykw AS (
  SELECT to_char(collected_on, 'YYYY-MM') AS ym, collected_on, country, retailer, category, kw, brand, avg(v) AS v
  FROM cell GROUP BY 1,2,3,4,5,6,7
), kwm AS (
  SELECT ym, country, retailer, category, kw, brand, avg(v) AS v, count(*) AS days FROM daykw GROUP BY 1,2,3,4,5,6
)
SELECT ym, country, retailer, category, brand, avg(v) AS category_sov, count(*) AS keywords, max(days) AS days
FROM kwm GROUP BY 1,2,3,4,5 ORDER BY 1,2,3,4,5
