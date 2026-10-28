-- BigQuery GoogleSQL: 이 파일 전체가 하나의 추출 쿼리입니다.
-- 2026-10-28 로컬 수정본. 실행 전 BigQuery 예상 처리량 확인 필요(실행 검증 전).
-- D058: Canada / Vietnam 10월19일(임시), 나머지 7곳은 기존 10월26일 유지.
-- 기존 V 뷰를 유지합니다. PTT_DATE 범위를 좁히는 조건은 추가하지 않았습니다.
-- 이유: 전체 국가에서 DATE와 PTT_DATE의 관계가 미확인이라 누락 방지.
-- 홈페이지 제외 후 제품군·브랜드·기존 URL 중복 제거·기존 2,000행 상한을 적용.
-- 건조기는 원본 SQL과 동일하게 세탁기 브랜드 목록 사용(별도 확정 기준 아님).
-- 리퍼·리셀·부품 제외는 이 SQL에서 수행하지 않음: 최종 진단 대상 확정 전 후보.
-- Canada CRAWL_URL에 영어 langId=-24 지정. RAW_URL 및 원본 LANG_FLAG도 보존.
-- CRAWL_URL 생성은 과거 OSM 자료가 영어였다는 검증이 아님. 실제 수집 후 확인 필요.
-- Costco .product.<ID>.html 과 /p/-/.../<ID> 간 동일 상품 병합은 이 SQL 범위 밖.

WITH

retailer_map AS (
  SELECT * FROM UNNEST([
    STRUCT('Canada' AS CNTRY, 'COSTCO' AS RTLR_NAME, DATE '2026-10-19' AS TARGET_DATE),
    STRUCT('Chile', 'FALABELLA', DATE '2026-10-26'),
    STRUCT('Mexico', 'LIVERPOOL', DATE '2026-10-26'),
    STRUCT('Brazil', 'MAGAZINELUIZA', DATE '2026-10-26'),
    STRUCT('SaudiArabia', 'EXTRA', DATE '2026-10-26'),
    STRUCT('Singapore', 'LAZADA', DATE '2026-10-26'),
    STRUCT('Thailand', 'LAZADA', DATE '2026-10-26'),
    STRUCT('Taiwan', 'MOMOSHOP', DATE '2026-10-26'),
    STRUCT('Vietnam', 'DIENMAYXANH', DATE '2026-10-19')
  ])
),

-- 출처: v2.2 엑셀 「경쟁브랜드」 시트 (2026-09-15 업데이트)
brand_map AS (
  SELECT m.CNTRY, m.DIV, BRAND
  FROM UNNEST([
    STRUCT('Canada' AS CNTRY, 'W/M' AS DIV, ['LG', 'SAMSUNG', 'GE', 'WHIRLPOOL', 'MIDEA'] AS BRANDS),
    STRUCT('Canada', 'REF', ['LG', 'SAMSUNG', 'FRIGIDAIRE', 'WHIRLPOOL', 'HISENSE']),
    STRUCT('Chile', 'W/M', ['LG', 'SAMSUNG', 'MIDEA', 'MADEMSA']),
    STRUCT('Chile', 'REF', ['LG', 'SAMSUNG', 'MIDEA', 'MADEMSA']),
    STRUCT('Mexico', 'W/M', ['LG', 'SAMSUNG', 'MABE', 'WHIRLPOOL']),
    STRUCT('Mexico', 'REF', ['LG', 'SAMSUNG', 'MABE', 'HISENSE']),
    STRUCT('Brazil', 'W/M', ['LG', 'SAMSUNG', 'ELECTROLUX', 'BRASTEMP', 'MIDEA']),
    STRUCT('Brazil', 'REF', ['LG', 'SAMSUNG', 'ELECTROLUX', 'BRASTEMP', 'MIDEA']),
    STRUCT('SaudiArabia', 'W/M', ['LG', 'SAMSUNG', 'MIDEA', 'TOSHIBA']),
    STRUCT('SaudiArabia', 'REF', ['LG', 'SAMSUNG', 'HITACHI', 'TOSHIBA']),
    STRUCT('Singapore', 'W/M', ['LG', 'SAMSUNG', 'TOSHIBA', 'MIDEA']),
    STRUCT('Singapore', 'REF', ['LG', 'SAMSUNG', 'HITACHI', 'PANASONIC']),
    STRUCT('Thailand', 'W/M', ['LG', 'SAMSUNG', 'TOSHIBA', 'HISENSE']),
    STRUCT('Thailand', 'REF', ['LG', 'SAMSUNG', 'TOSHIBA', 'HISENSE']),
    STRUCT('Taiwan', 'W/M', ['LG', 'PANASONIC', 'SANLUX', 'WHIRLPOOL']),
    STRUCT('Taiwan', 'REF', ['LG', 'PANASONIC', 'HITACHI', 'SANLUX']),
    STRUCT('Vietnam', 'W/M', ['LG', 'SAMSUNG', 'ELECTROLUX', 'TOSHIBA', 'AQUA']),
    STRUCT('Vietnam', 'REF', ['LG', 'SAMSUNG', 'TOSHIBA', 'AQUA'])
  ]) AS m,
  UNNEST(m.BRANDS) AS BRAND
),

