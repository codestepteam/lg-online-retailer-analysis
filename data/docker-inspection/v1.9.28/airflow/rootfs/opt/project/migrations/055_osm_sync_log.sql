-- Migration 055: osm_sync_log 신설 — OSM visibility daily 동기 원장 (osm_daily_sync DAG)
--
-- 배경 (2026-09-14 컷오버 설계 합의)
--   OSM L1 세 테이블은 D-1 이 02:00 KST daily 시점에 없고(실측 D-2), 늦게 채워지거나
--   고쳐질 수 있다. 고정 지연(OSM_LAG_DAYS)으로 daily 배치에 OSM 을 끼워 넣으면 같은
--   OSM 일자가 두 배치에 실리거나(9/12 이중, 0914 실사고) 리포트가 cnx D + OSM D-2 로
--   섞인다. 그래서 OSM 은 cnx daily 와 **분리**해 일자 단위 원장으로 관리한다:
--   창(lookback) 안의 각 OSM 일자를 재조회 → 정규화 해시가 원장과 다르면(신규·정정)
--   {D}_osm 재합성 → {D}_all 통합 리포트 → l1_visibility osm 슬라이스 교체.
--   cnx 쪽 서명(cnx_sig)이 바뀌어도(재크롤·백필) 통합 리포트를 다시 만든다.
--
-- 키 = OSM BASE_DATE. 재적재는 같은 행을 갱신(sync_count 증가). 실패는 hash 를
-- 갱신하지 않아 다음 런이 재시도한다. 빈 날(0행)은 status=empty 로 남겨 데이터가
-- 채워지면(해시 변화) 자동 적재된다 — 고정 지연 없음.
--
-- 적용: scripts/osm_daily_sync.py 가 부재 시 이 파일을 그대로 실행한다(멱등 DDL).
--       수동: mysql -u <user> -p lg_clinic < migrations/055_osm_sync_log.sql

CREATE TABLE IF NOT EXISTS osm_sync_log (
    osm_date      DATE          NOT NULL PRIMARY KEY COMMENT 'OSM L1 BASE_DATE',
    status        VARCHAR(12)   NOT NULL COMMENT 'loaded | empty | failed',
    content_hash  CHAR(64)      NULL     COMMENT 'srch+menu 조회 결과 정규화 sha256 — 재조회와 다르면 재적재',
    srch_rows     INT           NOT NULL DEFAULT 0 COMMENT '검색 랭킹 조회 행수',
    menu_rows     INT           NOT NULL DEFAULT 0 COMMENT '메뉴 랭킹 조회 행수',
    cnx_sig       VARCHAR(255)  NULL     COMMENT 'cnx daily 배치({D}) home parse 서명 — 바뀌면 통합 리포트 재생성',
    osm_batch_id  VARCHAR(32)   NULL     COMMENT '{D}_osm',
    all_batch_id  VARCHAR(32)   NULL     COMMENT '{D}_all (cnx + osm 통합 리포트 배치)',
    vis_rows      INT           NULL     COMMENT 'l1_visibility 적재 행수 (osm 배치 슬라이스)',
    sync_count    INT           NOT NULL DEFAULT 0 COMMENT '적재 횟수 (재적재 포함)',
    synced_at     DATETIME      NULL     COMMENT '마지막 적재 시각 (UTC)',
    checked_at    DATETIME      NOT NULL COMMENT '마지막 조회(비교) 시각 (UTC)',
    note          VARCHAR(255)  NULL     COMMENT 'seed / 실패 사유 등'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='OSM visibility daily 동기 원장 (osm_daily_sync)';
