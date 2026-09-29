"""
Airflow DAGs — LG HS Clinic 모니터링 파이프라인.

DAG 구성 (트랙별 독립 DAG + 래퍼):
    lg_clinic_pdp   — pdp  트랙 (discover → crawl → parse → backfill_mpc → report)
    lg_clinic_plp   — plp  트랙
    lg_clinic_home  — home 트랙
    lg_clinic_all   — 위 3개 DAG 을 병렬로 트리거하는 래퍼 (스케줄 담당)

이유:
    · 트랙 하나만 돌린 경우 Airflow UI 에서 "이 run 이 어떤 트랙이었는지" 가
      DAG 이름으로 바로 드러남 (skipped 색으로 추론할 필요 없음).
    · 스케줄/재실행/history 를 트랙별로 분리 가능.
    · "전체 한번에" 는 래퍼 DAG 이 여전히 하나의 실행 단위로 묶어줌.

트리거:
    · 스케줄  : 없음 — 전 DAG 트리거 전용 (설계 v2: 월간 풀런은 타깃 적재 후 FastAPI/수동, daily 는 lg_clinic_daily_self)
                (스케줄 실행은 conf 가 없으므로 batch_id 는 실행일(YYYYMMDD)로
                자동 발급 — repo.new_batch_id 도 날짜→base 변환이라 규약 동일.
                home 타깃은 배치 무관 DB 마스터(home_target_list×home_keywords)라
                배치별 업로드 없이 돌 수 있다. 월요일엔 all 래퍼의 home 트리거와
                겹치지만 같은 날짜 batch_id 공유 + meta.json resume 스킵이라 무해.)
    · 개별 실행: FastAPI POST /batches/{batch_id}/run?page_type=... 이
                page_type → dag_id 매핑으로 자동 선택 (또는 Airflow UI 수동)

params (트리거 시 conf):
    batch_id  — 실행할 batch_id (예: 20260630). FastAPI /batches 로 발급.
                생략(빈 값) 시 실행일 YYYYMMDD 로 자동 발급 (스케줄 실행 경로).
    instance  — 선택. 특정 국가만 실행 (예: IT). 생략 시 전체.
    retailer  — 선택. 특정 리테일러만 실행 (예: Darty_FR). 생략 시 전체.
    test_mode — 선택. True 면 crawl 단계에서 --all 생략 (리테일러별 1개, 스모크).
"""
from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.models.param import Param
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

_PROJECT = "/opt/project"

# page_type → 트랙별 DAG id 매핑 (FastAPI airflow_client 와 반드시 동일)
DAG_ID_BY_TRACK = {
    "pdp":   "lg_clinic_pdp",
    "plp":   "lg_clinic_plp",
    "home":  "lg_clinic_home",
    "brand": "lg_clinic_brand",   # brand_target_list 마스터 기반 (배치 무관 타깃)
}
WRAPPER_DAG_ID = "lg_clinic_all"

# 트랙별 스케줄 — None 이면 트리거 전용 (lg_clinic_all / FastAPI).
# home: 타깃이 배치 무관 DB 마스터라 conf 없이도 실행 가능 (스케줄 부여 시).
SCHEDULE_BY_TRACK = {
    "pdp":   None,
    "plp":   None,
    # home 전 리테일러 daily 는 설계 v2(2026-08-10)로 폐지 — daily 는 자체수집
    # 5개 한정의 lg_clinic_daily_self 가 담당(OSM 보유 9개는 eopocon→BQ).
    # home 풀런은 monthly 래퍼(lg_clinic_all)에 포함.
    "home":  None,
    "brand": None,
}

# 스케줄 실행은 conf(batch_id)가 없다 → 실행일 YYYYMMDD 로 자동 발급.
# data_interval_end = 이 run 이 발화한 시각(일/주 단위 스케줄 기준 run 당일)이라
# ds_nodash(interval 시작 = 전날)가 아니라 이쪽이 배치 날짜 규약과 일치한다.
# 템플릿 값은 DAG tz 무관 UTC → 배치 날짜는 KST 변환 필수 (0820 KST 전환).
# `[ -z ] && ...` 가드는 set -e 아래에서도 안전 (AND 리스트 조건부는 -e 미적용).
_BATCH_ID_FALLBACK = (
    """[ -z "$BATCH_ID" ] && BATCH_ID="{{ data_interval_end.in_timezone('Asia/Seoul').strftime('%Y%m%d') }}\""""
)


