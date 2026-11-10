## 호출 전 안내: Zyte (검색 수집 실험, WP1-1)

- 왜 부르나: OSM에 없는 12곳을 사람 손 없이 수집할 수 있는지, 곳별로 어느 방식이 되는지 확인한다
- 보내는 값:
  - 주소(url): 12곳의 검색 결과 1페이지. 아래 표 전체
  - 지역(geolocation): 리테일러 국가 코드. 아래 표 전체
  - 방식: H = {"httpResponseBody": true}; B0 = {"browserHtml": true}; B1 = {"browserHtml": true, "actions": [{"action": "scrollBottom"}]}
  - 인증: `.env`의 Zyte 키를 인증 머리글로만 보냄. 파일·로그에는 안 남김
- 규모·비용: 최대 36요청(HTML 12, 브라우저 24), 재시도 없음. 공개 단가로 약 $0.026 ~ $0.401. 묶음은 사이트별로 정해져 모름. 확장 지역 24요청·브라우저 동작 12요청의 추가 금액은 공개 문서에 없어 이 금액은 최소치. 성공 응답만 과금
- 실행 명령(승인 뒤):
  - `uv run --python 3.12 --with-requirements pipeline/requirements.txt python pipeline/run.py s1b --month 2026-11 --probe --run`

| 국가 | 리테일러 | 엑셀행 | 검색어 | 영어 뜻 | 지역 | 10월 1페이지 카드 | 10월 표시 전체 수 | 주소 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Netherlands | MEDIAMARKT | 98 | Amerikaanse koelkasten | side by side refrigerator | NL | 12 | (43 artikelen) | https://www.mediamarkt.nl/nl/search.html?query=Amerikaanse%20koelkasten&marketplace=MediaMarkt |
| Czech Republic | DATART | 118 | multi door lednice | french door refrigerator | CZ | 24 | (60) | https://www.datart.cz/vyhledavani?q=multi+door+lednice |
| Czech Republic | ALZA | 127 | multi door lednice | french door refrigerator | CZ | 24 | 28 položek | https://www.alza.cz/search.htm?exps=multi+door+lednice |
| Poland | MEDIAEXPERT | 136 | lodówka | refrigerator | PL | 30 | (1049) | https://www.mediaexpert.pl/search?query[menu_item]=&query[querystring]=lod%C3%B3wka |
| Poland | RTV_EURO_AGD | 146 | lodówka | refrigerator | PL | 20 | 1033 produkty | https://www.euro.com.pl/search2.bhtml?keyword=lod%C3%B3wka |
| UAE | Sharaf DG | 157 | bottom freezer refrigerator | bottom freezer refrigerator | AE | 48 | 75 | https://uae.sharafdg.com/?q=bottom%20freezer%20refrigerator&post_type=product |
| Hungary | Mediamarkt | 230 | felülfagyasztós hűtőszekrény | top freezer refrigerator | HU | 12 | 48 találat | https://www.mediamarkt.hu/hu/search.html?query=fel%C3%BClfagyaszt%C3%B3s%20h%C5%B1t%C5%91szekr%C3%A9ny |
| Portugal | Worten | 261 | frigorífico | refrigerator | PT | 50 | 1000+ produtos | https://www.worten.pt/search?query=frigor%C3%ADfico |
| Australia | Appliance Online | 345 | Front Load Washing Machines | front loader | AU | 24 | 128 filtered Products | https://www.appliancesonline.com.au/search/front+load+washing+machines/?currentpage=1&sortkey=highestrated |
| Peru | FALABELLA | 361 | Refrigeradora | refrigerator | PE | 53 | 5747 | https://www.falabella.com.pe/falabella-pe/search?Ntt=Refrigeradora |
| Egypt | Cairo Sales | 377 | ثلاجات Side by Side | Side by Side Refrigerators | EG | 2 | 2 | https://cairosales.com/ar/find?search_query=%D8%AB%D9%84%D8%A7%D8%AC%D8%A7%D8%AA+Side+by+Side |
| Morocco | Electroplanet | 392 | Lave-linge | Washing machine | MA | 3 | 3 results found | https://www.electroplanet.ma/#ada2/fullscreen/m=and&q=Lave-linge |

## 실험 결과

