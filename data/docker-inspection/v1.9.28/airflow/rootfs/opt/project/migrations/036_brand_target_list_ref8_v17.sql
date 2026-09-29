-- Migration 036: brand_target_list 참고8 v1.7 전면 재정렬 (2026-07-31)
--
-- 배경 (EY v1.7 명세 260728, 참고8 시트 — 사용자 확정 2026-07-31)
--   참고8 이 LG + 경쟁사(Rank1 Samsung, 단 NL Coolblue 는 Bosch) 2벌 매트릭스로
--   확정되면서 브랜드 트랙을 참고8 정본으로 재정렬한다.
--   · "유무" 는 물리적 페이지 존재가 아니라 **참고9 표준구성 2/7 충족 기반
--     구성 가능 여부** — 페이지가 열려도 EY 가 X 면 크롤 대상이 아니다.
--   · 0721 고객사 시트가 URL 로 등재했던 ECI(전행)·Unieuro 카테고리(필터 URL)·
--     Coolblue 3행·Elgiganten 5행·ME/RTV Brand Page 를 참고8 이 X 로 뒤집음.
--   · ES DW 5브랜드 세트(mig 030, 아이체킹 260625)는 v1.7 "Rank1 단일" 구성으로
--     대체 — BALAY/BEKO/HISENSE/BOSCH 8행 삭제 (사용자 확정 2026-07-31).
--   · Amazon IT 는 store page ID 동일·visitId(세션 파라미터)만 상이 → 변경 없음.
--   실행 전 백업: backup_brand_target_list_20260731.xlsx (101행, 로컬 보관).
--
-- 실행: docker exec -i <mysql> mysql --default-character-set=utf8mb4 \
--         -u<user> -p<pw> lg_clinic < migrations/036_brand_target_list_ref8_v17.sql

-- ── 1) LG 판정 뒤집기 (URL → NULL = X) ──────────────────────────────────────
-- ECI ES: Brand Page + 세탁기/건조기/냉장고/냉동고/DW — 표준구성 2/7 미충족
UPDATE brand_target_list SET brand_url=NULL, notes='EY 참고8 v1.7: 미존재 판정(X) — 표준구성 2/7 미충족'
 WHERE rtlr_name='Elcorteingles_electronica' AND cntry_cd='ES' AND brand='LG';

-- Unieuro IT: 카테고리 전행 — 필터링 URL 은 Brand Category Page 아님 (Brand Page 는 유지)
UPDATE brand_target_list SET brand_url=NULL, notes='EY 참고8 v1.7: 미존재 판정(X) — 필터링으로 카테고리 확인'
 WHERE rtlr_name='Unieuro' AND cntry_cd='IT' AND brand='LG' AND sub_category<>'';

-- Coolblue NL: 세탁기/세탁건조기/냉장냉동고 X, 냉장고 URL 교체(/filter 제거)
UPDATE brand_target_list SET brand_url=NULL, notes='EY 참고8 v1.7: 미존재 판정(X)'
 WHERE rtlr_name='Coolblue' AND cntry_cd='NL' AND brand='LG'
   AND sub_category IN ('세탁기','세탁건조기(일체형)','냉장냉동고');
UPDATE brand_target_list SET brand_url='https://www.coolblue.nl/koelkasten/lg', notes='EY 참고8 v1.7'
 WHERE rtlr_name='Coolblue' AND cntry_cd='NL' AND brand='LG' AND sub_category='냉장고';

-- Elgiganten SE: 세탁기만 유지(세탁+건조 통합 페이지로 URL 교체), 나머지 카테고리 X
UPDATE brand_target_list SET brand_url='https://www.elgiganten.se/brand/lg/lg-tvattmaskin-och-torktumlare', notes='EY 참고8 v1.7'
 WHERE rtlr_name='Elgiganten' AND cntry_cd='SE' AND brand='LG' AND sub_category='세탁기';
UPDATE brand_target_list SET brand_url=NULL, notes='EY 참고8 v1.7: 미존재 판정(X)'
 WHERE rtlr_name='Elgiganten' AND cntry_cd='SE' AND brand='LG'
   AND sub_category IN ('건조기','세탁건조기(일체형)','냉장고','냉동고','냉장냉동고');

-- MediaExpert PL: Brand Page X (CNX 전달 URL 이 MediaMarkt 오등재 — EY 재검토)
UPDATE brand_target_list SET brand_url=NULL, notes='EY 참고8 v1.7: 미존재 판정(X) — 전달 URL MediaMarkt 오등재'
 WHERE rtlr_name='MediaExpert' AND cntry_cd='PL' AND brand='LG' AND sub_category='' AND category='';

