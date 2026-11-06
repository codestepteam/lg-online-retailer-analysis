# 두레이 158 · 사우디 eXtra 재고 전수 확인 (2026-11-05)

## 상품 화면 문구 직접 확인 결과 (11월 5일 추가 검증)

사용자 요청에 따라 Codex **내부 브라우저 5개 탭**에서 v3의 Saudi Arabia / EXTRA / **포함 272개 URL 전부**를 직접 열어 상품 화면의 `هذا المنتج حاليًا`와 `غير متوفر حاليًا`가 함께 보이는지 확인했다. [화면 확인 272건 CSV](eXtra_v3포함272_상품화면_품절문구_전수확인_20261105.csv)와 [두 문구가 확인된 포함→제외 대상 129건 CSV](eXtra_v3포함_화면품절문구129건_포함에서제외_변경대상_20261105.csv)를 다운로드 폴더에도 복사했다. 이 판정은 화면 접근성 텍스트에서 해당 상품의 실제 문구를 확인한 결과이며 OSM `AVLBL_STAT`나 HTML 내 상품 JSON 재고코드로 대체한 판정이 아니다.

| 현재 화면 분류 | URL 수 | 확인 내용 |
|---|---:|---|
| 상품 판매 영역에 두 아랍어 문구 표시 | **129** | 장바구니 추가 버튼 없음. 이번 제외 대상 CSV에 수록 |
| 두 문구 없음, 장바구니 추가 버튼 표시 | **137** | 이번 문구 기준 제외 대상 아님 |
| 상품 페이지 404 | **3** | v3 행 9214·9329·9401, 별도 확인 대상 |
| 배송 불가 문구만 표시 | **3** | v3 행 9361·9416·9428. `غير متوفر حاليًا`만 있으며 상품 품절을 뜻하는 앞 문구는 없음 |

272개 행번호와 URL의 유일성, v3 포함 행 전체와의 일치, 제외 대상 129행의 원본 26열 보존, 다운로드 복사본의 바이트 일치를 확인했다. 재고 화면은 **2026-11-05 현재 관찰**이며 10월 수집 당시 화면 상태로 소급하지 않는다. 아래의 상품 JSON 기반 129건 CSV는 이전 조사 산출물이고, **화면 문구에 따른 제외 대상을 검토할 때는 위의 새 CSV를 사용한다.**

## 조사 범위와 자료

