-- Migration 028: brand_target_list 개편 — category 그룹화 + sub_category(한글) 신설
--
-- 배경 (2026-07-21 고객사 시트 확정)
--   기존 category 는 WM/DR/WD/REF/FZ/FF/DW flat 코드였다. 고객사 시트가
--   [W/M]·[REF] 2개 제품군 그룹 × 한글 하위 카테고리(세탁기/건조기/세탁건조기
--   (일체형)/냉장고/냉동고/냉장냉동고) 매트릭스로 재편됨에 따라:
--     · category     = 제품군 그룹 코드 (''=브랜드 메인 / WM / REF)
--     · sub_category = 하위 카테고리 **한글 정본** (시트·리포트 노출값 그대로,
--                      ''=브랜드 메인. 내부 코드는 core/naming.brand_sub_code 파생)
--   DW(식기세척기)는 브랜드 트랙에서 제외 (0721 시트에 행 없음 — pdp 트랙만 유지).
--   PL 브랜드 트랙은 MediaMarkt(임시 세트) → MediaExpert + RtvEuroAgd 재정립.
--   CZ(Datart/Alza)는 시트에 없으나 0720 온보딩분 복원 (2026-07-21 사용자 확정).
--
--   전체 삭제 후 재시딩 — 삭제 전 원본은 backup_brand_target_list_20260721.csv
--   (93행, 로컬 보관). X=고객사 부재 판정, 공란=미확인 — 둘 다 brand_url NULL,
--   notes 로 구분.
--
-- 실행: docker exec -i <mysql> mysql --default-character-set=utf8mb4 \
--         -u<user> -p<pw> lg_clinic < migrations/028_brand_target_list_sub_category.sql

-- ── 1) sub_category 컬럼 신설 + UNIQUE 갱신 ──────────────────────────────────
ALTER TABLE brand_target_list
    ADD COLUMN sub_category VARCHAR(32) NOT NULL DEFAULT ''
        COMMENT '하위 카테고리 한글 정본 (세탁기/건조기/세탁건조기(일체형)/냉장고/냉동고/냉장냉동고, ''''=브랜드 메인)'
        AFTER category,
    MODIFY COLUMN category VARCHAR(16) NOT NULL DEFAULT ''
        COMMENT '제품군 그룹 코드 (''''=브랜드 메인, WM/REF — 구 flat 코드 체계는 mig 028 폐지)',
    DROP KEY uq_brand,
    ADD UNIQUE KEY uq_brand (rtlr_name, cntry_cd, brand, category, sub_category);

-- ── 2) 전체 재시딩 (0721 고객사 시트 + CZ 복원) ──────────────────────────────
DELETE FROM brand_target_list;

INSERT INTO brand_target_list
    (brand_page_type, rtlr_name, cntry_cd, brand, category, sub_category, brand_url, notes)
