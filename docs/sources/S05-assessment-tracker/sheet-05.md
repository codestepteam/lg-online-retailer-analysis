# S05 시트 5 데이터 누락점검

원본 파일: `★EY_LGE_Clinic_Assessment Summary_Improvement Tracker_V0.1_20260911 (1).xlsx`

시트: `데이터 누락점검` · 상태: `hidden` · 범위: 값/수식 전체

빈 셀은 생략했다. 병합 셀의 값은 시작 셀에만 있으며 자동 채움하지 않았다. 캐시값은 재계산 결과가 아니다.

병합 범위: N3:O3, P3:Q3, D42:E42, F42:H42, L42:M42, N42:O42, P42:Q42, I3:J3, I42:J42, D3:E3, F3:H3, L3:M3

숨김 행: 없음

숨김 열 번호: 없음

## Row 1

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A1 | 국가 · 리테일러별 ID 진단항목 데이터 누락(Null) 판정 매트릭스 |  |

## Row 2

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A2 | 각 셀 = 해당 ID 시트의 원본 데이터 행 수 (COUNTIFS). 0 = 데이터 누락(Null) |  |

## Row 3

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A3 | ▼ 축 정의 |  |
| D3 | Spain |  |
| F3 | Italy |  |
| I3 | Netherlands |  |
| K3 | Sweden |  |
| L3 | France |  |
| N3 | Poland |  |
| P3 | Czech Republic |  |
| R3 | 합계 |  |
| S3 | 누락 |  |

## Row 4

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| D4 | ECI |  |
| E4 | Media Markt |  |
| F4 | Media World |  |
| G4 | Amazon |  |
| H4 | Unieuro |  |
| I4 | Coolblue |  |
| J4 | Media Markt |  |
| K4 | ELGIGANTEN |  |
| L4 | Darty |  |
| M4 | Boulanger |  |
| N4 | Media Expert |  |
| O4 | RTV EURO AGD |  |
| P4 | Datart |  |
| Q4 | Alza |  |
| R4 | 전체 행수 |  |
| S4 | Null 개수 |  |
| T4 | 결측 (일부 리테일러 데이터 누락) |  |

## Row 5

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A5 | [Helper] 국가 매칭 패턴 |  |
| D5 | Spain |  |
| E5 | Spain |  |
| F5 | Italy |  |
| G5 | Italy |  |
| H5 | Italy |  |
| I5 | Netherlands |  |
| J5 | Netherlands |  |
| K5 | Sweden |  |
| L5 | France |  |
| M5 | France |  |
| N5 | Poland |  |
| O5 | Poland |  |
| P5 | Czech* |  |
| Q5 | Czech* |  |

## Row 6

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A6 | [Helper] 리테일러 매칭 패턴 |  |
| D6 | Elcorteingles* |  |
| E6 | Media*Markt |  |
| F6 | Mediaworld |  |
| G6 | Amazon |  |
| H6 | Unieuro |  |
| I6 | Coolblue |  |
| J6 | Media*Markt |  |
| K6 | Elgiganten |  |
| L6 | Darty |  |
| M6 | Boulanger |  |
| N6 | Media*Expert |  |
| O6 | Rtv*Euro*Agd |  |
| P6 | Datart |  |
| Q6 | Alza |  |

## Row 7

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A7 | ID 시트 |  |
| B7 | 국가 열 |  |
| C7 | 리테일러 열 |  |

## Row 8

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A8 | ID1 |  |
| B8 | C |  |
| C8 | D |  |
| D8 | 543 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),D$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),D$6),0) [OOXML {"ca": "1"}] |
| E8 | 501 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),E$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),E$6),0) [OOXML {"t": "shared", "ref": "E8:Q23", "ca": "1", "si": "0"}] |
| F8 | 423 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),F$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G8 | 423 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),G$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H8 | 423 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),H$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I8 | 242 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),I$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K8 | 423 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),K$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L8 | 414 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),L$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M8 | 390 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),M$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N8 | 430 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),N$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O8 | 513 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),O$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P8 | 423 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),P$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q8 | 421 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A8&amp;"'!"&amp;$B8&amp;":"&amp;$B8),Q$5,INDIRECT("'"&amp;$A8&amp;"'!"&amp;$C8&amp;":"&amp;$C8),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R8 | 5569 | =SUM(D8:Q8) [OOXML {"ca": "1"}] |
| S8 | 0 | =COUNTIF(D8:Q8,0) [OOXML {"ca": "1"}] |

## Row 9

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A9 | ID2 |  |
| B9 | C |  |
| C9 | D |  |
| D9 | 139 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),D$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),D$6),0) [OOXML {"t": "shared", "ref": "D9:Q24", "ca": "1", "si": "1"}] |
| E9 | 139 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),E$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F9 | 141 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),F$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G9 | 94 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),G$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H9 | 141 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),H$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I9 | 52 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),I$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K9 | 141 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),K$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L9 | 92 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),L$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M9 | 92 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),M$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N9 | 141 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),N$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O9 | 141 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),O$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P9 | 141 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),P$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q9 | 141 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A9&amp;"'!"&amp;$B9&amp;":"&amp;$B9),Q$5,INDIRECT("'"&amp;$A9&amp;"'!"&amp;$C9&amp;":"&amp;$C9),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R9 | 1595 | =SUM(D9:Q9) [OOXML {"t": "shared", "ref": "R9:R35", "ca": "1", "si": "2"}] |
| S9 | 0 | =COUNTIF(D9:Q9,0) [OOXML {"t": "shared", "ref": "S9:S35", "ca": "1", "si": "3"}] |

