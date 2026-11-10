# 보쉬 KIV87NSE0M 토글 원인 설명 재검증

11월 10일 같은 세션에서 기존 검색어 `bottom freezer refrigerator`(하단 냉동실 냉장고)를 검색하고, 브랜드 선택 없이 직판 토글 OFF와 ON의 본 목록 1페이지를 대조했다.

- OFF: 표시 전체 76개, 관찰한 첫 페이지 48개 중 Sharaf DG 20개·외부 판매자 28개. 보쉬 KIV87NSE0M은 `promo=4037795`, Sharaf DG 직판이었다.
- ON: 표시 전체 52개, 관찰한 첫 페이지 48개 모두 Sharaf DG. 같은 보쉬 상품의 SKU·promo URL은 OFF와 동일했다.
- 기존 `promo=3933323` 상세를 다시 열면 본 상품 판매자는 Applianzee이고, 같은 화면 `Other Sellers`(다른 판매자)에 Sharaf DG `promo=4037795` 링크가 있었다. 그 링크를 눌러 본 상품 판매자가 Sharaf DG인 것도 확인했다.

따라서 ‘토글 OFF라 외부 판매자 것만 보였다’는 표현은 부정확하다. 10월28일 기존 카드의 promo 주소, 11월5일 그 URL의 외부 판매자 확인, 11월10일 직판 URL 확인은 서로 다른 시점이다. 10월 당시의 상세 HTML·동시 토글 전후 비교가 없어 당시 원인을 토글 미적용 하나로 확정할 수 없다. 이전 대외 설명 초안의 그 인과 단정은 정정한다.

확인된 사실은 기존 확보 URL을 외부 판매자로 확인해 제외했고, 재조사에서 직판 URL을 확보했다는 것이다. 직판 토글 ON 필수 규칙(D127)과 같은 제품의 promo별 판매자 차이는 이번 확인과 모순되지 않는다. 기존 v7 CSV·숫자·자동 수집 설정은 수정하지 않았다.

[검증 결과](verification.json) · [토글 전후 본 목록 기록](search-observations.json) · [두 판매 제안 상세 기록](pdp-observations.json) · [두 판매자가 함께 보이는 화면](two-offers.jpg). 체크 상태·카드 판매자 속성·동일 SKU/URL·두 상세 본 상품 판매자·다른 판매자 링크를 대조한 Python assertion 검사에서 실패 0개다.
