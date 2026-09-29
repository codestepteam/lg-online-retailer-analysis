"""osm_daily_sync — OSM visibility(ID1/ID3) 일자 단위 동기 DAG (2026-09-14 컷오버 설계 합의).

cnx daily(lg_clinic_daily_self 02:00 KST)와 분리된 OSM 전용 경로. 하루 3회(06/12/18 KST)
창(OSM_SYNC_LOOKBACK_DAYS, 기본 3일 — 0917 사용자 결정, 7→3) 안의 OSM 일자를 BQ 로 재조회해 원장(osm_sync_log,
mig 055)의 해시와 비교하고, 신규·정정·cnx 변경이 있는 날만 {D}_osm 재합성 → {D}_all 통합
리포트(+ CLINIC-DAILY-{D}.xlsx) → l1_visibility osm 슬라이스 교체를 한다. 같은 날은 skip
(조회 비용 ≈0.35GB/일자). 상세: scripts/osm_daily_sync.py 모듈 docstring.

- OSM L1 적재 지연(실측 D-2)은 고정 lag 대신 '데이터가 보이면 적재'로 흡수 — 빈 날은 empty
  로 기록했다가 채워지면 자동 적재.
- OSM_SOURCE=bq 가 아닌 환경(AWS 개발기)은 조용히 skip.
- 월 마감(매월 4~6일 월간 체인) 전 `--month YYYYMM` 수동 실행으로 늦은 정정을 한 번 더 훑는다.
"""
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

_PROJECT = "/opt/project"

with DAG(
    dag_id="osm_daily_sync",
    description="OSM visibility 일자 동기 — 창 재조회·해시 비교 → {D}_osm/{D}_all/마트 (visibility 만)",
    schedule="0 6,12,18 * * *",   # KST — 02:00 cnx daily 이후, OSM L1 적재를 하루 3회 확인
    start_date=pendulum.datetime(2026, 9, 1, tz="Asia/Seoul"),
    catchup=False,
    max_active_runs=1,
    tags=["lg-clinic", "daily", "osm"],
) as dag:

    osm_sync = BashOperator(
        task_id="osm_sync",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        if [ "${{OSM_SOURCE:-}}" != "bq" ]; then
          echo "[osm_sync] OSM_SOURCE=bq 아님 — skip (BQ 직결 환경 전용)"; exit 0
        fi
        python3 scripts/osm_daily_sync.py --lookback "${{OSM_SYNC_LOOKBACK_DAYS:-3}}"
        """,
        retries=1,
    )
