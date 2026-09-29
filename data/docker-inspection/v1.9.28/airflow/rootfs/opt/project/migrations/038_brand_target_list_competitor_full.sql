-- Migration 038 (2026-08-04): 경쟁사 Brand Category Page 전수 편입
--
-- 미결 전건 해소 (EY 회신 2026-08-04) — 적용 확정. 편입 기준 = 시트1 단일
--   (경쟁사 전용, NL MM LG 는 미대상). [선행] NL MM 온보딩 코드 배포 후 실행.
-- ⚠️ 적용 시 mysql 클라이언트에 --default-character-set=utf8mb4 필수 —
--   기본(latin1 계열)으로 흘리면 한글 리터럴이 이중 인코딩돼 INSERT 는
--   mojibake 로 들어가고 한글 WHERE 의 DELETE/UPDATE 는 0행 매치로 조용히
--   불발된다 (2026-08-04 devtools 1차 적용 실측 — 148행 재적재로 복구).
--
-- 소스: EY 'LGE_경쟁사 Brand_Brand Category Page_v0.1_260804.xlsx' 1번 시트
--   편입 규칙 = Target(D열) 'O' AND URL(K열) '-' 아님 (EY 메일 지시).
--   X(Target O + URL '-') 행도 NULL 로 등재 (기존 규약 — 유무 판정 모집단).
--   표기 정규화: 리테일러명 내부 표준, '세탁건조기'→'세탁건조기(일체형)',
--   'HAIER '(트레일링 스페이스)→'HAIER'.
--
-- [해소 1 — EY 회신 2026-08-04] Amazon IT SAMSUNG: 시트1 URL 은 오기입 확정.
--   정본 = 참고8 값(세탁기 958908B3 / 건조기 FCF5BF33 / 냉장고 5A1DEDEC,
--   세탁건조기는 미존재 X) — 현행 DB(mig 036)와 동일하므로 변경 없음.
-- [해소 2 — EY 회신 2026-08-04] ES MM SAMSUNG DW: 시트1 기준으로 확정 → 삭제
--   (섹션 2 의 DELETE). 참고3 DW 랭크에 Samsung 없음과도 정합.
-- [선행] NL MediaMarkt 리테일러 온보딩 코드 배포 (retailers/SB_POLICY —
--   2026-08-04 커밋) 후 적용할 것.

-- ── 1) LG 갱신 (참고8 v0.1_260804 — 7/29 업데이트 반영) ──────────────────────
UPDATE brand_target_list SET brand_url='https://www.coolblue.nl/wasmachines/lg', notes='EY 참고8 260804 (7/29 업데이트): O 복원'
 WHERE rtlr_name='Coolblue' AND cntry_cd='NL' AND brand='LG' AND sub_category='세탁기';
UPDATE brand_target_list SET brand_url='https://www.coolblue.nl/was-droogcombinaties/lg', notes='EY 참고8 260804 (7/29 업데이트): O 복원'
 WHERE rtlr_name='Coolblue' AND cntry_cd='NL' AND brand='LG' AND sub_category='세탁건조기(일체형)';
UPDATE brand_target_list SET brand_url='https://www.elgiganten.se/brand/lg/kylskap-lg', notes='EY 참고8 260804 (7/29 업데이트): O 복원'
 WHERE rtlr_name='Elgiganten' AND cntry_cd='SE' AND brand='LG' AND sub_category='냉장고';
-- NL MediaMarkt LG — 등재하지 않음 (EY 회신 2026-08-04: 편입 기준은 시트1
-- 단일, 시트1은 Competitor 전용이라 LG 미대상. URL모음의 홈 URL 은 참고용일 뿐).

-- ── 2) 경쟁사 정정 (시트1 기준 — ES MM SAMSUNG DW 삭제 + URL 신규 발굴/정정) ──
DELETE FROM brand_target_list
 WHERE rtlr_name='MediaMarkt' AND cntry_cd='ES' AND brand='SAMSUNG'
   AND category='DW' AND sub_category='식기세척기';
   -- EY 회신 2026-08-04: 시트1 기준 확정 — 참고8 에만 있던 행 제거
