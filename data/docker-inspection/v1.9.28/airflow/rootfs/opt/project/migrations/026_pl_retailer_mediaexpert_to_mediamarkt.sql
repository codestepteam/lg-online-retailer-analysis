-- Migration 026: 폴란드 home/plp 리테일러 교체 — MediaExpert → MediaMarkt
-- 실행: mysql -u <user> -p <db> < migrations/026_pl_retailer_mediaexpert_to_mediamarkt.sql
--
-- 배경
--   폴란드 대상 리테일러가 MediaExpert(mediaexpert.pl) 로 잘못 등록돼 있었다.
--   실제 진단 대상은 MediaMarkt 폴란드(mediamarkt.pl) — MMS(MediaMarktSaturn) 플랫폼.
--   → home/plp 트랙에 한해 PL 리테일러를 MediaMarkt 로 교체한다.
--   (RtvEuroAgd_PL(euro.com.pl) 은 실제 폴란드 리테일러라 그대로 유지.
--    pdp/brand 트랙의 MediaExpert 등록은 이번 범위 밖 — 별도 정리 예정.)
--
--   코드 측 대응 (동일 커밋):
--     · core/retailers.py            — RETAILERS 에 MediaMarkt_PL 추가 (domain=mediamarkt.pl)
--     · crawl_retailers/home,plp/__init__ — EXTRACTORS: MediaExpert_PL → MediaMarkt_PL
--     · parse_retailers/home,plp/__init__ — PARSERS:    MediaExpert_PL → MediaMarkt_PL
--     · core/home_keywords_load.py    — RETAILER_MAP: MEDIAMARKT 에 PL 추가
--
-- ⚠️ DB 저장 규약 (mig 013): home_target_list/home_keywords 의 rtlr_name 은 국가 suffix
--    없는 순수 리테일러명. 내부 레지스트리 키(MediaMarkt_PL)는 composite_key 가 조립.
--    → 여기서는 rtlr_name='MediaMarkt', cntry_cd='PL' 로 저장.
--
-- ⚠️ 검색 URL(/pl/search.html?query=)은 MMS 플랫폼 표준으로 시드 — mediamarkt.pl 실측 검증 대상.

-- ── 1) home_target_list: MediaExpert(PL) 제거 → MediaMarkt(PL) 추가 ──────────
DELETE FROM home_target_list WHERE rtlr_name = 'MediaExpert' AND cntry_cd = 'PL';

INSERT INTO home_target_list (rtlr_name, cntry_cd, home_url, search_url_template, notes) VALUES
    ('MediaMarkt', 'PL', 'https://www.mediamarkt.pl/',
     'https://www.mediamarkt.pl/pl/search.html?query={q}',
     'MMS 플랫폼 — 로컬 차단 시 SB escalate (검색 URL 실측 확인 2026-07-15)')
ON DUPLICATE KEY UPDATE
    home_url            = VALUES(home_url),
    search_url_template = VALUES(search_url_template),
    notes               = VALUES(notes);

-- ── 2) home_keywords: MediaExpert(PL) 잘못 적재분 제거 → MediaMarkt(PL) 재적재 ─
--    (kywd_type='home' 3행 — home 검색 SERP + plp 소스. category/GNB 는 별도 확정 예정)
--    home_keywords 는 평시 Excel(replace_all)로 적재되므로, 마스터 재업로드 시 이 시드가
--    사라질 수 있음 — 재업로드 Excel 에 PL MediaMarkt 행을 포함시킬 것.
DELETE FROM home_keywords WHERE rtlr_name = 'MediaExpert' AND cntry_cd = 'PL';

INSERT INTO home_keywords
    (rtlr_name, cntry_cd, loc_srch_kywd_info, eng_srch_kywd_info, srch_kywd_cat_name, kywd_type)
VALUES
    ('MediaMarkt', 'PL', 'lodówka',         'refrigerator',       'Refrigerator',    'home'),
    ('MediaMarkt', 'PL', 'pralka',          'washing machine',    'Washing Machine', 'home'),
    ('MediaMarkt', 'PL', 'pralko-suszarka', 'washer dryer combo', 'Washing Machine', 'home')
ON DUPLICATE KEY UPDATE
    eng_srch_kywd_info = VALUES(eng_srch_kywd_info),
    srch_kywd_cat_name = VALUES(srch_kywd_cat_name);
