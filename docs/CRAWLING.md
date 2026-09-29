# Zyte 크롤링 구조와 PoC 기록

최종 정리: 2026-09-28. 이 문서는 Zyte 수집 작업에서 **검증한 사실**, **사용자 결정**, **설계 제안**, **미결 사항**을 구분한다. 지표 판정 규칙은 [BUSINESS_RULES.md](BUSINESS_RULES.md), 사용자 결정은 [DECISIONS.md](DECISIONS.md)를 따른다.

2026-09-25 추가: Concentrix 운영 Docker v1.9.28 전달본(S10)에 브랜드 수집·파싱 모듈과 ScrapingBee 연동을 확인했다. 현재 문서의 Zyte 액션 가이드(S09)와 별개 자료다. 이미지의 `brand` 처리와 프로젝트의 `brand-category` 설정을 이름만으로 동일시하거나 API 키 교체만으로 전환 가능하다고 하지 않는다. [전달본·BCP 활용 검토](DOCKER_DELIVERY_REVIEW.md). 컨테이너 기동이나 추가 크롤링은 수행하지 않았다.

## 먼저 알아야 할 결론

- Zyte API 호출에 필요한 최소 요소는 API 키, 대상 URL, 요청 JSON, 호출 프로그램이다.
- 단순 `browserHtml` 요청은 페이지를 렌더링하지만 쿠키 창 닫기, 지역 선택, 더보기, 상세 패널 열기를 자동으로 보장하지 않는다.
- 이 프로젝트의 `recipe`는 Zyte에 등록하는 고유 리소스가 아니라, 동료 가이드가 요청 JSON과 검증 메타데이터를 묶어 부르는 **로컬 파일 형식**이다. Zyte API에 실제로 전송되는 것은 각 recipe의 `request` 객체다.
- 모든 URL마다 액션을 새로 작성하기보다 **리테일러 × 페이지 유형**별 대표 페이지에서 동작과 완료 조건을 확인하고, 같은 구조의 URL에 재사용하는 것이 현재 방향이다. 사이트 공통 동작과 페이지 유형별 동작을 분리해 합성하는 것은 이후 구현 제안이며 아직 코드 구조로 확정하지 않았다.
- 여기서 목표로 하는 것은 서버가 처음 보낸 원본 HTML이 아니라, 진단에 필요한 동적 콘텐츠를 노출하고 검증한 **진단용 렌더링 DOM**이다.

Zyte의 공식 용어와 제한은 [Browser automation](https://docs.zyte.com/zyte-api/usage/browser.html)과 [API reference](https://docs.zyte.com/zyte-api/usage/reference.html)를 기준으로 확인한다.

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

2026-09-26 D015에 따라 월별 크롤링의 예약과 실행 상태 관리는 Temporal로 한다. Temporal이 웹페이지를 직접 수집하는 것은 아니다. Temporal Schedule이 정해진 시각에 월간 Workflow를 시작하고, 별도로 배포한 Worker가 Task Queue에서 작업을 받아 Zyte 호출·결과 저장·완료 검증을 실행하는 구조다.

현재 프로젝트에 적용할 세부 Workflow 분할, Worker 배포 위치, 실행 시각·시간대, 이전 회차와 겹칠 때의 처리, 오류별 재시도 한도와 알림 방식은 아직 설계 제안 단계이며 확정하지 않았다.

## BCP의 GCS 이관 준비

2026-09-29 D023에 따라 이번 단계는 기존 구조 조사와 이관 계획 설명까지만 수행한다. 구현 파일을 만들거나 GCS에 업로드하지 않는다.

브라우저의 Google Cloud 콘솔에서 직접 확인한 예시는 `lg-content-capture-20260909-assets/pipeline/retailers/amazon-it/scenarios/pdp/`다. 이 경로의 `versions/pdp-13ids-20260928-r10.json`은 해당 버전의 `manifest.json` 주소와 패키지 SHA-256을 가리킨다. 실제 버전 폴더에는 `recipe.json`, `actions.json`, `manifest.json`, `zyte/`의 JavaScript 파일, `parser/pdp.py`, `observation/lg-diagnostic-observation-v1.schema.json`이 있다. 이 JSON 스키마는 `schema_version`, `target`, `facts`, `completeness`, `evidence`를 필수로 지정하고 직렬화 크기를 최대 2 MiB로 설명한다. 따라서 `observation/`에서 확인한 파일은 개별 페이지의 판정 결과가 아니라 파서 출력 형식을 정의하는 스키마다. 스키마 설명은 `pipeline.two_stage.validate_observation`의 검사를 언급하지만 해당 실행 코드와 BCP 지원 여부는 아직 확인하지 않았다. [PDP 버전 목록](https://console.cloud.google.com/storage/browser/lg-content-capture-20260909-assets/pipeline/retailers/amazon-it/scenarios/pdp/versions?project=lg-content-capture-20260909), [PDP 예시 버전](https://console.cloud.google.com/storage/browser/lg-content-capture-20260909-assets/pipeline/retailers/amazon-it/scenarios/pdp/pdp-13ids-20260928-r10?project=lg-content-capture-20260909).

로컬 `1차 테스트/bcp-zyte-poc/capture/recipes/`에는 14개 리테일러의 `brand-category.json`이 있다. 그러나 `population/source_urls.json`의 Brand Category Page는 139행·9개 리테일러이고, 별도 원본 `관련문서/retailer-urls-14/*/urls.csv`의 해당 유형은 165행·9개 리테일러다. Darty, ECI, Media Expert, RTV Euro AGD, Unieuro는 두 URL 목록에 BCP 행이 없다. 14개 설정 파일의 존재를 14개 리테일러의 BCP 실수집·판정 완료로 해석하지 않는다. 또한 대표 9개 페이지의 `parse_bcp_evidence.py`는 후보 추출용이며, 전체 159행의 `assess_full_population.py`는 그 출력이 아니라 수집 파일, 이미지 검토 기록, 링크 검사, AI 검토 기록 등을 직접 읽는다. GCS용 BCP 파서와 판정기를 합치려면 이 두 경로와 `REVIEW`·수집 오류·원본 불일치 처리를 명시적으로 연결해야 한다.

BCP용 `scenarios/bcp/` 경로, 버전 포인터, Zyte·파서·관찰 스키마 파일 배치는 **PDP 예시를 따른 설계 제안**이다. 기존 실행기가 BCP 페이지 유형과 9개 진단 ID를 허용하는지, 파서 호출 계약과 채점기 `scoring/v1`가 무엇을 기대하는지 확인하기 전에는 호환된다고 단정하지 않는다. 14개 리테일러 중 BCP URL이 없는 5곳에 빈 시나리오를 둘지도 미정이다.

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

2026-09-25 D012에 따라 1차 테스트 입력에는 일반 Brand Page와 Brand Category Page를 함께 둔다. 일반 Brand Page는 ID8·9·10만 수집하고, Brand Category Page는 ID8·9·10·18·19·20·21·22·23을 모두 수집한다. 2026-09-28에는 [입력 Excel의 159개 URL 전체](../1차%20테스트/bcp-zyte-poc/results_population/20260928-all-159/전체_URL_판정_진행상태.csv)를 Zyte로 수집하고 1차 판정을 기록했다. 이 작업은 별도의 5,946개 전체 URL 수집을 완료했다는 뜻이 아니다. 원본 주소 충돌, 본문 상품 목록 로딩, 일부 이미지와 배너의 판정 경계는 결과표에서 별도 상태로 남긴다.

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
