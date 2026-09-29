-- Migration 042: NL MediaMarkt home 트랙 온보딩 — ID1/2/4 공백 해소 (2026-08-17)
--   (구 041 — feature/v1.8 에선 041 이었으나 v1.9 의 041_brand_target_nlmm_lg 와
--    번호 충돌해 병합 시 042 로 리넘버. DB 적용분과 내용 동일 — 멱등 재실행 무해)
--
-- 배경
--   20260812 배치(NL MM 전용)는 ID3(gnb_keyword_map, mig 040 무필터 2행)만 산출.
--   ID1/ID2/ID4 는 home_target_list 에 ('MediaMarkt','NL') 행이 없어 검색 타깃이
--   0건이었다 (repo.load_home_targets = home_target_list × home_keywords 조인).
--
-- 키워드 (사용자 지시 2026-08-17: "NL Coolblue 와 같이")
--   home_keywords 는 (rtlr_name, cntry_cd) 키 구조라 리테일러 간 공유 참조 불가
--   → INSERT…SELECT 로 Coolblue NL 세트를 복사 (적용 시점 실측 9행: home 7 +
--   category 2 — koelkast/wasmachine 이중 소속 포함). INSERT IGNORE 로 멱등
--   (uq_keyword: rtlr_name, cntry_cd, loc_srch_kywd_info, kywd_type).
--
-- 검색 URL
--   MMS 플랫폼 공통 패턴 — ES(mig 008)·PL(mig 026) 과 동일한 /{lang}/search.html
--   쿼리스트링 주입. 한국 IP 로컬은 즉시 CAPTCHA(0817 실측) → force_sb 대상이라
--   SB 스모크 1건으로 그리드 렌더 확인 후 풀배치.
--
-- ⚠️ ID3 무필터 통일(2026-08-17 설계 B)은 사용자 반려 — gnb_keyword_map 불변.
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/042_nl_mediamarkt_home_onboarding.sql

-- 1) home_target_list — 랜딩 + 검색 템플릿 1행
INSERT INTO home_target_list (rtlr_name, cntry_cd, home_url, search_url_template, notes) VALUES
('MediaMarkt', 'NL', 'https://www.mediamarkt.nl/',
 'https://www.mediamarkt.nl/nl/search.html?query={q}',
 'MMS 플랫폼 — force_sb (한국IP 즉시 CAPTCHA 0817 실측). 키워드는 Coolblue NL 복사 (mig 042)')
ON DUPLICATE KEY UPDATE
    home_url            = VALUES(home_url),
    search_url_template = VALUES(search_url_template),
    notes               = VALUES(notes);

-- 2) home_keywords — Coolblue NL 세트 복제 (동일 키워드·카테고리명·kywd_type)
INSERT IGNORE INTO home_keywords
    (rtlr_name, cntry_cd, loc_srch_kywd_info, eng_srch_kywd_info, srch_kywd_cat_name, kywd_type)
SELECT 'MediaMarkt', cntry_cd, loc_srch_kywd_info, eng_srch_kywd_info, srch_kywd_cat_name, kywd_type
FROM home_keywords
WHERE rtlr_name = 'Coolblue' AND cntry_cd = 'NL';
