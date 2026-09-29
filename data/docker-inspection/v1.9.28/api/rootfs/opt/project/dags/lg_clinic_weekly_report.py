"""lg_clinic_weekly_report — 주간 합산 리포트 (2026-08-11 양식 확정).

매주 월요일 03:00 KST (발송 앵커 — 창은 앵커 제외 직전 7일이라 당일 daily
진행 중이어도 무관): 직전 7일 daily 리포트(기존 포맷)를
같은 이름 시트끼리 **행으로 이어붙여** LGE-CLINIC-REPORT-{앵커일}-WEEKLY.xlsx
산출 (scripts/weekly_rollup.py). 별도 주간 양식 없음 — 컬럼 무변경,
Date 컬럼만 일자별로 쌓여 연속성 확보 (사용자 확정. 30일 평균은 보류).
일자별 리포트는 osm_daily_sync 가 {D}_all(cnx+OSM 통합)에 산출(CLINIC-DAILY-{D}.xlsx, EY 납품형) —
없는 날은 cnx 배치 {D} 의 리포트로 폴백. 이 DAG 은 누적만 (2026-09-14: conversion 은 월간이라 pdp 없음).
산출물은 MinIO 자동 미러(발송은 수동/후속).
"""
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

_PROJECT = "/opt/project"

with DAG(
    dag_id="lg_clinic_weekly_report",
    description="주간 합산 리포트 — daily ID1~4(통합 {D}_all 의 CLINIC-DAILY 우선) 7일 병합",
    schedule="0 3 * * 1",   # 매주 월요일 03:00 KST — 앵커 제외 직전 7일 창
    # 컷오버(0914 월요일) 뒤 첫 발화 = 9/21 03:00 (창 9/14~9/20). cron 구간 [9/14 03:00, 9/21 03:00) 의
    # 시작이 start_date 이상이어야 하므로 9/14 00:00 — 지난 주 구간(9/7~)은 제외돼 unpause 즉시 런 없음.
    start_date=pendulum.datetime(2026, 9, 14, tz="Asia/Seoul"),
    catchup=False,
    max_active_runs=1,
    tags=["lg-clinic", "weekly"],
) as dag:

    rollup = BashOperator(
        task_id="weekly_rollup",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        python3 scripts/weekly_rollup.py \
            --anchor "{{{{ data_interval_end.in_timezone('Asia/Seoul').strftime('%Y%m%d') }}}}"
        """,
        retries=1,
    )
