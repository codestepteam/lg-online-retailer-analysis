-- Migration 018: gnb_keyword_map v3 재구축 (ID3 재정의 — GNB Top20 자사 노출 개수)
--
-- 배경 (2026-07-20):
--   ID3 를 '검색 vs GNB 랭킹 동일성(keyword 조인)'에서 'GNB 카테고리 페이지 Top20
--   내 자사(LG) 노출 개수'(ID1/ID2 동일 산식)로 재정의. keyword 조인이 사라져
--   load_home_gnb_targets 의 home_keywords INNER JOIN 을 제거하므로, keyword 컬럼은
--   조인 키가 아니라 **표시용 라벨(dataset search_keyword)**로 repurpose 한다.
--
--   소스: dataset/gnb_dataset.xlsx (사용자 제공) — 브랜드 필터가 걸린 GNB URL.
--   LG=자사, 나머지=경쟁사 → 필터된 Top20 의 LG 개수 = 경쟁 구도 내 노출.
--   (ID1/ID2 는 무필터 검색 리스트, ID3 는 경쟁사 필터 리스트 — 산출 양식 동일,
--    측정 모수만 다름.)
--
--   커버리지: dataset 4 리테일러(ECI·MediaMarkt·Mediaworld·Elgiganten) 10행만.
--   나머지(FR Boulanger·Darty, NL Coolblue, IT Amazon·Unieuro 등)는 브랜드 필터
--   GNB URL 확보 시 추후 UPSERT. 기존 v2 23행은 gnb_keyword_map_backup_v2 에 보존.
--
--   gnb_url = dataset 원본(브랜드 패싯 포함) 그대로. gnb_label = 리테일러 실제 GNB
--   노드명(v2 재사용). cat_cd 는 W/M→WM 정규화, cat_sub_cd 는 대분류에서 파생.
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/018_gnb_keyword_map_v3_dataset.sql

-- 1) 백업 (v2 — 별도 스크립트로 이미 생성됨. 멱등 보장용 재확인)
CREATE TABLE IF NOT EXISTS gnb_keyword_map_backup_v2 LIKE gnb_keyword_map;
INSERT INTO gnb_keyword_map_backup_v2
  SELECT * FROM gnb_keyword_map
  WHERE NOT EXISTS (SELECT 1 FROM gnb_keyword_map_backup_v2);

-- 2) 본 테이블 초기화
TRUNCATE TABLE gnb_keyword_map;

-- 3) dataset v3 시딩 10건
--    keyword = dataset search_keyword (표시용 라벨 — 조인 미사용)
--    gnb_url = dataset 원본(브랜드 필터 포함)
INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note) VALUES
-- ES · Elcorteingles (ECI)
('ES','Elcorteingles_electronica','WM','WASH','lavadora','Lavadoras',
 'https://www.elcorteingles.es/electrodomesticos/lavadoras/brand::Bosch,,Samsung,,LG,,Hisense/','CONFIRMED','dataset gnb_url (브랜드 필터: Bosch/Samsung/LG/Hisense)'),
('ES','Elcorteingles_electronica','REF','FRFR','Frigoríficos','Frigoríficos y neveras',
 'https://www.elcorteingles.es/electrodomesticos/frigorificos-y-neveras/brand::Samsung,,Bosch,,LG,,Hisense/','CONFIRMED','dataset gnb_url (브랜드 필터: Samsung/Bosch/LG/Hisense)'),
('ES','Elcorteingles_electronica','DW','DISH','lavavajillas','Lavavajillas',
 'https://www.elcorteingles.es/electrodomesticos/lavavajillas/brand::Bosch,,Samsung,,Beko,,LG,,Balay/','CONFIRMED','dataset gnb_url (브랜드 필터: Bosch/Samsung/Beko/LG/Balay)'),
-- ES · MediaMarkt
('ES','MediaMarkt','WM','WASH','Lavadoras','Lavadoras',
 'https://www.mediamarkt.es/es/category/lavadoras-671.html?brand=HISENSE%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG','CONFIRMED','dataset gnb_url (브랜드 필터: Hisense/Bosch/LG/Samsung)'),
('ES','MediaMarkt','REF','FRFR','Frigoríficos','Frigoríficos',
 'https://www.mediamarkt.es/es/category/frigor%C3%ADficos-554.html?brand=HISENSE%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG','CONFIRMED','dataset gnb_url (브랜드 필터: Hisense/Bosch/LG/Samsung)'),
('ES','MediaMarkt','DW','DISH','Lavavajillas','Lavavajillas',
 'https://www.mediamarkt.es/es/category/lavavajillas-660.html?brand=HISENSE%20OR%20BEKO%20OR%20LG%20OR%20BOSCH%20OR%20BALAY','CONFIRMED','dataset gnb_url (브랜드 필터: Hisense/Beko/LG/Bosch/Balay)'),
-- IT · Mediaworld
('IT','Mediaworld','WM','WASH','lavatrici','Lavatrici',
 'https://www.mediaworld.it/it/category/lavatrici-6001.html?brand=HISENSE%20OR%20HAIER%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG','CONFIRMED','dataset gnb_url (브랜드 필터: Hisense/Haier/Bosch/LG/Samsung)'),
('IT','Mediaworld','REF','FRFR','Frigoriferi','Frigoriferi',
 'https://www.mediaworld.it/it/category/frigoriferi-6004.html?brand=HISENSE%20OR%20HAIER%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG','CONFIRMED','dataset gnb_url (브랜드 필터: Hisense/Haier/Bosch/LG/Samsung)'),
-- SE · Elgiganten
('SE','Elgiganten','WM','WASH','Tvättmaskin','Tvättmaskin',
 'https://www.elgiganten.se/vitvaror/tvatt-tork/tvattmaskin?1%7Cbrand%5B%5D=Bosch&1%7Cbrand%5B%5D=Electrolux&1%7Cbrand%5B%5D=LG&1%7Cbrand%5B%5D=Samsung','CONFIRMED','dataset gnb_url (브랜드 필터: Bosch/Electrolux/LG/Samsung)'),
('SE','Elgiganten','REF','FRFR','Kylskåp','Kylskåp',
 'https://www.elgiganten.se/vitvaror/kyl-frys/kylskap?1%7Cbrand%5B%5D=Electrolux&1%7Cbrand%5B%5D=Bosch&1%7Cbrand%5B%5D=LG&1%7Cbrand%5B%5D=Hisense&1%7Cbrand%5B%5D=Samsung','CONFIRMED','dataset gnb_url (브랜드 필터: Electrolux/Bosch/LG/Hisense/Samsung)');