raw_union AS (
  SELECT
    t.DATE AS RPT_DATE, t.CNTRY, t.ONLINE_STR, t.BRAND, t.CAT, t.RPC, t.MPC, t.URL,
    t.PRODUCT_DESC, t.RK,
    t.AVLBL_STAT, t.OBSRV_LIST_PRICE, t.OBSRV_DC_PRICE, t.CURRENCY_CODE,
    t.IMG_COUNT, t.VIDEO_COUNT, t.SALE_AMT, t.SALE_QTY, t.SEARCH_TERM,
    NULL AS PRODUCT_IMG_URL, NULL AS PRICE, NULL AS DC_PRICE, NULL AS CURRENCY,
    'SALE_RK' AS SOURCE_TYPE, 1 AS SOURCE_PRIORITY
  FROM `pjt-lge-oned.L2_ONED.VSMRKT_DAILY_OSM_SALE_RK_D` t
  WHERE t.DATE IN (DATE '2026-10-19', DATE '2026-10-26')

  UNION ALL

  SELECT
    t.DATE, t.CNTRY, t.ONLINE_STR, t.BRAND, t.CAT, t.RPC, t.MPC, t.URL,
    t.PRODUCT_DESC, t.RK,
    NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL, NULL,
    t.PRODUCT_IMG_URL, t.PRICE, t.DC_PRICE, t.CURRENCY,
    'BANR_VSBLT', 2
  FROM `pjt-lge-oned.L2_ONED.VSMRKT_DAILY_OSM_BANR_VSBLT_D` t
  WHERE t.DATE IN (DATE '2026-10-19', DATE '2026-10-26')
),

base AS (
  SELECT
    u.RPT_DATE,
    TRIM(u.CNTRY) AS CNTRY,
    TRIM(u.ONLINE_STR) AS RTLR_NAME,
    TRIM(u.BRAND) AS BRAND,
    CASE UPPER(TRIM(u.CAT))
      WHEN 'WASHING MACHINE_HA' THEN 'W/M'
      WHEN 'REFRIGERATOR_HA' THEN 'REF'
      WHEN 'DRYER_HA' THEN 'DRY'
    END AS DIV,
    TRIM(IFNULL(u.RPC, '')) AS RPC,
    TRIM(IFNULL(u.MPC, '')) AS MPC,
    TRIM(u.URL) AS RAW_URL,
    REGEXP_REPLACE(TRIM(u.URL), r'[\?#].*$', '') AS CAT_URL_ADDR,
    COALESCE(
      NULLIF(UPPER(TRIM(u.MPC)), ''),
      NULLIF(UPPER(TRIM(u.RPC)), ''),
      UPPER(REGEXP_REPLACE(TRIM(u.URL), r'[\?#].*$', ''))
    ) AS MODEL_DEDUP_KEY,
    -- 캐나다 Costco 영어(langId=-24)·불어(langId=-25) 구분 확인용 (D050)
    CASE
      WHEN REGEXP_REPLACE(UPPER(TRIM(u.CNTRY)), r'\s', '') != 'CANADA' THEN NULL
      WHEN REGEXP_CONTAINS(u.URL, r'langId=-25') THEN 'FR'
      WHEN REGEXP_CONTAINS(u.URL, r'langId=-24') THEN 'EN'
      ELSE 'langId 없음'
    END AS LANG_FLAG,
    u.* EXCEPT (RPT_DATE, CNTRY, ONLINE_STR, BRAND, RPC, MPC, URL)
  FROM raw_union u
  JOIN retailer_map r
    ON  REGEXP_REPLACE(UPPER(TRIM(u.CNTRY)), r'\s', '') = REGEXP_REPLACE(UPPER(r.CNTRY), r'\s', '')
    AND UPPER(TRIM(u.ONLINE_STR)) = UPPER(r.RTLR_NAME)
    AND u.RPT_DATE = r.TARGET_DATE
  WHERE LENGTH(TRIM(IFNULL(u.URL, ''))) > 0
    -- 국가 공통: 도메인 루트(홈페이지)는 상품 상세 후보에서 제외
    AND NOT REGEXP_CONTAINS(TRIM(u.URL), r'(?i)^https?://[^/?#]+/?([?#].*)?$')
    AND UPPER(TRIM(u.CAT)) IN ('WASHING MACHINE_HA', 'REFRIGERATOR_HA', 'DRYER_HA')
),

