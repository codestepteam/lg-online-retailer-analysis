-- 016: 이미지 메타 영구 캐시 (URL sha 키, blob 미저장 — 2026-07-08 설계 확정)
--
-- 목적: 갤러리/본문 전량 OCR 체제에서 배치 간 중복 다운로드·OCR 제거.
--   · dedup 키 = sha1(원본 URL — 쿼리 제거). 리테일러 이미지 URL 은 CDN 영구
--     에셋 식별자라 배치 간 재사용률 99.1% 실측 (20260706 vs 20260707_02).
--   · 이미지 실체(blob)는 저장하지 않는다 — 판정에 필요한 건 메타 3종
--     (bytes/치수/ocr_text)뿐. 증빙 필요 시 url 로 재다운로드.
--   · 캐시 미스/DB 불가 시 파이프라인은 현행 그대로 동작 (안전 폴백).
--
-- 적용: docker exec -i lge-hs-clinic-monitoring-mysql-1 sh -c \
--        'mysql -uroot -p$MYSQL_ROOT_PASSWORD lg_clinic' < migrations/016_image_asset_cache.sql

CREATE TABLE IF NOT EXISTS image_asset (
  url_sha      CHAR(40)     NOT NULL COMMENT 'sha1(정규화 URL) — dedup 키',
  url          TEXT         NOT NULL COMMENT '원본 URL (쿼리 제거)',
  bytes        INT UNSIGNED NULL     COMMENT '파일 용량 (다운로드 실측)',
  width        INT UNSIGNED NULL,
  height       INT UNSIGNED NULL,
  ocr_text     MEDIUMTEXT   NULL     COMMENT '이미지 內 텍스트 (RapidOCR)',
  ocr_done     TINYINT(1)   NOT NULL DEFAULT 0 COMMENT 'OCR 수행 여부 — 0이면 do_ocr 요청 시 재처리',
  content_sha  CHAR(40)     NULL     COMMENT 'sha1(파일 내용) — URL 동일·내용 변경 감지용',
  first_batch  VARCHAR(20)  NULL,
  last_batch   VARCHAR(20)  NULL,
  last_seen_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (url_sha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='이미지 메타 영구 캐시 (blob 미저장)';

CREATE TABLE IF NOT EXISTS image_asset_link (
  product_id  VARCHAR(128) NOT NULL,
  url_sha     CHAR(40)     NOT NULL,
  rtlr_name   VARCHAR(64)  NOT NULL,
  batch_id    VARCHAR(20)  NOT NULL COMMENT '최초 관측 배치',
  PRIMARY KEY (product_id, url_sha),
  KEY idx_sha (url_sha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='제품 ↔ 이미지 매핑 (조회 축)';