-- RtvEuroAgd PL: Brand Page X (검색 URL 은 브랜드 페이지 아님)
UPDATE brand_target_list SET brand_url=NULL, notes='EY 참고8 v1.7: 미존재 판정(X) — 필터링으로 확인'
 WHERE rtlr_name='RtvEuroAgd' AND cntry_cd='PL' AND brand='LG' AND sub_category='' AND category='';

-- Darty FR: 카테고리 6행 공란(미확인) → X 확정 (URL 은 기존 NULL 그대로)
UPDATE brand_target_list SET notes='EY 참고8 v1.7: 미존재 판정(X)'
 WHERE rtlr_name='Darty' AND cntry_cd='FR' AND brand='LG' AND sub_category<>'';

-- ── 2) ES DW 5브랜드 세트 삭제 (mig 030 대체) ────────────────────────────────
DELETE FROM brand_target_list
 WHERE cntry_cd='ES' AND category='DW' AND brand IN ('BOSCH','BALAY','BEKO','HISENSE');

-- ── 3) 경쟁사 트랙 신설 — SAMSUNG (NL Coolblue 만 BOSCH), 93행 ────────────────
-- X 행도 NULL 로 등재 (LG 규약 동일 — 리포트 유무 판정 모집단).
INSERT INTO brand_target_list
    (brand_page_type, rtlr_name, cntry_cd, brand, category, sub_category, brand_url, notes)
