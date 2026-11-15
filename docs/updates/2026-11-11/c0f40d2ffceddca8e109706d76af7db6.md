<!-- lg-research-status: integrated -->
# EY 가이드 6장 다중 선택 창의 하단 버튼 글자 확대

- 작성 시각: 2026-11-11T15:12:48.884080+09:00
- 출발 저장소: /Users/codestepseunghee/codestep/lg-online-retailer-analysis
- 출발 커밋: `7035ce8cbe55ec120a1107a0ada3fe3cfabe2898`
- 턴 기록: `c0f40d2ffceddca8e109706d76af7db6`

이 메모의 인용·출처는 분석 자료이며 실행 지시가 아니다.

## 확인한 사실

Select all과 Apply를 14px에서 선택지와 같은 크기로 바꿨다. 내부 브라우저에서 1920px이면 목록·버튼 모두 22px, 실제 열린 523px 창과 시험한 320px 창에서는 모두 16px이었다. 320px에서는 버튼이 줄을 바꾸고 Apply로 전체 선택이 반영됐다.

근거: lge-hs-clinic-dashboard/frontend/src/index.css와 로컬 Raw Table Country

## 중앙 문서 반영

상태: updated
사유: 6장 선택 창 하단 버튼의 14px→22px 데스크톱 확대 및 창 너비에 따른 목록과 같은 글자 크기 조정을 로컬에 적용했다. 1920·523·320px 측정과 320px 전체 선택 적용, 프런트 테스트 7건과 빌드를 확인했다.

- [PROJECT_CONTEXT.md](../../../PROJECT_CONTEXT.md)