def _cmd(script: str, page_type: str, apply_test_mode: bool = False,
         apply_brand_scope: bool = False) -> str:
    """CLI 명령 템플릿 빌더. optional 인자는 bash 변수로 안전하게 처리.

    apply_test_mode=True 인 태스크(crawl)만 params.test_mode 로 --all 여부와
    params.limit(리테일러별 상한, crawl.py --limit)을 반영한다.
    parse/report 는 항상 배치 전체(크롤 산출물)를 대상으로 하므로 --all 을 유지한다.
    apply_brand_scope=True 인 태스크(report)만 params.brand_scope 를
    make_report.py --brand-scope 로 전달 (crawl/parse 는 이 인자가 없음 —
    brand 트랙 리포트 LG 필터 해제용, SKU coverage. 2026-07-22).
    """
    if apply_test_mode:
        all_flag_line = (
            'TEST_MODE="{{ params.test_mode }}"\n'
            '        if [ "$TEST_MODE" = "True" ] || [ "$TEST_MODE" = "true" ]; then\n'
            '          ALL_FLAG=""\n'
            '        else\n'
            '          ALL_FLAG="--all"\n'
            '        fi'
        )
        limit_line = 'LIMIT="{{ params.limit or \'\' }}"'
    else:
        all_flag_line = 'ALL_FLAG="--all"'
        limit_line = 'LIMIT=""'
    brand_scope_line = ('BRAND_SCOPE="{{ params.brand_scope or \'\' }}"'
                        if apply_brand_scope else 'BRAND_SCOPE=""')
    # crawl 만 --rerun 상시 부가 — 수동 체인(--all --rerun)과 동일 의미론.
    # 자동 실행 인자 감사(docs/scheduling_periodicity_design.md §5-2, 2026-08-10)
    # 에서 누락 확정된 항목. rerun 라운드 수는 crawl.py 기본(2회/60초)을 따른다.
    rerun_line = 'CMD="$CMD --rerun"' if apply_test_mode else ""

    return f"""
        set -e
        cd {_PROJECT}

        BATCH_ID="{{{{ params.batch_id }}}}"
        {_BATCH_ID_FALLBACK}
        INSTANCE="{{{{ params.instance or '' }}}}"
        RETAILER="{{{{ params.retailer or '' }}}}"
        {all_flag_line}
        {limit_line}
        {brand_scope_line}

        CMD="python3 {script} --batch-id $BATCH_ID --page-type {page_type} $ALL_FLAG"
        [ -n "$INSTANCE" ] && CMD="$CMD --instance $INSTANCE"
        [ -n "$RETAILER" ] && CMD="$CMD --retailer $RETAILER"
        [ -n "$LIMIT" ]    && CMD="$CMD --limit $LIMIT"
        [ -n "$BRAND_SCOPE" ] && CMD="$CMD --brand-scope $BRAND_SCOPE"
        {rerun_line}

        echo "[DAG] 실행: $CMD"
        eval $CMD
    """


_COMMON_PARAMS = {
    "batch_id": Param(
        "",
        type="string",
        description="실행할 batch_id (예: 20260630). FastAPI /batches 또는 /batches/upload/* 로 발급. "
                    "생략(빈 값) 시 실행일 YYYYMMDD 자동 발급 — 스케줄 실행 경로.",
    ),
    "instance": Param(
        None,
        type=["null", "string"],
        description="특정 국가만 실행 (SE/FR/IT/PL/NL/ES). 생략 시 전체.",
    ),
    "retailer": Param(
        None,
        type=["null", "string"],
        description="특정 리테일러만 실행 (예: Darty_FR). 생략 시 전체.",
    ),
    "test_mode": Param(
        False,
        type="boolean",
        description="True 면 crawl 단계에서 --all 을 생략해 리테일러별 1개만 수집(스모크 테스트).",
    ),
    "limit": Param(
        None,
        type=["null", "integer"],
        description="crawl 단계 리테일러별 최대 N개 (crawl.py --limit). 생략 시 무제한. "
                    "pdp 처럼 타깃이 많은 트랙의 부분 실행용.",
    ),
    "brand_scope": Param(
        "all",
        type="string",
        enum=["track", "all"],
        description="brand 트랙 리포트 브랜드 범위 (make_report --brand-scope). "
                    "기본 all=경쟁사 포함 — EYFMT 통합 고정 운영(2026-08-10, "
                    "기본 track 이면 자동 실행 시 경쟁사 행 누락). track=LG 행만. "
                    "brand 외 트랙에서는 무시된다.",
    ),
}


