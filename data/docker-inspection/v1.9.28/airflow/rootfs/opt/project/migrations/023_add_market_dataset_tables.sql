-- Migration 023: 시장 원본 데이터셋 3종 테이블 추가
--
-- 배경
--   외부에서 배포되는 원본 데이터셋(dataset/*.xlsx)을 그대로 DB 에 적재해
--   조회·후속 분석의 소스로 삼는다. 파일명 = 테이블명, 컬럼 = 데이터셋 컬럼 그대로.
--   (엑셀 파싱 아티팩트인 무명 컬럼 `Unnamed: N` 은 스키마에서 제외.)
--
--   · VSMRKT_DAILY_OSM_BANR_VSBLT_D — 일자별 배너/노출 순위 원장
--   · VSMRKT_DAILY_OSM_SALE_RK_D    — 일자별 판매·재고·미디어 카운트 원장
--   · TSPURC_LIST_FULL_SUMM_S       — 전사 요약 집계 (배너/검색/리뷰/평점)
--
--   관리: /datasets/{table} 업로드로 **전체 교체**(TRUNCATE 후 재삽입 — 마스터, batch 무관).
--   타입은 데이터셋 실측(값 범위·최대 길이) 기준. 문자열 컬럼은 미샘플 구간
--   대비 넉넉히, 집계 수치는 정수·소수 혼재를 흡수하도록 DECIMAL 로 둔다.
--
-- 실행: mysql -u <user> -p <db> < migrations/020_add_market_dataset_tables.sql

-- ── VSMRKT_DAILY_OSM_BANR_VSBLT_D ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS VSMRKT_DAILY_OSM_BANR_VSBLT_D (
    RPT_DATE        DATE          NULL COMMENT '리포트 기준일',
    CNTRY           VARCHAR(32)   NULL COMMENT '국가명 (Spain/Italy/...)',
    RTLR_NAME       VARCHAR(64)   NULL COMMENT '리테일러 표기명',
    BRAND           VARCHAR(64)   NULL COMMENT '브랜드',
    `DIV`           VARCHAR(16)   NULL COMMENT '제품군 (REF/W/M/D/W)',
    RPC             VARCHAR(64)   NULL COMMENT '리테일러 상품 코드',
    MPC             VARCHAR(128)  NULL COMMENT '모델 코드',
    CAT_URL_ADDR    VARCHAR(512)  NULL COMMENT '상품/카테고리 URL',
    PRODUCT_DESC    VARCHAR(1024) NULL COMMENT '상품 설명',
    PRODUCT_IMG_URL VARCHAR(512)  NULL COMMENT '대표 이미지 URL',
    PRICE           VARCHAR(64)   NULL COMMENT '가격(원문)',
    DC_PRICE        VARCHAR(64)   NULL COMMENT '할인가(원문)',
    CURRENCY        VARCHAR(64)   NULL COMMENT '통화(원문)',
    CAT             VARCHAR(255)  NULL COMMENT '카테고리',
    RK              VARCHAR(64)   NULL COMMENT '순위(원문)'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
  COMMENT='시장 원본: 일자별 배너/노출 순위 (dataset/VSMRKT_DAILY_OSM_BANR_VSBLT_D.xlsx)';

-- ── VSMRKT_DAILY_OSM_SALE_RK_D ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS VSMRKT_DAILY_OSM_SALE_RK_D (
    RPT_DATE         DATE          NULL COMMENT '리포트 기준일',
    CNTRY            VARCHAR(32)   NULL COMMENT '국가명',
    RTLR_NAME        VARCHAR(64)   NULL COMMENT '리테일러 표기명',
    BRAND            VARCHAR(64)   NULL COMMENT '브랜드',
    `DIV`            VARCHAR(16)   NULL COMMENT '제품군',
    RPC              VARCHAR(64)   NULL COMMENT '리테일러 상품 코드',
    MPC              VARCHAR(128)  NULL COMMENT '모델 코드',
    CAT_URL_ADDR     VARCHAR(512)  NULL COMMENT '상품 URL',
    PRODUCT_DESC     TEXT          NULL COMMENT '상품 설명(최대 수천자)',
    AVLBL_STAT       VARCHAR(32)   NULL COMMENT '재고 상태',
    OBSRV_LIST_PRICE VARCHAR(32)   NULL COMMENT '관측 정가(원문)',
    OBSRV_DC_PRICE   VARCHAR(32)   NULL COMMENT '관측 할인가(원문)',
    CURRENCY_CODE    VARCHAR(32)   NULL COMMENT '통화 코드',
    RK               VARCHAR(32)   NULL COMMENT '순위(원문)',
    CAT              VARCHAR(32)   NULL COMMENT '카테고리',
    IMG_COUNT        VARCHAR(32)   NULL COMMENT '이미지 수(원문)',
    VIDEO_COUNT      DECIMAL(18,4) NULL COMMENT '영상 수',
    SALE_AMT         DECIMAL(18,4) NULL COMMENT '판매 금액',
    SALE_QTY         DECIMAL(18,4) NULL COMMENT '판매 수량',
    SEARCH_TERM      VARCHAR(128)  NULL COMMENT '검색어'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
  COMMENT='시장 원본: 일자별 판매/재고/미디어 카운트 (dataset/VSMRKT_DAILY_OSM_SALE_RK_D.xlsx)';

-- ── TSPURC_LIST_FULL_SUMM_S ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS TSPURC_LIST_FULL_SUMM_S (
    `DATE`               DATE          NULL COMMENT '기준일',
    TOT_DIVS_CODE        VARCHAR(16)   NULL COMMENT '집계 구분 (Total 등)',
    CNTRY_CODE           VARCHAR(8)    NULL COMMENT '국가 코드',
    RTLR                 VARCHAR(64)   NULL COMMENT '리테일러',
    PRODUCT_CAT_NAME     VARCHAR(64)   NULL COMMENT '제품 카테고리명',
    BRAND_NAME           VARCHAR(128)  NULL COMMENT '브랜드명',
    CMPTR_YN             INT           NULL COMMENT '경쟁사 여부',
    BNNR_COUNT           DECIMAL(18,4) NULL COMMENT '배너 노출 수',
    SRCH_COUNT           DECIMAL(18,4) NULL COMMENT '검색 노출 수',
    MENU_COUNT           DECIMAL(18,4) NULL COMMENT '메뉴 노출 수',
    TOP_RK               DECIMAL(18,4) NULL COMMENT '최고 순위',
    AVG_RK               DECIMAL(18,4) NULL COMMENT '평균 순위',
    IMG_COUNT            DECIMAL(18,4) NULL COMMENT '평균 이미지 수',
    VIDEO_COUNT          DECIMAL(18,4) NULL COMMENT '평균 영상 수',
    REVIEW_COUNT         DECIMAL(18,4) NULL COMMENT '리뷰 수',
    AVG_SCORE            DECIMAL(18,4) NULL COMMENT '평균 평점',
    TOT_REVIEW_COUNT     DECIMAL(18,4) NULL COMMENT '총 리뷰 수',
    REVIEW_PRODUCT_COUNT DECIMAL(18,4) NULL COMMENT '리뷰 보유 상품 수',
    TOT_SCORE            DECIMAL(18,4) NULL COMMENT '총점',
    PARTN_CMPTR_YN       VARCHAR(64)   NULL COMMENT '파트너/경쟁사 구분(원문)',
    ETL_LOAD_DTTM        VARCHAR(64)   NULL COMMENT 'ETL 적재 시각(원문)',
    ETL_USR_ID           VARCHAR(64)   NULL COMMENT 'ETL 사용자 ID',
    ETL_PGM_ID           VARCHAR(64)   NULL COMMENT 'ETL 프로그램 ID'
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
  COMMENT='시장 원본: 전사 요약 집계 (dataset/TSPURC_LIST_FULL_SUMM_S.xlsx)';
