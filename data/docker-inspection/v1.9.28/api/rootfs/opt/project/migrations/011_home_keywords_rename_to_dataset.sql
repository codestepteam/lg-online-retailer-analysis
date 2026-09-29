-- Migration 011: home_keywords 컬럼명을 dataset 헤더로 정렬
-- 실행: mysql -u <user> -p <db> < migrations/011_home_keywords_rename_to_dataset.sql
--
-- 배경
--   pdp_target_list 는 mig 007 에서 dataset 헤더(cntry_code/div/mpc/rpc/rtlr_name/cat_url_addr)
--   로 정렬해 원본 스키마와 일치시켰다. home_keywords 는 아직 코드 뿌리(keyword /
--   english_keyword / category)로 남아 있어 dataset(LOC_SRCH_KYWD_INFO / ENG_SRCH_KYWD_INFO
--   / SRCH_KYWD_CAT_NAME)과 어긋난다.
--
-- 변경
--   keyword          → loc_srch_kywd_info
--   english_keyword  → eng_srch_kywd_info
--   category         → srch_kywd_cat_name
--
-- 다운스트림 호환
--   repo.load_home_targets 는 SELECT ... AS keyword / english_keyword / category 로 alias
--   유지 → crawl_retailers/parse_retailers/eval 는 무변경.

ALTER TABLE home_keywords
    CHANGE COLUMN keyword         loc_srch_kywd_info VARCHAR(255) NOT NULL COMMENT 'LOC_SRCH_KYWD_INFO — 실제 검색어 (로컬)',
    CHANGE COLUMN english_keyword eng_srch_kywd_info VARCHAR(255)     NULL COMMENT 'ENG_SRCH_KYWD_INFO — 라벨/폴백 (영문)',
    CHANGE COLUMN category        srch_kywd_cat_name VARCHAR(64)      NULL COMMENT 'SRCH_KYWD_CAT_NAME — 리포트 그룹핑 라벨';

-- 인덱스 uq_keyword 는 keyword 를 참조하므로 재생성
ALTER TABLE home_keywords DROP INDEX uq_keyword;
ALTER TABLE home_keywords ADD UNIQUE KEY uq_keyword (batch_id, retailer, cntry_code, loc_srch_kywd_info);