## Row 10

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A10 | ID3 |  |
| B10 | C |  |
| C10 | D |  |
| D10 | 139 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),D$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E10 | 139 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),E$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F10 | 78 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),F$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G10 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),G$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),G$6),0) [OOXML {"ca": "1"}] |
| H10 | 94 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),H$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I10 | 52 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),I$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K10 | 94 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),K$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L10 | 92 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),L$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M10 | 92 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),M$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N10 | 94 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),N$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O10 | 94 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),O$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P10 | 94 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),P$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q10 | 94 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A10&amp;"'!"&amp;$B10&amp;":"&amp;$B10),Q$5,INDIRECT("'"&amp;$A10&amp;"'!"&amp;$C10&amp;":"&amp;$C10),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R10 | 1156 | =SUM(D10:Q10) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S10 | 1 | =COUNTIF(D10:Q10,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |
| T10 | GNB 랜딩 URL 확인하여 EY-&gt;CNX에 전달 필요 |  |

## Row 11

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A11 | ID4 |  |
| B11 | C |  |
| C11 | D |  |
| D11 | 102 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),D$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E11 | 102 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),E$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F11 | 90 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),F$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G11 | 90 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),G$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H11 | 90 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),H$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I11 | 56 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),I$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K11 | 90 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),K$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L11 | 72 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),L$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M11 | 72 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),M$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N11 | 100 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),N$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O11 | 110 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),O$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P11 | 90 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),P$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q11 | 90 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A11&amp;"'!"&amp;$B11&amp;":"&amp;$B11),Q$5,INDIRECT("'"&amp;$A11&amp;"'!"&amp;$C11&amp;":"&amp;$C11),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R11 | 1154 | =SUM(D11:Q11) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S11 | 0 | =COUNTIF(D11:Q11,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 12

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A12 | ID7 |  |
| B12 | D |  |
| C12 | F |  |
| D12 | 38 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),D$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E12 | 38 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),E$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F12 | 31 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),F$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G12 | 30 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),G$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H12 | 30 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),H$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I12 | 26 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),I$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K12 | 28 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),K$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L12 | 26 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),L$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M12 | 26 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),M$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N12 | 32 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),N$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O12 | 32 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),O$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P12 | 14 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),P$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q12 | 14 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A12&amp;"'!"&amp;$B12&amp;":"&amp;$B12),Q$5,INDIRECT("'"&amp;$A12&amp;"'!"&amp;$C12&amp;":"&amp;$C12),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R12 | 365 | =SUM(D12:Q12) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S12 | 0 | =COUNTIF(D12:Q12,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 13

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A13 | ID8 |  |
| B13 | C |  |
| C13 | D |  |
| D13 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),D$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E13 | 54 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),E$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F13 | 56 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),F$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G13 | 206 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),G$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H13 | 16 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),H$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I13 | 163 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),I$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K13 | 46 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),K$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L13 | 6 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),L$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M13 | 37 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),M$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N13 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),N$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O13 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),O$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P13 | 286 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),P$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q13 | 265 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A13&amp;"'!"&amp;$B13&amp;":"&amp;$B13),Q$5,INDIRECT("'"&amp;$A13&amp;"'!"&amp;$C13&amp;":"&amp;$C13),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R13 | 1135 | =SUM(D13:Q13) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S13 | 3 | =COUNTIF(D13:Q13,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |
| T13 | X (Brand Category Page 관련) 단, Unieuro, Darty, Media Expert, RTV EURO AGD는 왜 데이터가 있는지 확인 요망(CNX) |  |

## Row 14

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A14 | ID9 |  |
| B14 | C |  |
| C14 | D |  |
| D14 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),D$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E14 | 17 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),E$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F14 | 17 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),F$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G14 | 25 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),G$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H14 | 2 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),H$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I14 | 17 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),I$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K14 | 12 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),K$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L14 | 2 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),L$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M14 | 11 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),M$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N14 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),N$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O14 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),O$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P14 | 22 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),P$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q14 | 21 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A14&amp;"'!"&amp;$B14&amp;":"&amp;$B14),Q$5,INDIRECT("'"&amp;$A14&amp;"'!"&amp;$C14&amp;":"&amp;$C14),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R14 | 146 | =SUM(D14:Q14) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S14 | 3 | =COUNTIF(D14:Q14,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |
| T14 | X (Brand Category Page 관련) 단, Unieuro, Darty, Media Expert, RTV EURO AGD는 왜 데이터가 있는지 확인 요망(CNX) |  |

## Row 15

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A15 | ID10 |  |
| B15 | C |  |
| C15 | D |  |
| D15 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),D$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E15 | 51 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),E$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F15 | 51 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),F$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G15 | 75 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),G$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H15 | 5 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),H$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I15 | 51 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),I$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K15 | 36 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),K$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L15 | 6 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),L$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M15 | 33 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),M$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N15 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),N$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O15 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),O$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P15 | 66 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),P$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q15 | 63 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A15&amp;"'!"&amp;$B15&amp;":"&amp;$B15),Q$5,INDIRECT("'"&amp;$A15&amp;"'!"&amp;$C15&amp;":"&amp;$C15),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R15 | 437 | =SUM(D15:Q15) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S15 | 3 | =COUNTIF(D15:Q15,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |
| T15 | X (Brand Category Page 관련) 단, Unieuro, Darty, Media Expert, RTV EURO AGD는 왜 데이터가 있는지 확인 요망(CNX) |  |

## Row 16

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A16 | ID11 |  |
| B16 | C |  |
| C16 | D |  |
| D16 | 99 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),D$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E16 | 92 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),E$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F16 | 99 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),F$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G16 | 83 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),G$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H16 | 98 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),H$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I16 | 54 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),I$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K16 | 97 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),K$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L16 | 80 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),L$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M16 | 77 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),M$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N16 | 84 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),N$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O16 | 102 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),O$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P16 | 97 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),P$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q16 | 96 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A16&amp;"'!"&amp;$B16&amp;":"&amp;$B16),Q$5,INDIRECT("'"&amp;$A16&amp;"'!"&amp;$C16&amp;":"&amp;$C16),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R16 | 1158 | =SUM(D16:Q16) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S16 | 0 | =COUNTIF(D16:Q16,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 17

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A17 | ID12 |  |
| B17 | C |  |
| C17 | D |  |
| D17 | 4677 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),D$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E17 | 3700 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),E$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F17 | 3327 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),F$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G17 | 1363 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),G$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H17 | 2255 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),H$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I17 | 1554 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),I$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K17 | 3118 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),K$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L17 | 876 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),L$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M17 | 2495 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),M$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N17 | 3603 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),N$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O17 | 4769 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),O$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P17 | 7408 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),P$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q17 | 10069 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A17&amp;"'!"&amp;$B17&amp;":"&amp;$B17),Q$5,INDIRECT("'"&amp;$A17&amp;"'!"&amp;$C17&amp;":"&amp;$C17),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R17 | 49214 | =SUM(D17:Q17) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S17 | 0 | =COUNTIF(D17:Q17,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 18

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A18 | ID13 |  |
| B18 | C |  |
| C18 | D |  |
| D18 | 440 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),D$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E18 | 290 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),E$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F18 | 288 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),F$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G18 | 244 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),G$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H18 | 235 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),H$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I18 | 120 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),I$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K18 | 528 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),K$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L18 | 169 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),L$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M18 | 306 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),M$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N18 | 693 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),N$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O18 | 413 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),O$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P18 | 621 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),P$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q18 | 836 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A18&amp;"'!"&amp;$B18&amp;":"&amp;$B18),Q$5,INDIRECT("'"&amp;$A18&amp;"'!"&amp;$C18&amp;":"&amp;$C18),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R18 | 5183 | =SUM(D18:Q18) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S18 | 0 | =COUNTIF(D18:Q18,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 19

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A19 | ID14 |  |
| B19 | C |  |
| C19 | D |  |
| D19 | 1478 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),D$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E19 | 566 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),E$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F19 | 654 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),F$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G19 | 866 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),G$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H19 | 242 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),H$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I19 | 634 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),I$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K19 | 2330 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),K$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L19 | 1732 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),L$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M19 | 904 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),M$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N19 | 2005 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),N$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O19 | 1227 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),O$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P19 | 4659 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),P$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q19 | 4254 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A19&amp;"'!"&amp;$B19&amp;":"&amp;$B19),Q$5,INDIRECT("'"&amp;$A19&amp;"'!"&amp;$C19&amp;":"&amp;$C19),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R19 | 21551 | =SUM(D19:Q19) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S19 | 0 | =COUNTIF(D19:Q19,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 20

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A20 | ID15 |  |
| B20 | C |  |
| C20 | D |  |
| D20 | 441 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),D$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E20 | 290 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),E$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F20 | 288 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),F$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G20 | 244 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),G$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H20 | 237 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),H$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I20 | 120 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),I$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K20 | 531 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),K$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L20 | 169 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),L$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M20 | 334 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),M$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N20 | 693 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),N$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O20 | 414 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),O$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P20 | 621 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),P$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q20 | 884 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A20&amp;"'!"&amp;$B20&amp;":"&amp;$B20),Q$5,INDIRECT("'"&amp;$A20&amp;"'!"&amp;$C20&amp;":"&amp;$C20),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R20 | 5266 | =SUM(D20:Q20) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S20 | 0 | =COUNTIF(D20:Q20,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 21

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A21 | ID18_19_20_21_22_23 |  |
| B21 | C |  |
| C21 | E |  |
| D21 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),D$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E21 | 90 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),E$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F21 | 90 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),F$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G21 | 144 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),G$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H21 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),H$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I21 | 90 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),I$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K21 | 60 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),K$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L21 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),L$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M21 | 54 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),M$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N21 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),N$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O21 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),O$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P21 | 12 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),P$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q21 | 114 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A21&amp;"'!"&amp;$B21&amp;":"&amp;$B21),Q$5,INDIRECT("'"&amp;$A21&amp;"'!"&amp;$C21&amp;":"&amp;$C21),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R21 | 654 | =SUM(D21:Q21) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S21 | 5 | =COUNTIF(D21:Q21,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |
| T21 | X (Brand Category Page 관련) |  |

## Row 22

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A22 | ID24 |  |
| B22 | C |  |
| C22 | D |  |
| D22 | 86 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),D$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E22 | 86 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),E$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F22 | 74 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),F$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G22 | 49 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),G$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H22 | 57 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),H$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I22 | 13 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),I$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K22 | 97 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),K$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L22 | 43 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),L$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M22 | 85 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),M$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N22 | 98 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),N$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O22 | 86 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),O$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P22 | 135 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),P$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q22 | 141 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A22&amp;"'!"&amp;$B22&amp;":"&amp;$B22),Q$5,INDIRECT("'"&amp;$A22&amp;"'!"&amp;$C22&amp;":"&amp;$C22),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R22 | 1050 | =SUM(D22:Q22) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S22 | 0 | =COUNTIF(D22:Q22,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 23

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A23 | ID25 |  |
| B23 | C |  |
| C23 | D |  |
| D23 | 67 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),D$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E23 | 51 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),E$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| F23 | 64 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),F$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| G23 | 28 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),G$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| H23 | 52 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),H$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| I23 | 11 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),I$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| K23 | 66 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),K$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| L23 | 27 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),L$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| M23 | 65 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),M$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| N23 | 50 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),N$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| O23 | 56 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),O$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| P23 | 95 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),P$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| Q23 | 106 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A23&amp;"'!"&amp;$B23&amp;":"&amp;$B23),Q$5,INDIRECT("'"&amp;$A23&amp;"'!"&amp;$C23&amp;":"&amp;$C23),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "0"}] |
| R23 | 738 | =SUM(D23:Q23) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S23 | 0 | =COUNTIF(D23:Q23,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 24

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A24 | ID_29 |  |
| B24 | C |  |
| C24 | D |  |
| D24 | 440 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),D$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| E24 | 290 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),E$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| F24 | 288 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),F$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| G24 | 244 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),G$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| H24 | 235 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),H$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| I24 | 120 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),I$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| K24 | 528 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),K$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| L24 | 169 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),L$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| M24 | 306 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),M$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| N24 | 693 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),N$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| O24 | 413 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),O$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| P24 | 621 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),P$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| Q24 | 836 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A24&amp;"'!"&amp;$B24&amp;":"&amp;$B24),Q$5,INDIRECT("'"&amp;$A24&amp;"'!"&amp;$C24&amp;":"&amp;$C24),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "1"}] |
| R24 | 5183 | =SUM(D24:Q24) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S24 | 0 | =COUNTIF(D24:Q24,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 25

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A25 | ID33 |  |
| B25 | C |  |
| C25 | D |  |
| D25 | 86 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),D$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),D$6),0) [OOXML {"t": "shared", "ref": "D25:Q35", "ca": "1", "si": "4"}] |
| E25 | 86 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),E$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F25 | 74 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),F$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G25 | 49 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),G$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H25 | 57 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),H$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I25 | 13 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),I$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K25 | 97 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),K$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L25 | 43 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),L$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M25 | 85 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),M$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N25 | 98 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),N$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O25 | 86 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),O$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P25 | 135 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),P$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q25 | 141 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A25&amp;"'!"&amp;$B25&amp;":"&amp;$B25),Q$5,INDIRECT("'"&amp;$A25&amp;"'!"&amp;$C25&amp;":"&amp;$C25),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R25 | 1050 | =SUM(D25:Q25) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S25 | 0 | =COUNTIF(D25:Q25,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 26

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A26 | ID34 |  |
| B26 | C |  |
| C26 | D |  |
| D26 | 440 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),D$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E26 | 290 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),E$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F26 | 288 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),F$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G26 | 244 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),G$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H26 | 235 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),H$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I26 | 120 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),I$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K26 | 528 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),K$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L26 | 169 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),L$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M26 | 306 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),M$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N26 | 693 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),N$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O26 | 413 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),O$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P26 | 621 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),P$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q26 | 836 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A26&amp;"'!"&amp;$B26&amp;":"&amp;$B26),Q$5,INDIRECT("'"&amp;$A26&amp;"'!"&amp;$C26&amp;":"&amp;$C26),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R26 | 5183 | =SUM(D26:Q26) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S26 | 0 | =COUNTIF(D26:Q26,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 27

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A27 | ID35 |  |
| B27 | C |  |
| C27 | D |  |
| D27 | 59 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),D$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E27 | 46 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),E$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F27 | 48 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),F$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G27 | 24 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),G$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H27 | 35 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),H$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I27 | 8 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),I$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K27 | 33 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),K$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L27 | 9 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),L$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M27 | 34 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),M$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N27 | 13 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),N$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O27 | 19 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),O$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P27 | 58 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),P$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q27 | 69 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A27&amp;"'!"&amp;$B27&amp;":"&amp;$B27),Q$5,INDIRECT("'"&amp;$A27&amp;"'!"&amp;$C27&amp;":"&amp;$C27),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R27 | 455 | =SUM(D27:Q27) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S27 | 0 | =COUNTIF(D27:Q27,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 28

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A28 | ID_37_38 |  |
| B28 | C |  |
| C28 | D |  |
| D28 | 880 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),D$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E28 | 580 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),E$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F28 | 576 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),F$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G28 | 488 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),G$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H28 | 470 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),H$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I28 | 240 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),I$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K28 | 1056 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),K$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L28 | 338 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),L$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M28 | 612 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),M$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N28 | 1386 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),N$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O28 | 826 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),O$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P28 | 1242 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),P$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q28 | 1672 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A28&amp;"'!"&amp;$B28&amp;":"&amp;$B28),Q$5,INDIRECT("'"&amp;$A28&amp;"'!"&amp;$C28&amp;":"&amp;$C28),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R28 | 10366 | =SUM(D28:Q28) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S28 | 0 | =COUNTIF(D28:Q28,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 29

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A29 | ID39 |  |
| B29 | C |  |
| C29 | D |  |
| D29 | 440 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),D$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E29 | 290 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),E$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F29 | 288 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),F$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G29 | 244 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),G$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H29 | 235 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),H$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I29 | 120 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),I$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K29 | 528 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),K$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L29 | 169 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),L$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M29 | 306 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),M$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N29 | 693 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),N$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O29 | 413 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),O$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P29 | 621 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),P$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q29 | 836 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A29&amp;"'!"&amp;$B29&amp;":"&amp;$B29),Q$5,INDIRECT("'"&amp;$A29&amp;"'!"&amp;$C29&amp;":"&amp;$C29),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R29 | 5183 | =SUM(D29:Q29) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S29 | 0 | =COUNTIF(D29:Q29,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 30

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A30 | ID40 |  |
| B30 | C |  |
| C30 | D |  |
| D30 | 440 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),D$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E30 | 290 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),E$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F30 | 288 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),F$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G30 | 244 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),G$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H30 | 235 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),H$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I30 | 120 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),I$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K30 | 528 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),K$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L30 | 169 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),L$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M30 | 306 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),M$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N30 | 693 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),N$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O30 | 413 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),O$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P30 | 621 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),P$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q30 | 836 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A30&amp;"'!"&amp;$B30&amp;":"&amp;$B30),Q$5,INDIRECT("'"&amp;$A30&amp;"'!"&amp;$C30&amp;":"&amp;$C30),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R30 | 5183 | =SUM(D30:Q30) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S30 | 0 | =COUNTIF(D30:Q30,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 31

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A31 | ID_42 |  |
| B31 | C |  |
| C31 | D |  |
| D31 | 440 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),D$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E31 | 290 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),E$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F31 | 288 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),F$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G31 | 244 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),G$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H31 | 235 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),H$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I31 | 120 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),I$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K31 | 528 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),K$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L31 | 169 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),L$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M31 | 306 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),M$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N31 | 693 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),N$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O31 | 413 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),O$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P31 | 621 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),P$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q31 | 836 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A31&amp;"'!"&amp;$B31&amp;":"&amp;$B31),Q$5,INDIRECT("'"&amp;$A31&amp;"'!"&amp;$C31&amp;":"&amp;$C31),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R31 | 5183 | =SUM(D31:Q31) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S31 | 0 | =COUNTIF(D31:Q31,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 32

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A32 | ID_43 |  |
| B32 | C |  |
| C32 | D |  |
| D32 | 86 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),D$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E32 | 81 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),E$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F32 | 74 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),F$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G32 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),G$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H32 | 57 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),H$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I32 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),I$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K32 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),K$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L32 | 43 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),L$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M32 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),M$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N32 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),N$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O32 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),O$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P32 | 135 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),P$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q32 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A32&amp;"'!"&amp;$B32&amp;":"&amp;$B32),Q$5,INDIRECT("'"&amp;$A32&amp;"'!"&amp;$C32&amp;":"&amp;$C32),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R32 | 476 | =SUM(D32:Q32) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S32 | 7 | =COUNTIF(D32:Q32,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |
| T32 | O (데이터셋 수급 예정 - CNX 수기수집 중) |  |

## Row 33

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A33 | ID_44 |  |
| B33 | C |  |
| C33 | D |  |
| D33 | 440 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),D$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E33 | 290 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),E$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F33 | 288 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),F$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G33 | 244 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),G$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H33 | 235 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),H$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I33 | 120 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),I$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K33 | 528 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),K$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L33 | 169 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),L$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M33 | 306 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),M$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N33 | 693 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),N$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O33 | 413 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),O$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P33 | 621 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),P$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q33 | 836 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A33&amp;"'!"&amp;$B33&amp;":"&amp;$B33),Q$5,INDIRECT("'"&amp;$A33&amp;"'!"&amp;$C33&amp;":"&amp;$C33),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R33 | 5183 | =SUM(D33:Q33) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S33 | 0 | =COUNTIF(D33:Q33,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 34

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A34 | ID45 |  |
| B34 | C |  |
| C34 | D |  |
| D34 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),D$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E34 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),E$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F34 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),F$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G34 | 28 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),G$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H34 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),H$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I34 | 11 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),I$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K34 | 66 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),K$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L34 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),L$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M34 | 65 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),M$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N34 | 50 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),N$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O34 | 56 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),O$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P34 | 0 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),P$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q34 | 106 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A34&amp;"'!"&amp;$B34&amp;":"&amp;$B34),Q$5,INDIRECT("'"&amp;$A34&amp;"'!"&amp;$C34&amp;":"&amp;$C34),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R34 | 382 | =SUM(D34:Q34) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S34 | 6 | =COUNTIF(D34:Q34,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |
| T34 | Flixmedia 연동 리테일러는 진단 대상에서 제외 |  |

## Row 35

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A35 | ID46 |  |
| B35 | C |  |
| C35 | D |  |
| D35 | 440 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),D$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),D$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| E35 | 290 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),E$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),E$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| F35 | 288 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),F$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),F$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| G35 | 244 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),G$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),G$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| H35 | 235 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),H$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),H$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| I35 | 120 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),I$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),I$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| K35 | 528 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),K$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),K$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| L35 | 169 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),L$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),L$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| M35 | 306 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),M$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),M$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| N35 | 693 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),N$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),N$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| O35 | 413 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),O$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),O$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| P35 | 621 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),P$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),P$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| Q35 | 836 | =IFERROR(COUNTIFS(INDIRECT("'"&amp;$A35&amp;"'!"&amp;$B35&amp;":"&amp;$B35),Q$5,INDIRECT("'"&amp;$A35&amp;"'!"&amp;$C35&amp;":"&amp;$C35),Q$6),0) [OOXML {"t": "shared", "ca": "1", "si": "4"}] |
| R35 | 5183 | =SUM(D35:Q35) [OOXML {"t": "shared", "ca": "1", "si": "2"}] |
| S35 | 0 | =COUNTIF(D35:Q35,0) [OOXML {"t": "shared", "ca": "1", "si": "3"}] |

