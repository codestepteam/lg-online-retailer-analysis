WITH pages AS (
  SELECT p.page_id, upper(p.country) AS country, p.retailer, upper(p.category) AS category
  FROM lg_registry.plp_operation_state st
  JOIN lg_registry.plp_pages p ON p.operation_id = st.operation_id AND p.selected_snapshot_id = st.current_snapshot_id
  WHERE st.operation_id = 'op-20261101-01'
), daily AS (
  SELECT d.page_id, d.assessment_id, upper(d.brand) AS brand, avg(d.score) AS score
  FROM lg_registry.plp_daily_results d
  JOIN lg_registry.plp_daily_sets s ON s.request_id = d.request_id AND s.collected_on = d.collected_on
  WHERE s.superseded_at IS NULL AND d.collected_on BETWEEN '2026-11-01' AND '__END__'
    AND d.assessment_id IN ('1','2','3','4') AND upper(d.brand) IN ('LG','SAMSUNG','TOSHIBA','HAIER','PANASONIC')
  GROUP BY 1,2,3
)
SELECT pages.country, pages.retailer, pages.category, daily.assessment_id, daily.brand,
       count(*) AS pages, count(daily.score) AS scored, sum(daily.score) AS sum_score, avg(daily.score) AS avg_score
FROM pages JOIN daily ON daily.page_id = pages.page_id
GROUP BY 1,2,3,4,5 ORDER BY 1,2,3,4,5
