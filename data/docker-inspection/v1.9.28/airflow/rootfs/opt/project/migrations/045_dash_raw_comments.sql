-- Migration 045: dash raw 4테이블 테이블·컬럼 COMMENT 소급 (2026-08-19)
--
-- mig 044 를 이미 적용한 설치본(devtools)용 — CREATE IF NOT EXISTS 는 기존 테이블에
-- no-op 이므로 ALTER 로 주석만 부여한다. 신규 설치는 044 자체에 동일 주석이 들어
-- 있어 이 파일이 사실상 no-op (MODIFY 는 동일 정의 재선언이라 무해).
-- ⚠️ MODIFY 정의는 devtools 실측 SHOW CREATE TABLE(0819) 과 자모 단위로 일치 —
--    스키마 변경 없음(주석만). 정의를 고칠 일이 있으면 별도 마이그레이션으로.
-- ⚠️ 044 의 COMMENT 문구와 반드시 동일 유지 (두 파일이 같은 문서 역할).
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/045_dash_raw_comments.sql

ALTER TABLE dash_visibility_daily
  COMMENT='대시보드 raw · 가시성 daily — ID1 검색(SRCH)/ID3 메뉴(GNB) 상품 랭킹. 1행=상품 1개 노출. 하루 1개 batch_id 슬라이스 축적(멱등 교체). 마트 규칙 미적용 전행 보존. 라이터: scripts/export_dash_raw.py (parsed.json 스캔, EYFMT 비연관)',
  MODIFY id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'surrogate PK — 업무 유니크 제약 없음 (전행 보존 원칙)',
  MODIFY base_date    DATE NOT NULL COMMENT '데이터 기준 일자 — OSM 합성은 BQ 조회일(meta.osm_base_date, KST 어제), CNX 는 배치명 파생',
  MODIFY cntry_cd     VARCHAR(4) NOT NULL COMMENT '국가 코드 (ES/FR/IT/NL/SE/PL/CZ)',
  MODIFY rtlr_name    VARCHAR(64) NOT NULL COMMENT '리테일러 순수명 — 국가 접미 없음 (예: MediaMarkt, mig 013 규약)',
  MODIFY page         ENUM('SRCH','GNB') NOT NULL COMMENT 'SRCH=검색 가시성(ID1) / GNB=메뉴 가시성(ID3)',
  MODIFY cat_cd       VARCHAR(8) DEFAULT NULL COMMENT '제품군 코드 (WM/REF/DW 등) — 미상 NULL',
  MODIFY srch_kywd    VARCHAR(255) DEFAULT NULL COMMENT '검색 키워드 — page=SRCH 전용 (GNB 는 NULL)',
  MODIFY menu_path    VARCHAR(512) DEFAULT NULL COMMENT '메뉴 경로 — page=GNB 전용 (OSM 메뉴 경로 / CNX 는 gnb 라벨)',
  MODIFY rnk          INT NOT NULL COMMENT '노출 순위 (1부터)',
  MODIFY brand        VARCHAR(64) DEFAULT NULL COMMENT '수집 브랜드 원문 — LG 여부 판정 전 텍스트 (판정은 마트/리포트 몫)',
  MODIFY product_name VARCHAR(512) DEFAULT NULL COMMENT '상품명 원문',
  MODIFY url          VARCHAR(1024) DEFAULT NULL COMMENT '상품 URL',
  MODIFY is_sponsored TINYINT DEFAULT NULL COMMENT '광고 노출 여부 — OSM PRODUCT_SPN_YN (CNX 수집분은 NULL)',
  MODIFY source       ENUM('osm_bq','cnx') NOT NULL COMMENT '데이터 출처 — osm_bq=BQ 합성 / cnx=자체 크롤',
  MODIFY batch_id     VARCHAR(20) NOT NULL COMMENT '적재 슬라이스 키 — daily 는 실행일 8자리. 같은 batch 재적재 시 DELETE 후 INSERT 교체',
  MODIFY created_at   TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DB 적재 시각';

