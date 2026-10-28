-- 독일 OTTO 10-19 PDP 모수 1차 후보 추출 (D058)
-- osm_target_extract.sql 원본에서 날짜(10-19)와 retailer_map·brand_map(Germany OTTO만)만 바꿨다. 나머지는 원본 그대로.
WITH

params AS (

  SELECT
    DATE '2026-10-19' AS START_DATE,
    DATE '2026-10-19' AS END_DATE

),

retailer_map AS (

  SELECT *

  FROM UNNEST([

    STRUCT(
      'Germany' AS CNTRY,
      'OTTO' AS RTLR_NAME
    )

  ])

),

brand_map AS (

  SELECT *

  FROM UNNEST([

    STRUCT(
      'Germany' AS CNTRY,
      'OTTO' AS RTLR_NAME,
      'REF' AS DIV,
      'LG' AS BRAND
    ),
    STRUCT('Germany', 'OTTO', 'REF', 'EXQUISIT'),
    STRUCT('Germany', 'OTTO', 'REF', 'LIEBHERR'),
    STRUCT('Germany', 'OTTO', 'REF', 'SIEMENS'),
    STRUCT('Germany', 'OTTO', 'REF', 'BOSCH'),
    STRUCT('Germany', 'OTTO', 'REF', 'AMICA'),
    STRUCT('Germany', 'OTTO', 'W/M', 'LG'),
    STRUCT('Germany', 'OTTO', 'W/M', 'BOSCH'),
    STRUCT('Germany', 'OTTO', 'W/M', 'AEG'),
    STRUCT('Germany', 'OTTO', 'W/M', 'BAUKNECHT'),
    STRUCT('Germany', 'OTTO', 'W/M', 'SIEMENS'),
    STRUCT('Germany', 'OTTO', 'W/M', 'BEKO'),
    STRUCT('Germany', 'OTTO', 'DRY', 'LG'),
    STRUCT('Germany', 'OTTO', 'DRY', 'SAMSUNG'),
    STRUCT('Germany', 'OTTO', 'DRY', 'BOSCH'),
    STRUCT('Germany', 'OTTO', 'DRY', 'SIEMENS')

  ])

),

sale_base AS (

  SELECT

    t.DATE AS RPT_DATE,

    TRIM(t.CNTRY) AS CNTRY,

    TRIM(t.ONLINE_STR) AS RTLR_NAME,

    TRIM(t.BRAND) AS BRAND,

    CASE

      WHEN UPPER(TRIM(t.CAT)) = 'WASHING MACHINE_HA'
        THEN 'W/M'

      WHEN UPPER(TRIM(t.CAT)) = 'REFRIGERATOR_HA'
        THEN 'REF'

      WHEN UPPER(TRIM(t.CAT)) = 'DISHWASHER_HA'
        THEN 'D/W'

      WHEN UPPER(TRIM(t.CAT)) = 'DRYER_HA'
        THEN 'DRY'

      ELSE NULL

    END AS DIV,

    TRIM(IFNULL(t.RPC, '')) AS RPC,

    TRIM(IFNULL(t.MPC, '')) AS MPC,

    TRIM(t.URL) AS RAW_URL,

    REGEXP_REPLACE(
      TRIM(t.URL),
      r'[\?#].*$',
      ''
    ) AS CAT_URL_ADDR,

    COALESCE(

      NULLIF(
        UPPER(TRIM(t.MPC)),
        ''
      ),

      NULLIF(
        UPPER(TRIM(t.RPC)),
        ''
      ),

      UPPER(
        REGEXP_REPLACE(
          TRIM(t.URL),
          r'[\?#].*$',
          ''
        )
      )

    ) AS MODEL_DEDUP_KEY,

    t.PRODUCT_DESC,

    t.AVLBL_STAT,

    t.OBSRV_LIST_PRICE,

    t.OBSRV_DC_PRICE,

    t.CURRENCY_CODE,

    t.RK,

    t.CAT,

    t.IMG_COUNT,

    t.VIDEO_COUNT,

    t.SALE_AMT,

    t.SALE_QTY,

    t.SEARCH_TERM,

    'SALE_RK' AS SOURCE_TYPE,

    1 AS SOURCE_PRIORITY

  FROM
    `pjt-lge-oned.L2_ONED.VSMRKT_DAILY_OSM_SALE_RK_D` t

  CROSS JOIN
    params p

  JOIN
    retailer_map r

    ON UPPER(TRIM(t.CNTRY))
       = UPPER(TRIM(r.CNTRY))

   AND UPPER(TRIM(t.ONLINE_STR))
       = UPPER(TRIM(r.RTLR_NAME))

  WHERE

        t.DATE BETWEEN p.START_DATE AND p.END_DATE

    AND LENGTH(
          TRIM(
            IFNULL(
              t.URL,
              ''
            )
          )
        ) > 0

    AND UPPER(TRIM(t.CAT)) IN (

      'WASHING MACHINE_HA',

      'REFRIGERATOR_HA',

      'DISHWASHER_HA',

      'DRYER_HA'

    )

),