## Row 36

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A36 | 합계 (Null 개수) |  |
| D36 | 5 | =COUNTIF(D8:D35,0) [OOXML {"ca": "1"}] |
| E36 | 1 | =COUNTIF(E8:E35,0) [OOXML {"t": "shared", "ref": "E36:Q36", "ca": "1", "si": "5"}] |
| F36 | 1 | =COUNTIF(F8:F35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| G36 | 2 | =COUNTIF(G8:G35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| H36 | 2 | =COUNTIF(H8:H35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| I36 | 1 | =COUNTIF(I8:I35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| K36 | 1 | =COUNTIF(K8:K35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| L36 | 2 | =COUNTIF(L8:L35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| M36 | 1 | =COUNTIF(M8:M35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| N36 | 5 | =COUNTIF(N8:N35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| O36 | 5 | =COUNTIF(O8:O35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| P36 | 1 | =COUNTIF(P8:P35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| Q36 | 1 | =COUNTIF(Q8:Q35,0) [OOXML {"t": "shared", "ca": "1", "si": "5"}] |
| S36 | 28 | =SUM(D36:Q36) [OOXML {"ca": "1"}] |

## Row 40

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A40 | 【Brand = "LG" 필터】 국가 · 리테일러별 ID 진단항목 데이터 누락(Null) 판정 매트릭스 |  |

## Row 41

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A41 | 각 셀 = 해당 ID 시트에서 Brand 속성값이 "LG"인 행 수. 0 = LG 데이터 누락(Null) |  |

## Row 42

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A42 | ▼ 축 정의 (상단 블록 참조) |  |
| D42 | Spain | =D3 |
| F42 | Italy | =F3 |
| I42 | Netherlands | =I3 |
| K42 | Sweden | =K3 |
| L42 | France | =L3 |
| N42 | Poland | =N3 |
| P42 | Czech Republic | =P3 |
| R42 | 합계 |  |
| S42 | 누락 |  |
| T42 | Brand |  |

## Row 43

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| D43 | ECI | =D$4 [OOXML {"t": "shared", "ref": "D43:I43", "si": "6"}] |
| E43 | Media Markt | =E$4 [OOXML {"t": "shared", "si": "6"}] |
| F43 | Media World | =F$4 [OOXML {"t": "shared", "si": "6"}] |
| G43 | Amazon | =G$4 [OOXML {"t": "shared", "si": "6"}] |
| H43 | Unieuro | =H$4 [OOXML {"t": "shared", "si": "6"}] |
| I43 | Coolblue | =I$4 [OOXML {"t": "shared", "si": "6"}] |
| J43 | Media Markt |  |
| K43 | ELGIGANTEN | =K$4 [OOXML {"t": "shared", "ref": "K43:Q43", "si": "7"}] |
| L43 | Darty | =L$4 [OOXML {"t": "shared", "si": "7"}] |
| M43 | Boulanger | =M$4 [OOXML {"t": "shared", "si": "7"}] |
| N43 | Media Expert | =N$4 [OOXML {"t": "shared", "si": "7"}] |
| O43 | RTV EURO AGD | =O$4 [OOXML {"t": "shared", "si": "7"}] |
| P43 | Datart | =P$4 [OOXML {"t": "shared", "si": "7"}] |
| Q43 | Alza | =Q$4 [OOXML {"t": "shared", "si": "7"}] |
| R43 | LG 행수 |  |
| S43 | Null 개수 |  |
| T43 | Brand 열 |  |

## Row 44

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A44 | [Helper] 국가 매칭 패턴 |  |
| D44 | Spain | =D$5 [OOXML {"t": "shared", "ref": "D44:I44", "si": "8"}] |
| E44 | Spain | =E$5 [OOXML {"t": "shared", "si": "8"}] |
| F44 | Italy | =F$5 [OOXML {"t": "shared", "si": "8"}] |
| G44 | Italy | =G$5 [OOXML {"t": "shared", "si": "8"}] |
| H44 | Italy | =H$5 [OOXML {"t": "shared", "si": "8"}] |
| I44 | Netherlands | =I$5 [OOXML {"t": "shared", "si": "8"}] |
| J44 | Netherlands |  |
| K44 | Sweden | =K$5 [OOXML {"t": "shared", "ref": "K44:Q44", "si": "9"}] |
| L44 | France | =L$5 [OOXML {"t": "shared", "si": "9"}] |
| M44 | France | =M$5 [OOXML {"t": "shared", "si": "9"}] |
| N44 | Poland | =N$5 [OOXML {"t": "shared", "si": "9"}] |
| O44 | Poland | =O$5 [OOXML {"t": "shared", "si": "9"}] |
| P44 | Czech* | =P$5 [OOXML {"t": "shared", "si": "9"}] |
| Q44 | Czech* | =Q$5 [OOXML {"t": "shared", "si": "9"}] |

## Row 45

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A45 | [Helper] 리테일러 매칭 패턴 |  |
| D45 | Elcorteingles* | =D$6 [OOXML {"t": "shared", "ref": "D45:I45", "si": "10"}] |
| E45 | Media*Markt | =E$6 [OOXML {"t": "shared", "si": "10"}] |
| F45 | Mediaworld | =F$6 [OOXML {"t": "shared", "si": "10"}] |
| G45 | Amazon | =G$6 [OOXML {"t": "shared", "si": "10"}] |
| H45 | Unieuro | =H$6 [OOXML {"t": "shared", "si": "10"}] |
| I45 | Coolblue | =I$6 [OOXML {"t": "shared", "si": "10"}] |
| J45 | Media*Markt |  |
| K45 | Elgiganten | =K$6 [OOXML {"t": "shared", "ref": "K45:Q45", "si": "11"}] |
| L45 | Darty | =L$6 [OOXML {"t": "shared", "si": "11"}] |
| M45 | Boulanger | =M$6 [OOXML {"t": "shared", "si": "11"}] |
| N45 | Media*Expert | =N$6 [OOXML {"t": "shared", "si": "11"}] |
| O45 | Rtv*Euro*Agd | =O$6 [OOXML {"t": "shared", "si": "11"}] |
| P45 | Datart | =P$6 [OOXML {"t": "shared", "si": "11"}] |
| Q45 | Alza | =Q$6 [OOXML {"t": "shared", "si": "11"}] |

## Row 46

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A46 | ID 시트 |  |
| B46 | 국가 열 |  |
| C46 | 리테일러 열 |  |

## Row 47

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A47 | ID1 | =A8 |
| B47 | C | =B8 |
| C47 | D | =C8 |
| D47 | 96 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),D$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),D$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),D$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),D$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ref": "D47:I56", "ca": "1", "si": "12"}] |
| E47 | 102 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),E$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),E$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),E$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),E$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F47 | 53 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),F$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),F$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),F$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),F$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G47 | 67 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),G$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),G$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),G$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),G$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H47 | 63 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),H$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),H$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),H$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),H$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I47 | 37 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),I$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),I$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),I$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),I$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K47 | 59 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),K$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),K$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),K$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),K$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ref": "K47:Q56", "ca": "1", "si": "13"}] |
| L47 | 55 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),L$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),L$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),L$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),L$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M47 | 71 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),M$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),M$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),M$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),M$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N47 | 52 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),N$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),N$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),N$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),N$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O47 | 71 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),O$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),O$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),O$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),O$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P47 | 85 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),P$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),P$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),P$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),P$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q47 | 155 | =IFERROR(IF($T47="",COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),Q$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),Q$45),COUNTIFS(INDIRECT("'"&amp;$A47&amp;"'!"&amp;$B47&amp;":"&amp;$B47),Q$44,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$C47&amp;":"&amp;$C47),Q$45,INDIRECT("'"&amp;$A47&amp;"'!"&amp;$T47&amp;":"&amp;$T47),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R47 | 966 | =SUM(D47:Q47) [OOXML {"ca": "1"}] |
| S47 | 0 | =COUNTIF(D47:Q47,0) [OOXML {"ca": "1"}] |
| T47 | F |  |

