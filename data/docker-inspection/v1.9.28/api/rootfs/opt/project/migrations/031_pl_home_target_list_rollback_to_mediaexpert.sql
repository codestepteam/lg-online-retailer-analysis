-- Migration 031: 폴란드 home_target_list 리테일러 롤백 — MediaMarkt → MediaExpert
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/031_pl_home_target_list_rollback_to_mediaexpert.sql
--
-- 배경 (2026-07-21)
--   mig 026 이 PL home/plp 리테일러를 MediaExpert → MediaMarkt 로 교체했으나,
--   이번에 그 결정을 되돌려(MediaMarkt → MediaExpert) home/plp 를 MediaExpert 로
--   확정한다. 코드 라우터(crawl/parse home·plp __init__)와 home_keywords 는 이미
--   MediaExpert 로 롤백됐으나(커밋 138136e 및 후속), home_target_list 의 PL 행만
--   MediaMarkt 로 남아 반쪽 상태였다 — 익스트랙터(MediaExpert_PL)와 크롤 타깃
--   (mediamarkt.pl)이 어긋나 home PL 크롤 진입 불가.
--   → home_target_list PL 행을 MediaExpert(mediaexpert.pl)로 되돌려 정합성 회복.
--
--   home_url/search_url_template 은 mig 008(구 MediaExpert_PL 시드) 원값 복원.
--   RtvEuroAgd(PL) 은 mig 026 범위 밖이라 그대로 유지.
--
-- ⚠️ DB 저장 규약 (mig 013): rtlr_name 은 국가 suffix 없는 순수 리테일러명.
--    → rtlr_name='MediaExpert', cntry_cd='PL' 로 저장 (composite_key 가 MediaExpert_PL 조립).

-- ── PL home_target_list: MediaMarkt(PL) 제거 → MediaExpert(PL) 복원 ──────────
DELETE FROM home_target_list WHERE rtlr_name = 'MediaMarkt' AND cntry_cd = 'PL';

INSERT INTO home_target_list (rtlr_name, cntry_cd, home_url, search_url_template, notes) VALUES
    ('MediaExpert', 'PL', 'https://www.mediaexpert.pl/',
     'https://www.mediaexpert.pl/search?query%5Bquerystring%5D={q}',
     'stealth 필수 — mig 026 롤백 복원 (2026-07-21)')
ON DUPLICATE KEY UPDATE
    home_url            = VALUES(home_url),
    search_url_template = VALUES(search_url_template),
    notes               = VALUES(notes);
