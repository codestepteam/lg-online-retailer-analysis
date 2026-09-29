-- Migration 017: gnb_keyword_map v2 재시딩 (home_keywords v2 대표어 기준)
--
-- 배경 (2026-07-09):
--   home_keywords v2(migrations/015·016) 에서 kywd_type='category' 키워드가
--   세부 키워드("frigorifero side by side" 등)에서 **일반 대표어**("frigorifero" 등)로
--   바뀌었다. 기존 gnb_keyword_map 36행은 전부 v1 세부 키워드 기준이라
--   load_home_gnb_targets() 의 (rtlr_name, cntry_cd, keyword) 조인이 0행 → ID3 단절.
--   → 기존 행은 백업 테이블로 보존하고, 본 테이블은 대표어 23건으로 재시딩.
--
-- URL 출처 (status 로 구분):
--   · CONFIRMED — 홈 크롤 HTML(data/20260708_2/home) GNB 메뉴에서 실측 추출,
--     또는 v1 map 에서 검증된 URL 재사용.
--   · RECAPTURE — 슬러그/제품 URL 트리에서 유도한 후보. --pages gnb 크롤로 실측 후
--     CONFIRMED 승격 필요. gnb_url IS NULL 행은 URL 자체 미상(크롤로 확보).
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/017_gnb_keyword_map_v2_reseed.sql

-- 1) 백업 (스키마+데이터 그대로 보존)
CREATE TABLE IF NOT EXISTS gnb_keyword_map_backup_v1 LIKE gnb_keyword_map;
INSERT INTO gnb_keyword_map_backup_v1 SELECT * FROM gnb_keyword_map;

-- 2) 본 테이블 초기화
TRUNCATE TABLE gnb_keyword_map;

-- 3) v2 대표어 23건 시딩
--    keyword 는 home_keywords.loc_srch_kywd_info 와 문자열 완전일치 (조인 키)
INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note) VALUES
-- ES · Elcorteingles_electronica — 홈 오퍼링크 슬러그 기반 후보
('ES','Elcorteingles_electronica','REF','FRFR','refrigerador','Frigoríficos y neveras',
 'https://www.elcorteingles.es/electrodomesticos/frigorificos-y-neveras/','CONFIRMED','홈 오퍼링크 슬러그 유도 → 20260709_gnb 크롤 실측 리스팅 확인'),
('ES','Elcorteingles_electronica','WM','WASH','lavadora','Lavadoras',
 'https://www.elcorteingles.es/electrodomesticos/lavadoras/','CONFIRMED','홈 오퍼링크 슬러그 유도 → 20260709_gnb 크롤 실측 리스팅 확인'),
('ES','Elcorteingles_electronica','DW','DISH','Lavavajillas','Lavavajillas',
 'https://www.elcorteingles.es/electrodomesticos/lavavajillas/','CONFIRMED','슬러그 추정 → 20260709_gnb 크롤 실측 리스팅 확인'),
-- ES · MediaMarkt — 20260708_2 홈 HTML 은 1뎁스만 노출이나, 20260622 배치 홈 HTML 에
--   2뎁스 플라이아웃이 포함돼 있어 거기서 실측 (frigoríficos-554, lavadoras-671)
('ES','MediaMarkt','REF','FRFR','refrigerador','Frigoríficos',
 'https://www.mediamarkt.es/es/category/frigor%C3%ADficos-554.html','CONFIRMED','홈 GNB 실측 (20260622 배치 홈 HTML)'),
('ES','MediaMarkt','WM','WASH','lavadora','Lavadoras',
 'https://www.mediamarkt.es/es/category/lavadoras-671.html','CONFIRMED','홈 GNB 실측 (20260622 배치 홈 HTML)'),
('ES','MediaMarkt','DW','DISH','Lavavajillas','Lavavajillas',
 'https://www.mediamarkt.es/es/category/lavavajillas-660.html','CONFIRMED','v1 map 검증 URL 재사용'),
-- FR · Boulanger — 홈 GNB 실측 (20260708_2)
('FR','Boulanger','REF','FRFR','Réfrigérateur','Réfrigérateur',
 'https://www.boulanger.com/c/refrigerateur','CONFIRMED','홈 GNB 실측 (20260708_2)'),
('FR','Boulanger','WM','WASH','lave-linge','Lave-linge',
 'https://www.boulanger.com/c/lave-linge','CONFIRMED','홈 GNB 실측 (20260708_2)'),
-- FR · Darty — 홈 GNB 실측, #dartyclic 트래킹 제거
('FR','Darty','REF','FRFR','Réfrigérateur','Réfrigérateur',
 'https://www.darty.com/nav/achat/gros_electromenager/refrigerateurs/index.html','CONFIRMED','홈 GNB 실측 — #dartyclic 제거'),
