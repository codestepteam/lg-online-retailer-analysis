# 리테일러별 Zyte 로드 스크립트

핵심 산출물은 `recipes/<리테일러>/<페이지 유형>.json`의 `request.actions`다. 브라우저에서 확인한 동작은 `configs-*.json`에 기록하고 `build_recipes.py`로 실행 요청을 만든다. 각 액션은 Zyte API의 `evaluate`로 실행된다. 공통 로더만 복사하는 방식이 아니라 각 페이지의 완료 조건·쿠키 선택자·펼치기·팝업 보존 설정을 함께 포함한다.

## 실행

프로젝트 루트의 `.env` 또는 환경 변수에 `ZYTE_API_KEY`를 설정한다. 키는 요청·응답 기록에 저장하지 않는다.

```sh
python3 capture/build_recipes.py
python3 scripts/zyte_capture.py --retailer boulanger --page-type pdp --dry-run
python3 scripts/zyte_capture.py --retailer boulanger --page-type pdp --assets --asset-cache-dir output/offline/_cache
python3 scripts/zyte_capture.py --retailer boulanger --all
python3 scripts/zyte_capture.py --all
python3 scripts/zyte_capture.py --all --assets-only --asset-cache-dir output/offline/_cache
```

`--dry-run`은 API를 호출하지 않고 검토용 요청을 `output/offline/<리테일러>/<유형>/request.preview.json`에 저장한다. 실제 수집의 `request.json`을 덮어쓰지 않는다. `--assets-only`는 저장된 HTML의 자산만 다시 처리한다. `--force`는 기존 수집 결과가 있어도 새로 수집한다.

Amazon은 홈에서 쿠키를 처리한 뒤 `goto`로 대상 페이지에 이동하고 쿠키 상태를 다시 확인한다. 홈은 실제 로고 링크 `/ref=nav_logo`를 사용한다. 원래 대상은 요청 파일의 `target_url`, 실제 API 시작 주소는 `request.url`이다.

## 파일 역할

- `configs-*.json`: 브라우저 확인에 근거한 리테일러별·유형별 로딩 설정과 확인 한계.
- `recipes/`: 생성된 70개 유형별 API 요청. `request`를 API 본문으로 사용한다.
- `cookies.js`: 늦게 나타나는 쿠키 창과 Shadow DOM 내부 동의 버튼을 기다린다. 동의에 따른 페이지 새로고침이 끝난 뒤 본문 액션을 실행한다.
- `load.js`: 완료 조건 대기 → 안전한 펼치기 → 단계적 스크롤 → 상세 패널 보존 → 이미지 로딩 확인. 설정의 `steps`와 `after_scroll`은 순서가 있다.
- `prepare.js`: 열린 Shadow DOM과 동적으로 삽입된 스타일을 HTML에 보존한다. 생성된 요청의 마지막 액션에 포함된다. 실행기는 이 액션이 없는 이전 요청에도 이를 보충한다.
- `../output/offline-review/observations-*.json`: 실제 브라우저 관측. 관측하지 못한 동작은 확인 완료로 취급하지 않는다.
- `../output/offline/<리테일러>/<유형>/`: `request.json`, `response.json`, `raw.html`, `screenshot.jpg`, `view/index.html`, `view/assets/`, `view/manifest.json`.

## 완료 판정과 한계

HTTP 200만으로 성공을 판정하지 않는다. API 액션 상태, 요청 페이지에서 홈으로의 잘못된 이동, 차단 문구, 필수 영역, 로더 완료 기록을 확인한다. 실제 클릭과 패널 보존 결과는 HTML의 `#lg-capture-state` JSON에 있다.

무한 목록의 모든 페이지를 수집하는 작업이 아니다. 페이지별 `scroll_steps`로 스크롤 상한을 정하며 `scroll.reachedBottom`으로 도달 여부를 기록한다. 수집 중 교체되는 PDP 팝업은 각각 보존한 뒤 `Captured expanded information` 영역에 표시한다. 자산 실패와 제한은 `view/manifest.json`에 기록한다.

