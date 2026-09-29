-- Migration 024: 국가·카테고리별 취급 브랜드 마스터 (brand_track_list)
--
-- 배경
--   home 검색 리포트(ID1/ID2)가 통일 12컬럼 unpivot 양식으로 바뀌면서 Brand 컬럼을
--   제품별 판별값으로 채운다 (2026-07-14 사용자 확정). 그 판별 사전이 이 테이블 —
--   (국가, 카테고리)별 고객사 취급 브랜드 목록이며, 목록 외/판별 불가는 OTHERS.
--   brand_rank 는 고객사 원표의 1~5 순번(취급 우선순위) 보존용.
--
--   · CZ(체코)는 원표가 '추가 확인 필요' 상태라 미시딩 — 확정되면 행 추가.
--   · (국가, 카테고리) 조합이 미등재면 리포트는 LG 만 판별 + 나머지 OTHERS
--     (전체 사전을 조용히 적용하지 않음 — 기준 미등록을 가시화).
--   · 조회는 core/refdata.brand_track_map(), 판별은 core/brand_match.detect().
--
-- 실행: mysql -u <user> -p <db> < migrations/021_add_brand_track_list.sql

CREATE TABLE IF NOT EXISTS brand_track_list (
    cntry_cd   VARCHAR(4)  NOT NULL COMMENT '국가 코드 (ES/FR/IT/NL/SE/PL/CZ)',
    cat_cd     VARCHAR(8)  NOT NULL COMMENT '카테고리 코드 (WM/REF/DW)',
    brand_name VARCHAR(32) NOT NULL COMMENT '브랜드 표기 (대문자 = 리포트 노출값)',
    brand_rank TINYINT     NULL     COMMENT '취급 우선순위 (고객사 표 1~5)',
    PRIMARY KEY (cntry_cd, cat_cd, brand_name)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
  COMMENT='국가·카테고리별 취급 브랜드 (ID1/ID2 Brand 판별 사전 — 목록 외 = OTHERS)';

-- 시딩: 고객사 취급 브랜드 표 (2026-07-14 수령분)
INSERT INTO brand_track_list (cntry_cd, cat_cd, brand_name, brand_rank) VALUES
-- W/M
('ES','WM','LG',1),('ES','WM','BOSCH',2),('ES','WM','SAMSUNG',3),('ES','WM','HISENSE',4),
('FR','WM','BOSCH',1),('FR','WM','SAMSUNG',2),('FR','WM','LG',3),('FR','WM','HISENSE',4),
('IT','WM','LG',1),('IT','WM','SAMSUNG',2),('IT','WM','BOSCH',3),('IT','WM','HISENSE',4),('IT','WM','HAIER',5),
('NL','WM','SAMSUNG',1),('NL','WM','BOSCH',2),('NL','WM','AEG',3),('NL','WM','LG',4),
('SE','WM','BOSCH',1),('SE','WM','ELECTROLUX',2),('SE','WM','LG',3),('SE','WM','SAMSUNG',4),
('PL','WM','ELECTROLUX',1),('PL','WM','SAMSUNG',2),('PL','WM','BOSCH',3),('PL','WM','LG',4),('PL','WM','HISENSE',5),
-- REF (Cooling)
('ES','REF','LG',1),('ES','REF','SAMSUNG',2),('ES','REF','HISENSE',3),('ES','REF','BOSCH',4),
('FR','REF','SAMSUNG',1),('FR','REF','HISENSE',2),('FR','REF','LG',3),('FR','REF','HAIER',4),
('IT','REF','SAMSUNG',1),('IT','REF','HISENSE',2),('IT','REF','LG',3),('IT','REF','BOSCH',4),('IT','REF','HAIER',5),
('NL','REF','SAMSUNG',1),('NL','REF','BOSCH',2),('NL','REF','ETNA',3),('NL','REF','LG',4),
('SE','REF','SAMSUNG',1),('SE','REF','ELECTROLUX',2),('SE','REF','LG',3),('SE','REF','BOSCH',4),('SE','REF','HISENSE',5),
('PL','REF','SAMSUNG',1),('PL','REF','LG',2),('PL','REF','HISENSE',3),('PL','REF','BOSCH',4),('PL','REF','HAIER',5),
-- D/W (ES 전용 — DW 카테고리 자체가 ES 전용 트랙)
('ES','DW','LG',1),('ES','DW','BOSCH',2),('ES','DW','BALAY',3),('ES','DW','BEKO',4),('ES','DW','HISENSE',5)
ON DUPLICATE KEY UPDATE brand_rank = VALUES(brand_rank);
