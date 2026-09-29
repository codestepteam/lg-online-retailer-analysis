-- LG HS Clinic Monitoring — DB 스키마
-- MySQL 8.0+
-- docker-entrypoint-initdb.d 에서 01_init.sql 다음에 자동 실행됨

USE lg_clinic;

-- ── pdp_target_list ───────────────────────────────────────────────────────────
-- 사용자가 업로드한 PDP URL 리스트. batch_id 단위로 격리.
--
-- batch_id 정책:
--   · 사용자가 report_date('2026-06-30') 를 입력 → 시스템이 batch_id('20260630') 발급
--   · 같은 날 재업로드 → '20260630_02', '20260630_03' ... (버전 자동 증가)
--   · batch_id 는 디렉토리명·CLI 인자·결과 테이블 키와 동일한 문자열
CREATE TABLE IF NOT EXISTS pdp_target_list (
    target_id   BIGINT       NOT NULL AUTO_INCREMENT,
    batch_id    VARCHAR(20)  NOT NULL,               -- '20260630' / '20260630_02'
    report_date DATE         NOT NULL,               -- 사용자 입력 원본 ('2026-06-30')
    instance    VARCHAR(8)   NOT NULL,               -- 국가코드: SE / FR / IT / PL
    category1   VARCHAR(16)  NOT NULL,               -- 단축 카테고리: DW / WM / REF
    category2   VARCHAR(64)  NOT NULL,               -- 풀 카테고리: DISHWASHER / WASHING MACHINE
    brand       VARCHAR(64)  NOT NULL,               -- LG / Samsung / Bosch ...
    model_mpc   VARCHAR(64)      NULL,               -- 모델명 (ID31 대조 — 구 테이블 이관/업로드 시 선택)
    retailer    VARCHAR(64)  NOT NULL,               -- URL 도메인 → 내부 키 변환 (업로드 시 파생)
    product_id  VARCHAR(128)     NULL,               -- URL에서 추출한 상품 ID (저장 경로 키)
    url         TEXT         NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (target_id),
    UNIQUE KEY uq_url    (batch_id, instance, url(512)),
    INDEX idx_batch      (batch_id),
    INDEX idx_filter     (batch_id, instance, retailer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── plp_target_list ───────────────────────────────────────────────────────────
-- 사용자가 업로드한 PLP(카테고리 목록) URL 리스트. batch_id 단위로 격리.
CREATE TABLE IF NOT EXISTS plp_target_list (
    target_id   BIGINT       NOT NULL AUTO_INCREMENT,
    batch_id    VARCHAR(20)  NOT NULL,
    report_date DATE         NOT NULL,
    instance    VARCHAR(8)   NOT NULL,
    category1   VARCHAR(16)  NOT NULL,
    category2   VARCHAR(64)  NOT NULL,
    brand       VARCHAR(64)  NOT NULL,
    retailer    VARCHAR(64)  NOT NULL,
    hs_category VARCHAR(64)  NOT NULL,               -- HS 카테고리 키 (예: washing_machine)
    url         TEXT         NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (target_id),
    UNIQUE KEY uq_plp    (batch_id, instance, retailer, hs_category),
    INDEX idx_batch      (batch_id),
    INDEX idx_filter     (batch_id, instance, retailer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── home_target_list ──────────────────────────────────────────────────────────
-- home 트랙 마스터 (배치 무관, 고정 설정).
--   · retailer × instance 당 1 행 = 홈 URL + 검색 URL 템플릿 + 운영 메모
--   · search_url_template: {q} placeholder 포함. NULL 이면 검색 미방출 (차단/미제공).
--   · home_keywords 와 조인해 검색 URL 조립 (template.replace('{q}', quote_plus(keyword))).
-- (mig 008 에서 통합 — 이전엔 home_target_list(batch-scoped) + home_search_config 로 분리.)
CREATE TABLE IF NOT EXISTS home_target_list (
    id                  INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    retailer            VARCHAR(64)   NOT NULL COMMENT '내부 리테일러 키 (예: Coolblue)',
    cntry_cd          CHAR(2)       NOT NULL COMMENT '국가 코드 대문자 (예: NL) — pdp_target_list.cntry_cd 와 통일',
    home_url            VARCHAR(2048) NOT NULL COMMENT '홈페이지 URL',
    search_url_template VARCHAR(2048)     NULL COMMENT '{q} placeholder 포함 검색 URL. NULL 이면 검색 미방출.',
    notes               VARCHAR(255)      NULL COMMENT '메모 — NULL 이유 / 렌더 대기 / SB 정책 등 특이사항',
    created_at          TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_home (retailer, cntry_cd)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── home_keywords ─────────────────────────────────────────────────────────────
-- 리테일러별 검색 키워드 마스터 (mig 012 — 배치 무관).
-- home 트랙: home_target_list × home_keywords 조인으로 검색 URL 조립. 실행 시점
-- 마스터 스냅샷을 그대로 사용하며 결과물은 data/{batch_id}/home/ 로 남음.
CREATE TABLE IF NOT EXISTS home_keywords (
    id                 INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    retailer           VARCHAR(64)   NOT NULL,
    cntry_cd         CHAR(2)       NOT NULL COMMENT '국가 코드 대문자 (예: NL)',
    loc_srch_kywd_info VARCHAR(255)  NOT NULL COMMENT '실제 검색어 (로컬)',
    eng_srch_kywd_info VARCHAR(255)      NULL COMMENT '라벨/폴백 (영문)',
    srch_kywd_cat_name VARCHAR(64)       NULL COMMENT '리포트 그룹핑 라벨',
    kywd_type          ENUM('home','category') NOT NULL DEFAULT 'category'
        COMMENT 'home=home 트랙 검색 kw (ID1/2/4/11), category=GNB 카테고리 kw (ID3)',

    PRIMARY KEY (id),
    UNIQUE KEY uq_keyword (retailer, cntry_cd, loc_srch_kywd_info, kywd_type),
    INDEX      idx_filter (cntry_cd, retailer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
