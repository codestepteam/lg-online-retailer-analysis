-- Migration 032: gnb_keyword_map v4 재구축 (dataset/gnb_dataset2.xlsx)
--
-- 배경 (2026-07-21)
--   사용자 제공 gnb_dataset2.xlsx(18행)로 gnb_keyword_map 을 재시딩한다.
--   기존 v3(mig 018, 10행: ES ECI·MediaMarkt / IT Mediaworld / SE Elgiganten)에
--   FR(Darty·Boulanger) / NL(Coolblue) / PL(MediaExpert) 을 추가 — 총 18행.
--   PL 은 home/plp 리테일러 롤백(MediaExpert, mig 031)에 맞춰 RTLR_NAME=MediaExpert.
--
--   컬럼 매핑: 국가명→cntry_cd, 리테일러 표기→RTLR_NAME(내부명), 카테고리
--   W/M→WM·REF·DW→cat_cd, cat_sub_cd 는 WASH/FRFR/DISH 파생. keyword=dataset
--   search_keyword(표시용 라벨 — 조인 미사용), gnb_url=dataset 원본(브랜드 필터 포함).
--   ⚠️ Coolblue 는 dataset URL 에 브랜드 파라미터가 없어 카테고리 전체 리스트다
--      (ID3 경쟁사 필터 산식과 모수 차이 — note 로 명시, URL 확보 시 UPSERT).
--
--   기존 v3 10행은 gnb_keyword_map_backup_v3 에 보존.
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/032_gnb_keyword_map_v4_dataset2.sql

-- 1) 백업 (v3 — 멱등)
CREATE TABLE IF NOT EXISTS gnb_keyword_map_backup_v3 LIKE gnb_keyword_map;
INSERT INTO gnb_keyword_map_backup_v3
  SELECT * FROM gnb_keyword_map
  WHERE NOT EXISTS (SELECT 1 FROM gnb_keyword_map_backup_v3);

-- 2) 본 테이블 초기화
TRUNCATE TABLE gnb_keyword_map;

-- 3) dataset2 v4 시딩 18건
INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note) VALUES
('ES','Elcorteingles_electronica','WM','WASH','lavadora','Lavadoras',
 'https://www.elcorteingles.es/electrodomesticos/lavadoras/brand::Bosch,,Samsung,,LG,,Hisense/','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('ES','Elcorteingles_electronica','REF','FRFR','Frigoríficos','Frigoríficos y neveras',
 'https://www.elcorteingles.es/electrodomesticos/frigorificos-y-neveras/brand::Samsung,,Bosch,,LG,,Hisense/','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('ES','Elcorteingles_electronica','DW','DISH','lavavajillas','Lavavajillas',
 'https://www.elcorteingles.es/electrodomesticos/lavavajillas/brand::Bosch,,Samsung,,Beko,,LG,,Balay/','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('ES','MediaMarkt','WM','WASH','Lavadoras','Lavadoras',
 'https://www.mediamarkt.es/es/category/lavadoras-671.html?brand=HISENSE%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('ES','MediaMarkt','REF','FRFR','Frigoríficos','Frigoríficos',
 'https://www.mediamarkt.es/es/category/frigor%C3%ADficos-554.html?brand=HISENSE%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('ES','MediaMarkt','DW','DISH','Lavavajillas','Lavavajillas',
 'https://www.mediamarkt.es/es/category/lavavajillas-660.html?brand=HISENSE%20OR%20BEKO%20OR%20LG%20OR%20BOSCH%20OR%20BALAY','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('FR','Darty','WM','WASH','Lave-linge','Lave-linge',
 'https://www.darty.com/nav/extra/list?cat=12428&m=BOSCH-LG-HISEN-SAMSU','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('FR','Darty','REF','FRFR','Réfrigérateur','Réfrigérateur',
 'https://www.darty.com/nav/extra/list?cat=23561&m=HAIER-LG-HISEN-SAMSU','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('FR','Boulanger','WM','WASH','Lave-linge','Lave-linge',
 'https://www.boulanger.com/c/nav-filtre/lave-linge?brand%7Ebosch%7Cbrand%7Ehisense%7Cbrand%7Elg%7Cbrand%7Esamsung=','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('FR','Boulanger','REF','FRFR','Réfrigérateur','Réfrigérateur',
 'https://www.boulanger.com/c/nav-filtre/refrigerateur?brand~haier|brand~hisense|brand~lg|brand~samsung','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('IT','Mediaworld','WM','WASH','lavatrici','Lavatrici',
 'https://www.mediaworld.it/it/category/lavatrici-6001.html?brand=HISENSE%20OR%20HAIER%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('IT','Mediaworld','REF','FRFR','Frigoriferi','Frigoriferi',
 'https://www.mediaworld.it/it/category/frigoriferi-6004.html?brand=HISENSE%20OR%20HAIER%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('NL','Coolblue','WM','WASH','Wasmachines','Wasmachines',
 'https://www.coolblue.nl/wasmachines/filter','CONFIRMED','dataset2 gnb_url (브랜드 필터 없음 — 카테고리 전체 리스트)'),
('NL','Coolblue','REF','FRFR','Koelkasten','Koelkasten',
 'https://www.coolblue.nl/koelkasten/filter','CONFIRMED','dataset2 gnb_url (브랜드 필터 없음 — 카테고리 전체 리스트)'),
('SE','Elgiganten','WM','WASH','Tvättmaskin','Tvättmaskin',
 'https://www.elgiganten.se/vitvaror/tvatt-tork/tvattmaskin?1%7Cbrand%5B%5D=Bosch&1%7Cbrand%5B%5D=Electrolux&1%7Cbrand%5B%5D=LG&1%7Cbrand%5B%5D=Samsung','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('SE','Elgiganten','REF','FRFR','Kylskåp','Kylskåp',
 'https://www.elgiganten.se/vitvaror/kyl-frys/kylskap?1%7Cbrand%5B%5D=Electrolux&1%7Cbrand%5B%5D=Bosch&1%7Cbrand%5B%5D=LG&1%7Cbrand%5B%5D=Hisense&1%7Cbrand%5B%5D=Samsung','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('PL','MediaExpert','WM','WASH','Pralki','Pralki',
 'https://www.mediaexpert.pl/agd/pralki-i-suszarki/pralki/bosch.lg.samsung.electrolux.hisense','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)'),
('PL','MediaExpert','REF','FRFR','Lodówki','Lodówki',
 'https://www.mediaexpert.pl/agd/lodowki-i-zamrazarki/lodowki/popularne-serie_lg.samsung.hisense.bosch.haier','CONFIRMED','dataset2 gnb_url (브랜드 필터 포함)');
