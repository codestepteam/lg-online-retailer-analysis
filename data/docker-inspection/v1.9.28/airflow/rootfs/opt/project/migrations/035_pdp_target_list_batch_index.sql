-- 035_pdp_target_list_batch_index.sql
-- pdp_target_list.batch_id 인덱스 보증 (2026-07-23).
--
-- 배경: 배치 단위 필터(WHERE batch_id = ?)가 주 접근 패턴인데 12만 행에서
-- 지연이 관측됨. schema.sql 기준으로 idx_batch(batch_id) 는 이미 존재하지만
-- (uq_url·idx_filter 최좌측 프리픽스도 batch_id 로 커버), 라이브 테이블이
-- 컬럼 리네임 마이그레이션(007/009)을 거친 이력이 있어 인덱스 실재를 보증한다.
--
-- ⚠️ 지연의 유력 원인은 인덱스 부재가 아니라 batch_id 를 INT 로 바인딩해
-- 인덱스가 무력화되는 것(repo.base_batch_id 주석 참조 — varchar 컬럼에 int
-- 비교 시 full scan). 이 마이그레이션은 인덱스 실재만 보장하고, 그 함정은
-- 호출부에서 str 바인딩으로 막아야 한다.
--
-- MySQL 은 CREATE INDEX IF NOT EXISTS 를 지원하지 않으므로 information_schema
-- 가드로 멱등 처리한다. 이미 있으면 no-op, 없을 때만 ADD INDEX.

SET @idx_exists := (
    SELECT COUNT(*) FROM information_schema.statistics
    WHERE table_schema = DATABASE()
      AND table_name   = 'pdp_target_list'
      AND index_name   = 'idx_batch'
);

SET @ddl := IF(@idx_exists = 0,
    'ALTER TABLE pdp_target_list ADD INDEX idx_batch (batch_id)',
    'DO 0  /* idx_batch 이미 존재 — no-op */');

PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
