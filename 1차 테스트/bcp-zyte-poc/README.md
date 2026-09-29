# 리테일러별 Zyte 액션과 API 사용방법

14개 리테일러 × 5개 페이지 유형의 현재 Zyte 로드 스크립트 70개를 담았습니다.

## 먼저 볼 파일

- capture/recipes/<리테일러>/<유형>.json: 실제 API 요청은 각 파일의 request 필드입니다. 액션 목록은 request.actions입니다.
- capture/configs-*.json: 리테일러별 클릭, 대기, 스크롤, 완료 조건 설정입니다.
- capture/README.md: 상세 실행 방법과 확인 한계입니다.
- scripts/zyte_capture.py: API 호출 실행기입니다. 페이지는 순차 처리합니다.

## 실행 방법

Python 3.10 이상을 사용합니다. 실행기는 Python 표준 라이브러리를 사용합니다.
압축을 푼 폴더에서 다음 명령을 실행합니다.

1. 폴더 최상단에 .env 파일을 만들고 ZYTE_API_KEY=본인의_API_키 를 기록하거나 같은 이름의 환경 변수를 설정합니다. 이 ZIP에는 API 키가 없습니다.
2. API 호출 없이 요청을 확인합니다.

```sh
python3 scripts/zyte_capture.py --retailer boulanger --page-type pdp --dry-run
```

3. 한 페이지를 수집합니다. 이 단계부터 실제 API 사용량이 발생합니다.

```sh
python3 scripts/zyte_capture.py --retailer boulanger --page-type pdp
```

4. 이미지와 CSS까지 로컬에 저장하려면 다음 명령을 사용합니다. 자산 다운로드 실패 시 Zyte 추가 요청이 발생할 수 있습니다.

```sh
python3 scripts/zyte_capture.py --retailer boulanger --page-type pdp --assets --asset-cache-dir output/offline/_cache
```

전체 70개를 실행하려면 --all을 사용합니다.

```sh
python3 scripts/zyte_capture.py --all
```

결과는 output/offline/<리테일러>/<유형>/에 생성됩니다.
설정을 수정한 뒤 요청 JSON을 다시 만들 때만 python3 capture/build_recipes.py를 실행합니다.
재생성에 필요한 output/_poc_zyte/url-manifest.json도 포함했습니다.

## 다른 API 클라이언트에서 호출

POST https://api.zyte.com/v1/extract
인증: HTTP Basic 인증의 사용자 이름에 Zyte API 키, 비밀번호는 빈 문자열.
Content-Type: application/json
요청 본문: 레시피 JSON 전체가 아닌 request 필드의 JSON 객체.
응답 browserHtml이 렌더링된 HTML입니다. 요청의 actions가 로딩과 화면 조작을 수행합니다.

공식 명세: https://docs.zyte.com/zyte-api/usage/reference.html
공식 액션 문서: https://docs.zyte.com/zyte-api/usage/browser.html

## 포함 범위

실행 코드, 설정, 액션 JSON, 안내 문서와 검사 파일을 포함했습니다.
기존 수집 HTML, 이미지, 응답, 캐시, 브라우저 관측 자료와 API 키는 포함하지 않았습니다.
capture/README.md가 참조하는 기존 수집 보고서는 원본 프로젝트에 있습니다.
현재 레시피와 과거 수집 당시 요청이 다를 수 있으며, 모든 페이지의 완전한 로딩이나 오프라인 시각적 일치를 보증하지 않습니다.
