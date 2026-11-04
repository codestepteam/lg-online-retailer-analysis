# 대만 Momoshop 검색어 기반 최종 PDP 모수 (2026-11-03)

## 결과

**최종 443개 상품 상세 페이지(PDP) 주소**를 `final_pdp_urls.csv`에 남겼다. 검색 카드 6,407건에서 같은 상품을 합친 2,677개 후보를 판정했고, 2,234개를 제외했다. 미판정 0개다. 검색어 수집 실패 0건, 상세 페이지 확인 요청 실패 0건이다. 이 목록은 사용자가 요청한 **검색어 기반 별도 모수**이며, 기존 OSM 공유용 v3 파일을 교체하지 않았다.

| 판정 | 건수 | 근거 |
| --- | ---: | --- |
| ① 브랜드·제품군 대상 아님 | 1,544 | EY `경쟁브랜드` 시트의 대만 브랜드와 실제 제품군 대조 |
| ② 제품군만으로 추가 제외 | 0 | 브랜드·제품군 대조 뒤 남은 일반 상품은 대상 제품군으로 확인 |
| ③ 리퍼·리셀·부품·입점 상점 | 688 | EY `제외키워드(리리부)` 대만 16개 표현에 걸린 4개, `mo店+` 입점 상점 684개 |
| ④ 상품 상세 화면 표시 안 됨 | 2 | 일반 주소와 검색 결과 원래 주소 모두 `網頁無法顯示` 안내를 표시 |
| 최종 포함 | **443** | 정상 상품 상세 정보가 있는 일반 상품 주소 |