def _build_track_dag(page_type: str) -> DAG:
    """트랙 하나짜리 DAG: crawl → parse → report (pdp 는 discover·backfill_mpc 추가)."""
    with DAG(
        dag_id=DAG_ID_BY_TRACK[page_type],
        description=f"LG HS Clinic 모니터링 — {page_type} 트랙 (crawl → parse → report)",
        # 현재 4트랙 전부 트리거 전용 (lg_clinic_all 또는 FastAPI —
        # SCHEDULE_BY_TRACK). 스케줄 발화는 conf 가 없어 batch_id 가
        # 빈 값 → _BATCH_ID_FALLBACK 이 실행일(KST) YYYYMMDD 로 자동 발급한다.
        schedule=SCHEDULE_BY_TRACK[page_type],
        start_date=pendulum.datetime(2026, 1, 1, tz="Asia/Seoul"),
        catchup=False,
        max_active_runs=1,
        tags=["lg-clinic", "monitoring", page_type],
        params=_COMMON_PARAMS,
        # 크롤은 meta.json resume 이라 재시도 비용이 없음. retries=0 이면 스택
        # 재배포(docker compose up)의 SIGTERM 한 번에 run 전체가 failed 로 끝난다
        # (2026-07-04 pdp full run 사망 원인) → 새 scheduler 가 뜬 뒤 이어받도록 상향.
        default_args={"retries": 3, "retry_delay": timedelta(minutes=3)},
    ) as dag:
        crawl = BashOperator(
            task_id=f"crawl_{page_type}",
            bash_command=_cmd("crawl.py", page_type, apply_test_mode=True),
            execution_timeout=None,
            # pdp: discover 실패가 본 크롤(업로드 타깃 수천 건)을 막지 않도록.
            # discover 태스크 자체는 failed 로 남아 run 상태로 가시화된다.
            trigger_rule="all_done" if page_type == "pdp" else "all_success",
        )
        parse = BashOperator(
            task_id=f"parse_{page_type}",
            bash_command=_cmd("parse.py", page_type),
        )
        report = BashOperator(
            task_id=f"report_{page_type}",
            bash_command=_cmd("make_report.py", page_type, apply_brand_scope=True),
            # pdp: backfill_mpc 실패가 리포트 산출을 막지 않도록 (discover→crawl 과
            # 동일 패턴 — backfill 은 failed 로 남아 run 상태로 가시화). parse 실패
            # 시에도 report 가 시도되는 부작용은 merge_report 의 "완료분만이라도"
            # 철학과 동일하게 수용 (run 자체는 parse failed 로 표시된다).
            trigger_rule="all_done" if page_type == "pdp" else "all_success",
        )

        if page_type == "pdp":
            # Phase 0 — 검색 SERP 에서 dataset 에 없는 타깃 발견 (ES DW 등).
            # append-only(repo.append_pdp_targets) 라 재실행/retry 멱등.
            # test_mode 스모크는 크레딧 절약을 위해 스킵 (crawl 도 1개/리테일러만 도는 판).
            discover = BashOperator(
                task_id="discover_pdp_targets",
                bash_command=f"""
        set -e
        cd {_PROJECT}

        TEST_MODE="{{{{ params.test_mode }}}}"
        if [ "$TEST_MODE" = "True" ] || [ "$TEST_MODE" = "true" ]; then
          echo "[DAG] test_mode — discover 스킵"; exit 0
        fi

        BATCH_ID="{{{{ params.batch_id }}}}"
        {_BATCH_ID_FALLBACK}
        INSTANCE="{{{{ params.instance or '' }}}}"
        RETAILER="{{{{ params.retailer or '' }}}}"
        LIMIT="{{{{ params.limit or '' }}}}"

        CMD="python3 discover_targets.py --batch-id $BATCH_ID"
        [ -n "$INSTANCE" ] && CMD="$CMD --instance $INSTANCE"
        [ -n "$RETAILER" ] && CMD="$CMD --retailer $RETAILER"
        [ -n "$LIMIT" ]    && CMD="$CMD --limit $LIMIT"

        echo "[DAG] 실행: $CMD"
        eval $CMD
                """,
                retries=1,   # SERP 몇 페이지 — crawl 의 3회 재시도는 과함
            )
            discover >> crawl

            # Phase 2.5 — parsed.json(JSON-LD model)로 pdp_target_list.mpc 정본
            # 승격 (B안, scripts/backfill_mpc.py). discover 의 A안(타이틀/슬러그
            # 휴리스틱 model_mpc)과 짝을 이룬다. --overwrite-heuristic 은 넘기지
            # 않는다 — 기본 no-overwrite 로 빈 mpc 만 채워 업로드 시트 정본 보존
            # (덮어쓰기 보정은 수동 CLI 전용). 빈 값 채우기 UPDATE 라 retry 멱등.
            backfill = BashOperator(
                task_id="backfill_mpc",
                bash_command=f"""
        set -e
        cd {_PROJECT}

        BATCH_ID="{{{{ params.batch_id }}}}"
        {_BATCH_ID_FALLBACK}
        INSTANCE="{{{{ params.instance or '' }}}}"
        RETAILER="{{{{ params.retailer or '' }}}}"

        CMD="python3 scripts/backfill_mpc.py --batch-id $BATCH_ID"
        [ -n "$INSTANCE" ] && CMD="$CMD --instance $INSTANCE"
        [ -n "$RETAILER" ] && CMD="$CMD --retailer $RETAILER"

        echo "[DAG] 실행: $CMD"
        eval $CMD
                """,
            )
            # Phase 2.7 — 잔여 실패 이미지 지연 백필 + 표적 재파싱 (2026-07-28
            # 사용자 확정: 수집 실패의 보정이므로 **이번 리포트에 반영**돼야
            # 한다 → report 앞 직렬). parse 회수 패스(B)가 남긴 원장을
            # backfill_mpc 가 도는 동안 차단 창이 풀린 뒤 재시도하고, 회수분은
            # 영향 레코드 표적 재파싱으로 parsed 에 병합 → report 가 읽는다.
            image_backfill = BashOperator(
                task_id="image_backfill",
                bash_command=f"""
        set -e
        cd {_PROJECT}
        BATCH_ID="{{{{ params.batch_id }}}}"
        {_BATCH_ID_FALLBACK}
        python3 scripts/backfill_image_ledger.py --batch-id $BATCH_ID
                """,
                retries=1,
            )
            crawl >> parse >> backfill >> image_backfill >> report
        else:
            crawl >> parse >> report
    return dag


