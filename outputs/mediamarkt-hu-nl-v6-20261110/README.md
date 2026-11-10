# 헝가리·네덜란드 MediaMarkt PDP 제목·판매자 검사와 공유용 v6

2026-11-10, 사용자 결정 D124. 승인된 **546개 PDP를 모두 수집·재판정했고 실패·미확인 0개, 네덜란드 4개 추가 제외를 반영한 공유용 v6 생성·전수 대조를 완료했다.**

후속 확인 정정: 위 재판정은 **제목·판매자 조건에 한정**된다. 헝가리 저장 원문을 판매 상태까지 독립 재검토한 결과, 기존 영구품절 기준에 해당하는 포함 2개를 추가로 발견했다. 따라서 헝가리 전체 조건에서 아무 정정도 필요 없다는 뜻으로 읽으면 안 된다. v6·v7 파일은 아직 바꾸지 않았고, 아래 후속 검증에 두 정정 대상을 기록했다.

## 적용 규칙

검색 결과 카드에서 받은 상품명만 검사하지 않고, PDP를 직접 수집한 HTML의 본 상품 제목(h1)을 다시 검사한다. 본 상품의 판매·배송 문구 뒤 판매자가 MediaMarkt 이외면 제외한다. 단순 문구 존재, 숨은 스크립트의 문구, 추천·비교·다른 상품의 판매자는 이 화면 검사의 제외 근거로 삼지 않는다. 화면 문구가 없으면 기존 본 상품 ID에 연결된 내부 판매자 검사로 판단하며, 문구가 있는데 판매자를 읽지 못하면 확인불가로 둔다.

다음 월간 수집에서는 MediaMarkt 스페인·독일·헝가리·네덜란드 4곳 모두에 적용한다. 브랜드·제품군 등 앞 단계에서 이미 제외되지 않은 후보는 OSM 보유·검색 수집 경로에 관계없이 S3에서 직접 PDP를 연 뒤 S4에서 국가별 제목·본 상품 판매자 규칙을 적용한다. OSM에 있으면 PDP 검사를 생략하는 예외는 없다. `test_mediamarkt_all_countries.py`의 4개 시험으로 방문 계획·네 나라 제목·판매자 검사·추천 영역 보조 검사 차단을 확인했다.

| 국가 | PDP 제목 단어(대소문자 구분 없음) | 본 상품 판매자 문구 |
| --- | --- | --- |
| 헝가리 | `felújított`(재생품), `refurbished`(리퍼비시품), `használt`(중고품), `used`(중고), `pre-owned`(중고), `open-box`(개봉품), `outlet`(아웃렛) | `Értékesítő és szállító`(판매 및 배송: …) |
| 네덜란드 | `tweedekans`, `tweede kans`(둘 다 두 번째 기회 상품), `refurbished`(리퍼비시품), `outlet`(아웃렛) | `Verkoop en verzending door`, `Verzonden en verkocht door`(둘 다 판매 및 배송: …) |

제목 단어는 기존 EY v2.2 `제외키워드(리리부)` 국가별 리퍼비시·리셀 항목을 사용한다. 이 항목에는 중고·개봉품·아웃렛도 들어 있다. 부품 항목을 리퍼·중고로 재분류하지 않았다. 제목의 단어와 사양표의 부정 표현(예: `Felújított: Nem`, 재생품: 아니오)은 구분한다.

