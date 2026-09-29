-- Migration 002: target_list 테이블 — 공용 clinic DB 반영 (merge_develop_phase1.md §8, A안)
-- 실행: mysql -u {user} -p {db} < migrations/002_add_target_list.sql
--
-- ⚠️ DDL 만 단독 실행하지 말 것 — 테이블이 생기는 순간 crawl.py 의
--    구 retailer_product_targets 폴백(1146 기반)이 비활성화되므로,
--    반드시 백필까지 한 번에 수행하는 migrations/migrate_002_target_list.py 를 쓸 것.
--    (이 파일은 DDL 원본 문서용. 스크립트가 동일 DDL 을 내장 실행한다.)
--
-- schema.sql 과 동일 정의 + model_mpc 컬럼 (구 테이블 이관 시 ID31 모델 대조 유실 방지)

CREATE TABLE IF NOT EXISTS target_list (
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

    -- 같은 batch 안에서 동일 URL 중복 방지 (url은 TEXT라 앞 512자로 인덱스)
    UNIQUE KEY uq_url    (batch_id, instance, url(512)),

    -- 부분 재실행 필터용 (batch_id + instance 또는 retailer 로 WHERE)
    INDEX idx_batch      (batch_id),
    INDEX idx_filter     (batch_id, instance, retailer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