## Row 48

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A48 | ID2 | =A9 [OOXML {"t": "shared", "ref": "A48:C48", "si": "14"}] |
| B48 | C | =B9 [OOXML {"t": "shared", "si": "14"}] |
| C48 | D | =C9 [OOXML {"t": "shared", "si": "14"}] |
| D48 | 15 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),D$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),D$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),D$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),D$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| E48 | 21 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),E$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),E$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),E$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),E$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F48 | 13 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),F$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),F$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),F$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),F$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G48 | 8 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),G$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),G$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),G$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),G$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H48 | 17 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),H$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),H$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),H$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),H$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I48 | 8 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),I$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),I$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),I$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),I$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K48 | 23 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),K$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),K$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),K$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),K$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| L48 | 10 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),L$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),L$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),L$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),L$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M48 | 18 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),M$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),M$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),M$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),M$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N48 | 15 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),N$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),N$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),N$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),N$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O48 | 17 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),O$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),O$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),O$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),O$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P48 | 33 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),P$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),P$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),P$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),P$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q48 | 47 | =IFERROR(IF($T48="",COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),Q$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),Q$45),COUNTIFS(INDIRECT("'"&amp;$A48&amp;"'!"&amp;$B48&amp;":"&amp;$B48),Q$44,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$C48&amp;":"&amp;$C48),Q$45,INDIRECT("'"&amp;$A48&amp;"'!"&amp;$T48&amp;":"&amp;$T48),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R48 | 245 | =SUM(D48:Q48) [OOXML {"t": "shared", "ref": "R48:R74", "ca": "1", "si": "15"}] |
| S48 | 0 | =COUNTIF(D48:Q48,0) [OOXML {"t": "shared", "ref": "S48:S74", "ca": "1", "si": "16"}] |
| T48 | F |  |

