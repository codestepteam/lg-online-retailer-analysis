# outputs 폴더 목록

조사·검증을 한 번 할 때마다 결과 묶음 하나가 이 폴더 아래에 생긴다. 이 파일은 2026-11-15에 폴더 41개를 주제별로 정리한 찾아보기다. 폴더는 옮기거나 이름을 바꾸지 않았다(코드와 다른 문서가 지금 경로를 가리킨다).

- **‘설명 근거’ 열 읽는 법.** `안내 문서`는 그 폴더의 README를 읽고 적었다. `요약 파일`은 폴더 안 요약 JSON·스크립트 첫머리를 보고 적었다. `파일 이름`은 파일 이름만 보고 적은 것이라 정확한 경위는 확인이 필요하다.
- **결정 번호**는 [결정 기록](../docs/DECISIONS.md)에서 이 폴더를 직접 가리키는 항목만 적었다. 빈칸은 결정 기록에 이 폴더 이름이 없다는 뜻이지 관련 결정이 없다는 뜻이 아니다.
- 날짜는 폴더 이름에 붙은 날짜다. 새 결과 폴더를 만들면 이 표에 한 줄을 더한다.

## PDP 모수 공유본을 만들고 대조한 기록

PDP 모수는 진단할 상품 상세 페이지 주소 목록이다. 공유본 파일 자체는 [`pdp 모수 추출/최종_20261029/`](../pdp%20모수%20추출/최종_20261029/READ.md)에 있고, 여기에는 만들 때 쓴 스크립트와 검증 근거가 있다.

| 폴더 | 날짜 | 내용 | 결정 | 설명 근거 |
| --- | --- | --- | --- | --- |
| [pdp-version-comparison-20261030-a5cabba9](pdp-version-comparison-20261030-a5cabba9/) | 10-30 | 전체판정 v1(56,071행)과 v2(55,997행)의 행·열·판정 분포 대조. `verify.py`는 자동화 계획에서 다시 쓰는 검증 본보기 | | 요약 파일 |
| [pdp-share-wording-20261030-ae7bd3ac](pdp-share-wording-20261030-ae7bd3ac/) | 10-30 | 공유용 첫 파일(55,997행) 사본 1개 | | 파일 이름 |
| [pdp-share-v2-brand-code-20261030-7c41e2d9](pdp-share-v2-brand-code-20261030-7c41e2d9/) | 10-30 | 공유용 파일에 브랜드·제품코드 열을 넣는 스크립트와 검증 값 | | 요약 파일 |
| [pdp-share-v2-20261030-94e9c3b7](pdp-share-v2-20261030-94e9c3b7/) | 10-30 | 공유용 v2 생성 스크립트·입력·검증, 행별 `브랜드_제품코드_근거.csv` | | 다른 문서의 언급 |
| [pdp-stock-status-evidence-20261030-b3100b69](pdp-stock-status-evidence-20261030-b3100b69/) | 10-30 | EY가 제외를 요청한 11개 URL의 저장 페이지 근거 | D085 | 결정 기록 |
| [pdp-share-v3-ey-review-20261031](pdp-share-v3-ey-review-20261031/) | 10-31 | 공유용 v2에 EY 검토와 사용자 결정을 반영해 v3를 만든 스크립트 `make_v3.py` | D086·D087(스크립트 주석) | 요약 파일 |
| [riribu-keyword-effect-20261103-d0bfd680](riribu-keyword-effect-20261103-d0bfd680/) | 11-03 | 리리부 키워드(판정 순서의 ‘③리리부’ 제외 단계)로 빠지는 URL을 국가별로 요약한 엑셀 | | 파일 이름 |

## 리테일러별 조사

### UAE Sharaf DG (두레이 157, 직판 토글)

