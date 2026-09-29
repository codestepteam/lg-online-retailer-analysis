-- 050 — 대시보드 마트 L1 개편 (2026-09-02 설계안)
--
-- 3테이블 체제로 통합한다 (daily/monthly 분리 폐지):
--     dash_visibility_daily + _monthly   →  l1_visibility
--     dash_conversion_daily + _monthly   →  l1_conversion   (평점·리뷰만)
--     dash_flixmedia_monthly             →  l1_flixmedia    (+ CNX 콘텐츠 지표 이관)
--
-- 확정 사항:
--  · 컬럼명은 설계 시트 표기(DATE/CNTRY_CODE/SITE_NAME/…)를 따른다 — OSM L1 과 같은 어휘.
--    ⚠️ `date`·`rank` 는 MySQL 예약어라 코드·쿼리에서 backtick 필수.
--  · CNX 전용 콘텐츠 지표(video_count·warranty·dimension)는 conversion → flixmedia 로 이관.
--    conversion 은 OSM 평점·리뷰 단일 성격이 된다.
--  · dimension_pdp → dimension_asset 로 개명 (설계 시트 DIMENSION_ASSET).
--  · flixmedia 결함 컬럼은 FM_ 접두 (error → fm_error, err_img → fm_err_img …).
--  · daily/monthly 를 한 테이블에 담아도 충돌하지 않는다 — 성격이 source 로 갈린다
--    (일간 스냅샷 cnx / 월간 확정 osm_bq). flixmedia 는 월간 전용이라 애초에 단일.
--  · batch_id 는 설계 시트에 없는 운영 키지만 유지한다 — 재적재 시 슬라이스 교체 단위.
--    (없으면 재적재가 중복 적재가 된다.)

