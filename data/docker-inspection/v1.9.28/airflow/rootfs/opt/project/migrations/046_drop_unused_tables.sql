-- Migration 046: 미사용 테이블 정리 (2026-08-19 코드 참조 전수 대조 실측)
--
-- 판정 기준: 전 소스(*.py — core/scripts/dags/app/crawl·parse_retailers) git grep
-- 워드 매칭 0건 + 데이터 성격 확인. 대어(image_asset_link 787MB, pdp_20260622
-- 155MB 등)는 전부 실사용이라 유지 — 이 정리는 용량보다 스키마 위생 목적.
--
-- A. 테스트/백업 잔재 (참조 0)
DROP TABLE IF EXISTS TEST_PDP_TARGET_TABLE;        -- 0707 업로드 실험 (21,720행)
DROP TABLE IF EXISTS TEST_PDP_TARGET_TABLE_2;      -- 0708 업로드 실험 (9,693행)
DROP TABLE IF EXISTS gnb_keyword_map_backup_v1;    -- 리시드 백업 — 정본은 mig 017/018/032/040
DROP TABLE IF EXISTS gnb_keyword_map_backup_v2;
DROP TABLE IF EXISTS gnb_keyword_map_backup_v3;
DROP TABLE IF EXISTS gnb_keyword_map_backup_v4;

-- B. osm-metric 초기 실험의 OSM 엑셀 덤프 (mig 023) — 읽는 코드 전무 (쓰기
--    엔드포인트만 존재). 현행 v1.9 는 BQ 직조회(파일 브릿지)로 대체 — 원본은
--    BQ pjt-lge-oned.L2_ONED 에 있어 재획득 가능. app/main.py 의
--    /masters 업로드 라우트(core/market_datasets.py)는 고아 코드 — 별도 정리.
DROP TABLE IF EXISTS VSMRKT_DAILY_OSM_BANR_VSBLT_D; -- 0713 덤프 (28,449행)
DROP TABLE IF EXISTS VSMRKT_DAILY_OSM_SALE_RK_D;    -- 0713 덤프 (29,804행)
DROP TABLE IF EXISTS TSPURC_LIST_FULL_SUMM_S;       -- 0행 (적재된 적 없음)

-- C. 초기 수동 시드 후 미사용 (마이그레이션 밖 생성, SQL 문맥 참조 0)
DROP TABLE IF EXISTS country;                       -- 7행
DROP TABLE IF EXISTS locale;                        -- 80행
DROP TABLE IF EXISTS hs_category_group;             -- 3행 (hs_category 는 실사용 — 유지)
DROP TABLE IF EXISTS gnb_brand_category_map;        -- 21행 (mig 014 리네임 스침뿐)

-- D. 사용자 확정 0819: 대시보드 raw 는 daily 2벌만 운용 — monthly 2벌 폐기.
--    export_dash_raw.py 는 테이블 부재(1146) 시 경고 후 skip 이라 코드 무변경
--    안전 (monthly_dash DAG 의 export_monthly 도 무해 통과).
DROP TABLE IF EXISTS dash_visibility_monthly;
DROP TABLE IF EXISTS dash_conversion_monthly;

-- 보류 (이 파일에 미포함): usp_sku_keywords_ori — 참조 0 이지만 '_ori' 원본
-- 보관 성격 + mig 025 에 시드 없음(DB 가 유일 사본일 수 있음). 삭제하려면
-- 덤프 백업 후 별도 진행 권장.
