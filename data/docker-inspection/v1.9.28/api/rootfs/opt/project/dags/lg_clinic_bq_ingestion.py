"""bq_target_ingestion — BQ(OSM) → pdp_target_list 월간 적재 (설계 v2 §5, 2026-08-11).

월간 체인 개시 (2026-09-14 확정: **매월 4일 07:00 KST 에 전월 조회** — "4~6일쯤 전달 조회"):
  bq_target_ingestion(전월 OSM 모수 → base=실행일) → czpl_target_refresh(CZ·PL append + NL MM)
  → lg_clinic_all(4트랙 크롤 + EYFMT 병합) → lg_clinic_monthly_dash(전월 말일 OSM 확정 사이드카 +
  리포트 재생성 + 마트 --as-of 전월 말일). 체인은 conf.chain=true 로 이어진다 — 수동 트리거
  (CSV 업로드 뒤 czpl 만, 또는 lg_clinic_all 단독)는 기본 false 라 뒤로 번지지 않는다.
  base 배치 = 실행일(예: 20261004) = **당월** 이름이지만 내용은 전월 리포트 — 마트/모수 date 는
  규약 A(타깃 월 말일)로 강제된다.

개시 단계:
  BQ 통합 쿼리(dags/sql/osm_target_extract.sql — 사용자 제공 v2 0818,
  dedupe·2,000캡·SALE_RK 우선을 쿼리 내 처리. Coverage QA 필터는 미포함 원칙.
  v5 0917: dedupe 키 = 정규화 URL — RPC/MPC 같아도 URL 다르면 별개 타깃)
  → 검증 게이트(G1 인코딩 차단 · G2 행수 드리프트 **경고 전용**(0918, BQ_G2_STRICT=1 로 차단) · G3 upsert 안전)
  → upsert_pdp_targets (1차 5개국 9개 리테일러)
  → 성공 시 czpl_target_refresh 자동 트리거 (CZ·PL append + NL MM discovery)
  로 7개국 모수를 완성한다. 이후 월간 수집 체인은 이 base batch 를 사용.

⚠️ 순서 불변식: BQ upsert(DELETE-후-재삽입)는 반드시 append 이전 —
   이 DAG 가 czpl_target_refresh 를 뒤에 트리거하는 이유이자, G3 게이트가
   기존 행 존재 시 차단하는 이유다 (역순이면 CZ·PL·NL MM 분 소실).

사전 조건 (v1.9-other 라인 — 파일 브릿지 단일 소스): 브릿지 머신이
  `scripts/bq_fetch_bundle.py --mode targets` 로 생성한 번들이
  data/bq_inbox/targets_{전월YYYYMM}/ 에 반입돼 있어야 한다.
  (BQ 직결·SA 키 구성은 feature/v1.9-gcp-scheduling 라인)
"""
import pendulum
from airflow import DAG
from airflow.models.param import Param
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

_PROJECT = "/opt/project"

with DAG(
    dag_id="bq_target_ingestion",
    description="BQ OSM 통합 쿼리 → pdp_target_list 월간 적재 + czpl refresh 체인",
    schedule="0 7 4 * *",   # 매월 4일 07:00 KST — 전월 조회 (2026-09-14: 7일 → 4일)
    # 컷오버(0914) 이후 첫 발화 = 10/4 07:00 이어야 한다. cron 데이터 구간은 [9/4 07:00, 10/4 07:00)
    # 이고 그 시작(9/4)이 start_date 이상이어야 하므로 9/1 — 9/15 로 두면 첫 구간이 [10/4, 11/4) 가
    # 돼 11/4 에야 돈다. 8/4 보다 뒤라 unpause 즉시 '지난 구간'(8월 모수 재적재 → 체인 과금)도 안 뜬다.
    start_date=pendulum.datetime(2026, 9, 1, tz="Asia/Seoul"),
    catchup=False,
    max_active_runs=1,
    tags=["lg-clinic", "monthly", "targets", "bq"],
    params={
        "batch_id": Param("", type="string",
                          description="base batch (빈 값이면 실행일 KST YYYYMMDD)"),
        "start_date": Param("", type="string",
                            description="원천 조회 시작 YYYY-MM-DD (빈 값이면 전월 — 창은 월 내 실데이터 MIN/MAX)"),
        "end_date": Param("", type="string",
                          description="원천 조회 종료 YYYY-MM-DD (빈 값이면 전월 말일)"),
        "dry_run": Param(False, type="boolean",
                         description="검증까지만 — 적재·후속 트리거 생략"),
        "force": Param(False, type="boolean",
                       description="G2 드리프트·G3 기존 행 게이트 무시"),
    },
) as dag:

    # 마지막 stdout 줄(echo $BATCH_ID)이 XCom → 후속 트리거 conf 로 전달
    ingest = BashOperator(
        task_id="extract_validate_load",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        BATCH_ID="{{{{ params.batch_id }}}}"
        if [ -z "$BATCH_ID" ]; then
          BATCH_ID=$(TZ=Asia/Seoul date +%Y%m%d)
        fi
        CMD="python3 scripts/bq_target_ingest.py --batch-id $BATCH_ID"
        MONTH=$(TZ=Asia/Seoul date -d "$(TZ=Asia/Seoul date +%Y-%m-01) -1 day" +%Y%m)
        if ls data/bq_inbox/targets_$MONTH/*.csv >/dev/null 2>&1; then
          CMD="$CMD --source file"
        elif [ "${{OSM_SOURCE:-}}" = "bq" ]; then
          echo "[bq-ingest] 번들 없음 → BQ 직결 (OSM_SOURCE=bq)" >&2
          CMD="$CMD --source bq"
        else
          echo "[bq-ingest] 타깃 번들(targets_$MONTH) 없음 — 브릿지에서 생성·전송 필요" >&2; exit 1
        fi
        {{% if params.start_date %}}CMD="$CMD --start-date {{{{ params.start_date }}}} --end-date {{{{ params.end_date }}}}"{{% endif %}}
        {{% if params.dry_run %}}CMD="$CMD --dry-run"{{% endif %}}
        {{% if params.force %}}CMD="$CMD --force"{{% endif %}}
        echo "[bq-ingest] $CMD" >&2
        $CMD >&2
        echo "$BATCH_ID"
        """,
        retries=2,   # extract 는 BQ 일시 오류 재시도 — 적재는 upsert 멱등이라 안전
    )

    # dry_run 이면 후속 체인 차단 — base 미적재 상태에 CZ·PL 만 append 되는 것 방지
    gate_not_dry = ShortCircuitOperator(
        task_id="gate_not_dry_run",
        python_callable=lambda params: not params["dry_run"],
    )

    trigger_refresh = TriggerDagRunOperator(
        task_id="trigger_czpl_refresh",
        trigger_dag_id="czpl_target_refresh",
        # chain=true → czpl 이 끝나면 lg_clinic_all → monthly_dash 로 이어진다 (2026-09-14)
        conf={"batch_id": "{{ ti.xcom_pull(task_ids='extract_validate_load') }}",
              "chain": True},
        wait_for_completion=False,
    )

    ingest >> gate_not_dry >> trigger_refresh
