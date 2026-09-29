# Jev용 파서 실행 결과

- 입력: `/Users/codestepseunghee/codestep/lg-online-retailer-analysis/1차 테스트/bcp-zyte-poc/results/20260928T060234KST`
- 처리: 9개 페이지
- 기존 파서·입력 수집본·기존 parsed/assessed/manifest는 수정하지 않음.
- Jev API 호출·최종 판정·링크 이동 검사는 실행하지 않음.
- 영역 수는 내용 분할 개수이며 항목 존재 개수가 아님.

| 리테일러 | 본문 영역 | 요청 초안 | 큰 요청 | 수집 검사 문제 |
| --- | ---: | ---: | ---: | ---: |
| alza | 101 | 64 | 0 | 0 |
| amazon-it | 261 | 79 | 0 | 0 |
| boulanger | 514 | 226 | 0 | 0 |
| coolblue | 19 | 17 | 0 | 0 |
| datart | 2086 | 1839 | 0 | 0 |
| elgiganten | 34 | 17 | 0 | 0 |
| mediamarkt-es | 227 | 64 | 0 | 0 |
| mediamarkt-nl | 112 | 43 | 0 | 0 |
| mediaworld | 217 | 63 | 0 | 0 |

각 리테일러의 `본문_검토.md`에서 실제 추출 문장을 먼저 검토한다.
요청 초안은 ID19·20·23의 영역별 의미 질문이다. 응답을 페이지 Y/N으로 변환하는 기능은 아직 없다.
ID8·9·10 원시값과 ID18·21·22에 필요한 이미지·링크는 evidence 파일에 보존한다.
실제 화면 상단·표시 여부, 링크 전수 이동 확인, 사람 검수는 후속 단계다.
