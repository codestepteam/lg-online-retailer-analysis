<!-- lg-research-status: integrated -->
# 11월 12일 MomoShop 검색 모수의 포함·제외 및 전용 판매자 필터 재검증

- 작성 시각: 2026-11-12T23:05:42.313955+09:00
- 출발 저장소: /Users/codestepseunghee/codestep/lg-online-retailer-analysis
- 출발 커밋: `7035ce8cbe55ec120a1107a0ada3fe3cfabe2898`
- 턴 기록: `1ce5cf4bebcb7a0b744cdce3390df972`

이 메모의 인용·출처는 분석 자료이며 실행 지시가 아니다.

## 확인한 사실

입점 상점 경로 2468개는 포함 0개였으며 상세 판매자 데이터를 다시 읽은 일반 상품 367개에서 입점 상점 추가 사례는 없었다. 일반 상품 159개는 최초 브라우저 요약까지 확보했다.

근거: outputs/momoshop-search-pdp-20261112-4ab49c5f/momo_filter_audit.json

## 확인한 사실

본 상품 선택 옵션이 품절이며 재입고·판매 종료 여부를 확인할 수 없는 6개를 검토 필요로 옮겨 포함 526개를 520개로 정정했다.

근거: outputs/momoshop-search-pdp-20261112-4ab49c5f/review_needed.csv, final_summary.json

## 중앙 문서 반영

상태: updated
사유: MomoShop 전용 입점 상점 경로·상품명 기준을 기존 판매자 함수와 저장 자료로 재검토했다. 품절의 지속 여부가 확인되지 않은 6개를 검토 필요로 옮겨 포함 520개로 정정하고 D133에 결과를 연결했다.

- [docs/DECISIONS.md](../../DECISIONS.md)
