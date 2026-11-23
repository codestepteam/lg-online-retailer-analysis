SELECT o.revision, u.country, u.retailer,
       u.page_summary->>'brand' AS brand, u.retailer_product_id,
       u.page_summary->>'product_code' AS product_code,
       u.page_summary->>'captured_at' AS captured_at,
       u.page_summary->>'http_status' AS http_status,
       r.diagnostic_detail #> '{evidence,0,product_bundle,components}' AS components,
       r.diagnostic_detail #>> '{evidence,0,product_bundle,evidence}' AS evidence,
       u.url, u.page_summary->>'final_url' AS final_url
FROM lg_registry.operation_urls u
JOIN lg_registry.operations o ON o.operation_id = u.operation_id
LEFT JOIN lg_registry.current_assessment_results r
  ON r.operation_id = u.operation_id AND r.url_id = u.url_id AND r.assessment_id = '13'
WHERE u.operation_id = 'op-20261029-01' AND u.scenario = 'pdp'
  AND (r.diagnostic_detail #> '{evidence,0,product_bundle,components}' IS NOT NULL
       OR coalesce(u.page_summary->>'final_url', u.url) ~*
          '(laundry-bundle|washer-and-dryer-(set|bundle)|laveuse-et-secheuse|waschmaschine[^?]*trockner[^?]*bundle|wasmachine[^?]*droger[^?]*bundel|wasmachine[^?]*droogkast[^?]*bundel|pralka[^?]*suszarka|zestaw[^?]*pralk|refrigerador-lavadora)'
       OR (u.retailer = 'costco_ca' AND u.retailer_product_id IN
           ('4000335518','4000335542','4000347968','4000347992','4000435597','4000435618','4000435637'))
       OR (u.retailer = 'liverpool' AND u.retailer_product_id IN
           ('1100156861','1126744613','1126948987','1141324931','1179776339','1184476734','1193071879','1207734558',
            '1196862508','1103883047'))
       OR (u.retailer = 'falabella_cl' AND u.retailer_product_id IN ('156468437','156542729','156468440'))
       OR coalesce(u.page_summary->>'final_url', u.url) ~*
          '(ksn36vlcg-gsn36vlcg|rl5k370gsfc1-ft5k310gsfc1|ksn36vwcg-gsn36vwdg)'
       OR u.page_summary->>'product_code' ~ '[A-Za-z0-9]{4,}[[:space:]]*[+][[:space:]]*[A-Za-z0-9]{4,}')
ORDER BY u.retailer, u.url
