# BCP ID8 파일 용량 기준 3차 테스트

> 2026-10-12 확인: 팀원이 `lg-pipeline/pipeline/bcp/`에 같은 방향의 ID8 기준(원본 파일 바이트 내림차순, 최대 10개, 같은 크기는 먼저 나온 순서)을 넣었다. 이 3차 시험과 세부까지 같은지는 확인하지 않았다. [lg-pipeline ID8 설명](../../lg-pipeline/docs/bcp-id8-image-recovery.md), [동기화 메모](../PROJECT_CONTEXT.md#2026-10-12-팀-저장소-현황-동기화)

이 디렉터리는 사용자의 2026-10-01 지시에 따라 `2차 테스트(temporal)/`을 **복사**해 만들었다. 사용자는 EY 피드백 이후의 변경이므로 2차 테스트를 직접 수정하지 말라고 했다. EY 피드백 원문은 이 저장소에서 확인하지 못했으며, 출처는 사용자의 설명이다. 아래 「복사 당시 안내」 부분은 2차 코드의 이력을 보존한 것으로, 현재 3차 실행 명령이 아니다.

## 이번에 바꾼 것과 비교 방법

- Brand Category Page(브랜드·제품군 페이지, BCP)의 ID8에 한해, 대상 HTML 이미지 중 **보관된 이미지 파일의 바이트 수가 큰 순서**로 최대 10개를 고른다. 본문·제품 카드 포함, CSS 배경·순수 장식 제외, 이미지 자체의 의미 있는 `alt` 설명 확인 조건은 유지한다. 파일 크기가 같은 경우에는 수집 당시 이미지 순서를 사용한다.
- 2차 Temporal 회차 `bcp-local-retry-20260929T172142Z`의 저장 화면·이미지 보관 목록·기존 ID8 결과를 **읽기만** 한다. 3차용 Zyte 재수집이나 Temporal 재실행은 하지 않았다. 따라서 수집 시점 차이가 이번 비교에 섞이지 않는다.
- 이미지 용량이 하나라도 확인되지 않으면 그 URL은 이번 비교에서 Y/N으로 판정하지 않는다. 이 보류 방식은 불완전한 근거로 추정하지 않기 위한 시험 구현이며 사용자 승인 운영 정책은 아니다.
- 3차 AI 검토는 이미지 번호와 한국어 이유를 기록한다. AI가 본문/제품 이미지와 장식·사이트 공통 이미지를 구별하고 설명의 의미를 판단하므로, Y/N 차이를 파일 크기 순위 변화의 인과 효과라고 바로 해석하지 않는다.

입력은 GCS의 `gs://lg-content-capture-20260909-assets/pipeline/batches/bcp-local-retry-20260929T172142Z/score-index.json`과 각 URL의 `raw.html`, `screenshot.jpg`, `assets/manifest.json`, `observations/<URL 행>/parser.json`이다. 실행 파일은 [`retest_id8_file_bytes.py`](retest_id8_file_bytes.py), 변경된 AI 질문은 [`ai_observe.py`](ai_observe.py), ID8 결과 계약은 [`scoring/bcp/v1/id_8.py`](scoring/bcp/v1/id_8.py)다. 프로젝트 루트 `.env`의 `OPENAI_API_KEY`와 Google Cloud 기본 인증을 사용한다. 키는 결과에 저장하지 않는다.

```sh
/Users/codestepseunghee/codestep/lg-crawling/.venv/bin/python '3차테스트/retest_id8_file_bytes.py' --prepare-only
/Users/codestepseunghee/codestep/lg-crawling/.venv/bin/python '3차테스트/retest_id8_file_bytes.py'
```

현재 결과는 [비교 요약](results/id8-file-bytes-20261001/비교_요약.md)과 [URL별 JSON](results/id8-file-bytes-20261001/comparison.json)에 있다. AI 원응답은 같은 결과 폴더의 `runs/bcp-ai/8/`에 별도로 보존했다.

## 복사 당시 안내 — 2차 코드의 이력

### BCP 1차 테스트의 로컬 변환본

이 폴더는 `1차 테스트/bcp-zyte-poc`의 **Brand Category Page(BCP)** 수집·근거 추출·판정을 동료 `lg-crawling`의 리테일러별 시나리오 형태로 옮기기 위한 로컬 작업본이다. D028에서 이 변환본을 로컬 [`lg-crawling/bcp/README.md`](../../lg-crawling/bcp/README.md)의 발행·Temporal 실행 경로에 연결했고, D029에서 14개 시나리오를 GCS에 발행했다. 아래의 미연결 설명은 최초 변환 당시 상태를 기록한 것이다.

## 들어 있는 것

| 위치 | 역할 |
| --- | --- |
| `retailers/<리테일러>/scenarios/bcp/config.json`, `zyte/` | 1차 테스트의 쿠키·스크롤·더보기·메타데이터·배너 근거 수집 동작을 URL별 Zyte 요청으로 만들 재료 |
| `retailers/<리테일러>/scenarios/bcp/parser/bcp.py` | `parse(bundle)`로 저장 HTML과 수집 상태를 읽어 후보·본문·메타데이터를 `lg-diagnostic-observation-v1` 형태로 반환. 후보를 Y/N으로 판정하지 않음 |
| `retailers/<리테일러>/scenarios/bcp/observation/` | 동료의 관측 결과 JSON 스키마 사본 |
| `scoring/bcp/v1/id_*.py` | ID8·9·10·18·19·20·21·22·23의 `score(observation)` 함수 |
| `ai_observe.py` | 신뢰된 워커에서 새 화면을 AI에게 보내고 모델·질문 버전·응답·근거를 저장할 코드. 파일 생성·검증 과정에서는 호출하지 않음 |
| `navigation_observe.py` | ID21에서 실제 클릭·도착이 확인된 카드만 Jev에 묻고, 답과 근거를 관측 결과에 연결. 클릭 자체는 수행하지 않음 |
| `product_observe.py` | ID22에서 저장 HTML과 연결된 상품 목적지 검사 결과를 관측 결과에 연결. 목적지 수집 자체는 수행하지 않음 |
| `inputs/bcp-urls.json` | 1차 테스트 URL 목록에서 BCP로 분류한 139행. 이 중 실제 이번 URL 대상은 9개 리테일러이고, 수집 설정은 14개 리테일러에 존재함 |

## 판정 방식

ID9·10은 기존의 코드 규칙을 옮겼다. ID8·18·19·20·23은 **현재 URL의 수집본과 연결된 AI 응답이 있어야만** Y/N을 반환한다. 특히 ID18은 AI에게 **페이지 전체 스크린샷**을 보내고, 배너 후보의 위치·크기·주변 문구는 보조 정보로 제공한다. 스크린샷이 없으면 ID8·18은 판정 불가다. 과거 엑셀 행 번호별 AI 판단값은 이 변환본에 넣지 않았다.

`ai_observe.py`는 동료의 기존 이미지 관측 코드와 같은 GPT-6 Luna 요청 형식을 **로컬 변환용 구현 선택**으로 사용한다. 사용자가 BCP 운영 모델을 확정한 것은 아니며, Jev의 이미지 입력 지원 여부도 이 코드로 확인한 것은 아니다. 실제 모델 호출은 하지 않았다.

ID21은 평가 대상 탐색 카드를 실제 클릭하고 도착 제품군까지 확인한 기록이 필요하다. 지금 1차 테스트에서 이 방식으로 구현한 것은 Datart 38행 시험뿐이다. `navigation_observe.py`는 그 클릭 기록의 원본 HTML 해시를 확인하고, 도착 화면 수집이 유효한 카드에만 Jev를 호출한다. ID22는 선정한 상품 카드의 상세 페이지 도착 기록이 필요하며, 현재 방식은 최대 2개를 검사한다. `product_observe.py`는 **새 수집본의 HTML 해시와 URL이 붙은** 검사 결과만 받아들인다. 기존 1차 테스트의 상품 링크 JSON에는 이 해시가 없으므로 그대로 재사용하지 않는다. 이 기록이 없으면 두 항목 모두 `indeterminate`로 남긴다. `lg-crawling`에서 이는 1차 결과표의 `REVIEW`에 대응하는 상태이며 N으로 바꾸지 않는다. 예전 수집에서 원본 URL 불일치로 보류한 Datart 40·41행과 Amazon Italy 80행도 정상 BCP 판정으로 간주하지 않아야 한다.

동료의 채점 결과 계약은 `completed`일 때 `value`를 저장하고 `reason`을 허용하지 않는다. 이 변환본은 AI가 설명한 이유를 별도의 관측 기록에 저장하고, 항목별 결과에는 그 기록의 URI를 근거로 남긴다. 판정 불가 상태에는 `reason` 코드를 남긴다.

## 로컬 확인

프로젝트 루트에서 다음 명령을 실행한다. 두 명령 모두 GCS·Zyte·AI API를 호출하지 않는다.

```sh
python3 '1차테스트변환/build.py'
python3 '1차테스트변환/verify.py'
```

`build.py`는 현재 1차 테스트 파일을 다시 읽어 14개 시나리오 팁과 139행 입력 목록을 갱신한다. `compile_capture.compile_request(리테일러, URL_기록)`은 `zyte/` 파일의 해시를 검사하고 URL·브랜드·제품군을 주입한 요청 JSON을 반환한다.
`verify.py`는 139개 요청이 1차 테스트의 요청 JSON과 같은지, 저장된 139개 BCP 화면이 새 파서로 읽히는지, ID9·10 결과가 기존 1차 판정과 같은지 확인한다.

## 최초 변환 당시 남아 있던 연결 작업

1. `pipeline/scenarios.py`의 허용 시나리오와 발행 검증에 `bcp`를 추가하고, 이 폴더의 초안 `manifest.json`을 실제 불변 버전 패키지 형식에 맞춘다. **현재의 `lg-bcp-scenario-draft-v1`은 발행 가능한 스키마가 아니다.**
2. 수집 워커가 BCP 요청을 만들고 `lg-capture-state`가 들어 있는 HTML과 전체 스크린샷을 회차별 저장본에 남기게 한다. 파서 진입점을 `bcp.py`로 선택하고 BCP 항목에 맞는 채점 세트를 연결한다. 현재 일반 배치 채점은 PDP 전용이다.
3. 신뢰된 워커에서 `ai_observe.py`를 관측과 채점 사이에 연결한다. ID21 실제 클릭·도착 확인과 ID22 상품 상세 도착 확인을 리테일러별로 확장한다. AI 호출 실패·화면 불충분은 판정 불가로 남긴다.
4. 저장본으로 항목별 예상 결과를 검증한 뒤 Temporal 회차와 GCS 저장을 연결한다. 이 단계는 아직 수행하지 않았다.

후속 구현에서 1~3의 BCP 유형·발행·파서·채점·AI 연결과 ID22 도착 확인을 로컬 `lg-crawling`에 추가했다. D029에서 실제 GCS 발행과 139개 URL의 로컬 Temporal 회차를 실행했다. ID21 클릭 선택은 Datart 외 여러 리테일러로 확장했지만 모든 카드의 클릭·도착 확인이 끝난 것은 아니다. 원격 Worker 배포도 아직 완료하지 않았다. 현재 실행 상태는 [`PROJECT_CONTEXT.md`](../PROJECT_CONTEXT.md)의 「BCP 클라우드 이관 준비」를 참고한다.

원본: [`1차 테스트/bcp-zyte-poc`](../1차%20테스트/bcp-zyte-poc/). 동료 구조: [`lg-crawling`](../../lg-crawling/retailers/amazon-it/scenarios/pdp/).
