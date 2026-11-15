WITH kw AS (
  SELECT DISTINCT upper(country) AS country, retailer, upper(category) AS category, COALESCE(search_keyword, '') AS kw
  FROM lg_registry.operation_baseline_records
  WHERE operation_id = 'op-20261026-01' AND assessment_id = '3'
), top AS (
  SELECT upper(country) AS country, retailer, upper(category) AS category, COALESCE(search_keyword, '') AS kw, upper(brand) AS brand, count(*) AS n
  FROM lg_registry.operation_baseline_records
  WHERE operation_id = 'op-20261026-01' AND assessment_id = '3' AND metric_name ~ '^top([1-9]|10)_product_name$'
  GROUP BY 1,2,3,4,5
), filled AS (
  SELECT country, retailer, category, kw, sum(n) AS top10_rows FROM top GROUP BY 1,2,3,4
)
SELECT kw.country, kw.retailer, kw.category, kw.kw, b.brand, COALESCE(t.n, 0) AS top10_count, COALESCE(f.top10_rows, 0) AS top10_rows
FROM kw CROSS JOIN (VALUES ('LG'), ('SAMSUNG')) AS b(brand)
LEFT JOIN top t ON t.country = kw.country AND t.retailer = kw.retailer AND t.category = kw.category AND t.kw = kw.kw AND t.brand = b.brand
LEFT JOIN filled f ON f.country = kw.country AND f.retailer = kw.retailer AND f.category = kw.category AND f.kw = kw.kw
ORDER BY 1,2,3,4,5