## Row 49

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A49 | ID3 | =A10 [OOXML {"t": "shared", "ref": "A49:C49", "si": "17"}] |
| B49 | C | =B10 [OOXML {"t": "shared", "si": "17"}] |
| C49 | D | =C10 [OOXML {"t": "shared", "si": "17"}] |
| D49 | 17 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),D$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),D$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),D$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),D$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| E49 | 27 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),E$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),E$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),E$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),E$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F49 | 6 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),F$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),F$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),F$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),F$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G49 | 0 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),G$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),G$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),G$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),G$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H49 | 14 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),H$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),H$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),H$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),H$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I49 | 6 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),I$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),I$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),I$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),I$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K49 | 16 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),K$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),K$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),K$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),K$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| L49 | 14 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),L$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),L$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),L$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),L$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M49 | 16 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),M$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),M$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),M$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),M$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N49 | 12 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),N$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),N$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),N$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),N$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O49 | 14 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),O$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),O$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),O$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),O$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P49 | 20 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),P$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),P$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),P$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),P$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q49 | 28 | =IFERROR(IF($T49="",COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),Q$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),Q$45),COUNTIFS(INDIRECT("'"&amp;$A49&amp;"'!"&amp;$B49&amp;":"&amp;$B49),Q$44,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$C49&amp;":"&amp;$C49),Q$45,INDIRECT("'"&amp;$A49&amp;"'!"&amp;$T49&amp;":"&amp;$T49),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R49 | 190 | =SUM(D49:Q49) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S49 | 1 | =COUNTIF(D49:Q49,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T49 | F |  |

## Row 50

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A50 | ID4 | =A11 [OOXML {"t": "shared", "ref": "A50:C50", "si": "18"}] |
| B50 | C | =B11 [OOXML {"t": "shared", "si": "18"}] |
| C50 | D | =C11 [OOXML {"t": "shared", "si": "18"}] |
| D50 | 24 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),D$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),D$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),D$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),D$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| E50 | 24 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),E$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),E$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),E$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),E$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F50 | 18 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),F$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),F$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),F$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),F$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G50 | 18 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),G$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),G$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),G$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),G$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H50 | 18 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),H$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),H$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),H$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),H$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I50 | 14 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),I$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),I$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),I$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),I$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K50 | 18 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),K$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),K$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),K$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),K$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| L50 | 18 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),L$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),L$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),L$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),L$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M50 | 18 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),M$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),M$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),M$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),M$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N50 | 20 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),N$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),N$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),N$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),N$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O50 | 22 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),O$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),O$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),O$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),O$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P50 | 18 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),P$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),P$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),P$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),P$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q50 | 18 | =IFERROR(IF($T50="",COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),Q$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),Q$45),COUNTIFS(INDIRECT("'"&amp;$A50&amp;"'!"&amp;$B50&amp;":"&amp;$B50),Q$44,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$C50&amp;":"&amp;$C50),Q$45,INDIRECT("'"&amp;$A50&amp;"'!"&amp;$T50&amp;":"&amp;$T50),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R50 | 248 | =SUM(D50:Q50) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S50 | 0 | =COUNTIF(D50:Q50,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T50 | F |  |

## Row 51

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A51 | ID7 | =A12 [OOXML {"t": "shared", "ref": "A51:C51", "si": "19"}] |
| B51 | D | =B12 [OOXML {"t": "shared", "si": "19"}] |
| C51 | F | =C12 [OOXML {"t": "shared", "si": "19"}] |
| D51 | 8 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),D$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),D$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),D$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),D$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| E51 | 8 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),E$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),E$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),E$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),E$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F51 | 6 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),F$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),F$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),F$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),F$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G51 | 6 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),G$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),G$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),G$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),G$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H51 | 6 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),H$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),H$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),H$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),H$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I51 | 6 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),I$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),I$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),I$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),I$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K51 | 6 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),K$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),K$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),K$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),K$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| L51 | 6 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),L$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),L$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),L$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),L$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M51 | 6 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),M$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),M$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),M$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),M$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N51 | 6 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),N$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),N$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),N$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),N$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O51 | 6 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),O$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),O$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),O$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),O$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P51 | 4 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),P$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),P$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),P$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),P$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q51 | 4 | =IFERROR(IF($T51="",COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),Q$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),Q$45),COUNTIFS(INDIRECT("'"&amp;$A51&amp;"'!"&amp;$B51&amp;":"&amp;$B51),Q$44,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$C51&amp;":"&amp;$C51),Q$45,INDIRECT("'"&amp;$A51&amp;"'!"&amp;$T51&amp;":"&amp;$T51),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R51 | 78 | =SUM(D51:Q51) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S51 | 0 | =COUNTIF(D51:Q51,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T51 | B |  |

## Row 52

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A52 | ID8 | =A13 [OOXML {"t": "shared", "ref": "A52:C52", "si": "20"}] |
| B52 | C | =B13 [OOXML {"t": "shared", "si": "20"}] |
| C52 | D | =C13 [OOXML {"t": "shared", "si": "20"}] |
| D52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),D$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),D$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),D$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),D$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| E52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),E$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),E$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),E$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),E$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),F$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),F$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),F$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),F$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),G$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),G$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),G$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),G$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),H$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),H$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),H$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),H$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),I$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),I$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),I$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),I$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),K$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),K$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),K$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),K$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| L52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),L$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),L$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),L$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),L$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),M$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),M$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),M$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),M$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),N$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),N$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),N$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),N$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),O$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),O$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),O$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),O$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),P$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),P$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),P$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),P$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q52 | 0 | =IFERROR(IF($T52="",COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),Q$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),Q$45),COUNTIFS(INDIRECT("'"&amp;$A52&amp;"'!"&amp;$B52&amp;":"&amp;$B52),Q$44,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$C52&amp;":"&amp;$C52),Q$45,INDIRECT("'"&amp;$A52&amp;"'!"&amp;$T52&amp;":"&amp;$T52),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R52 | 0 | =SUM(D52:Q52) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S52 | 13 | =COUNTIF(D52:Q52,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T52 | G |  |

## Row 53

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A53 | ID9 | =A14 [OOXML {"t": "shared", "ref": "A53:C53", "si": "21"}] |
| B53 | C | =B14 [OOXML {"t": "shared", "si": "21"}] |
| C53 | D | =C14 [OOXML {"t": "shared", "si": "21"}] |
| D53 | 0 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),D$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),D$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),D$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),D$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| E53 | 17 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),E$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),E$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),E$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),E$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F53 | 17 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),F$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),F$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),F$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),F$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G53 | 25 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),G$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),G$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),G$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),G$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H53 | 2 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),H$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),H$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),H$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),H$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I53 | 17 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),I$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),I$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),I$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),I$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K53 | 12 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),K$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),K$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),K$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),K$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| L53 | 2 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),L$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),L$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),L$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),L$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M53 | 11 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),M$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),M$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),M$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),M$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N53 | 0 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),N$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),N$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),N$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),N$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O53 | 0 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),O$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),O$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),O$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),O$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P53 | 22 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),P$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),P$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),P$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),P$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q53 | 21 | =IFERROR(IF($T53="",COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),Q$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),Q$45),COUNTIFS(INDIRECT("'"&amp;$A53&amp;"'!"&amp;$B53&amp;":"&amp;$B53),Q$44,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$C53&amp;":"&amp;$C53),Q$45,INDIRECT("'"&amp;$A53&amp;"'!"&amp;$T53&amp;":"&amp;$T53),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R53 | 146 | =SUM(D53:Q53) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S53 | 3 | =COUNTIF(D53:Q53,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |

## Row 54

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A54 | ID10 | =A15 [OOXML {"t": "shared", "ref": "A54:C54", "si": "22"}] |
| B54 | C | =B15 [OOXML {"t": "shared", "si": "22"}] |
| C54 | D | =C15 [OOXML {"t": "shared", "si": "22"}] |
| D54 | 0 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),D$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),D$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),D$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),D$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| E54 | 51 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),E$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),E$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),E$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),E$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F54 | 51 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),F$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),F$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),F$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),F$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G54 | 75 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),G$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),G$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),G$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),G$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H54 | 5 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),H$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),H$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),H$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),H$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I54 | 51 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),I$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),I$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),I$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),I$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K54 | 36 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),K$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),K$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),K$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),K$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| L54 | 6 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),L$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),L$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),L$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),L$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M54 | 33 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),M$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),M$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),M$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),M$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N54 | 0 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),N$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),N$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),N$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),N$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O54 | 0 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),O$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),O$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),O$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),O$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P54 | 66 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),P$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),P$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),P$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),P$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q54 | 63 | =IFERROR(IF($T54="",COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),Q$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),Q$45),COUNTIFS(INDIRECT("'"&amp;$A54&amp;"'!"&amp;$B54&amp;":"&amp;$B54),Q$44,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$C54&amp;":"&amp;$C54),Q$45,INDIRECT("'"&amp;$A54&amp;"'!"&amp;$T54&amp;":"&amp;$T54),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R54 | 437 | =SUM(D54:Q54) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S54 | 3 | =COUNTIF(D54:Q54,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |

## Row 55

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A55 | ID11 | =A16 [OOXML {"t": "shared", "ref": "A55:C55", "si": "23"}] |
| B55 | C | =B16 [OOXML {"t": "shared", "si": "23"}] |
| C55 | D | =C16 [OOXML {"t": "shared", "si": "23"}] |
| D55 | 33 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),D$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),D$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),D$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),D$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| E55 | 33 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),E$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),E$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),E$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),E$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F55 | 27 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),F$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),F$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),F$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),F$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G55 | 25 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),G$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),G$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),G$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),G$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H55 | 27 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),H$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),H$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),H$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),H$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I55 | 19 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),I$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),I$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),I$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),I$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K55 | 26 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),K$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),K$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),K$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),K$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| L55 | 27 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),L$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),L$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),L$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),L$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M55 | 26 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),M$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),M$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),M$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),M$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N55 | 24 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),N$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),N$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),N$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),N$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O55 | 31 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),O$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),O$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),O$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),O$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P55 | 27 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),P$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),P$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),P$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),P$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q55 | 27 | =IFERROR(IF($T55="",COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),Q$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),Q$45),COUNTIFS(INDIRECT("'"&amp;$A55&amp;"'!"&amp;$B55&amp;":"&amp;$B55),Q$44,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$C55&amp;":"&amp;$C55),Q$45,INDIRECT("'"&amp;$A55&amp;"'!"&amp;$T55&amp;":"&amp;$T55),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R55 | 352 | =SUM(D55:Q55) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S55 | 0 | =COUNTIF(D55:Q55,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T55 | F |  |

## Row 56

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A56 | ID12 | =A17 [OOXML {"t": "shared", "ref": "A56:C56", "si": "24"}] |
| B56 | C | =B17 [OOXML {"t": "shared", "si": "24"}] |
| C56 | D | =C17 [OOXML {"t": "shared", "si": "24"}] |
| D56 | 1076 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),D$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),D$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),D$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),D$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| E56 | 1078 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),E$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),E$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),E$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),E$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| F56 | 920 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),F$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),F$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),F$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),F$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| G56 | 306 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),G$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),G$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),G$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),G$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| H56 | 601 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),H$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),H$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),H$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),H$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| I56 | 169 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),I$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),I$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),I$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),I$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "12"}] |
| K56 | 555 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),K$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),K$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),K$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),K$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| L56 | 170 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),L$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),L$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),L$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),L$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| M56 | 723 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),M$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),M$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),M$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),M$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| N56 | 492 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),N$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),N$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),N$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),N$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| O56 | 1024 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),O$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),O$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),O$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),O$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| P56 | 1486 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),P$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),P$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),P$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),P$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| Q56 | 1583 | =IFERROR(IF($T56="",COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),Q$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),Q$45),COUNTIFS(INDIRECT("'"&amp;$A56&amp;"'!"&amp;$B56&amp;":"&amp;$B56),Q$44,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$C56&amp;":"&amp;$C56),Q$45,INDIRECT("'"&amp;$A56&amp;"'!"&amp;$T56&amp;":"&amp;$T56),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "13"}] |
| R56 | 10183 | =SUM(D56:Q56) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S56 | 0 | =COUNTIF(D56:Q56,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T56 | F |  |

## Row 57

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A57 | ID13 | =A18 [OOXML {"t": "shared", "ref": "A57:C57", "si": "25"}] |
| B57 | C | =B18 [OOXML {"t": "shared", "si": "25"}] |
| C57 | D | =C18 [OOXML {"t": "shared", "si": "25"}] |
| D57 | 86 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),D$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),D$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),D$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),D$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ref": "D57:I66", "ca": "1", "si": "26"}] |
| E57 | 86 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),E$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),E$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),E$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),E$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F57 | 74 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),F$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),F$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),F$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),F$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G57 | 49 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),G$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),G$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),G$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),G$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H57 | 57 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),H$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),H$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),H$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),H$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I57 | 13 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),I$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),I$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),I$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),I$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K57 | 97 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),K$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),K$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),K$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),K$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ref": "K57:Q66", "ca": "1", "si": "27"}] |
| L57 | 43 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),L$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),L$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),L$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),L$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M57 | 85 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),M$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),M$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),M$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),M$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N57 | 98 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),N$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),N$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),N$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),N$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O57 | 86 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),O$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),O$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),O$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),O$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P57 | 135 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),P$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),P$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),P$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),P$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q57 | 141 | =IFERROR(IF($T57="",COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),Q$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),Q$45),COUNTIFS(INDIRECT("'"&amp;$A57&amp;"'!"&amp;$B57&amp;":"&amp;$B57),Q$44,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$C57&amp;":"&amp;$C57),Q$45,INDIRECT("'"&amp;$A57&amp;"'!"&amp;$T57&amp;":"&amp;$T57),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R57 | 1050 | =SUM(D57:Q57) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S57 | 0 | =COUNTIF(D57:Q57,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T57 | F |  |

## Row 58

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A58 | ID14 | =A19 [OOXML {"t": "shared", "ref": "A58:C58", "si": "28"}] |
| B58 | C | =B19 [OOXML {"t": "shared", "si": "28"}] |
| C58 | D | =C19 [OOXML {"t": "shared", "si": "28"}] |
| D58 | 287 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),D$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),D$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),D$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),D$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| E58 | 167 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),E$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),E$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),E$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),E$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F58 | 177 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),F$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),F$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),F$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),F$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G58 | 203 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),G$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),G$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),G$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),G$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H58 | 59 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),H$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),H$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),H$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),H$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I58 | 60 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),I$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),I$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),I$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),I$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K58 | 447 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),K$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),K$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),K$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),K$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| L58 | 487 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),L$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),L$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),L$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),L$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M58 | 170 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),M$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),M$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),M$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),M$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N58 | 228 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),N$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),N$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),N$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),N$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O58 | 212 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),O$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),O$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),O$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),O$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P58 | 504 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),P$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),P$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),P$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),P$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q58 | 722 | =IFERROR(IF($T58="",COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),Q$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),Q$45),COUNTIFS(INDIRECT("'"&amp;$A58&amp;"'!"&amp;$B58&amp;":"&amp;$B58),Q$44,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$C58&amp;":"&amp;$C58),Q$45,INDIRECT("'"&amp;$A58&amp;"'!"&amp;$T58&amp;":"&amp;$T58),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R58 | 3723 | =SUM(D58:Q58) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S58 | 0 | =COUNTIF(D58:Q58,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T58 | F |  |

## Row 59

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A59 | ID15 | =A20 [OOXML {"t": "shared", "ref": "A59:C59", "si": "29"}] |
| B59 | C | =B20 [OOXML {"t": "shared", "si": "29"}] |
| C59 | D | =C20 [OOXML {"t": "shared", "si": "29"}] |
| D59 | 87 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),D$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),D$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),D$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),D$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| E59 | 86 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),E$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),E$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),E$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),E$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F59 | 74 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),F$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),F$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),F$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),F$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G59 | 49 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),G$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),G$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),G$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),G$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H59 | 57 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),H$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),H$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),H$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),H$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I59 | 13 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),I$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),I$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),I$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),I$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K59 | 97 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),K$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),K$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),K$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),K$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| L59 | 43 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),L$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),L$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),L$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),L$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M59 | 88 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),M$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),M$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),M$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),M$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N59 | 98 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),N$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),N$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),N$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),N$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O59 | 86 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),O$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),O$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),O$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),O$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P59 | 135 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),P$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),P$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),P$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),P$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q59 | 148 | =IFERROR(IF($T59="",COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),Q$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),Q$45),COUNTIFS(INDIRECT("'"&amp;$A59&amp;"'!"&amp;$B59&amp;":"&amp;$B59),Q$44,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$C59&amp;":"&amp;$C59),Q$45,INDIRECT("'"&amp;$A59&amp;"'!"&amp;$T59&amp;":"&amp;$T59),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R59 | 1061 | =SUM(D59:Q59) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S59 | 0 | =COUNTIF(D59:Q59,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T59 | F |  |

## Row 60

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A60 | ID18_19_20_21_22_23 | =A21 [OOXML {"t": "shared", "ref": "A60:C60", "si": "30"}] |
| B60 | C | =B21 [OOXML {"t": "shared", "si": "30"}] |
| C60 | E | =C21 [OOXML {"t": "shared", "si": "30"}] |
| D60 | 0 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),D$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),D$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),D$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),D$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| E60 | 18 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),E$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),E$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),E$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),E$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F60 | 18 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),F$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),F$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),F$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),F$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G60 | 24 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),G$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),G$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),G$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),G$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H60 | 0 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),H$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),H$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),H$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),H$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I60 | 18 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),I$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),I$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),I$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),I$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K60 | 12 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),K$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),K$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),K$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),K$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| L60 | 0 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),L$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),L$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),L$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),L$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M60 | 12 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),M$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),M$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),M$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),M$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N60 | 0 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),N$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),N$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),N$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),N$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O60 | 0 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),O$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),O$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),O$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),O$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P60 | 12 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),P$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),P$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),P$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),P$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q60 | 18 | =IFERROR(IF($T60="",COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),Q$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),Q$45),COUNTIFS(INDIRECT("'"&amp;$A60&amp;"'!"&amp;$B60&amp;":"&amp;$B60),Q$44,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$C60&amp;":"&amp;$C60),Q$45,INDIRECT("'"&amp;$A60&amp;"'!"&amp;$T60&amp;":"&amp;$T60),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R60 | 132 | =SUM(D60:Q60) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S60 | 5 | =COUNTIF(D60:Q60,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T60 | D |  |

## Row 61

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A61 | ID24 | =A22 [OOXML {"t": "shared", "ref": "A61:C61", "si": "31"}] |
| B61 | C | =B22 [OOXML {"t": "shared", "si": "31"}] |
| C61 | D | =C22 [OOXML {"t": "shared", "si": "31"}] |
| D61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),D$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),D$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),D$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),D$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| E61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),E$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),E$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),E$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),E$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),F$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),F$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),F$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),F$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),G$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),G$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),G$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),G$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),H$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),H$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),H$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),H$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),I$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),I$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),I$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),I$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),K$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),K$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),K$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),K$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| L61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),L$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),L$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),L$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),L$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),M$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),M$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),M$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),M$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),N$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),N$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),N$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),N$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),O$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),O$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),O$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),O$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),P$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),P$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),P$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),P$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q61 | 0 | =IFERROR(IF($T61="",COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),Q$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),Q$45),COUNTIFS(INDIRECT("'"&amp;$A61&amp;"'!"&amp;$B61&amp;":"&amp;$B61),Q$44,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$C61&amp;":"&amp;$C61),Q$45,INDIRECT("'"&amp;$A61&amp;"'!"&amp;$T61&amp;":"&amp;$T61),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R61 | 0 | =SUM(D61:Q61) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S61 | 13 | =COUNTIF(D61:Q61,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T61 | G |  |

## Row 62

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A62 | ID25 | =A23 [OOXML {"t": "shared", "ref": "A62:C62", "si": "32"}] |
| B62 | C | =B23 [OOXML {"t": "shared", "si": "32"}] |
| C62 | D | =C23 [OOXML {"t": "shared", "si": "32"}] |
| D62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),D$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),D$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),D$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),D$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| E62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),E$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),E$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),E$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),E$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),F$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),F$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),F$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),F$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),G$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),G$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),G$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),G$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),H$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),H$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),H$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),H$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),I$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),I$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),I$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),I$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),K$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),K$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),K$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),K$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| L62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),L$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),L$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),L$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),L$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),M$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),M$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),M$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),M$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),N$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),N$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),N$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),N$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),O$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),O$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),O$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),O$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),P$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),P$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),P$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),P$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q62 | 0 | =IFERROR(IF($T62="",COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),Q$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),Q$45),COUNTIFS(INDIRECT("'"&amp;$A62&amp;"'!"&amp;$B62&amp;":"&amp;$B62),Q$44,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$C62&amp;":"&amp;$C62),Q$45,INDIRECT("'"&amp;$A62&amp;"'!"&amp;$T62&amp;":"&amp;$T62),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R62 | 0 | =SUM(D62:Q62) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S62 | 13 | =COUNTIF(D62:Q62,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T62 | G |  |

## Row 63

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A63 | ID_29 | =A24 [OOXML {"t": "shared", "ref": "A63:C63", "si": "33"}] |
| B63 | C | =B24 [OOXML {"t": "shared", "si": "33"}] |
| C63 | D | =C24 [OOXML {"t": "shared", "si": "33"}] |
| D63 | 86 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),D$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),D$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),D$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),D$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| E63 | 86 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),E$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),E$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),E$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),E$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F63 | 74 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),F$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),F$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),F$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),F$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G63 | 49 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),G$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),G$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),G$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),G$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H63 | 57 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),H$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),H$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),H$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),H$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I63 | 13 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),I$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),I$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),I$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),I$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K63 | 97 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),K$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),K$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),K$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),K$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| L63 | 43 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),L$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),L$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),L$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),L$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M63 | 85 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),M$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),M$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),M$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),M$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N63 | 98 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),N$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),N$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),N$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),N$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O63 | 86 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),O$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),O$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),O$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),O$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P63 | 135 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),P$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),P$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),P$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),P$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q63 | 141 | =IFERROR(IF($T63="",COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),Q$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),Q$45),COUNTIFS(INDIRECT("'"&amp;$A63&amp;"'!"&amp;$B63&amp;":"&amp;$B63),Q$44,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$C63&amp;":"&amp;$C63),Q$45,INDIRECT("'"&amp;$A63&amp;"'!"&amp;$T63&amp;":"&amp;$T63),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R63 | 1050 | =SUM(D63:Q63) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S63 | 0 | =COUNTIF(D63:Q63,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T63 | F |  |

## Row 64

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A64 | ID33 | =A25 [OOXML {"t": "shared", "ref": "A64:C64", "si": "34"}] |
| B64 | C | =B25 [OOXML {"t": "shared", "si": "34"}] |
| C64 | D | =C25 [OOXML {"t": "shared", "si": "34"}] |
| D64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),D$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),D$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),D$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),D$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| E64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),E$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),E$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),E$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),E$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),F$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),F$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),F$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),F$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),G$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),G$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),G$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),G$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),H$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),H$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),H$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),H$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),I$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),I$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),I$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),I$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),K$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),K$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),K$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),K$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| L64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),L$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),L$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),L$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),L$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),M$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),M$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),M$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),M$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),N$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),N$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),N$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),N$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),O$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),O$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),O$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),O$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),P$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),P$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),P$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),P$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q64 | 0 | =IFERROR(IF($T64="",COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),Q$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),Q$45),COUNTIFS(INDIRECT("'"&amp;$A64&amp;"'!"&amp;$B64&amp;":"&amp;$B64),Q$44,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$C64&amp;":"&amp;$C64),Q$45,INDIRECT("'"&amp;$A64&amp;"'!"&amp;$T64&amp;":"&amp;$T64),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R64 | 0 | =SUM(D64:Q64) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S64 | 13 | =COUNTIF(D64:Q64,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T64 | G |  |

## Row 65

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A65 | ID34 | =A26 [OOXML {"t": "shared", "ref": "A65:C65", "si": "35"}] |
| B65 | C | =B26 [OOXML {"t": "shared", "si": "35"}] |
| C65 | D | =C26 [OOXML {"t": "shared", "si": "35"}] |
| D65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),D$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),D$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),D$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),D$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| E65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),E$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),E$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),E$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),E$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),F$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),F$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),F$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),F$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),G$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),G$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),G$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),G$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),H$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),H$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),H$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),H$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),I$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),I$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),I$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),I$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),K$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),K$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),K$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),K$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| L65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),L$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),L$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),L$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),L$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),M$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),M$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),M$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),M$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),N$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),N$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),N$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),N$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),O$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),O$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),O$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),O$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),P$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),P$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),P$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),P$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q65 | 0 | =IFERROR(IF($T65="",COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),Q$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),Q$45),COUNTIFS(INDIRECT("'"&amp;$A65&amp;"'!"&amp;$B65&amp;":"&amp;$B65),Q$44,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$C65&amp;":"&amp;$C65),Q$45,INDIRECT("'"&amp;$A65&amp;"'!"&amp;$T65&amp;":"&amp;$T65),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R65 | 0 | =SUM(D65:Q65) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S65 | 13 | =COUNTIF(D65:Q65,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T65 | G |  |

## Row 66

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A66 | ID35 | =A27 [OOXML {"t": "shared", "ref": "A66:C66", "si": "36"}] |
| B66 | C | =B27 [OOXML {"t": "shared", "si": "36"}] |
| C66 | D | =C27 [OOXML {"t": "shared", "si": "36"}] |
| D66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),D$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),D$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),D$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),D$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| E66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),E$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),E$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),E$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),E$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| F66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),F$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),F$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),F$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),F$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| G66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),G$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),G$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),G$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),G$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| H66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),H$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),H$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),H$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),H$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| I66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),I$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),I$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),I$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),I$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "26"}] |
| K66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),K$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),K$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),K$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),K$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| L66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),L$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),L$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),L$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),L$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| M66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),M$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),M$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),M$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),M$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| N66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),N$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),N$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),N$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),N$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| O66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),O$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),O$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),O$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),O$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| P66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),P$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),P$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),P$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),P$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| Q66 | 0 | =IFERROR(IF($T66="",COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),Q$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),Q$45),COUNTIFS(INDIRECT("'"&amp;$A66&amp;"'!"&amp;$B66&amp;":"&amp;$B66),Q$44,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$C66&amp;":"&amp;$C66),Q$45,INDIRECT("'"&amp;$A66&amp;"'!"&amp;$T66&amp;":"&amp;$T66),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "27"}] |
| R66 | 0 | =SUM(D66:Q66) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S66 | 13 | =COUNTIF(D66:Q66,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T66 | G |  |

## Row 67

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A67 | ID_37_38 | =A28 [OOXML {"t": "shared", "ref": "A67:C67", "si": "37"}] |
| B67 | C | =B28 [OOXML {"t": "shared", "si": "37"}] |
| C67 | D | =C28 [OOXML {"t": "shared", "si": "37"}] |
| D67 | 172 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),D$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),D$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),D$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),D$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ref": "D67:I74", "ca": "1", "si": "38"}] |
| E67 | 172 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),E$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),E$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),E$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),E$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| F67 | 148 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),F$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),F$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),F$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),F$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| G67 | 98 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),G$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),G$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),G$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),G$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| H67 | 114 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),H$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),H$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),H$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),H$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| I67 | 26 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),I$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),I$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),I$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),I$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| K67 | 194 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),K$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),K$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),K$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),K$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ref": "K67:Q74", "ca": "1", "si": "39"}] |
| L67 | 86 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),L$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),L$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),L$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),L$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| M67 | 170 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),M$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),M$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),M$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),M$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| N67 | 196 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),N$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),N$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),N$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),N$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| O67 | 172 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),O$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),O$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),O$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),O$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| P67 | 270 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),P$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),P$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),P$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),P$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| Q67 | 282 | =IFERROR(IF($T67="",COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),Q$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),Q$45),COUNTIFS(INDIRECT("'"&amp;$A67&amp;"'!"&amp;$B67&amp;":"&amp;$B67),Q$44,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$C67&amp;":"&amp;$C67),Q$45,INDIRECT("'"&amp;$A67&amp;"'!"&amp;$T67&amp;":"&amp;$T67),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| R67 | 2100 | =SUM(D67:Q67) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S67 | 0 | =COUNTIF(D67:Q67,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T67 | F |  |

## Row 68

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A68 | ID39 | =A29 [OOXML {"t": "shared", "ref": "A68:C68", "si": "40"}] |
| B68 | C | =B29 [OOXML {"t": "shared", "si": "40"}] |
| C68 | D | =C29 [OOXML {"t": "shared", "si": "40"}] |
| D68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),D$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),D$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),D$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),D$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| E68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),E$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),E$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),E$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),E$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| F68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),F$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),F$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),F$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),F$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| G68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),G$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),G$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),G$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),G$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| H68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),H$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),H$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),H$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),H$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| I68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),I$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),I$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),I$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),I$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| K68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),K$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),K$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),K$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),K$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| L68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),L$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),L$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),L$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),L$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| M68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),M$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),M$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),M$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),M$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| N68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),N$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),N$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),N$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),N$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| O68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),O$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),O$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),O$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),O$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| P68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),P$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),P$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),P$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),P$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| Q68 | 0 | =IFERROR(IF($T68="",COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),Q$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),Q$45),COUNTIFS(INDIRECT("'"&amp;$A68&amp;"'!"&amp;$B68&amp;":"&amp;$B68),Q$44,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$C68&amp;":"&amp;$C68),Q$45,INDIRECT("'"&amp;$A68&amp;"'!"&amp;$T68&amp;":"&amp;$T68),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| R68 | 0 | =SUM(D68:Q68) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S68 | 13 | =COUNTIF(D68:Q68,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T68 | G |  |

## Row 69

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A69 | ID40 | =A30 [OOXML {"t": "shared", "ref": "A69:C69", "si": "41"}] |
| B69 | C | =B30 [OOXML {"t": "shared", "si": "41"}] |
| C69 | D | =C30 [OOXML {"t": "shared", "si": "41"}] |
| D69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),D$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),D$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),D$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),D$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| E69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),E$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),E$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),E$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),E$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| F69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),F$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),F$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),F$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),F$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| G69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),G$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),G$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),G$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),G$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| H69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),H$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),H$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),H$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),H$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| I69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),I$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),I$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),I$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),I$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| K69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),K$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),K$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),K$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),K$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| L69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),L$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),L$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),L$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),L$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| M69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),M$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),M$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),M$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),M$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| N69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),N$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),N$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),N$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),N$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| O69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),O$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),O$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),O$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),O$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| P69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),P$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),P$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),P$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),P$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| Q69 | 0 | =IFERROR(IF($T69="",COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),Q$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),Q$45),COUNTIFS(INDIRECT("'"&amp;$A69&amp;"'!"&amp;$B69&amp;":"&amp;$B69),Q$44,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$C69&amp;":"&amp;$C69),Q$45,INDIRECT("'"&amp;$A69&amp;"'!"&amp;$T69&amp;":"&amp;$T69),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| R69 | 0 | =SUM(D69:Q69) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S69 | 13 | =COUNTIF(D69:Q69,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T69 | G |  |

## Row 70

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A70 | ID_42 | =A31 [OOXML {"t": "shared", "ref": "A70:C70", "si": "42"}] |
| B70 | C | =B31 [OOXML {"t": "shared", "si": "42"}] |
| C70 | D | =C31 [OOXML {"t": "shared", "si": "42"}] |
| D70 | 86 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),D$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),D$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),D$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),D$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| E70 | 86 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),E$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),E$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),E$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),E$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| F70 | 74 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),F$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),F$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),F$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),F$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| G70 | 49 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),G$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),G$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),G$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),G$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| H70 | 57 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),H$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),H$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),H$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),H$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| I70 | 13 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),I$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),I$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),I$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),I$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| K70 | 97 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),K$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),K$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),K$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),K$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| L70 | 43 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),L$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),L$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),L$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),L$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| M70 | 85 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),M$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),M$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),M$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),M$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| N70 | 98 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),N$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),N$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),N$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),N$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| O70 | 86 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),O$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),O$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),O$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),O$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| P70 | 135 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),P$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),P$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),P$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),P$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| Q70 | 141 | =IFERROR(IF($T70="",COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),Q$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),Q$45),COUNTIFS(INDIRECT("'"&amp;$A70&amp;"'!"&amp;$B70&amp;":"&amp;$B70),Q$44,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$C70&amp;":"&amp;$C70),Q$45,INDIRECT("'"&amp;$A70&amp;"'!"&amp;$T70&amp;":"&amp;$T70),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| R70 | 1050 | =SUM(D70:Q70) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S70 | 0 | =COUNTIF(D70:Q70,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T70 | F |  |

## Row 71

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A71 | ID_43 | =A32 [OOXML {"t": "shared", "ref": "A71:C71", "si": "43"}] |
| B71 | C | =B32 [OOXML {"t": "shared", "si": "43"}] |
| C71 | D | =C32 [OOXML {"t": "shared", "si": "43"}] |
| D71 | 86 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),D$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),D$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),D$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),D$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| E71 | 81 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),E$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),E$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),E$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),E$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| F71 | 74 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),F$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),F$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),F$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),F$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| G71 | 0 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),G$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),G$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),G$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),G$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| H71 | 57 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),H$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),H$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),H$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),H$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| I71 | 0 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),I$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),I$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),I$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),I$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| K71 | 0 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),K$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),K$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),K$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),K$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| L71 | 43 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),L$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),L$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),L$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),L$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| M71 | 0 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),M$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),M$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),M$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),M$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| N71 | 0 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),N$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),N$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),N$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),N$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| O71 | 0 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),O$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),O$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),O$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),O$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| P71 | 135 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),P$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),P$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),P$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),P$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| Q71 | 0 | =IFERROR(IF($T71="",COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),Q$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),Q$45),COUNTIFS(INDIRECT("'"&amp;$A71&amp;"'!"&amp;$B71&amp;":"&amp;$B71),Q$44,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$C71&amp;":"&amp;$C71),Q$45,INDIRECT("'"&amp;$A71&amp;"'!"&amp;$T71&amp;":"&amp;$T71),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| R71 | 476 | =SUM(D71:Q71) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S71 | 7 | =COUNTIF(D71:Q71,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T71 | F |  |

## Row 72

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A72 | ID_44 | =A33 [OOXML {"t": "shared", "ref": "A72:C72", "si": "44"}] |
| B72 | C | =B33 [OOXML {"t": "shared", "si": "44"}] |
| C72 | D | =C33 [OOXML {"t": "shared", "si": "44"}] |
| D72 | 86 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),D$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),D$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),D$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),D$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| E72 | 86 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),E$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),E$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),E$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),E$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| F72 | 74 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),F$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),F$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),F$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),F$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| G72 | 49 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),G$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),G$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),G$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),G$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| H72 | 57 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),H$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),H$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),H$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),H$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| I72 | 13 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),I$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),I$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),I$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),I$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| K72 | 97 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),K$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),K$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),K$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),K$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| L72 | 43 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),L$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),L$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),L$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),L$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| M72 | 85 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),M$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),M$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),M$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),M$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| N72 | 98 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),N$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),N$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),N$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),N$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| O72 | 86 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),O$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),O$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),O$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),O$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| P72 | 135 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),P$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),P$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),P$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),P$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| Q72 | 141 | =IFERROR(IF($T72="",COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),Q$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),Q$45),COUNTIFS(INDIRECT("'"&amp;$A72&amp;"'!"&amp;$B72&amp;":"&amp;$B72),Q$44,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$C72&amp;":"&amp;$C72),Q$45,INDIRECT("'"&amp;$A72&amp;"'!"&amp;$T72&amp;":"&amp;$T72),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| R72 | 1050 | =SUM(D72:Q72) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S72 | 0 | =COUNTIF(D72:Q72,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T72 | F |  |

## Row 73

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A73 | ID45 | =A34 [OOXML {"t": "shared", "ref": "A73:C73", "si": "45"}] |
| B73 | C | =B34 [OOXML {"t": "shared", "si": "45"}] |
| C73 | D | =C34 [OOXML {"t": "shared", "si": "45"}] |
| D73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),D$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),D$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),D$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),D$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| E73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),E$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),E$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),E$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),E$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| F73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),F$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),F$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),F$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),F$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| G73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),G$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),G$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),G$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),G$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| H73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),H$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),H$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),H$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),H$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| I73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),I$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),I$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),I$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),I$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| K73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),K$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),K$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),K$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),K$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| L73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),L$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),L$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),L$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),L$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| M73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),M$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),M$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),M$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),M$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| N73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),N$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),N$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),N$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),N$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| O73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),O$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),O$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),O$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),O$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| P73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),P$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),P$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),P$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),P$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| Q73 | 0 | =IFERROR(IF($T73="",COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),Q$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),Q$45),COUNTIFS(INDIRECT("'"&amp;$A73&amp;"'!"&amp;$B73&amp;":"&amp;$B73),Q$44,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$C73&amp;":"&amp;$C73),Q$45,INDIRECT("'"&amp;$A73&amp;"'!"&amp;$T73&amp;":"&amp;$T73),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| R73 | 0 | =SUM(D73:Q73) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S73 | 13 | =COUNTIF(D73:Q73,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T73 | G |  |

## Row 74

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A74 | ID46 | =A35 [OOXML {"t": "shared", "ref": "A74:C74", "si": "46"}] |
| B74 | C | =B35 [OOXML {"t": "shared", "si": "46"}] |
| C74 | D | =C35 [OOXML {"t": "shared", "si": "46"}] |
| D74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),D$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),D$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),D$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),D$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| E74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),E$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),E$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),E$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),E$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| F74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),F$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),F$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),F$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),F$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| G74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),G$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),G$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),G$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),G$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| H74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),H$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),H$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),H$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),H$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| I74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),I$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),I$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),I$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),I$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "38"}] |
| K74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),K$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),K$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),K$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),K$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| L74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),L$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),L$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),L$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),L$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| M74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),M$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),M$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),M$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),M$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| N74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),N$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),N$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),N$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),N$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| O74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),O$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),O$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),O$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),O$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| P74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),P$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),P$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),P$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),P$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| Q74 | 0 | =IFERROR(IF($T74="",COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),Q$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),Q$45),COUNTIFS(INDIRECT("'"&amp;$A74&amp;"'!"&amp;$B74&amp;":"&amp;$B74),Q$44,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$C74&amp;":"&amp;$C74),Q$45,INDIRECT("'"&amp;$A74&amp;"'!"&amp;$T74&amp;":"&amp;$T74),"LG")),0) [OOXML {"t": "shared", "ca": "1", "si": "39"}] |
| R74 | 0 | =SUM(D74:Q74) [OOXML {"t": "shared", "ca": "1", "si": "15"}] |
| S74 | 13 | =COUNTIF(D74:Q74,0) [OOXML {"t": "shared", "ca": "1", "si": "16"}] |
| T74 | G |  |

