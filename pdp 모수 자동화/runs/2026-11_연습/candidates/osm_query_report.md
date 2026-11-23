## 호출 전 안내: BigQuery (lgops → 콘솔 서버)

- 왜 부르나: 이번 회차 OSM 보유 리테일러의 PDP 후보 URL을 가져옵니다(S1a). 조회만 하고 데이터를 바꾸지 않습니다.
- 보내는 값:
  - 요청 기준일: 2026-11-17 (이 날까지 최근 30일 중 수집량이 충분한 가장 최근 날을 리테일러별로 자동 선택)
  - 조회 테이블: pjt-lge-oned.L1_ONED.TRPURC_OSM_PRODUCT_DAILY_L, pjt-lge-oned.L2_ONED.VSMRKT_DAILY_OSM_BANR_VSBLT_D, pjt-lge-oned.L2_ONED.VSMRKT_DAILY_OSM_SALE_RK_D
  - 쿼리 옵션: pdp_view=audit, pdp_filter_mode=False (전체 행과 판정 표시를 받고, 콘솔 제외 필터는 끔)
  - 대상: 23곳: Spain ELCORTEINGLES_ELECTRONICA, Spain MEDIAMARKT, France DARTY, France BOULANGER, Italy MEDIAWORLD, Italy AMAZON, Italy UNIEURO, Netherlands COOLBLUE, Sweden ELGIGANTEN, Germany AMAZON, Germany MEDIAMARKT, Germany OTTO, United Kingdom AO, United Kingdom CURRYS, Canada COSTCO, Chile FALABELLA, Mexico LIVERPOOL, Brazil MAGAZINELUIZA, Saudi Arabia EXTRA, Singapore LAZADA, Thailand LAZADA, Taiwan MOMOSHOP, Vietnam DIENMAYXANH
  - 제품군·브랜드: 리테일러·제품군 73줄, 브랜드 342개 (곳별 표는 아래)
  - 콘솔 대상에 더한 제품군: 9곳 — Canada COSTCO DRY, Chile FALABELLA DRY, Mexico LIVERPOOL DRY, Brazil MAGAZINELUIZA DRY, SaudiArabia EXTRA DRY, Singapore LAZADA DRY, Thailand LAZADA DRY, Taiwan MOMOSHOP DRY, Vietnam DIENMAYXANH DRY
  - SQL: /Users/codestepseunghee/codestep/lg-online-retailer-analysis/pdp 모수 자동화/runs/2026-11/candidates/osm_query.sql (18,541자, 지문 55cdbdb49346)
- 규모·비용: 처리량은 `--estimate`로 확인합니다(이 안내만으로는 호출하지 않습니다). 실제 요금은 LG 계정 청구 방식을 확인하지 못했습니다.
- 실행 명령(승인 뒤):
  - `python pipeline/run.py s1a --month 2026-11 --end-date 2026-11-17 --estimate`
  - `python pipeline/run.py s1a --month 2026-11 --end-date 2026-11-17 --run`

# OSM 쿼리 생성 보고 (요청 기준일 2026-11-17)

- SQL 길이: 18,541자 (한도 20,000자)
- 대상: 23곳, 리테일러·제품군 73줄
- 콘솔 브랜드 목록에 없어 EY 시트·#110에서 더한 줄: 6줄, 브랜드 10개
- 콘솔 대상에 없어 더한 제품군(후보로만 뽑고 기준일 선정에는 안 씀): 9곳 — Canada COSTCO DRY, Chile FALABELLA DRY, Mexico LIVERPOOL DRY, Brazil MAGAZINELUIZA DRY, SaudiArabia EXTRA DRY, Singapore LAZADA DRY, Thailand LAZADA DRY, Taiwan MOMOSHOP DRY, Vietnam DIENMAYXANH DRY

