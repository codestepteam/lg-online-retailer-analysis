-- Migration 056: gnb_keyword_map — EY v2.0(260913) 참고12 신규 확대 16개국 32행 선적재 (무필터 카테고리 URL)
--
-- 배경 (2026-09-15)
--   EY 진단항목 v2.0 참고12 [v2.0 신규 확대 리테일러 GNB 검색어] 32행은 EY 가 "LG 브랜드 카테고리 URL"
--   로 실사한 것이라 전부 LG 필터형(?f.product.brandName=lg · /brand---lg/ · /f/marca/LG · 브랜드관)
--   이거나 X/확인 필요다. ID3(GNB 카테고리 페이지 Top20 자사 노출 개수)는 **무필터 카테고리 페이지**가
--   정본(EY 0820 지적 → mig 047)이므로, 필터를 벗기거나 사이트 GNB 트리에서 카테고리 리스트 URL 을
--   직접 발굴해 적재한다 (사용자 지시 2026-09-15 "찾아서 적재").
--
--   status 규약(.claude/skills/gnb-url-extraction.md):
--     CONFIRMED — 0915 브라우저 실측: 카테고리 타이틀 + 브랜드 혼재 상품 리스팅 확인
--     RECAPTURE — URL 은 유도·검색 색인으로 확보했으나 봇월(Cloudflare/Akamai/reCAPTCHA)로 리스팅 미확인
--                 → 온보딩 크롤 시 parsed.json 리스팅 확인 후 CONFIRMED 승격
--   keyword = 시트 "Search Keyword (GNB)"(리포트 SearchKeyword 라벨), gnb_label = 사이트 실제 노드명.
--   RTLR_NAME 은 mig 013 규약(순수명, 국가 suffix 없음). 미등록 리테일러는 core/retailers.py 등록 +
--   crawl_retailers/plp 모듈이 생기기 전까지 crawl.py 의 has_extractor 게이트가 방출하지 않는다.
--
--   ⚠️ 온보딩 시 주의:
--     · Electroplanet(MA) 는 GNB 노드가 허브(리스팅 없음) — 리프 카테고리 선택을 EY 와 확정해야 한다.
--     · Amazon AU 세탁기는 브라우즈 노드가 없어(Toys 노드뿐) gnb_url NULL 자리표시자 — 로더가 건너뛴다.
--     · Falabella 는 bare 카테고리 URL 이 랜딩일 수 있어 크롤 시 ?isPLP=1 강제 검토(gnb_fetch_url 훅).
--     · Momoshop 은 구 LgrpCategory.jsp?l_code= 가 /categories/{code} 로 301 — 최종 URL 로 적재.
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/056_gnb_keyword_map_v20_new_markets.sql
-- 멱등: uq_kw(cntry_cd, RTLR_NAME, keyword) 기준 ON DUPLICATE KEY UPDATE.

CREATE TABLE IF NOT EXISTS gnb_keyword_map_backup_v5 LIKE gnb_keyword_map;
INSERT INTO gnb_keyword_map_backup_v5
  SELECT * FROM gnb_keyword_map
  WHERE NOT EXISTS (SELECT 1 FROM gnb_keyword_map_backup_v5);

INSERT INTO gnb_keyword_map
  (cntry_cd, RTLR_NAME, cat_cd, cat_sub_cd, keyword, gnb_label, gnb_url, status, note) VALUES
-- CA · Home Depot (시트 리테일러 '문의 필요' — URL 이 homedepot.ca 라 HomeDepot 로 적재)
('CA','HomeDepot','REF','FRFR','Refrigerators','Refrigerators',
 'https://www.homedepot.ca/en/home/categories/appliances/refrigerators.html','RECAPTURE',
 'v2.0 참고12(0913) LG 필터(/f/ki8-fs2) 제거 유도. 시트 리테일러 문의 필요. Akamai 차단으로 리스팅 미확인'),
('CA','HomeDepot','WM','WASH','Washers','Washing Machines',
 'https://www.homedepot.ca/en/home/categories/appliances/washers-and-dryers/washers.html','RECAPTURE',
 'v2.0 참고12(0913) LG 필터(/f/bok-fs2) 제거 — 검색 색인 "Washing Machines" 확인. Akamai 차단으로 리스팅 미확인'),
