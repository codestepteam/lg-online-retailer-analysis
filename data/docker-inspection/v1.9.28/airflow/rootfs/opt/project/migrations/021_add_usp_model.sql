-- Migration 021: pdp_usp_keywords 에 model (SKU 전용 USP 세트) 추가
--
-- 배경
--   USP 판정 기준이 카테고리 표준 세트 → lg.com 실크롤 SKU(세일즈 모델)별
--   eyebrow 로 전환 (2026-07-15 확정 — '260615 lg.com feature bodycopy
--   crawling_EU7.xlsx', 7개국 se/pl/it/fr/es/cz/nl).
--   eyebrow = lg.com PDP feature 블록의 USP 라벨 — 국가별 현지어 표기 그대로라
--   FR 현지어 세트(mig 020) 문제를 SKU 세트가 자연 해소한다.
--
-- 의미 규칙 (2026-07-15 확정)
--   model IS NULL     : 기존 카테고리 세트 행 — eval 은 더 이상 사용하지 않지만
--                       구 배치 리포트 폴백(report_xlsx._id24)용으로 보존.
--   model IS NOT NULL : SKU 전용 세트 — (cntry_cd, model) 정확 일치로만 조회
--                       (refdata.usp_for_model). 국가/카테고리 폴백 없음.
--   SKU 행이 없는 타깃(단종·리테일러 전용 파생 모델, LG 외 타 브랜드)은
--   ID24/25/35/45 판정 패스(MISSING) — 2026-07-15 확정.
--   model 은 베이스 모델 대문자 — lg.com sales model 은 슬러그 형태
--   ('LG-F14X56WHST-LAVE-LINGE')라 'LG-' 접두 제거 + 첫 하이픈 토큰 추출,
--   타깃 mpc 는 닷(.) 앞 토큰 (기존 mig 019 규칙과 동일).
--   category_code 는 SKU 행에서 쓰지 않음 → NULL 허용으로 완화.
--
--   관리: /masters/usp_sku_keywords 업로드로 SKU 행만 전체 교체
--   (기존 /masters/usp_keywords 는 카테고리 행만 교체하도록 스코프 분리).
--
-- 실행: mysql -u <user> -p <db> < migrations/021_add_usp_model.sql

ALTER TABLE pdp_usp_keywords
    MODIFY category_code VARCHAR(10) NULL COMMENT '제품군 코드 (카테고리 세트 행 전용 — SKU 행은 NULL)',
    ADD COLUMN model VARCHAR(64) NULL
        COMMENT 'SKU 전용 세트 베이스 모델 (NULL=카테고리 세트 행 — mig 021)'
        AFTER cntry_cd,
    ADD INDEX idx_model (model, cntry_cd);
