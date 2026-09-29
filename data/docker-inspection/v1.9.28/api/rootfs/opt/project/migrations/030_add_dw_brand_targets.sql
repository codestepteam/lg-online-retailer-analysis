-- Migration 030: DW(식기세척기) 브랜드 트랙 재편입 — ES 전용, 브랜드별 5종
--
-- 배경 (2026-07-21 사용자 확정)
--   0721 개편(mig 028) 때 시트에 없어 제외했던 DW 를 커버리지 요구로 재편입.
--   아이체킹 시트(260625, 67~72행)가 DW 만 브랜드별(LG/BOSCH/BALAY/BEKO/HISENSE)
--   구성이라, brand 컬럼을 활용해 브랜드×리테일러 행으로 시딩한다 (ES 전용 —
--   CATEGORY_COUNTRY_ALLOW 정책 유지). 저장 폴더는 {BRAND}_DW.
--   경쟁사 URL 패턴은 SB 프로브로 8/8 실측 확인 (HTTP 200 + 브랜드 타이틀):
--     ECI https://www.elcorteingles.es/{brand}/electrodomesticos/lavavajillas/
--     MM  https://www.mediamarkt.es/es/brand/{brand}/lavavajillas
--
-- 실행: docker exec -i <mysql> mysql --default-character-set=utf8mb4 \
--         -u<user> -p<pw> lg_clinic < migrations/030_add_dw_brand_targets.sql

INSERT INTO brand_target_list
    (brand_page_type, rtlr_name, cntry_cd, brand, category, sub_category, brand_url, notes)
VALUES
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'LG',      'DW', '식기세척기', 'https://www.elcorteingles.es/lg/electrodomesticos/lavavajillas/',      'DW 재편입 0721 (아이체킹 시트 260625)'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'BOSCH',   'DW', '식기세척기', 'https://www.elcorteingles.es/bosch/electrodomesticos/lavavajillas/',   'DW 재편입 0721 — SB 프로브 200'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'BALAY',   'DW', '식기세척기', 'https://www.elcorteingles.es/balay/electrodomesticos/lavavajillas/',   'DW 재편입 0721 — SB 프로브 200'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'BEKO',    'DW', '식기세척기', 'https://www.elcorteingles.es/beko/electrodomesticos/lavavajillas/',    'DW 재편입 0721 — SB 프로브 200'),
('Brand Category Page', 'Elcorteingles_electronica', 'ES', 'HISENSE', 'DW', '식기세척기', 'https://www.elcorteingles.es/hisense/electrodomesticos/lavavajillas/', 'DW 재편입 0721 — SB 프로브 200'),
('Brand Category Page', 'MediaMarkt', 'ES', 'LG',      'DW', '식기세척기', 'https://www.mediamarkt.es/es/brand/lg-electronics/lavavajillas', 'DW 재편입 0721 (구 mig 이전 등록분 복원)'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BOSCH',   'DW', '식기세척기', 'https://www.mediamarkt.es/es/brand/bosch/lavavajillas',   'DW 재편입 0721 — SB 프로브 200'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BALAY',   'DW', '식기세척기', 'https://www.mediamarkt.es/es/brand/balay/lavavajillas',   'DW 재편입 0721 — SB 프로브 200'),
('Brand Category Page', 'MediaMarkt', 'ES', 'BEKO',    'DW', '식기세척기', 'https://www.mediamarkt.es/es/brand/beko/lavavajillas',    'DW 재편입 0721 — SB 프로브 200'),
('Brand Category Page', 'MediaMarkt', 'ES', 'HISENSE', 'DW', '식기세척기', 'https://www.mediamarkt.es/es/brand/hisense/lavavajillas', 'DW 재편입 0721 — SB 프로브 200')
ON DUPLICATE KEY UPDATE brand_url = VALUES(brand_url), notes = VALUES(notes),
                        brand_page_type = VALUES(brand_page_type);