-- BR · Magazine Luiza
('BR','MagazineLuiza','REF','FRFR','Geladeiras','Geladeira / Refrigerador',
 'https://www.magazineluiza.com.br/geladeira-refrigerador/eletrodomesticos/s/ed/refr/','CONFIRMED',
 'v2.0 참고12(0913) /brand---lg/ 제거. 0915 실측: h1 Geladeira / Refrigerador, 브랜드 혼재(Electrolux·Midea·Consul)'),
('BR','MagazineLuiza','WM','WASH','Máquinas de Lavar','Máquina de Lavar',
 'https://www.magazineluiza.com.br/maquina-de-lavar/eletrodomesticos/s/ed/lava/','CONFIRMED',
 'v2.0 참고12(0913) /brand---lg/ 제거. 0915 실측: 52 카드, 브랜드 혼재'),
-- MX · Liverpool (시트 X — GNB 트리에서 발굴)
('MX','Liverpool','REF','FRFR','Refrigeradores','Refrigeradores y congeladores',
 'https://www.liverpool.com.mx/tienda/refrigeradores/CATST53841452','CONFIRMED',
 'v2.0 참고12(0913) 시트 X → Línea blanca GNB 실측. 0915: 56 카드, 브랜드 혼재(TCL·LG·Hisense·Midea). 냉동고 포함 카테고리'),
('MX','Liverpool','WM','WASH','Lavadoras','Lavadoras y secadoras',
 'https://www.liverpool.com.mx/tienda/lavadoras/catst42843485','CONFIRMED',
 'v2.0 참고12(0913) 시트 X → Línea blanca GNB 실측. 0915: 56 카드, 브랜드 혼재(Hisense·Mabe·Whirlpool). 건조기 포함 카테고리'),
-- PE · Falabella
('PE','Falabella','REF','FRFR','Refrigeradoras','Refrigeradoras',
 'https://www.falabella.com.pe/falabella-pe/category/cat780530/Refrigeradoras','RECAPTURE',
 'v2.0 참고12(0913) ?f.product.brandName=lg 제거. Cloudflare 챌린지로 리스팅 미확인. 랜딩이면 ?isPLP=1 강제'),
('PE','Falabella','WM','WASH','Lavadoras','Lavadoras',
 'https://www.falabella.com.pe/falabella-pe/category/cat780522/Lavadoras','RECAPTURE',
 'v2.0 참고12(0913) ?f.product.brandName=lg 제거. Cloudflare 챌린지로 리스팅 미확인. 랜딩이면 ?isPLP=1 강제'),
-- CL · Falabella
('CL','Falabella','REF','FRFR','Refrigeradores','Refrigeradores',
 'https://www.falabella.com/falabella-cl/category/cat3205/Refrigeradores','RECAPTURE',
 'v2.0 참고12(0913) ?f.product.brandName=lg 제거. Cloudflare 챌린지로 리스팅 미확인. 랜딩이면 ?isPLP=1 강제'),
('CL','Falabella','WM','WASH','Lavadoras','Lavadoras',
 'https://www.falabella.com/falabella-cl/category/cat4060/Lavadoras','RECAPTURE',
 'v2.0 참고12(0913) ?f.product.brandName=lg 제거. Cloudflare 챌린지로 리스팅 미확인. 랜딩이면 ?isPLP=1 강제'),
-- PT · Worten
('PT','Worten','REF','FRFR','Frigoríficos','Frigoríficos',
 'https://www.worten.pt/grandes-eletrodomesticos/frigorificos','RECAPTURE',
 'v2.0 참고12(0913) /f/marca/LG 제거 — 검색 색인 확인. Cloudflare 챌린지로 리스팅 미확인'),
('PT','Worten','WM','WASH','Máquinas de lavar roupa','Máquinas de Lavar Roupa',
 'https://www.worten.pt/grandes-eletrodomesticos/maquinas-de-roupa/maquinas-de-lavar-roupa','RECAPTURE',
 'v2.0 참고12(0913) /f/marca/LG 제거 — 검색 색인(Samsung·LG·Bosch 혼재) 확인. Cloudflare 로 리스팅 미확인'),