## Row 75

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A75 | 합계 (Null 개수) |  |
| D75 | 13 | =COUNTIF(D47:D74,0) [OOXML {"ca": "1"}] |
| E75 | 10 | =COUNTIF(E47:E74,0) [OOXML {"t": "shared", "ref": "E75:Q75", "ca": "1", "si": "47"}] |
| F75 | 10 | =COUNTIF(F47:F74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| G75 | 12 | =COUNTIF(G47:G74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| H75 | 11 | =COUNTIF(H47:H74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| I75 | 11 | =COUNTIF(I47:I74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| K75 | 11 | =COUNTIF(K47:K74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| L75 | 11 | =COUNTIF(L47:L74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| M75 | 11 | =COUNTIF(M47:M74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| N75 | 14 | =COUNTIF(N47:N74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| O75 | 14 | =COUNTIF(O47:O74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| P75 | 10 | =COUNTIF(P47:P74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| Q75 | 11 | =COUNTIF(Q47:Q74,0) [OOXML {"t": "shared", "ca": "1", "si": "47"}] |
| S75 | 149 | =SUM(D75:Q75) [OOXML {"ca": "1"}] |

## Row 77

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A77 | ※ ID9 · ID10 은 원본에 Brand 컬럼이 없어 LG 필터 적용 불가 → 전체 행수를 그대로 표시(회색 이탤릭) |  |

## Row 78

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A78 | ※ ID_43 은 시트가 비어 있어 전 조합 0, ID18~23 은 LG만 조사된 시트로 전체=LG 동일 |  |

