# 내장 브라우저 보조 도구

## 이게 뭔가

PDP 모수 자동화(S0~S6)는 상품 페이지를 Zyte(유료 수집 서비스)로 받아 판정한다. 그런데 몇몇 리테일러는 Zyte로는 상품 화면을 받을 수 없거나, 받아도 판매자가 화면에만 그려지고 HTML에는 없다. 이 폴더는 그런 곳을 **사람이 지켜보는 내장 브라우저(Claude 데스크톱 앱의 브라우저 창)** 로 열어 필요한 값만 뽑고, 그 값을 S3, S4의 수동 보완표로 바꾸는 도구다.

- 자동 실행 단계가 아니다. `run.py`가 부르지 않는다. Zyte 결과에 "수동 확인 필요"나 "확인불가"가 많이 남을 때만 쓴다.
- Zyte를 부르지 않으므로 돈이 들지 않는다. 대신 사이트가 막는 속도를 넘지 않게 천천히 연다.
- **로봇 확인(reCAPTCHA 등)은 도구가 풀지 않는다.** 뜨면 멈추고, 사람이 브라우저 창에서 직접 눌러 통과시킨 뒤 이어 간다.
- 2026-11 회차에서 처음 썼다. 결정 기록 D164(S3 Magalu), D165(S4 Lazada, Darty)에 쓴 과정과 결과가 있다.

## 언제 쓰나 (2026-11 기준)

| 리테일러 | 단계 | Zyte로 안 되는 이유 | 도구 |
| --- | --- | --- | --- |
| Magalu 브라질 | S3 페이지 확인 | 나라 지정, 거주지 IP를 써도 차단 화면이나 빈 화면(217바이트) | `magalu_pages.js` → `to_pages_manual.py` |
| Lazada 싱가포르, 태국 | S4 판매자 | HTML에 판매자 번호만 있고 이름은 화면을 그려야 나옴. 번호→이름 연결은 쓰지 않음(K2) | `lazada_sellers.js` → `to_sellers_manual.py` |
| Darty 프랑스 | S4 판매자 확인 | 판매자 칸이 없는 페이지가 정말 판매 불가인지 볼 때. 한국에서는 403이라 프랑스 VPN 필요 | `darty_check.js`(결과는 눈으로 확인) |

Costco 캐나다, Elgiganten 스웨덴은 이 도구가 아니라 Zyte HTML을 나라 지정 없이 다시 받으면 된다(D166).

## 파일

| 파일 | 하는 일 |
| --- | --- |
| `receiver.py` | 로컬 수신기(127.0.0.1 전용). 주소 목록을 사이트 주소 `#` 뒤에 붙여 넘겨 주고(`/go`), 브라우저가 form으로 보낸 결과를 JSON으로 저장한다(`/submit`). 리테일러 사이트의 보안 설정 때문에 브라우저에서 수신기로 바로 fetch를 보낼 수 없어서 이렇게 주고받는다. 이미 받은 항목은 다음 `/go`에서 뺀다. |
| `magalu_pages.js` | Magalu 탭에서 실행. 상품 페이지를 같은 사이트 안에서 받아 상품명, 판매자 문구(`Vendido por …`), `Produto indisponível`(판매 불가)만 뽑는다. 403, 429, 보호 화면이 나오면 1분 쉬고 동시 수를 절반으로 줄인다. |
| `lazada_sellers.js` | Lazada 탭에서 실행. 상품 페이지를 보이지 않는 창(iframe)으로 띄워 판매자 칸과 상점 주소를 읽는다. 로봇 확인이 뜨면 멈춘다. |
| `darty_check.js` | Darty 탭에서 실행. 상품 화면의 판매자 문구와 `PRODUIT INDISPONIBLE`(판매 불가), `PRODUIT ÉPUISÉ`(품절)를 읽는다. |
| `to_pages_manual.py` | Magalu 결과를 `runs/<월>/judgments/pages_manual.csv`와 작은 HTML로 바꾸고, Zyte를 부르지 않고 S3 결과 파일을 다시 만든다. |
| `to_sellers_manual.py` | Lazada 결과를 `runs/<월>/judgments/sellers_manual.csv`로 바꾼다. 판매자구분은 지난 회차에 사람이 판정한 같은 이름의 구분을 쓰고, 처음 보는 이름은 외부판매자 + "확인 필요"로 둔다. |

