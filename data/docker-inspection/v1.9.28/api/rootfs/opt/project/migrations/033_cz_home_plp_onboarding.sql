-- Migration 033: CZ(Datart/Alza) home/plp 트랙 온보딩 — 타깃 마스터 시딩
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/033_cz_home_plp_onboarding.sql
--
-- 배경 (2026-07-23)
--   CZ 는 0720 온보딩 때 brand·pdp 만 스코프였다 (mig 028 brand_target_list,
--   discover 산출 pdp_target_list). home/plp 편입에 따라 두 트랙의 타깃 마스터를
--   시딩한다. home_keywords CZ 행(리테일러당 6키워드, home/category 이중)은 기존재.
--
--   검색 URL 템플릿 (2026-07-23 SB premium cz 홈 검색 폼 실측):
--     Datart — form action=/vyhledavani, GET input name=q
--     Alza   — form action=/search.htm,  GET input name=exps
--   제네릭 쿼리(pračka 등)는 양사 모두 301/302 로 카테고리 PLP 리다이렉트 —
--   그리드는 동일 SSR 이라 파서 지장 없음 (extract_products 공유).
--
--   gnb_keyword_map: CZ 는 dataset(gnb_dataset2.xlsx) 시트에 없어 브랜드 필터
--   URL 미확보 → Coolblue 선례(mig 032)대로 카테고리 전체 리스트 URL 시딩.
--   URL 은 discover_targets 실측 canonical (Datart /{slug}.html, Alza
--   /{slug}/{cat_id}.htm). 브랜드 필터 URL 확보 시 UPSERT 로 교체.
--   스코프는 mig 032 와 동일하게 WM/REF 2종 (brand_track_list CZ 도 REF/WM 만).
--
-- ⚠️ DB 저장 규약 (mig 013): rtlr_name 은 국가 suffix 없는 순수 리테일러명.
--    Datart/Alza 는 단국가라 composite_key 도 suffix 없이 그대로 반환.

-- ── 1) home_target_list: CZ 2행 (홈 랜딩 + 검색 템플릿) ───────────────────────
INSERT INTO home_target_list (rtlr_name, cntry_cd, home_url, search_url_template, notes) VALUES
    ('Datart', 'CZ', 'https://www.datart.cz/',
     'https://www.datart.cz/vyhledavani?q={q}',
     'SSR — 로컬 한국IP 즉시 CAPTCHA, SB premium cz 정답 (0723 실측)'),
    ('Alza', 'CZ', 'https://www.alza.cz/',
     'https://www.alza.cz/search.htm?exps={q}',
     'SSR — 로컬 JS 챌린지(headless 불안정), SB premium cz 무챌린지 (0723 실측)')
ON DUPLICATE KEY UPDATE
    home_url            = VALUES(home_url),
    search_url_template = VALUES(search_url_template),
    notes               = VALUES(notes);

-- ── 2) gnb_keyword_map: CZ 4행 (WM/REF × Datart/Alza — ID3 GNB Top20 소스) ──
INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note) VALUES
('CZ','Datart','WM','WASH','pračka','Pračky',
 'https://www.datart.cz/pracky.html','CONFIRMED',
 '브랜드 필터 없음 — 카테고리 전체 리스트 (Coolblue 선례). 0723 실측 canonical'),
('CZ','Datart','REF','FRFR','lednice','Lednice',
 'https://www.datart.cz/lednicky.html','CONFIRMED',
 '브랜드 필터 없음 — 카테고리 전체 리스트 (Coolblue 선례). 0723 실측 canonical'),
('CZ','Alza','WM','WASH','pračka','Pračky',
 'https://www.alza.cz/pracky/18852774.htm','CONFIRMED',
 '브랜드 필터 없음 — 카테고리 전체 리스트 (Coolblue 선례). 0723 실측 canonical'),
('CZ','Alza','REF','FRFR','lednice','Lednice',
 'https://www.alza.cz/lednicky/18852759.htm','CONFIRMED',
 '브랜드 필터 없음 — 카테고리 전체 리스트 (Coolblue 선례). 0723 실측 canonical')
ON DUPLICATE KEY UPDATE
    cat_cd     = VALUES(cat_cd),
    cat_sub_cd = VALUES(cat_sub_cd),
    gnb_label  = VALUES(gnb_label),
    gnb_url    = VALUES(gnb_url),
    status     = VALUES(status),
    note       = VALUES(note);
