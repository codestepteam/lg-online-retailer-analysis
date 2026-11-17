SELECT upper(p.country) AS country, p.retailer, upper(p.category) AS category, r.assessment_id, upper(r.brand) AS brand,
       count(*) AS pages, count(r.score) AS scored, sum(r.score) AS sum_score, avg(r.score) AS avg_score
FROM lg_registry.plp_operation_state st
JOIN lg_registry.plp_pages p ON p.operation_id = st.operation_id AND p.selected_snapshot_id = st.current_snapshot_id
JOIN lg_registry.current_plp_results r ON r.operation_id = p.operation_id AND r.page_id = p.page_id AND r.selected_snapshot_id = p.selected_snapshot_id
WHERE st.operation_id = '__OP__' AND r.assessment_id IN ('1','2','3','4') AND upper(r.brand) IN ('LG','SAMSUNG','TOSHIBA','HAIER','PANASONIC')
GROUP BY 1,2,3,4,5 ORDER BY 1,2,3,4,5
