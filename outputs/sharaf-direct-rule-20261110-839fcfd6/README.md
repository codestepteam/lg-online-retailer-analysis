# Sharaf DG PDP 모수의 직판 토글 필수 수집 반영

2026-11-10 사용자 결정 D127. Sharaf DG의 상품 상세 페이지 진단 대상 URL을 모으는 검색은 `Sold By Sharaf DG`(Sharaf DG 직판) 토글을 켠 조건으로 진행한다. 모든 검색어·페이지에 같은 조건을 유지한다. 매일 검색 노출 순위를 진단하는 별도 PLP 수집 설정은 이번 변경 범위가 아니다.

## 규칙과 관찰 근거

- 사용자 결정: 직판 토글 ON을 리테일러 규칙과 자동 수집 설정에 반영한다. 직판 토글을 적용한 뒤에도 정확한 본 상품의 `Sold by`(판매자)를 재확인한다. 추천 상품·다른 판매자 목록·`Fulfilled by`(배송 주체)·HTML 첫 판매자값으로 대신하지 않는다.
- 직접 관찰: 같은 상품도 `promo`로 구분되는 판매 제안마다 판매자가 다를 수 있다. 보쉬 KIV87NSE0M의 `promo=3933323`은 11월 5일 Applianzee, `promo=4037795`는 11월 10일 Sharaf DG로 확인했다. 모든 promo가 서로 다른 판매자라는 뜻은 아니며, 서로 다른 날짜의 관찰로 10월 당시 상태를 소급 확정하지 않는다. [기존·직판 URL 대조](../sharaf-157-v7-20261110-e02f39e3/included-increase-trace.json).
- URL 보존: 상품 카드에서 수집한 정확한 `?promo=` 주소를 저장·요청한다. 검색 목록에 적용하는 직판 조건을 개별 상품 주소에 덧붙이지 않는다.

## 설정과 호출 경로

[11월 검색 설정](../../pdp%20모수%20자동화/runs/2026-11/config/search_urls.json)의 `UAE|Sharaf DG` 항목에 시작 주소와 `required_query_params`를 넣었다. 직판 토글 ON에서 관찰한 두 조건은 `dFR[promotion_offer_json.seller_code][0]=sdg`, `dFR[promotion_offer_json.seller_code][1]=sdg_online_excl`이다. 10월의 무필터 `october_arrivals`는 과거 기록으로 보존한다. 이 파일은 사람이 유지하고, S0는 targets·brands·search_terms·keywords만 생성하므로 새 설정을 덮어쓰지 않는다. 다음 달 회차를 준비할 때도 이 직판 설정을 이어 사용한다.

[리테일러 설정](../../pdp%20모수%20자동화/runs/2026-11/config/retailer_rules.json)의 Sharaf 설명 항목은 수집 규칙·promo 관찰·실행 설정의 위치를 명시한다. 실행에 쓰는 필드는 `search_urls.json`의 `required_query_params`이며, 설명 필드는 실행 플래그가 아니다.

[검색 수집 코드](../../pdp%20모수%20자동화/pipeline/s1b_search.py)의 소비 경로는 다음과 같다.

1. `main`이 회차의 search_urls·search_terms를 읽는다. 수집 방식 실험은 `plan_requests → start_url`, 본 수집·시험 수집은 `plan_collection → run_collection → collect_term → term_start`로 시작 주소를 만든다.
2. `start_url`, 과거 도착 주소를 쓰는 `term_start`, `page_url`, 실제 요청 직전 `fetch_page`에서 필수 검색 조건을 유지한다. 다음 페이지에서 누락·잘못된 인코딩 값이 들어와도 동일 직판 조건을 복원한다.
3. 응답 도착 URL에 필수 직판 조건이 없으면 정상 원본으로 채택하지 않고, 기존 재시도 한도 뒤 수집 실패로 기록한다. 이 검사는 응답 URL 조건 검사이며, 새 Zyte 실행의 화면 내용까지 검증한 것은 아니다.
4. 필수 조건을 쓰는 곳은 시작 주소의 해시를 포함한 이어받기 키를 쓴다. 과거 무필터 페이지·실험 기록을 재사용하지 않는다. 이미 만들어진 무필터 후보 CSV도 완료 결과로 건너뛰지 않고 안내 오류를 내며, 파일을 삭제·자동 덮어쓰지 않는다.
5. `parse_page → card_link → card_rows`는 개별 상품의 `?promo=` 주소를 보존한다. S3 상세 수집도 후보의 정확한 URL을 계획·요청한다. 본 상품 판매자 재확인은 기존 기준을 유지한다.

## 변경 전후

| 항목 | 변경 전 | 변경 후 |
| --- | --- | --- |
| Sharaf DG 검색 시작 | 검색어·상품 검색 종류만 지정 | 직판 토글 ON과 동일한 두 판매자 조건 지정 |
| 다음 페이지 | 도착 주소에 페이지 번호 추가 | 직판 조건을 유지·복원하고 페이지 번호 추가 |
| 응답의 직판 조건 유실 | 일반 결과로 처리 가능 | 실패로 기록 |
| 무필터 과거 기록 | 동일 검색어·페이지 키로 재사용 가능 | 요청 조건별로 구분, 무필터 CSV 재사용 거부 |
| 개별 상품 promo | 보존 | 보존 유지, 시험으로 확인 |

## 무료 검증과 실행 범위

실행 위치는 `pdp 모수 자동화/pipeline`, Python은 `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python`이다.

| 명령·검사 | 결과 |
| --- | --- |
| `python -B -m unittest discover -s tests -p test_s1b_search.py -v` | 65개, OK |
| `python -B -m unittest discover -s tests -q` | 317개, 14.493초, OK |
| 설정을 읽어 실제 주소 생성 함수를 실행 | Sharaf DG 검색어 9개 전체의 첫/다음 페이지에 직판 두 조건·원래 검색어 유지 |

새 가짜 입력 시험 8개는 검색어 9개·실험 요청, 누락/잘못된 인코딩 조건 복원, 과거 도착 주소, 무필터 캐시 분리·직판 캐시 이어받기, 조건 변경 키 분리, 요청·상품 promo 보존, 응답 조건 유실 실패, 무필터 기존 CSV 거부·원본 보존을 검사했다. 네트워크 호출 함수는 가짜 응답으로 대체했다.

[검증 JSON](verification.json)에 9개 검색어의 실제 생성 주소·변경 전후·검사 명령·파일 해시를 저장했다. 기존 회귀 검사에는 다른 리테일러와 모수 전체 단계가 포함된다. 실제 Zyte 호출 0회이며, 현재 사이트에서 새 자동 수집을 실행한 결과·배포·운영 반영은 아니다. 기존 v7 CSV도 수정하지 않았다.
