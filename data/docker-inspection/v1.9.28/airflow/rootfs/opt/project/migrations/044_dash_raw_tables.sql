-- Migration 044: 대시보드 마트 raw 테이블 4벌 — daily/monthly 분리 (2026-08-18)
--
-- 배경 (docs/osm_bq_dashboard_design.md §6)
--   대시보드 마트는 대시보드팀이 만들고, CNX 는 마트를 만들 수 있는 **raw 테이블**만
--   제공한다 (EYFMT 비연관 — 산출 경로 완전 분리). 사용자 확정 0818:
--   ① 반출은 MySQL 우선(BQ 는 추후) ② daily / monthly 는 별도 테이블.
--   daily  = Daily 분석 지표(ID1/3 가시성 + 평점 시계열) 축적
--   monthly= 월말 확정 스냅샷 + CNX 월간 콘텐츠 지표(video 등 — 월간 배치에만 존재)
--
-- 적재자: scripts/export_dash_raw.py 단일 경로 (parsed.json 스캔 — 소스 불문).
--   멱등: batch_id 슬라이스 DELETE 후 INSERT (재실행 안전).
-- 마트 규칙(top10 절단·중복 수기체크·재고/리퍼 제외)은 적용하지 않는다 —
--   전행 보존 + 플래그(in_stock/rn 등)로 마트가 스스로 거를 수 있게만 제공.
-- 0819: 테이블·컬럼 COMMENT 부여 (기존 설치본 소급은 mig 045 — 내용 동일 유지 필수).
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/044_dash_raw_tables.sql

