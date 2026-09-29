-- Migration 020: pdp_usp_keywords 에 cntry_cd (국가 전용 USP 세트) 추가
--
-- 배경
--   FR(프랑스) 리테일러(Darty·Boulanger)는 USP 를 현지어/현지 표기로 노출
--   (HS KEY USP_rev.xlsx 2607 시트 — French 컬럼, 2026-07 EY 전달).
--   → 국가 전용 키워드 세트를 같은 테이블에 cntry_cd 로 구분해 적재한다.
--
-- 의미 규칙 (2026-07-14 확정)
--   cntry_cd = NULL : 기본(공통) 세트 — 전용 세트가 없는 국가 전부에 적용
--   cntry_cd = 'FR' : 프랑스 전용 세트 — FR 은 이 세트만 사용 (기본 세트 미적용)
--   즉 "해당 카테고리에 국가 전용 행이 하나라도 있으면 그 국가는 전용 세트만,
--   없으면 NULL 세트" — refdata.usp_for_category(cntry_cd=..) 가 판정.
--   추후 ES/IT/NL/SE/PL 번역이 오면 행만 추가하면 코드 수정 없이 분기된다.
--
--   원본 xlsx 의 'A / B' 병기(표기 변형)는 행 분리 적재 — eval 매칭이
--   행 단위 정규화 부분일치이므로 병기 문자열 통째로는 절대 매칭 안 됨.
--   (기존 관행 동일: 'FreshConverter / FreshBalancer' → 개별 행)
--
--   컬럼명/값은 표준 컨벤션(mig 014): cntry_cd, 대문자 2자 ('FR').
--
-- 실행: mysql -u <user> -p <db> < migrations/020_add_usp_cntry_cd.sql

ALTER TABLE pdp_usp_keywords
    ADD COLUMN cntry_cd VARCHAR(2) NULL DEFAULT NULL
        COMMENT '국가 전용 세트 (NULL=기본 — 전용 세트 없는 국가에 적용)'
        AFTER sub_category_code,
    ADD INDEX idx_cntry (category_code, cntry_cd);
