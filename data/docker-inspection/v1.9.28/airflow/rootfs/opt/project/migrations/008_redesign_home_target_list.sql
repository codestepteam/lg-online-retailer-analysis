-- Migration 008: home_target_list 재설계 — 배치 무관 마스터로 통합
-- 실행: mysql -u <user> -p <db> < migrations/008_redesign_home_target_list.sql
--
-- 배경
--   home 트랙이 두 테이블로 쪼개져 있었다:
--     · home_target_list  (mig 002) — batch-scoped, retailer/instance/url 만 (사실상 미사용)
--     · home_search_config (mig 004) — 배치 무관, home_url + search_url_template
--   결과: 크롤이 참조하는 마스터는 home_search_config 인데, 이름은 home_target_list 가 차지.
--   → 하나의 배치 무관 마스터로 통합 (home_target_list 로 명명 유지).
--     검색 URL / 운영 메모 / 감사 컬럼 포함.
--
-- 흐름
--   home_target_list (retailer, cntry_code)   -- 마스터 (홈 + 검색 템플릿 + notes)
--     × home_keywords  (retailer, cntry_code) -- 검색 키워드 (별도 관리 — 사용자 제공 예정)
--     → 검색 URL 조립: template.replace('{q}', quote_plus(local_keyword))
--
-- ⚠️ 왜 batch_id 가 없는가 (pdp_target_list 와의 차이)
--   pdp_target_list: 사용자가 report_date 마다 URL 리스트를 업로드 → 배치별로 다른 집합.
--   home_target_list: 12개 리테일러의 고정 URL 스킴 = 마스터 설정.
--     배치가 바뀌어도 홈/검색 URL 스킴이 그대로라 batch_id 를 넣으면 매 배치마다
--     동일한 12행이 복제될 뿐 정보량이 없음.
--   ▶ 만약 "배치별 스냅샷" 이 필요하면 (URL 스킴 변경 이력 추적 등)
--     batch_id VARCHAR(20) + report_date DATE 추가 + INSERT..SELECT 로 copy_on_new_batch 도입.

-- ── 1) 기존 배치-스코프 home_target_list 폐기 ──────────────────────────────
DROP TABLE IF EXISTS home_target_list;

-- ── 2) home_search_config → home_target_list 로 rename (데이터 보존) ────────
--    home_search_config 는 mig 004 에서 생성, mig 005 에서 시드됨.
RENAME TABLE home_search_config TO home_target_list;

-- ── 3) 컬럼 rename + 보강 ──────────────────────────────────────────────────
--    instance → cntry_code (pdp_target_list.cntry_code 와 명명 통일)
ALTER TABLE home_target_list
    CHANGE COLUMN instance cntry_code CHAR(2) NOT NULL COMMENT '국가 코드 대문자 (예: NL)',
    ADD COLUMN notes      VARCHAR(255) NULL COMMENT '메모 — NULL 이유 / 렌더 대기 / SB 정책 등 특이사항' AFTER search_url_template,
    ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- 인덱스명(uq_home_search → uq_home) 재정비 — 컬럼 참조 갱신
ALTER TABLE home_target_list DROP INDEX uq_home_search;
ALTER TABLE home_target_list ADD UNIQUE KEY uq_home (retailer, cntry_code);

-- ── 4) Darty search 재개통 반영 (mig 005 시점엔 NULL — Queue-IT 차단 전제) ─
--    2026-07-03 SB stealth 재검증에서 11/11 수집 성공.
UPDATE home_target_list
SET search_url_template = 'https://www.darty.com/nav/recherche?text={q}',
    notes = '2026-07-03 SB stealth 재검증 성공 (Queue-IT 재활성화 감시)'
WHERE retailer = 'Darty_FR';

-- ── 5) notes 백필 ─────────────────────────────────────────────────────────
UPDATE home_target_list SET notes = 'robots.txt Disallow — 검색 크롤 금지 (CEO 결정 2a)'
    WHERE retailer = 'But_FR';