sale_filtered AS (

  SELECT
    s.*

  FROM
    sale_base s

  JOIN
    brand_map b

    ON UPPER(TRIM(s.CNTRY))
       = UPPER(TRIM(b.CNTRY))

   AND (
         b.RTLR_NAME = '*'
      OR UPPER(TRIM(s.RTLR_NAME)) = UPPER(TRIM(b.RTLR_NAME))
       )

   AND UPPER(TRIM(s.DIV))
       = UPPER(TRIM(b.DIV))

   AND UPPER(TRIM(s.BRAND))
       = UPPER(TRIM(b.BRAND))

),

sale_deduped AS (

  SELECT
    *

  FROM
    sale_filtered

  QUALIFY

    ROW_NUMBER() OVER (

      PARTITION BY

        UPPER(TRIM(CNTRY)),

        UPPER(TRIM(RTLR_NAME)),

        UPPER(TRIM(DIV)),

        UPPER(TRIM(BRAND)),

        UPPER(CAT_URL_ADDR)

      ORDER BY

        RPT_DATE DESC,

        RK ASC,

        LENGTH(CAT_URL_ADDR) ASC,

        CAT_URL_ADDR ASC,

        RAW_URL ASC

    ) = 1

),

banr_base AS (

  SELECT

    t.DATE AS RPT_DATE,

    TRIM(t.CNTRY) AS CNTRY,

    TRIM(t.ONLINE_STR) AS RTLR_NAME,

    TRIM(t.BRAND) AS BRAND,

    CASE

      WHEN UPPER(TRIM(t.CAT)) = 'WASHING MACHINE_HA'
        THEN 'W/M'

      WHEN UPPER(TRIM(t.CAT)) = 'REFRIGERATOR_HA'
        THEN 'REF'

      WHEN UPPER(TRIM(t.CAT)) = 'DISHWASHER_HA'
        THEN 'D/W'

      WHEN UPPER(TRIM(t.CAT)) = 'DRYER_HA'
        THEN 'DRY'

      ELSE NULL

    END AS DIV,

    TRIM(IFNULL(t.RPC, '')) AS RPC,

    TRIM(IFNULL(t.MPC, '')) AS MPC,

    TRIM(t.URL) AS RAW_URL,

    REGEXP_REPLACE(
      TRIM(t.URL),
      r'[\?#].*$',
      ''
    ) AS CAT_URL_ADDR,

    COALESCE(

      NULLIF(
        UPPER(TRIM(t.MPC)),
        ''
      ),

      NULLIF(
        UPPER(TRIM(t.RPC)),
        ''
      ),

      UPPER(
        REGEXP_REPLACE(
          TRIM(t.URL),
          r'[\?#].*$',
          ''
        )
      )

    ) AS MODEL_DEDUP_KEY,

    t.PRODUCT_DESC,

    t.PRODUCT_IMG_URL,

    t.PRICE,

    t.DC_PRICE,

    t.CURRENCY,

    t.CAT,

    t.RK,

    'BANR_VSBLT' AS SOURCE_TYPE,

    2 AS SOURCE_PRIORITY

  FROM
    `pjt-lge-oned.L2_ONED.VSMRKT_DAILY_OSM_BANR_VSBLT_D` t

  CROSS JOIN
    params p

  JOIN
    retailer_map r

    ON UPPER(TRIM(t.CNTRY))
       = UPPER(TRIM(r.CNTRY))

   AND UPPER(TRIM(t.ONLINE_STR))
       = UPPER(TRIM(r.RTLR_NAME))

  WHERE

        t.DATE BETWEEN p.START_DATE AND p.END_DATE

    AND LENGTH(
          TRIM(
            IFNULL(
              t.URL,
              ''
            )
          )
        ) > 0

    AND UPPER(TRIM(t.CAT)) IN (

      'WASHING MACHINE_HA',

      'REFRIGERATOR_HA',

      'DISHWASHER_HA',

      'DRYER_HA'

    )

),