VALUES
('Brand Page', 'Elcorteingles_electronica', 'ES', 'LG', '', '', 'https://www.elcorteingles.es/lg/electrodomesticos/', '0721 고객사 시트'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'LG', 'WM', '세탁기', 'https://www.elcorteingles.es/lg/electrodomesticos/lavadoras/', '0721 고객사 시트'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'LG', 'WM', '건조기', 'https://www.elcorteingles.es/lg/electrodomesticos/secadoras-de-ropa/', '0721 고객사 시트'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'LG', 'WM', '세탁건조기(일체형)', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'LG', 'REF', '냉장고', 'https://www.elcorteingles.es/lg/electrodomesticos/frigorificos-y-neveras/', '0721 고객사 시트'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'LG', 'REF', '냉동고', 'https://www.elcorteingles.es/lg/electrodomesticos/congeladores/', '0721 고객사 시트'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'LG', 'REF', '냉장냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Page', 'MediaMarkt', 'ES', 'LG', '', '', 'https://www.mediamarkt.es/es/brand/lg-electronics', '0721 고객사 시트'),
('Brand Category Page', 'MediaMarkt', 'ES', 'LG', 'WM', '세탁기', 'https://www.mediamarkt.es/es/brand/lg-electronics/lavado', '0721 고객사 시트'),
('Brand Category Page', 'MediaMarkt', 'ES', 'LG', 'WM', '건조기', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'LG', 'WM', '세탁건조기(일체형)', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'LG', 'REF', '냉장고', 'https://www.mediamarkt.es/es/brand/lg-electronics/frigorificos', '0721 고객사 시트'),
('Brand Category Page', 'MediaMarkt', 'ES', 'LG', 'REF', '냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'LG', 'REF', '냉장냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Page', 'Darty', 'FR', 'LG', '', '', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'Darty', 'FR', 'LG', 'WM', '세탁기', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'Darty', 'FR', 'LG', 'WM', '건조기', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'Darty', 'FR', 'LG', 'WM', '세탁건조기(일체형)', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'Darty', 'FR', 'LG', 'REF', '냉장고', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'Darty', 'FR', 'LG', 'REF', '냉동고', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'Darty', 'FR', 'LG', 'REF', '냉장냉동고', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Page', 'Boulanger', 'FR', 'LG', '', '', 'https://www.boulanger.com/marque/lg', '0721 고객사 시트'),
('Brand Category Page', 'Boulanger', 'FR', 'LG', 'WM', '세탁기', 'https://www.boulanger.com/c/lave-linge/brand~lg', '0721 고객사 시트'),
('Brand Category Page', 'Boulanger', 'FR', 'LG', 'WM', '건조기', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'LG', 'WM', '세탁건조기(일체형)', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'LG', 'REF', '냉장고', 'https://www.boulanger.com/c/refrigerateur/brand~lg', '0721 고객사 시트'),
('Brand Category Page', 'Boulanger', 'FR', 'LG', 'REF', '냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Boulanger', 'FR', 'LG', 'REF', '냉장냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Page', 'Mediaworld', 'IT', 'LG', '', '', 'https://www.mediaworld.it/it/brand/lg', '0721 고객사 시트'),
('Brand Category Page', 'Mediaworld', 'IT', 'LG', 'WM', '세탁기', 'https://www.mediaworld.it/it/brand/lg/lavatrici', '0721 고객사 시트'),
('Brand Category Page', 'Mediaworld', 'IT', 'LG', 'WM', '건조기', 'https://www.mediaworld.it/it/brand/lg/asciugatrici', '0721 고객사 시트'),
('Brand Category Page', 'Mediaworld', 'IT', 'LG', 'WM', '세탁건조기(일체형)', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'LG', 'REF', '냉장고', 'https://www.mediaworld.it/it/brand/lg/frigoriferi', '0721 고객사 시트'),
('Brand Category Page', 'Mediaworld', 'IT', 'LG', 'REF', '냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Mediaworld', 'IT', 'LG', 'REF', '냉장냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Page', 'Amazon', 'IT', 'LG', '', '', 'https://www.amazon.it/stores/page/CFD4D966-B596-4662-9305-AE3889DCC47C?ingress=0&visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde', '0721 고객사 시트'),
('Brand Category Page', 'Amazon', 'IT', 'LG', 'WM', '세탁기', 'https://www.amazon.it/stores/page/045E563A-5374-463E-BFDB-E7E47BDBC9F6?ingress=0&visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde', '0721 고객사 시트'),
('Brand Category Page', 'Amazon', 'IT', 'LG', 'WM', '건조기', 'https://www.amazon.it/stores/page/19248ADC-0AFB-4232-AB14-35EE45ABB5A5?ingress=0&visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde', '0721 고객사 시트'),
('Brand Category Page', 'Amazon', 'IT', 'LG', 'WM', '세탁건조기(일체형)', 'https://www.amazon.it/stores/page/999E54C1-41F6-4C23-BD58-C9CFDC61A728?ingress=0&visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde', '0721 고객사 시트'),
('Brand Category Page', 'Amazon', 'IT', 'LG', 'REF', '냉장고', 'https://www.amazon.it/stores/page/5DE174FF-7426-4856-9BA8-3EF64DA9BCC5?ingress=0&visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde', '0721 고객사 시트'),
('Brand Category Page', 'Amazon', 'IT', 'LG', 'REF', '냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Amazon', 'IT', 'LG', 'REF', '냉장냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Page', 'Unieuro', 'IT', 'LG', '', '', 'https://www.unieuro.it/online/LG', '0721 고객사 시트'),
('Brand Category Page', 'Unieuro', 'IT', 'LG', 'WM', '세탁기', 'https://www.unieuro.it/online/LG?dFR%5Bbrands.lvl1%5D%5B0%5D=brand_293&dFR%5BcategoryNames_it.lvl3%5D%5B0%5D=Lavatrici', '0721 고객사 시트'),
('Brand Category Page', 'Unieuro', 'IT', 'LG', 'WM', '건조기', 'https://www.unieuro.it/online/LG?dFR%5Bbrands.lvl1%5D%5B0%5D=brand_293&dFR%5BcategoryNames_it.lvl3%5D%5B0%5D=Asciugatrici', '0721 고객사 시트'),
('Brand Category Page', 'Unieuro', 'IT', 'LG', 'WM', '세탁건조기(일체형)', 'https://www.unieuro.it/online/LG?dFR%5Bbrands.lvl1%5D%5B0%5D=brand_293&dFR%5BcategoryNames_it.lvl3%5D%5B0%5D=Lavasciuga', '0721 고객사 시트'),
('Brand Category Page', 'Unieuro', 'IT', 'LG', 'REF', '냉장고', 'https://www.unieuro.it/online/LG?dFR%5Bbrands.lvl1%5D%5B0%5D=brand_293&dFR%5BcategoryNames_it.lvl3%5D%5B0%5D=Frigoriferi', '0721 고객사 시트'),
('Brand Category Page', 'Unieuro', 'IT', 'LG', 'REF', '냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Unieuro', 'IT', 'LG', 'REF', '냉장냉동고', 'https://www.unieuro.it/online/LG?dFR%5Bbrands.lvl1%5D%5B0%5D=brand_293&dFR%5BcategoryNames_it.lvl3%5D%5B0%5D=Frigoriferi%20combinati', '0721 고객사 시트'),
('Brand Page', 'Coolblue', 'NL', 'LG', '', '', 'https://www.coolblue.nl/lg', '0721 고객사 시트'),
('Brand Category Page', 'Coolblue', 'NL', 'LG', 'WM', '세탁기', 'https://www.coolblue.nl/wasmachines/lg', '0721 고객사 시트'),
('Brand Category Page', 'Coolblue', 'NL', 'LG', 'WM', '건조기', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Coolblue', 'NL', 'LG', 'WM', '세탁건조기(일체형)', 'https://www.coolblue.nl/was-droogcombinaties/lg', '0721 고객사 시트'),
('Brand Category Page', 'Coolblue', 'NL', 'LG', 'REF', '냉장고', 'https://www.coolblue.nl/koelkasten/lg/filter', '0721 고객사 시트'),
('Brand Category Page', 'Coolblue', 'NL', 'LG', 'REF', '냉동고', NULL, '0721 고객사 시트: 부재 판정(X)'),
('Brand Category Page', 'Coolblue', 'NL', 'LG', 'REF', '냉장냉동고', 'https://www.coolblue.nl/koelkasten/vrijstaand/koel-vriescombinaties/lg', '0721 고객사 시트'),
('Brand Page', 'Elgiganten', 'SE', 'LG', '', '', 'https://www.elgiganten.se/brand/lg', '0721 고객사 시트'),
('Brand Category Page', 'Elgiganten', 'SE', 'LG', 'WM', '세탁기', 'https://www.elgiganten.se/brand/lg/lg-tvattmaskin', '0721 고객사 시트'),
('Brand Category Page', 'Elgiganten', 'SE', 'LG', 'WM', '건조기', 'https://www.elgiganten.se/brand/lg/lg-torktumlare', '0721 고객사 시트'),
('Brand Category Page', 'Elgiganten', 'SE', 'LG', 'WM', '세탁건조기(일체형)', 'https://www.elgiganten.se/brand/lg/lg-kombinerad-tvattmaskin-torktumlare', '0721 고객사 시트'),
('Brand Category Page', 'Elgiganten', 'SE', 'LG', 'REF', '냉장고', 'https://www.elgiganten.se/brand/lg/kylskap-lg#result-top', '0721 고객사 시트'),
('Brand Category Page', 'Elgiganten', 'SE', 'LG', 'REF', '냉동고', 'https://www.elgiganten.se/brand/lg/lg-frysar', '0721 고객사 시트'),
('Brand Category Page', 'Elgiganten', 'SE', 'LG', 'REF', '냉장냉동고', 'https://www.elgiganten.se/brand/lg/lg-kyl-frys-kombiskap', '0721 고객사 시트'),
('Brand Page', 'MediaExpert', 'PL', 'LG', '', '', 'https://www.mediaexpert.pl/lg', '0721 고객사 시트'),
('Brand Category Page', 'MediaExpert', 'PL', 'LG', 'WM', '세탁기', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'MediaExpert', 'PL', 'LG', 'WM', '건조기', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'MediaExpert', 'PL', 'LG', 'WM', '세탁건조기(일체형)', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'MediaExpert', 'PL', 'LG', 'REF', '냉장고', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'MediaExpert', 'PL', 'LG', 'REF', '냉동고', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'MediaExpert', 'PL', 'LG', 'REF', '냉장냉동고', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Page', 'RtvEuroAgd', 'PL', 'LG', '', '', 'https://www.euro.com.pl/search.bhtml?keyword=LG', '0721 고객사 시트'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'LG', 'WM', '세탁기', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'LG', 'WM', '건조기', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'LG', 'WM', '세탁건조기(일체형)', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'LG', 'REF', '냉장고', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'LG', 'REF', '냉동고', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Category Page', 'RtvEuroAgd', 'PL', 'LG', 'REF', '냉장냉동고', NULL, '0721 고객사 시트: 공란(미확인)'),
('Brand Page', 'Datart', 'CZ', 'LG', '', '', 'https://www.datart.cz/shop/lg', 'EY 참고8 0714 (0721 개편 시 복원)'),
('Brand Category Page', 'Datart', 'CZ', 'LG', 'WM', '세탁기', NULL, 'EY 참고8 0714: Brand Category Page 미존재 판정 (0721 복원)'),
('Brand Category Page', 'Datart', 'CZ', 'LG', 'WM', '건조기', 'https://www.datart.cz/susicky-lg.html', 'EY 참고8 0714 (0721 개편 시 복원)'),
('Brand Category Page', 'Datart', 'CZ', 'LG', 'WM', '세탁건조기(일체형)', NULL, 'EY 참고8 0714: Brand Category Page 미존재 판정 (0721 복원)'),
('Brand Category Page', 'Datart', 'CZ', 'LG', 'REF', '냉장고', 'https://www.datart.cz/lednice-lg.html', 'EY 참고8 0714 (0721 개편 시 복원)'),
('Brand Category Page', 'Datart', 'CZ', 'LG', 'REF', '냉동고', NULL, 'EY 참고8 0714: Brand Category Page 미존재 판정 (0721 복원)'),
('Brand Category Page', 'Datart', 'CZ', 'LG', 'REF', '냉장냉동고', NULL, 'EY 참고8 0714: Brand Category Page 미존재 판정 (0721 복원)'),
('Brand Page', 'Alza', 'CZ', 'LG', '', '', 'https://www.alza.cz/lg/v1357.htm', 'EY 참고8 0714 (0721 개편 시 복원)'),
('Brand Category Page', 'Alza', 'CZ', 'LG', 'WM', '세탁기', 'https://www.alza.cz/pracky/lg/18852774-v1357.htm', 'EY 참고8 0714 (0721 개편 시 복원)'),
('Brand Category Page', 'Alza', 'CZ', 'LG', 'WM', '건조기', 'https://www.alza.cz/susicky/lg/18852767-v1357.htm', 'EY 참고8 0714 (0721 개편 시 복원)'),
('Brand Category Page', 'Alza', 'CZ', 'LG', 'WM', '세탁건조기(일체형)', NULL, 'EY 참고8 0714: Brand Category Page 미존재 판정 (0721 복원)'),
('Brand Category Page', 'Alza', 'CZ', 'LG', 'REF', '냉장고', 'https://www.alza.cz/lednicky/lg/18852759-v1357.htm', 'EY 참고8 0714 (0721 개편 시 복원)'),
('Brand Category Page', 'Alza', 'CZ', 'LG', 'REF', '냉동고', NULL, 'EY 참고8 0714: Brand Category Page 미존재 판정 (0721 복원)'),
('Brand Category Page', 'Alza', 'CZ', 'LG', 'REF', '냉장냉동고', NULL, 'EY 참고8 0714: Brand Category Page 미존재 판정 (0721 복원)');