| 국가 | 리테일러 | 제품군 | 콘솔 수 | 시트 수 | 더한 브랜드 | 콘솔에만 있는 브랜드(S2에서 거름) |
| --- | --- | --- | ---: | ---: | --- | --- |
| Spain | ELCORTEINGLES_ELECTRONICA | W/M | 4 | 4 |  |  |
| Spain | ELCORTEINGLES_ELECTRONICA | REF | 4 | 4 |  |  |
| Spain | ELCORTEINGLES_ELECTRONICA | D/W | 5 | 5 |  |  |
| Spain | ELCORTEINGLES_ELECTRONICA | DRY | 4 | 4 |  |  |
| Spain | MEDIAMARKT | W/M | 4 | 4 |  |  |
| Spain | MEDIAMARKT | REF | 4 | 4 |  |  |
| Spain | MEDIAMARKT | D/W | 5 | 5 |  |  |
| Spain | MEDIAMARKT | DRY | 4 | 4 |  |  |
| France | DARTY | W/M | 4 | 4 |  |  |
| France | DARTY | REF | 4 | 4 |  |  |
| France | DARTY | DRY | 4 | 4 |  |  |
| France | BOULANGER | W/M | 4 | 4 |  |  |
| France | BOULANGER | REF | 4 | 4 |  |  |
| France | BOULANGER | DRY | 4 | 4 |  |  |
| Italy | MEDIAWORLD | W/M | 5 | 5 |  |  |
| Italy | MEDIAWORLD | REF | 5 | 5 |  |  |
| Italy | MEDIAWORLD | DRY | 5 | 5 |  |  |
| Italy | AMAZON | W/M | 5 | 5 |  |  |
| Italy | AMAZON | REF | 5 | 5 |  |  |
| Italy | AMAZON | DRY | 5 | 5 |  |  |
| Italy | UNIEURO | W/M | 5 | 5 |  |  |
| Italy | UNIEURO | REF | 5 | 5 |  |  |
| Italy | UNIEURO | DRY | 5 | 5 |  |  |
| Netherlands | COOLBLUE | W/M | 4 | 4 |  |  |
| Netherlands | COOLBLUE | REF | 4 | 4 |  |  |
| Netherlands | COOLBLUE | DRY | 4 | 4 |  |  |
| Sweden | ELGIGANTEN | W/M | 5 | 5 |  |  |
| Sweden | ELGIGANTEN | REF | 5 | 5 |  |  |
| Sweden | ELGIGANTEN | DRY | 5 | 5 |  |  |
| Germany | AMAZON | REF | 6 | 4 | LIEBHERR, SAMSUNG | EXQUISIT, KLARSTEIN, BOMANN, SIEMENS |
| Germany | AMAZON | W/M | 6 | 4 |  | AEG, CECOTEC |
| Germany | AMAZON | DRY | 4 | 4 |  |  |
| Germany | MEDIAMARKT | REF | 6 | 4 |  | EXQUISIT, BOMANN |
| Germany | MEDIAMARKT | W/M | 6 | 4 |  | BAUKNECHT, AEG |
| Germany | MEDIAMARKT | DRY | 4 | 4 |  |  |
| Germany | OTTO | REF | 6 | 4 | SAMSUNG | EXQUISIT, SIEMENS, AMICA |
| Germany | OTTO | W/M | 6 | 4 | SAMSUNG | AEG, BAUKNECHT, BEKO |
| Germany | OTTO | DRY | 4 | 4 |  |  |
| United Kingdom | AO | REF | 6 | 4 | BOSCH | SMEG, BEKO, RUSSELLHOBBS |
| United Kingdom | AO | W/M | 6 | 4 | BOSCH, HISENSE, SAMSUNG | HOOVER, HOTPOINT, BEKO, AEG, HAIER |
| United Kingdom | AO | DRY | 4 | 4 |  |  |
| United Kingdom | AO | D/W | 3 | 0 |  | LG, BOSCH, HISENSE |
| United Kingdom | CURRYS | REF | 6 | 4 |  | BEKO, HAIER |
| United Kingdom | CURRYS | W/M | 6 | 4 | BOSCH, HISENSE | HOOVER, HOTPOINT, BEKO, HAIER |
| United Kingdom | CURRYS | DRY | 4 | 4 |  |  |
| United Kingdom | CURRYS | D/W | 3 | 0 |  | LG, BOSCH, HISENSE |
| Canada | COSTCO | W/M | 5 | 5 |  |  |
| Canada | COSTCO | REF | 5 | 5 |  |  |
| Canada | COSTCO | DRY | 5 | 5 |  |  |
| Chile | FALABELLA | W/M | 4 | 4 |  |  |
| Chile | FALABELLA | REF | 4 | 4 |  |  |
| Chile | FALABELLA | DRY | 4 | 4 |  |  |
| Mexico | LIVERPOOL | W/M | 4 | 4 |  |  |
| Mexico | LIVERPOOL | REF | 4 | 4 |  |  |
| Mexico | LIVERPOOL | DRY | 4 | 4 |  |  |
| Brazil | MAGAZINELUIZA | W/M | 5 | 5 |  |  |
| Brazil | MAGAZINELUIZA | REF | 5 | 5 |  |  |
| Brazil | MAGAZINELUIZA | DRY | 5 | 5 |  |  |
| Saudi Arabia | EXTRA | W/M | 4 | 4 |  |  |
| Saudi Arabia | EXTRA | REF | 4 | 4 |  |  |
| Saudi Arabia | EXTRA | DRY | 4 | 4 |  |  |
| Singapore | LAZADA | W/M | 4 | 4 |  |  |
| Singapore | LAZADA | REF | 4 | 4 |  |  |
| Singapore | LAZADA | DRY | 4 | 4 |  |  |
| Thailand | LAZADA | W/M | 4 | 4 |  |  |
| Thailand | LAZADA | REF | 4 | 4 |  |  |
| Thailand | LAZADA | DRY | 4 | 4 |  |  |
| Taiwan | MOMOSHOP | W/M | 4 | 4 |  |  |
| Taiwan | MOMOSHOP | REF | 4 | 4 |  |  |
| Taiwan | MOMOSHOP | DRY | 4 | 4 |  |  |
| Vietnam | DIENMAYXANH | W/M | 5 | 5 |  |  |
| Vietnam | DIENMAYXANH | REF | 4 | 4 |  |  |
| Vietnam | DIENMAYXANH | DRY | 5 | 5 |  |  |