| 폴더 | 날짜 | 내용 | 결정 | 설명 근거 |
| --- | --- | --- | --- | --- |
| [sharaf-157-20261105](sharaf-157-20261105/README.md) | 11-05 | v3 포함 URL 조사. 외부 판매자 9건을 포함에서 제외하는 변경 대상 CSV | D098·D099 | 안내 문서 |
| [sharaf-157-live-toggle-20261109](sharaf-157-live-toggle-20261109/) | 11-09 | 직판 토글(`Sold By Sharaf DG`)을 켠 화면에서 본 냉장고·세탁 상품과 검색어별 결과 기록 | | 요약 파일 |
| [sharaf-157-october-filter-20261110](sharaf-157-october-filter-20261110/) | 11-10 | 11월 9일 검색 기록에 10월 상품명 필터를 다시 적용하고 v5와 대조 | | 요약 파일 |
| [sharaf-157-raw-toggle-20261110-267a8cbc](sharaf-157-raw-toggle-20261110-267a8cbc/) | 11-10 | 직판 토글을 켠 채 검색어 9개·31쪽을 필터 없이 그대로 모은 원본 1,239행 | | 요약 파일 |
| [sharaf-157-filtered-20261110-e4651deb](sharaf-157-filtered-20261110-e4651deb/) | 11-10 | 위 원본 1,239행에 판정을 적용한 결과. v7의 교체 입력 | | 다른 문서의 언급 |
| [sharaf-low-inclusion-cause-20261110-f122f38b](sharaf-low-inclusion-cause-20261110-f122f38b/README.md) | 11-10 | 기존 포함이 16개뿐이었던 원인 조사(새 요청·유료 호출 없음) | | 안내 문서 |
| [sharaf-toggle-causality-20261110-5972e8b2](sharaf-toggle-causality-20261110-5972e8b2/README.md) | 11-10 | 보쉬 KIV87NSE0M으로 토글 OFF·ON 목록을 대조해 원인 설명을 재검증 | | 안내 문서 |
| [sharaf-157-v6-preview-20261110-c268dd76](sharaf-157-v6-preview-20261110-c268dd76/) | 11-10 | **빈 폴더.** 11월 10일 작업 메모는 이 안의 `preview.json`을 근거로 적었으나 파일이 남아 있지 않다 | | 폴더 확인 |
| [sharaf-157-v7-20261110-e02f39e3](sharaf-157-v7-20261110-e02f39e3/README.md) | 11-10 | Sharaf DG 전체를 재조사 결과로 교체한 **공유용 v7** 생성·전수 대조 | D126 | 안내 문서 |
| [sharaf-direct-rule-20261110-839fcfd6](sharaf-direct-rule-20261110-839fcfd6/README.md) | 11-10 | 직판 토글 필수 수집을 규칙·자동 수집 설정에 반영한 기록과 무료 검증 | D127 | 안내 문서 |

### 대만 MomoShop (검색어 기반 수집)

| 폴더 | 날짜 | 내용 | 결정 | 설명 근거 |
| --- | --- | --- | --- | --- |
| [momo-population-audit-20261102-e8c0a2e0](momo-population-audit-20261102-e8c0a2e0/) | 11-02 | OSM 후보·공유용 v3·OSM 추출 SQL을 대조한 MomoShop 모수 점검과 검색어 겹침 기록 | | 요약 파일 |
| [momoshop-search-pdp-20261103-76f0f589](momoshop-search-pdp-20261103-76f0f589/README.md) | 11-03 | EY 검색어 11개로 상품 카드 후보를 수집 | D091 | 안내 문서 |
| [momoshop-final-pdp-20261103-51e01084](momoshop-final-pdp-20261103-51e01084/README.md) | 11-03 | 위 후보를 판정한 검색어 기반 최종 PDP 443개 | D092 | 안내 문서 |
| [f04787ba70c4e8c9b3e8b7e237de161a](f04787ba70c4e8c9b3e8b7e237de161a/README.md) | 11-03 | 검색 카드 6,407행 전체를 공유용 v3와 같은 26열로 실은 전체판정 엑셀·CSV | D093 | 안내 문서 |
| [momoshop-search-pdp-20261112-4ab49c5f](momoshop-search-pdp-20261112-4ab49c5f/README.md) | 11-12 | 같은 검색어 11개로 다시 수집. 포함 520개, 다운로드용 6,256건 CSV | D133·D134 | 안내 문서 |

### 이탈리아 MediaWorld (두레이 72, LG 표기·클릭 조건)

| 폴더 | 날짜 | 내용 | 결정 | 설명 근거 |
| --- | --- | --- | --- | --- |
| [mediaworld-lg-html-audit-20261101-77dee0f9](mediaworld-lg-html-audit-20261101-77dee0f9/) | 11-01 | 저장된 HTML만으로 LG 148개 상품을 대조(화면 실행·새 수집 없음). 판단 보류 141개 | | 요약 파일 |
| [mediaworld-lg-rule72-scenario-20261101-1e206f26](mediaworld-lg-rule72-scenario-20261101-1e206f26/) | 11-01 | 141개에 대한 **가정 계산**(저장 HTML에 링크가 없으면 누를 수 없다고 봄). 실제 화면 확인 결과가 아니다 | | 요약 파일 |
| [mediaworld-rule72-direct-20261101-dbb7e69d](mediaworld-rule72-direct-20261101-dbb7e69d/) | 11-01 | 141개를 실제 화면에서 대조한 기록, 누르기 전후 화면 예시, 접속 제한 근거 | | 파일 이름 |
| [mediaworld-all84-clicks-20261102-5850b120](mediaworld-all84-clicks-20261102-5850b120/) | 11-02 | 84개 상품에서 LG 링크를 실제로 눌러 브랜드 페이지 도착 여부를 검증 | | 요약 파일 |

### MediaMarkt (독일·헝가리·네덜란드)

