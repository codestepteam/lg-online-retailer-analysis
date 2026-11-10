-- Read-only audit: source coverage and exact labels, Germany MediaMarkt on 2026-10-26.
-- No collection, writes, or changes to the original extraction SQL.
WITH source_rows AS (
  SELECT 'SALE_RK' AS source, DATE AS data_date, CNTRY AS country, ONLINE_STR AS retailer,
         BRAND AS brand, CAT AS category, URL AS url
  FROM `pjt-lge-oned.L2_ONED.VSMRKT_DAILY_OSM_SALE_RK_D`
  WHERE DATE = DATE '2026-10-26'
    AND REGEXP_REPLACE(UPPER(TRIM(CNTRY)), r'\s', '') = 'GERMANY'
    AND UPPER(TRIM(ONLINE_STR)) LIKE '%MEDIA%MARKT%'
  UNION ALL
  SELECT 'BANR_VSBLT', DATE, CNTRY, ONLINE_STR, BRAND, CAT, URL
  FROM `pjt-lge-oned.L2_ONED.VSMRKT_DAILY_OSM_BANR_VSBLT_D`
  WHERE DATE = DATE '2026-10-26'
    AND REGEXP_REPLACE(UPPER(TRIM(CNTRY)), r'\s', '') = 'GERMANY'
    AND UPPER(TRIM(ONLINE_STR)) LIKE '%MEDIA%MARKT%'
  UNION ALL
  SELECT 'L1_PRODUCT', BASE_DATE, CNTRY_CODE, SITE_NAME,
         COALESCE(MAPP_BRAND_NAME, BRAND_NAME), MAPP_CAT_NAME, PRODUCT_PAGE_URL_ADDR
  FROM `pjt-lge-oned.L1_ONED.TRPURC_OSM_PRODUCT_DAILY_L`
  WHERE BASE_DATE = DATE '2026-10-26'
    AND UPPER(TRIM(CNTRY_CODE)) = 'DE'
    AND UPPER(TRIM(SITE_NAME)) LIKE '%MEDIA%MARKT%'
)
SELECT source,data_date,country,retailer,brand,category,
       COUNT(*) AS row_count,COUNT(DISTINCT TRIM(url)) AS distinct_raw_urls,
       COUNT(DISTINCT REGEXP_REPLACE(TRIM(url),r'[\?#].*$','')) AS distinct_clean_urls
FROM source_rows
GROUP BY 1,2,3,4,5,6
ORDER BY source,brand,category