| 국가 | 리테일러 | 방식 | 받음 | API 상태 | 사이트 상태 | HTML 크기 | 차단 문구 | 10월 링크 보임 | 오류 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Netherlands | MEDIAMARKT | H | 예 | 200 | 200 | 1,917,267 |  | 6/12 |  |
| Netherlands | MEDIAMARKT | B0 | 예 | 200 | 200 | 1,879,884 |  | 6/12 |  |
| Netherlands | MEDIAMARKT | B1 | 예 | 200 | 200 | 1,955,552 |  | 6/12 |  |
| Czech Republic | DATART | H | 예 | 200 | 200 | 1,797,885 |  | 2/24 |  |
| Czech Republic | DATART | B0 | 아니오 | 520 |  | 0 |  | 0/24 | Website Ban |
| Czech Republic | DATART | B1 | 아니오 | 520 |  | 0 |  | 0/24 | Website Ban |
| Czech Republic | ALZA | H | 아니오 | 520 |  | 0 |  | 0/24 | Website Ban |
| Czech Republic | ALZA | B0 | 예 | 200 | 200 | 563,662 |  | 20/24 |  |
| Czech Republic | ALZA | B1 | 예 | 200 | 200 | 599,580 |  | 20/24 |  |
| Poland | MEDIAEXPERT | H | 예 | 200 | 200 | 1,023,898 |  | 27/30 |  |
| Poland | MEDIAEXPERT | B0 | 예 | 200 | 200 | 1,081,577 |  | 27/30 |  |
| Poland | MEDIAEXPERT | B1 | 예 | 200 | 200 | 1,848,691 |  | 28/30 |  |
| Poland | RTV_EURO_AGD | H | 아니오 | 520 |  | 0 |  | 0/20 | Website Ban |
| Poland | RTV_EURO_AGD | B0 | 예 | 200 | 200 | 3,117,779 |  | 5/20 |  |
| Poland | RTV_EURO_AGD | B1 | 예 | 200 | 200 | 3,116,745 |  | 5/20 |  |
| UAE | Sharaf DG | H | 예 | 200 | 200 | 252,395 |  | 0/48 |  |
| UAE | Sharaf DG | B0 | 예 | 200 | 200 | 714,159 |  | 44/48 |  |
| UAE | Sharaf DG | B1 | 예 | 200 | 200 | 713,276 |  | 44/48 |  |
| Hungary | Mediamarkt | H | 예 | 200 | 200 | 1,387,535 |  | 2/12 |  |
| Hungary | Mediamarkt | B0 | 예 | 200 | 200 | 1,423,832 |  | 2/12 |  |
| Hungary | Mediamarkt | B1 | 예 | 200 | 200 | 1,581,003 |  | 2/12 |  |
| Portugal | Worten | H | 예 | 200 | 200 | 630,099 |  | 0/50 |  |
| Portugal | Worten | B0 | 예 | 200 | 200 | 5,163,203 |  | 32/50 |  |
| Portugal | Worten | B1 | 예 | 200 | 200 | 5,198,927 |  | 32/50 |  |
| Australia | Appliance Online | H | 예 | 200 | 200 | 83,068 |  | 0/24 |  |
| Australia | Appliance Online | B0 | 예 | 200 | 200 | 1,069,944 |  | 16/24 |  |
| Australia | Appliance Online | B1 | 예 | 200 | 200 | 1,067,164 |  | 16/24 |  |
| Peru | FALABELLA | H | 아니오 | 520 |  | 0 |  | 0/53 | Website Ban |
| Peru | FALABELLA | B0 | 예 | 200 | 200 | 2,925,321 |  | 25/53 |  |
| Peru | FALABELLA | B1 | 예 | 200 | 200 | 2,930,207 |  | 25/53 |  |
| Egypt | Cairo Sales | H | 예 | 200 | 200 | 338,819 |  | 2/2 |  |
| Egypt | Cairo Sales | B0 | 예 | 200 | 200 | 381,242 |  | 2/2 |  |
| Egypt | Cairo Sales | B1 | 예 | 200 | 200 | 381,259 |  | 2/2 |  |
| Morocco | Electroplanet | H | 예 | 200 | 200 | 538,363 |  | 0/3 |  |
| Morocco | Electroplanet | B0 | 예 | 200 | 200 | 1,176,652 |  | 2/3 |  |
| Morocco | Electroplanet | B1 | 예 | 200 | 200 | 1,175,701 |  | 2/3 |  |
