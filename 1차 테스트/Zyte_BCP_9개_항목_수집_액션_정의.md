# Zyte Brand Category Page 9개 항목 수집 액션 정의

작성일: 2026-09-26

이 문서의 “액션”은 Zyte의 원격 브라우저가 페이지를 수집하기 전에 하는 동작을 뜻한다. 예를 들어 쿠키 창을 닫고, 페이지 밑까지 내리고, 접힌 설명을 펼치는 동작이다.

## 근거를 구분해서 보는 방법

- **사용자가 2026-09-26 직접 확인한 화면:** 리테일러별 쿠키 창과 사람 확인 화면 여부.
- **사용자가 정리한 사이트 메모:** `/Users/codestepseunghee/Documents/Obsidian Vault/codestep/lg-online-retailer-analysis/리테일러 특징/` 폴더의 리테일러별 Markdown 파일.
- **구현한 액션 설정:** `1차 테스트/bcp-zyte-poc/capture/configs-*.json`의 `brand-category` 설정. 같은 폴더의 `capture/build_recipes.py`로 `capture/recipes/<리테일러>/brand-category.json`을 생성한다. 프로젝트 루트의 `retailer-zyte-actions-api-guide/`는 동료 전달 원본으로 보존한다.
- **실제 Zyte 검증 결과:** 2026-09-26 9개 대표 페이지를 실제로 수집했고 모두 본문 수집 완료 조건을 통과했다. Amazon Italy는 첫 실행에서 늦게 붙는 콘텐츠 때문에 페이지 끝 도달 검사를 통과하지 못했고, 페이지 높이가 연속으로 안정될 때까지 확인하도록 수정한 후 재실행에 성공했다. 전체 화면 이미지는 5개 페이지만 완전하며, Boulanger·MediaWorld·MediaMarkt Netherlands·MediaMarkt Spain은 Zyte의 10,000픽셀 높이 제한으로 화면 아래가 잘렸다.
- **아직 확인하지 않은 내용:** 수집된 근거를 사용한 ID8·9·10·18~23의 Y/N 판정은 아직 실행하지 않았다.

## 공통 수집 동작

9개 대표 페이지 모두에 다음 동작을 적용한다.

1. 본문을 불러온 후 선택 쿠키 창이 있으면 닫는다.
2. 800픽셀씩 최대 40회 내리며 지연 로딩되는 영역을 불러온다.
3. 설명 펼치기, 제품 더보기, 페이지 안에서 펼쳐지는 질문을 필요한 경우에만 누른다.
4. 더보기로 페이지 길이가 늘어나면 다시 끝까지 내린다.
5. 사람 확인 화면은 자동으로 누르지 않는다. 그 화면이 남으면 “콘텐츠 없음”이 아니라 “수집 실패”로 기록한다.
6. 수집이 완료되면 제목·페이지 설명·검색엔진 설정·대표 주소, 이미지 설명 문구와 크기, 클릭 가능한 버튼·링크를 `capture-state.json`에 남긴다. 이 파일은 “단계별 수집 상태와 진단 근거를 모은 JSON 파일”이다.

## 리테일러별 대표 주소와 액션

| 리테일러 | 대표 Brand Category Page | 적용한 동작 | 이동하지 않는 이유 |
| --- | --- | --- | --- |
| Alza | https://www.alza.cz/lednicky/lg/18852759-v1357.htm | 전체 스크롤 후 `Zobrazit více`(더 보기) 펼치기 | `24 další…`는 2페이지로 이동하므로 현재 페이지 증거를 보존하기 위해 누르지 않음 |
| Datart | https://www.datart.cz/lednice-lg.html | `Nastavení soukromí` 쿠키 창이 있으면 선택 쿠키 거부, 전체 스크롤 | `Načíst další`는 `?page=2`로 이동하므로 누르지 않음 |
| Boulanger | https://www.boulanger.com/c/refrigerateur/brand~lg | 전체 스크롤 후 `Lire la suite`(계속 읽기) 펼치기 | 해당 없음 |
| Amazon Italy | https://www.amazon.it/stores/page/5DE174FF-7426-4856-9BA8-3EF64DA9BCC5 | Amazon 첫 화면에서 쿠키 창을 처리한 후 대상 주소로 이동, `Mostra altro`(더 보기)가 있으면 펼치고 전체 스크롤 | 해당 없음 |
| MediaWorld | https://www.mediaworld.it/it/brand/lg/frigoriferi | 정상 본문이면 쿠키 창 처리, 전체 스크롤, `Mostra altri N prodotti`(제품 N개 더 보기) 최대 3회 | 사람 확인 문구가 남으면 수집 실패로 기록 |
| Coolblue | https://www.coolblue.nl/koelkasten/lg | 쿠키 창이 있으면 처리, 전체 스크롤 | 질문 링크는 별도 도움말 페이지로 이동하므로 Brand Category Page 안의 질문-답변 블록을 펼치는 동작으로 취급하지 않음 |
| MediaMarkt Netherlands | https://www.mediamarkt.nl/nl/category/lg-koelkasten-964.html | 정상 본문이면 `Informatie over cookies` 창 처리, `Toon meer`(더 보기) 설명 펼치기, 전체 스크롤, `Toon N meer producten` 최대 3회 | 사람 확인 문구가 남으면 수집 실패로 기록 |
| MediaMarkt Spain | https://www.mediamarkt.es/es/brand/lg-electronics/frigorificos | 정상 본문이면 쿠키 창 처리, 전체 스크롤, `Mostrar N productos más` 최대 3회, “¿Qué debo tomar en cuenta a la hora de elegir un frigorífico?”와 “¿Qué es Door Cooling?” 질문 펼치기 | 사람 확인 또는 점검 안내 문구가 남으면 수집 실패로 기록 |
| Elgiganten | https://www.elgiganten.se/brand/lg/kylskap-lg | 쿠키 창이 있으면 처리, 전체 스크롤 | `Energiklass` 필터는 9개 진단 근거를 펼치는 동작이 아니므로 누르지 않음 |