-- HU · MediaMarkt (시트 /v/lg-* 는 LG 브랜드관 — MMS 카테고리 노드로 교체)
('HU','MediaMarkt','REF','FRFR','Hűtőszekrények','Hűtőszekrény',
 'https://www.mediamarkt.hu/hu/category/hutoszekreny-504624.html','RECAPTURE',
 'v2.0 참고12(0913) /v/lg-hutoszekreny 는 LG 브랜드관 → MMS 카테고리 504624(검색 색인, GORENJE·SAMSUNG·LG 혼재). Cloudflare 로 미확인'),
('HU','MediaMarkt','WM','WASH','Mosógépek','Mosógép',
 'https://www.mediamarkt.hu/hu/category/mosogep-504636.html','RECAPTURE',
 'v2.0 참고12(0913) /v/lg-mosogep 는 LG 브랜드관 → MMS 카테고리 504636(검색 색인). Cloudflare 로 미확인'),
-- AE · Sharaf DG
('AE','SharafDG','REF','FRFR','Refrigerators','Refrigerators',
 'https://uae.sharafdg.com/c/home_appliances/fridges_freezers/refrigerators/','RECAPTURE',
 'v2.0 참고12(0913) dFR[Brand]=LG 제거 + 트리 정본 경로(검색 색인). Cloudflare 챌린지로 리스팅 미확인'),
('AE','SharafDG','WM','WASH','Washing Machines','Washing Machines',
 'https://uae.sharafdg.com/c/home_appliances/laundry/washing_machines/','RECAPTURE',
 'v2.0 참고12(0913) 시트 확인 필요 → 트리 정본 경로(검색 색인). Cloudflare 챌린지로 리스팅 미확인'),
-- EG · Cairo Sales (시트 manufacturer/lg.html 은 제조사 페이지 — GNB 카테고리로 교체)
('EG','CairoSales','REF','FRFR','ثلاجات','ثلاجات',
 'https://cairosales.com/ar/refrigerators/','CONFIRMED',
 'v2.0 참고12(0913) manufacturer/lg.html 은 제조사 페이지 → GNB 카테고리. 0915 실측 1,010 제품, 브랜드 혼재'),
('EG','CairoSales','WM','WASH','غسالات','غسالات ملابس و مجففات',
 'https://cairosales.com/ar/washers-dryers/','CONFIRMED',
 'v2.0 참고12(0913) manufacturer/lg.html 은 제조사 페이지 → GNB 카테고리(건조기 포함). 0915 실측 778 제품, 브랜드 혼재(Zanussi·Toshiba·LG)'),
-- SA · eXtra (시트 /lg/c/LG/facet/… 은 LG 브랜드숍 — 카테고리 리스트로 교체)
('SA','Extra','REF','FRFR','ثلاجات','Refrigerators',
 'https://www.extra.com/en-sa/large-appliances-/refrigerators/c/4-401','CONFIRMED',
 'v2.0 참고12(0913) /lg/c/LG/facet 은 브랜드숍 → 카테고리 c/4-401. 0915 실측 350 products, Selected Filters (0), 브랜드 혼재. cp/4-401 은 랜딩 허브'),
('SA','Extra','WM','WASH','غسالات','Washing Machines',
 'https://www.extra.com/en-sa/large-appliances-/washing-machines/c/4-403','CONFIRMED',
 'v2.0 참고12(0913) /lg/c/LG/facet 은 브랜드숍 → 카테고리 c/4-403. 0915 실측 165 products, 브랜드 혼재'),
-- MA · Electroplanet (시트 X: 리프만 리스팅 — GNB 노드는 허브)
('MA','Electroplanet','REF','FRFR','Réfrigérateurs','Réfrigérateur',
 'https://www.electroplanet.ma/gros-electromenager/refrigerateur','RECAPTURE',
 'v2.0 참고12(0913) 시트 X. GNB 노드는 허브(리스팅 없음, 0915 실측) — 리프(…/refrigerateur-avec-congelateur-en-bas 등)만 리스팅. EY 리프 선택 필요'),
('MA','Electroplanet','WM','WASH','Lave-linge','Machine à laver',
 'https://www.electroplanet.ma/gros-electromenager/machine-a-laver','RECAPTURE',
 'v2.0 참고12(0913) 시트 X. GNB 노드는 허브(리스팅 없음, 0915 실측) — 리프(…/machine-a-laver-a-hublot 등)만 리스팅. EY 리프 선택 필요'),
