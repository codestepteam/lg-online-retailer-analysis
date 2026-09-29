-- Migration 005: home_search_config 시드 데이터
-- 리테일러 홈 URL + 검색 URL 템플릿 ({q} placeholder).
-- 실행: mysql -u <user> -p <db> < migrations/005_seed_home_search_config.sql
--
-- URL 출처: crawl_retailers/pdp/*.py 의 _BASE + page_targets() 검색 URL 조립 로직
-- But_FR, Darty_FR: 검색 트랙 차단 (robots.txt Disallow / Queue-IT) → search_url_template NULL

INSERT INTO home_search_config (retailer, instance, home_url, search_url_template) VALUES
    ('Coolblue',                  'NL', 'https://www.coolblue.nl/',                   'https://www.coolblue.nl/zoeken?query={q}'),
    ('Amazon_IT',                 'IT', 'https://www.amazon.it/',                     'https://www.amazon.it/s?k={q}'),
    ('Elcorteingles_electronica', 'ES', 'https://www.elcorteingles.es/',              'https://www.elcorteingles.es/search-nwx/?s={q}'),
    ('MediaMarkt_ES',             'ES', 'https://www.mediamarkt.es/',                 'https://www.mediamarkt.es/es/search.html?query={q}'),
    ('Mediaworld',                'IT', 'https://www.mediaworld.it/',                 'https://www.mediaworld.it/it/search.html?query={q}'),
    ('Unieuro',                   'IT', 'https://www.unieuro.it/online/',             'https://www.unieuro.it/online/products?q={q}'),
    ('Elgiganten',                'SE', 'https://www.elgiganten.se/',                 'https://www.elgiganten.se/search?q={q}'),
    ('MediaExpert_PL',            'PL', 'https://www.mediaexpert.pl/',                'https://www.mediaexpert.pl/search?query%5Bquerystring%5D={q}'),
    ('RtvEuroAgd_PL',             'PL', 'https://www.euro.com.pl/',                   'https://www.euro.com.pl/search.bhtml?keyword={q}'),
    ('Boulanger',                 'FR', 'https://www.boulanger.com/',                 'https://www.boulanger.com/resultats?tr={q}'),
    ('But_FR',                    'FR', 'https://www.but.fr/',                        NULL),
    ('Darty_FR',                  'FR', 'https://www.darty.com/',                     NULL)
ON DUPLICATE KEY UPDATE
    home_url            = VALUES(home_url),
    search_url_template = VALUES(search_url_template);
