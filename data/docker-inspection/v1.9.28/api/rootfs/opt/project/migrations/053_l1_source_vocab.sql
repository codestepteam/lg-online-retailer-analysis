-- 053 — L1 SOURCE 어휘 통일: osm_bq → osm (2026-09-03 사용자 확정)
--
-- OSM 이 넘기는 L1 엑셀은 SOURCE='osm' 으로 온다. 적재기가 쓰던 'osm_bq' 를
-- 그대로 두면 같은 소스가 테이블 안에서 두 이름을 갖는다 — 대시보드가
-- `source='osm'` 으로 거르면 BQ 합성분이 통째로 빠진다.
--
-- 입력 쪽 식별자(파서 collector, bq_override 의 'osm_bq')는 그대로다.
-- 여기서 바꾸는 건 **적재 방출값**뿐.
--
-- devtools 는 OSM 미가동이라 0행일 수 있다(정상). GCP 에서 유효.

UPDATE l1_visibility SET source = 'osm' WHERE source = 'osm_bq';
UPDATE l1_conversion SET source = 'osm' WHERE source = 'osm_bq';
UPDATE l1_flixmedia  SET source = 'osm' WHERE source = 'osm_bq';

ALTER TABLE l1_visibility MODIFY COLUMN source VARCHAR(16) NOT NULL DEFAULT 'cnx'
      COMMENT '데이터 출처 — osm=OSM 유래 / cnx=자체 크롤';
ALTER TABLE l1_conversion MODIFY COLUMN source VARCHAR(16) NOT NULL DEFAULT 'cnx'
      COMMENT '데이터 출처 — osm=OSM 유래(월간 확정) / cnx=자체 크롤(일간 스냅샷)';
ALTER TABLE l1_flixmedia  MODIFY COLUMN source VARCHAR(16) NOT NULL DEFAULT 'cnx'
      COMMENT '데이터 출처 — osm=OSM 유래 / cnx=자체 크롤';