-- 1) 가시성 daily — ID1(SRCH)/ID3(GNB, 메뉴 경로 별개) 랭킹 행
CREATE TABLE IF NOT EXISTS dash_visibility_daily (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
                 COMMENT 'surrogate PK — 업무 유니크 제약 없음 (전행 보존 원칙)',
    base_date    DATE         NOT NULL
                 COMMENT '데이터 기준 일자 — OSM 합성은 BQ 조회일(meta.osm_base_date, KST 어제), CNX 는 배치명 파생',
    cntry_cd     VARCHAR(4)   NOT NULL
                 COMMENT '국가 코드 (ES/FR/IT/NL/SE/PL/CZ)',
    rtlr_name    VARCHAR(64)  NOT NULL
                 COMMENT '리테일러 순수명 — 국가 접미 없음 (예: MediaMarkt, mig 013 규약)',
    page         ENUM('SRCH','GNB') NOT NULL
                 COMMENT 'SRCH=검색 가시성(ID1) / GNB=메뉴 가시성(ID3)',
    cat_cd       VARCHAR(8)   DEFAULT NULL
                 COMMENT '제품군 코드 (WM/REF/DW 등) — 미상 NULL',
    srch_kywd    VARCHAR(255) DEFAULT NULL
                 COMMENT '검색 키워드 — page=SRCH 전용 (GNB 는 NULL)',
    menu_path    VARCHAR(512) DEFAULT NULL
                 COMMENT '메뉴 경로 — page=GNB 전용 (OSM 메뉴 경로 / CNX 는 gnb 라벨)',
    rnk          INT          NOT NULL
                 COMMENT '노출 순위 (1부터)',
    brand        VARCHAR(64)  DEFAULT NULL
                 COMMENT '수집 브랜드 원문 — LG 여부 판정 전 텍스트 (판정은 마트/리포트 몫)',
    product_name VARCHAR(512) DEFAULT NULL
                 COMMENT '상품명 원문',
    url          VARCHAR(1024) DEFAULT NULL
                 COMMENT '상품 URL',
    is_sponsored TINYINT      DEFAULT NULL
                 COMMENT '광고 노출 여부 — OSM PRODUCT_SPN_YN (CNX 수집분은 NULL)',
    source       ENUM('osm_bq','cnx') NOT NULL
                 COMMENT '데이터 출처 — osm_bq=BQ 합성 / cnx=자체 크롤',
    batch_id     VARCHAR(20)  NOT NULL
                 COMMENT '적재 슬라이스 키 — daily 는 실행일 8자리. 같은 batch 재적재 시 DELETE 후 INSERT 교체',
    created_at   TIMESTAMP    NULL DEFAULT CURRENT_TIMESTAMP
                 COMMENT 'DB 적재 시각',
    KEY ix_dvd_main  (base_date, cntry_cd, rtlr_name, page),
    KEY ix_dvd_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='대시보드 raw · 가시성 daily — ID1 검색(SRCH)/ID3 메뉴(GNB) 상품 랭킹. 1행=상품 1개 노출. 하루 1개 batch_id 슬라이스 축적(멱등 교체). 마트 규칙 미적용 전행 보존. 라이터: scripts/export_dash_raw.py (parsed.json 스캔, EYFMT 비연관)';

-- 2) 가시성 monthly — 월말 확정 스냅샷 (스키마 동일, 적재 시점만 상이)
CREATE TABLE IF NOT EXISTS dash_visibility_monthly (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
                 COMMENT 'surrogate PK — 업무 유니크 제약 없음 (전행 보존 원칙)',
    base_date    DATE         NOT NULL
                 COMMENT '데이터 기준 일자 — OSM 합성은 BQ 조회일(월 마지막 일자), CNX 는 배치명 파생',
    cntry_cd     VARCHAR(4)   NOT NULL
                 COMMENT '국가 코드 (ES/FR/IT/NL/SE/PL/CZ)',
    rtlr_name    VARCHAR(64)  NOT NULL
                 COMMENT '리테일러 순수명 — 국가 접미 없음 (예: MediaMarkt, mig 013 규약)',
    page         ENUM('SRCH','GNB') NOT NULL
                 COMMENT 'SRCH=검색 가시성(ID1) / GNB=메뉴 가시성(ID3)',
    cat_cd       VARCHAR(8)   DEFAULT NULL
                 COMMENT '제품군 코드 (WM/REF/DW 등) — 미상 NULL',
    srch_kywd    VARCHAR(255) DEFAULT NULL
                 COMMENT '검색 키워드 — page=SRCH 전용 (GNB 는 NULL)',
    menu_path    VARCHAR(512) DEFAULT NULL
                 COMMENT '메뉴 경로 — page=GNB 전용 (OSM 메뉴 경로 / CNX 는 gnb 라벨)',
    rnk          INT          NOT NULL
                 COMMENT '노출 순위 (1부터)',
    brand        VARCHAR(64)  DEFAULT NULL
                 COMMENT '수집 브랜드 원문 — LG 여부 판정 전 텍스트 (판정은 마트/리포트 몫)',
    product_name VARCHAR(512) DEFAULT NULL
                 COMMENT '상품명 원문',
    url          VARCHAR(1024) DEFAULT NULL
                 COMMENT '상품 URL',
    is_sponsored TINYINT      DEFAULT NULL
                 COMMENT '광고 노출 여부 — OSM PRODUCT_SPN_YN (CNX 수집분은 NULL)',
    source       ENUM('osm_bq','cnx') NOT NULL
                 COMMENT '데이터 출처 — osm_bq=BQ 합성 / cnx=자체 크롤',
    batch_id     VARCHAR(20)  NOT NULL
                 COMMENT '적재 슬라이스 키 — 전월 풀배치 batch. 같은 batch 재적재 시 DELETE 후 INSERT 교체',
    created_at   TIMESTAMP    NULL DEFAULT CURRENT_TIMESTAMP
                 COMMENT 'DB 적재 시각',
    KEY ix_dvm_main  (base_date, cntry_cd, rtlr_name, page),
    KEY ix_dvm_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='대시보드 raw · 가시성 monthly — 월말 확정 스냅샷. 매월 1일 monthly_dash 가 전월 풀배치 1슬라이스 적재. 스키마·규약은 dash_visibility_daily 와 동일';

-- 3) 전환 daily — ID37/38 평점·리뷰 시계열 (마트 Conversion daily 축)
CREATE TABLE IF NOT EXISTS dash_conversion_daily (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
                 COMMENT 'surrogate PK — 업무 유니크 제약 없음 (전행 보존 원칙)',
    base_date    DATE         NOT NULL
                 COMMENT '데이터 기준 일자 — OSM 합성은 BQ 조회일(meta.osm_base_date, KST 어제), CNX 는 배치명 파생({base}_dMMDD → MMDD)',
    cntry_cd     VARCHAR(4)   NOT NULL
                 COMMENT '국가 코드 (ES/FR/IT/NL/SE/PL/CZ)',
    rtlr_name    VARCHAR(64)  NOT NULL
                 COMMENT '리테일러 순수명 — 국가 접미 없음 (예: MediaMarkt, mig 013 규약)',
    cat_cd       VARCHAR(8)   DEFAULT NULL
                 COMMENT '제품군 코드 (WM/REF/DW 등) — 미상 NULL',
    brand        VARCHAR(64)  DEFAULT NULL
                 COMMENT '브랜드/제조사 원문 (parsed brand, 없으면 manufacturer 폴백)',
    product_name VARCHAR(512) DEFAULT NULL
                 COMMENT '상품명 (parsed title)',
    url          VARCHAR(1024) DEFAULT NULL
                 COMMENT 'PDP URL',
    mpc          VARCHAR(64)  DEFAULT NULL
                 COMMENT 'LG 모델코드 (parsed mpc, 없으면 model 폴백) — OSM 조인 키 축',
    rating       DECIMAL(4,2) DEFAULT NULL
                 COMMENT '평점 평균 — 원 스케일 그대로 (rating_scale 로 해석)',
    rating_scale TINYINT      DEFAULT NULL
                 COMMENT '평점 만점 — OSM=5 고정 (0818 확정), CNX 는 리테일러별 5/10 혼재 (Coolblue 10점제)',
    review_count INT          DEFAULT NULL
                 COMMENT '리뷰 수',
    in_stock     TINYINT      DEFAULT NULL
                 COMMENT '재고 플래그 — availability code IN* 이면 1, 아니면 0, 미상 NULL (재고 제외 규칙은 마트 몫)',
    source       ENUM('osm_bq','cnx') NOT NULL
                 COMMENT '데이터 출처 — osm_bq=BQ 합성(daily 합성 레코드·monthly 사이드카) / cnx=자체 크롤',
    batch_id     VARCHAR(20)  NOT NULL
                 COMMENT '적재 슬라이스 키 — daily 는 {당월base}_dMMDD suffix. 같은 batch 재적재 시 DELETE 후 INSERT 교체',
    created_at   TIMESTAMP    NULL DEFAULT CURRENT_TIMESTAMP
                 COMMENT 'DB 적재 시각',
    KEY ix_dcd_main  (base_date, cntry_cd, rtlr_name),
    KEY ix_dcd_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='대시보드 raw · 전환 daily — ID37/38 평점·리뷰 시계열. 1행=PDP 제품 1개 스냅샷. 하루 1개 batch_id 슬라이스 축적(멱등 교체). 라이터: scripts/export_dash_raw.py (parsed.json 스캔, EYFMT 비연관)';

-- 4) 전환 monthly — 월말 스냅샷 + CNX 월간 콘텐츠 지표 (video/warranty/dimension)
CREATE TABLE IF NOT EXISTS dash_conversion_monthly (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
                 COMMENT 'surrogate PK — 업무 유니크 제약 없음 (전행 보존 원칙)',
    base_date    DATE         NOT NULL
                 COMMENT '데이터 기준 일자 — OSM 합성은 BQ 조회일(월 마지막 일자), CNX 는 배치명 파생',
    cntry_cd     VARCHAR(4)   NOT NULL
                 COMMENT '국가 코드 (ES/FR/IT/NL/SE/PL/CZ)',
    rtlr_name    VARCHAR(64)  NOT NULL
                 COMMENT '리테일러 순수명 — 국가 접미 없음 (예: MediaMarkt, mig 013 규약)',
    cat_cd       VARCHAR(8)   DEFAULT NULL
                 COMMENT '제품군 코드 (WM/REF/DW 등) — 미상 NULL',
    brand        VARCHAR(64)  DEFAULT NULL
                 COMMENT '브랜드/제조사 원문 (parsed brand, 없으면 manufacturer 폴백)',
    product_name VARCHAR(512) DEFAULT NULL
                 COMMENT '상품명 (parsed title)',
    url          VARCHAR(1024) DEFAULT NULL
                 COMMENT 'PDP URL',
    mpc          VARCHAR(64)  DEFAULT NULL
                 COMMENT 'LG 모델코드 (parsed mpc, 없으면 model 폴백) — OSM 조인 키 축',
    rating       DECIMAL(4,2) DEFAULT NULL
                 COMMENT '평점 평균 — 원 스케일 그대로 (rating_scale 로 해석)',
    rating_scale TINYINT      DEFAULT NULL
                 COMMENT '평점 만점 — OSM=5 고정 (0818 확정), CNX 는 리테일러별 5/10 혼재 (Coolblue 10점제)',
    review_count INT          DEFAULT NULL
                 COMMENT '리뷰 수',
    video_count  INT          DEFAULT NULL
                 COMMENT 'CNX 월간 콘텐츠 — 갤러리+본문 영상 개수 (ID34 축). 파서 video 키 부재 시 NULL',
    warranty_ok  TINYINT      DEFAULT NULL
                 COMMENT 'CNX 월간 — 보증 표기 유무 (ID40/46 축, v2 배선 예정 — 현재 NULL)',
    dimension_ok TINYINT      DEFAULT NULL
                 COMMENT 'CNX 월간 — 치수 표기 유무 (ID39 축, v2 배선 예정 — 현재 NULL)',
    in_stock     TINYINT      DEFAULT NULL
                 COMMENT '재고 플래그 — availability code IN* 이면 1, 아니면 0, 미상 NULL (재고 제외 규칙은 마트 몫)',
    source       ENUM('osm_bq','cnx') NOT NULL
                 COMMENT '데이터 출처 — osm_bq=BQ 합성(daily 합성 레코드·monthly 사이드카) / cnx=자체 크롤',
    batch_id     VARCHAR(20)  NOT NULL
                 COMMENT '적재 슬라이스 키 — 전월 풀배치 batch. 같은 batch 재적재 시 DELETE 후 INSERT 교체',
    created_at   TIMESTAMP    NULL DEFAULT CURRENT_TIMESTAMP
                 COMMENT 'DB 적재 시각',
    KEY ix_dcm_main  (base_date, cntry_cd, rtlr_name),
    KEY ix_dcm_batch (batch_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='대시보드 raw · 전환 monthly — 월말 확정 스냅샷 + CNX 월간 콘텐츠 지표(video 등 월간 배치에만 존재). 매월 1일 monthly_dash 가 전월 풀배치 1슬라이스 적재. 그 외 규약은 dash_conversion_daily 와 동일';
