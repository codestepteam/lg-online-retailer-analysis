-- Migration 001: PLP / HOME 설정 테이블 추가
-- 실행: mysql -u {user} -p {db} < migrations/001_add_plp_home_tables.sql

-- ── plp_config ────────────────────────────────────────────────────────────────
-- 리테일러별 HS 카테고리 PLP URL 설정 (고정값, 배치와 무관)
-- 행 수 = 리테일러 × HS카테고리
CREATE TABLE IF NOT EXISTS plp_config (
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    retailer    VARCHAR(64)     NOT NULL COMMENT '내부 리테일러 키 (예: Coolblue)',
    instance    CHAR(2)         NOT NULL COMMENT '국가 코드 대문자 (예: NL)',
    url         VARCHAR(2048)   NOT NULL COMMENT 'PLP 카테고리 URL',
    hs_category VARCHAR(64)     NOT NULL COMMENT 'HS 카테고리 키 (예: washing_machine)',
    PRIMARY KEY (id),
    UNIQUE KEY uq_plp (retailer, instance, hs_category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── home_config ───────────────────────────────────────────────────────────────
-- 리테일러별 홈 URL 설정 (고정값, 배치와 무관)
-- 행 수 = 리테일러 수
CREATE TABLE IF NOT EXISTS home_config (
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    retailer    VARCHAR(64)     NOT NULL COMMENT '내부 리테일러 키 (예: Coolblue)',
    instance    CHAR(2)         NOT NULL COMMENT '국가 코드 대문자 (예: NL)',
    url         VARCHAR(2048)   NOT NULL COMMENT '홈 페이지 URL (검색 API 엔드포인트 포함)',
    PRIMARY KEY (id),
    UNIQUE KEY uq_home (retailer, instance)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── home_keywords ─────────────────────────────────────────────────────────────
-- home_config와 1:N — 리테일러별 검색 키워드 목록
CREATE TABLE IF NOT EXISTS home_keywords (
    id          INT UNSIGNED    NOT NULL AUTO_INCREMENT,
    retailer    VARCHAR(64)     NOT NULL,
    instance    CHAR(2)         NOT NULL,
    keyword     VARCHAR(255)    NOT NULL COMMENT '검색 키워드 (예: LG, 세탁기)',
    PRIMARY KEY (id),
    UNIQUE KEY uq_keyword (retailer, instance, keyword),
    CONSTRAINT fk_home_keywords
        FOREIGN KEY (retailer, instance)
        REFERENCES home_config (retailer, instance)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
