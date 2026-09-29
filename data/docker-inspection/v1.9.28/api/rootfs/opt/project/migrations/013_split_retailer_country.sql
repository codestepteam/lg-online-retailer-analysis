-- Migration 013: retailer 컬럼에서 국가 suffix 분리 + retailer→rtlr_name 통일
--
-- 배경
--   내부 레지스트리 키는 국가 suffix 를 포함한다 (Amazon_IT / Darty_FR / But_FR /
--   MediaExpert_PL / RtvEuroAgd_PL / MediaMarkt_ES — retailers.RETAILERS 참조).
--   DB 에는 이 조합 문자열이 그대로 저장돼 있어 "리테일러 순수명" 과 "국가" 가
--   한 컬럼에 뭉쳐 있음.
--
-- 변경
--   1) rtlr_name 값에서 국가 suffix 를 벗겨 순수 리테일러명만 저장:
--        Amazon_IT      → Amazon
--        Darty_FR       → Darty
--        But_FR         → But
--        MediaExpert_PL → MediaExpert
--        RtvEuroAgd_PL  → RtvEuroAgd
--        MediaMarkt_ES  → MediaMarkt
--      (Elcorteingles_electronica 는 국가 suffix 가 아니라 카테고리 식별자 —
--       ES 만 있는 ECI 전자제품 페이지 구분용이라 그대로 유지.
--       Coolblue / Boulanger / Mediaworld / Unieuro / Elgiganten 은 단국가 —
--       suffix 없음, 변경 없음.)
--
--   2) 컬럼명 통일: home_target_list / home_keywords / brand_target_list 는
--      아직 'retailer' 이름을 쓰고 있어 pdp_target_list.rtlr_name 과 어긋남.
--      → 모두 rtlr_name 으로 통일.
--
-- 다운스트림 호환 유지
--   내부 레지스트리 키(예: Amazon_IT)는 계속 이 형태 그대로 사용된다 —
--   폴더 경로 data/{batch}/*/crawl/Amazon_IT/, RETAILER_CONFIG, PAGE_TARGET_BUILDERS,
--   GNB_DEFS, SB_POLICY 딕셔너리 키 등. repo.load_*_targets 가 SELECT 시점에
--   core.retailers.composite_key(rtlr_name, cntry_cd) 로 재조합해 반환 (Python 후처리).
--
-- 실행: mysql -u <user> -p <db> < migrations/013_split_retailer_country.sql
-- ⚠️ 실행 전 백업: mysqldump -u <user> -p <db> pdp_target_list home_target_list \
--                  home_keywords brand_target_list > backup_pre_013.sql

-- ── 1) pdp_target_list.rtlr_name 값 정규화 ────────────────────────────────────
UPDATE pdp_target_list
   SET rtlr_name = CASE rtlr_name
         WHEN 'Amazon_IT'      THEN 'Amazon'
         WHEN 'Darty_FR'       THEN 'Darty'
         WHEN 'But_FR'         THEN 'But'
         WHEN 'MediaExpert_PL' THEN 'MediaExpert'
         WHEN 'RtvEuroAgd_PL'  THEN 'RtvEuroAgd'
         WHEN 'MediaMarkt_ES'  THEN 'MediaMarkt'
         ELSE rtlr_name
       END
 WHERE rtlr_name IN ('Amazon_IT','Darty_FR','But_FR','MediaExpert_PL','RtvEuroAgd_PL','MediaMarkt_ES');

-- ── 2) home_target_list: retailer → rtlr_name + 값 정규화 ─────────────────────
ALTER TABLE home_target_list
    CHANGE COLUMN retailer rtlr_name VARCHAR(64) NOT NULL COMMENT '내부 리테일러 순수명 (예: Amazon, Coolblue). 국가 suffix 없음.';

UPDATE home_target_list
   SET rtlr_name = CASE rtlr_name
         WHEN 'Amazon_IT'      THEN 'Amazon'
         WHEN 'Darty_FR'       THEN 'Darty'
         WHEN 'But_FR'         THEN 'But'
         WHEN 'MediaExpert_PL' THEN 'MediaExpert'
         WHEN 'RtvEuroAgd_PL'  THEN 'RtvEuroAgd'
         WHEN 'MediaMarkt_ES'  THEN 'MediaMarkt'
         ELSE rtlr_name
       END
 WHERE rtlr_name IN ('Amazon_IT','Darty_FR','But_FR','MediaExpert_PL','RtvEuroAgd_PL','MediaMarkt_ES');

-- UNIQUE 인덱스 재생성 (컬럼 rename 반영)
ALTER TABLE home_target_list DROP INDEX uq_home;
ALTER TABLE home_target_list ADD UNIQUE KEY uq_home (rtlr_name, cntry_code);

-- ── 3) home_keywords: retailer → rtlr_name + 값 정규화 ────────────────────────
ALTER TABLE home_keywords
    CHANGE COLUMN retailer rtlr_name VARCHAR(64) NOT NULL;

UPDATE home_keywords
   SET rtlr_name = CASE rtlr_name
         WHEN 'Amazon_IT'      THEN 'Amazon'
         WHEN 'Darty_FR'       THEN 'Darty'
         WHEN 'But_FR'         THEN 'But'
         WHEN 'MediaExpert_PL' THEN 'MediaExpert'
         WHEN 'RtvEuroAgd_PL'  THEN 'RtvEuroAgd'
         WHEN 'MediaMarkt_ES'  THEN 'MediaMarkt'
         ELSE rtlr_name
       END
 WHERE rtlr_name IN ('Amazon_IT','Darty_FR','But_FR','MediaExpert_PL','RtvEuroAgd_PL','MediaMarkt_ES');

ALTER TABLE home_keywords DROP INDEX uq_keyword;
ALTER TABLE home_keywords DROP INDEX idx_filter;
ALTER TABLE home_keywords
    ADD UNIQUE KEY uq_keyword (rtlr_name, cntry_code, loc_srch_kywd_info),
    ADD INDEX      idx_filter (cntry_code, rtlr_name);

-- ── 4) brand_target_list: retailer → rtlr_name + 값 정규화 ────────────────────
ALTER TABLE brand_target_list
    CHANGE COLUMN retailer rtlr_name VARCHAR(64) NOT NULL COMMENT '내부 리테일러 순수명 (예: Amazon, Coolblue).';

UPDATE brand_target_list
   SET rtlr_name = CASE rtlr_name
         WHEN 'Amazon_IT'      THEN 'Amazon'
         WHEN 'Darty_FR'       THEN 'Darty'
         WHEN 'But_FR'         THEN 'But'
         WHEN 'MediaExpert_PL' THEN 'MediaExpert'
         WHEN 'RtvEuroAgd_PL'  THEN 'RtvEuroAgd'
         WHEN 'MediaMarkt_ES'  THEN 'MediaMarkt'
         ELSE rtlr_name
       END
 WHERE rtlr_name IN ('Amazon_IT','Darty_FR','But_FR','MediaExpert_PL','RtvEuroAgd_PL','MediaMarkt_ES');

-- ⚠️ 실 UNIQUE 는 (rtlr_name, cntry_code, brand, category) 4개 컬럼 — 리테일러당
--    브랜드 메인('') 1행 + 카테고리별(WM/DR/WD/REF/FZ/FF/DW) 7행 = 총 8행 구조.
ALTER TABLE brand_target_list DROP INDEX uq_brand;
ALTER TABLE brand_target_list ADD UNIQUE KEY uq_brand (rtlr_name, cntry_code, brand, category);

-- ── 5) plp_target_list (있으면 값만 정규화 — 컬럼명은 mig 002 원본대로 유지) ─
--    plp_target_list 는 아직 dataset 헤더 정렬(mig 007) 미적용 상태 (retailer 컬럼).
--    현재는 데이터 미적재 → 값 정규화 UPDATE 만 조건부 실행 (있어도 no-op).
UPDATE plp_target_list
   SET retailer = CASE retailer
         WHEN 'Amazon_IT'      THEN 'Amazon'
         WHEN 'Darty_FR'       THEN 'Darty'
         WHEN 'But_FR'         THEN 'But'
         WHEN 'MediaExpert_PL' THEN 'MediaExpert'
         WHEN 'RtvEuroAgd_PL'  THEN 'RtvEuroAgd'
         WHEN 'MediaMarkt_ES'  THEN 'MediaMarkt'
         ELSE retailer
       END
 WHERE retailer IN ('Amazon_IT','Darty_FR','But_FR','MediaExpert_PL','RtvEuroAgd_PL','MediaMarkt_ES');
