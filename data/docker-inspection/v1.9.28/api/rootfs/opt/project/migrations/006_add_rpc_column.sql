-- Migration 006: pdp_target_list 에 rpc 컬럼 추가
--
-- 배경:
--   신규 원본 데이터셋 (dataset/pdp_list.xlsx) 은 RPC (Retailer Product Code) 를
--   상품 식별자로 사용한다. 같은 RPC 라도 리테일러/URL 이 다르면 별개 행이므로
--   유니크 키는 여전히 (batch_id, instance, url) 로 유지하고, RPC 는 조회/집계용
--   보조 컬럼으로 저장한다. product_id 는 uuid5(NS, f"{rpc}|{url}") 로 파생.
--
-- 실행: mysql -u {user} -p {db} < migrations/006_add_rpc_column.sql

ALTER TABLE pdp_target_list
    ADD COLUMN rpc VARCHAR(64) NULL AFTER model_mpc,
    ADD INDEX idx_rpc (rpc);