UPDATE brand_target_list SET brand_url='https://www.mediamarkt.es/es/brand/samsung/frigor%C3%ADficos', notes='EY 경쟁사 시트 v0.1_260804' WHERE rtlr_name='MediaMarkt' AND cntry_cd='ES' AND brand='SAMSUNG' AND category='REF' AND sub_category='냉장고';
UPDATE brand_target_list SET brand_url='https://www.coolblue.nl/was-droogcombinaties/bosch', notes='EY 경쟁사 시트 v0.1_260804' WHERE rtlr_name='Coolblue' AND cntry_cd='NL' AND brand='BOSCH' AND category='WM' AND sub_category='세탁건조기(일체형)';
UPDATE brand_target_list SET brand_url='https://www.datart.cz/pracky/samsung', notes='EY 경쟁사 시트 v0.1_260804' WHERE rtlr_name='Datart' AND cntry_cd='CZ' AND brand='SAMSUNG' AND category='WM' AND sub_category='세탁기';
UPDATE brand_target_list SET brand_url='https://www.datart.cz/susicky-38648/filter/v:-4:-835', notes='EY 경쟁사 시트 v0.1_260804' WHERE rtlr_name='Datart' AND cntry_cd='CZ' AND brand='SAMSUNG' AND category='WM' AND sub_category='건조기';
UPDATE brand_target_list SET brand_url='https://www.datart.cz/lednicky/samsung', notes='EY 경쟁사 시트 v0.1_260804' WHERE rtlr_name='Datart' AND cntry_cd='CZ' AND brand='SAMSUNG' AND category='REF' AND sub_category='냉장고';

-- ── 3) 경쟁사 신규 등재 (INSERT 148행 — URL 보유 + X 판정 NULL) ─────────────
INSERT INTO brand_target_list
    (brand_page_type, rtlr_name, cntry_cd, brand, category, sub_category, brand_url, notes)