banr_filtered AS (

  SELECT
    s.*

  FROM
    banr_base s

  JOIN
    brand_map b

    ON UPPER(TRIM(s.CNTRY))
       = UPPER(TRIM(b.CNTRY))

   AND (
         b.RTLR_NAME = '*'
      OR UPPER(TRIM(s.RTLR_NAME)) = UPPER(TRIM(b.RTLR_NAME))
       )

   AND UPPER(TRIM(s.DIV))
       = UPPER(TRIM(b.DIV))

   AND UPPER(TRIM(s.BRAND))
       = UPPER(TRIM(b.BRAND))

),

banr_deduped AS (

  SELECT
    *

  FROM
    banr_filtered

  QUALIFY

    ROW_NUMBER() OVER (

      PARTITION BY

        UPPER(TRIM(CNTRY)),

        UPPER(TRIM(RTLR_NAME)),

        UPPER(TRIM(DIV)),

        UPPER(TRIM(BRAND)),

        UPPER(CAT_URL_ADDR)

      ORDER BY

        RPT_DATE DESC,

        RK ASC,

        LENGTH(CAT_URL_ADDR) ASC,

        CAT_URL_ADDR ASC,

        RAW_URL ASC

    ) = 1

),

combined_candidates AS (

  SELECT

    RPT_DATE,

    CNTRY,

    RTLR_NAME,

    BRAND,

    DIV,

    RPC,

    MPC,

    CAT_URL_ADDR,

    RAW_URL,

    MODEL_DEDUP_KEY,

    PRODUCT_DESC,

    RK,

    CAT,

    SOURCE_TYPE,

    SOURCE_PRIORITY

  FROM
    sale_deduped

  UNION ALL

  SELECT

    RPT_DATE,

    CNTRY,

    RTLR_NAME,

    BRAND,

    DIV,

    RPC,

    MPC,

    CAT_URL_ADDR,

    RAW_URL,

    MODEL_DEDUP_KEY,

    PRODUCT_DESC,

    RK,

    CAT,

    SOURCE_TYPE,

    SOURCE_PRIORITY

  FROM
    banr_deduped

),

cross_source_deduped AS (

  SELECT
    *

  FROM
    combined_candidates

  QUALIFY

    ROW_NUMBER() OVER (

      PARTITION BY

        UPPER(TRIM(CNTRY)),

        UPPER(TRIM(RTLR_NAME)),

        UPPER(TRIM(DIV)),

        UPPER(TRIM(BRAND)),

        UPPER(CAT_URL_ADDR)

      ORDER BY

        SOURCE_PRIORITY ASC,

        RPT_DATE DESC,

        RK ASC,

        LENGTH(CAT_URL_ADDR) ASC,

        CAT_URL_ADDR ASC,

        RAW_URL ASC

    ) = 1

),