-- ── 1. visibility ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS l1_visibility (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `date`       DATE         NOT NULL COMMENT '데이터 기준 일자',
    cntry_code   VARCHAR(4)   NOT NULL COMMENT '국가 코드',
    site_name    VARCHAR(64)  NOT NULL COMMENT '리테일러 (국가 접미 없음)',
    brand_name   VARCHAR(64)  DEFAULT NULL COMMENT '브랜드 (대문자 정규화)',
    brand_type   VARCHAR(16)  DEFAULT NULL COMMENT 'LG | COMPETITOR | OTHERS',
    product      VARCHAR(32)  DEFAULT NULL COMMENT '제품군 (WM/REF/DW)',
    product_name VARCHAR(512) DEFAULT NULL COMMENT '제품명',
    mpc          VARCHAR(64)  DEFAULT NULL COMMENT '모델코드 (OSM 전용)',
    page         ENUM('SRCH','GNB') NOT NULL COMMENT 'SRCH=검색 / GNB=메뉴',
    srch_kwd     VARCHAR(255) DEFAULT NULL COMMENT '검색어 (page=SRCH)',
    `rank`       INT          NOT NULL COMMENT '노출 순위',
    url          VARCHAR(1024) DEFAULT NULL,
    source       VARCHAR(16)  NOT NULL DEFAULT 'cnx' COMMENT 'cnx | osm_bq',
    batch_id     VARCHAR(32)  NOT NULL COMMENT '운영 키 — 재적재 슬라이스 단위',
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_vis_date (`date`),
    KEY idx_vis_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  COMMENT='L1 노출 — 검색·메뉴 순위 (구 dash_visibility_*)';

INSERT INTO l1_visibility
    (`date`, cntry_code, site_name, brand_name, brand_type, product, product_name,
     mpc, page, srch_kwd, `rank`, url, source, batch_id, created_at)
SELECT base_date, cntry_cd, rtlr_name, brand, brand_type, cat_cd, product_name,
       mpc, page, srch_kywd, rnk, url, source, batch_id, created_at
FROM dash_visibility_daily;

-- ── 2. conversion (평점·리뷰) ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS l1_conversion (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `date`       DATE         NOT NULL COMMENT '데이터 기준 일자',
    cntry_code   VARCHAR(4)   NOT NULL,
    site_name    VARCHAR(64)  NOT NULL,
    brand_name   VARCHAR(64)  DEFAULT NULL,
    product      VARCHAR(32)  DEFAULT NULL COMMENT '제품군 (WM/REF/DW)',
    product_name VARCHAR(512) DEFAULT NULL,
    mpc          VARCHAR(64)  DEFAULT NULL,
    rating       DECIMAL(4,2) DEFAULT NULL COMMENT '평점 — 5점 환산',
    review_count INT          DEFAULT NULL,
    url          VARCHAR(1024) DEFAULT NULL,
    source       VARCHAR(16)  NOT NULL DEFAULT 'cnx'
                 COMMENT 'cnx=일간 스냅샷 / osm_bq=월간 확정',
    batch_id     VARCHAR(32)  NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_conv_date (`date`),
    KEY idx_conv_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  COMMENT='L1 전환 — 평점·리뷰 (구 dash_conversion_*, 콘텐츠 지표는 l1_flixmedia 로 이관)';

INSERT INTO l1_conversion
    (`date`, cntry_code, site_name, brand_name, product, product_name, mpc,
     rating, review_count, url, source, batch_id, created_at)
SELECT base_date, cntry_cd, rtlr_name, brand, cat_cd, product_name, mpc,
       rating, review_count, url, source, batch_id, created_at
FROM dash_conversion_daily;

-- ── 3. flixmedia (CNX 콘텐츠 진단) ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS l1_flixmedia (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `date`          DATE         NOT NULL COMMENT '데이터 기준 일자',
    cntry_code      VARCHAR(4)   NOT NULL,
    site_name       VARCHAR(64)  NOT NULL,
    brand_name      VARCHAR(64)  DEFAULT NULL,
    product         VARCHAR(32)  DEFAULT NULL COMMENT '제품군 (WM/REF/DW)',
    product_name    VARCHAR(512) DEFAULT NULL,
    mpc             VARCHAR(64)  DEFAULT NULL COMMENT '운영 식별용 (설계 시트 외)',
    url             VARCHAR(1024) DEFAULT NULL COMMENT '운영 식별용 (설계 시트 외)',
    video_count     INT          DEFAULT NULL COMMENT 'ID34 — PDP 비디오 개수',
    warranty        TINYINT      DEFAULT NULL COMMENT 'ID39 — 보증 이미지 보유 1/0',
    dimension_asset TINYINT      DEFAULT NULL COMMENT 'ID46 — 본문(PDP) 치수 이미지 1/0',
    dimension_gal   TINYINT      DEFAULT NULL COMMENT 'ID40 — 갤러리 치수 이미지 1/0',
    flixmedia       TINYINT      DEFAULT NULL COMMENT 'ID42 — 연동 정상 1 / 결함 0 / 대상 아님 NULL',
    fm_error        TINYINT      DEFAULT NULL COMMENT 'ID43 — 콘텐츠 결함 존재 1/0',
    fm_err_img      INT          DEFAULT NULL COMMENT '이미지 결함 개수',
    fm_err_video    INT          DEFAULT NULL COMMENT '비디오 결함 개수',
    fm_err_text     INT          DEFAULT NULL COMMENT '텍스트 결함 개수',
    fm_err_etc      INT          DEFAULT NULL COMMENT '기타 결함 개수',
    fm_cause        VARCHAR(255) DEFAULT NULL COMMENT '판정 사유 / 대표 결함 유형',
    source          VARCHAR(16)  NOT NULL DEFAULT 'cnx',
    batch_id        VARCHAR(32)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_flix_date (`date`),
    KEY idx_flix_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  COMMENT='L1 콘텐츠 진단 — 영상·보증·치수 + Flixmedia (월간)';

-- 구 flixmedia 데이터가 있으면 이관 (컬럼 개명 반영, 콘텐츠 지표는 NULL 로 시작)
INSERT INTO l1_flixmedia
    (`date`, cntry_code, site_name, brand_name, product, product_name, mpc, url,
     flixmedia, fm_error, fm_err_img, fm_err_video, fm_err_text, fm_err_etc,
     fm_cause, source, batch_id, created_at)
SELECT base_date, cntry_cd, rtlr_name, brand, cat_cd, product_name, mpc, url,
       flixmedia, error, err_img, err_video, err_text, err_etc,
       cause, source, batch_id, created_at
FROM dash_flixmedia_monthly;

-- ── 4. 구 테이블 정리 (데이터 이관 후) ───────────────────────────────────────
DROP TABLE IF EXISTS dash_visibility_monthly;
DROP TABLE IF EXISTS dash_conversion_monthly;
DROP TABLE IF EXISTS dash_flixmedia_monthly;
DROP TABLE IF EXISTS dash_visibility_daily;
DROP TABLE IF EXISTS dash_conversion_daily;
