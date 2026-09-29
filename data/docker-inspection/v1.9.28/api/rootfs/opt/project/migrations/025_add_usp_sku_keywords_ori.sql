-- Migration 025: usp_sku_keywords_ori — lg.com feature bodycopy 크롤 원본 보존 테이블
--
-- 배경
--   pdp_usp_keywords 의 SKU 세트(mig 021)는 원본 xlsx 에서 (국가, 베이스 모델,
--   eyebrow)만 추출·정규화한 파생본이다. 추출 규칙 검증/재적재/다른 컬럼
--   (headline·bodycopy·div_name 등) 활용을 위해 원본 파일을 행 그대로 보존한다.
--   소스: '260615 lg.com feature bodycopy crawling_EU7.xlsx' (7개국, 28,959행).
--
--   컬럼명은 xlsx 헤더를 snake_case 로만 바꾼 것 — 값 가공 없음
--   (sales_model 도 슬러그 원문 그대로. 베이스 모델 정규화는 repo.usp_sku_base_model).
--   전체 교체 방식 적재 (원본 파일이 곧 전체 상태).
--
--   ※ 원래 022 로 작성돼 DB(devtools lg_clinic)에 이미 적용된 DDL 인데 파일이
--     유실됐던 것을 복원 (2026-07-15). 022~024 번호는 ocr_lexicon/market_dataset/
--     brand_track_list 가 선점 → 025 로 재번호. 내용은 적용본과 동일.
--
-- 실행: mysql -u <user> -p <db> < migrations/025_add_usp_sku_keywords_ori.sql

CREATE TABLE IF NOT EXISTS usp_sku_keywords_ori (
    id               BIGINT NOT NULL AUTO_INCREMENT,
    get_date         DATETIME     NULL COMMENT '크롤 일자 (xlsx get_date)',
    url              TEXT         NULL COMMENT 'lg.com PDP URL',
    country          VARCHAR(8)   NULL COMMENT '국가 (se/pl/it/fr/es/cz/nl — 원문 소문자)',
    product          VARCHAR(128) NULL COMMENT 'lg.com 제품군 슬러그 (원문)',
    product_category VARCHAR(128) NULL COMMENT 'lg.com 카테고리 슬러그 (원문)',
    sales_model      VARCHAR(128) NULL COMMENT '세일즈 모델 (원문 — FR 은 URL 슬러그)',
    div_name         TEXT         NULL COMMENT 'feature 블록 div 셀렉터 (원문)',
    eyebrow          TEXT         NULL COMMENT 'USP 라벨 — pdp_usp_keywords SKU 세트의 소스',
    headline         TEXT         NULL COMMENT 'feature 블록 headline',
    bodycopy         TEXT         NULL COMMENT 'feature 블록 bodycopy',
    created_at       TIMESTAMP    NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_country_model (country, sales_model)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
  COMMENT='lg.com feature bodycopy 크롤 원본 (EU7 xlsx 그대로 — SKU USP 소스 보존)';
