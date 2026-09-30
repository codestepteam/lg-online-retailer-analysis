# ID21 제품군 탐색 클릭 검사

이 시험은 `Brand_BCP_1차_테스트_URL_목록.xlsx`의 `URL 목록` 탭 38행, Datart LG 냉장고 페이지에 적용했다. 기준 원문은 『EY_LGE HS 온라인 리테일 클리닉 진단 항목_v1.95_20260915 (1)』의 「Clinic 진단 항목」 ID21이다. 제품군 탐색 블록에서 클릭 가능한 카드 또는 CTA(행동 유도 문구)를 확인하고, 실제 누른 뒤 해당 제품군의 상품 목록에 도착하는지 본다.

```bash
PYTHON=/Users/codestepseunghee/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
"$PYTHON" '1차 테스트/bcp-zyte-poc/scripts/check_id21_clicks.py' --live
"$PYTHON" '1차 테스트/bcp-zyte-poc/scripts/assess_full_population.py' '1차 테스트/bcp-zyte-poc/results_population/20260928-all-159'
```

프로젝트 루트의 `.env` 또는 환경 변수에 `ZYTE_API_KEY`, `TYPESAFE_API_KEY`가 필요하다. `--live` 없이 실행하면 요청안만 만들며 `navigator-click-dry-run/`에 저장한다. 한 카드만 시험하려면 `--card-index 7`처럼 번호를 준다. 코드가 확인한 카드 순서는 `id21-click-review.json`의 `results[].card.label`에 기록된다.

결과 폴더: `results_population/20260928-all-159/navigator-click-check/row-0038-datart/`.

| 파일 | 뜻 |
| --- | --- |
| `id21-click-review.json` | 원본 HTML 지문, 카드 개수, 카드별 클릭·도착·Jev 결과와 전체 상태 |
| `card-XX/zyte-request.json` | 원본 페이지에서 어느 카드를 누르도록 했는지 |
| `card-XX/landing.html` | Zyte가 클릭 뒤 저장한 실제 화면 HTML. 원본 `raw.html`과 다른 자료 |
| `card-XX/zyte-response-summary.json` | 클릭 액션, 최종 주소, 화면 제목, 상품 개수·예시, 수집 오류 |
| `card-XX/jev-request.json` · `jev-response.json` | 클릭과 상품 목록 수집이 모두 유효할 때 카드 뜻과 도착 제품군의 일치 여부를 Jev에 묻고 받은 답 |

`Y`는 평가 대상 카드 전부의 클릭·제품군 일치가 확인된 경우, `N`은 실제로 다른 제품군에 도착한 카드가 확인된 경우, `REVIEW`는 카드 일부를 검사하지 못했거나 클릭 후 화면을 제대로 받지 못한 경우다. 도착 화면의 H1 태그 유무만으로 결정하지 않는다. Jev의 의미 판정은 사람 정답표로 정확도를 검증한 결과가 아니므로 근거를 함께 검토한다. 이 코드는 현재 Datart 38행만 구현했다. 다른 리테일러에는 탐색 영역·상품 목록 식별 방식을 별도로 확장해야 한다.

2026-09-29 실행에서 11개 중 3개는 Zyte 클릭 후 상품 목록이 저장되고 Jev가 제품군 일치를 답했다. 나머지 8개 중 6개는 Zyte의 클릭 성공 기록에도 최종 화면이 원래 페이지 그대로였고, 2개는 카드 주소로 이동한 뒤 CAPTCHA(사람 확인용 그림 코드) 화면을 받았다. 전체 결과는 REVIEW다. 별도 앱 내 브라우저에서 `Kombinované` 카드가 실제로 해당 LG 냉장고 목록으로 이동함을 확인했으므로, Zyte의 원본 화면 잔류를 사이트 링크 실패로 해석하지 않는다.
