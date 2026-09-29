# 원본 자료와 AI용 추출본 안내

정리일: 2026-09-25. 제공 원본 문서 8개, 후속 전달된 Zyte 코드 가이드와 운영 Docker v1.9.28 배포 자료를 보존하면서 검색용 Markdown을 관리한다.
파일명 날짜는 문서 식별에 사용하며 승인일이나 현재 운영 상태를 보증하지 않는다.

## 원본별 역할

각 추출본 맨 위에 실제 원본 경로 링크가 있다. 시트 번호는 해당 파일의 저장 순서, 슬라이드 번호는 1부터 센 순서다.

| ID | 원본 식별 | 용도 | 추출본 |
| --- | --- | --- | --- |
| S01 | 과제 현황 보고 v1.6, 20260807, PPTX | 배경·목적·당시 범위·운영 체계 | [슬라이드별 텍스트](sources/S01-project-overview.md) |
| S02 | 진단 항목 상세정의서 v1.0, 260812, PPTX | 진단 항목 설명·계산 예시 | [슬라이드별 텍스트](sources/S02-assessment-definitions.md) |
| S03 | W37 주간업무, 20260910, PPTX | 해당 시점의 진척·이슈·의사결정 안건 | [슬라이드별 텍스트](sources/S03-weekly-report.md) |
| S04 | 진단 항목 v1.95, 20260915, XLSX | 34개 지표 정의·판정·집계·기준정보 | [시트 목록](sources/S04-assessment-criteria.md), [지표 카탈로그](METRIC_CATALOG.md) |
| S05 | Assessment Summary / Improvement Tracker V0.1, 20260911, XLSX | 실제 Excel 집계식·개선 과제·ID별 입력 데이터 | [시트 목록](sources/S05-assessment-tracker.md) |
| S06 | 인수인계 워크숍 세부주제, DOCX | 확인해야 할 운영 지식과 질문 | [문단·표 추출본](sources/S06-handover-workshop.md) |
| S07 | 인수인계 완료 확인서 v1_1, DOCX | 인계 대상 체크리스트와 검수 양식 | [문단·표 추출본](sources/S07-handover-checklist.md) |
| S08 | collected-pages (1), CSV | 페이지별 수집 결과 열과 환경 비교 데이터 | [스키마·분포 프로파일](sources/S08-collected-pages.md) |
| S09 | `retailer-zyte-actions-api-guide/` | 14개 리테일러 × 5개 대표 페이지의 Zyte 브라우저 액션 레시피, 실행기, 오프라인 자산 저장·검사 코드 | [가이드 README](../retailer-zyte-actions-api-guide/README.md), [상세 README](../retailer-zyte-actions-api-guide/capture/README.md). 실제 과거 HTML·스크린샷·오프라인 결과와 관측 보고서는 묶음에 포함되지 않음 |
| S10 | [운영 Docker 이미지(v1.9.28) 및 배포 키트](<../관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트/>) | 메일 링크의 이미지 2개·Compose·환경설정 양식·초기화 SQL, 대표 첨부 분석 MD/HTML: 원본 총 7개 | [파일·추출 목록](sources/S10-docker-delivery.md), [BCP 활용 검토](DOCKER_DELIVERY_REVIEW.md). 핵심 구현은 컴파일 모듈이며 컨테이너 실행·운영 재현은 미검증 |

최초 문서 8개의 원본 파일명·바이트 크기·SHA-256·추출 산출물 목록은 [manifest.json](sources/manifest.json)에 있다. S10의 원본 7개는 별도 [다운로드-목록.json](<../관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트/다운로드-목록.json>)으로 관리한다. 대표 첨부의 AI 분석 주장과 직접 확인한 이미지·소스·문자열 증거는 구분한다.

## 어떤 파일부터 찾을 것인가

| 작업 | 먼저 볼 자료 |
| --- | --- |
| 목적과 제품 방향 | PROJECT_CONTEXT.md, S01 슬라이드 2–3 |
| 지표·판정·집계 | BUSINESS_RULES.md, METRIC_CATALOG.md, S04 시트 1, 해당 S02 슬라이드 |
| 실제 Excel 계산 | S05 Summary / Summary Detail → 수식이 참조하는 개별 ID 시트 |
| 경쟁 브랜드·검색어·제외 키워드·지역 설정 | S04의 해당 시트. 예전 `(old)` 시트와 숨김 시트 여부 확인 |
| Flixmedia 적용 대상·변경 상태 | S04 Flixmedia 현황, S03의 날짜가 있는 현황. 현재 운영 상태는 별도 검증 |
| 수집 데이터 연결 | S08 프로파일·원본 CSV, S06 세션 2·3·8 |
| Zyte 요청·액션·수집 결과 | [CRAWLING.md](CRAWLING.md)에서 검증 상태 확인 → S09 코드·README → 필요하면 PoC `manifest.json`과 HTML·스크린샷 |
| 인수인계 누락 점검 | S06·S07. 체크리스트 존재와 실제 인계 완료를 구분 |

