-- Migration 057: osm_sync_history 신설 — osm_daily_sync 런×일자 관측 이력 (append-only)
--
-- 배경 (2026-09-17)
--   원장 osm_sync_log(mig 055)는 일자당 1행을 갱신(upsert)하는 "현재 상태"라, "재조회(resync)
--   시점 대비 그 일자 데이터가 얼마나 바뀌었나"(사용자·EY 질의)를 되짚을 수 없다 — sync_count 로
--   재적재 횟수만 남고 직전 행수·해시·시각은 사라진다. 그동안은 Airflow 태스크 로그의
--   [sync]/[summary] 줄을 파싱해 복원(scripts/osm_sync_history.py --airflow-logs)했다.
--   앞으로는 런마다 창 안의 모든 일자에 대해 관측 1행을 남겨 DB 만으로 답한다.
--
--   한 행 = (run_at 런, osm_date 일자)의 판정: outcome + 그 시점 조회 행수 + 직전 원장값.
--   outcome: empty(0행) | same(해시·cnx 동일) | new(첫 적재) | osm-changed(BQ 정정 재적재) |
--            cnx-changed(cnx 서명 변화로 통합 리포트만 재생성) | retry(직전 실패 재시도) |
--            force(--force) | failed(적재 실패)
--   dry-run 은 기록하지 않는다. 기록 실패는 동기 자체를 막지 않는다(경고만).
--
-- 적용: scripts/osm_daily_sync.py 가 부재 시 이 파일을 그대로 실행한다(멱등 DDL).
--       수동: mysql -u <user> -p lg_clinic < migrations/057_osm_sync_history.sql

CREATE TABLE IF NOT EXISTS osm_sync_history (
    id             INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    run_at         DATETIME      NOT NULL COMMENT '런 시작 시각 (UTC) — 같은 런의 일자들은 같은 값',
    osm_date       DATE          NOT NULL COMMENT 'OSM L1 BASE_DATE',
    outcome        VARCHAR(12)   NOT NULL COMMENT 'empty|same|new|osm-changed|cnx-changed|retry|force|failed',
    content_hash   CHAR(64)      NULL     COMMENT '이번 조회 정규화 해시',
    prev_hash      CHAR(64)      NULL     COMMENT '직전 원장 해시 (변화 판단 근거)',
    srch_rows      INT           NOT NULL DEFAULT 0 COMMENT '이번 조회 검색 랭킹 행수',
    menu_rows      INT           NOT NULL DEFAULT 0 COMMENT '이번 조회 메뉴 랭킹 행수',
    prev_srch_rows INT           NULL     COMMENT '직전 원장 검색 행수',
    prev_menu_rows INT           NULL     COMMENT '직전 원장 메뉴 행수',
    vis_rows       INT           NULL     COMMENT '재적재 시 l1_visibility osm 슬라이스 행수',
    cnx_sig        VARCHAR(255)  NULL     COMMENT '이번 조회 시점 cnx 서명',
    note           VARCHAR(255)  NULL,
    PRIMARY KEY (id),
    INDEX idx_date_run (osm_date, run_at),
    INDEX idx_run (run_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  COMMENT='osm_daily_sync 런×일자 관측 이력 — 재조회 시점 대비 변화 추적';