ALTER TABLE dash_visibility_monthly
  COMMENT='대시보드 raw · 가시성 monthly — 월말 확정 스냅샷. 매월 1일 monthly_dash 가 전월 풀배치 1슬라이스 적재. 스키마·규약은 dash_visibility_daily 와 동일',
  MODIFY id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'surrogate PK — 업무 유니크 제약 없음 (전행 보존 원칙)',
  MODIFY base_date    DATE NOT NULL COMMENT '데이터 기준 일자 — OSM 합성은 BQ 조회일(월 마지막 일자), CNX 는 배치명 파생',
  MODIFY cntry_cd     VARCHAR(4) NOT NULL COMMENT '국가 코드 (ES/FR/IT/NL/SE/PL/CZ)',
  MODIFY rtlr_name    VARCHAR(64) NOT NULL COMMENT '리테일러 순수명 — 국가 접미 없음 (예: MediaMarkt, mig 013 규약)',
  MODIFY page         ENUM('SRCH','GNB') NOT NULL COMMENT 'SRCH=검색 가시성(ID1) / GNB=메뉴 가시성(ID3)',
  MODIFY cat_cd       VARCHAR(8) DEFAULT NULL COMMENT '제품군 코드 (WM/REF/DW 등) — 미상 NULL',
  MODIFY srch_kywd    VARCHAR(255) DEFAULT NULL COMMENT '검색 키워드 — page=SRCH 전용 (GNB 는 NULL)',
  MODIFY menu_path    VARCHAR(512) DEFAULT NULL COMMENT '메뉴 경로 — page=GNB 전용 (OSM 메뉴 경로 / CNX 는 gnb 라벨)',
  MODIFY rnk          INT NOT NULL COMMENT '노출 순위 (1부터)',
  MODIFY brand        VARCHAR(64) DEFAULT NULL COMMENT '수집 브랜드 원문 — LG 여부 판정 전 텍스트 (판정은 마트/리포트 몫)',
  MODIFY product_name VARCHAR(512) DEFAULT NULL COMMENT '상품명 원문',
  MODIFY url          VARCHAR(1024) DEFAULT NULL COMMENT '상품 URL',
  MODIFY is_sponsored TINYINT DEFAULT NULL COMMENT '광고 노출 여부 — OSM PRODUCT_SPN_YN (CNX 수집분은 NULL)',
  MODIFY source       ENUM('osm_bq','cnx') NOT NULL COMMENT '데이터 출처 — osm_bq=BQ 합성 / cnx=자체 크롤',
  MODIFY batch_id     VARCHAR(20) NOT NULL COMMENT '적재 슬라이스 키 — 전월 풀배치 batch. 같은 batch 재적재 시 DELETE 후 INSERT 교체',
  MODIFY created_at   TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DB 적재 시각';

ALTER TABLE dash_conversion_daily
  COMMENT='대시보드 raw · 전환 daily — ID37/38 평점·리뷰 시계열. 1행=PDP 제품 1개 스냅샷. 하루 1개 batch_id 슬라이스 축적(멱등 교체). 라이터: scripts/export_dash_raw.py (parsed.json 스캔, EYFMT 비연관)',
  MODIFY id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'surrogate PK — 업무 유니크 제약 없음 (전행 보존 원칙)',
  MODIFY base_date    DATE NOT NULL COMMENT '데이터 기준 일자 — OSM 합성은 BQ 조회일(meta.osm_base_date, KST 어제), CNX 는 배치명 파생({base}_dMMDD → MMDD)',
  MODIFY cntry_cd     VARCHAR(4) NOT NULL COMMENT '국가 코드 (ES/FR/IT/NL/SE/PL/CZ)',
  MODIFY rtlr_name    VARCHAR(64) NOT NULL COMMENT '리테일러 순수명 — 국가 접미 없음 (예: MediaMarkt, mig 013 규약)',
  MODIFY cat_cd       VARCHAR(8) DEFAULT NULL COMMENT '제품군 코드 (WM/REF/DW 등) — 미상 NULL',
  MODIFY brand        VARCHAR(64) DEFAULT NULL COMMENT '브랜드/제조사 원문 (parsed brand, 없으면 manufacturer 폴백)',
  MODIFY product_name VARCHAR(512) DEFAULT NULL COMMENT '상품명 (parsed title)',
  MODIFY url          VARCHAR(1024) DEFAULT NULL COMMENT 'PDP URL',
  MODIFY mpc          VARCHAR(64) DEFAULT NULL COMMENT 'LG 모델코드 (parsed mpc, 없으면 model 폴백) — OSM 조인 키 축',
  MODIFY rating       DECIMAL(4,2) DEFAULT NULL COMMENT '평점 평균 — 원 스케일 그대로 (rating_scale 로 해석)',
  MODIFY rating_scale TINYINT DEFAULT NULL COMMENT '평점 만점 — OSM=5 고정 (0818 확정), CNX 는 리테일러별 5/10 혼재 (Coolblue 10점제)',
  MODIFY review_count INT DEFAULT NULL COMMENT '리뷰 수',
  MODIFY in_stock     TINYINT DEFAULT NULL COMMENT '재고 플래그 — availability code IN* 이면 1, 아니면 0, 미상 NULL (재고 제외 규칙은 마트 몫)',
  MODIFY source       ENUM('osm_bq','cnx') NOT NULL COMMENT '데이터 출처 — osm_bq=BQ 합성(daily 합성 레코드·monthly 사이드카) / cnx=자체 크롤',
  MODIFY batch_id     VARCHAR(20) NOT NULL COMMENT '적재 슬라이스 키 — daily 는 {당월base}_dMMDD suffix. 같은 batch 재적재 시 DELETE 후 INSERT 교체',
  MODIFY created_at   TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DB 적재 시각';

