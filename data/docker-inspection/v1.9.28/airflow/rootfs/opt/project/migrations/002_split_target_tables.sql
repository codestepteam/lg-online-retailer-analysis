-- Migration 002: target_list → pdp_target_list 분리 + plp/home_target_list 신설
-- 실행: mysql -u {user} -p {db} < migrations/002_split_target_tables.sql

-- ── Step 1: target_list → pdp_target_list ─────────────────────────────────────
RENAME TABLE target_list TO pdp_target_list;

-- ── Step 2: plp_target_list (plp_config 대체) ────────────────────────────────
CREATE TABLE IF NOT EXISTS plp_target_list (
    target_id   BIGINT       NOT NULL AUTO_INCREMENT,
    batch_id    VARCHAR(20)  NOT NULL,
    report_date DATE         NOT NULL,
    instance    VARCHAR(8)   NOT NULL,
    category1   VARCHAR(16)  NOT NULL,
    category2   VARCHAR(64)  NOT NULL,
    brand       VARCHAR(64)  NOT NULL,
    retailer    VARCHAR(64)  NOT NULL,
    hs_category VARCHAR(64)  NOT NULL,
    url         TEXT         NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (target_id),
    UNIQUE KEY uq_plp    (batch_id, instance, retailer, hs_category),
    INDEX idx_batch      (batch_id),
    INDEX idx_filter     (batch_id, instance, retailer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Step 3: home_target_list (home_config 대체) ──────────────────────────────
CREATE TABLE IF NOT EXISTS home_target_list (
    target_id   BIGINT       NOT NULL AUTO_INCREMENT,
    batch_id    VARCHAR(20)  NOT NULL,
    report_date DATE         NOT NULL,
    instance    VARCHAR(8)   NOT NULL,
    retailer    VARCHAR(64)  NOT NULL,
    url         TEXT         NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (target_id),
    UNIQUE KEY uq_home   (batch_id, instance, retailer),
    INDEX idx_batch      (batch_id),
    INDEX idx_filter     (batch_id, instance, retailer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Step 4: home_keywords 신설 (home_config.home_keywords FK 제거 후 독립) ──
-- 기존 home_keywords 가 있으면 FK 제거 후 재생성
DROP TABLE IF EXISTS home_keywords;
CREATE TABLE home_keywords (
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    retailer    VARCHAR(64)     NOT NULL,
    instance    CHAR(2)         NOT NULL,
    keyword     VARCHAR(255)    NOT NULL,

    PRIMARY KEY (id),
    UNIQUE KEY uq_keyword (retailer, instance, keyword)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Step 5: 구 설정 테이블 제거 ──────────────────────────────────────────────
DROP TABLE IF EXISTS plp_config;
DROP TABLE IF EXISTS home_config;