## 쓰는 순서

1. 작업 폴더(예: 임시 폴더)를 정하고 대상 목록을 `list_<이름>.json`으로 만든다.
   - Magalu: `pages.jsonl`에서 MAGAZINELUIZA이고 상태가 차단화면, 수집실패인 주소의 `https://magazineluiza.com.br/` 뒤 경로
   - Lazada: `sellers.csv`에서 LAZADA이고 확인불가인 주소의 페이지 id(`-i숫자`)를 나라별로 중복 없이
2. 수신기를 켠다: `python3 tools/browser/receiver.py <작업 폴더>`
3. 내장 브라우저에서 `http://127.0.0.1:8765/go?name=<이름>&to=<사이트 첫 화면>`을 연다. 예: `to=https://www.lazada.co.th/`
   - 사이트 첫 화면으로 넘어가면서 목록이 주소 `#` 뒤에 붙는다.
   - Lazada는 처음부터 로봇 확인이 뜰 수 있다. 사람이 먼저 상품 페이지 하나를 열어 통과시킨다.
4. 그 탭에서 해당 `.js` 파일 내용을 실행한다. 진행은 `window.__mg`, `window.__lz`, `window.__dt`로 본다.
5. 로봇 확인으로 멈추면(Lazada `window.__lz.punish`), 다른 탭에서 남은 첫 상품 주소를 열고 사람이 확인을 누른 뒤 `lzResume()`.
6. 끝나면 `mgSubmit('<이름>')` 또는 `lzSubmit('<이름>')`으로 결과를 수신기에 보낸다(탭이 수신기 화면으로 넘어간다).
7. 변환:
   - `python3 tools/browser/to_pages_manual.py --month <월> --results <작업 폴더>/<이름>.json`
   - `python3 tools/browser/to_sellers_manual.py --month <월> --results <…>/lazada_th.json <…>/lazada_sg.json --previous <지난 sellers_manual.csv> --date <MM-DD>` 뒤 `run.py s4 --month <월> --force`
8. 수신기를 끈다. 결정 기록에 무엇을 몇 건 했는지 적는다.

## 속도 기준 (2026-11 실제 값)

| 리테일러 | 동시 수 | 간격 | 막힌 기준 |
| --- | --- | --- | --- |
| Magalu | 최대 5 | 0.9~1.8초 | 6~7개에서 429, 403 → 1분 쉬고 절반 |
| Lazada | 2 | 3.5~6.5초 | 60~70페이지마다 로봇 확인 |
| Darty | 1 | 2.5~4.5초 | 프랑스 VPN에서 막힘 없음 |

## 주의

- 두 사이트를 동시에 돌릴 때 뒤에 있는 탭은 브라우저가 느리게 돌릴 수 있다.
- form 제출은 화면 이동이라 그 탭의 진행 상태(`window.__…`)가 사라진다. 결과를 보내기 전에 끝났는지 확인한다.
- 사이트 화면 구조가 바뀌면 선택자(예: `.seller-name-v2__detail-name`)를 고쳐야 한다. 11월에도 MediaExpert, Boulanger는 화면 구조가 바뀌어 S4 규칙을 고쳤다(D165).
- `to_pages_manual.py`, `to_sellers_manual.py`는 수동 보완표를 새로 쓴다. 다른 리테일러 수동 행이 있으면 먼저 합쳐 둔다. 11월 Otto 1건처럼 한두 건은 표에 직접 행을 더한다.
