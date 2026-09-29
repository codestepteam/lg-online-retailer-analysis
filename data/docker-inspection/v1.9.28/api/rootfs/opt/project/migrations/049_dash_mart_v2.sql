-- 049 — 대시보드 마트 설계 v1.0(2) 반영 (2026-09-02 EY 설계안)
--
-- 설계 시트 '마트설계' 3블록(visibility·conversion·flixmedia)에 컬럼을 맞춘다.
-- l2_* 4종은 대시보드 집계층이라 대상 외(사용자 확정 0902).
--
-- 확정 사항(사용자 0902):
--   · PRODUCT 는 현행 코드값(cat_cd: WM/REF/DW) 유지 — 스펙 샘플의 OSM 원문
--     ('WASHING MACHINE') 표기로 바꾸지 않는다.
--   · BRAND_TYPE 은 LG / COMPETITOR / OTHERS 3값 — 자사는 'LG'.
--   · menu_path·is_sponsored·in_stock·rating_scale 은 스펙에 없는 자체 컬럼이라 제거.
--     in_stock 은 컬럼 대신 **적재 필터**로 적용(설계 '데이터기준' INV_STAT_INFO='IN STOCK').
--     rating_scale 제거에 맞춰 rating 은 **5점 환산**으로 적재한다(지표 산출식이
--     '평점 3.0 이상'으로 5점 만점 전제 — 10점제 리테일러는 /2).
--
-- 주기(설계 '지표' 시트): visibility·rating·review = Daily / video·warranty·
-- dimension·flixmedia = Monthly. 컬럼 스키마는 daily·monthly 동일(스펙 1벌)이고
-- daily 는 Monthly 전용 컬럼이 NULL 로 남는다.

-- ── visibility ────────────────────────────────────────────────────────────────
ALTER TABLE dash_visibility_daily
    ADD COLUMN brand_type VARCHAR(16) DEFAULT NULL
        COMMENT '브랜드 구분 — LG(자사) / COMPETITOR(취급 경쟁사) / OTHERS'
        AFTER brand,
    ADD COLUMN mpc VARCHAR(64) DEFAULT NULL
        COMMENT '모델코드 — OSM(MAPP_PRODUCT_MODEL_CODE) 전용, CNX 검색결과는 원천 부재라 NULL'
        AFTER product_name,
    DROP COLUMN is_sponsored,
    DROP COLUMN menu_path;

-- ── conversion ────────────────────────────────────────────────────────────────
ALTER TABLE dash_conversion_daily
    ADD COLUMN video_count INT DEFAULT NULL
        COMMENT 'ID34 — PDP 비디오 개수 (Monthly 지표, daily 는 NULL)',
    ADD COLUMN warranty TINYINT DEFAULT NULL
        COMMENT 'ID39 — Warranty 이미지 보유 1/0 (Monthly)',
    ADD COLUMN dimension_pdp TINYINT DEFAULT NULL
        COMMENT 'ID46 — 본문(PDP) Dimension 이미지 보유 1/0 (Monthly)',
    ADD COLUMN dimension_gal TINYINT DEFAULT NULL
        COMMENT 'ID40 — 갤러리 Dimension 이미지 보유 1/0 (Monthly)',
    DROP COLUMN rating_scale,
    DROP COLUMN in_stock;

-- ── monthly 3종 (부재분 신설) ─────────────────────────────────────────────────
-- daily 와 동일 스키마. monthly DAG(export_dash_raw --grain monthly)가 이 테이블을
-- 찾다가 1146 으로 실패해 왔다(0828 실측 — 테이블 자체가 없었음).
CREATE TABLE IF NOT EXISTS dash_visibility_monthly LIKE dash_visibility_daily;
CREATE TABLE IF NOT EXISTS dash_conversion_monthly LIKE dash_conversion_daily;

-- ── flixmedia (신규) ──────────────────────────────────────────────────────────
-- 소스: eval ID42(연동 정상 여부) + ID43(콘텐츠 결함 원장 7유형).
-- ERR_* 는 결함 유형을 설계 4축으로 접은 개수:
--   ERR_IMG   ← image_broken · image_missing · image_duplicate
--   ERR_VIDEO ← video_missing
--   ERR_TEXT  ← text_truncated · duplicate_text
--   ERR_ETC   ← carousel_overlap
CREATE TABLE IF NOT EXISTS dash_flixmedia_monthly (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
                 COMMENT 'surrogate PK — 업무 유니크 제약 없음 (전행 보존 원칙)',
    base_date    DATE         NOT NULL COMMENT '데이터 기준 일자',
    cntry_cd     VARCHAR(4)   NOT NULL COMMENT '국가 코드',
    rtlr_name    VARCHAR(64)  NOT NULL COMMENT '리테일러 순수명 (국가 접미 없음)',
    brand        VARCHAR(64)  DEFAULT NULL COMMENT '브랜드 (대문자 정규화)',
    cat_cd       VARCHAR(8)   DEFAULT NULL COMMENT '제품군 코드 (WM/REF/DW)',
    product_name VARCHAR(512) DEFAULT NULL COMMENT '제품명',
    mpc          VARCHAR(64)  DEFAULT NULL COMMENT '모델코드',
    url          VARCHAR(1024) DEFAULT NULL COMMENT 'PDP URL',
    flixmedia    TINYINT      DEFAULT NULL
                 COMMENT 'ID42 — Flixmedia 연동 정상 1 / 결함·미연동 0 / 대상 아님 NULL',
    error        TINYINT      DEFAULT NULL COMMENT 'ID43 — 콘텐츠 결함 존재 1/0',
    err_img      INT          DEFAULT NULL COMMENT '이미지 결함 개수',
    err_video    INT          DEFAULT NULL COMMENT '비디오 결함 개수',
    err_text     INT          DEFAULT NULL COMMENT '텍스트 결함 개수',
    err_etc      INT          DEFAULT NULL COMMENT '기타 결함 개수 (캐러셀 겹침 등)',
    cause        VARCHAR(255) DEFAULT NULL COMMENT '판정 사유 — 미평가 원인 또는 대표 결함 유형',
    source       VARCHAR(16)  NOT NULL DEFAULT 'cnx' COMMENT '수집 소스 (cnx|osm_bq)',
    batch_id     VARCHAR(32)  NOT NULL COMMENT '산출 배치 — 재적재 슬라이스 키',
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_flix_date (base_date),
    KEY idx_flix_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  COMMENT='Flixmedia 연동·렌더링 진단 (ID42/43) — 대시보드 마트 v1.0(2)';