| 폴더 | 날짜 | 내용 | 결정 | 설명 근거 |
| --- | --- | --- | --- | --- |
| [mediamarkt-de-v4-20261106](mediamarkt-de-v4-20261106/) | 11-06 | 독일 v4 370행의 현재 화면 점검과 포함에서 제외로 바꿀 대상 | D103 | 결정 기록 |
| [mediamarkt-de-osm-query-20261110](mediamarkt-de-osm-query-20261110/) | 11-10 | 독일 OSM 추출 SQL을 다시 돌려 저장분 370행과 차이 0건임을 확인 | | 요약 파일 |
| [mediamarkt-hu-nl-v6-20261110](mediamarkt-hu-nl-v6-20261110/README.md) | 11-10 | 헝가리·네덜란드 546개 PDP 제목·판매자 재검사와 **공유용 v6**. 헝가리 포함 2행 정정은 보류 | D124 | 안내 문서 |

### 베트남 Dienmayxanh (두레이 159) · 사우디 eXtra (두레이 158) · 프랑스 Darty

| 폴더 | 날짜 | 내용 | 결정 | 설명 근거 |
| --- | --- | --- | --- | --- |
| [dienmayxanh-closed-business-20261104-c58d71f6](dienmayxanh-closed-business-20261104-c58d71f6/) | 11-04 | Git에 올라간 파일 없음(실행 찌꺼기 `__pycache__`만 있음) | | 폴더 확인 |
| [dienmayxanh-closed-business-20261105-vpn-20261105-091740](dienmayxanh-closed-business-20261105-vpn-20261105-091740/README.md) | 11-05 | v3 포함 LG 114개의 영업 중단 표시 재확인 | | 안내 문서 |
| [dienmayxanh-v3-all-included-closed-20261105-20261105-112819](dienmayxanh-v3-all-included-closed-20261105-20261105-112819/README.md) | 11-05 | v3 포함 453개 전수 확인. 판매 중단 183건을 포함에서 제외하는 변경 대상 | D098·D099 | 안내 문서 |
| [extra-158-20261105](extra-158-20261105/README.md) | 11-05 | v3 포함 272개 상품 화면의 품절 문구 전수 확인. 포함에서 제외 대상 129건 | D097~D099 | 안내 문서 |
| [darty-original-url-20261113](darty-original-url-20261113/) | 11-13 | 152개 상품의 원래 주소 재확인 결과 CSV. 기준은 결정 D138 | | 파일 이름 |

## EY 요청 자료

| 폴더 | 날짜 | 내용 | 결정 | 설명 근거 |
| --- | --- | --- | --- | --- |
| [ey-25개국-분석-20261113](ey-25개국-분석-20261113/README.md) | 11-13 | EY 「25개국 분석_261113_v0.1.xlsx」 양식에 LG·삼성 값을 채운 사본과 근거. 계산 기준은 EY 확인 대기 | D139·D140 | 안내 문서 |
| [ey-25-country-audit-20261113-39d0ac5e](ey-25-country-audit-20261113-39d0ac5e/검사결과.md) | 11-13 | 위 파일의 독립 검사 결과와 조회 자료. 대조표는 8월 값을 고치기 **전** 파일 기준 | | 폴더 안 검사결과.md |
| [ey-design-guide-report](ey-design-guide-report/index.html) | 11-12~ | EY 디자인 가이드의 장별 적용 보고서(HTML). 대시보드 저장소도 이 파일을 링크한다 | D135~D137·D141 | 결정 기록 |

## OSM 대상 목록

| 폴더 | 날짜 | 내용 | 결정 | 설명 근거 |
| --- | --- | --- | --- | --- |
| [osm-target-filter-20261012-01a12f10](osm-target-filter-20261012-01a12f10/) | 10-12 | OSM 수집 URL에서 진단 대상 35개 리테일러·제품군만 남긴 엑셀과 행별 근거 | D032·D033 | 결정 기록 |
| [osm-history-20261013-01a12f10](osm-history-20261013-01a12f10/) | 10-13 | OSM 대상 유통 리스트의 수집 URL 수정본과 행별 근거. [원본 목록](../docs/SOURCES.md)에 등록 | | 다른 문서의 언급 |

## BCP 시험 결과 비교 (2026-09)

| 폴더 | 날짜 | 내용 | 결정 | 설명 근거 |
| --- | --- | --- | --- | --- |
| [bcp-temporal-compare-20260930](bcp-temporal-compare-20260930/) | 09-30 | BCP 1차 테스트와 Temporal 실행 결과를 비교한 엑셀 | | 파일 이름 |
| [bcp-three-way-compare-20260930](bcp-three-way-compare-20260930/) | 09-30 | 원본·1차·Temporal 세 값을 비교한 엑셀 | | 파일 이름 |
