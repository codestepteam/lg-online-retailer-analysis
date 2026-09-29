"""lg_clinic_monthly_dash — 월말 OSM 확정 스냅샷 + 대시보드 monthly raw
(osm_bq_dashboard_design §3.3/§9-W1·W3, 2026-08-18 → 2026-09-14 월간 체인 재편).

⚠️ 2026-09-14: **스케줄 없음 — 월간 체인의 마지막 단계로 트리거된다**
(bq_target_ingestion 4일 07:00 → czpl_target_refresh → lg_clinic_all → 여기). base 는 conf.batch_id
(체인이 넘김), 없으면 **당월** base(실행일이 속한 달의 8자리 base — 4일에 만든 배치) 자동 탐색.
종전 "매월 1일 03:00 + 전월 base" 규칙은 base 생성월과 리포트 월이 한 달 어긋나는 문제가 있어 폐지.
타깃 일자(OSM 확정·마트 date)는 변함없이 **전월 말일** (규약 A — 4~6일 실행 기준 전달).

  1) osm_finalize — 전월 말일자 OSM 을 base 배치에 반영 (W1-B):
       · pdp: 크롤 레코드에 bq_rating.json 사이드카 (레코드 신설·교체 없음) — DE/UK 5사 포함
       · home: 크롤 키워드 레코드에 bq_results.json 사이드카
                + OSM 전용 키워드·메뉴 경로(ID3)는 합성 레코드 신설
     → parse 재실행 (OSM 14 리테일러 pdp + home 전체) — rating/results 만
       OSM 정본으로 교체 (bq_override 마커).
  2) report_regen — base 의 pdp·home 리포트 재생성 (EYFMT 병합은 이
     리포트를 그대로 집는다 — merge_report 무수정, W1 해소 경로).
  3) export_monthly — l1_conversion / l1_flixmedia 적재 (--as-of 전월 말일, pdp 만 — visibility 는
     daily+osm_daily_sync 가 정본이라 월간 export 안 함(배치명 충돌 방지, 2026-09-15). mig 044 부재 시 무해 skip).

MONTHLY 규칙 (0818 확정): 월간 값 = 해당 월 **마지막 일자 하루치** — 워커 기본값
(--mode monthly = 전월 말일)이 그대로 이 규칙. OSM 엑셀 수동 적재(import_osm_l1)는 9월분부터
폐지 — visibility 는 osm_daily_sync, conversion 은 이 사이드카가 정본.
소스: 번들(파일 브릿지) 우선, 없으면 OSM_SOURCE=bq 직결, 둘 다 없으면 1) skip (2)·3) 은 크롤 원본 기준).
"""
import pendulum
from airflow import DAG
from airflow.models.param import Param
from airflow.operators.bash import BashOperator

_PROJECT = "/opt/project"
# OSM 사이드카 대상 pdp 리테일러 — 9사 + DE/UK 5사 (bq_metric_ingest 스코프와 동일; 레코드 없으면 no-op)
_OSM_RETAILERS = ("Elcorteingles_electronica MediaMarkt_ES Darty_FR Boulanger "
                  "Mediaworld Amazon_IT Unieuro Coolblue Elgiganten "
                  "Amazon_DE MediaMarkt_DE Otto Ao Currys")

# base 결정 — conf.batch_id(체인) > 당월 base(실행일 달의 8자리 base, bq_osm_common.month_base_batch)
_BASE_LOOKUP = (
    'BASE="{{ params.batch_id }}"\n'
    'if [ -z "$BASE" ]; then BASE=$(python3 -c "'
    "import sys; sys.path.insert(0, '.');"
    "from scripts import bq_osm_common as C;"
    "b = C.month_base_batch(C.kst_today()[:6]);"
    "print(b or '', end='')"
    '"); fi\n'
    'if [ -z "$BASE" ]; then echo "[monthly-dash] 당월 base 없음 — 스킵 (체인은 conf.batch_id 로 넘긴다)"; exit 0; fi\n'
    'echo "[monthly-dash] base=$BASE"'
)