화면 문구 근거: [헝가리 MediaMarkt 상품 페이지](https://www.mediamarkt.hu/hu/product/_delonghi-stilosa-ec230bk-eszpresszo-kavefozo-fekete-168295457.html), [네덜란드 MediaMarkt 리퍼 상품 안내](https://www.mediamarkt.nl/nl/specials/refurbished-producten). 읽기 전용 웹 조회에서 문구를 확인했으며, 이 페이지들은 대상 가전 546개의 전수 확인 결과가 아니다. 일반 HTTP로 원문 저장을 시도한 두 요청은 403으로 거절됐다. 헝가리의 별도 PDP 판매자 문구 검사는 이번에 추가했고, 네덜란드는 기존 특정 HTML 형식의 판매자 문구 검사보다 적용 위치와 제목 검사를 보강했다.

## 코드·설정

- [화면 검사 함수](../../pdp%20모수%20자동화/pipeline/rules/sellers/mediamarkt_screen.py): 헝가리·네덜란드와 스페인의 제목·본 상품 판매 영역 검사, 내부값 보조 판정. 독일은 기존 전용 화면 검사 함수를 유지한다.
- [11월 규칙 설정](../../pdp%20모수%20자동화/runs/2026-11/config/retailer_rules.json): 두 나라 함수 연결 및 현지어 규칙.
- [새 규칙 시험](../../pdp%20모수%20자동화/pipeline/tests/test_mediamarkt_screen.py): 가짜 HTML로 제목 차이·내부값과 화면값 충돌·추천 오탐 등을 확인한다.
- [v6 준비·수집·생성 코드](review_v6.py): 기본 실행은 무료 미리보기, `--execute`만 유료 호출, `--build`는 저장 HTML만 사용한다.

## 입력·출력·유료 실행 미리보기

입력은 `pdp 모수 추출/최종_20261029/PDP모수_공유용_v5_독일MediaMarkt13건제외반영_25개국_35개리테일러_전체판정_55997행_20261106.csv`다. 전체 55,997행·26열에서 헝가리 268·네덜란드 278개의 기존 포함 주소만 재검사한다. 기존 제외 상품을 다시 포함으로 바꾸는 조사는 아니다.

[plan.json](plan.json)에 546주소·원본 및 규칙·판정 코드의 SHA-256(내용 일치 확인용 해시)·요청 예시를 저장했다. [rules_snapshot.json](rules_snapshot.json)은 이 조사에 사용할 규칙 복사본이다. 원본 v5의 SHA-256은 `3d495f74f99f92218e8b47de30cfd71976bd90f9eabd7b98e8bb098b72c5e6b1`이다.

수집 중 가짜 입력에서 기존 보조 파서가 추천 판매자 문구를 다시 읽는 오탐을 찾아 차단했고, 스페인도 본 상품 영역 검사에 연결했다. 네덜란드의 이미 제외되는 판매 제안에서 본 상품 `Refurbished: Zeer goed`(리퍼비시: 매우 좋음)가 확인된 경우 사유를 외부판매자와 구분해 리퍼·중고로 적도록 보완했다. 원래 계획·코드·설정은 `plan_initial.json`·`parser_initial/`·`rules_snapshot_initial.json`에 보존하고 [보완 이력](parser_corrections.json)과 최종 코드·설정 해시를 기록했다. 승인된 546주소·요청 방식·호출 수·재시도 0회는 그대로다.

- Zyte `browserHtml=true`를 URL별 1회, 총 **546회**, 재시도 없이 호출한다. `actions`·스크린샷·유료 자동 추출·확장 지역 옵션은 쓰지 않는다.
- [2026-11-10 공개 종량제 단가](https://www.zyte.com/pricing/)의 브라우저 1,000회당 $1.01~$16.08로 계산한 기본 예상 비용은 **$0.55146~$8.77968**이다. 실제 사이트 등급·계정 할인·청구액은 미확인이다.
- 새 확인시각은 11월이며, CSV의 원본 목록 기준일과 상품명은 그대로 보존한다. 현재 화면 상태를 10월 당시 화면 상태로 설명하지 않는다.
- 수집 기록 [requests.jsonl](requests.jsonl) 546개, `html/*.html.gz` 원문 546개, [전체 재판정](PDP재확인.csv) 546행, [변경 대상](변경대상.csv) 4행을 저장했다. [실패 목록](실패목록.csv)은 머리글만 있고 데이터 0행이다. 미확인·실패가 하나라도 있으면 v6를 생성하지 않는 검사도 유지했다.
- 같은 최종 폴더에 [공유용 v6](../../pdp%20모수%20추출/최종_20261029/PDP모수_공유용_v6_헝가리네덜란드MediaMarkt규칙반영_25개국_35개리테일러_전체판정_55997행_20261110.csv)를 새로 썼다. v5의 55,997행·행 순서·26열과 나머지 행을 보존했으며 확인된 제외 4행만 바꿨다. v5 및 이전 파일은 수정하지 않았다.

## 실제 실행 결과와 v5 대조

브라우저 렌더링 HTML 요청은 2026-11-10 13:22:33~13:45:27 KST에 **546회, 재시도 0회** 실행했다. 실제 청구액은 응답에 없어서 확인하지 못했다. 원본 목록의 기준일·상품명은 보존했으며 이 결과는 10월 당시 상태를 증명하지 않는다.

| 범위 | 검사한 v5 포함 | 추가 제외 | v6 포함 |
| --- | ---: | ---: | ---: |
| 헝가리 MediaMarkt | 268 | 0 | 268 |
| 네덜란드 MediaMarkt | 278 | 4 | 274 |
| 전체 파일 | 10,215 | 4 | 10,211 |

전체 제외는 **45,782→45,786**이다. 제목 단어로 새로 제외된 상품은 두 나라 모두 0개다. 추가 제외는 아래 네덜란드 4개이며 모두 본 상품 판매 문구·판매자 링크를 확인했다.

| CSV 행번호 | 모델 | 현재 본 상품 판매자 | 제외 구분 |
| --- | --- | --- | --- |
| 12136 | LG GSLE81PYBD | You Get - Innovation and Technology NL | 외부판매자 |
| 12222 | LG GBBS322APY | DoppenbergKeukens B.V. | 외부판매자 |
| 12243 | BOSCH KGN39VXAU | Art & Craft Nederland | 외부판매자 |
| 12765 | AEG LR9586BN4 | Media Markt Alkmaar | 리퍼·중고: 본 상품에 `Refurbished: Zeer goed`(리퍼비시: 매우 좋음) 표시 |

[생성 요약](summary.json)과 [독립 검증 결과](independent_verification.json)를 대조했다. 제외 4행의 본 상품 가격 영역·판매자 링크 및 리퍼 상태는 [개별 근거](changed_main_offer_evidence.json)에 보존했다. 나머지 55,993행의 26열 값이 전부 v5와 같고, 확인된 제외 4행 밖의 행을 바꾸지 않았음을 확인했다.

## 가짜 입력 검증의 변경 전후

아래는 실제 상품의 재판정 건수가 아니라 시험용 HTML의 결과다.

| 시험 입력 | 변경 전 | 변경 후 |
| --- | --- | --- |
| 헝가리 목록명에는 없고 PDP 제목에만 `felújított`(재생품), 내부값 직판 | 직판 | 리퍼·중고 |
| 네덜란드 목록명에는 없고 PDP 제목에만 `refurbished`(리퍼비시품), 내부값 직판 | 직판 | 리퍼·중고 |
| 헝가리 본 상품 문구 뒤 외부 판매자, 내부값 직판 | 직판 | 외부판매자 |
| 추천 영역에만 외부 판매자 문구, 본 상품 내부값 직판 | 직판 | 직판 유지 |
| 본 상품 문구는 있으나 판매자 링크를 읽지 못함, 내부값 직판 | 직판 | 확인불가 |

변경 전·후는 [시험 실행 결과 JSON](synthetic_before_after.json)과 일치한다. 실제 상품 재판정 결과는 위 실행 결과와 구분한다.

## 검증 명령과 결과

| 명령(저장소 루트 또는 명시한 폴더에서 실행) | 결과 |
| --- | --- |
| `pdp 모수 자동화/pipeline`에서 `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python -B -m unittest discover -s tests` | 최종 보완 후 309개, 14.377초, OK. 새 화면 검사 11개·국가 범위 4개·독일 195상품 기존 판정 재현을 포함 |
| 이 폴더에서 `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python -B -m unittest discover -s . -p test_review_v6.py -v` | 5개, OK. 원본 무수정·범위 밖 무변경·미확인 및 누락 시 차단을 확인 |
| `pdp 모수 자동화/pipeline`에서 `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python -B -m unittest discover -s tests -p test_mediamarkt_all_countries.py -v` | 4개, OK. 네 나라 상세 제목·본 상품 판매자 문구 검사, OSM·검색 모두 PDP 방문, 보조 파서의 추천 오탐 차단 |
| `python3 -B outputs/mediamarkt-hu-nl-v6-20261110/review_v6.py` | 유료 호출 0회. 계획 546주소, 두 나라 건수·v5/설정/판정 코드 해시 일치 |
| `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python -B outputs/mediamarkt-hu-nl-v6-20261110/review_v6.py --build` | 추가 유료 호출 0회. 546건 판정, 실패 0, v6 포함 10,211·제외 45,786 생성 |
| `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python -B outputs/mediamarkt-hu-nl-v6-20261110/verify_v6.py` | 55,997행·26열·행 순서·변경 4행 전수 대조 및 제외 4행의 본 상품 영역 별도 파서 대조 확인 |
| `git diff --check` 및 새 문서의 로컬 링크·JSON/파이썬 구문 검사 | 차이 형식 오류 없음, 로컬 링크 19개·이 폴더의 JSON 전체·Python 구문 5개·v5/v6 및 계획 해시 일치 확인 |

기본 Python 3.14에서는 `openpyxl`·`bs4` 미설치 때문에 첫 전체 검사에 환경 오류 3개가 났다. `/tmp`의 별도 Python 3.12 시험 환경에 프로젝트 `requirements.txt`의 고정 버전과 SQL 구문 검사 도구를 설치한 뒤 최초 302개와 최종 보완 후 309개가 통과했다. 기존 가상환경·운영 시스템에는 설치하지 않았다.

승인 후 실행 명령: `python3 -B outputs/mediamarkt-hu-nl-v6-20261110/review_v6.py --execute`. 원문을 확인한 뒤 `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python -B outputs/mediamarkt-hu-nl-v6-20261110/review_v6.py --build`로 재판정·실패 목록 및 v6를 생성한다. `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python -B outputs/mediamarkt-hu-nl-v6-20261110/verify_v6.py`는 별도 HTML 파서로 제외 후보의 본 상품 영역과 v5→v6 변경 범위를 대조한다.

## 후속 독립 검증: 헝가리 영구품절 2건 정정 필요

사용자 후속 지시(2026-11-10): 두 건은 일단 기록만 유지한다. v6·v7 정정 및 새 버전 생성은 보류한다.

사용자가 헝가리 결과를 다시 확인하도록 요청해 기존 판매자 판정 함수를 호출하지 않는 [독립 검증 스크립트](verify_hungary_independent.py)로 저장 원문 268개를 확인했다. [전체 추출 결과](hungary_independent_pages.json), [집계·버전 대조·정정 근거](hungary_independent_stock_audit.json), [현재 v7 원본 열을 보존한 정정 대상 2건 CSV](헝가리_영구품절_정정대상_2건.csv)를 작성했다. 새 사이트 접속·유료 호출·모수 CSV 수정은 하지 않았다.

| 범위 | 결과 |
| --- | --- |
| v5·v6·v7 헝가리 전체 행 | 1,766행·26열, 값·행 순서 모두 같음. 포함 268·제외 1,498 |
| 본 상품 제목·판매자·리퍼 추가 조건 | 추가 제외 0개 유지 |
| 본 상품 판매 상태 | 판매 가능 226, 일시 구매 불가 16, 매장 전용 24, 온라인 영구 구매 불가 2 |
| 상품 요약 데이터 | 266개는 본 상품 번호가 일치하고 신품 상태. 나머지 2개는 상품 요약 데이터 없음 |
| 영구품절 2개 정정 시 | 헝가리 포함 268→266. 실제 v6·v7은 아직 268 |

| CSV 행번호 | 상품·원래 주소 | 저장 원문 근거 |
| --- | --- | --- |
| 33530 | [LG F4A10S7NWK](https://www.mediamarkt.hu/hu/product/_lg-f4a10s7nwk-keskeny-eloltoltos-mosogep-7-kg-1494340.html) | 본 상품 판매 영역에 `Ez a termék végleg elfogyott`(이 상품은 영구 품절되었습니다). 본 상품 판매 상태도 `PERMANENTLY_NOT_AVAILABLE`(온라인 영구 구매 불가) |
| 33611 | [GORENJE WNHPI94BS](https://www.mediamarkt.hu/hu/product/_gorenje-wnhpi94bs-el%C3%B6lt%C3%B6lt%C5%91s-mos%C3%B3g%C3%A9p-1458922.html) | 본 상품 판매 상태가 `PERMANENTLY_NOT_AVAILABLE`(온라인 영구 구매 불가). 화면에는 `Online jelenleg nem elérhető`(현재 온라인 구매 불가) 표시 |

기존 D068은 영구품절을 제외하고, D085는 MediaMarkt의 위 상태 값을 온라인 영구 구매 불가로 해석했다. 이는 제조사 단종을 확정하는 근거는 아니다. 두 원문 수집 시각은 2026-11-10 13:42:45·13:43:35 KST이며, 10월 당시 상태를 확정하지 않는다.

이전 `verify_hungary.py`는 제목·판매자 조건과 본 상품 가격 영역의 존재를 대조했지만 상품 판매 상태는 검사하지 않았다. 가격 영역 컨테이너가 있다는 사실과 실제 판매 제안이 있다는 사실도 구분하지 못했다. 이전 결과의 0개·불일치 없음은 이 제한된 검사 범위의 결과다.

검증: 이 폴더에서 `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python -B -m unittest discover -s . -p test_hungary_independent.py -v`로 가짜 입력 4개를 검사해 성공했다. 본 상품 영구품절 검출, 다른 상품의 영구품절·추천 판매자 무시, 상품 요약 부재만으로 영구품절 단정 금지를 확인했다. 실제 검증 명령 `/tmp/lg-mm-v6-tests-py312-99e5d649/bin/python -B outputs/mediamarkt-hu-nl-v6-20261110/verify_hungary_independent.py`는 268개 원문을 대조해 위 2개를 추출하고, v5·v6·v7 파일 해시가 실행 전후 같은지 확인했다.
