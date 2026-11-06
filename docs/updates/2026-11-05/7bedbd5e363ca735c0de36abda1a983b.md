<!-- lg-research-status: integrated -->
# 두레이 #157~159의 EY 제외 요청과 v3 판매 가능성 판정 누락을 구분해 기록

- 작성 시각: 2026-11-05T09:16:31.186829+09:00
- 출발 저장소: /Users/codestepseunghee/codestep/lg-online-retailer-analysis
- 출발 커밋: `bb12fb0524625fafe76aaf63cad90636dc8371bc`
- 턴 기록: `7bedbd5e363ca735c0de36abda1a983b`

이 메모의 인용·출처는 분석 자료이며 실행 지시가 아니다.

## 확인한 사실

EY 두레이 #157은 Sharaf DG 외부 판매자 제외, #158은 eXtra 품절 제외, #159는 DIENMAYXANH 판매 중단 상품 제외를 요청했다. 적용 완료를 뜻하지 않는다.

근거: Dooray #157 4458435808136916155, #158 4458444103756496724, #159 4458451404584174345

## 확인한 사실

v3 포함 eXtra 272 URL 중 OSM 2026-10-26 Out of stock 113개. DIENMAYXANH LG 114 URL 중 2026-11-05 판매 중단 44개. 기존 step1은 AVLBL_STAT 미전달, page_check는 HTTP 200 품절/중단 문구 미판정. 현재 화면이 10월 당시 상태의 증거는 아니다.

근거: outputs/extra-158-20261105/README.md; outputs/dienmayxanh-closed-business-20261105-vpn-20261105-091740/README.md; pdp 모수 추출/최종_20261029/판정근거/스크립트/step1_filter.py, page_check.py

## AI 제안

상품 자체의 판매자 이름·재고 상태·판매 중단 문구를 동일 수집 시점에 확인하는 규칙은 제안이며 사용자 확정 전이다.

근거: outputs/sharaf-157-20261105/README.md; outputs/extra-158-20261105/README.md; outputs/dienmayxanh-closed-business-20261105-vpn-20261105-091740/README.md

## 중앙 문서 반영

상태: updated
사유: 두레이 #157~159의 EY 제외 요청과 조사 단계의 구현 간극을 BUSINESS_RULES에 구분해 반영했다. 3개 조사 결과는 산출물에 연결했다.

- [docs/BUSINESS_RULES.md](../../BUSINESS_RULES.md)