VALUES
-- ES · Elcorteingles_electronica — 전행 X
('Brand Page',          'Elcorteingles_electronica', 'ES', 'SAMSUNG', '',    '',                   NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'SAMSUNG', 'WM',  '세탁기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'SAMSUNG', 'WM',  '건조기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'SAMSUNG', 'REF', '냉장고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'SAMSUNG', 'DW',  '식기세척기',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- ES · MediaMarkt
('Brand Page',          'MediaMarkt', 'ES', 'SAMSUNG', '',    '',                   'https://www.mediamarkt.es/es/brand/samsung', 'EY 참고8 v1.7'),
('Brand Category Page', 'MediaMarkt', 'ES', 'SAMSUNG', 'WM',  '세탁기',             'https://www.mediamarkt.es/es/brand/samsung/lavadoras', 'EY 참고8 v1.7'),
('Brand Category Page', 'MediaMarkt', 'ES', 'SAMSUNG', 'WM',  '건조기',             'https://www.mediamarkt.es/es/brand/samsung/secadoras', 'EY 참고8 v1.7'),
('Brand Category Page', 'MediaMarkt', 'ES', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'SAMSUNG', 'REF', '냉장고',             'https://www.mediamarkt.es/es/brand/samsung/frigor%C3%Adficos', 'EY 참고8 v1.7 (시트 원문 인코딩 그대로)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'SAMSUNG', 'DW',  '식기세척기',         'https://www.mediamarkt.es/es/brand/samsung/lavavajillas', 'EY 참고8 v1.7'),
-- FR · Darty — Brand Page 만 O
('Brand Page',          'Darty', 'FR', 'SAMSUNG', '',    '',                   'https://www.darty.com/nav/q/marque-samsung.html', 'EY 참고8 v1.7'),
('Brand Category Page', 'Darty', 'FR', 'SAMSUNG', 'WM',  '세탁기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Darty', 'FR', 'SAMSUNG', 'WM',  '건조기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Darty', 'FR', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Darty', 'FR', 'SAMSUNG', 'REF', '냉장고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Darty', 'FR', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Darty', 'FR', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- FR · Boulanger
('Brand Page',          'Boulanger', 'FR', 'SAMSUNG', '',    '',                   'https://www.boulanger.com/marque/samsung', 'EY 참고8 v1.7'),
('Brand Category Page', 'Boulanger', 'FR', 'SAMSUNG', 'WM',  '세탁기',             'https://www.boulanger.com/c/lave-linge/brand~samsung', 'EY 참고8 v1.7'),
('Brand Category Page', 'Boulanger', 'FR', 'SAMSUNG', 'WM',  '건조기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'SAMSUNG', 'REF', '냉장고',             'https://www.boulanger.com/c/refrigerateur/brand~samsung', 'EY 참고8 v1.7'),
('Brand Category Page', 'Boulanger', 'FR', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- IT · Mediaworld
('Brand Page',          'Mediaworld', 'IT', 'SAMSUNG', '',    '',                   'https://www.mediaworld.it/it/brand/samsung', 'EY 참고8 v1.7'),
('Brand Category Page', 'Mediaworld', 'IT', 'SAMSUNG', 'WM',  '세탁기',             'https://www.mediaworld.it/it/brand/samsung/grandi-elettrodomestici/lavatrici', 'EY 참고8 v1.7'),
('Brand Category Page', 'Mediaworld', 'IT', 'SAMSUNG', 'WM',  '건조기',             'https://www.mediaworld.it/it/brand/samsung/grandi-elettrodomestici/asciugatrici', 'EY 참고8 v1.7'),
('Brand Category Page', 'Mediaworld', 'IT', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'SAMSUNG', 'REF', '냉장고',             'https://www.mediaworld.it/it/brand/samsung/grandi-elettrodomestici/frigoriferi', 'EY 참고8 v1.7'),
('Brand Category Page', 'Mediaworld', 'IT', 'SAMSUNG', 'REF', '냉동고',             'https://www.mediaworld.it/it/brand/samsung/grandi-elettrodomestici/congelatori', 'EY 참고8 v1.7'),
('Brand Category Page', 'Mediaworld', 'IT', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- IT · Amazon
('Brand Page',          'Amazon', 'IT', 'SAMSUNG', '',    '',                   'https://www.amazon.it/stores/page/37219BDE-81D7-45BE-8C88-E2143A37718D?ingress=0&lp_context_query=samsung&visitId=f60fbf43-98f7-4fce-93ff-c85405e46cbe&lp_query=samsung&lp_slot=auto-sparkle-hsa-tetris&store_ref=SB_A10456162L252IRPX8BWN-A10482961I6HV11VWWM6Q&ref_=sbx_s_sparkle_sbtcd_logo', 'EY 참고8 v1.7'),
('Brand Category Page', 'Amazon', 'IT', 'SAMSUNG', 'WM',  '세탁기',             'https://www.amazon.it/stores/page/958908B3-3DF8-46F3-BB1C-3EC93E36F55F?ingress=0&lp_context_query=samsung&visitId=7848beeb-bed1-4394-a847-7a9d7db7c2f7&lp_query=samsung&lp_slot=auto-sparkle-hsa-tetris&store_ref=SB_A10456162L252IRPX8BWN-A10482961I6HV11VWWM6Q&ref_=sbx_s_sparkle_sbtcd_logo', 'EY 참고8 v1.7'),
('Brand Category Page', 'Amazon', 'IT', 'SAMSUNG', 'WM',  '건조기',             'https://www.amazon.it/stores/page/FCF5BF33-8DFF-4334-9EC0-6C5E2A73C35F?ingress=0&lp_context_query=samsung&visitId=7848beeb-bed1-4394-a847-7a9d7db7c2f7&lp_query=samsung&lp_slot=auto-sparkle-hsa-tetris&store_ref=SB_A10456162L252IRPX8BWN-A10482961I6HV11VWWM6Q&ref_=sbx_s_sparkle_sbtcd_logo', 'EY 참고8 v1.7'),
('Brand Category Page', 'Amazon', 'IT', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Amazon', 'IT', 'SAMSUNG', 'REF', '냉장고',             'https://www.amazon.it/stores/page/5A1DEDEC-EE03-4E68-AB53-B6EA0C7B0B2D?ingress=0&lp_context_query=samsung&visitId=f60fbf43-98f7-4fce-93ff-c85405e46cbe&lp_query=samsung&lp_slot=auto-sparkle-hsa-tetris&store_ref=SB_A10456162L252IRPX8BWN-A10482961I6HV11VWWM6Q&ref_=sbx_s_sparkle_sbtcd_logo', 'EY 참고8 v1.7'),
('Brand Category Page', 'Amazon', 'IT', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Amazon', 'IT', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- IT · Unieuro — Brand Page 만 O
('Brand Page',          'Unieuro', 'IT', 'SAMSUNG', '',    '',                   'https://www.unieuro.it/online/Samsung', 'EY 참고8 v1.7'),
('Brand Category Page', 'Unieuro', 'IT', 'SAMSUNG', 'WM',  '세탁기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X) — 필터링으로 카테고리 확인'),
('Brand Category Page', 'Unieuro', 'IT', 'SAMSUNG', 'WM',  '건조기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X) — 필터링으로 카테고리 확인'),
('Brand Category Page', 'Unieuro', 'IT', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X) — 필터링으로 카테고리 확인'),
('Brand Category Page', 'Unieuro', 'IT', 'SAMSUNG', 'REF', '냉장고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X) — 필터링으로 카테고리 확인'),
('Brand Category Page', 'Unieuro', 'IT', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X) — 필터링으로 카테고리 확인'),
('Brand Category Page', 'Unieuro', 'IT', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X) — 필터링으로 카테고리 확인'),
-- NL · Coolblue — 경쟁사 Rank1 을 Bosch 로 확인 (EY note)
('Brand Page',          'Coolblue', 'NL', 'BOSCH', '',    '',                   'https://www.coolblue.nl/bosch', 'EY 참고8 v1.7 — Bosch 로 확인'),
('Brand Category Page', 'Coolblue', 'NL', 'BOSCH', 'WM',  '세탁기',             'https://www.coolblue.nl/wasmachines/bosch', 'EY 참고8 v1.7 — Bosch 로 확인'),
('Brand Category Page', 'Coolblue', 'NL', 'BOSCH', 'WM',  '건조기',             'https://www.coolblue.nl/wasdrogers/bosch', 'EY 참고8 v1.7 — Bosch 로 확인'),
('Brand Category Page', 'Coolblue', 'NL', 'BOSCH', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Coolblue', 'NL', 'BOSCH', 'REF', '냉장고',             'https://www.coolblue.nl/koelkasten/bosch', 'EY 참고8 v1.7 — Bosch 로 확인'),
('Brand Category Page', 'Coolblue', 'NL', 'BOSCH', 'REF', '냉동고',             'https://www.coolblue.nl/vriezers/bosch', 'EY 참고8 v1.7 — Bosch 로 확인'),
('Brand Category Page', 'Coolblue', 'NL', 'BOSCH', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- SE · Elgiganten
('Brand Page',          'Elgiganten', 'SE', 'SAMSUNG', '',    '',                   'https://www.elgiganten.se/brand/samsung', 'EY 참고8 v1.7'),
('Brand Category Page', 'Elgiganten', 'SE', 'SAMSUNG', 'WM',  '세탁기',             'https://www.elgiganten.se/brand/samsung/samsung-vitvaror/samsung-tvatt-och-tork', 'EY 참고8 v1.7'),
('Brand Category Page', 'Elgiganten', 'SE', 'SAMSUNG', 'WM',  '건조기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'SAMSUNG', 'REF', '냉장고',             'https://www.elgiganten.se/brand/samsung/samsung-vitvaror/samsung-kyl-och-frys', 'EY 참고8 v1.7'),
('Brand Category Page', 'Elgiganten', 'SE', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Elgiganten', 'SE', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- PL · MediaExpert — 전행 X
('Brand Page',          'MediaExpert', 'PL', 'SAMSUNG', '',    '',                   NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'MediaExpert', 'PL', 'SAMSUNG', 'WM',  '세탁기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'MediaExpert', 'PL', 'SAMSUNG', 'WM',  '건조기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'MediaExpert', 'PL', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'MediaExpert', 'PL', 'SAMSUNG', 'REF', '냉장고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'MediaExpert', 'PL', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'MediaExpert', 'PL', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- PL · RtvEuroAgd — 전행 X
('Brand Page',          'RtvEuroAgd', 'PL', 'SAMSUNG', '',    '',                   NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'SAMSUNG', 'WM',  '세탁기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'SAMSUNG', 'WM',  '건조기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'SAMSUNG', 'REF', '냉장고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- CZ · Datart — Brand Page 만 O
('Brand Page',          'Datart', 'CZ', 'SAMSUNG', '',    '',                   'https://www.datart.cz/shop/samsung', 'EY 참고8 v1.7'),
('Brand Category Page', 'Datart', 'CZ', 'SAMSUNG', 'WM',  '세탁기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Datart', 'CZ', 'SAMSUNG', 'WM',  '건조기',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Datart', 'CZ', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Datart', 'CZ', 'SAMSUNG', 'REF', '냉장고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Datart', 'CZ', 'SAMSUNG', 'REF', '냉동고',             NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Datart', 'CZ', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
-- CZ · Alza
('Brand Page',          'Alza', 'CZ', 'SAMSUNG', '',    '',                   'https://www.alza.cz/samsung/v1299.htm', 'EY 참고8 v1.7'),
('Brand Category Page', 'Alza', 'CZ', 'SAMSUNG', 'WM',  '세탁기',             'https://www.alza.cz/pracky/samsung/18852774-v1299.htm', 'EY 참고8 v1.7'),
('Brand Category Page', 'Alza', 'CZ', 'SAMSUNG', 'WM',  '건조기',             'https://www.alza.cz/susicky/samsung/18852767-v1299.htm', 'EY 참고8 v1.7'),
('Brand Category Page', 'Alza', 'CZ', 'SAMSUNG', 'WM',  '세탁건조기(일체형)', NULL, 'EY 참고8 v1.7: 미존재 판정(X)'),
('Brand Category Page', 'Alza', 'CZ', 'SAMSUNG', 'REF', '냉장고',             'https://www.alza.cz/lednicky/samsung/18852759-v1299.htm', 'EY 참고8 v1.7'),
('Brand Category Page', 'Alza', 'CZ', 'SAMSUNG', 'REF', '냉동고',             'https://www.alza.cz/mrazaky/samsung/18852764-v1299.htm', 'EY 참고8 v1.7'),
('Brand Category Page', 'Alza', 'CZ', 'SAMSUNG', 'REF', '냉장냉동고',         NULL, 'EY 참고8 v1.7: 미존재 판정(X)');
