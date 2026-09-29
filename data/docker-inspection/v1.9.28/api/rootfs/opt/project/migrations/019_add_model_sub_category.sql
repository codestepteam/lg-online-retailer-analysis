-- Migration 019: model_sub_category 테이블 추가
--
-- 배경
--   v1.5 ID24/25/35/45 — 카테고리 표준 USP 가 서브카테고리로 분화됨
--   (pdp_usp_keywords.sub_category_code: REF = SBS/FDR, 참고4 v1.5_260709).
--   어떤 모델이 어느 서브카테고리인지는 EY 참고11 '카테고리 매핑 테이블'
--   Kitchen 블록(Model.Suffix × Category group)이 정본 — 이 테이블에 적재한다.
--
--   매핑 규칙 (2026-07-10 확정):
--     Category group F/D → FDR, 그 외(B/F·SxS·T/F·L&F·B/in·기타) → SBS
--     (참고4 가 'F/D=하위모델, 나머지=상위모델' 로만 구분).
--   model 은 Model.Suffix 의 닷(.) 앞 베이스 모델 대문자 — pdp_target_list.mpc
--   도 같은 규칙으로 정규화해 조인한다 (refdata.sub_category_for_model).
--   매핑 실패(경쟁사/미등재 모델)는 카테고리 합집합 폴백 (현행 동작 유지).
--
--   관리: /masters/model_sub_category 업로드로 전체 교체 (마스터 — batch 무관).
--
-- 실행: mysql -u <user> -p <db> < migrations/019_add_model_sub_category.sql

CREATE TABLE IF NOT EXISTS model_sub_category (
    id                BIGINT NOT NULL AUTO_INCREMENT,
    category_code     VARCHAR(10)  NOT NULL COMMENT '제품군 코드 (REF/WM/... — naming.cat_code 표준)',
    model             VARCHAR(64)  NOT NULL COMMENT '베이스 모델 (Model.Suffix 닷 앞, 대문자)',
    sub_category_code VARCHAR(20)  NOT NULL COMMENT 'pdp_usp_keywords.sub_category_code 와 조인 (SBS/FDR)',
    category_group    VARCHAR(32)  NULL COMMENT '참고11 Category group 원문 (B/F, SxS, F/D ... — 추적용)',
    created_at        TIMESTAMP    NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_cat_model (category_code, model),
    KEY idx_model (model)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
  COMMENT='모델→USP 서브카테고리 매핑 마스터 (EY 참고11 — ID24/25/35/45 세트 선택)';
-- collation 은 마스터 테이블(pdp_usp_keywords)과 통일 (utf8mb4_unicode_ci).
-- ⚠️ pdp_target_list 는 utf8mb4_0900_ai_ci 라 mpc 와 SQL 직접 조인 시 1267 —
-- 비교측에 COLLATE utf8mb4_0900_ai_ci 명시 필요 (운영 코드는 파이썬 단건 조회라 무관).
