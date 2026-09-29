-- Migration 012: home_keywords 를 마스터 테이블로 회귀 (batch_id/report_date 제거)
-- 실행: mysql -u <user> -p <db> < migrations/012_home_keywords_master.sql
--
-- 배경
--   mig 010 에서 home_keywords 를 batch-scoped 로 만들었으나, 실제 운영 요구는
--   "리테일러 × 국가 × 키워드" 마스터 (LG HS 팀이 가끔 갱신) — 배치별로 다른
--   키워드셋을 유지할 필요가 없다. 산출물(HTML/파싱/리포트)은 이미 data/{batch_id}/
--   home/ 로 스냅샷 남음.
--   home_target_list 와 동일한 배치 무관 마스터로 통일.
--
-- 변경
--   · batch_id, report_date 컬럼 제거
--   · UNIQUE (batch_id, retailer, cntry_code, loc_srch_kywd_info)
--       → UNIQUE (retailer, cntry_code, loc_srch_kywd_info)
--   · idx_batch, idx_filter 제거 (batch_id 없음) + idx_filter (cntry_code, retailer) 재생성
--
-- 데이터
--   기존 batch_id='20260704' 94행 + batch_id='legacy' 15행이 있음. legacy 는 삭제,
--   20260704 만 남기고 batch_id/report_date 컬럼 drop (중복은 UNIQUE 로 무산 → 그대로 살아남음).

DELETE FROM home_keywords WHERE batch_id = 'legacy';

ALTER TABLE home_keywords DROP INDEX uq_keyword;
ALTER TABLE home_keywords DROP INDEX idx_batch;
ALTER TABLE home_keywords DROP INDEX idx_filter;

ALTER TABLE home_keywords DROP COLUMN batch_id;
ALTER TABLE home_keywords DROP COLUMN report_date;

ALTER TABLE home_keywords
    ADD UNIQUE KEY uq_keyword (retailer, cntry_code, loc_srch_kywd_info),
    ADD INDEX      idx_filter (cntry_code, retailer);