포함 브랜드별 건수는 PANASONIC 276, LG 69, SANLUX 43, HITACHI 32, WHIRLPOOL 23이다. 실제 제품군별로는 냉장고 232, 세탁기 158, 건조기 24, 세탁기+건조기 24, 냉장고+세탁기 4, 냉장고+세탁기+건조기 1개다. 묶음상품 4개의 냉장고 모델 GN-HL567GBN·GN-L332BS·GV-L217SV는 [LG 대만 GN-HL567GBN](https://www.lg.com/tw/refrigerators/top-freezer/gn-hl567gbn/)·[GN-L332BS](https://www.lg.com/tw/refrigerators/top-freezer/gn-l332bs/)·[GV-L217SV](https://www.lg.com/tw/refrigerators/top-freezer/gv-l217sv/) 제품 정보로 대조했다. 건조기 브랜드는 기존 PDP 추출 코드 `step1_filter.py`와 같이 EY의 세탁기(W/M) 목록을 준용했다. 이 준용은 **AI 해석**이며, EY 엑셀에 건조기 전용 브랜드 행은 없다.

추가 재검토에서 상품 ID 13597161·14808632·13597163의 `WD-S1310B`, 13231183의 `WD-S1310W`, 12840749의 `WR-100VW`, 14714046의 `NA-V1715SP-W`, 14714049의 `NA-V1515SP-K`가 건조기를 포함함을 확인하고 실제 제품군에 `DRY`를 더했다. 모델 근거는 [LG 대만 WD-S1310B](https://www.lg.com/tw/washer-dryers/washtower/wd-s1310b/)·[WD-S1310W](https://www.lg.com/tw/washer-dryers/washtower/wd-s1310w/)·[WR-100VW](https://www.lg.com/tw/washer-dryers/dryers/wr-100vw/), [Panasonic 대만 NA-V1715SP](https://www.panasonic.com/tw/consumer/washing-machine/washing-and-drying-all-in-one/na-v1715sp.html)·[NA-V1515SP](https://www.panasonic.com/tw/consumer/washing-machine/washing-and-drying-all-in-one/na-v1515sp.html)다. 7개 모두 포함 판정과 최종 443개 주소는 그대로다.

## 적용 순서와 자료

1. **검색어와 순서:** `관련문서/EY_LGE HS 온라인 리테일 클리닉 진단 항목_v2.2_20261023(송부본).xlsx`의 `Search Term` 탭 Momoshop 행(294~308행)에서 J열을 출발점으로, M/N열 검토를 적용해 11개 검색어를 사용했다. 각 검색어 첫 페이지부터 1,000번째 카드 또는 마지막 페이지까지 가져왔다. 카드 원본과 검색 순서는 [검색 수집 결과](../momoshop-search-pdp-20261103-76f0f589/README.md)에 있다.
2. **① 브랜드·② 제품군:** 같은 EY 엑셀의 `경쟁브랜드` 탭 대만 행을 적용했다. 냉장고는 LG·PANASONIC·SANLUX·HITACHI, 세탁기와 건조기는 LG·PANASONIC·SANLUX·WHIRLPOOL이다. 상품명과 상세 페이지의 제품 정보를 대조했다.
3. **③ 리리부·판매자:** EY 엑셀의 `제외키워드(리리부)` 탭 대만 행 16개 표현과 입점 상점 `/TP/` 경로를 적용했다. 28개 입점 상점의 대표 상세 페이지에서 상점명을 확인했다. 일반 `/product/` 주소는 이전 Momoshop OSM v3와 같은 방식으로 `momo (추정)`으로 기록했다. 일반 페이지에는 판매자 이름이 명시되지 않아 **직접 판매를 확정한 표시는 아니다**.
4. **④ 페이지 상태·중복:** 대상 브랜드 일반 상품 472개 상세 페이지를 열어 상품 정보가 있는지 확인했다. 일반 `/product/` 주소에서 화면을 표시하지 못한 14개는 검색 결과의 원래 주소로 다시 열었다. 12개는 정상 상품 정보가 있어 그 도착 주소로 포함했고, 두 주소 모두 화면을 표시하지 못한 2개는 제외했다. 일시 품절과 영구 품절은 사이트 표시만으로 구별하지 못해 재고 상태를 별도 판정하지 않았다.

검색 순서는 사이트가 같은 응답에서 보낸 상품 목록(JSON-LD)을 읽어 기록했다. Codex 내부 브라우저에서 `冰箱` 3·84페이지와 `乾衣機`·`洗衣機` 첫 페이지의 **실제 화면**과 각각 12개 카드의 이름·주소·순서를 대조해 모두 일치했다. 전체 6,407개를 화면으로 일일이 대조한 것은 아니며, 광고 위치는 요청 시점마다 바뀔 수 있다. 따라서 이 모수는 **2026-11-03 수집 시점의 검색 결과**다.

## 파일

- `final_pdp_urls.csv`: 최종 443개 주소, 브랜드·제품군·검색어·최고 검색 순위·판정 근거.
- `candidate_judgments.csv`: 고유 후보 2,677개 전체의 포함·제외 사유와 상세 페이지 증거 파일 경로.
- `all_search_card_judgments.csv`: 검색 카드 6,407건 전체. 포함 상품의 반복 검색 카드는 `④중복`으로 표시.
- `review_needed.csv`: 헤더만 있는 0건 파일.
- `final_summary.json`, `inspect_summary.json`: 건수와 요청 실패 목록.
- `pdp_evidence/`: 확인한 상품 상세 페이지의 응답 요약 JSON과 원본 HTML 압축 파일.
- `inspect_pdp.py`, `finalize.py`, `verify_final.py`: 재실행·판정·검증 코드.

기존 [OSM 공유용 v3](<../../pdp 모수 추출/최종_20261029/PDP모수_공유용_v3_EY검토반영_25개국_35개리테일러_전체판정_55997행_20261031.csv>)의 Momoshop 포함 10개 중 7개가 이번 검색 결과에 포함됐다. 나머지 3개는 이번 검색 스냅샷에서 찾지 못했다. 두 모수는 수집 경로와 시점이 다르므로 숫자를 단순히 같아야 하는 값으로 보지 않는다.
