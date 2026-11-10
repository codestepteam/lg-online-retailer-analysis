<!-- lg-research-status: integrated -->
# 모든 로컬 Codex 프로젝트에 원문-답변 누락 대조 하네스 설치

- 작성 시각: 2026-11-10T13:57:18.573461+09:00
- 출발 저장소: /Users/codestepseunghee/codestep/lg-online-retailer-analysis
- 출발 커밋: `a3d41077695a33564dad172c91517f32c4a9f86c`
- 턴 기록: `bf36cc4f6575d1eb8b35ddc1aea60a8a`

이 메모의 인용·출처는 분석 자료이며 실행 지시가 아니다.

## 사용자 결정

사용자는 답변 누락·뭉뚱그림 개선을 모든 Codex 작업에 공통 지침·검사 절차로 적용하기로 선택했다. LG에만 한정하지 않는다.

근거: 이 채팅의 적용 범위 질문에 대한 사용자 선택(2026-11-10)

## 확인한 사실

사용자 홈 하네스의 구조화 원문 대조 프로그램·시험·절차와 AGENTS.md 지침 및 UserPromptSubmit/Stop 훅 정의를 추가했다. 기존 훅은 보존했으며 새 훅의 앱 신뢰·실제 자동 실행은 아직 확인 전이다.

근거: ~/.codex/harness/answer_coverage.py, test_answer_coverage.py, ANSWER_COVERAGE.md; ~/.codex/AGENTS.md 및 hooks.json

## 확인한 사실

새 하네스 unittest 32개와 기존 LG 문서 훅 unittest 17개가 통과했다. 실제 네덜란드 원문으로 생성 초안은 성공하고 Verzonden en verkocht door 한 문구를 뺀 초안은 종료코드 2로 실패했다. 설정 검증에서 기존 훅 전부와 새 훅 각 1개, Python 구문 및 문서 링크를 확인했다.

근거: python3 -B -m unittest discover -s ~/.codex/harness -p test_answer_coverage.py -v; /usr/bin/python3 -B -m unittest discover -s .codex/hooks -p test_lg_research_memory.py -v; ~/.codex/harness/verification.json

## 미확인

새 훅의 Codex 앱 신뢰와 실제 자동 실행은 미확인이다. 정상 설정 UI 확인을 시도했으나 Computer Use가 com.openai.codex 앱을 안전상 조작 금지 대상으로 거절했다. 신뢰 상태 직접 수정·우회 실행은 하지 않았다. 사용자 Settings > Hooks 검토·신뢰가 남아 있다.

근거: 공식 https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks 및 이 턴 cua.getApp("Codex") 결과

## 중앙 문서 반영

상태: updated
사유: 모든 Codex 프로젝트 적용 선택을 D125와 HOOKS에 반영했다. 전역 AGENTS·원문 단위 대조 프로그램·설정·절차를 추가하고 기존 훅을 보존했다. 새 시험32개·기존17개·실제 원문 누락 탐지·설정과 문서 검증을 마쳤다. 새 훅의 앱 신뢰·실제 자동 실행은 보호된 앱 조작 제한으로 미확인이며 완료라고 보고하지 않는다.

- [docs/DECISIONS.md](../../DECISIONS.md)
- [docs/HOOKS.md](../../HOOKS.md)
