-- Migration 054: pdp_metric_overrides 신설 — PDP 지표 예외처리(EY Eye-check 강제값) 마스터
--
-- 배경 (EY 2026-08-31 'LGE_HS_Clinic_예외처리 URL 리스트_USP 관련_260831.xlsx')
--   스페인 식기세척기 PDP 19개 URL 에 대해 EY 가 실물 확인(Eye-check)한 ID24/25/35
--   판정을 Y 로 못 박아 보냈다 — "Y 로 표시된 항목에 한하여 추후 재진단/크롤링 시
--   예외 처리". 예시 시트 규칙: 해당 URL 의 노란 셀 컬럼(ID24 포함 여부 / ID25 갤러리 내
--   USP 존재 여부 / ID35 갤러리 첫세트 내 USP 여부)만 **항상 1 로 고정**, 그 외 컬럼은
--   크롤값 그대로. N 은 크롤 결과 그대로(강제 없음). 매 배치 리포트에 자동 반영돼야
--   하므로 파일 수정이 아니라 마스터 + eval 후처리(core/eval.apply_metric_overrides)로 둔다.
--
-- 키 설계
--   - sku_key = URL 에서 뽑은 리테일러 상품코드 (core/product_id.extract — ECI 'A54257250',
--     MM '1592827'). pdp_target_list.product_id 는 URL uuid5 라 같은 상품도 슬러그가
--     바뀌면 id 가 달라진다(A54257250: 20260807 099f5519… / 20260902 070ab454… 실측)
--     → 월간 모수가 바뀌어도 따라가도록 SKU 코드로 매칭한다.
--   - rtlr_name 은 DB 순수 표기(brand_target_list 와 동일): MediaMarkt / Elcorteingles_electronica.
--   - metric_id ∈ {24, 25, 35} (eval.OVERRIDE_METRICS 가 지표명으로 매핑). forced_value 1 = 존재(10점).
--   - active=0 으로 끄면 무시(행 삭제 대신 이력 보존).
--
-- 적재/갱신: scripts/load_metric_overrides.py <EY xlsx> (Y/Ｙ 정규화, ON DUPLICATE KEY 갱신).
-- 실행: mysql -u <user> -p lg_clinic < migrations/054_pdp_metric_overrides.sql
--   ⚠️ AWS(개발)·devtools·GCP(운영) DB 모두 적용할 것 — 미적용이면 refdata 로더가 빈 결과로
--     흡수해 전 행이 조용히 크롤값 그대로 나간다 (mig 037 과 같은 사각).

CREATE TABLE IF NOT EXISTS pdp_metric_overrides (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    rtlr_name    VARCHAR(64)   NOT NULL
        COMMENT '순수 리테일러명 (brand_target_list 표기 — MediaMarkt / Elcorteingles_electronica)',
    cntry_cd     CHAR(2)       NOT NULL COMMENT '국가 코드 (ES …)',
    sku_key      VARCHAR(128)  NOT NULL
        COMMENT 'URL 의 리테일러 상품코드 (core.product_id.extract) — uuid product_id 는 슬러그 변경에 깨져 키로 못 씀',
    metric_id    SMALLINT      NOT NULL COMMENT '지표 ID (24 / 25 / 35)',
    forced_value TINYINT       NOT NULL DEFAULT 1 COMMENT '강제 판정 (1=존재/Y → 10점, 0=부재 → 0점)',
    src_url      VARCHAR(2048) NULL COMMENT 'EY 제공 URL 원문 (참고용 — 매칭엔 sku_key 사용)',
    source       VARCHAR(128)  NULL COMMENT '출처 (EY 리스트 파일명·일자)',
    active       TINYINT(1)    NOT NULL DEFAULT 1 COMMENT '0 이면 무시 (이력 보존용)',
    notes        VARCHAR(255)  NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_override (rtlr_name, cntry_cd, sku_key, metric_id)
) COMMENT='PDP 지표 예외처리(EY Eye-check 강제값) 마스터 — ID24/25/35 (EY 2026-08-31 리스트)';