('FR','Darty','WM','WASH','lave-linge','Lave-linge',
 'https://www.darty.com/nav/achat/gros_electromenager/lave-linge/index.html','CONFIRMED','홈 GNB 실측 — #dartyclic 제거'),
-- IT · Amazon — 노드 URL (frigoriferi 는 v1 재사용, lavatrici 는 v1 gnb 크롤 서브넷 링크)
('IT','Amazon','REF','FRFR','frigorifero','Frigoriferi',
 'https://www.amazon.it/b/?node=14567265031','CONFIRMED','v1 map 검증 URL 재사용'),
('IT','Amazon','WM','WASH','lavatrice','Lavatrici',
 'https://www.amazon.it/b/?node=5495940031','CONFIRMED','v1 gnb 크롤 서브내비 링크 → 20260709_gnb 크롤 실측 리스팅 확인'),
-- IT · Mediaworld — 홈 GNB 실측 (20260708_2)
('IT','Mediaworld','REF','FRFR','frigorifero','Frigoriferi',
 'https://www.mediaworld.it/it/category/frigoriferi-6004.html','CONFIRMED','홈 GNB 실측 (20260708_2)'),
('IT','Mediaworld','WM','WASH','lavatrice','Lavatrici',
 'https://www.mediaworld.it/it/category/lavatrici-6001.html','CONFIRMED','홈 GNB 실측 (20260708_2)'),
('IT','Mediaworld','DRY','DRYR','Asciugatrici','Asciugatrici',
 'https://www.mediaworld.it/it/category/asciugatrici-600201.html','CONFIRMED','홈 GNB 실측 — asciugatura-6002(상위) 아닌 건조기 노드'),
-- IT · Unieuro — PDP 브레드크럼 실측 경로 (GNB 트리:
--   Piccoli e Grandi Elettrodomestici > Grandi Elettrodomestici > 카테고리).
--   /online/{카테고리} 단축형은 빈 페이지("Ops, abbiamo cercato...") — 사용 금지.
('IT','Unieuro','REF','FRFR','frigorifero','Frigoriferi',
 'https://www.unieuro.it/online/Piccoli-e-Grandi-Elettrodomestici/Grandi-Elettrodomestici/Frigoriferi','CONFIRMED','PDP 브레드크럼 실측 — /online/Frigoriferi 단축형은 빈 페이지'),
('IT','Unieuro','WM','WASH','lavatrice','Lavatrici',
 'https://www.unieuro.it/online/Piccoli-e-Grandi-Elettrodomestici/Grandi-Elettrodomestici/Lavatrici','CONFIRMED','PDP 브레드크럼 실측 — /online/Lavatrici 단축형은 빈 페이지'),
('IT','Unieuro','DRY','DRYR','Asciugatrici','Asciugatrici',
 'https://www.unieuro.it/online/Piccoli-e-Grandi-Elettrodomestici/Grandi-Elettrodomestici/Asciugatrici','CONFIRMED','PDP 브레드크럼 실측 + GNB 수동 진입 확인 (2026-07-09)'),
-- NL · Coolblue — 홈 GNB 실측 + v1 map 일치
('NL','Coolblue','REF','FRFR','koelkast','Koelkasten',
 'https://www.coolblue.nl/koelkasten','CONFIRMED','홈 GNB 실측 (v1 map 일치)'),
('NL','Coolblue','WM','WASH','wasmachine','Wasmachines',
 'https://www.coolblue.nl/wasmachines','CONFIRMED','홈 GNB 실측 (v1 map 일치)'),
-- SE · Elgiganten — v1 gnb 크롤 하위경로/제품 URL 트리에서 유도
('SE','Elgiganten','REF','FRFR','Kylskåp','Kylskåp',
 'https://www.elgiganten.se/vitvaror/kyl-frys/kylskap','CONFIRMED','gnb 크롤 하위경로 유도 → 20260709_gnb 크롤 실측 리스팅 확인'),
('SE','Elgiganten','WM','WASH','Tvättmaskin','Tvättmaskin',
 'https://www.elgiganten.se/vitvaror/tvatt-tork/tvattmaskin','CONFIRMED','제품 URL 트리 유도 → 20260709_gnb 크롤 실측 리스팅 확인'),
('SE','Elgiganten','DRY','DRYR','Torktumlare','Torktumlare',
 'https://www.elgiganten.se/vitvaror/tvatt-tork/torktumlare-torkskap/torktumlare','CONFIRMED','제품 URL 트리 유도 → 20260709_gnb 크롤 실측 리스팅 확인');