-- AU · Amazon (시트 확인 필요)
('AU','Amazon','REF','FRFR','Fridges','Fridges',
 'https://www.amazon.com.au/b/?node=7547932051','CONFIRMED',
 'v2.0 참고12(0913) 시트 확인 필요 → Home > Household Appliances > Fridges, Freezers & Ice Cube Makers > Fridges. 0915 /s?rh=n: 84 results(KR GLOW)'),
('AU','Amazon','WM','WASH','Washing Machines','Washing Machines',
 NULL,'RECAPTURE',
 'v2.0 참고12(0913) 시트 확인 필요. 0915 탐색: Household Appliances 하위에 세탁기 브라우즈 노드 없음(Toys 5031225051 뿐) — 검색 대안 /s?k=washing+machine. URL 확보 시 UPSERT'),
-- SG · Lazada (시트 X)
('SG','Lazada','REF','FRFR','Refrigerators','Refrigerators',
 'https://www.lazada.sg/shop-refrigerators/','RECAPTURE',
 'v2.0 참고12(0913) 시트 X → 카테고리 슬러그. 0915 타이틀 "Buy Refrigerators Online" 확인, 리스팅은 reCAPTCHA 로 미확인'),
('SG','Lazada','WM','WASH','Washing Machines','Washing Machines',
 'https://www.lazada.sg/shop-washing-machines/','RECAPTURE',
 'v2.0 참고12(0913) 시트 X → 카테고리 슬러그. 0915 타이틀 "Buy Washing Machines Online" 확인, 리스팅은 reCAPTCHA 로 미확인'),
-- TH · Lazada (시트 X)
('TH','Lazada','REF','FRFR','ตู้เย็น','ตู้เย็น',
 'https://www.lazada.co.th/shop-refrigerators/','RECAPTURE',
 'v2.0 참고12(0913) 시트 X → 카테고리 슬러그. 0915 타이틀 확인, 리스팅은 reCAPTCHA 로 미확인'),
('TH','Lazada','WM','WASH','เครื่องซักผ้า','เครื่องซักผ้า',
 'https://www.lazada.co.th/shop-washing-machines/','RECAPTURE',
 'v2.0 참고12(0913) 시트 X → 카테고리 슬러그. 0915 타이틀 확인, 리스팅은 reCAPTCHA 로 미확인'),
-- VN · Dien May Xanh (시트 /tu-lanh-lg 는 브랜드 필터 경로)
('VN','DienMayXanh','REF','FRFR','Tủ lạnh','Tủ lạnh',
 'https://www.dienmayxanh.com/tu-lanh','CONFIRMED',
 'v2.0 참고12(0913) /tu-lanh-lg 의 -lg 제거. 0915 실측 64 items, 브랜드 혼재(Toshiba·LG·Hitachi·Samsung)'),
('VN','DienMayXanh','WM','WASH','Máy giặt','Máy giặt',
 'https://www.dienmayxanh.com/may-giat','CONFIRMED',
 'v2.0 참고12(0913) /may-giat-lg 의 -lg 제거. 0915 실측 38 items, 브랜드 혼재'),
-- TW · Momoshop (시트 MgrpCategory m_code=2140900xxx 는 LG 브랜드관 — 家電 카테고리로 교체)
('TW','Momoshop','REF','FRFR','冰箱','冰箱',
 'https://www.momoshop.com.tw/categories/2919100000','CONFIRMED',
 'v2.0 참고12(0913) m_code=2140900003 은 LG 브랜드관 → 家電>冰箱(l_code 2919100000, /categories/ 로 301). 0915 실측 브랜드 혼재'),
('TW','Momoshop','WM','WASH','洗衣機','洗衣機/乾衣機',
 'https://www.momoshop.com.tw/categories/2900800000','CONFIRMED',
 'v2.0 참고12(0913) m_code=2140900002 는 LG 브랜드관 → 家電>洗衣機/乾衣機(l_code 2900800000). 0915 실측 브랜드 혼재')
ON DUPLICATE KEY UPDATE
    cat_cd     = VALUES(cat_cd),
    cat_sub_cd = VALUES(cat_sub_cd),
    gnb_label  = VALUES(gnb_label),
    gnb_url    = VALUES(gnb_url),
    status     = VALUES(status),
    note       = VALUES(note);
