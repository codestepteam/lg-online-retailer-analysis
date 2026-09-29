-- Migration 007: pdp_target_list 컬럼명을 원본 데이터셋 헤더에 맞춤
--
-- dataset/pdp_list.xlsx 원본 헤더:
--   CNTRY, RTLR_NAME, BRAND, DIV, RPC, MPC, CAT_URL_ADDR
--
-- 변경 요약:
--   instance   → cntry         (값은 여전히 국가코드 ES/IT/FR/NL/SE — 크롤러 필터 호환)
--   category1  → div            (값은 REF/WM — 슬래시 제거)
--   category2  → DROP           (사용 안 함 — CLAUDE 확정)
--   model_mpc  → mpc
--   retailer   → rtlr_name      (값은 내부 리테일러 키 Amazon_IT/Darty_FR — 크롤러 라우팅 호환)
--   url        → cat_url_addr
--   product_id (유지, uuid5 파생)
--   rpc, brand (유지)
--
-- 다운스트림 (crawl.py/parse.py/eval.py/crawl_retailers/*) 은 dict key
-- instance/category1/model_mpc/retailer/url 를 그대로 쓴다 → repo.load_targets 에서
-- SELECT ... AS <old> 로 alias 하여 호환. INSERT 는 신규 컬럼명 사용.
--
-- 실행: mysql -u {user} -p {db} < migrations/007_rename_columns_to_dataset.sql

ALTER TABLE pdp_target_list
    CHANGE COLUMN instance   cntry        VARCHAR(8)   NOT NULL,
    CHANGE COLUMN category1  div          VARCHAR(16)  NOT NULL,
    CHANGE COLUMN model_mpc  mpc          VARCHAR(64)  NULL,
    CHANGE COLUMN retailer   rtlr_name    VARCHAR(64)  NOT NULL,
    CHANGE COLUMN url        cat_url_addr TEXT         NOT NULL,
    DROP COLUMN category2;

-- 인덱스 재생성 (컬럼 rename 후 정의는 유지되지만 명확히 재생성)
DROP INDEX uq_url    ON pdp_target_list;
DROP INDEX idx_filter ON pdp_target_list;
ALTER TABLE pdp_target_list
    ADD UNIQUE KEY uq_url    (batch_id, cntry, cat_url_addr(512)),
    ADD INDEX      idx_filter (batch_id, cntry, rtlr_name);
