-- 051 — L1 마트 product_name 폭 확대 (2026-09-03)
--
-- 20260807 월간 적재가 1406(Data too long for column 'product_name')으로 죽었다.
-- Darty_FR 파서가 제품명 자리에 마케팅 본문을 통째로 실어 보내는 레코드가 있고
-- (최대 3,980자 / 512 초과 17건), VARCHAR(512) 로는 못 담는다.
--
-- 1024 로 넓힌다 — 정상 제품명은 200자 안쪽이라 충분하고, 4,000자짜리 쓰레기를
-- 스키마로 승인하지는 않는다. 초과분은 적재기가 잘라 넣고 경고를 남긴다
-- (export_dash_raw._trunc). 근본 원인인 Darty 제목 파싱은 별건.

ALTER TABLE l1_visibility MODIFY COLUMN product_name VARCHAR(1024) DEFAULT NULL;
ALTER TABLE l1_conversion MODIFY COLUMN product_name VARCHAR(1024) DEFAULT NULL;
ALTER TABLE l1_flixmedia  MODIFY COLUMN product_name VARCHAR(1024) DEFAULT NULL;
