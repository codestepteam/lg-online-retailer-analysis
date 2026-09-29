# Brand Category Page Zyte 1차 테스트

이 폴더는 **동료가 전달한 `retailer-zyte-actions-api-guide`를 참고해 만든 1차 테스트용 별도 작업 공간**이다. 프로젝트 루트의 `retailer-zyte-actions-api-guide/`는 동료 전달 원본이며 이 폴더와 구분해 보존한다.

## 이 폴더에서 변경한 내용

- Alza, Datart, Boulanger, Amazon Italy, MediaWorld, Coolblue, MediaMarkt Netherlands, MediaMarkt Spain, Elgiganten의 Brand Category Page 전용 액션
- 모든 대표 페이지의 전체 스크롤 확인
- 리테일러별 쿠키 창, 설명 펼치기, 제품 더보기, 질문 펼치기
- 사람 확인 화면이 남은 수집을 정상 결과로 받아들이지 않는 검사
- ID8·9·10·22·23 근거를 수집하는 `capture/evidence.js`
- 정상 수집 후 단계별 상태와 진단 근거를 `capture-state.json`으로 별도 저장하는 실행기

리테일러별 주소와 액션, 9개 항목과 수집 근거의 연결은 상위 폴더의 [`Zyte_BCP_9개_항목_수집_액션_정의.md`](../Zyte_BCP_9%EA%B0%9C_%ED%95%AD%EB%AA%A9_%EC%88%98%EC%A7%91_%EC%95%A1%EC%85%98_%EC%A0%95%EC%9D%98.md)를 본다.

## 실행 전 검사

프로젝트 루트에서 실행한다.

```bash
python3 "1차 테스트/bcp-zyte-poc/capture/build_recipes.py"
python3 "1차 테스트/bcp-zyte-poc/tests/test_recipes.py"
python3 "1차 테스트/bcp-zyte-poc/tests/test_offline_assets.py"
python3 "1차 테스트/bcp-zyte-poc/tests/test_verify_offline.py"
```

Alza 대표 Brand Category Page의 Zyte 요청 내용만 먼저 검사하는 명령은 다음과 같다. 이 명령은 Zyte API를 호출하지 않는다.

```bash
python3 "1차 테스트/bcp-zyte-poc/scripts/zyte_capture.py" \
  --retailer alza \
  --page-type brand-category \
  --dry-run
```

## 실제 수집

실제 호출은 `--dry-run`을 빼고 실행한다. `ZYTE_API_KEY`는 이 폴더의 `.env`, 프로젝트 루트의 `.env`, 또는 현재 터미널의 환경변수에서 읽는다. 키 값은 결과 파일에 저장하지 않는다.

결과는 `output/offline/<리테일러>/brand-category/`에 저장된다.

- `request.json`: 실제 요청 내용
- `response.json`: 성공·실패 정보와 최종 주소
- `raw.html`: 액션 후의 페이지 HTML
- `screenshot.jpg`: 전체 페이지 화면
- `capture-state.json`: 액션 수행 상태와 9개 항목 판정에 사용할 구조화 근거

성공한 9개 수집본을 실행 시각별 결과 묶음으로 보존하는 명령은 다음과 같다.

```bash
python3 "1차 테스트/bcp-zyte-poc/scripts/save_bcp_batch.py"
```

2026-09-26 첫 실수집 결과는 `results/20260926T120245KST/`에 있다. 9개 모두 본문 수집 완료 조건을 통과했으며, 진단 판정 상태는 `미판정`이다. 화면 이미지는 5개만 페이지 전체가 저장됐고, Boulanger·MediaWorld·MediaMarkt Netherlands·MediaMarkt Spain은 Zyte의 최대 10,000픽셀 높이 제한으로 아래 영역이 잘렸다. `results/20260926T120245KST/수집_완전성_점검.md`에서 페이지별 상태를 확인한다.

다음 명령은 실수집 결과의 본문 수집 조건과 화면 이미지 완전성을 다시 점검한다.

## 9개 항목 근거 파서

현재 수집 묶음의 `raw.html`, `capture-state.json`, `response.json`을 읽어 9개 항목별 근거와 검토 후보를 추출한다. 이 단계는 Y/N 판정을 수행하지 않는다.

```bash
python3 "1차 테스트/bcp-zyte-poc/scripts/parse_bcp_evidence.py" "1차 테스트/bcp-zyte-poc/results/20260926T120245KST"
```

결과는 입력 수집 묶음 안에 저장된다.

- `파서_근거_요약.md`: 리테일러별 후보 수와 현재 단계
- `파서_근거_요약.csv`: 비교 가능한 항목별 개수
- `parsed/<리테일러>/bcp-evidence.json`: 항목별 원문·HTML 위치·후보 선정 이유

`screenshot.jpg`는 페이지 상태를 사람이 참고하는 보조자료다. 10,000픽셀 뒤가 잘려도 HTML과 수집 상태가 정상이라면 파서 입력 실패로 처리하지 않는다.

## 확정 기준으로 시작한 1차 판정

```bash
python3 "1차 테스트/bcp-zyte-poc/scripts/assess_bcp_evidence.py" "1차 테스트/bcp-zyte-poc/results/20260926T120245KST"
```