- [두레이 158](https://codestep.dooray.com/task/4424097923196640208/4458444103756496724): EY는 10월 모수에 품절 상품이 들어 있다고 지적하고, 예시 상품 코드 `100337111`을 제시했다. 본문은 “총 114개”라고 적었으나, 현재 로컬 v3 CSV의 **LG 포함 판정은 112 URL**이다. 그 수치가 왜 다른지는 확인하지 못했다.
- v3 원본: `pdp 모수 추출/최종_20261029/PDP모수_공유용_v3_EY검토반영_25개국_35개리테일러_전체판정_55997행_20261031.csv`에서 Saudi Arabia / EXTRA / 포함 **272개 고유 URL**을 추출했다. 브랜드별 LG 112, SAMSUNG 64, TOSHIBA 46, HITACHI 32, MIDEA 18이다.
- OSM 원본: `pdp 모수 추출/OSM_추가9개리테일러_PDP후보_4942건_20261028.csv`의 `CRAWL_URL`로 272 URL 전부 정확히 연결했다. 수집일 `RPT_DATE`는 전부 **2026-10-26**이다.
- [전체 272 URL 결과](eXtra_v3포함272_OSM재고및현재PDP_전수조사_20261105_최종.csv), [LG 112 URL 결과](eXtra_LG_v3포함112_OSM재고및현재PDP_전수조사_20261105_최종.csv). 각 URL의 공개 PDP HTML 응답을 `html/`에 gzip으로 저장하고 CSV의 `HTML_SHA256`에 원문 해시를 적었다. 유료 Zyte 호출은 하지 않았다.
- 초기 상품 JSON 기준 129행 변경 대상 CSV(`eXtra_v3포함_현재품절129건_포함에서제외_변경대상_20261105.csv`)도 만들었으나 이번 커밋에서는 제외한다. 검토·전달 대상은 위의 **상품 화면 문구 직접 확인 129행 CSV**다. v3 원본은 수정하지 않았다.

## OSM 원본 재고와 11월 5일 현재 상품별 재고

| 10월 26일 OSM `AVLBL_STAT` | 현재 상품 JSON `outOfStock` | `inStock` | `lowStock` | HTTP 404 | 합계 |
|---|---:|---:|---:|---:|---:|
| `Out of stock` | 107 | 4 | 0 | 2 | **113** |
| `In stock` | 4 | 97 | 9 | 0 | **110** |
| `\N` (값 없음) | 18 | 27 | 3 | 1 | **49** |
| **합계** | **129** | **128** | **12** | **3** | **272** |

LG 112 URL만 보면 OSM은 `Out of stock` 66, `In stock` 45, `\N` 1이다. 현재 상품 JSON은 `outOfStock` 61, `inStock` 46, `lowStock` 4, HTTP 404 1이다. 10월 `Out of stock` 66개 중 61개는 현재도 품절, 4개는 현재 재고 있음, 1개는 현재 404다. 수집일과 현재 시점이 다르므로 현재 상태를 10월 당시 화면 상태로 소급하지 않는다.

모든 272 HTML에 아랍어 `غير متوفر حاليًا`가 나오지만, 이는 사이트 전역 `ACC.config.outOfStock` 설정에도 들어 있다. **HTML 전체 문자열 포함 여부만으로 상품 품절을 판정할 수 없다.** CSV의 현재 상태는 URL의 상품별 `var pdpDetails` 객체에서 `stock.stockLevelStatus.code`를 읽어 분류했다. `stockAvailableForHD`는 참고값이다. `isAddToCartEnabled`는 품절 상품에서도 `true`여서 구매 버튼 여부의 근거로 쓰지 않았다. 재고는 선택 도시와 시간에 따라 달라질 수 있다.

## 이전 단계의 내부 브라우저 화면 표본과 오류

아래 네 화면은 초기 조사 단계에서 확인한 표본이다. 이후 위 절의 **272개 URL을 내부 브라우저에서 전수 재확인**했다.

- [LG 100337111](https://www.extra.com/ar-sa/large-appliances-/refrigerators/large/lg-refrigerator-14-8cu-ft-freezer-6-1cu-ft-smart-inverter-white/p/100337111): 상품 판매 영역에 `هذا المنتج حاليًا`, `غير متوفر حاليًا`, 재입고 알림이 보였고 장바구니 버튼은 보이지 않았다. OSM과 현재 상품 JSON 모두 품절.
- [LG 100503745](https://www.extra.com/ar-sa/large-appliances-/built-in/refrigerator/lg-built-in-refrigerator-6cu-ft-bottom-freezer-2-2-cu-ft-multi-air-flow-white/p/100503745): `اضف إلى عربة التسوق`(장바구니 추가) 버튼이 보였다. OSM과 현재 상품 JSON 모두 재고 있음.
- [LG 100418426](https://www.extra.com/ar-sa/large-appliances-/refrigerators/side-by-side-refrigerator/lg-refrigerator-18cu-ft-freezer-9-3cu-ft-sidebyside-multi-door-inverter-linear-comp/p/100418426): 장바구니 버튼과 `1 متبقي فقط`(1개 남음)이 보였다. 현재 JSON은 `lowStock`.
- [LG 100345928](https://www.extra.com/ar-sa/large-appliances-/washing-machines/topload/lg-top-load-washing-machine-24kg-platinum-black/p/100345928): 화면에 `404 / لم يتم العثور على الصفحة`(페이지를 찾을 수 없음). HTTP 응답도 404다.

272개 중 최종 수집 오류·해석 미확인은 **0건**이다. HTTP 404는 수집 오류가 아닌 현재 상품 페이지 없음으로 별도 분류한 **3건**이다: v3 행 9214 HITACHI(`Out of stock`), 9329 TOSHIBA(`\N`), 9401 LG(`Out of stock`). 최초 요청이 시간 초과된 LG 2건(행 9282·9340)은 재시도에서 HTTP 200과 상품 JSON을 얻었으며 최종 CSV의 오류는 비어 있다.

변경 대상 CSV에는 HTTP 200 상품 HTML의 해당 상품 `pdpDetails.stock.stockLevelStatus.code=outOfStock`이 확인된 **129행**만 넣었다(LG 61, Samsung 31, Toshiba 18, Hitachi 12, Midea 7). 404인 3행은 품절과 구분해 이번 자동 제외 요청에서 보류했다. 129행의 10월 26일 OSM 재고값은 `Out of stock` 107, `In stock` 4, `\N` 18이다. 수집 시점 차이와 선택 지역에 따른 재고 변동 가능성은 남는다.

## v3에 품절 상품이 포함된 원인과 다음 규칙 제안

`판정근거/스크립트/step1_filter.py`의 `osm_rows`(124~134행)는 OSM `AVLBL_STAT`를 다음 단계로 전달하지 않는다. `page_check.py`(22~25행)는 HTTP 200 상품 페이지를 `정상`으로 두고 품절 문구는 410 응답일 때 일부 표현만 검사한다. 과거 `페이지확인/pages_best.jsonl`에서 eXtra 포함 272개 전부(그중 LG 112개)가 HTTP 200 / `정상`이다. `step2_page_seller.py`(63~75행)는 그 페이지 상태와 판매자만으로 제외한다. `seller_g4.py`의 `extra`(60~74행)는 상품별 `marketPlaceProduct`로 외부 판매자만 구분한다. 따라서 10월 OSM에서 이미 품절로 적힌 LG 66개가 판정 체인에서 재고 기준을 적용받지 않고 포함됐다.

**제안(사용자 확정 규칙 아님):** eXtra URL을 포함하기 전, 수집일과 동일한 주기의 OSM 재고값과 PDP의 해당 상품 `pdpDetails.stock.stockLevelStatus.code`를 보존해 비교한다. 상품별 `outOfStock` 또는 상품 판매 영역의 `غير متوفر حاليًا`는 품절로 제외하고, `lowStock`은 재고 있음으로 구분한다. `\N`은 품절로 간주하지 말고 상품별 상태를 다시 확인한다. HTML에 있는 전역 설정 문자열은 제외 근거로 사용하지 않는다. 응답 404·파싱 실패·정보 충돌은 별도 확인 대상으로 남긴다.

## 검증

`python3 outputs/extra-158-20261105/combine.py`로 272개 URL·v3 행번호 고유성과 원본 HTML 전부의 크기·SHA-256 일치, HTTP 200인 269개 상품 JSON 코드와 URL의 일치를 검증했다. 결과 CSV의 오류 칸은 전부 비어 있다. Downloads 복사본 `eXtra_v3포함272_OSM재고및현재PDP_전수조사_20261105_최종.csv`의 SHA-256은 원본과 같은 `2fda931cd2d12e25c1677dbdb1a566af7290a0d8f4154eb55f13e413f677b276`이다. LG 112개만 있는 최종 CSV도 Downloads 복사본과 SHA-256 `6bb8e96c1699ed710a09dfdfc222c8a7e0f2820c1222110106a34a34f2b47245`로 일치한다.

`python3 outputs/extra-158-20261105/prepare_change_input.py`로 변경 대상 129개 원문 HTML의 크기·SHA-256·상품별 재고코드가 전수조사 CSV와 일치함을 확인했다. `build_change_csv.mjs`가 원본 v3 행을 보존한 CSV를 만들었고, 생성 후 129개 행번호·원본 26열·재고코드·다운로드 복사본의 일치를 다시 검사했다.
