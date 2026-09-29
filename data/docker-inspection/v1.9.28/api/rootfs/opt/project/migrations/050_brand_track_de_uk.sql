-- 050: brand_track_list 에 DE·UK 취급 브랜드 등재 (2026-09-02)
--
-- 배경: 8/21 DE·UK 온보딩이 pdp_target_list 만 채우고 이 마스터를 빠뜨려,
--   ('REF','DE') ('REF','UK') ('WM','DE') ('WM','UK') 조합이 미등재였다.
--   결과 2가지 (20260902 배치 실측):
--     1) crawl 의 브랜드 트랙 필터가 "미등재 → 필터 없이 통과"라 DE·UK 만
--        LIEBHERR·AMICA 등 비트래킹 브랜드까지 전량 수집 (타 7개국은 트래킹만)
--     2) export_dash_raw._brand_type 이 같은 사전을 써서 DE·UK 는 LG 외
--        전부 OTHERS 로 찍힘 (SAMSUNG·BOSCH 같은 핵심 경쟁사 포함)
--
-- 출처: '대시보드 마트 설계_v1.0 (2).xlsx' > 데이터범위 시트 > 국가별 경쟁사 리스트
--   (M2:Q43 — 열 순서 W/M (+Dryer) / REF / DW / OVEN). 시트 나열 순서를
--   brand_rank 로 그대로 옮긴다 (기존 국가 규약과 동일: LG=1).
--
-- ⚠️ OVEN: 파이프라인에 OV 카테고리가 아직 없다(cat_cd 는 WM/REF/DW/DR/WD).
--   설계서에 있어 사전만 선등재해 둔다 — 수집·평가 배선은 별도.
-- ⚠️ DW: CATEGORY_COUNTRY_ALLOW 가 DW 를 ES 전용으로 막고 있어, DE·UK 의 DW
--   타깃은 적재 단계에서 차단된다. 데이터범위 시트는 Amazon DE·Currys·AO 를
--   DW 대상(O)으로 표시 — 게이트 해제는 core/config.py 수정이 선행돼야 한다.

INSERT INTO brand_track_list (cntry_cd, cat_cd, brand_name, brand_rank) VALUES
  -- DE : W/M (+Dryer)
  ('DE', 'WM',  'LG',       1),
  ('DE', 'WM',  'SAMSUNG',  2),
  ('DE', 'WM',  'BOSCH',    3),
  ('DE', 'WM',  'SIEMENS',  4),
  -- DE : REF
  ('DE', 'REF', 'LG',       1),
  ('DE', 'REF', 'SAMSUNG',  2),
  ('DE', 'REF', 'BOSCH',    3),
  ('DE', 'REF', 'LIEBHERR', 4),
  -- DE : DW
  ('DE', 'DW',  'LG',       1),
  ('DE', 'DW',  'BOSCH',    2),
  ('DE', 'DW',  'HISENSE',  3),
  -- DE : OVEN (선등재 — 수집 배선 없음)
  ('DE', 'OV',  'LG',       1),
  ('DE', 'OV',  'SAMSUNG',  2),
  ('DE', 'OV',  'HISENSE',  3),
  -- UK : W/M (+Dryer)
  ('UK', 'WM',  'LG',       1),
  ('UK', 'WM',  'SAMSUNG',  2),
  ('UK', 'WM',  'BOSCH',    3),
  ('UK', 'WM',  'HISENSE',  4),
  -- UK : REF
  ('UK', 'REF', 'LG',       1),
  ('UK', 'REF', 'SAMSUNG',  2),
  ('UK', 'REF', 'BOSCH',    3),
  ('UK', 'REF', 'HISENSE',  4),
  -- UK : DW
  ('UK', 'DW',  'LG',       1),
  ('UK', 'DW',  'BOSCH',    2),
  ('UK', 'DW',  'HISENSE',  3),
  -- UK : OVEN (선등재 — 수집 배선 없음)
  ('UK', 'OV',  'LG',       1),
  ('UK', 'OV',  'SAMSUNG',  2),
  ('UK', 'OV',  'HISENSE',  3)
ON DUPLICATE KEY UPDATE brand_rank = VALUES(brand_rank);