이 명령은 `parsed/<리테일러>/bcp-evidence.json`과 수집 당시 HTML·화면 상태를 읽어 `판정_1차_요약.md`, `판정_1차_요약.csv`, `assessed/<리테일러>/bcp-assessment.json`을 만든다. ID9 메타데이터와 ID10 Canonical 태그 존재 여부는 자동 검사한다. ID8은 아래의 이미지별 검토 기록이 있고 그 기록이 현재 HTML·화면 상태와 일치할 때만 검수한 Y/N을 반영한다. ID18~23은 `REVIEW`로 남긴다.

최신 9개 페이지의 ID8 이미지별 검토와 판정 반영은 다음 순서로 실행한다. 첫 명령은 이미지별 후보와 검토표를 만들며, AI가 이미지별로 확인해 작성한 `ID8_판정_검수.json`을 자동 생성하거나 덮어쓰지 않는다. 이 검수는 사용자 승인 결과가 아니다.

```bash
python3 "1차 테스트/bcp-zyte-poc/scripts/audit_id8_images.py" "1차 테스트/bcp-zyte-poc/results/20260928T060234KST"
python3 "1차 테스트/bcp-zyte-poc/scripts/assess_bcp_evidence.py" "1차 테스트/bcp-zyte-poc/results/20260928T060234KST"
```

검토 후보는 [`ID8_이미지_검토_요약.md`](results/20260928T060234KST/ID8_이미지_검토_요약.md)와 `ID8_이미지_검토.csv`, 이미지별 판정 이유와 원본 파일 확인값은 `ID8_판정_검수.json`에서 확인한다. 원본 수집 자료가 바뀌면 기존 ID8 검수 결과는 적용하지 않고 `REVIEW`로 둔다.

2026-09-26 첫 수집본은 MediaMarkt Spain·Netherlands, MediaWorld에서 스크롤 뒤 URL이 바뀌어 ID9·10을 `REVIEW`로 표시한다. 이를 확인하기 위해 스크롤 **전** 제목·메타 태그·H1·Canonical을 별도로 보존하는 액션을 추가하고 세 곳을 다시 수집했다. 새 결과에서는 처음 요청한 URL 기준 ID8이 Y 3곳·N 6곳(이미지별 AI 검수), ID9가 Y 7곳·N 2곳, ID10이 Y 9곳이다. 최신 [1차 판정 결과](results/20260928T060234KST/판정_1차_요약.md)에서 확인한다. 이 묶음은 나머지 6곳의 9월 26일 수집본과 재수집한 3곳의 9월 28일 수집본을 함께 보존하며, 각 페이지의 수집 시각은 `manifest.json`에 있다.

```bash
python3 "1차 테스트/bcp-zyte-poc/scripts/audit_bcp_batch.py" \
  "1차 테스트/bcp-zyte-poc/results/20260926T120245KST"
```

## URL 목록 159개 행의 1차 판정

사용자가 제공한 `Brand_BCP_1차_테스트_URL_목록.xlsx`의 `URL 목록` 탭 159개 행을 수집한 결과는 `results_population/20260928-all-159/`에 있다. 일반 Brand Page 20개는 ID8·9·10만, Brand Category Page 139개는 9개 항목을 평가한다. 원본 목록의 주소·브랜드가 맞지 않는 행은 `SOURCE_MISMATCH`, 근거가 부족하거나 기준 경계가 미정인 항목은 `REVIEW`로 남긴다. 이 두 상태는 N이 아니다.

판정표를 현재 저장본과 검사 기록에서 다시 만드는 명령은 다음과 같다.

```bash
python3 "1차 테스트/bcp-zyte-poc/scripts/assess_full_population.py" \
  "1차 테스트/bcp-zyte-poc/results_population/20260928-all-159"
```

- `전체_URL_판정_진행상태.csv`: 159개 행의 항목별 Y/N·검토 필요·원본 충돌·비대상
- `전체_URL_판정_진행상태.md`: 항목별 개수와 확정하지 못한 URL의 이유
- `전체_URL_판정_진행상태_상세.json`: 항목별 판단 이유와 원본 HTML·화면·검사 링크 근거

ID18·19·20·23은 저장된 화면·HTML에 대한 AI의 1차 검토다. ID21은 선정한 제품군 탐색 링크의 도착 페이지를 검사했다. ID22는 각 페이지에서 선정한 동일 브랜드 상품 카드 최대 2개의 도착 페이지를 확인한 것이므로 페이지의 모든 상품 카드 링크를 전수 검사했다는 뜻은 아니다. 기존 Concentrix 판정과 동일한 공식 결과로 보아서는 안 된다.

2026-09-28 재검토에서는 LG 브랜드 카테고리 페이지 24개를 `scripts/review_lg_population.py`로 다시 검토하고, `scripts/check_lg_navigators.py`로 제품군 탐색 링크의 도착 페이지 48개를 확인했다. 검토 기록은 `본문_항목_AI검수.json`과 `ID8_전체검수.json`, 이동 검사 기록은 `navigator-sidebar-check/` 및 `product-link-check/`에 보관한다. 그 결과 159개 URL 판정표에서 `REVIEW`는 6개 항목이다. URL 목록의 38행은 빈 제목·본문 주제 문구를 돌려준 Datart 제품군 링크, 43·44행은 Datart 일반 브랜드 페이지의 미표시 이미지, 149·150행은 영상 배너 인정 기준이 미정인 Bosch 페이지, 152행은 상품 목록 수집이 실패한 Electrolux 페이지다. 접속 상태가 200이어도 제목과 본문 주제 문구가 비어 있으면 이동 성공으로 판정하지 않는다.
