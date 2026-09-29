-- Migration 015: home_keywords.kywd_type 컬럼 추가 (문서화)
--
-- 배경
--   실 DB 에는 kywd_type ENUM('home','category') NOT NULL DEFAULT 'category' 이
--   이미 존재하나, migrations/ · schema.sql · docker/mysql/init/02_schema.sql 에
--   반영되지 않아 신규 환경 셋업 시 컬럼이 누락되는 문서-실측 갭이 있었다.
--
--   · kywd_type='home'     — home 트랙 검색 키워드 (ID1/2/4 소스). PLP 진단(ID11
--                            브랜드 필터 LG 존재 여부)에도 동일 키워드 재사용.
--   · kywd_type='category' — GNB 카테고리 매핑용 키워드 (ID3 소스). gnb_keyword_map
--                            × home_keywords 삼중키 JOIN 으로 카테고리 kw 만 골라냄
--                            (core/repo.load_home_gnb_targets 참조).
--
-- 변경
--   1) kywd_type 컬럼 IF NOT EXISTS 로 추가 (기존 환경 no-op)
--
-- 실행: mysql -u <user> -p <db> < migrations/015_home_keywords_kywd_type.sql
-- ⚠️ 실행 전 백업: mysqldump -u <user> -p <db> home_keywords > backup_pre_015.sql

-- ── home_keywords.kywd_type ──────────────────────────────────────────────────
-- MySQL 8.0+ 는 IF NOT EXISTS 지원. 미지원 버전이면 information_schema 로 가드.
ALTER TABLE home_keywords
    ADD COLUMN IF NOT EXISTS kywd_type ENUM('home', 'category') NOT NULL
        DEFAULT 'category'
        COMMENT 'home=home 트랙 검색 kw (ID1/2/4/11), category=GNB 카테고리 kw (ID3)';
