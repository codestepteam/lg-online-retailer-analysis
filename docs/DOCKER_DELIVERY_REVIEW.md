# 운영 Docker v1.9.28 전달본과 BCP 활용 검토

확인일: 2026-09-25. 다운로드·원본 정리는 사용자 요청에 따라 GPT-5.6 Sol이, 이 분석은 현재 Astra가 수행했다. 컨테이너·전달받은 프로그램은 실행하지 않았다.

## 먼저 결론

**브랜드 카테고리 페이지(Brand Category Page, BCP)와 관련된 수집·분석 실행 모듈이 들어 있다. 다만 편집 가능한 Python 원본 전체를 받은 것은 아니다.** 이미지 내부의 실행 순서 코드, BCP 대상 URL을 넣는 SQL, 브랜드 수집·파싱 모듈, 9개 진단 함수에 대응하는 문자열을 확인했다. 핵심 구현은 `.so`라는 컴파일된 파일이다.

실행 환경을 다시 만드는 출발점으로 사용할 수 있지만, 이 파일들만으로 콘센트릭스 운영 환경과 데이터까지 그대로 복원했다고 할 수 없다. DB 덤프·실제 설정·인증 정보·외부 저장소 및 기준 데이터가 추가로 필요하다. 서비스 기동과 실제 BCP 수집·판정은 이번에 검증하지 않았다.

## 1. 받은 파일과 출처

