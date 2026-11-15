SELECT r.assessment_id, min(d->>'collected_on') AS first_day, max(d->>'collected_on') AS last_day, count(*) AS day_entries
FROM lg_registry.plp_operation_state s
JOIN lg_registry.current_plp_results r ON r.operation_id=s.operation_id AND r.selected_snapshot_id=s.current_snapshot_id
CROSS JOIN LATERAL jsonb_array_elements(r.diagnostic_detail->'days') d
WHERE s.operation_id='op-20261101-01' AND r.assessment_id IN ('1','2','3','4') GROUP BY 1 ORDER BY 1;
