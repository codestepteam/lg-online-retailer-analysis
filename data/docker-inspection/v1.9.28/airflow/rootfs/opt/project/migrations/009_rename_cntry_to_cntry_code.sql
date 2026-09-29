-- Migration 009: pdp_target_list.cntry → cntry_code
--
-- 배경: 컬럼명은 dataset 헤더(CNTRY)를 따라 지었지만, 실제 저장값은 항상 2글자
-- 국가코드(ES/IT/FR/NL/SE/PL)라 이름과 의미가 어긋난다 (pdp_dataset.normalize_pdp_df
-- 가 ITALY→IT 등으로 정규화 후 저장).
--
-- 변경: cntry → cntry_code (값·타입 동일, 이름만 의미에 맞춤).
--
-- 인덱스 uq_url / idx_filter 는 cntry 를 참조하므로 rename 후 재생성.
--
-- 실행: mysql -u {user} -p {db} < migrations/009_rename_cntry_to_cntry_code.sql

ALTER TABLE pdp_target_list
    CHANGE COLUMN cntry cntry_code VARCHAR(8) NOT NULL;

DROP INDEX uq_url    ON pdp_target_list;
DROP INDEX idx_filter ON pdp_target_list;
ALTER TABLE pdp_target_list
    ADD UNIQUE KEY uq_url    (batch_id, cntry_code, cat_url_addr(512)),
    ADD INDEX      idx_filter (batch_id, cntry_code, rtlr_name);
