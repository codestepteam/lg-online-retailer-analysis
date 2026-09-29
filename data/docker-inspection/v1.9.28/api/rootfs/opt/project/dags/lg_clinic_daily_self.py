"""lg_clinic_daily_self — daily 트랙: 자체수집 5개 크롤 + Boulanger gnb (cnx 전용, 설계 v2
§0-A/0-C, 2026-08-18 재구성 → 2026-09-14 OSM 분리).

⚠️ 2026-09-14 (사용자 확정): **daily 항목 = ID1~4(visibility) 만.** conversion(ID37/38
평점·리뷰)은 cnx·OSM 모두 월간 항목으로 이동 — 월간 체인(lg_clinic_all 14사 pdp 크롤 +
lg_clinic_monthly_dash 의 OSM 월말 사이드카)이 담당한다. 종전 pdp 레그(자체 5사 평점
스냅샷 크롤 ~41k cr/일 · bq_metric_ingest · ID37/38 리포트 · l1_conversion daily 적재)와
모수 daily 갱신(target_refresh_daily)은 제거. 코드 경로는 백필·수동용으로 남아 있다.

⚠️ 2026-09-14 컷오버: **OSM 9(+DE/UK 5)사 합성 레그는 이 DAG 에서 빠져 `osm_daily_sync` 로
분리**됐다. OSM L1 은 D-1 이 02:00 에 없어(실측 D-2) 고정 lag 로 끼워 넣으면 같은 OSM 일자가
두 배치에 실리거나(9/12 이중 실사고) 리포트가 cnx D + OSM D-2 로 섞인다. 이 DAG 는 cnx 만
배치 {D} 에 남기고, osm_daily_sync 가 OSM 일자 D 가 보이는 대로 {D}_osm 을 합성해
{D}_all 통합 리포트(cnx {D} parse 하드링크 + osm)와 마트 osm 슬라이스를 만든다.
→ 통합 리포트·EY 납품 파일(CLINIC-DAILY-{D}.xlsx)은 data/{D}_all/home/report/.

대상:
  자체수집 5개 — NL MediaMarkt · PL MediaExpert · PL RtvEuroAgd · CZ Datart ·
  CZ Alza: CNX daily 크롤 (home ID1~4).
  + DAILY_GNB_CNX_RETAILERS(기본 Boulanger): OSM 메뉴에 상위 카테고리 페이지가 없는
    OSM 리테일러의 ID3 만 우리 gnb 크롤(--gnb-only, 2페이지).

구성 (매일 02:00 KST):
  1) home_crawl_self   — 자체 5개 crawl+parse + gnb-only 리테일러 (실행일 base 배치)
  2) home_report       — make_report home (cnx 만 — 통합본은 osm_daily_sync 의 {D}_all)
  3) export_home_daily — l1_visibility cnx 슬라이스 적재 (mig 050 — 부재 시 무해 skip)
"""
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

_PROJECT = "/opt/project"
# 자체수집 5개 — crawl --retailer 는 단건이라 bash 루프로 순차 실행
# (scripts/osm_daily_sync.CNX_DAILY_RETAILERS 와 같은 셋 — 변경 시 함께)
_SELF_RETAILERS = "MediaMarkt_NL MediaExpert_PL RtvEuroAgd_PL Datart Alza"
# OSM 메뉴 데이터에 **상위 카테고리 페이지가 없는** OSM 리테일러 — ID3(GNB)는 우리
# gnb_keyword_map 크롤(--gnb-only, 2페이지)로 채우고 bq_visibility_ingest 는 이 리테일러의
# OSM 메뉴 경로를 건너뛴다 (2026-09-14 사용자 확정: "원래 cnx 크롤을 써야 하는 케이스").
# 실측: Boulanger 는 OSM 메뉴가 'lave-linge hublot > …' 하위 경로뿐(OSM 자체 menu_map 도 제외).
# Darty·Coolblue·Elgiganten·Unieuro·ECI·MM ES·MW·Amazon IT 는 상위 경로가 있어 OSM 그대로.
# 컨테이너 env DAILY_GNB_CNX_RETAILERS(공백 구분) — 워커와 같은 값을 읽는다.
_GNB_CNX_DEFAULT = "Boulanger"

# ⚠️ Airflow 템플릿의 data_interval_end 는 DAG tz 와 무관하게 항상 UTC —
# 날짜 파생은 반드시 .in_timezone('Asia/Seoul') 경유. KST 02:00 런의 미변환
# strftime 은 UTC 전일 17:00 이라 배치 날짜가 하루 밀린다.

with DAG(
    dag_id="lg_clinic_daily_self",
    description="daily — 자체 5개 크롤 + gnb 예외: ID1~4(home) cnx 만. OSM 은 osm_daily_sync (2026-09-14)",
    schedule="0 2 * * *",   # 02:00 KST (start_date tz 기준 — 2026-08-20 UTC→KST 전환)
    start_date=pendulum.datetime(2026, 8, 1, tz="Asia/Seoul"),
    catchup=False,
    max_active_runs=1,
    tags=["lg-clinic", "daily"],
) as dag:

    home_crawl_self = BashOperator(
        task_id="home_crawl_self",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        BATCH_ID="{{{{ data_interval_end.in_timezone('Asia/Seoul').strftime('%Y%m%d') }}}}"
        for RT in {_SELF_RETAILERS}; do
          echo "[daily-self] home crawl $RT"
          python3 crawl.py --batch-id $BATCH_ID --page-type home --all --rerun \
              --retailer $RT
          python3 parse.py --batch-id $BATCH_ID --page-type home --all --retailer $RT
        done
        # OSM 리테일러 중 상위 카테고리 페이지가 OSM 메뉴에 없는 곳 — GNB 만 우리 크롤
        for RT in ${{DAILY_GNB_CNX_RETAILERS:-{_GNB_CNX_DEFAULT}}}; do
          echo "[daily-self] gnb-only crawl $RT (OSM 메뉴 상위 경로 부재 보강)"
          python3 crawl.py --batch-id $BATCH_ID --page-type home --all --rerun \
              --gnb-only --retailer $RT
          python3 parse.py --batch-id $BATCH_ID --page-type home --all --retailer $RT
        done
        """,
        retries=1,
    )

    home_report = BashOperator(
        task_id="home_report",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        BATCH_ID="{{{{ data_interval_end.in_timezone('Asia/Seoul').strftime('%Y%m%d') }}}}"
        python3 make_report.py --batch-id $BATCH_ID --page-type home --all
        """,
        retries=1,
    )

    export_home_daily = BashOperator(
        task_id="export_home_daily",
        bash_command=f"""
        set -e
        cd {_PROJECT}
        BATCH_ID="{{{{ data_interval_end.in_timezone('Asia/Seoul').strftime('%Y%m%d') }}}}"
        python3 scripts/export_dash_raw.py --batch-id $BATCH_ID \
            --grain daily --page-type home
        """,
        retries=1,
    )

    (home_crawl_self >> home_report >> export_home_daily)