-- 시드: EY 260831 리스트의 Y 항목 40건 (ID24 13 · ID25 19 · ID35 8) — N / N/A 는 미적재
INSERT INTO pdp_metric_overrides (rtlr_name, cntry_cd, sku_key, metric_id, forced_value, src_url, source) VALUES
    ('Elcorteingles_electronica', 'ES', 'A52607166', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A52607166-8806096005477-pr-lavavajillas-lg-13-servicios-60-cm-df030fl-acero-inoxidable-antihuellas/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A53309696', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A53309696-lavavajillas-lg-13-servicios-60-cm-df030fw/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A54257250', 24, 1, 'https://www.elcorteingles.es/electrodomesticos/A54257250-8806096235973-pr-lavavajillas-lg-14-serviciosquadwashtm-60-cm-df142fw-blanco/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A54257250', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A54257250-8806096235973-pr-lavavajillas-lg-14-serviciosquadwashtm-60-cm-df142fw-blanco/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A54257251', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A54257251-lavavajillas-integrable-lg-14-servicios-bandeja-para-cubiertos-60-cm-db476txs/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A54258678', 24, 1, 'https://www.elcorteingles.es/electrodomesticos/A54258678-8806096348864-pr-lavavajillas-lg-14-serviciosquadwashtm-60-cm-df142fv-inox-antihuellas/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A54258678', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A54258678-8806096348864-pr-lavavajillas-lg-14-serviciosquadwashtm-60-cm-df142fv-inox-antihuellas/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A54773312', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A54773312-lavavajillas-integrable-lg-14-servicios-bandeja-para-cubiertos-db597txs/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A55345345', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A55345345-lavavajillas-lg-14-servicios-bandeja-para-cubiertos-60-cm-df587hhs/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A56647477', 24, 1, 'https://www.elcorteingles.es/electrodomesticos/A56647477-8806096504246-pr-lavavajillas-integrable-lg-14-servicios-quadwashtm-db273tx/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A56647477', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A56647477-8806096504246-pr-lavavajillas-integrable-lg-14-servicios-quadwashtm-db273tx/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A56647489', 24, 1, 'https://www.elcorteingles.es/electrodomesticos/A56647489-lavavajillas-lg-14-servicios-quadwashtm-steam-con-lavado-a-vapor-y-tercera-bandeja-df375hws/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A56647489', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A56647489-lavavajillas-lg-14-servicios-quadwashtm-steam-con-lavado-a-vapor-y-tercera-bandeja-df375hws/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A56647495', 24, 1, 'https://www.elcorteingles.es/electrodomesticos/A56647495-8806096541135-pr-lavavajillas-lg-14-servicios-quadwashtm-con-tercera-bandeja-df273fw-blanco/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('Elcorteingles_electronica', 'ES', 'A56647495', 25, 1, 'https://www.elcorteingles.es/electrodomesticos/A56647495-8806096541135-pr-lavavajillas-lg-14-servicios-quadwashtm-con-tercera-bandeja-df273fw-blanco/', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592827', 24, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df142fv-14-servicios-5-programas-60-cm-quadwashtm-inverter-direct-drivetm-inox-antihuellas-1592827.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592827', 25, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df142fv-14-servicios-5-programas-60-cm-quadwashtm-inverter-direct-drivetm-inox-antihuellas-1592827.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592827', 35, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df142fv-14-servicios-5-programas-60-cm-quadwashtm-inverter-direct-drivetm-inox-antihuellas-1592827.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592828', 24, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df142fw-14-servicios-5-programas-60-cm-quadwashtm-easyracktm-blanco-1592828.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592828', 25, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df142fw-14-servicios-5-programas-60-cm-quadwashtm-easyracktm-blanco-1592828.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592828', 35, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df142fw-14-servicios-5-programas-60-cm-quadwashtm-easyracktm-blanco-1592828.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592829', 24, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df587hhs-14-servicios-10-programas-60-cm-quadwashtm-tercera-bandeja-thinqtm-blanco-1592829.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592829', 25, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df587hhs-14-servicios-10-programas-60-cm-quadwashtm-tercera-bandeja-thinqtm-blanco-1592829.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592829', 35, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df587hhs-14-servicios-10-programas-60-cm-quadwashtm-tercera-bandeja-thinqtm-blanco-1592829.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592845', 24, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-integrable-lg-db476txs-14-servicios-10-programas-60-cm-truesteamtm-tercera-bandeja-sin-panelar-1592845.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592845', 25, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-integrable-lg-db476txs-14-servicios-10-programas-60-cm-truesteamtm-tercera-bandeja-sin-panelar-1592845.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592846', 24, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-integrable-lg-db597txs-14-servicios-10-programas-60-cm-truesteamtm-easyracktm-sin-panelar-1592846.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592846', 25, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-integrable-lg-db597txs-14-servicios-10-programas-60-cm-truesteamtm-easyracktm-sin-panelar-1592846.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1592846', 35, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-integrable-lg-db597txs-14-servicios-10-programas-60-cm-truesteamtm-easyracktm-sin-panelar-1592846.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601363', 24, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-integrable-lg-db273tx-14-servicios-9-programas-598-cm-tercera-bandeja-quadwashtm-sin-panelar-1601363.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601363', 25, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-integrable-lg-db273tx-14-servicios-9-programas-598-cm-tercera-bandeja-quadwashtm-sin-panelar-1601363.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601363', 35, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-integrable-lg-db273tx-14-servicios-9-programas-598-cm-tercera-bandeja-quadwashtm-sin-panelar-1601363.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601372', 24, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df375hws-14-servicios-10-programas-60-cm-led-tactil-tercera-bandeja-truesteamtm-quadwashtm-blanco-1601372.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601372', 25, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df375hws-14-servicios-10-programas-60-cm-led-tactil-tercera-bandeja-truesteamtm-quadwashtm-blanco-1601372.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601372', 35, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df375hws-14-servicios-10-programas-60-cm-led-tactil-tercera-bandeja-truesteamtm-quadwashtm-blanco-1601372.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601373', 24, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df375hms-14-servicios-10-programas-60-cm-led-tactil-tercera-bandeja-truesteamtm-quadwashtm-acero-negro-grafito-antihuellas-1601373.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601373', 25, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df375hms-14-servicios-10-programas-60-cm-led-tactil-tercera-bandeja-truesteamtm-quadwashtm-acero-negro-grafito-antihuellas-1601373.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601373', 35, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df375hms-14-servicios-10-programas-60-cm-led-tactil-tercera-bandeja-truesteamtm-quadwashtm-acero-negro-grafito-antihuellas-1601373.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601374', 25, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df273fw-14-servicios-10-programas-60-cm-quadwashtm-blanco-1601374.html', 'EY 예외처리 URL 리스트_USP 관련_260831'),
    ('MediaMarkt', 'ES', '1601374', 35, 1, 'https://www.mediamarkt.es/es/product/_lavavajillas-lg-df273fw-14-servicios-10-programas-60-cm-quadwashtm-blanco-1601374.html', 'EY 예외처리 URL 리스트_USP 관련_260831')
ON DUPLICATE KEY UPDATE forced_value = VALUES(forced_value), src_url = VALUES(src_url),
                        source = VALUES(source), active = 1;
