-- Migration 014: cntry_code → cntry_cd 컬럼명 통일
--
-- 배경
--   국가 코드 컬럼이 두 표기로 갈라져 있음:
--     · cntry_cd   (3): country, gnb_brand_category_map, gnb_keyword_map
--     · cntry_code (6): brand_target_list, flixmedia_scope, home_keywords,
--                       home_target_list, ocr_lexicon, pdp_target_list
--   → cntry_cd 로 통일 (짧은 표기 + 마스터 country 테이블 기준).
--
-- 변경
--   1) 6개 테이블 CHANGE COLUMN cntry_code → cntry_cd (형·NULL·주석 유지)
--   2) UNIQUE / INDEX 재생성 (cntry_code 참조 인덱스)
--
-- 다운스트림
--   Python 은 이 마이그레이션과 동일 커밋에서 일괄 반영 (~55 refs).
--
-- 실행: mysql -u <user> -p <db> < migrations/014_rename_cntry_code_to_cntry_cd.sql
-- ⚠️ 실행 전 백업: mysqldump -u <user> -p <db> \
--     brand_target_list flixmedia_scope home_keywords home_target_list \
--     ocr_lexicon pdp_target_list > backup_pre_014.sql

-- ── 1) pdp_target_list ────────────────────────────────────────────────────────
ALTER TABLE pdp_target_list DROP INDEX uq_url;
ALTER TABLE pdp_target_list DROP INDEX idx_filter;
ALTER TABLE pdp_target_list
    CHANGE COLUMN cntry_code cntry_cd CHAR(2) NOT NULL COMMENT '국가 코드 대문자 (예: NL)';
ALTER TABLE pdp_target_list
    ADD UNIQUE KEY uq_url    (batch_id, cntry_cd, cat_url_addr(512)),
    ADD INDEX      idx_filter (batch_id, cntry_cd, rtlr_name);

-- ── 2) home_target_list ───────────────────────────────────────────────────────
ALTER TABLE home_target_list DROP INDEX uq_home;
ALTER TABLE home_target_list
    CHANGE COLUMN cntry_code cntry_cd CHAR(2) NOT NULL COMMENT '국가 코드 대문자 (예: NL) — pdp_target_list.cntry_cd 와 통일';
ALTER TABLE home_target_list ADD UNIQUE KEY uq_home (rtlr_name, cntry_cd);

-- ── 3) home_keywords ──────────────────────────────────────────────────────────
ALTER TABLE home_keywords DROP INDEX uq_keyword;
ALTER TABLE home_keywords DROP INDEX idx_filter;
ALTER TABLE home_keywords
    CHANGE COLUMN cntry_code cntry_cd CHAR(2) NOT NULL COMMENT '국가 코드 대문자 (예: NL)';
ALTER TABLE home_keywords
    ADD UNIQUE KEY uq_keyword (rtlr_name, cntry_cd, loc_srch_kywd_info),
    ADD INDEX      idx_filter (cntry_cd, rtlr_name);

-- ── 4) brand_target_list ──────────────────────────────────────────────────────
ALTER TABLE brand_target_list DROP INDEX uq_brand;
ALTER TABLE brand_target_list
    CHANGE COLUMN cntry_code cntry_cd CHAR(2) NOT NULL COMMENT '국가 코드 대문자 (예: NL)';
ALTER TABLE brand_target_list ADD UNIQUE KEY uq_brand (rtlr_name, cntry_cd, brand, category);

-- ── 5) flixmedia_scope ────────────────────────────────────────────────────────
ALTER TABLE flixmedia_scope DROP INDEX uq_scope;
ALTER TABLE flixmedia_scope
    CHANGE COLUMN cntry_code cntry_cd CHAR(2) NOT NULL;
ALTER TABLE flixmedia_scope ADD UNIQUE KEY uq_scope (retailer, cntry_cd);

-- ── 6) ocr_lexicon ────────────────────────────────────────────────────────────
ALTER TABLE ocr_lexicon DROP INDEX uq_term;
ALTER TABLE ocr_lexicon DROP INDEX idx_lookup;
ALTER TABLE ocr_lexicon
    CHANGE COLUMN cntry_code cntry_cd CHAR(2) NOT NULL COMMENT '국가 대문자. EN=6개국 공통(브랜드토큰·mm·TÜV 등)';
ALTER TABLE ocr_lexicon
    ADD UNIQUE KEY uq_term    (metric, slot, cntry_cd, term),
    ADD INDEX      idx_lookup (metric, cntry_cd);
