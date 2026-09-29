-- Migration 041: brand_target_list — NL MediaMarkt LG 2행 추가 (EY 강지원 메일 2026-08-10)
--
-- 배경
--   0804 확정 시 NL MM 은 경쟁사 전용(시트1 기준 LG 행 0건)이었으나,
--   EY 회신(ID8/9/10 추가 수집 요청)으로 LG Brand Category Page 2건 신설:
--     REF 냉장고: https://www.mediamarkt.nl/nl/category/lg-koelkasten-964.html
--     WM  세탁기: https://www.mediamarkt.nl/nl/category/lg-wasmachines-968.html
--   멱등: brand_url 기준 NOT EXISTS.
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/041_brand_target_nlmm_lg.sql

INSERT INTO brand_target_list
    (brand_page_type, rtlr_name, cntry_cd, brand, category, sub_category, brand_url, notes)
SELECT 'Brand Category Page', 'MediaMarkt', 'NL', 'LG', 'REF', '냉장고',
       'https://www.mediamarkt.nl/nl/category/lg-koelkasten-964.html',
       'EY 메일 2026-08-10 (ID8/9/10 LG 추가)'
FROM DUAL WHERE NOT EXISTS (
  SELECT 1 FROM brand_target_list
  WHERE brand_url = 'https://www.mediamarkt.nl/nl/category/lg-koelkasten-964.html');

INSERT INTO brand_target_list
    (brand_page_type, rtlr_name, cntry_cd, brand, category, sub_category, brand_url, notes)
SELECT 'Brand Category Page', 'MediaMarkt', 'NL', 'LG', 'WM', '세탁기',
       'https://www.mediamarkt.nl/nl/category/lg-wasmachines-968.html',
       'EY 메일 2026-08-10 (ID8/9/10 LG 추가)'
FROM DUAL WHERE NOT EXISTS (
  SELECT 1 FROM brand_target_list
  WHERE brand_url = 'https://www.mediamarkt.nl/nl/category/lg-wasmachines-968.html');