dag_pdp   = _build_track_dag("pdp")
dag_plp   = _build_track_dag("plp")
dag_home  = _build_track_dag("home")
dag_brand = _build_track_dag("brand")


# ── 래퍼 DAG: 4개 자식 DAG 을 병렬 트리거 ─────────────────────────────────────
with DAG(
    dag_id=WRAPPER_DAG_ID,
    description="LG HS Clinic — pdp/plp/home/brand 4개 트랙 병렬 실행 (래퍼)",
    # 주1회(월 02:00) 스케줄 폐지 — 설계 v2(2026-08-10, scheduling_periodicity_design
    # '주1회 스케줄 폐지 → bq_target_ingestion 후속 + FastAPI 수동') 코드 반영(0819).
    # 월간 풀런은 타깃 적재(매월 7일) 후 FastAPI/수동 트리거 — 과금 자동발화 없음.
    # daily 축은 lg_clinic_daily_self, 주간 합산은 lg_clinic_weekly_report 담당.
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    max_active_runs=1,
    tags=["lg-clinic", "monitoring", "all"],
    params={**_COMMON_PARAMS,
            "chain": Param(False, type="boolean",
                           description="월간 체인 — 4트랙 전부 성공 + 병합 후 lg_clinic_monthly_dash "
                                       "자동 트리거 (czpl_target_refresh 가 true 로 넘긴다; 수동은 false)")},
    # TriggerDagRunOperator conf 의 "{{ params.test_mode }}" 가 문자열 'True' 로
    # 렌더되면 자식 DAG boolean 파라미터 검증에 걸린다 → 네이티브 타입 렌더링.
    render_template_as_native_obj=True,
) as dag_all:
    # 각 자식 DAG 에 wrapper 의 conf 를 그대로 전달.
    # instance/retailer 는 None → Jinja 가 "None" 으로 렌더하지 않도록 or '' 로 guard.
    # limit 은 pdp 자식에만 전달 (params.limit → pdp crawl --limit) — pdp 만 타깃이
    # 수천 건 규모라 부분 실행이 필요하고, 나머지 트랙은 수십 건이라 무의미.
    triggers = []
    for pt, child_id in DAG_ID_BY_TRACK.items():
        conf = {
            # ⚠️ native 렌더링이 결과를 literal_eval 하므로 batch_id 는 tojson 필수 —
            # "20260705" → int, "20260705_2" → 202607052 (숫자 리터럴 underscore!) 로
            # 오염돼 자식 DAG 의 type="string" 검증에서 즉사한다 (2026-07-05 실측).
            # 스케줄 발화(conf 없음) 시엔 래퍼 시점에 실행일로 1회 확정해 전달 —
            # 자식별 폴백에 맡기면 자정 경계에서 트랙 간 batch_id 가 갈릴 수 있다.
            "batch_id":  "{{ (params.batch_id or data_interval_end.in_timezone('Asia/Seoul').strftime('%Y%m%d')) | tojson }}",
            "instance":  "{{ params.instance or '' }}",
            "retailer":  "{{ params.retailer or '' }}",
            "test_mode": "{{ params.test_mode }}",
            # native 렌더링의 literal_eval 이 'track'/'all' 을 str 로 되돌리도록 tojson
            "brand_scope": "{{ params.brand_scope | tojson }}",
        }
        if pt == "pdp":
            conf["limit"] = "{{ params.limit }}"
        triggers.append(TriggerDagRunOperator(
            task_id=f"trigger_{pt}",
            trigger_dag_id=child_id,
            conf=conf,
            wait_for_completion=True,
            poke_interval=30,
            reset_dag_run=False,
        ))

    # 4개 트랙 완료 후 통합 리포트 2종 (2026-07-16 사용자 확정 — 둘 다 자동 산출):
    #   #1 LGE-CLINIC-REPORT-{DATE}.xlsx        (ID별 wide 시트)
    #   #2 LGE-CLINIC-REPORT-{DATE}-TRACK.xlsx  (--by-track — wide unpivot 4트랙 시트)
    # 일부 트랙 실패 시에도 완료된 트랙만이라도 병합 — INFO 시트에 누락 명시.
    merge = BashOperator(
        task_id="merge_report",
        bash_command=(
            f"set -e\ncd {_PROJECT}\n"
            'BATCH_ID="{{ params.batch_id }}"\n'
            f"{_BATCH_ID_FALLBACK}\n"
            'python3 merge_report.py --batch-id "$BATCH_ID" --by-track'
        ),
        trigger_rule="all_done",
    )

    # 월간 체인(2026-09-14): 4트랙이 **전부 성공**했을 때만 monthly_dash 로 — 일부 실패면 여기서
    # 멈추고 사람이 판단 (부분 모수로 마트 슬라이스가 교체되는 사고 방지).
    def _chain_ok(params, dag_run):
        if not params.get("chain"):
            return False
        bad = [ti.task_id for ti in dag_run.get_task_instances()
               if ti.task_id.startswith("trigger_") and ti.task_id != "trigger_monthly_dash"
               and ti.state != "success"]
        if bad:
            print(f"[chain] 실패 트랙 {bad} — monthly_dash 트리거 생략 (수동 판단)")
        return not bad

    gate_chain = ShortCircuitOperator(task_id="gate_chain", python_callable=_chain_ok)
    trigger_dash = TriggerDagRunOperator(
        task_id="trigger_monthly_dash",
        trigger_dag_id="lg_clinic_monthly_dash",
        conf={"batch_id": "{{ (params.batch_id or data_interval_end.in_timezone('Asia/Seoul').strftime('%Y%m%d')) | tojson }}"},
        wait_for_completion=False,
    )
    triggers >> merge >> gate_chain >> trigger_dash