UPDATE home_target_list SET notes = 'generic 키워드는 카테고리 리다이렉트 — 실제 사이트 동작'
    WHERE retailer = 'Coolblue';
UPDATE home_target_list SET notes = 'HTML 에 LG 미노출 — 실제 SERP 부재 (파서 문제 아님)'
    WHERE retailer = 'Elcorteingles_electronica';
UPDATE home_target_list SET notes = 'CSR — Playwright 렌더 wait 8~12s 필요'
    WHERE retailer = 'Elgiganten';
UPDATE home_target_list SET notes = 'Angular SPA — Playwright 렌더 wait 10s 필요'
    WHERE retailer = 'Unieuro';
UPDATE home_target_list SET notes = 'stealth (DataDome)'
    WHERE retailer = 'Boulanger';
UPDATE home_target_list SET notes = 'stealth 필수'
    WHERE retailer = 'MediaExpert_PL';
UPDATE home_target_list SET notes = 'premium 필수'
    WHERE retailer IN ('Amazon_IT', 'Mediaworld', 'RtvEuroAgd_PL');

-- ── 6) 안전망 UPSERT (rename 실패로 빈 테이블 재생성됐을 때만 값 채움) ─────
--    RENAME 이 성공했다면 이 INSERT 는 uq_home 충돌로 ON DUPLICATE 만 발동 (no-op).
INSERT INTO home_target_list (retailer, cntry_code, home_url, search_url_template, notes) VALUES
    ('Amazon_IT',                 'IT', 'https://www.amazon.it/',         'https://www.amazon.it/s?k={q}',                              'premium 필수'),
    ('Boulanger',                 'FR', 'https://www.boulanger.com/',     'https://www.boulanger.com/resultats?tr={q}',                 'stealth (DataDome)'),
    ('But_FR',                    'FR', 'https://www.but.fr/',            NULL,                                                         'robots.txt Disallow — 검색 크롤 금지 (CEO 결정 2a)'),
    ('Coolblue',                  'NL', 'https://www.coolblue.nl/',       'https://www.coolblue.nl/zoeken?query={q}',                   'generic 키워드는 카테고리 리다이렉트 — 실제 사이트 동작'),
    ('Darty_FR',                  'FR', 'https://www.darty.com/',         'https://www.darty.com/nav/recherche?text={q}',               '2026-07-03 SB stealth 재검증 성공 (Queue-IT 재활성화 감시)'),
    ('Elcorteingles_electronica', 'ES', 'https://www.elcorteingles.es/',  'https://www.elcorteingles.es/search-nwx/?s={q}',             'HTML 에 LG 미노출 — 실제 SERP 부재 (파서 문제 아님)'),
    ('Elgiganten',                'SE', 'https://www.elgiganten.se/',     'https://www.elgiganten.se/search?q={q}',                     'CSR — Playwright 렌더 wait 8~12s 필요'),
    ('MediaExpert_PL',            'PL', 'https://www.mediaexpert.pl/',    'https://www.mediaexpert.pl/search?query%5Bquerystring%5D={q}', 'stealth 필수'),
    ('MediaMarkt_ES',             'ES', 'https://www.mediamarkt.es/',     'https://www.mediamarkt.es/es/search.html?query={q}',         NULL),
    ('Mediaworld',                'IT', 'https://www.mediaworld.it/',     'https://www.mediaworld.it/it/search.html?query={q}',         'premium 필수'),
    ('RtvEuroAgd_PL',             'PL', 'https://www.euro.com.pl/',       'https://www.euro.com.pl/search.bhtml?keyword={q}',           'premium 필수'),
    ('Unieuro',                   'IT', 'https://www.unieuro.it/online/', 'https://www.unieuro.it/online/products?q={q}',               'Angular SPA — Playwright 렌더 wait 10s 필요')
ON DUPLICATE KEY UPDATE
    home_url            = VALUES(home_url),
    search_url_template = VALUES(search_url_template),
    notes               = VALUES(notes);