## 변환 범위와 한계

| 형식 | 보존한 것 | 이 추출본만으로 확인할 수 없는 것 |
| --- | --- | --- |
| PPTX | 슬라이드별 텍스트, 그룹 안 텍스트, 표, 발표자 노트 | 그림 속 글자, 도형 간 관계, 차트 수치, 화면 스크린샷, 색·선택 표시, 시각적 읽기 순서 |
| DOCX | 본문 순서의 문단과 표, 문단·표 번호 | 페이지 배치, 머리말·꼬리말, 그림, 댓글·변경 추적의 전체 의미, 서명·체크 상태의 시각 확인 |
| S04 XLSX | 23개 시트의 비어 있지 않은 값·수식·저장 캐시, 병합 범위, 숨김 행·열·시트 | 표시 서식, 그림·차트·조건부 서식, 링크 관계·주석, Excel 재계산 결과 |
| S05 XLSX | 38개 시트 목록. Summary, Summary Detail, 기준_Reference, 데이터 누락점검, 톤다운 버전은 값·수식 전체 | 나머지 시트는 값이 있는 첫 12행과 첫 12개 수식 표본만 추출. RawData의 전체 내용은 원본 필요 |
| CSV | 41개 열의 빈값 수, 주요 분포, 7,107행 확인, 캡처일 문자열 범위, URL 문자열 중복 수 | best_quality 생성·선택 로직, 외부 HTML/스크린샷의 실제 내용, 진단 점수와의 조인 |

PPT에 `Manual/Crawling`, `Daily/Monthly`, `Y/N`이 모두 추출돼 있으면 색상이나 선택 표식이 빠졌을 수 있다. 텍스트 나열만으로 선택값을 추정하지 말고 Excel 정의 또는 원본 화면을 확인한다.

Excel의 날짜 셀은 표시 서식 없이 일련번호로 나올 수 있고 백분율은 0–1의 저장값으로 나올 수 있다. 셀의 저장값과 표시값을 구분한다. 공유 수식은 원본 수식과 셀 위치를 이용해 상대 참조를 복원했으며 OOXML 속성을 함께 기록했다. 빈 셀을 임의로 채우거나 병합 셀 값을 복제하지 않았다.

일부 Excel 시트는 실제 값보다 훨씬 큰 사용 범위를 선언한다. 예를 들어 S05 `Improvement Task`의 최대 행 선언은 데이터 건수가 아니다. 추출기는 실제 값·수식이 있는 셀을 기준으로 처리한다.

이번 작업은 원본을 로컬에서 읽었다. CSV 안의 외부 저장소 URL에 접속하거나 원본을 외부 서비스에 업로드하지 않았다.

## 갱신 방법

추출기는 [scripts/extract_context.py](../scripts/extract_context.py)다. Python 3과 `python-docx`, `python-pptx`, `openpyxl`을 사용하며, 원본을 수정하지 않고 추출본·카탈로그·manifest를 다시 쓴다.

```bash
python3 scripts/extract_context.py
```

현재 Codex 환경에서 확인한 Python 경로는 `/Users/codestepseunghee/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`다. 다른 환경에서는 위 패키지가 설치된 런타임을 사용한다. 산출물 폴더를 먼저 삭제할 필요가 없다.

1. 새 버전 원본을 보존하고 출처·적용 상태를 확인한다. 같은 접두사의 원본이 둘 이상이면 추출기의 `SOURCES` 매핑을 수정해 대상 파일을 명시한다. 추출기는 임의로 최신 파일을 선택하지 않는다.
2. 추출기를 실행하고 원본 해시·지표 ID·시트 수·주요 셀을 확인한다.
3. 변경된 정의와 기존 계산의 차이를 BUSINESS_RULES.md에 반영한다. 자동 추출만으로 마스터의 의미가 갱신되지는 않는다.
4. 사용자 확정 내용은 DECISIONS.md에 남기고 PROJECT_CONTEXT.md의 상태·날짜를 갱신한다.

기계 추출본에 직접 해석을 덧쓰면 재실행 시 사라진다. 해석은 PROJECT_CONTEXT.md / BUSINESS_RULES.md / DECISIONS.md에 기록한다.

## AGENTS.md를 쓰는 이유

Codex는 작업 시작 시 AGENTS.md를 읽어 지시를 구성한다. [공식 문서](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
모든 AI 도구가 같은 파일명을 자동 인식한다고 보장하지 않는다. 다른 환경에서는 `AGENTS.md`와 `PROJECT_CONTEXT.md`를 직접 전달하거나 해당 도구의 프로젝트 지시에서 이 문서를 읽도록 연결한다. 목적·핵심 로직의 본문은 모델과 무관하게 읽을 수 있는 Markdown으로 유지한다.