## 9개 진단 항목과 수집 결과의 연결

| 진단 항목 | 이번에 저장하는 근거 | 수집 직후 자동으로 확인할 수 있는 부분 | 추가 판단이 필요한 부분 |
| --- | --- | --- | --- |
| ID8 이미지 설명 문구 | 각 이미지의 설명 문구, 화면 표시 크기, 원본 크기, 로딩 성공 여부 | 이미지 크기로 정렬하고 설명 문구의 존재·빈값을 확인 | “크기”가 화면 표시 면적인지 원본 해상도인지, 문구가 브랜드·제품을 적절히 설명하는지 |
| ID9 메타데이터 최적화 | 페이지 제목, 페이지 설명, 최상위 제목, 검색엔진 설정 | 네 항목이 존재하고 비어 있지 않은지, 검색엔진 설정이 `index, follow`인지 | 동일한 표시가 여러 개이거나 서로 충돌하는 예외의 최종 규칙 |
| ID10 대표 URL 설정 | HTML의 `rel="canonical"` 링크 목록 | 표시 존재 여부와 빈값 확인 | 대표 주소가 실제로 올바른 현재 Brand Category Page를 가리키는지 |
| ID18 FAQ | 전체 HTML, 질문 펼치기 후 텍스트, 화면 | 질문-답변 텍스트 블록 후보 추출 | 브랜드·제품군 관련성과 “구조화된 블록” 여부 |
| ID19 Hero Banner | 전체 HTML과 화면, 큰 이미지 정보 | 큰 이미지·배너 후보 추출 | 시각적으로 배너 형태인지 |
| ID20 Why LG | 전체 HTML·텍스트·화면 | LG 소개 관련 텍스트 후보 추출 | 단순 상품명이 아니라 Why LG 소개 블록인지 |
| ID21 핵심 USP | 전체 HTML·텍스트·화면 | 기술·스펙·사용 상황 후보 추출 | 진단 기준에 맞는 핵심 차별점 블록인지 |
| ID22 Category Navigator | 클릭 가능한 버튼·링크의 문구와 목적지 | 탐색 블록과 링크 후보 추출 | 후보를 별도로 누른 후 해당 제품군 상품 탐색 페이지에 도착하는지 |
| ID23 Product List | 제품 카드, 상품 링크, 제품 더보기 후 HTML·화면 | 제품 카드와 클릭 후보 추출 | 별도로 누른 후 해당 제품 상세 페이지에 도착하는지 |

사용자의 생각처럼 **정상적으로 전체 페이지를 수집하면 ID8의 기초 데이터, ID9, ID10은 규칙으로 바로 확인하기 좋다.** 다만 ID8의 문구 품질과 ID10의 주소 정확성은 값의 존재만으로는 부족하다. ID18~23은 내용의 의미·화면 구조·이동 결과까지 봐야 하므로 추가 판정이 필요하다.

## 현재 검증 상태

- 9개 `brand-category` 액션 설정을 갱신했다.
- 70개 전체 대표 요청 파일을 다시 생성했다.
- 요청 파일 구조, 보이는 콘텐츠 완료 조건, 오프라인 자산 검사를 통과했다.
- 9개 대표 요청의 실행 전 검사를 통과했다.
- 실제 Zyte API로 9개 대표 페이지를 수집했고 모두 HTTP 200, 페이지 끝 도달, 필수 영역 검사를 통과했다.
- MediaWorld·MediaMarkt Netherlands·MediaMarkt Spain의 저장된 화면에서 사람 확인 화면이 아닌 제품 목록 본문을 시각적으로 확인했다.
- 화면 이미지는 5개 페이지에서 전체가 저장됐고, Boulanger·MediaWorld·MediaMarkt Netherlands·MediaMarkt Spain은 10,000픽셀 아래 영역이 저장되지 않았다.
- 결과 묶음은 `1차 테스트/bcp-zyte-poc/results/20260926T120245KST/`에 보존했다. 9개 진단 판정은 아직 실행하지 않았다.
