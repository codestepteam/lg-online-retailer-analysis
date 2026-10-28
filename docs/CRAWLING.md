# Zyte 크롤링 구조와 PoC 기록

최종 정리: 2026-09-28. 2026-10-12 주의: 아래 `lg-crawling` Temporal 경로와 GCS 시나리오 발행 설명은 당시 상태다. 팀은 2026-10-07에 Temporal을 지우고 `lg-pipeline`의 GCP 실행 서버 명령으로 바꿨다. [동기화 메모](../PROJECT_CONTEXT.md#2026-10-12-팀-저장소-현황-동기화). 이 문서는 Zyte 수집 작업에서 **검증한 사실**, **사용자 결정**, **설계 제안**, **미결 사항**을 구분한다. 지표 판정 규칙은 [BUSINESS_RULES.md](BUSINESS_RULES.md), 사용자 결정은 [DECISIONS.md](DECISIONS.md)를 따른다.

## 2026-10-27 Costco Canada 영어·불어 페이지 구조 관찰

- Costco Canada는 `/en`·`/fr` 경로 대신 URL 끝의 `langId`로 언어를 나눈다. 영어 `?langId=-24`(페이지 언어 `en-ca`), 불어 `?langId=-25`(`fr-ca`). 같은 상품은 상품 ID·모델이 같다(LG 냉장고 `4000416185` 1개로 확인).
- `langId`가 없는 주소는 직전에 고른 언어로 보일 수 있다. 수집할 때 `langId=-24`를 명시하고 페이지 언어를 확인하는 방식은 AI 제안이다.
- 진단 대상은 영어 페이지만이다([D050](DECISIONS.md#2026-10-27-캐나다-costco는-영어-페이지만-진단-대상)). 관찰 근거: [메모](updates/2026-10-27/4929665c6d0a6a40d3a0d8aa9a20c952.md).

## 2026-10-26 OSM 미보유 리테일러 검색어 점검

- v2.2 `Search Term` J열 126행을 각 리테일러 사이트에서 검색해 첫 페이지 문제(검색어 안 먹힘·상품 없음·다른 제품 섞임 등)를 분류했다. 결과: [검색어 점검 CSV](../pdp%20모수%20추출/검색어_점검_20261026.csv). 처음에 차단된 행은 국가별 VPN으로 다시 확인했다([D048](DECISIONS.md#2026-10-26-검색어-차단-45행의-현지-vpn-재점검)).
- 이 점검으로 공식 검색어·제외 규칙·수집 상한을 정하지 않았다.
- 묶음 상품(예: 냉장고+전자레인지)은 포함하고, 대상 제품이 하나라도 들어 있으면 남긴다. [확인] 사용자 결정 D052

## 2026-10-22 현재 실행 구조를 찾는 방법

아래 본문은 이 저장소의 1~3차 시험·이관 이력이다. 현재 팀 실행 작업은 [lg-pipeline 작업 지침](../../lg-pipeline/AGENTS.md)과 해당 저장소의 실행 문서를 먼저 확인한다. 10월 22일 로컬 코드·문서 점검에서 확인한 연결은 다음과 같다. 이번에 수집·유료 모델 호출·GCS나 DB 접근·배포를 새로 실행하지 않았다.

- PDP(상품 상세 페이지)는 리테일러별 수집·파서→공통 관측 자료(Observation)→이미지 분류·채점→회차 반영 구조다. 공통 명령은 `pipeline/local/`, 리테일러별 코드는 `pipeline/retailers/`에 있다. 과거 `pipeline/temporal/` 경로를 실행 안내로 사용하지 않는다.
- BCP(브랜드·브랜드 카테고리 페이지)는 [BCP 로컬 실행 문서 ‘운영 회차 반영’](../../lg-pipeline/docs/bcp-local-runtime.md#운영-회차-반영-2026-10-14)에 공통 명령 `bcp push`로 반영하는 경로가 추가돼 있다. 10월 12일 ‘새 결과 반영 없음’은 당시 상태다.
- PLP(검색·상품 목록과 탐색 경로)는 [매일 수집 안내](../../lg-pipeline/docs/plp-daily.md), [판정·집계 기준](../../lg-pipeline/docs/plp/scoring.md), [회차 운영 문서](../../lg-pipeline/docs/operations.md)를 본다. 홈에서 브랜드 카테고리까지 클릭 수(ID7)는 현재 PLP 그룹의 월 입력으로 관리하는 경로가 있다.
- [파이프라인 선언문](../../lg-pipeline/knowledge/statements.md)의 ‘PDP URL 모수 확정’(LGOP-053)은 현재 모수 단계에서 리퍼·재판매·부품 제외나 쿼리 정규화를 하지 않는다고 기록한다. ‘비교 행 짝짓기’(LGOP-057)의 주소 대응은 비교 화면의 처리이며 모수 자체를 정리한 것이 아니다. 앞 단계에서 전달받은 목록의 선별 여부는 생성 지점에서 별도 확인한다.

확인 커밋·다른 저장소의 미커밋 작업·문서 충돌은 [동기화 점검](REPOSITORY_SYNC.md), BCP 이미지 설명 세 영역과 PDP 갤러리 설명의 후속 판정은 [업무 규칙](BUSINESS_RULES.md#2026-10-22-연결-저장소에서-확인한-후속-기준)에 연결했다. 아래의 ‘현재’·‘미구현’은 별도 후속 표시가 없으면 해당 시험의 작성 시점으로 읽는다.

2026-09-25 추가: Concentrix 운영 Docker v1.9.28 전달본(S10)에 브랜드 수집·파싱 모듈과 ScrapingBee 연동을 확인했다. 현재 문서의 Zyte 액션 가이드(S09)와 별개 자료다. 이미지의 `brand` 처리와 프로젝트의 `brand-category` 설정을 이름만으로 동일시하거나 API 키 교체만으로 전환 가능하다고 하지 않는다. [전달본·BCP 활용 검토](DOCKER_DELIVERY_REVIEW.md). 컨테이너 기동이나 추가 크롤링은 수행하지 않았다.

## 먼저 알아야 할 결론

- Zyte API 호출에 필요한 최소 요소는 API 키, 대상 URL, 요청 JSON, 호출 프로그램이다.
- 단순 `browserHtml` 요청은 페이지를 렌더링하지만 쿠키 창 닫기, 지역 선택, 더보기, 상세 패널 열기를 자동으로 보장하지 않는다.
- 이 프로젝트의 `recipe`는 Zyte에 등록하는 고유 리소스가 아니라, 동료 가이드가 요청 JSON과 검증 메타데이터를 묶어 부르는 **로컬 파일 형식**이다. Zyte API에 실제로 전송되는 것은 각 recipe의 `request` 객체다.
- 모든 URL마다 액션을 새로 작성하기보다 **리테일러 × 페이지 유형**별 대표 페이지에서 동작과 완료 조건을 확인하고, 같은 구조의 URL에 재사용하는 것이 현재 방향이다. 사이트 공통 동작과 페이지 유형별 동작을 분리해 합성하는 것은 이후 구현 제안이며 아직 코드 구조로 확정하지 않았다.
- 여기서 목표로 하는 것은 서버가 처음 보낸 원본 HTML이 아니라, 진단에 필요한 동적 콘텐츠를 노출하고 검증한 **진단용 렌더링 DOM**이다.

Zyte의 공식 용어와 제한은 [Browser automation](https://docs.zyte.com/zyte-api/usage/browser.html)과 [API reference](https://docs.zyte.com/zyte-api/usage/reference.html)를 기준으로 확인한다.

### ID18 대표 배너 후보의 화면 근거 수집 (2026-09-29)

D025에 따라 로컬 `1차 테스트/bcp-zyte-poc`의 Brand Category Page 수집 요청에 [`hero-evidence.js`](../1차%20테스트/bcp-zyte-poc/capture/hero-evidence.js)를 두 번 넣었다. 쿠키 처리 후 스크롤 전, 기존 전체 스크롤·더보기 처리 후 화면을 다시 맨 위로 돌린 시점에 실행한다. 요청은 [`build_recipes.py`](../1차%20테스트/bcp-zyte-poc/capture/build_recipes.py)가 만든 14개 리테일러의 BCP recipe와 [`capture_bcp_population.py`](../1차%20테스트/bcp-zyte-poc/scripts/capture_bcp_population.py)의 URL별 설정을 사용한다. Zyte의 `evaluate` 액션 안에서 브라우저가 계산한 위치·크기를 읽으며, 최종 [`prepare.js`](../1차%20테스트/bcp-zyte-poc/capture/prepare.js)가 이 기록을 `raw.html` 안의 `lg-capture-state` JSON에 넣고 수집기가 `capture-state.json`으로 추출한다.

저장 위치는 `capture-state.json → heroEvidence.snapshots.before_scroll / after_scroll`이다. 각 시점의 URL·실제 브라우저 화면 크기·본문 시작 위치와 함께 후보별 이미지/영상/내장 화면(iframe)/인라인 SVG/CSS 배경 종류, HTML 요소 경로, 파일 주소·이미지 설명 문구, 화면 위치·크기, 같은 영역의 제목·문구, 공통 메뉴·상품 카드 의심 표시를 저장한다. URL별 원본 목록의 브랜드·제품군도 별도 필드로 보존한다. 후보 탐색은 본문 시작부터 **화면 높이 세 배까지**로 제한하되, 이는 저장량을 제한하는 임시 수집 범위이며 ID18의 확정된 “상단” 판정 범위가 아니다. 큰 후보 100개와 가장 먼저 나온 후보 60개의 합집합을 보존하고 원래 후보 수·잘림 여부를 기록한다. [`parse_bcp_evidence.py`](../1차%20테스트/bcp-zyte-poc/scripts/parse_bcp_evidence.py)는 이 기록을 ID18의 `renderedCandidateSnapshots`로 복사한다. 기존 ID18 Y/N/REVIEW 결과는 변경하지 않는다.

새 좌표는 저장된 옛 `raw.html`에서 사후 재현할 수 없으므로 새 Zyte 수집본에서만 존재한다. 저장된 후보는 배너 확정값이 아니다. 상단의 수치 경계, 일반 광고·상품 카드 제외 방식, 영상·슬라이드 인정 여부가 결정되기 전에는 후보 존재만으로 Y/N을 계산하지 않는다. 화면이 차단되거나 초기 스냅샷이 빠졌거나 URL이 다른 페이지로 바뀌면 해당 시점의 부재를 N 근거로 사용하지 않는다.

실제 재수집 시험에서는 [Alza LG 냉장고](../1차%20테스트/bcp-zyte-poc/results_population/20260929-id18-pilot/pages/row-0014-alza/brand-category/capture-state.json)의 스크롤 전·후 기록이 모두 저장됐다. 스크롤 전 큰 LG 냉장고 이미지가 페이지 위에서 149px, 1084×363px로 기록됐다. [Elgiganten Bosch 건조기](../1차%20테스트/bcp-zyte-poc/results_population/20260929-id18-video-pilot/pages/row-0149-elgiganten/brand-category/capture-state.json)에서는 스크롤 전·후 모두 영상 후보 1개가 페이지 위에서 204px, 648×365px로 기록됐다. 이는 수집 필드가 작동한다는 확인이지 두 URL의 새 ID18 최종 판정이 아니다. 두 저장본 모두 파서 실행으로 `renderedCandidateSnapshots` 전달을 확인했다.

### ID21 제품군 탐색 카드 클릭 시험 (2026-09-29)

『EY_LGE HS 온라인 리테일 클리닉 진단 항목_v1.95_20260915 (1)』의 「Clinic 진단 항목」에서 ID21은 카드/CTA를 눌렀을 때 해당 제품군을 탐색할 수 있는지 묻는다. 도착 화면의 H1 태그 존재 여부를 별도 필수 조건으로 적지 않는다(D024). 따라서 기존 `navigator-sidebar-check/`의 **도착 주소 별도 접속 + 제목/H1 비교**는 클릭 정상 작동의 최종 근거가 될 수 없다.

로컬 시험 코드 [`check_id21_clicks.py`](../1차%20테스트/bcp-zyte-poc/scripts/check_id21_clicks.py)는 Datart LG 냉장고 원본 38행에서 `.subcategory-box` 카드 11개를 추출한다. 각 카드마다 Zyte 브라우저의 `click` 액션으로 원본 페이지에서 클릭하고 도착 HTML, 액션 성공 여부·최종 주소·상품 목록 예시를 저장한다. 클릭과 화면 수집이 확인된 경우에만 카드 문구와 도착 제품군의 의미 관계를 Jev에 묻는다. Jev는 링크가 실제로 눌렸는지, 화면이 차단되지 않았는지를 대신 판정하지 않는다. Zyte의 `click` 액션과 `waitForNavigationTimeout`은 [공식 API 문서](https://docs.zyte.com/zyte-api/usage/reference.html)의 `actions` 항목에 명시되어 있다.

실행: `python3 '1차 테스트/bcp-zyte-poc/scripts/check_id21_clicks.py' --live`. 결과는 `results_population/20260928-all-159/navigator-click-check/row-0038-datart/`에 카드별로 저장한다. 카드별 `zyte-request.json`은 클릭할 요소, `landing.html`은 클릭 후 Zyte가 저장한 화면, `zyte-response-summary.json`은 클릭·주소·상품 목록의 기계 점검, `jev-response.json`은 의미 판단 응답이다. `id21-click-review.json`은 11개 카드의 진행 상태와 근거를 모은다. 11개 모두 확인된 경우에만 전체 Y, 확인된 무관한 도착지는 N, 원본 화면이 그대로 남거나 도착 화면이 불충분한 수집은 REVIEW다. 현재 구현은 Datart 38행용 시험이며 다른 리테일러의 탐색 영역 식별 규칙은 아직 구현하지 않았다. 기존 159행의 ID21 Y/N을 이 시험만으로 모두 재검증했다고 볼 수 없다.

실행 관찰: 38행의 11개 카드에 대해 요청을 실행했고 `Úsporné`, `S připojením na vodu`, `Tiché` 3개는 클릭 후 해당 LG 냉장고 목록이 저장되어 Jev가 `matching_lineup`으로 답했다. 실패한 8개 중 6개(`Kombinované`, `Americké`, `No frost`, `S výrobníkem ledu`, `S displejem`, `Velké`)는 Zyte의 `click` 액션이 성공으로 기록됐어도 저장된 최종 주소와 화면은 원래 `lednice-lg.html` 그대로였다. 2개(`Chytré`, `S dávkovačem vody`)는 카드 주소로 이동했지만 저장된 HTML이 체코어 “Opište kód z obrázku”(그림의 코드를 입력하라) 사람 확인 화면이었다. 이 2건은 저장 HTML을 재분석해 처음의 단순 “상품 기록 0개” 오류를 CAPTCHA로 정정했다. 정확히 왜 6개에서 화면 전환이 일어나지 않았는지는 액션 결과만으로 확정할 수 없다. 따라서 38행 전체 ID21은 REVIEW이며, 이 8개를 사이트의 링크 고장으로 단정하지 않는다. 별도 앱 내 브라우저에서는 `Kombinované` 카드를 눌러 해당 LG 제품군 목록으로 이동하는 것을 직접 확인했으므로 Zyte의 수집 실패와 사이트 실제 동작 실패를 구별해야 한다. 전체 159행 판정표를 다시 만들었을 때 ID21은 Y 0·N 63·REVIEW 73·원본 불일치 3·비대상 20이다. 기존 별도 주소 접속만으로 Y였던 행들은 새 기준에서 REVIEW로 보류했다.

### ID21의 `lg-crawling` 로컬 클릭 연결 (2026-09-30)

2026-09-29 당시 동료 저장소의 [`pipeline/bcp_navigation_capture.py`](../../lg-crawling/pipeline/bcp_navigation_capture.py)에서 원본 BCP 화면의 탐색 영역을 리테일러별로 찾고 그 안의 링크를 각각 Zyte 브라우저로 클릭하도록 연결했다. 저장된 1차 테스트 HTML에서 Alza는 19행 중 15행의 `brandpage-category-list`, Datart는 20행 중 5행의 `subcategory-box-list`에서 카드를 찾았다. 이는 **카드 발견 수**이며 새 클릭의 성공이나 Y 판정 수가 아니다. 주소가 중복돼 클릭 대상이 모호한 카드, 카드가 없는 화면, 같은 페이지가 그대로 저장된 클릭은 판정을 보류한다. 클릭 요청·액션 결과·도착 HTML을 검토 근거로 저장하고, 정상 도착한 상품 목록의 의미만 Jev로 묻는다. Boulanger의 저장본에는 다른 브랜드까지 섞인 일반 관련 카테고리가 있었다. 9월 30일 로컬 확장은 아래에 별도로 기록했다.

## 현재 PoC의 실제 흐름

진입 파일은 [`scripts/run_zyte_poc.py`](../scripts/run_zyte_poc.py)다. 프로젝트 루트의 `.env` 또는 환경 변수에서 `ZYTE_API_KEY`를 읽고, 키 자체는 결과에 저장하지 않는다.

```text
retailer-urls-14/eci/urls.csv
        │
        ├─ 첫 PLP 1개 선택
        └─ 첫 LG PDP 1개 선택
                 │
                 ▼
       build_jobs()가 요청 JSON 3개 생성
        ├─ PDP: httpResponseBody
        ├─ PDP: browserHtml + screenshot + product
        └─ PLP: browserHtml + screenshot + productList
                 │
                 ▼
        POST https://api.zyte.com/v1/extract
                 │
                 ▼
 data/zyte/runs/<UTC 실행시각>/eci/
        ├─ manifest.json: 입력 행·요청·상태·파일 목록
        ├─ *-response.json: Zyte JSON 응답 원문
        ├─ *.html / *.jpg
        └─ product 또는 productList JSON
```

### 2026-09-22 실행에서 확인한 결과

근거는 [`manifest.json`](../data/zyte/runs/20260922T062938Z/eci/manifest.json)과 같은 폴더의 산출물이다.

| 요청 | 결과 | 걸린 시간 | 확인 내용 |
| --- | --- | ---: | --- |
| `pdp-http` | 실패, Zyte HTTP 520 | 2.882초 | 오류 유형 `/download/website-ban`. 이 한 번의 결과만으로 모든 ECI HTTP 요청이 항상 실패한다고 일반화하지 않는다. |
| `pdp-browser` | 성공, 대상 200 | 19.929초 | 렌더링 HTML·스크린샷·구조화 상품 데이터 저장. LG F4X5009TLB, EUR 599, InStock을 반환했다. |
| `plp-browser` | 성공, 대상 200 | 25.518초 | 렌더링 HTML·스크린샷·18개 상품의 구조화 목록을 저장했다. 최종 URL은 목록 2페이지였다. |

총 3회 요청 중 2회가 저장되고 1회가 실패했다. 성공한 PDP 스크린샷에도 쿠키 배너가 남아 있었다. 따라서 이 PoC는 **Zyte 요청·응답·저장 흐름을 확인한 것**이며, 진단에 필요한 모든 동적 영역을 열고 완료 여부까지 검증한 수집기는 아니다.

PoC의 `build_jobs()`가 실행 시점에 요청 객체를 만들기 때문에 별도 recipe 파일은 없다. 실행 후 생성되는 `manifest.json`은 무엇을 요청했고 무엇이 저장됐는지를 기록하는 결과 명세이지, 다음 요청에 사용하는 recipe는 아니다.

## 동료 가이드(S09)의 구조

S09는 [`retailer-zyte-actions-api-guide/`](../retailer-zyte-actions-api-guide/)에 있는 실행 코드·설정·생성 요청 묶음이다. 포함된 README가 언급하는 과거 HTML, 스크린샷, 브라우저 관측 보고서, 최종 오프라인 결과는 이 전달본에 포함되지 않았다. 따라서 **현재 코드와 정적 검사 파일은 검토할 수 있지만, 과거 70개 실수집이 모두 성공했다고 이 묶음만으로 입증할 수는 없다.**

```text
configs-*.json                URL 대표 목록
  리테일러·유형별 설정          output/_poc_zyte/url-manifest.json
          │                              │
cookies.js + load.js + prepare.js        │
          └──────────────┬───────────────┘
                         ▼
                 build_recipes.py
                         ▼
       recipes/<retailer>/<page-type>.json
       ├─ retailer, page_type, evidence  ← 로컬 메타데이터
       └─ request                        ← Zyte API 요청 본문
                         ▼
                  zyte_capture.py
                         ▼
 output/offline/<retailer>/<page-type>/
 request.json · response.json · raw.html · screenshot.jpg
```

지속적으로 수정할 원본은 `configs-*.json`, 공통 JavaScript, URL manifest다. 생성된 recipe를 직접 수정할 수는 있지만 `build_recipes.py`를 다시 실행하면 덮어써진다.

### 전달본에서 코드로 확인한 범위

| 항목 | 확인값 | 해석 |
| --- | ---: | --- |
| 대표 프로필 | 70개 | 14개 리테일러 × `home`, `brand`, `brand-category`, `plp`, `pdp` 5개 유형 |
| 쿠키 처리 설정 | 65/70 | 대부분의 대표 페이지에 쿠키 액션이 있으나, 실제 성공 여부는 새 실행으로 확인해야 함 |
| 별도 클릭 단계가 있는 프로필 | 31/70 | 지역 선택·더보기 등의 `steps`, `after_scroll`, `final_steps` 기준 |
| 상세 패널이 있는 PDP 프로필 | 8개, 패널 16개 | 열고 저장하고 닫는 동작이 필요한 유형 |
| 필수 selector 완료 조건 | 70/70 | `required`, `required_visible`, `required_hidden` 중 하나 이상 포함 |
| 텍스트·URL 등 추가 evidence 조건 | 27/70 | 나머지는 selector와 액션 상태 중심이므로 완료 계약을 더 구체화할 여지가 있음 |

ECI PDP 설정은 쿠키 동의와 지역 확인을 처리한 뒤 `#extra-info-composition-button`으로 특징 패널을 열고, 내용을 보존한 후 닫도록 되어 있다. `Capacidad máxima de carga`, `Consumo agua` 텍스트가 있는지도 검사한다. 이는 ECI PDP 대표 페이지에서 필요한 동작이며, 다른 리테일러나 페이지 유형에 그대로 적용할 수 있다는 뜻은 아니다.

가이드 실행기는 HTTP 200만으로 성공 처리하지 않는다. 액션 오류, 최종 URL, 차단 문구, 필수 selector, `#lg-capture-state`의 쿠키·패널·완료 상태를 검사한다. 요청 해시가 같은 성공 결과는 재사용하고, 재수집 전 기존 성공 결과를 `last-good`에 보존한다. 현재 재시도 대상에는 408·429·500·502·503·504가 있지만 PoC에서 나온 520은 포함되지 않는다.

## 대표 프로필과 전체 URL의 차이

`retailer-urls-14/*/urls.csv`에는 헤더를 제외하고 총 5,946개 URL 행이 있다. S09의 `--all`은 이 5,946개를 모두 수집하는 명령이 아니라, 생성된 대표 recipe 70개를 순차 실행하는 명령이다.

| 리테일러 | URL 행 | 리테일러 | URL 행 |
| --- | ---: | --- | ---: |
| alza | 933 | amazon-it | 286 |
| boulanger | 355 | coolblue | 149 |
| darty | 181 | datart | 654 |
| eci | 456 | elgiganten | 554 |
| media-expert | 705 | mediamarkt-es | 322 |
| mediamarkt-nl | 350 | mediaworld | 321 |
| rtv-euro-agd | 427 | unieuro | 253 |

70개 대표 프로필은 동작을 조사하고 재사용하기 위한 설정 단위다. 5,946개 전체 수집기로 확장하려면 각 URL 행을 적절한 프로필에 연결하고, 요청 생성·실패 격리·재시도·저장·완료 검증을 반복하는 오케스트레이션이 추가로 필요하다.

## 왜 리테일러 × 페이지 유형으로 나누는가

두 축이 바뀌면 필요한 상호작용과 완료 조건이 각각 달라진다.

| 축 | 달라지는 대표 요소 |
| --- | --- |
| 리테일러 | 쿠키·지역 팝업 selector, Shadow DOM 여부, 차단 방식, DOM 구조, 버튼 문구 |
| 페이지 유형 | PDP 상세 패널·리뷰·스펙, PLP 더보기·무한 스크롤·상품 카드, 홈/브랜드 탐색 영역 |

따라서 “리테일러만” 또는 “페이지 유형만”으로 설정하면 예외가 커진다. 다만 구현 시 70개 파일에 공통 로직을 복제할 필요는 없다. 아래처럼 합성하는 구조가 유지보수에 유리하다는 것은 현재의 **설계 제안**이다.

```text
리테일러 공통 설정
  쿠키 · 지역 · 사이트별 selector
             +
페이지 유형 공통 설정
  PDP 패널 · PLP 스크롤 · 완료 조건
             +
필요한 예외 override
             ↓
해당 URL의 Zyte request.actions 생성
```

## 진단용 DOM의 의미와 주의점

2026-09-28 BCP 재수집에서 MediaMarkt ES·NL과 MediaWorld는 스크롤·더보기 중 주소가 목록 3·4페이지로 바뀌고 Robots Meta도 처음 요청한 BCP의 `index, follow`에서 최종 화면의 `noindex,follow`로 바뀌는 것을 확인했다. BCP 수집 액션은 이제 스크롤 전에 요청 URL의 Title·Meta Description·H1·Robots Meta·Canonical을 `capture-state.json`의 `initialMetadata`로 보존한다. 최종 화면의 `metadata`는 계속 별도로 남는다. [새 판정 결과](../1차%20테스트/bcp-zyte-poc/results/20260928T060234KST/판정_1차_요약.md)

S09가 저장하는 HTML은 상호작용 후 DOM이며 일부는 수집을 위해 가공된다.

- `load.js`는 교체되거나 사라질 수 있는 상세 패널 내용을 복사해 `#lg-captured-panels`라는 합성 영역을 문서 끝에 추가한다.
- `prepare.js`는 열린 Shadow DOM을 선언형 Shadow DOM 템플릿으로 직렬화하고, 수집 상태를 `#lg-capture-state` JSON으로 삽입한다.
- 따라서 특정 텍스트·이미지·스펙의 **존재 여부**를 진단하기에는 유리하지만, 해당 요소가 원래 화면의 어느 위치에 있었는지 또는 사용자가 같은 상태로 보았는지를 HTML만으로 단정하면 안 된다.
- 위치·노출 상태가 중요한 진단은 스크린샷, 액션 로그, 원래 selector와 함께 판단해야 한다.

이 이유로 결과 저장 시 “원본 HTML”과 “진단용 렌더링 DOM”이라는 용어를 혼용하지 않는다.

## 전체 수집기로 확장할 때의 권장 흐름

아래는 D009를 구현하기 위한 설계 제안이며, 아직 최종 구현 결정은 아니다.

```text
5,946개 URL 입력
      ↓
URL의 retailer · page_type 확인
      ↓
대표 프로필 선택 + 예외 override
      ↓
Zyte request와 actions 생성
      ↓
HTML · screenshot · 선택적 구조화 데이터 수집
      ↓
완료 계약 검사
  쿠키/지역창 제거 · 필수 영역 · 패널 보존 · 차단 여부 · 최종 URL
      ├─ 통과 → 결과와 provenance 저장
      └─ 실패 → 오류 분류 · 재시도 또는 검토 대기열
```

URL별로 최소한 다음을 함께 저장하는 것이 좋다.

| 범주 | 저장 후보 |
| --- | --- |
| 입력·추적 | 원본 CSV 행 식별자, 요청 URL, canonical URL, retailer, page type |
| 요청 재현 | 실제 요청 JSON, 프로필 버전 또는 해시, geolocation, 실행 시각 |
| 결과 | 최종 URL, 대상 상태, 진단용 HTML, 스크린샷, 선택적 `product`/`productList` |
| 완료 검증 | 액션 결과, 필수 selector·텍스트 결과, 쿠키/지역창 잔존, 패널 저장 결과 |
| 실패 | Zyte 오류 유형, HTTP 상태, 재시도 횟수, 마지막 정상 결과 여부 |

## 월별 실행에서 Temporal의 역할

2026-10-12 확인: 팀 실행 저장소 `lg-pipeline`은 2026-10-06에 VPS Worker를 멈추고 2026-10-07에 Temporal 코드를 지웠다. 아래 D015 설명은 이 프로젝트의 결정 기록으로 남긴다. D015 유지 여부는 사용자 확인이 필요하다.

2026-09-26 D015에 따라 월별 크롤링의 예약과 실행 상태 관리는 Temporal로 한다. Temporal이 웹페이지를 직접 수집하는 것은 아니다. Temporal Schedule이 정해진 시각에 월간 Workflow를 시작하고, 별도로 배포한 Worker가 Task Queue에서 작업을 받아 Zyte 호출·결과 저장·완료 검증을 실행하는 구조다.

현재 프로젝트에 적용할 세부 Workflow 분할, Worker 배포 위치, 실행 시각·시간대, 이전 회차와 겹칠 때의 처리, 오류별 재시도 한도와 알림 방식은 아직 설계 제안 단계이며 확정하지 않았다.

## BCP의 GCS 이관 준비

2026-10-12 확인: 이 절은 2026-09-29~30 상태다. 그 뒤 2026-10-06에 이 회차 결과가 `lg-pipeline`의 운영 회차 `op-20261003-01`로 연결됐고, 2026-10-12에 팀원이 `lg-pipeline/pipeline/bcp/`에 새 BCP 실행 코드를 넣었다. 지금 팀 GCS의 새 파일은 `blobs/` 아래 내용 해시 이름으로 저장되며, 이 절의 `pipeline/retailers/<리테일러>/scenarios/` 발행 형식은 새 실행에서 쓰지 않는다. [동기화 메모](../PROJECT_CONTEXT.md#2026-10-12-팀-저장소-현황-동기화)

2026-09-29 D023의 최초 요청 범위는 기존 구조 조사와 이관 계획 설명까지였다. 이후 D027에서 로컬 변환 파일 작성이 명시적으로 허용됐다. GCS 업로드는 아직 허용되지 않았다.

브라우저의 Google Cloud 콘솔에서 직접 확인한 예시는 `lg-content-capture-20260909-assets/pipeline/retailers/amazon-it/scenarios/pdp/`다. 이 경로의 `versions/pdp-13ids-20260928-r10.json`은 해당 버전의 `manifest.json` 주소와 패키지 SHA-256을 가리킨다. 실제 버전 폴더에는 `recipe.json`, `actions.json`, `manifest.json`, `zyte/`의 JavaScript 파일, `parser/pdp.py`, `observation/lg-diagnostic-observation-v1.schema.json`이 있다. 이 JSON 스키마는 `schema_version`, `target`, `facts`, `completeness`, `evidence`를 필수로 지정하고 직렬화 크기를 최대 2 MiB로 설명한다. 따라서 `observation/`에서 확인한 파일은 개별 페이지의 판정 결과가 아니라 파서 출력 형식을 정의하는 스키마다. 동료의 [`pipeline/two_stage.py`](https://github.com/codestepteam/lg-crawling/blob/main/pipeline/two_stage.py)에서 `validate_observation`이 이 필수 필드를 검사하는 것도 직접 확인했다. BCP 지원 여부는 아직 확인하지 않았다. [PDP 버전 목록](https://console.cloud.google.com/storage/browser/lg-content-capture-20260909-assets/pipeline/retailers/amazon-it/scenarios/pdp/versions?project=lg-content-capture-20260909), [PDP 예시 버전](https://console.cloud.google.com/storage/browser/lg-content-capture-20260909-assets/pipeline/retailers/amazon-it/scenarios/pdp/pdp-13ids-20260928-r10?project=lg-content-capture-20260909).

이번 BCP 이관의 URL 출처는 사용자가 지정한 `관련문서/★EY_LGE_Clinic_Assessment Summary_Improvement Tracker_V0.1_20260911 (1).xlsx`다. 이 원본의 `ID8`, `ID9`, `ID10` 탭에는 `Page Type = Brand Category Page` 행이 있고, `ID18_19_20_21_22_23` 탭에는 `Brand Category Page URL` 열이 있다. 이를 합쳐 만든 `1차 테스트/Brand_BCP_1차_테스트_URL_목록.xlsx`의 `URL 목록` 탭에는 BCP 139행과 별도 Brand Page 20행이 있다. 이번 클라우드 이관에서는 BCP 139행만 대상이다. `관련문서/retailer-urls-14/*/urls.csv`의 BCP 165행은 다른 목록의 관찰값이지 이번 URL 범위를 다시 고르라는 뜻이 아니다. 따라서 URL 페이지 유형 선정은 미해결 사항이 아니다.

로컬 `1차 테스트/bcp-zyte-poc/capture/recipes/`에는 14개 리테일러의 `brand-category.json` 설정 파일이 있지만 위 139개 BCP 행은 9개 리테일러에 분포한다. 나머지 5개(Darty, ECI, Media Expert, RTV Euro AGD, Unieuro)는 현재 지정한 목록에 BCP URL이 없어 실행할 대상이 없다. 이는 URL 추출 오류나 이번 준비의 장애물이라는 뜻이 아니다. 다만 [159행 1차 판정 결과](../1차%20테스트/bcp-zyte-poc/results_population/20260928-all-159/전체_URL_판정_진행상태.md)에서 BCP 139행 중 Datart 삼성 40·41행은 일반 제품 목록으로 이동했고, Amazon 이탈리아 삼성 80행은 LG 77행과 같은 주소를 가리켜 `SOURCE_MISMATCH`로 보류했다. BCP로 분류한 것 자체의 오류는 아니지만 이 3행을 올바른 BCP 판정 결과로 취급해서는 안 된다. 또한 대표 9개 페이지의 `parse_bcp_evidence.py`는 후보 추출용이며, 전체 159행의 `assess_full_population.py`는 그 출력이 아니라 수집 파일, 이미지 검토 기록, 링크 검사, AI 검토 기록 등을 직접 읽는다. GCS용 BCP 파서와 판정기를 합치려면 이 두 경로와 `REVIEW`·수집 오류·원본 불일치 처리를 명시적으로 연결해야 한다.

BCP용 `scenarios/bcp/` 경로, 버전 포인터, Zyte·파서·관찰 스키마 파일 배치는 **PDP 예시를 따른 설계 제안**이다. 다만 동료 로컬 저장소의 [`pipeline/scenarios.py`](/Users/codestepseunghee/codestep/lg-crawling/pipeline/scenarios.py)는 현재 `scenario_type`으로 `pdp`, `search`, `menu`만 허용하고, [`pipeline/scenario_observations.py`](/Users/codestepseunghee/codestep/lg-crawling/pipeline/scenario_observations.py)도 그 유형의 파서만 고른다. [`pipeline/scoring_contract.py`](/Users/codestepseunghee/codestep/lg-crawling/pipeline/scoring_contract.py)는 현행 로컬 채점을 PDP `scoring/v1`에 한정한다. 따라서 현재 코드에 BCP 파일을 올리기만 해서는 실행되지 않으며, BCP 유형·파서·9개 항목 채점 연결을 추가해야 한다. URL이 없는 5개 리테일러에 이번 회차의 실행 대상을 억지로 만들 필요는 없다.

사용자가 재확인한 최종 실행 목표는 `Temporal 실행 요청 → 배포된 Worker가 GCS의 BCP 버전·URL 목록 읽기 → Zyte 수집 → 파싱·9개 항목 판정 → 수집 근거와 판정 결과를 GCS에 저장`이다. 이는 **사용자가 정리한 목표 흐름**이며 동료의 실제 실행 구조를 그대로 표현한 말은 아니다. GCS의 시나리오 버전은 실행 방법을 담고, 회차별 수집·판정 결과는 별도 출력으로 보존하는 방향이다. 현재 로컬 `capture_bcp_population.py`는 프로젝트 폴더의 `population/source_urls.json`과 `capture/recipes/`를 읽고 `results_population/`에 쓰며, `assess_full_population.py`는 저장된 HTML 외에 `본문_항목_AI검수.json`·`ID8_전체검수.json` 같은 검토 파일도 읽는다. 따라서 파일 업로드만으로 매달 새 화면의 판정이 완성되지는 않는다. 동료의 PDP Temporal 경로는 아래와 같이 확인했지만 BCP에 대한 실제 연결은 확인되지 않았다. 이는 URL 목록을 다시 정해야 한다는 뜻이 아니다.

동료 로컬 저장소의 최상위에는 `retailers/`, `pipeline/`, `scoring/`이 별도로 있다. 편집용 시나리오 파일은 `retailers/<retailer>/scenarios/<type>/` 아래, 발행된 버전은 GCS의 버전·해시 경로에 있다. [현재 시나리오 배치 설명](/Users/codestepseunghee/codestep/lg-crawling/docs/scenario-batches.md)과 [실제 Workflow 코드](/Users/codestepseunghee/codestep/lg-crawling/pipeline/dataset_processing.py)를 확인했다. 현행 일반 배치는 Temporal이 URL별 작업을 분배하여 `pdp_capture_url`(Zyte 수집), `pdp_archive_assets`(자산 저장), `pdp_observe_url`(패키지 파서를 실행해 관측 결과 별도 저장), `pdp_score_ids`(선택된 항목 채점)를 실행한다. 활동 이름에 `pdp`가 남아 있지만 일반 배치는 `pdp`, `search`, `menu`에 사용한다. 다만 현재 채점 활동은 전달받은 `observation_ref`를 읽지 않고 [`score_pdp_url()`](/Users/codestepseunghee/codestep/lg-crawling/pipeline/pdp_live.py)에서 PDP 파서를 다시 실행한 결과로 항목별 판정 코드를 부른다. 저장된 관측 결과를 판정의 직접 입력으로 사용한다고 설명해서는 안 된다. GCS PDP 패키지의 `observation/*.schema.json`은 파서 출력 구조의 정의이고 판정 코드는 별도 `scoring/v1/id_*.py`다. [ID18 예시](/Users/codestepseunghee/codestep/lg-crawling/scoring/v1/id_18.py)는 파서가 만든 `facts.sections` 등을 읽는다. [결과 검증 코드](/Users/codestepseunghee/codestep/lg-crawling/pipeline/two_stage.py)는 `completed` 상태에 `value`를 요구하고 `reason`을 금지하며, 완료되지 않은 상태에는 `reason`을 요구한다. 로컬 `assess_full_population.py`가 각 항목에 `reason`을 담는 방식과 달라 BCP 이관 때 결과 형식의 대응을 설계해야 한다.

D027에 따라 [로컬 변환본](../1차테스트변환/README.md)을 프로젝트 최상단에 작성했다. 14개 리테일러의 BCP 수집 설정을 동료의 시나리오 폴더 모양으로 분리하고, 이번 입력 목록의 BCP 139행을 보존했다. 저장된 BCP 139개 화면을 새 `parse(bundle)` 파서로 읽었고, ID9·10 코드 판정은 기존 1차 결과와 차이가 없었다. ID8·18·19·20·23은 새 화면에 연결된 AI 응답이 없으면 판정 불가로 남긴다. ID18 AI 입력은 후보 숫자·문구에 더해 전체 화면 스크린샷을 요구한다. 이것은 로컬 변환 검증이며 BCP Temporal 실행, GCS 발행, AI 실제 호출 검증은 아니다.

**2026-09-29 후속 구현(D028):** 위의 `lg-crawling` 코드가 BCP를 허용하지 않는다는 설명은 후속 구현 전 상태다. 현재 로컬 [`lg-crawling/bcp/README.md`](../../lg-crawling/bcp/README.md)의 코드에서는 BCP 시나리오 발행·139행 배치 사전 검증·Zyte 요청 컴파일·패키지 파서·BCP 전용 9개 판정 함수를 기존 Temporal 일반 회차에 연결했다. 판정 활동은 PDP와 달리 저장된 BCP 파서 관측 기록을 직접 읽는다. ID8·18·19·20·23은 새 AI 응답과 근거를 별도 저장하고, ID22는 같은 브랜드 상품 카드 최대 두 개의 도착지를 다시 확인한다. ID21의 최초 연결은 Datart 카드에 한정됐다. 14개 시나리오를 **로컬 `file://` 저장소에 발행**하고 139행 사전 검증, 139개 수집 요청의 1차 테스트 요청과의 완전 일치를 확인했다. 실제 GCS 업로드, Temporal 실행, Zyte·AI 실호출 검증은 수행하지 않았다. D028은 로컬 구현만 허용하며 GCS 수정은 여전히 보류한다.

**2026-09-30 ID21 로컬 확장:** [`pipeline/bcp_navigation_capture.py`](../../lg-crawling/pipeline/bcp_navigation_capture.py)에 Alza·Datart 외 Boulanger·Coolblue·Elgiganten·MediaMarkt Spain/Netherlands·MediaWorld의 화면 내 탐색 영역 표식을 추가했다. 저장된 LG BCP 19행에서 클릭 후보는 Boulanger 50·51행 각 10개, Coolblue 112행 3개, Elgiganten 156행 3개, MediaMarkt Spain 142행 2개·143행 3개, Netherlands 127행 4개, MediaWorld 94행 2개로 잡혔다. 이 숫자는 **저장 HTML에서 찾아낸 카드 수**이지 실제 클릭 성공이나 Y/N 판정이 아니다. Boulanger 카드에는 경쟁사·전체 브랜드 목록으로 가는 링크도 있으므로 새 [`pipeline/bcp_navigation_observe.py`](../../lg-crawling/pipeline/bcp_navigation_observe.py) 질문은 도착 화면이 원본 브랜드와 카드 제품군을 모두 충족하는지 확인한다. 상품 목록 인식도 각 사이트의 HTML 표식에 맞게 추가했다. 카드가 없으면 [`pipeline/bcp_ai_observe.py`](../../lg-crawling/pipeline/bcp_ai_observe.py)의 전체 화면 AI 검토가 탐색 영역 부재를 판단할 수 있지만, 저장 화면 높이가 수집 당시 페이지 높이에 못 미치면 아예 N 검토를 실행하지 않는다. 로컬 저장본에서 Amazon Italy LG 냉장고 화면은 이 높이 조건을 통과했고, Boulanger·MediaMarkt Spain/Netherlands·MediaWorld의 긴 화면은 통과하지 못했다. 이 결과는 **새 수집본의 실제 AI 응답이 아니다.** GCS 내용과 기존 159행 판정표는 변경하지 않았다.

실제 Zyte 확인은 Coolblue LG 냉장고 112행의 `LG Amerikaanse koelkasten` 카드 **한 개**로 했다. 2026-09-30 원본 주소 `https://www.coolblue.nl/koelkasten/lg`에서 새 XPath를 기다린 뒤 `click` 액션이 성공했고, 최종 주소는 `https://www.coolblue.nl/koelkasten/vrijstaand/amerikaanse-koelkasten/lg`, HTTP 상태는 200이었다. 도착 HTML에서 상품 링크 문구 3개를 읽었다. 이 한 건은 새 카드 선택·클릭·도착 수집의 작동 확인이다. 나머지 카드 전체, Jev 의미 판정, 전체 ID21 Y/N, Temporal 회차는 아직 실제 호출로 검증하지 않았다.
같은 날 Boulanger LG 냉장고 50행의 `Petit réfrigérateur` 카드 한 개도 새 XPath로 Zyte 클릭했다. 액션 기록은 성공이지만 최종 주소와 저장 화면은 원본 `https://www.boulanger.com/c/refrigerateur/brand~lg` 그대로라 코드상 클릭 검증 실패·판정 보류다. 저장 HTML에는 `didomi-popup-open` 클래스가 있으나 전체 화면 이미지에는 쿠키 창이 보이지 않아 이 현상의 원인을 쿠키 창이라고 단정할 수 없다. 이 호출만으로 해당 카드나 사이트 자체의 링크 고장을 N으로 확정하지 않는다.

## 2026-09-26 Brand Category Page 대표 액션 구현

`retailer-zyte-actions-api-guide/`는 동료 전달 원본으로 보존하고, 이 시험의 구현과 실행 결과는 [`1차 테스트/bcp-zyte-poc/`](../1%EC%B0%A8%20%ED%85%8C%EC%8A%A4%ED%8A%B8/bcp-zyte-poc/)에서 관리한다.

Alza, Datart, Boulanger, Amazon Italy, MediaWorld, Coolblue, MediaMarkt Netherlands, MediaMarkt Spain, Elgiganten의 대표 `brand-category` 설정에 사용자가 확인한 쿠키 창·사람 확인 화면과 Obsidian Vault의 `리테일러 특징` 메모를 반영했다. 9개 모두 전체 페이지를 끝까지 내리며, 리테일러별 설명 펼치기·제품 더보기·질문 펼치기를 필요한 경우에만 적용한다. Alza·Datart의 2페이지 링크와 Coolblue의 별도 도움말 링크는 현재 페이지를 벗어나므로 수집 중에는 누르지 않는다.

[`1차 테스트/bcp-zyte-poc/capture/evidence.js`](../1%EC%B0%A8%20%ED%85%8C%EC%8A%A4%ED%8A%B8/bcp-zyte-poc/capture/evidence.js)를 추가해 다음 근거를 HTML 안의 `#lg-capture-state`에 담고, 정상 수집 후 `capture-state.json`으로 별도 저장한다. `capture-state.json`은 단계별 수집 상태와 진단 근거를 모은 JSON 파일이다.

- ID8: 이미지별 설명 문구, 화면 표시 크기, 원본 크기, 로딩·노출 상태.
- ID9: 페이지 제목, 페이지 설명, 최상위 제목, 검색엔진 설정.
- ID10: `rel="canonical"`로 표시된 대표 주소.
- ID22·23 후보: 보이는 버튼·링크의 문구, 목적지, 펼침 상태.

사람 확인 화면은 자동 클릭하지 않는다. MediaWorld·MediaMarkt Netherlands·MediaMarkt Spain의 관찰 문구와 일반 `captcha` 문구를 실패 표시로 추가했다. `require_scroll_bottom=true`인 데이터에서 페이지 끝에 도달하지 못하면 실패로 검증한다. 항목 부재는 정상적인 N 판정일 수 있으므로 Hero Banner, FAQ, Why LG, USP 자체를 수집 성공의 필수 요소로 두지 않았다.

70개 대표 요청 재생성과 정적 검사 3종을 통과했고, 2026-09-26에 위 9개 Brand Category Page를 실제 Zyte API로 수집했다. 9개 모두 HTTP 200, 페이지 끝 도달, 필수 영역 검사를 통과했다. Amazon Italy는 첫 실행에서 늦게 붙는 콘텐츠 때문에 페이지 끝 도달 검사를 통과하지 못했고, 페이지 높이가 연속으로 안정될 때까지 기다리도록 스크롤 로직을 수정한 후 재실행에 성공했다. 다만 Boulanger·MediaWorld·MediaMarkt Netherlands·MediaMarkt Spain의 전체 화면 이미지는 Zyte의 10,000픽셀 높이 제한으로 아래 영역이 잘렸다. 따라서 “본문 수집 조건 통과”와 “화면 전체 저장”을 구분한다.

결과는 [`results/20260926T120245KST/`](../1%EC%B0%A8%20%ED%85%8C%EC%8A%A4%ED%8A%B8/bcp-zyte-poc/results/20260926T120245KST/)에 수집 묶음으로 보존했다. `수집_요약.csv`와 `manifest.json`에 9개 수집 상태를 기록했고, 각 리테일러 폴더에 요청·응답·HTML·화면·구조화 근거 5개 파일을 보존했다. 화면 완전성은 [`수집_완전성_점검.md`](../1%EC%B0%A8%20%ED%85%8C%EC%8A%A4%ED%8A%B8/bcp-zyte-poc/results/20260926T120245KST/%EC%88%98%EC%A7%91_%EC%99%84%EC%A0%84%EC%84%B1_%EC%A0%90%EA%B2%80.md)에 별도로 기록했다. 진단 판정은 실행하지 않았다. 대표 URL과 액션 상세는 [`1차 테스트/Zyte_BCP_9개_항목_수집_액션_정의.md`](../1%EC%B0%A8%20%ED%85%8C%EC%8A%A4%ED%8A%B8/Zyte_BCP_9%EA%B0%9C_%ED%95%AD%EB%AA%A9_%EC%88%98%EC%A7%91_%EC%95%A1%EC%85%98_%EC%A0%95%EC%9D%98.md)에 있다.

### 긴 페이지의 화면 이미지 제한과 처리 결정

Zyte Extract API의 `screenshotOptions.fullPage=true`는 전체 페이지 화면을 요청하지만, 최대 크기 5,000×10,000픽셀을 넘는 이미지는 잘린다. 공식 근거: [Zyte API reference — screenshotOptions](https://docs.zyte.com/zyte-api/usage/reference.html). 이 제한을 늘리는 Extract API 옵션은 공식 문서에서 확인하지 못했다.

2026-09-26 D016에 따라 이 제한은 현재 파서 작업을 막지 않는다. `raw.html`과 `capture-state.json`이 본문 수집 완료 조건을 통과하면 이를 판정 근거의 입력으로 사용하고, `screenshot.jpg`는 사람이 페이지 상태를 참고하는 보조자료로 둔다. Hero Banner·Why LG·USP는 정의를 구체화한 뒤 HTML의 제목·본문·이미지와 수집 시점의 표시 여부·위치·크기를 함께 사용한다. 시각 근거가 필요하면 전체 페이지를 여러 장으로 저장하는 기능보다 해당 후보 요소만 별도로 저장하는 기능을 우선 검토한다.

ID22는 제품 목록과 상세 페이지 이동 수단의 존재를 확인하는 항목이다. 1차 테스트에서는 페이지에서 선택한 동일 브랜드 상품 카드 최대 2개의 도착 페이지를 확인했다. 제품 더보기를 몇 번 눌러야 하는지와 상품 카드 전수 검사 방식은 아직 정하지 않았다.

## 아직 결정할 것

### 현재 Brand Page·BCP 검증에 적용할 범위

2026-09-25 D012에 따라 1차 테스트 입력에는 일반 Brand Page와 Brand Category Page를 함께 둔다. 일반 Brand Page는 ID8·9·10만 수집하고, Brand Category Page는 ID8·9·10·18·19·20·21·22·23을 모두 수집한다. 2026-09-28에는 [입력 Excel의 159개 URL 전체](../1차%20테스트/bcp-zyte-poc/results_population/20260928-all-159/전체_URL_판정_진행상태.csv)를 Zyte로 수집하고 1차 판정을 기록했다. 이 작업은 별도의 5,946개 전체 URL 수집을 완료했다는 뜻이 아니다. 원본 주소 충돌과 일부 이미지·배너의 판정 경계는 결과표에서 별도 상태로 남긴다. Elgiganten Electrolux 세탁 페이지의 ID22는 원래 저장본의 상품 목록 로딩 때문에 REVIEW였지만, 2026-09-29 실제 브라우저에서 카드 2개를 눌러 상세 페이지로 이동함을 확인한 [별도 기록](../1차%20테스트/bcp-zyte-poc/results_population/20260928-all-159/product-link-check-live/row-0152-elgiganten.json)을 적용해 Y로 갱신했다. 원래 수집본은 변경하지 않았으므로 이 행은 9월 28일 수집 결과와 9월 29일 직접 확인 결과를 함께 사용한다.

- 로컬 `retailer-urls-14/*/urls.csv`의 `page_type=브랜드 카테고리 페이지`는 165행·정확한 URL 문자열 165개이며 LG는 41행이다. S09 recipe의 유형명은 `brand-category`여서 매핑이 필요하다. 이는 목록 관찰이며 승인된 진단 모수나 현재 접속 가능 건수가 아니다.
- ECI CSV에는 BCP 유형 행이 없고 S04에서도 BCP 미존재로 표기하지만 S09에는 ECI `brand-category` 프로필이 있다. 프로필을 곧바로 업무상 BCP 판정 대상으로 삼지 않는다.
- MediaMarkt ES 냉장고 URL은 S04 `BCP!I11`, 해당 CSV, S09 대표 recipe에 공통으로 존재한다. 첫 수집 후보로 제안할 수 있으나 현재 접속·수집 성공은 확인하지 않았다. recipe 메모도 새 Zyte 실행 필요를 명시한다.
- ID21·22는 도착 페이지 확인이 필요하므로 BCP 본문 수집과 클릭 목적지의 최소 검증을 구분한다. 이를 PDP 전체 진단으로 확장하지 않는다. 존재하지 않을 수도 있는 FAQ/USP 블록 자체를 수집 성공의 필수 조건으로 두면 N인 정상 페이지를 수집 실패로 오분류하므로, 완료 검증은 항목 존재 판정과 분리한다.

1. profile 설정을 정본으로 두고 recipe를 빌드할지, 실행 시 요청을 동적으로 만들지.
2. 5개 페이지 유형별 “수집 완료” 조건과 진단 항목의 연결.
3. 같은 리테일러·페이지 유형 안에서 템플릿이 다른 URL을 어떻게 탐지하고 예외 처리할지.
4. `product`/`productList` 구조화 추출을 HTML과 함께 계속 요청할지.
5. Zyte 전체 응답 원문, 오프라인 CSS·이미지 자산까지 보관할지와 보존 기간.
6. 520 같은 웹사이트 차단, CAPTCHA, selector 변경, 부분 수집의 재시도·검토 정책.
7. 병렬 처리량, API 비용 한도, 국가별 geolocation과 실행 주기.

## 근거 파일

- 현재 PoC: [`scripts/run_zyte_poc.py`](../scripts/run_zyte_poc.py), [실행 manifest](../data/zyte/runs/20260922T062938Z/eci/manifest.json)
- S09 안내: [상위 README](../retailer-zyte-actions-api-guide/README.md), [capture README](../retailer-zyte-actions-api-guide/capture/README.md)
- recipe 생성: [`capture/build_recipes.py`](../retailer-zyte-actions-api-guide/capture/build_recipes.py)
- 요청 실행·검증: [`scripts/zyte_capture.py`](../retailer-zyte-actions-api-guide/scripts/zyte_capture.py)
- 상호작용·DOM 보존: [`capture/load.js`](../retailer-zyte-actions-api-guide/capture/load.js), [`capture/prepare.js`](../retailer-zyte-actions-api-guide/capture/prepare.js)
