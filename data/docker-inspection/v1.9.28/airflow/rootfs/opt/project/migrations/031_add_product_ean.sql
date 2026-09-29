-- Migration 031: product_ean — 모델(mpc) → EAN 마스터
--
-- 배경 (2026-07-21, docs/handoff_id31_43.md 'flix 자동 캡처 조사')
--   flix delivery API(media.flixcar.com) 직접 조회에는 (distributor, EAN) 이 필요한데
--   DB 에 EAN 컬럼이 없었다. EAN 은 제품 전역 식별자(리테일러 무관)라 모델 단위 마스터로
--   둔다. 소스는 이미 수집된 리테일러 HTML(flix 로더 data-flix-ean / JSON-LD / 인라인
--   "Ean") — scripts/build_ean_map.py 가 추출·적재한다(append/upsert).
--   ID31/43 러너가 refdata.ean_for_model() 로 조회 → 캡처 실패 시 delivery 폴백
--   ('있는데 없다' 오검출 제거 — QA 메일 2026-07-21).
--
-- 실행: docker exec -i <mysql> mysql --default-character-set=utf8mb4 \
--         -u<user> -p<pw> lg_clinic < migrations/031_add_product_ean.sql

CREATE TABLE IF NOT EXISTS product_ean (
    model_mpc   VARCHAR(64)  NOT NULL,           -- 모델 코드 (mpc, 접미 .XXX 제거 대문자)
    ean         VARCHAR(14)  NOT NULL,           -- EAN-13 (12~14자리 숫자)
    source      VARCHAR(128) NULL,               -- 추출 근거 (retailer/batch 등)
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
                             ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (model_mpc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
