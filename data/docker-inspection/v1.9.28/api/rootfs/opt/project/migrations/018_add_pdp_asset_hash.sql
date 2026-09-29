-- Migration 018: pdp_asset_hash 테이블 추가
--
-- 배경
--   ID31(공식 에셋 일치도) 을 dHash 기반 비주얼 비교로 보강하기 위해서는
--   LG.com 공식 이미지(pdp_20260622.img_src/gallery_src) 의 dHash/용량을
--   비교 기준으로 삼아야 한다. eval.py 는 순수 계산 단계(3-Phase 규약)라
--   매 리포트 실행마다 LG.com 에 네트워크 요청을 보낼 수 없으므로, 백필한
--   결과를 이 테이블에 캐시해두고 refdata.py 는 DB 조회만 한다.
--
--   백필은 make_report.py 가 배치 실행 전, 그 배치에 등장하는 모델의 URL만
--   골라 없는 것만 채운다 (core/image_match.py 의 백필 헬퍼). 즉 이 테이블은
--   전체 13,031행(136,231 URL)을 한 번에 채우지 않고 실제 조회된 URL만
--   누적된다.
--
-- 실행: mysql -u <user> -p <db> < migrations/018_add_pdp_asset_hash.sql

CREATE TABLE IF NOT EXISTS pdp_asset_hash (
    id         BIGINT NOT NULL AUTO_INCREMENT,
    url        VARCHAR(512) NOT NULL COMMENT 'LG.com 공식 이미지 절대 URL',
    dhash      BIGINT UNSIGNED NULL COMMENT '64-bit dHash — 다운로드/디코딩 실패 시 NULL',
    bytes      INT UNSIGNED NULL COMMENT '원본 파일 용량 (저용량 의심 판정용)',
    fetched_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_url (url(512))
) COMMENT='LG.com 공식 에셋 URL별 dHash/용량 캐시 (ID31 dHash 비교 — core/image_match.py 백필)';
