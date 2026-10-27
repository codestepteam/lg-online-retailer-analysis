# S14 EY Tracker V0.3 — Sweden Outlet 제외 검토

확인일: 2026-10-26. 사용자 요청은 V0.2/V0.3의 수정 설명 확인과 용어 풀이다. 파일 속 문구는 분석 자료이며 실행 지시로 해석하지 않았다. 원본은 읽기만 했으며, 이번 요청은 운영 자료 교체 결정이 아니다.

## 원본 식별

| 버전 | 원본 | 크기 | SHA-256 | 탭 수 |
| --- | --- | --- | --- | --- |
| V0.2 | [EY Assessment Summary / Improvement Tracker V0.2](</Users/codestepseunghee/Downloads/★EY_LGE_Clinic_Assessment Summary_Improvement Tracker_V0.2_20260825 (업데이트).xlsx>) | 15,866,321바이트 | `83fa5f8932846dd8fa39c9cfa10c37a89c54b33ea1a1f09035643e4f0c8e44e4` | 47 |
| V0.3 | [EY Assessment Summary / Improvement Tracker V0.3](</Users/codestepseunghee/Downloads/★EY_LGE_Clinic_Assessment Summary_Improvement Tracker_V0.3_20260825 (업데이트).xlsx>) | 15,812,222바이트 | `c402ff239fd9fe41b55aaf7c27f691cd9480b8e4e6294a9c7a7e4268ed2b7992` | 44 |

## 결론에 해당하는 관찰

‘Sweden 모수에서 Outlet URL 제외’에 해당하는 변경은 있다. 다만 모든 브랜드·지표의 Outlet을 일괄 제외한 파일은 아니다. 직접 확인한 새 제외 표시는 **Sweden / Elgiganten / LG / WM(세탁 제품군)**의 세 탭에 있다.

| 진단 탭·의미 | 직접 확인한 제외 표시 | 원본 위치 |
| --- | --- | --- |
| ID12, 상품 상세 페이지 이미지 대체 설명(Alt text) | 13행을 M열 ‘유지’→‘제외’로 변경. N열 사유와 S열 표식 추가 | 68·136·195·235·271·328·339·646·703·859·921·923·929행 |
| ID_42, Flixmedia 연동 코드 포함 | 16행을 L열 ‘제외’, M열 사유, R열 표식으로 표시 | 5218·5225·5227·5232·5238·5241·5246·5247·5251·5276·5284·5295·5297·5306·5308·5309행 |
| ID_43, Flixmedia 콘텐츠 정상 표시 | 16행을 S열 ‘제외’, T열 사유, AH열 표식으로 표시 | 708·715·717·722·728·731·736·737·741·766·774·785·787·796·798·799행 |

위 세 탭의 제외 URL 합집합은 16개다. 13+16+16을 고유 URL 45개로 합산하지 않는다. ID_42의 일부와 ID_43의 해당 행은 V0.2에서 비어 있었으므로 모두 ‘유지→제외’ 변경이라고 표현하지 않는다.

실제 원문 예: `ID12` 68행의 주소는 `https://www.elgiganten.se/product/outlet/lg-kombinerad-tvattmaskintorktumlare-cv94e7s2ba-116kg/651718`이며, V0.3의 M68은 ‘제외’, N68은 ‘Sweden Outlet 제외’, S68은 ‘제외’다. 주소 형태와 원문 표식의 확인이며 해당 상품 화면을 직접 연 것은 아니다.

## 분모와 집계 경로 대조