VALUES
('Brand Category Page', 'Elgiganten', 'SE', 'HISENSE', 'WM', '세탁기', 'https://www.elgiganten.se/brand/hisense/hisense-tvatt', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Elgiganten', 'SE', 'HISENSE', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'HISENSE', 'WM', '건조기', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'HISENSE', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'HISENSE', 'REF', '냉장고', 'https://www.elgiganten.se/brand/hisense/hisense-kyl-och-frys', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Elgiganten', 'SE', 'HISENSE', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'ELECTROLUX', 'WM', '세탁기', 'https://www.elgiganten.se/brand/electrolux/electrolux-tvatt-och-tork', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Elgiganten', 'SE', 'ELECTROLUX', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'ELECTROLUX', 'WM', '건조기', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'ELECTROLUX', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'ELECTROLUX', 'REF', '냉장고', 'https://www.elgiganten.se/brand/electrolux/electrolux-kyl-och-frys', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Elgiganten', 'SE', 'ELECTROLUX', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'BOSCH', 'WM', '세탁기', 'https://www.elgiganten.se/brand/bosch/bosch-vitvaror/bosch-tvattmaskin', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Elgiganten', 'SE', 'BOSCH', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'BOSCH', 'WM', '건조기', 'https://www.elgiganten.se/brand/bosch/bosch-vitvaror/bosch-torktumlare', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Elgiganten', 'SE', 'BOSCH', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'BOSCH', 'REF', '냉장고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'BOSCH', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'HISENSE', 'WM', '세탁기', 'https://www.mediamarkt.es/es/brand/hisense/lavadoras-y-secadoras', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'ES', 'HISENSE', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'HISENSE', 'WM', '건조기', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'HISENSE', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'HISENSE', 'REF', '냉장고', 'https://www.mediamarkt.es/es/brand/hisense/frigorificos-y-congeladores', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'ES', 'HISENSE', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'HISENSE', 'DW', '식기세척기', 'https://www.mediamarkt.es/es/brand/hisense/lavavajillas', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BOSCH', 'WM', '세탁기', 'https://www.mediamarkt.es/es/brand/bosch/lavadoras', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BOSCH', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BOSCH', 'WM', '건조기', 'https://www.mediamarkt.es/es/brand/bosch/secadoras', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BOSCH', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BOSCH', 'REF', '냉장고', 'https://www.mediamarkt.es/es/brand/bosch/frigorificos', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BOSCH', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BOSCH', 'DW', '식기세척기', 'https://www.mediamarkt.es/es/brand/bosch/lavavajillas', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BEKO', 'DW', '식기세척기', 'https://www.mediamarkt.es/es/brand/beko/lavavajillas', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BALAY', 'DW', '식기세척기', 'https://www.mediamarkt.es/es/brand/balay/lavavajillas', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'SAMSUNG', 'WM', '세탁기', 'https://www.mediamarkt.nl/nl/category/samsung-wasmachines-897.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'SAMSUNG', 'WM', '세탁건조기(일체형)', 'https://www.mediamarkt.nl/nl/category/samsung-was-droogcombinaties-1614.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'SAMSUNG', 'WM', '건조기', 'https://www.mediamarkt.nl/nl/category/samsung-wasdrogers-896.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'SAMSUNG', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'NL', 'SAMSUNG', 'REF', '냉장고', 'https://www.mediamarkt.nl/nl/category/samsung-koelkasten-859.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'SAMSUNG', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'NL', 'ETNA', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'NL', 'ETNA', 'REF', '냉장고', 'https://www.mediamarkt.nl/nl/category/etna-koelkasten-990.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'ETNA', 'REF', '냉동고', 'https://www.mediamarkt.nl/nl/category/vriezen-1323.html?filter=brand%3AETNA', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'BOSCH', 'WM', '세탁기', 'https://www.mediamarkt.nl/nl/category/bosch-wasmachines-945.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'BOSCH', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'NL', 'BOSCH', 'WM', '건조기', 'https://www.mediamarkt.nl/nl/category/bosch-wasdrogers-944.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'BOSCH', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'NL', 'BOSCH', 'REF', '냉장고', 'https://www.mediamarkt.nl/nl/category/bosch-koelkasten-940.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'BOSCH', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'NL', 'AEG', 'WM', '세탁기', 'https://www.mediamarkt.nl/nl/category/aeg-wasmachines-924.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'AEG', 'WM', '세탁건조기(일체형)', 'https://www.mediamarkt.nl/nl/category/was-droogcombinaties-634.html?filter=brand%3AAEG', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'MediaMarkt', 'NL', 'AEG', 'WM', '건조기', 'https://www.mediamarkt.nl/nl/category/aeg-wasdrogers-923.html', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Coolblue', 'NL', 'SAMSUNG', 'WM', '세탁기', 'https://www.coolblue.nl/wasmachines/samsung', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Coolblue', 'NL', 'SAMSUNG', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Coolblue', 'NL', 'SAMSUNG', 'WM', '건조기', 'https://www.coolblue.nl/wasdrogers/samsung', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Coolblue', 'NL', 'SAMSUNG', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Coolblue', 'NL', 'SAMSUNG', 'REF', '냉장고', 'https://www.coolblue.nl/koelkasten/samsung', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Coolblue', 'NL', 'SAMSUNG', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Coolblue', 'NL', 'ETNA', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Coolblue', 'NL', 'ETNA', 'REF', '냉장고', 'https://www.coolblue.nl/koelkasten/etna', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Coolblue', 'NL', 'ETNA', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Coolblue', 'NL', 'AEG', 'WM', '세탁기', 'https://www.coolblue.nl/wasmachines/aeg', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Coolblue', 'NL', 'AEG', 'WM', '세탁건조기(일체형)', 'https://www.coolblue.nl/was-droogcombinaties/aeg', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Coolblue', 'NL', 'AEG', 'WM', '건조기', 'https://www.coolblue.nl/wasdrogers/aeg', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Mediaworld', 'IT', 'HISENSE', 'WM', '세탁기', 'https://www.mediaworld.it/it/brand/hisense/lavatrici', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Mediaworld', 'IT', 'HISENSE', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'HISENSE', 'WM', '건조기', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'HISENSE', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'HISENSE', 'REF', '냉장고', 'https://www.mediaworld.it/it/brand/hisense/frigoriferi', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Mediaworld', 'IT', 'HISENSE', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'HAIER', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'HAIER', 'REF', '냉장고', 'https://www.mediaworld.it/it/brand/haier/frigoriferi', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Mediaworld', 'IT', 'HAIER', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'CANDY', 'WM', '세탁기', 'https://www.mediaworld.it/it/brand/candy/lavatrici', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Mediaworld', 'IT', 'CANDY', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'CANDY', 'WM', '건조기', 'https://www.mediaworld.it/it/brand/candy/asciugatrici', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Mediaworld', 'IT', 'BOSCH', 'WM', '세탁기', 'https://www.mediaworld.it/it/brand/bosch/lavatrici', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Mediaworld', 'IT', 'BOSCH', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'BOSCH', 'WM', '건조기', 'https://www.mediaworld.it/it/brand/bosch/asciugatrici', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Mediaworld', 'IT', 'BOSCH', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'BOSCH', 'REF', '냉장고', 'https://www.mediaworld.it/it/brand/bosch/frigoriferi', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Mediaworld', 'IT', 'BOSCH', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Amazon', 'IT', 'HISENSE', 'WM', '세탁기', 'https://www.amazon.it/stores/page/12C13EB9-2F48-4E6E-B59C-E64C0C74644D?ingress=0&lp_context_query=hisense&visitId=53b53ec1-13b9-4f19-8aea-08a688d3034a&lp_query=hisense&lp_slot=auto-sparkle-hsa-tetris&i=aps&store_ref=SB_A0997757TI52ISXPSDQE-A0187789KXIBW53JUK1M&ref_=sbx__sbtcd_cta', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'HISENSE', 'WM', '세탁건조기(일체형)', 'https://www.amazon.it/stores/page/46B50E90-E396-4AA2-9656-DF0CF462DC3C?ingress=0&lp_context_query=hisense&visitId=53b53ec1-13b9-4f19-8aea-08a688d3034a&lp_query=hisense&lp_slot=auto-sparkle-hsa-tetris&i=aps&store_ref=SB_A0997757TI52ISXPSDQE-A0187789KXIBW53JUK1M&ref_=sbx__sbtcd_cta', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'HISENSE', 'WM', '건조기', 'https://www.amazon.it/stores/page/416016B1-E647-4558-9113-BB9200B1E99D?ingress=0&lp_context_query=hisense&visitId=53b53ec1-13b9-4f19-8aea-08a688d3034a&lp_query=hisense&lp_slot=auto-sparkle-hsa-tetris&i=aps&store_ref=SB_A0997757TI52ISXPSDQE-A0187789KXIBW53JUK1M&ref_=sbx__sbtcd_cta', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'HISENSE', 'REF', '냉장냉동고', 'https://www.amazon.it/stores/page/7D3BBE3C-A254-4EC7-B510-D3FCEC5DD866?ingress=0&lp_context_query=hisense&visitId=53b53ec1-13b9-4f19-8aea-08a688d3034a&lp_query=hisense&lp_slot=auto-sparkle-hsa-tetris&i=aps&store_ref=SB_A0997757TI52ISXPSDQE-A0187789KXIBW53JUK1M&ref_=sbx__sbtcd_cta', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'HISENSE', 'REF', '냉장고', 'https://www.amazon.it/stores/page/EDACF759-2774-4DBD-A144-63644FF44232?ingress=0&lp_context_query=hisense&visitId=53b53ec1-13b9-4f19-8aea-08a688d3034a&lp_query=hisense&lp_slot=auto-sparkle-hsa-tetris&i=aps&store_ref=SB_A0997757TI52ISXPSDQE-A0187789KXIBW53JUK1M&ref_=sbx__sbtcd_cta', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'HISENSE', 'REF', '냉동고', 'https://www.amazon.it/stores/page/660258E8-64CC-4017-ABC9-69E03E316455?ingress=0&lp_context_query=hisense&visitId=53b53ec1-13b9-4f19-8aea-08a688d3034a&lp_query=hisense&lp_slot=auto-sparkle-hsa-tetris&i=aps&store_ref=SB_A0997757TI52ISXPSDQE-A0187789KXIBW53JUK1M&ref_=sbx__sbtcd_cta', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'HAIER', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Amazon', 'IT', 'HAIER', 'REF', '냉장고', 'https://www.amazon.it/stores/page/3A6C6882-5C54-466D-8AF3-6E7358934D73?ingress=0&visitId=1661543e-2d9b-4623-b3e2-156b97820943', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'HAIER', 'REF', '냉동고', 'https://www.amazon.it/stores/page/0110EA0D-E325-4EDA-A062-7DC6072F1B72?ingress=0&visitId=1661543e-2d9b-4623-b3e2-156b97820943', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'CANDY', 'WM', '세탁기', 'https://www.amazon.it/stores/page/BE105E08-9382-4237-A680-117A656096C3?ingress=2&lp_context_asin=B0CWS3GC7P&lp_context_query=candy%20refrigerator&visitId=6d7aa2e8-a56b-470d-bb03-078bf79a9b4e&store_ref=bl_ast_dp_brandlogo_sto&ref_=ast_bln', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'CANDY', 'WM', '세탁건조기(일체형)', 'https://www.amazon.it/stores/page/DFA890B8-6EEF-44B0-A5BE-3DD912691DFE?ingress=2&lp_context_asin=B0CWS3GC7P&lp_context_query=candy%20refrigerator&visitId=6d7aa2e8-a56b-470d-bb03-078bf79a9b4e&store_ref=bl_ast_dp_brandlogo_sto&ref_=ast_bln', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'CANDY', 'WM', '건조기', 'https://www.amazon.it/stores/page/51EF5A58-6228-4DD4-BD20-0578576CCFCC?ingress=2&lp_context_asin=B0CWS3GC7P&lp_context_query=candy%20refrigerator&visitId=6d7aa2e8-a56b-470d-bb03-078bf79a9b4e&store_ref=bl_ast_dp_brandlogo_sto&ref_=ast_bln', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'BOSCH', 'WM', '세탁기', 'https://www.amazon.it/stores/page/97A7ED25-73E3-4E69-8868-A7B59C838BC3?ingress=2&lp_context_asin=B0CPYNWHVS&lp_context_query=Bosch%20refrigerator&visitId=d34f529d-a08c-4687-ad54-ce34aa152c90&store_ref=bl_ast_dp_brandlogo_sto&ref_=ast_bln', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'BOSCH', 'WM', '세탁건조기(일체형)', 'https://www.amazon.it/stores/page/87EAB4B9-5D1F-4DC3-BE54-990F6FFEC110?ingress=2&lp_context_asin=B0CPYNWHVS&lp_context_query=Bosch%20refrigerator&visitId=d34f529d-a08c-4687-ad54-ce34aa152c90&store_ref=bl_ast_dp_brandlogo_sto&ref_=ast_bln', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'BOSCH', 'WM', '건조기', 'https://www.amazon.it/stores/page/D3E62031-F40C-4482-BA7A-77BC4062705F?ingress=2&lp_context_asin=B0CPYNWHVS&lp_context_query=Bosch%20refrigerator&visitId=d34f529d-a08c-4687-ad54-ce34aa152c90&store_ref=bl_ast_dp_brandlogo_sto&ref_=ast_bln', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'BOSCH', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Amazon', 'IT', 'BOSCH', 'REF', '냉장고', 'https://www.amazon.it/stores/page/B89E340D-1D09-4192-AF7E-93921736213B?ingress=2&lp_context_asin=B0CPYNWHVS&lp_context_query=Bosch%20refrigerator&visitId=d34f529d-a08c-4687-ad54-ce34aa152c90&store_ref=bl_ast_dp_brandlogo_sto&ref_=ast_bln', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Amazon', 'IT', 'BOSCH', 'REF', '냉동고', 'https://www.amazon.it/stores/page/936956BE-50D6-4D2F-A13D-145D8B1AA873?ingress=2&lp_context_asin=B0CPYNWHVS&lp_context_query=Bosch%20refrigerator&visitId=d34f529d-a08c-4687-ad54-ce34aa152c90&store_ref=bl_ast_dp_brandlogo_sto&ref_=ast_bln', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Boulanger', 'FR', 'HISENSE', 'WM', '세탁기', 'https://www.boulanger.com/c/lave-linge/brand~hisense', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Boulanger', 'FR', 'HISENSE', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'HISENSE', 'WM', '건조기', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'HISENSE', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'HISENSE', 'REF', '냉장고', 'https://www.boulanger.com/c/refrigerateur/brand~hisense', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Boulanger', 'FR', 'HISENSE', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'HAIER', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'HAIER', 'REF', '냉장고', 'https://www.boulanger.com/c/refrigerateur/brand~haier', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Boulanger', 'FR', 'HAIER', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'BOSCH', 'WM', '세탁기', 'https://www.boulanger.com/c/lave-linge/brand~bosch', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Boulanger', 'FR', 'BOSCH', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'BOSCH', 'WM', '건조기', 'https://www.boulanger.com/c/cat-seche-linge/brand~bosch', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'HISENSE', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Datart', 'CZ', 'HISENSE', 'REF', '냉장고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Datart', 'CZ', 'HISENSE', 'REF', '냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Datart', 'CZ', 'GORENJE', 'WM', '세탁기', 'https://www.datart.cz/pracky-s-prednim-plnenim-66210/gorenje', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'GORENJE', 'WM', '세탁건조기(일체형)', 'https://www.datart.cz/pracky-se-susickou-52529/gorenje', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'GORENJE', 'WM', '건조기', 'https://www.datart.cz/susicky-53515/gorenje', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'GORENJE', 'REF', '냉장냉동고', 'https://www.datart.cz/chladnicky-kombinovane-s-mrazakem-dole/gorenje', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'GORENJE', 'REF', '냉장고', 'https://www.datart.cz/americke-chladnicky-51579/gorenje', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'GORENJE', 'REF', '냉동고', 'https://www.datart.cz/mrazaky-suplikove-52744/gorenje', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'BOSCH', 'WM', '세탁기', 'https://www.datart.cz/pracky-s-prednim-plnenim-66210/bosch', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'BOSCH', 'WM', '세탁건조기(일체형)', 'https://www.datart.cz/pracky-se-susickou-52529/bosch', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'BOSCH', 'WM', '건조기', 'https://www.datart.cz/susicky-53515/bosch', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'BOSCH', 'REF', '냉장냉동고', 'https://www.datart.cz/chladnicky-kombinovane-s-mrazakem-dole/bosch', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'BOSCH', 'REF', '냉장고', 'https://www.datart.cz/americke-chladnicky-51579/bosch', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'BOSCH', 'REF', '냉동고', 'https://www.datart.cz/mrazaky-suplikove-52744/bosch', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'AEG', 'WM', '세탁기', 'https://www.datart.cz/pracky-s-prednim-plnenim-66210/aeg', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'AEG', 'WM', '세탁건조기(일체형)', 'https://www.datart.cz/pracky-se-susickou-52529/aeg', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Datart', 'CZ', 'AEG', 'WM', '건조기', 'https://www.datart.cz/susicky-53515/aeg', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'HISENSE', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Alza', 'CZ', 'HISENSE', 'REF', '냉장고', 'https://www.alza.cz/lednicky/hisense/18852759-v6822.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'HISENSE', 'REF', '냉동고', 'https://www.alza.cz/mrazaky/hisense/18852764-v6822.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'GORENJE', 'WM', '세탁기', 'https://www.alza.cz/pracky/gorenje/18852774-v2156.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'GORENJE', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Alza', 'CZ', 'GORENJE', 'WM', '건조기', 'https://www.alza.cz/susicky/gorenje/18852767-v2156.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'GORENJE', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Alza', 'CZ', 'GORENJE', 'REF', '냉장고', 'https://www.alza.cz/lednicky/gorenje/18852759-v2156.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'GORENJE', 'REF', '냉동고', 'https://www.alza.cz/mrazaky/gorenje/18852764-v2156.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'BOSCH', 'WM', '세탁기', 'https://www.alza.cz/automatic-washing-machines/bosch/18852774-v1877.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'BOSCH', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Alza', 'CZ', 'BOSCH', 'WM', '건조기', 'https://www.alza.cz/tumble-dryers/bosch/18852767-v1877.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'BOSCH', 'REF', '냉장냉동고', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Alza', 'CZ', 'BOSCH', 'REF', '냉장고', 'https://www.alza.cz/refrigerators/bosch/18852759-v1877.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'BOSCH', 'REF', '냉동고', 'https://www.alza.cz/freezers/bosch/18852764-v1877.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'AEG', 'WM', '세탁기', 'https://www.alza.cz/pracky/aeg/18852774-v1742.htm', 'EY 경쟁사 시트 v0.1_260804'),
('Brand Category Page', 'Alza', 'CZ', 'AEG', 'WM', '세탁건조기(일체형)', NULL, 'EY 경쟁사 시트 v0.1_260804: 미존재 판정(X)'),
('Brand Category Page', 'Alza', 'CZ', 'AEG', 'WM', '건조기', 'https://www.alza.cz/susicky/aeg/18852767-v1742.htm', 'EY 경쟁사 시트 v0.1_260804');

-- ── 4) [해소] Amazon IT SAMSUNG — EY 회신 2026-08-04: 시트1 URL(045E563A 등
--   LG 스토어 ID) 오기입 확정. 정본은 참고8 값 = 현행 DB 그대로 → 실행문 없음.
