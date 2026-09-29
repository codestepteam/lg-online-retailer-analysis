-- Migration 047: gnb_keyword_map — 필터형 16행을 참고12 무필터 정본으로 교체
--
-- 배경 (2026-08-20, EY ID3 크롤링 데이터 오류 수정 요청 메일)
--   ID3(GNB 카테고리 진입) URL 은 진단항목 엑셀 [참고12](v1.8 0807 갱신, v1.9 0814 유지)의
--   무필터 순수 카테고리 URL 이 정본. 자사+경쟁사 필터가 걸린 URL 은 OTHERS 브랜드를
--   모수에서 제거해 자사·경쟁사 진단값이 과대측정된다 (EY 지적 원문 그대로).
--   지정 경쟁브랜드 외 제품은 리포트 계층에서 OTHERS 분류(core/brand_match) — CZ Alza 와
--   동일 기준으로 전 리테일러 통일.
--
--   경위: 0721 gnb_dataset2.xlsx(필터 포함 원본)를 mig 032 가 그대로 시딩 →
--   mig 040(0810)은 참고12 대조에서 신규 6행만 추가하고 기존 필터형은 "기커버"로 유지 →
--   0819 질의에서도 "경쟁 구도 내 노출 취지, 현행 유지"로 회신 → EY 0820 메일로 공식 뒤집힘.
--   대상 16행 = ES ECI 3(WM/REF/DW)·ES MediaMarkt 3 / FR Darty 2·Boulanger 2 /
--   IT Mediaworld 2 / SE Elgiganten 2 / PL MediaExpert 2. 무필터 12행(CZ·NL·IT Unieuro·
--   PL RTV)은 불변. 구 URL 은 이 파일과 mig 032 에 기록돼 있어 별도 백업 테이블 없음
--   (mig 046 에서 gnb 백업 테이블 정리한 방침 유지).
--
--   ⚠️ gnb_uuid(폴더명 gnb_{uuid5(url)})가 URL 파생이라, 기존 배치에서 재수집할 땐
--   구 URL 레코드(crawl+parse 양쪽)를 먼저 지워야 ID3 행이 이중 방출되지 않는다.
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/047_gnb_keyword_map_ref12_unfiltered.sql
-- 멱등: gnb_url 정확 일치 UPDATE — 재실행 시 0행.

-- ES Elcorteingles_electronica (3)
UPDATE gnb_keyword_map SET gnb_url = 'https://www.elcorteingles.es/electrodomesticos/lavadoras/',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.elcorteingles.es/electrodomesticos/lavadoras/brand::Bosch,,Samsung,,LG,,Hisense/';
UPDATE gnb_keyword_map SET gnb_url = 'https://www.elcorteingles.es/electrodomesticos/frigorificos-y-neveras/',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.elcorteingles.es/electrodomesticos/frigorificos-y-neveras/brand::Samsung,,Bosch,,LG,,Hisense/';
UPDATE gnb_keyword_map SET gnb_url = 'https://www.elcorteingles.es/electrodomesticos/lavavajillas/',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.elcorteingles.es/electrodomesticos/lavavajillas/brand::Bosch,,Samsung,,Beko,,LG,,Balay/';

-- ES MediaMarkt (3)
UPDATE gnb_keyword_map SET gnb_url = 'https://www.mediamarkt.es/es/category/lavadoras-671.html',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.mediamarkt.es/es/category/lavadoras-671.html?brand=HISENSE%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG';
UPDATE gnb_keyword_map SET gnb_url = 'https://www.mediamarkt.es/es/category/frigor%C3%ADficos-554.html',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.mediamarkt.es/es/category/frigor%C3%ADficos-554.html?brand=HISENSE%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG';
UPDATE gnb_keyword_map SET gnb_url = 'https://www.mediamarkt.es/es/category/lavavajillas-660.html',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.mediamarkt.es/es/category/lavavajillas-660.html?brand=HISENSE%20OR%20BEKO%20OR%20LG%20OR%20BOSCH%20OR%20BALAY';

-- FR Darty (2) — 무필터 cat 리스트는 소모품 혼입(참고12 비고: 3,168건) 있으나 EY 지시대로 원본 사용
UPDATE gnb_keyword_map SET gnb_url = 'https://www.darty.com/nav/extra/list?cat=12428',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.darty.com/nav/extra/list?cat=12428&m=BOSCH-LG-HISEN-SAMSU';
UPDATE gnb_keyword_map SET gnb_url = 'https://www.darty.com/nav/extra/list?cat=23561',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.darty.com/nav/extra/list?cat=23561&m=HAIER-LG-HISEN-SAMSU';

-- FR Boulanger (2)
UPDATE gnb_keyword_map SET gnb_url = 'https://www.boulanger.com/c/nav-filtre/lave-linge',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.boulanger.com/c/nav-filtre/lave-linge?brand%7Ebosch%7Cbrand%7Ehisense%7Cbrand%7Elg%7Cbrand%7Esamsung=';
UPDATE gnb_keyword_map SET gnb_url = 'https://www.boulanger.com/c/nav-filtre/refrigerateur',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.boulanger.com/c/nav-filtre/refrigerateur?brand~haier|brand~hisense|brand~lg|brand~samsung';

-- IT Mediaworld (2)
UPDATE gnb_keyword_map SET gnb_url = 'https://www.mediaworld.it/it/category/lavatrici-6001.html',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.mediaworld.it/it/category/lavatrici-6001.html?brand=HISENSE%20OR%20HAIER%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG';
UPDATE gnb_keyword_map SET gnb_url = 'https://www.mediaworld.it/it/category/frigoriferi-6004.html',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.mediaworld.it/it/category/frigoriferi-6004.html?brand=HISENSE%20OR%20HAIER%20OR%20BOSCH%20OR%20LG%20OR%20SAMSUNG';

-- SE Elgiganten (2)
UPDATE gnb_keyword_map SET gnb_url = 'https://www.elgiganten.se/vitvaror/tvatt-tork/tvattmaskin',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.elgiganten.se/vitvaror/tvatt-tork/tvattmaskin?1%7Cbrand%5B%5D=Bosch&1%7Cbrand%5B%5D=Electrolux&1%7Cbrand%5B%5D=LG&1%7Cbrand%5B%5D=Samsung';
UPDATE gnb_keyword_map SET gnb_url = 'https://www.elgiganten.se/vitvaror/kyl-frys/kylskap',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.elgiganten.se/vitvaror/kyl-frys/kylskap?1%7Cbrand%5B%5D=Electrolux&1%7Cbrand%5B%5D=Bosch&1%7Cbrand%5B%5D=LG&1%7Cbrand%5B%5D=Hisense&1%7Cbrand%5B%5D=Samsung';

-- PL MediaExpert (2)
UPDATE gnb_keyword_map SET gnb_url = 'https://www.mediaexpert.pl/agd/pralki-i-suszarki/pralki',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.mediaexpert.pl/agd/pralki-i-suszarki/pralki/bosch.lg.samsung.electrolux.hisense';
UPDATE gnb_keyword_map SET gnb_url = 'https://www.mediaexpert.pl/agd/lodowki-i-zamrazarki/lodowki',
  note = 'v1.9 참고12(0814) 무필터 정본 — EY 0820 ID3 지적 반영'
  WHERE gnb_url = 'https://www.mediaexpert.pl/agd/lodowki-i-zamrazarki/lodowki/popularne-serie_lg.samsung.hisense.bosch.haier';
