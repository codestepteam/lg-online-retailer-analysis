-- Migration 004: home 트랙 스키마 정리
-- 실행: mysql -u <user> -p <db> < migrations/004_home_search.sql
--
-- 배경
--   기존 home_target_list 는 batch-scoped 리테일러 선택만 담당했으나,
--   검색 URL 조립을 위한 템플릿 저장소가 없어 `--page-type home` 로 검색 결과를 저장할 수 없었다.
--   → 리테일러 마스터(홈 URL + 검색 URL 템플릿) 를 별도 고정 테이블로 두고,
--     home_keywords 에는 로컬/영문 키워드와 라벨용 카테고리를 추가한다.
--
-- 흐름
--   home_search_config (retailer, instance)          -- 리테일러 마스터, 배치 무관
--     × home_keywords     (retailer, instance)       -- 검색 키워드, 배치 무관
--     → 검색 URL 조립: template.replace('{q}', quote_plus(local_keyword))

-- ── home_search_config ────────────────────────────────────────────────────────
-- 리테일러별 홈페이지 URL + 검색 URL 템플릿 (고정, 배치 무관)
CREATE TABLE IF NOT EXISTS home_search_config (
    id                  INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    retailer            VARCHAR(64)   NOT NULL COMMENT '내부 리테일러 키 (예: Coolblue)',
    instance            CHAR(2)       NOT NULL COMMENT '국가 코드 대문자 (예: NL)',
    home_url            VARCHAR(2048) NOT NULL COMMENT '홈페이지 URL',
    search_url_template VARCHAR(2048)     NULL COMMENT '{q} placeholder 포함 검색 URL. NULL 이면 검색 미방출(But/Darty 등 차단).',
    PRIMARY KEY (id),
    UNIQUE KEY uq_home_search (retailer, instance)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── home_keywords 확장 ───────────────────────────────────────────────────────
-- 기존: (id, retailer, instance, keyword)
-- 추가: english_keyword, category  (라벨/폴백/집계용)
-- NOTE: 기존 keyword 컬럼 = LOC_SRCH_KYWD_INFO (실제 검색어)
ALTER TABLE home_keywords
    ADD COLUMN english_keyword VARCHAR(255) NULL COMMENT 'ENG_SRCH_KYWD_INFO — 폴백/라벨용' AFTER keyword,
    ADD COLUMN category        VARCHAR(64)  NULL COMMENT 'SRCH_KYWD_CAT_NAME — 리포트 그룹핑용 라벨 (Refrigerator/Washing Machine/...)' AFTER english_keyword;
