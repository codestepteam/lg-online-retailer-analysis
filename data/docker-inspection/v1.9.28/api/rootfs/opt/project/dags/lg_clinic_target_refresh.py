"""czpl_target_refresh — 월간 모수 완성 단계 (설계 v2 §5-1, 2026-08-10).

월간 체인에서 base batch 발급(bq_target_ingestion / FastAPI 업로드) 직후 실행되어,
BQ/OSM 이 커버하지 않는 자체수집 타깃을 같은 base 에 append 해 7개국 모수를
완성한다. 2단 구성 (2026-08-11 NL MM 편입):
  1) CZ·PL — 확정 타깃셋 배치에서 복사 append (크레딧 0)
  2) NL MM pdp — 카테고리 직행 discovery (scripts/discover_nlmm_pdp.py,
     SB ~1,800cr/월. MM 라인업 변동을 월간 재수확 — append 멱등이라 기존분 보존)

schedule=None — 수동/체인 트리거 전용 (conf.chain=true 면 끝에서 lg_clinic_all 을 이어 트리거 — 2026-09-14 월간 체인):
  · bq_target_ingestion 성공 → TriggerDagRun 자동 연결 (batch_id conf 전달)
  · FastAPI 업로드 경로는 수동 트리거로 병행
멱등: append_pdp_targets 의 product_id dedupe — 재실행 안전.
"""
import pendulum
from airflow import DAG
from airflow.models.param import Param
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

_PROJECT = "/opt/project"

with DAG(
    dag_id="czpl_target_refresh",
    description="월간 base 에 자체수집(CZ·PL) 확정 타깃셋 append — 7개국 모수 완성",
    schedule=None,
    start_date=pendulum.datetime(2026, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    max_active_runs=1,
    tags=["lg-clinic", "monthly", "targets"],
    params={
        "batch_id": Param("", type="string",
                          description="append 대상 base batch (빈 값이면 당월 base 자동 탐색)"),
        "source_batch": Param("20260721_02", type="string",
                              description="확정 타깃셋 배치 — 구셋 사용 금지 "
                                          "(0810 실측: 구셋 잔재 11건 단종 되살림)"),
        "nlmm_discovery": Param(True, type="boolean",
                                description="NL MM pdp 카테고리 직행 discovery "
                                            "실행 여부 (SB ~1,800cr)"),
        "chain": Param(False, type="boolean",
                       description="월간 체인 — 완료 후 lg_clinic_all(4트랙 크롤+EYFMT, SB 과금) → "
                                   "monthly_dash 자동 트리거. bq_target_ingestion 이 true 로 넘긴다; "
                                   "수동 트리거는 기본 false"),
    },
) as dag:

    append_targets = BashOperator(
        task_id="append_selfcollect_targets",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        BATCH_ID="{{{{ params.batch_id }}}}"
        if [ -z "$BATCH_ID" ]; then
          BATCH_ID=$(python3 scripts/current_month_base.py)
        fi
        echo "[target-refresh] base=$BATCH_ID source={{{{ params.source_batch }}}}"
        python3 scripts/append_selfcollect_targets.py --batch-id "$BATCH_ID" \
            --source-batch "{{{{ params.source_batch }}}}"
        """,
        retries=1,
    )

    # NL MM 은 OSM 미커버 + 확정셋도 없음 — 매월 라이브 라인업을 직접 수확.
    # 검색 경유 불가(SB 그리드 미하이드레이션 실측)라 카테고리 직행이 유일 경로.
    discover_nlmm = BashOperator(
        task_id="discover_nlmm_pdp",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        {{% if not params.nlmm_discovery %}}
        echo "[target-refresh] nlmm_discovery=false — 스킵"; exit 0
        {{% endif %}}
        BATCH_ID="{{{{ params.batch_id }}}}"
        if [ -z "$BATCH_ID" ]; then
          BATCH_ID=$(python3 scripts/current_month_base.py)
        fi
        echo "[target-refresh] NL MM discovery base=$BATCH_ID"
        python3 scripts/discover_nlmm_pdp.py --batch-id "$BATCH_ID"
        """,
        retries=1,
    )

    # 월간 체인 — base 모수 완성 뒤 4트랙 크롤 (conf.chain 일 때만; batch_id 는 그대로 전달)
    gate_chain = ShortCircuitOperator(
        task_id="gate_chain",
        python_callable=lambda params: bool(params["chain"]),
    )
    trigger_all = TriggerDagRunOperator(
        task_id="trigger_lg_clinic_all",
        trigger_dag_id="lg_clinic_all",
        # 이 DAG 은 일반 렌더링 — 문자열 그대로 전달 (자식 lg_clinic_all 이 native 로 받아 str 검증 통과)
        conf={"batch_id": "{{ params.batch_id }}", "chain": True},
        wait_for_completion=False,
    )

    append_targets >> discover_nlmm >> gate_chain >> trigger_all