오프라인 사본은 이미 로드한 화면을 보존한 정적 HTML이다. 원격 스크립트는 비활성화하여 재접속·재렌더링·CAPTCHA 재표시를 막는다. 구매·로그인·검색 서버 요청·실시간 재고 갱신은 정적 사본의 기능이 아니다. CAPTCHA 화면을 지워 정상 수집처럼 표시하지 않는다.

원본 목록의 ECI 두 유형은 같은 URL이었으나 품질 점검 후 브랜드 카테고리를 실제 LG 냉장고 목록으로 수정했다. Media Expert 브랜드도 냉장고 목록에서 여러 제품군을 포함한 `/lg`로 수정하고 재수집했다. 원본 목록은 출처 기록으로 유지하며 재실행 주소는 현재 레시피를 따른다. MediaMarkt 네덜란드 PLP는 실제 `Alle koelkasten` 상품 목록을 사용한다.

## 내용 품질 점검

`../output/quality-audit/report.md`에 70개 저장 HTML·Zyte 수집 화면·Zyte 로드 스크립트의 점검 결과와 수정 후 상태를 구분해 기록한다. API 검사 통과는 내용의 완전성이나 시각적 일치의 보증이 아니다.

`required_visible`은 Shadow DOM을 포함해 실제 보이는 영역을 검사하고, `panels[].min_chars`는 제목·로딩 문구만 저장되는 것을 방지한다. `min_viewport_width`는 요청과 달리 좁은 모바일 화면으로 실행되는 Darty 수집을 거절한다. 원본 화면에 숨겨진 내부 버튼을 억지로 표시하거나 클릭하지 않는다.

Zyte 액션의 전체 실행 시간은 60초, `evaluate.source`는 액션당 6,000자 제한이 있으므로 설정과 실행·보존을 나눴다. [Zyte 공식 액션 문서](https://docs.zyte.com/zyte-api/usage/browser.html), [API 명세](https://docs.zyte.com/zyte-api/usage/reference.html).

## 오프라인 파일 검사

```sh
python3 scripts/verify_offline.py output/offline/boulanger/pdp/view
python3 tests/test_recipes.py
python3 tests/test_offline_assets.py
python3 tests/test_verify_offline.py
```

직접 다운로드가 차단되거나 잘못된 HTML을 반환한 이미지·CSS·글꼴은 Zyte HTTP 요청으로 다시 받는다. `zyte_capture.py --assets`와 `--assets-only`는 기존 키를 메모리로 전달한다. 자산 저장 도구를 직접 실행할 때는 `--zyte-fallback`을 사용하며 키를 명령행 인자로 넣지 않는다.

이 환경에서 `file://` HTML을 브라우저 도구로 여는 작업은 보안 정책으로 차단되었다. 로컬 사본은 자산 파일·경로·해시와 외부 요청 여부를 검사했으며, 더블클릭 화면의 자동 시각 검증은 수행하지 못했다. Zyte 원격 화면과 내려받은 이미지 파일의 시각 검증은 별도로 수행했다.

`#lg-capture-state`의 `required[].present`는 해당 조건의 통과 여부다. `expected: hidden`인 항목에서는 대상이 보이지 않아야 `true`다.

수집 중 스크립트를 개선했으므로 현재 레시피와 이전 수집 당시 요청은 다를 수 있다. 반복 실행에는 `capture/recipes/`를 사용한다. 초기 dry-run이 요청 파일을 덮어쓴 기록은 `results.json`의 `request_payload_matches_capture`로 구분하며, 실제 응답에 기록된 요청 해시는 변경하지 않는다.

Datart 브랜드 페이지의 CSS·글꼴·이미지 9개는 별도 HTTP/Zyte 자산 요청으로 정상 파일을 받지 못해, 실제 Chrome 페이지가 받은 파일을 `pageAssets`로 저장하여 캐시에 보완했다. 출처는 `output/offline-review/browser-assets/datart/provenance.json`에 있다. 이 캐시도 함께 보관하면 같은 자산을 다시 네트워크로 받을 필요가 없다.

최종 현황은 `output/offline/results.json`과 `output/offline-review/final-offline-audit.json`을 따른다. 다른 `offline-review` 문서는 수집 과정의 시점별 관측·검토 기록이다.
