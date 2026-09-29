-- 052 — L1 마트 표기 규약 통일 (2026-09-03 사용자 확정)
--
-- OSM L1 파일과 같은 어휘로 맞춘다 — 두 소스가 한 테이블에서 조인·집계되므로
-- 표기가 갈리면 브랜드·리테일러·제품군 축이 전부 두 벌이 된다.
--   site_name  → 대문자        (MediaMarkt → MEDIAMARKT)
--   brand_name → 소문자        (SAMSUNG → samsung)
--   product    → 풀네임 3종    (REF → REFRIGERATOR / WM·DR·WD → WASHING MACHINE
--                               / DW → DISHWASHER)
--
-- 건조기(DR)·세탁건조기(WD)는 **WM 상위 카테고리로 접는다** — 사용자 확정.
-- 냉동고(FZ)·냉장냉동고(FF)도 같은 규약(BRAND_SUB_GROUP_MAP)으로 REF 에 속한다.
--
-- ⚠️ **EY 리포트에는 적용하지 않는다** — 리포트 Category 는 종전 코드 표기
--    (core/naming.report_category) 그대로다. 이 규약은 마트 적재 전용.

UPDATE l1_visibility SET
    site_name  = UPPER(site_name),
    brand_name = LOWER(brand_name),
    product    = CASE product
        WHEN 'WM'  THEN 'WASHING MACHINE' WHEN 'DR' THEN 'WASHING MACHINE'
        WHEN 'WD'  THEN 'WASHING MACHINE'
        WHEN 'REF' THEN 'REFRIGERATOR'    WHEN 'FZ' THEN 'REFRIGERATOR'
        WHEN 'FF'  THEN 'REFRIGERATOR'
        WHEN 'DW'  THEN 'DISHWASHER'
        ELSE product END;

UPDATE l1_conversion SET
    site_name  = UPPER(site_name),
    brand_name = LOWER(brand_name),
    product    = CASE product
        WHEN 'WM'  THEN 'WASHING MACHINE' WHEN 'DR' THEN 'WASHING MACHINE'
        WHEN 'WD'  THEN 'WASHING MACHINE'
        WHEN 'REF' THEN 'REFRIGERATOR'    WHEN 'FZ' THEN 'REFRIGERATOR'
        WHEN 'FF'  THEN 'REFRIGERATOR'
        WHEN 'DW'  THEN 'DISHWASHER'
        ELSE product END;

UPDATE l1_flixmedia SET
    site_name  = UPPER(site_name),
    brand_name = LOWER(brand_name),
    product    = CASE product
        WHEN 'WM'  THEN 'WASHING MACHINE' WHEN 'DR' THEN 'WASHING MACHINE'
        WHEN 'WD'  THEN 'WASHING MACHINE'
        WHEN 'REF' THEN 'REFRIGERATOR'    WHEN 'FZ' THEN 'REFRIGERATOR'
        WHEN 'FF'  THEN 'REFRIGERATOR'
        WHEN 'DW'  THEN 'DISHWASHER'
        ELSE product END;