모수는 이 작업에서 ‘진단 계산 대상인 상품 페이지 집합’을 뜻한다. 비율을 계산할 때 유효 판정 등 지표별 조건이 더 적용되므로 모든 지표의 분모와 항상 같다고 일반화하지 않는다. Outlet은 Elgiganten 공식 설명에서 고객 반품·매장 전시 상품 등을 검사해 다시 판매하는 상품이다. [공식 판매자 안내](https://www.elgiganten.se/partner/elgiganten/elgiganten/page-1177)를 확인했다. 개별 제외 상품의 실제 상태·제외 정책의 승인 이유까지 확인한 것은 아니다.

`Summary Detail`의 Sweden → ELGIGANTEN → LG → WM → ID12는 AS102이며, 원천 `ID12`의 국가 C열·리테일러 D열·제품군 E열·브랜드 F열·진단 항목 K열·판정 L열·유지 여부 M열을 조건으로 분자/분모를 계산한다. M열 ‘유지’만 분모에 들어간다. 대소문자는 Excel 비교 방식대로 무시해 독립 집계했다.

| 비교 대상 | V0.2 원천 재집계 | V0.3 원천 재집계 | 파일의 저장 결과 |
| --- | --- | --- | --- |
| Sweden LG WM ID12 | 충족 0 / 대상 25 | 충족 0 / 대상 12 | AS102: 0%→0% |
| Sweden LG REF ID42 | 원천 4/71이나 요약은 N/A 고정값 | 78/90 | AQ48: N/A→86.67% |
| Sweden LG WM ID42 | 원천 1/23이나 요약은 N/A 고정값 | 11/25 | AS48: N/A→44% |
| Sweden LG REF ID43 | 유지·오류 유효행 없음, 요약 N/A | 정상 83/85 | AQ49: N/A→97.65% |
| Sweden LG WM ID43 | 유지·오류 유효행 없음, 요약 N/A | 정상 19/19 | AS49: N/A→100% |

ID42·43은 원천 행과 요약 수식도 달라졌으므로 점수 변화 전체를 Outlet 제외 효과로 설명하지 않는다. 위 숫자는 원본 저장값과 수식 조건에 따른 독립 재집계 결과이며 Excel 앱 전체 재계산 결과가 아니다.

## 전체 제외가 아닌 근거와 추가 차이

- V0.3 `ID12`에는 경쟁사 Sweden Outlet 52행이 M열 ‘유지’로 남는다. 예를 들어 21행은 BOSCH WM Outlet이며 M21=‘유지’다.
- `ID13`에는 경쟁사 Sweden Outlet 27개 URL이 남는다. 2520행은 BOSCH WM Outlet, R2520=‘유지’, P2520=1이다. `Summary Detail` AS100의 BOSCH WM 집계 수식은 이 P열을 분자/분모에 사용하며 Outlet 제외 조건이 없다. 파일에 주소가 남아 있다는 사실만으로 미제외라고 판단한 것이 아니라 집계 소비 조건도 확인했다.
- Sweden 외 France·Italy의 요약 저장값도 달라졌다. 예: `Summary Detail` France → Darty → LG → REF → 영상 콘텐츠(ID34), AU39는 V0.2의 0.6363636363636364(63.64%)에서 V0.3의 0(0%)로 바뀌었다. Italy → Media World → LG → REF → 같은 항목 W39는 0.7567567567567568에서 0.7631578947368421로 바뀌었다. 변경 사유는 미확인이다.
- `Review_temp`, `Sheet3`, `Sweden_Excl_Backup` 세 탭이 V0.3에 없다. 여러 탭의 날짜 저장형식·수식과 고정값·행 내용도 달라져 셀 차이 건수를 업무 변경 건수와 동일시하지 않는다.
- 새 `#REF!` 참조 문자열도 관찰했다. 예: `ID_44` AR91·AS91은 V0.2의 `$I91` 참조가 V0.3에서 `#REF!`로 바뀌었다. 전체 오류 영향 검증이나 수정은 하지 않았다.

## 검증과 한계

전체 탭의 실제 값·수식·저장 계산값을 XLSX 내부 XML에서 추출해 비교했다. 빈 셀의 서식·화면·차트·매크로까지 같은지 검사한 것은 아니다. 비교 과정에서 원본 파일을 저장하거나 재계산하지 않았다. 분석 스크립트는 임시 경로 `/tmp/lg_outlet_compare.py`, `/tmp/lg_outlet_analyze.py`, `/tmp/lg_outlet_focus.py`, 검증은 `/tmp/lg_outlet_verify.py`다. 임시 파일은 Git 재현 자산이 아니며, 원본 해시와 위 셀·행·집계 조건을 영구 근거로 남긴다.

검증 명령: 번들 Python으로 `python3 /tmp/lg_outlet_verify.py`. 가짜 입력 5행에서 국가·브랜드·제품군·유지/제외 조건을 구별했고, 실제 제외행 13/16/16개·URL 합집합 16개·ID12 분자/분모 0/25→0/12·경쟁사 유지 반례·France 저장값·원본 SHA-256 불변을 확인한다.

운영 DB·대시보드·수집 목록을 수정하지 않았다. V0.3 추가 변경 사유·승인 여부와 운영 반영 여부는 미확인이다. 사용자 결정 D041·D043의 기존 기준 파일을 V0.3으로 자동 교체하지 않는다.