with DAG(
    dag_id="lg_clinic_monthly_dash",
    description="월말 OSM 확정(사이드카) + 리포트 재생성 + 대시보드 monthly raw — 월간 체인 마지막 단계(트리거 전용)",
    schedule=None,   # 2026-09-14: 매월 1일 스케줄 폐지 — lg_clinic_all 이 체인으로 트리거 (수동 트리거 가능)
    start_date=pendulum.datetime(2026, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    max_active_runs=1,
    tags=["lg-clinic", "monthly", "dash", "bq"],
    params={
        "batch_id": Param("", type="string",
                          description="base batch (체인이 넘김; 빈 값이면 당월 base 자동 탐색)"),
        "dry_run": Param(False, type="boolean",
                         description="BQ 조회·조인 통계까지만 (기록·적재 생략)"),
    },
) as dag:

    osm_finalize = BashOperator(
        task_id="osm_finalize",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        TGT=$(TZ=Asia/Seoul date -d "$(TZ=Asia/Seoul date +%Y-%m-01) -1 day" +%Y%m%d)
        if ls data/bq_inbox/$TGT/*.csv >/dev/null 2>&1; then
          SRC="--source file --inbox data/bq_inbox/$TGT"
        elif [ "${{OSM_SOURCE:-}}" = "bq" ]; then
          echo "[monthly-dash] 번들 없음 → BQ 직결 (OSM_SOURCE=bq)"
          SRC="--source bq"
        else
          echo "[monthly-dash] 전월 말일 번들($TGT) 없음 — OSM 확정 skip"; exit 0
        fi
        {_BASE_LOOKUP}
        DRY="{{{{ '--dry-run' if params.dry_run else '' }}}}"
        # base 를 명시 — 워커 기본 탐색(bq_visibility_ingest 는 타깃 월=전월 base)은 4일 캐덴스에선
        # 한 달 전 배치를 집는다. 타깃 일자(전월 말일)는 워커 기본값 그대로.
        python3 scripts/bq_metric_ingest.py --mode monthly --base $BASE --batch-id $BASE $DRY $SRC
        python3 scripts/bq_visibility_ingest.py --mode monthly --batch-id $BASE $DRY $SRC
        {{% if not params.dry_run %}}
        for RT in {_OSM_RETAILERS}; do
          python3 parse.py --batch-id $BASE --page-type pdp --all --retailer $RT
        done
        python3 parse.py --batch-id $BASE --page-type home --all
        {{% endif %}}
        """,
        retries=1,
    )

    report_regen = BashOperator(
        task_id="report_regen",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        {{% if params.dry_run %}}echo "[monthly-dash] dry_run — 리포트 생략"; exit 0{{% endif %}}
        {_BASE_LOOKUP}
        python3 make_report.py --batch-id $BASE --page-type pdp --all
        python3 make_report.py --batch-id $BASE --page-type home --all
        """,
        retries=1,
    )

    export_monthly = BashOperator(
        task_id="export_monthly",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        {{% if params.dry_run %}}echo "[monthly-dash] dry_run — 적재 생략"; exit 0{{% endif %}}
        {_BASE_LOOKUP}
        # 규약 A (2026-09-14): 마트 date = 타깃 월(=전월) 말일 — 배치명(크롤일)이 아니라 강제값
        # ⚠️ --page-type pdp (conversion·flixmedia) 만 — visibility 는 daily(cnx 일자 배치) + osm_daily_sync(osm 일자 배치) 가
        # 정본이다. 월간 base 배치명은 실행일(예: 20261004)이라 그날 daily 배치와 **같은 이름** — home 까지
        # export 하면 batch 슬라이스 교체로 그날 daily cnx 행이 지워지고 14사 행이 전월 말일로 들어와
        # OSM 일자 슬라이스와 이중 계상된다 (0824 재적재 사고 1,348→4,195행과 같은 구조, 2026-09-15).
        ASOF=$(TZ=Asia/Seoul date -d "$(TZ=Asia/Seoul date +%Y-%m-01) -1 day" +%Y-%m-%d)
        python3 scripts/export_dash_raw.py --batch-id $BASE \
            --grain monthly --page-type pdp --as-of $ASOF
        """,
        retries=1,
    )

    osm_finalize >> report_regen >> export_monthly