출처는 Dooray의 [「FW: [LG HS Clinic] 운영 Docker 이미지(v1.9.28) 및 배포 키트 전달」](https://codestep.dooray.com/mail/systems/inbox/4427413851278093293)이다. 최종원(Concentrix)의 원본 메일은 2026-09-22 17:36 KST, 장재휴 대표의 전달 메일은 2026-09-23 01:01 KST다. 원본 메일은 당시 운영 서버와 같은 이미지라고 설명하지만, 실제 운영 서버의 이미지 해시와 대조하지 않았다.

저장 폴더: [관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트](<../관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트/>).

| 파일 | 바이트 | 역할 |
| --- | ---: | --- |
| `images/lge-hs-clinic_airflow_v1.9.28.tar.gz` | 1,362,293,047 | 수집·처리 작업과 Airflow 실행 이미지 |
| `images/lge-hs-clinic_api_v1.9.28.tar.gz` | 128,456,258 | 업로드·작업 시작 요청을 받는 API 이미지 |
| `docker-compose.prod.yml` | 8,002 | 여러 서비스를 함께 띄우는 구성 |
| `.env.example` | 4,490 | 설정 양식. 전부 빈 값이 아니라 예시·기본값·자리표시자가 들어 있음 |
| `docker/mysql/init/01_init.sql` | 1,054 | 데이터베이스 생성과 계정 권한 부여 |
| `clinic-collect-judge.md` | 46,696 | 대표가 첨부한 AI 분석 문서, 규칙·테스트 결과 설명 |
| `clinic-collect-judge.html` | 38,058 | 대표가 첨부한 사람이 읽기 쉬운 설명 문서 |

7개 원본을 보존했고, 별도 [다운로드-목록.json](<../관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트/다운로드-목록.json>)에 크기와 SHA-256(파일 변경 여부를 비교할 수 있는 해시값)을 기록했다. 두 이미지의 gzip 압축 검사가 통과했다. 발신자가 제공한 별도 체크섬과의 대조는 아니다. 만료되는 서명 URL은 메타데이터에 저장하지 않았다.

메일의 다운로드 만료 안내는 2026-09-29 17:23 KST다. 이미 내려받은 파일의 사용 기한을 뜻하지 않는다.

## 2. BCP 코드가 있는지 확인한 근거

### 직접 읽을 수 있는 실행 코드

이미지에서 추출한 [`lg_clinic_pipeline.py`](../data/docker-inspection/v1.9.28/airflow/rootfs/opt/project/dags/lg_clinic_pipeline.py)의 실제 코드에서 다음을 확인했다.

- 45–50행: `brand`를 `lg_clinic_brand` 작업에 연결한다.
- 118–123행: `--page-type brand`와 국가·리테일러·제한 개수 등의 명령 인자를 조립한다. 브랜드 범위 인자는 `apply_brand_scope=True`인 보고서 단계에서만 조립한다.
- 189–203행: `crawl.py`, `parse.py`, `make_report.py`를 작업으로 만든다.
- 286행: PDP 이외의 작업은 `crawl → parse → report` 순서로 연결한다.
- 293행: `_build_track_dag("brand")`를 실제로 호출한다.

이것은 단순히 `brand`라는 파일명이 있다는 근거보다 강하다. 실제 실행 순서 정의에 브랜드 처리 작업이 포함되어 있다. 다만 그 안의 컴파일된 함수까지 모두 추적한 것은 아니다.

[`crawl.py`](../data/docker-inspection/v1.9.28/airflow/rootfs/opt/project/crawl.py) 4–13행은 같은 폴더의 `crawl.*.so`를 찾아 모듈로 불러온다. 따라서 눈에 보이는 짧은 Python 파일은 핵심 소스가 아니라 컴파일된 구현을 실행하는 연결 코드다. `parse.py`, `make_report.py`도 같은 형태다.

### 대상 URL의 생성과 소비 흔적

- [`041_brand_target_nlmm_lg.sql`](../data/docker-inspection/v1.9.28/airflow/rootfs/opt/project/migrations/041_brand_target_nlmm_lg.sql) 13–28행은 네덜란드 MediaMarkt의 LG 냉장고·세탁기 URL을 `brand_target_list` 테이블에 넣는 SQL이다. 페이지 분류에 **`Brand Category Page`**를 명시한다. 이 SQL이 전달받지 못한 실제 운영 DB에 적용되었는지는 미확인이다.
- `core/repo.*.so`의 읽기 전용 상수 영역에서 `brand_target_list`의 국가·브랜드·제품군·세부 제품군·페이지 유형·URL을 읽는 SELECT 문을 확인했다. `brand_url IS NOT NULL` 조건이 있다. [추출 문자열 175행](../data/docker-inspection/v1.9.28/airflow/strings/core/repo.cpython-311-x86_64-linux-gnu.strings.jsonl), 원본 바이트 위치 `0x87e40`.
- `crawl.*.so`에 `load_brand_targets`, `brand_page_type`, `Brand Category Page` 문자열이 있다. [수집 모듈 추출 문자열](../data/docker-inspection/v1.9.28/airflow/strings/crawl.cpython-311-x86_64-linux-gnu.strings.jsonl).

이로써 BCP를 저장하는 입력 구조와 이를 읽는 SQL·수집 모듈의 존재를 확인했다. 문자열만으로 모든 호출 분기와 최신 운영 대상 목록을 확정하지 않는다.

### 포함된 브랜드 모듈과 진단 관련 흔적

`crawl_retailers/brand/`와 `parse_retailers/brand/`에 각각 다음 14개 이름의 리테일러 모듈이 있다: alza, amazon, boulanger, but_fr, coolblue, darty, datart, elcorteingles, elgiganten, mediaexpert, mediamarkt, mediaworld, rtveuroadd, unieuro. 모듈 수는 지원 국가·사이트 수 또는 현재 수집 성공 건수가 아니다.

공통 브랜드 파서의 바이너리에는 HTML 요소를 찾는 정규식·선택자와 `hero_banner`, `why_lg_block`, `usp_block`, `category_navigator`, `product_list`, FAQ 관련 이름이 있다. 예를 들어 Why LG를 여러 언어로 찾는 정규식이 실제 포함되어 있다. [공통 브랜드 파서의 추출 문자열](../data/docker-inspection/v1.9.28/airflow/strings/parse_retailers/brand/_common.cpython-311-x86_64-linux-gnu.strings.jsonl) 159행, 원본 위치 `0x3d660`.

`core/eval.*.so`에는 BCP 9개 항목에 해당하는 함수명과 결과 키가 들어 있다.

| 항목 | 뜻 | 확인한 함수명 |
| --- | --- | --- |
| ID8 | 이미지의 대체 설명(Alt text) | `metric_08_brand_page_alt_text` |
| ID9 | 제목·설명·검색 허용 태그 | `metric_09_brand_page_metadata` |
| ID10 | 대표 주소(Canonical URL) | `metric_10_brand_page_canonical_url` |
| ID18 | 첫 화면의 대표 배너 | `metric_18_brand_hero_banner` |
| ID19 | LG 브랜드 소개 | `metric_19_brand_why_lg` |
| ID20 | 핵심 제품 장점(USP) 블록 | `metric_20_brand_usp_block` |
| ID21 | 제품군으로 이동하는 메뉴 | `metric_21_brand_category_navigator` |
| ID22 | 제품 상세로 이어지는 제품 목록 | `metric_22_brand_product_list` |
| ID23 | 자주 묻는 질문과 답변(FAQ) | `metric_23_brand_faq` |

근거: [판정 모듈 추출 문자열](../data/docker-inspection/v1.9.28/airflow/strings/core/eval.cpython-311-x86_64-linux-gnu.strings.jsonl). 대표 첨부 문서의 「3. 판정 진입」도 `brand`의 대상이 이 9개라고 설명한다. **함수명 존재는 동작·정확도·최종 보고서 채택을 검증한 사실이 아니다.** 첨부 문서가 주장하는 함수 호출 테스트는 이번 분석에서 재실행하지 않았다.

## 3. 콘센트릭스 환경을 그대로 만들 수 있는가

**프로그램 실행 구성을 재현할 자료는 상당 부분 받았다. 운영 데이터와 설정을 포함한 완전한 복제본은 아니다.**

| 구분 | 이번 전달본으로 확인한 범위 | 재현 전에 남은 것 |
| --- | --- | --- |
| 애플리케이션 | 두 이미지의 태그가 v1.9.28, OS는 Linux, CPU는 amd64 | 실제 운영 이미지 해시와 동일성·기동 검증 |
| 서비스 구성 | MySQL, MinIO(파일 저장소), FastAPI, Airflow 초기화·웹서버·스케줄러 구성 | Docker 실행 환경, 실제 설정·접속 비밀값 |
| 데이터베이스 | 외부 `01_init.sql`은 DB 생성·권한 부여만 수행 | 덤프 복원, 현재 테이블·기준 데이터·운영 대상 URL |
| 외부 서비스 | ScrapingBee 설정 전달과 연동 모듈, BigQuery·GCS 관련 설정 항목 | 실제 사용하는 경로별 계정·권한·데이터 접근 |
| 보고서·화면 | 수집·파싱·Excel 보고서 작업 정의 | 기존 대시보드 전체 재현 여부는 이 구성으로 입증되지 않음 |

구체적인 제약은 다음과 같다.

1. **DB 초기화는 데이터 복원이 아니다.** 외부 [01_init.sql](<../관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트/docker/mysql/init/01_init.sql>)은 DB 두 개 생성과 권한 부여만 한다. 이미지 내부에 `02_schema.sql`과 62개 변경 SQL 파일은 있지만, 전달된 Compose의 MySQL 서비스는 호스트의 `docker/mysql/init/`을 읽는다. Airflow 이미지 안의 SQL이 MySQL 초기화 폴더에 자동으로 연결되지 않는다. 내부 SQL을 그대로 모두 실행해 현재 운영 DB를 재현할 수 있는지도 검증하지 않았다.
2. **운영 DB의 기준값이 결과에 영향을 준다.** 첨부 문서 「7. 빈 refdata와 미확인」은 USP 키워드 테이블이 없는 테스트 환경에서 USP 조회 결과가 비고, 브랜드 목록 테이블이 없을 때 필터가 적용되지 않았다고 보고한다. 이번에 운영 DB가 없어 이 동작을 재현하지 않았으나, 덤프를 받아야 하는 구체적인 이유가 된다.
3. **MySQL·MinIO 이미지가 별도로 필요하다.** Compose는 `mysql:8.0`, 기본 `minio/minio:latest`, `minio/mc:latest`를 참조한다. 전달된 두 tar에는 이 별도 서비스 이미지가 포함된 것으로 볼 수 없다. 운영 버전을 정확히 맞추려면 실제 태그·digest를 확인해야 한다.
4. **이 Mac과 이미지 CPU 종류가 다르다.** 로컬 `uname -m`은 `arm64`, 이미지 메타데이터는 `amd64`다. 실행 시 해당 아키텍처 지원·호환 실행 조건을 확인해야 한다. 이번에 실행 가능 여부나 성능을 측정하지 않았다.
5. **Zyte 설정으로 바로 바뀌지 않는다.** Compose는 `SCRAPINGBEE_API_KEY`를 전달하고, 이미지 `core/config.*.so`에 ScrapingBee API 주소가 있으며 `crawl.*.so`에 해당 모듈과 호출 경로 관련 문자열이 있다. 프로젝트에서 이미 선택한 Zyte는 별도 서비스다. 기존 이미지에 Zyte 키만 넣으면 전환된다고 볼 근거는 없다.

근거: [배포 Compose](<../관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트/docker-compose.prod.yml>) 22–70, 73–126, 143–197행; [Airflow 이미지 목록](../data/docker-inspection/v1.9.28/airflow/inventory.json); [API 이미지 목록](../data/docker-inspection/v1.9.28/api/inventory.json). 메일은 비밀값·DB 덤프·상세 매뉴얼을 별도 제공한다고 설명한다. `BQ_*`, `GCS_*`가 Compose에 등장한다는 사실만으로 모든 BCP 작업이 해당 서비스 없이는 불가능하다고 단정하지 않는다.

## 4. 이번 BCP 업무에서 얻을 수 있는 것

- **처음부터 설계를 추측할 필요가 줄었다.** 대상 URL 저장 구조, 브랜드 전용 실행 경로, 수집 이후 파싱·보고서 연결을 볼 수 있다.
- **기존 구현을 비교 대상으로 삼을 수 있다.** 환경을 준비하면 같은 BCP HTML을 기존 파서에 넣고 결과를 비교하는 실험이 후보가 된다. 이것은 다음 작업 제안이며 이번에 실행한 결과는 아니다.
- **사이트별 처리의 출발점을 얻었다.** 첨부 분석에는 더보기·페이지 넘김·배너·FAQ 처리 방식이 정리되어 있다. 해당 사이트의 현재 화면에서 동작하는지는 재검증해야 한다.
- **기존 구현과 업무 정의의 차이를 찾을 수 있다.** 아래 차이가 특히 BCP에 중요하다.

### 기존 엔진의 점수를 바로 정답으로 쓰면 안 되는 이유

오른쪽 열은 대표가 첨부한 AI 분석 문서의 테스트 주장이다. 이번 분석이 직접 재현한 결과가 아니다. 왼쪽은 [『EY_LGE HS 온라인 리테일 클리닉 진단 항목_v1.95_20260915 (1).xlsx』](<../관련문서/EY_LGE HS 온라인 리테일 클리닉 진단 항목_v1.95_20260915 (1).xlsx>)의 「Clinic 진단 항목」 탭 원문이다.

| 항목 | 진단 엑셀의 정의 | 대표 첨부 「3.1 지표 계약」의 설명 | 이번 해석 |
| --- | --- | --- | --- |
| ID8 이미지 설명 | 큰 이미지 상위 10개에 모두 설명이 있어야 Y | 누락·무의미한 설명 수를 10에서 차감하는 점수 | Y/N과 0–10점의 변환·최종 집계 관계 확인 필요 |
| ID9 검색용 태그 | Robots는 `index, follow` 요구 | `noindex`도 태그 존재로 통과 | 조건 불일치 후보. 검색 금지인데 통과하는지 직접 시험 필요 |
| ID10 대표 주소 | 대표 주소 태그 포함 여부 | 현재 URL과 경로·호스트 등이 다르면 0점 | 정의보다 추가 비교를 하는지 확인 필요 |
| ID21 카테고리 이동 | 클릭 가능하고 해당 제품군 탐색 페이지로 정상 이동 | `clickable_count`가 1 이상이면 10점 | 링크 존재만으로 도착 페이지 정상 여부를 입증할 수 없음 |
| ID18–23 콘텐츠 항목 | 엑셀의 Crawling Data는 N, 과거 판정표는 Eye-Check Raw Data | 자동 추출·판정과 공통 휴리스틱을 설명 | 코드 존재와 실제 납품 결과 생성·수기 검수 경로의 관계 확인 필요 |

원문 위치: 진단 엑셀 「Clinic 진단 항목」 T16/W16, T17, T18/W18, T27/W27, Y19/Y24:Y28. [해당 탭의 원문 추출본](sources/S04-assessment-criteria/sheet-01.md). 대표 첨부 [clinic-collect-judge.md](<../관련문서/운영 Docker 이미지(v1.9.28) 및 배포 키트/clinic-collect-judge.md>) 279–316행, 517–645행. 공통 휴리스틱을 사용했다는 설명 문구 자체는 `core/eval.*.so` 안에도 존재한다(추출 문자열 1097행, `0x1127c0`).

## 5. 권장하는 다음 작업 — 사용자 결정 아님

현재 목표가 BCP만 수집·판정하는 것이므로, **BCP 한 페이지와 9개 항목으로 기존 방식과 새 방식의 차이를 확인하는 것**을 제안한다.

1. 대표 예시 BCP 하나와 적용할 판정 기준을 선택한다. 현재 프로젝트의 Coolblue LG 냉장고 예시는 화면을 확인한 적이 있지만, 이 이미지의 수집기로 성공한 사례는 아니다.
2. 이미 선택한 Zyte로 HTML·화면·링크 근거를 수집하는 기존 프로젝트 설정을 점검한다. `retailer-zyte-actions-api-guide`의 `brand-category` 설정은 이번 Concentrix 이미지와 별개 자료다.
3. 자동으로 뽑을 값과 실제 합격 기준을 대조한다. 특히 검색 허용 태그, 이미지 선정·설명 품질, 클릭 후 도착 페이지를 먼저 확인한다.
4. 기존 엔진과 결과 비교가 필요하면 DB 덤프·기준값·키를 준비하고 별도 테스트 환경에서 브랜드 작업만 제한 실행한다. `brand`가 BCP만을 뜻하는지, Brand Page 대상도 섞이는지는 DB 대상 분류를 함께 확인한다.

콘센트릭스에 요청할 자료는 **현재 BCP 대상 URL·기준 테이블이 포함된 DB 덤프, v1.9.28 복원·실행 절차, 실제 BCP 실행 예시와 산출물, 자동 판정과 수기 수정의 연결 설명, 수정 가능한 브랜드 수집·파싱·판정 소스의 인계 범위**다. 기존 운영 환경을 채택하거나 Zyte 결정을 변경한 것은 아니다.

## 분석 재현과 한계

- [`inspect_delivery_image.py`](../scripts/inspect_delivery_image.py)는 Docker 이미지를 실행하지 않고 레이어 순서대로 `/opt/project`, `/opt/airflow/dags`, `/app`의 일반 파일을 추출한다. 심볼릭 링크를 따라가지 않고 삭제 마커를 반영한다. 전체 운영체제 파일 분석은 아니다.
- [`extract_elf_evidence.py`](../scripts/extract_elf_evidence.py)는 컴파일 파일의 읽기 전용 문자열 영역을 원본 바이트 위치와 함께 저장한다. 복원된 Python 소스나 실행 추적이라고 부르지 않는다.
- API 이미지에서 선택된 파일 362개, Airflow 이미지에서 369개. 각 이미지에 `.so` 228개가 있고, 공통 경로 361개는 파일 해시가 전부 일치했다. `/opt/project`의 Python 파일 54개 중 45개는 컴파일된 모듈을 로드하는 연결 코드 패턴을 포함한다.
- `.so` 내부에 Cython 생성 식별자와 빌드 경로가 있다. 메일의 “CPython으로 컴파일” 표현만으로 판단한 것이 아니라, 실제 Cython 생성 흔적을 확인했다. 원본 전체 복원은 수행하지 않았다.
- 다운로드, 정적 파일·SQL·문자열 분석과 문서 대조를 수행했다. Docker 기동, DB 복원, 외부 크롤링, 함수 호출 테스트, 점수 계산 검증은 수행하지 않았다.