final_capped AS (

  SELECT
    *

  FROM
    cross_source_deduped

  QUALIFY

    ROW_NUMBER() OVER (

      PARTITION BY

        UPPER(TRIM(CNTRY)),

        UPPER(TRIM(DIV)),

        UPPER(TRIM(RTLR_NAME))

      ORDER BY

        RPT_DATE DESC,

        RK ASC,

        MODEL_DEDUP_KEY ASC,

        CAT_URL_ADDR ASC

    ) <= 2000

),

sale_detail AS (

  SELECT

    RPT_DATE,

    CNTRY,

    RTLR_NAME,

    BRAND,

    DIV,

    MODEL_DEDUP_KEY,

    CAT_URL_ADDR,

    AVLBL_STAT,

    OBSRV_LIST_PRICE,

    OBSRV_DC_PRICE,

    CURRENCY_CODE,

    IMG_COUNT,

    VIDEO_COUNT,

    SALE_AMT,

    SALE_QTY,

    SEARCH_TERM

  FROM
    sale_deduped

),

banr_detail AS (

  SELECT

    RPT_DATE,

    CNTRY,

    RTLR_NAME,

    BRAND,

    DIV,

    MODEL_DEDUP_KEY,

    CAT_URL_ADDR,

    PRODUCT_IMG_URL,

    PRICE,

    DC_PRICE,

    CURRENCY

  FROM
    banr_deduped

)

SELECT

  f.RPT_DATE,

  f.CNTRY,

  f.RTLR_NAME,

  f.BRAND,

  f.DIV,

  f.RPC,

  f.MPC,

  f.CAT_URL_ADDR,

  f.RAW_URL,

  f.MODEL_DEDUP_KEY,

  f.PRODUCT_DESC,

  s.AVLBL_STAT,

  s.OBSRV_LIST_PRICE,

  s.OBSRV_DC_PRICE,

  s.CURRENCY_CODE,

  f.RK,

  f.CAT,

  s.IMG_COUNT,

  s.VIDEO_COUNT,

  s.SALE_AMT,

  s.SALE_QTY,

  s.SEARCH_TERM,

  b.PRODUCT_IMG_URL,

  b.PRICE,

  b.DC_PRICE,

  b.CURRENCY,

  f.SOURCE_TYPE

FROM
  final_capped f

LEFT JOIN
  sale_detail s

  ON  f.SOURCE_TYPE = 'SALE_RK'

  AND UPPER(TRIM(f.CNTRY))
      = UPPER(TRIM(s.CNTRY))

  AND UPPER(TRIM(f.RTLR_NAME))
      = UPPER(TRIM(s.RTLR_NAME))

  AND UPPER(TRIM(f.DIV))
      = UPPER(TRIM(s.DIV))

  AND UPPER(TRIM(f.BRAND))
      = UPPER(TRIM(s.BRAND))

  AND f.MODEL_DEDUP_KEY
      = s.MODEL_DEDUP_KEY

  AND f.CAT_URL_ADDR
      = s.CAT_URL_ADDR

  AND f.RPT_DATE
      = s.RPT_DATE

LEFT JOIN
  banr_detail b

  ON  f.SOURCE_TYPE = 'BANR_VSBLT'

  AND UPPER(TRIM(f.CNTRY))
      = UPPER(TRIM(b.CNTRY))

  AND UPPER(TRIM(f.RTLR_NAME))
      = UPPER(TRIM(b.RTLR_NAME))

  AND UPPER(TRIM(f.DIV))
      = UPPER(TRIM(b.DIV))

  AND UPPER(TRIM(f.BRAND))
      = UPPER(TRIM(b.BRAND))

  AND f.MODEL_DEDUP_KEY
      = b.MODEL_DEDUP_KEY

  AND f.CAT_URL_ADDR
      = b.CAT_URL_ADDR

  AND f.RPT_DATE
      = b.RPT_DATE

ORDER BY

  f.CNTRY,

  f.DIV,

  f.RTLR_NAME,

  f.BRAND,

  f.RK,

  f.MODEL_DEDUP_KEY;
