-- Migration 040: gnb_keyword_map — v1.8 참고 12(0807) 신규 6행 추가
--
-- 배경 (2026-08-10)
--   v1.8 참고 12(ID3 GNB 카테고리 URL, 28행) 대조 결과 현행 22행 중 20행 기커버.
--   신규 6행 = IT Unieuro(W/M·REF) / NL MediaMarkt(W/M·REF) / PL RtvEuroAgd(W/M·REF).
--   Coolblue 2행은 현행(필터 진입형) 유지 — 참고 12 와 동일 카테고리의 URL 변형.
--   ⚠️ 신규 6행은 참고 12 원본 그대로 **무필터 순수 카테고리 URL** — 기존 18행의
--      브랜드 필터 프리셋과 형태가 다르다 (mig 032 Coolblue 주석과 동일 상황).
--   백업: gnb_keyword_map_backup_v4 (적용 전 22행 보존). 멱등: gnb_url 중복 방지.
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/040_gnb_keyword_map_ref12_additions.sql

CREATE TABLE IF NOT EXISTS gnb_keyword_map_backup_v4 LIKE gnb_keyword_map;
INSERT INTO gnb_keyword_map_backup_v4
  SELECT * FROM gnb_keyword_map
  WHERE NOT EXISTS (SELECT 1 FROM gnb_keyword_map_backup_v4);

INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note)
SELECT 'IT','Unieuro','WM','WASH','Lavatrici','Lavatrici',
       'https://www.unieuro.it/online/Piccoli-e-Grandi-Elettrodomestici/Grandi-Elettrodomestici/Lavatrici','CONFIRMED','v1.8 참고 12 (0807) — 무필터 순수 카테고리 URL'
FROM DUAL WHERE NOT EXISTS (
  SELECT 1 FROM gnb_keyword_map WHERE gnb_url = 'https://www.unieuro.it/online/Piccoli-e-Grandi-Elettrodomestici/Grandi-Elettrodomestici/Lavatrici');
INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note)
SELECT 'IT','Unieuro','REF','FRFR','Frigoriferi','Frigoriferi',
       'https://www.unieuro.it/online/Piccoli-e-Grandi-Elettrodomestici/Grandi-Elettrodomestici/Frigoriferi','CONFIRMED','v1.8 참고 12 (0807) — 무필터 순수 카테고리 URL'
FROM DUAL WHERE NOT EXISTS (
  SELECT 1 FROM gnb_keyword_map WHERE gnb_url = 'https://www.unieuro.it/online/Piccoli-e-Grandi-Elettrodomestici/Grandi-Elettrodomestici/Frigoriferi');
INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note)
SELECT 'NL','MediaMarkt','WM','WASH','Wasmachines','Wasmachines',
       'https://www.mediamarkt.nl/nl/category/wasmachines-1283.html','CONFIRMED','v1.8 참고 12 (0807) — 무필터 순수 카테고리 URL'
FROM DUAL WHERE NOT EXISTS (
  SELECT 1 FROM gnb_keyword_map WHERE gnb_url = 'https://www.mediamarkt.nl/nl/category/wasmachines-1283.html');
INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note)
SELECT 'NL','MediaMarkt','REF','FRFR','Koelkasten','Koelkasten',
       'https://www.mediamarkt.nl/nl/category/koelkasten-1304.html','CONFIRMED','v1.8 참고 12 (0807) — 무필터 순수 카테고리 URL'
FROM DUAL WHERE NOT EXISTS (
  SELECT 1 FROM gnb_keyword_map WHERE gnb_url = 'https://www.mediamarkt.nl/nl/category/koelkasten-1304.html');
INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note)
SELECT 'PL','RtvEuroAgd','WM','WASH','Pralki','Pralki',
       'https://www.euro.com.pl/pralki.bhtml','CONFIRMED','v1.8 참고 12 (0807) — 무필터 순수 카테고리 URL'
FROM DUAL WHERE NOT EXISTS (
  SELECT 1 FROM gnb_keyword_map WHERE gnb_url = 'https://www.euro.com.pl/pralki.bhtml');
INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note)
SELECT 'PL','RtvEuroAgd','REF','FRFR','Lodówki','Lodówki',
       'https://www.euro.com.pl/lodowki.bhtml','CONFIRMED','v1.8 참고 12 (0807) — 무필터 순수 카테고리 URL'
FROM DUAL WHERE NOT EXISTS (
  SELECT 1 FROM gnb_keyword_map WHERE gnb_url = 'https://www.euro.com.pl/lodowki.bhtml');