brand_filtered AS (
  SELECT s.*
  FROM base s
  JOIN brand_map b
    ON  REGEXP_REPLACE(UPPER(s.CNTRY), r'\s', '') = REGEXP_REPLACE(UPPER(b.CNTRY), r'\s', '')
    -- 건조기(DRY)는 세탁기(W/M) 브랜드 목록으로 거른다
    AND IF(s.DIV = 'DRY', 'W/M', s.DIV) = b.DIV
    AND UPPER(s.BRAND) = b.BRAND
),

deduped AS (
  SELECT *
  FROM brand_filtered
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY UPPER(CNTRY), UPPER(RTLR_NAME), DIV, UPPER(BRAND), UPPER(CAT_URL_ADDR)
    ORDER BY SOURCE_PRIORITY ASC, RPT_DATE DESC, RK ASC,
             LENGTH(CAT_URL_ADDR) ASC, CAT_URL_ADDR ASC, RAW_URL ASC
  ) = 1
),

final_capped AS (
  SELECT *
  FROM deduped
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY UPPER(CNTRY), DIV, UPPER(RTLR_NAME)
    ORDER BY RPT_DATE DESC, RK ASC, MODEL_DEDUP_KEY ASC, CAT_URL_ADDR ASC
  ) <= 2000
)

SELECT
  -- RAW_URL은 원본, CAT_URL_ADDR는 기존 중복 확인 주소, CRAWL_URL은 실제 접속 주소.
  CASE
    WHEN REGEXP_REPLACE(UPPER(CNTRY), r'\s', '') = 'CANADA'
      THEN CONCAT(CAT_URL_ADDR, '?langId=-24')
    ELSE RAW_URL
  END AS CRAWL_URL,
  CASE
    WHEN REGEXP_REPLACE(UPPER(CNTRY), r'\s', '') = 'CANADA'
      THEN '영어 요청 주소 생성; 실제 수집 후 언어 확인 필요'
    ELSE NULL
  END AS CRAWL_LANGUAGE_NOTE,
  RPT_DATE, CNTRY, RTLR_NAME, BRAND, DIV, RPC, MPC,
  CAT_URL_ADDR, RAW_URL, MODEL_DEDUP_KEY, PRODUCT_DESC,
  AVLBL_STAT, OBSRV_LIST_PRICE, OBSRV_DC_PRICE, CURRENCY_CODE,
  RK, CAT, IMG_COUNT, VIDEO_COUNT, SALE_AMT, SALE_QTY, SEARCH_TERM,
  PRODUCT_IMG_URL, PRICE, DC_PRICE, CURRENCY,
  SOURCE_TYPE, LANG_FLAG
FROM final_capped
ORDER BY CNTRY, DIV, RTLR_NAME, BRAND, RK, MODEL_DEDUP_KEY;