ALTER TABLE dash_conversion_monthly
  COMMENT='대시보드 raw · 전환 monthly — 월말 확정 스냅샷 + CNX 월간 콘텐츠 지표(video 등 월간 배치에만 존재). 매월 1일 monthly_dash 가 전월 풀배치 1슬라이스 적재. 그 외 규약은 dash_conversion_daily 와 동일',
  MODIFY id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'surrogate PK — 업무 유니크 제약 없음 (전행 보존 원칙)',
  MODIFY base_date    DATE NOT NULL COMMENT '데이터 기준 일자 — OSM 합성은 BQ 조회일(월 마지막 일자), CNX 는 배치명 파생',
  MODIFY cntry_cd     VARCHAR(4) NOT NULL COMMENT '국가 코드 (ES/FR/IT/NL/SE/PL/CZ)',
  MODIFY rtlr_name    VARCHAR(64) NOT NULL COMMENT '리테일러 순수명 — 국가 접미 없음 (예: MediaMarkt, mig 013 규약)',
  MODIFY cat_cd       VARCHAR(8) DEFAULT NULL COMMENT '제품군 코드 (WM/REF/DW 등) — 미상 NULL',
  MODIFY brand        VARCHAR(64) DEFAULT NULL COMMENT '브랜드/제조사 원문 (parsed brand, 없으면 manufacturer 폴백)',
  MODIFY product_name VARCHAR(512) DEFAULT NULL COMMENT '상품명 (parsed title)',
  MODIFY url          VARCHAR(1024) DEFAULT NULL COMMENT 'PDP URL',
  MODIFY mpc          VARCHAR(64) DEFAULT NULL COMMENT 'LG 모델코드 (parsed mpc, 없으면 model 폴백) — OSM 조인 키 축',
  MODIFY rating       DECIMAL(4,2) DEFAULT NULL COMMENT '평점 평균 — 원 스케일 그대로 (rating_scale 로 해석)',
  MODIFY rating_scale TINYINT DEFAULT NULL COMMENT '평점 만점 — OSM=5 고정 (0818 확정), CNX 는 리테일러별 5/10 혼재 (Coolblue 10점제)',
  MODIFY review_count INT DEFAULT NULL COMMENT '리뷰 수',
  MODIFY video_count  INT DEFAULT NULL COMMENT 'CNX 월간 콘텐츠 — 갤러리+본문 영상 개수 (ID34 축). 파서 video 키 부재 시 NULL',
  MODIFY warranty_ok  TINYINT DEFAULT NULL COMMENT 'CNX 월간 — 보증 표기 유무 (ID40/46 축, v2 배선 예정 — 현재 NULL)',
  MODIFY dimension_ok TINYINT DEFAULT NULL COMMENT 'CNX 월간 — 치수 표기 유무 (ID39 축, v2 배선 예정 — 현재 NULL)',
  MODIFY in_stock     TINYINT DEFAULT NULL COMMENT '재고 플래그 — availability code IN* 이면 1, 아니면 0, 미상 NULL (재고 제외 규칙은 마트 몫)',
  MODIFY source       ENUM('osm_bq','cnx') NOT NULL COMMENT '데이터 출처 — osm_bq=BQ 합성(daily 합성 레코드·monthly 사이드카) / cnx=자체 크롤',
  MODIFY batch_id     VARCHAR(20) NOT NULL COMMENT '적재 슬라이스 키 — 전월 풀배치 batch. 같은 batch 재적재 시 DELETE 후 INSERT 교체',
  MODIFY created_at   TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'DB 적재 시각';
