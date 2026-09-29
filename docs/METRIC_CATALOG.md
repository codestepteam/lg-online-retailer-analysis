# 진단 항목 카탈로그

S04의 `Clinic 진단 항목` 시트에서 자동 추출했다. 현재 파일의 지표명·판정 문구·집계 문구를 함께 보존한다.
원문 사이의 충돌을 해결한 명세가 아니다. 구현 전에 [핵심 규칙과 확인 사항](BUSINESS_RULES.md)을 읽는다.

지표 ID가 있는 본문 행: 34개. ID는 비연속이며 삭제된 번호를 임의로 다시 채우지 않는다.

| ID | CEJ | 지표 | 주기 | 경쟁사 비교 | Compliance | 원본 행 |
| --- | --- | --- | --- | --- | --- | --- |
| [ID1](#id1) | 1. 인지 | 키워드 검색결과 Top 10 노출 순위 점수 | Daily | Y | N | [행 11](sources/S04-assessment-criteria/sheet-01.md#row-11) |
| [ID2](#id2) | 1. 인지 | 카테고리 키워드 검색결과 Top 10 노출 순위 점수 | Daily | Y | N | [행 12](sources/S04-assessment-criteria/sheet-01.md#row-12) |
| [ID3](#id3) | 1. 인지 | GNB 카테고리 검색결과 Top 10 노출 순위 점수 | Daily | Y | N | [행 13](sources/S04-assessment-criteria/sheet-01.md#row-13) |
| [ID4](#id4) | 1. 인지 | 키워드 검색결과 Top 10 내 자사 제품 노출 점유율 | Daily | Y | N | [행 14](sources/S04-assessment-criteria/sheet-01.md#row-14) |
| [ID7](#id7) | 1. 인지 | GNB 브랜드 카테고리 페이지 도달 단계 수 | Monthly  | Y | N | [행 15](sources/S04-assessment-criteria/sheet-01.md#row-15) |
| [ID8](#id8) | 1. 인지 | 이미지 크기 상위 10개 이미지의 Alt text 적용 여부 | Monthly | Y | Y | [행 16](sources/S04-assessment-criteria/sheet-01.md#row-16) |
| [ID9](#id9) | 1. 인지 | Brand Category Page 내 메타데이터 포함 여부 | Monthly | Y | Y | [행 17](sources/S04-assessment-criteria/sheet-01.md#row-17) |
| [ID10](#id10) | 1. 인지 | Brand Category Page 내 Canonical URL 적용 여부 | Monthly | Y | Y | [행 18](sources/S04-assessment-criteria/sheet-01.md#row-18) |
| [ID23](#id23) | 1. 인지 | Brand Category Page 내 FAQ 존재 여부 | Monthly | Y | Y | [행 19](sources/S04-assessment-criteria/sheet-01.md#row-19) |
| [ID11](#id11) | 1. 인지 | LG 브랜드 필터가 첫 화면에 노출되는 PLP의 비중 | Monthly  | Y | Y | [행 20](sources/S04-assessment-criteria/sheet-01.md#row-20) |
| [ID12](#id12) | 1. 인지 | PDP 상위 10개 이미지 Alt text 적용 비중 | Monthly | Y | Y | [행 21](sources/S04-assessment-criteria/sheet-01.md#row-21) |
| [ID13](#id13) | 1. 인지 | Canonical URL이 올바르게 적용된 PDP 비중 | Monthly | Y | Y | [행 22](sources/S04-assessment-criteria/sheet-01.md#row-22) |
| [ID14](#id14) | 1. 인지 | 순환 유입 경로 보유 SKU 비중 | Monthly | Y | Y | [행 23](sources/S04-assessment-criteria/sheet-01.md#row-23) |
| [ID18](#id18) | 2. 탐색 | Brand Category Page 내 Hero Banner 존재 여부 | Monthly | Y | Y | [행 24](sources/S04-assessment-criteria/sheet-01.md#row-24) |
| [ID19](#id19) | 2. 탐색 | Brand Category Page 내 Why LG 블록 존재 여부 | Monthly | Y | Y | [행 25](sources/S04-assessment-criteria/sheet-01.md#row-25) |
| [ID20](#id20) | 2. 탐색 | Brand Category Page 내 USP 블록 존재 여부 | Monthly | Y | Y | [행 26](sources/S04-assessment-criteria/sheet-01.md#row-26) |
| [ID21](#id21) | 2. 탐색 | Brand Category Page 내 Category Navigator 존재 여부 | Monthly | Y | Y | [행 27](sources/S04-assessment-criteria/sheet-01.md#row-27) |
| [ID22](#id22) | 2. 탐색 | Brand Category Page 내 Product List 존재 여부 | Monthly | Y | Y | [행 28](sources/S04-assessment-criteria/sheet-01.md#row-28) |
| [ID15](#id15) | 2. 탐색 | 정상 접속되는 PDP URL 비중 | Monthly | Y | Y | [행 29](sources/S04-assessment-criteria/sheet-01.md#row-29) |
| [ID24](#id24) | 2. 탐색 | PDP 타이틀 내 USP 키워드를 하나 이상 포함하는 PDP 비중 | Monthly | N | Y | [행 30](sources/S04-assessment-criteria/sheet-01.md#row-30) |
| [ID29](#id29) | 3. 결정 | PDP Asset 해상도 기준(가로 1,200px) 충족 이미지 비중 | Monthly | Y | Y | [행 31](sources/S04-assessment-criteria/sheet-01.md#row-31) |
| [ID44](#id44) | 3. 결정 | PDP Gallery 해상도 기준(가로 1,200px) 충족 이미지 비중 | Monthly | Y | Y | [행 32](sources/S04-assessment-criteria/sheet-01.md#row-32) |
| [ID33](#id33) | 3. 결정 | 갤러리 내 제품 내외부 이미지가 5개 이상인 PDP의 비중 | Monthly | N | Y | [행 33](sources/S04-assessment-criteria/sheet-01.md#row-33) |
| [ID25](#id25) | 3. 결정 | PDP 갤러리 내 USP 이미지를 1개 이상 포함하는 PDP 비중 | Monthly | N | Y | [행 34](sources/S04-assessment-criteria/sheet-01.md#row-34) |
| [ID35](#id35) | 3. 결정 | PDP 갤러리 첫 세트에 USP 카드를 1개 이상 노출하는 PDP 비중 | Monthly | N | Y | [행 35](sources/S04-assessment-criteria/sheet-01.md#row-35) |
| [ID45](#id45) | 3. 결정 | 닷컴에 정의된 USP 대비 PDP 내 노출된 USP 이미지 반영률 | Monthly | N | N | [행 36](sources/S04-assessment-criteria/sheet-01.md#row-36) |
| [ID34](#id34) | 3. 결정 | 제품 관련 비디오 콘텐츠를 보유한 PDP 비중 | Monthly | Y | Y | [행 37](sources/S04-assessment-criteria/sheet-01.md#row-37) |
| [ID39](#id39) | 3. 결정 | Warranty 이미지를 갤러리 또는 본문에 포함하는 PDP 비중 | Monthly | Y | Y | [행 38](sources/S04-assessment-criteria/sheet-01.md#row-38) |
| [ID40](#id40) | 3. 결정 | 갤러리 내 Dimension 이미지를 보유한 PDP 비중 | Monthly | Y | Y | [행 39](sources/S04-assessment-criteria/sheet-01.md#row-39) |
| [ID46](#id46) | 3. 결정 | PDP Asset 영역에 Dimension 이미지를 보유한 PDP 비중 | Monthly | Y | Y | [행 40](sources/S04-assessment-criteria/sheet-01.md#row-40) |
| [ID37](#id37) | 3. 결정 | 리뷰 평점 3.0 이상 SKU 비중 | Daily | N | Y | [행 41](sources/S04-assessment-criteria/sheet-01.md#row-41) |
| [ID38](#id38) | 3. 결정 | 리뷰 5개 이상 보유 SKU 비중 | Daily | N | Y | [행 42](sources/S04-assessment-criteria/sheet-01.md#row-42) |
| [ID42](#id42) | 3. 결정 | HTML내 Flixmedia 코드 포함된 SKU 비중 | Monthly | Y | Y | [행 43](sources/S04-assessment-criteria/sheet-01.md#row-43) |
| [ID43](#id43) | 3. 결정 | Flixmedia 컨텐츠 정상 렌더링 SKU 비중 | Monthly | N | N | [행 44](sources/S04-assessment-criteria/sheet-01.md#row-44) |

## ID1

**키워드 검색결과 Top 10 노출 순위 점수**

출처: S04 `Clinic 진단 항목`, 행 11. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-11)

- 관리 목적 (P11): 고객이 제품 관련 키워드 검색 시 LG 제품을 검색 결과 상단에서 발견할 수 있도록 하여, 초기 유입 기회를 측정하기 위함
- 점수화 기준 (W11): 구간을 나누어 등급화 하지 않고, Top10內 자사 제품 노출 순위기반 점수화 하여 측정<br>case1. Top10內 자사 제품 노출 : 1위(10점), 2위(9점) -&gt; 19점<br>case2. Top10內 자사 제품 노출 : 9위(2점), 10위(1점) -&gt; 3점
- 최소 진단 단위 (AB11): Search Term (Product Keyword)
- 집계 규칙 (AC11): 카테고리별 / 리테일러별 키워드 검색 결과의 평균
- 측정 주기 (V11): Daily
- 경쟁사 비교 (Z11): Y
- Compliance (AA11): N

## ID2

**카테고리 키워드 검색결과 Top 10 노출 순위 점수**

출처: S04 `Clinic 진단 항목`, 행 12. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-12)

- 관리 목적 (P12): 제품 카테고리 검색 고객이 검색 결과 리스트에서 LG 제품을 쉽게 발견하고 비교 검토 대상으로 인식할 수 있도록 하여, 초기 유입 기회를 확보하기 위함
- 점수화 기준 (W12): 구간을 나누어 등급화 하지 않고, Top10內 자사 제품 노출 순위기반 점수화 하여 측정<br>case1. Top10內 자사 제품 노출 : 1위(10점), 2위(9점) -&gt; 19점<br>case2. Top10內 자사 제품 노출 : 9위(2점), 10위(1점) -&gt; 3점
- 최소 진단 단위 (AB12): Search Term (Product Category Keyword)
- 집계 규칙 (AC12): 카테고리별 / 리테일러별 카테고리 키워드 검색 결과의 평균
- 측정 주기 (V12): Daily
- 경쟁사 비교 (Z12): Y
- Compliance (AA12): N

## ID3

**GNB 카테고리 검색결과 Top 10 노출 순위 점수**

출처: S04 `Clinic 진단 항목`, 행 13. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-13)

- 관리 목적 (P13): GNB 클릭 통한 카테고리 탐색 고객이 검색 결과 리스트에서 LG 제품을 쉽게 발견하도록 하여 초기 유입 기회 확보하도록 함
- 점수화 기준 (W13): 구간을 나누어 등급화 하지 않고, Top10內 자사 제품 노출 순위기반 점수화 하여 측정<br>case1. Top10內 자사 제품 노출 : 1위(10점), 2위(9점) -&gt; 19점<br>case2. Top10內 자사 제품 노출 : 9위(2점), 10위(1점) -&gt; 3점
- 최소 진단 단위 (AB13): Product Category
- 집계 규칙 (AC13): 카테고리별 / 리테일러별 카테고리 키워드 GNB 검색 결과의 평균
- 측정 주기 (V13): Daily
- 경쟁사 비교 (Z13): Y
- Compliance (AA13): N

## ID4

**키워드 검색결과 Top 10 내 자사 제품 노출 점유율**

출처: S04 `Clinic 진단 항목`, 행 14. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-14)

- 관리 목적 (P14): 고객이 제품 관련 키워드 검색 시 LG의 제품 리스트 차지 비중을 인식하고 LG 점유 정도를 확인할 수 있도록 함
- 점수화 기준 (W14): PLP Top 10 내 자사 제품 개수의 비중<br>case1. Top10內 자사 제품 노출 개수 : 10개 (10점/10) = 100%<br>case2. Top10內 자사 제품 노출 개수 : 3개 (3점/10) = 30%
- 최소 진단 단위 (AB14): Search Term (Product Keyword)
- 집계 규칙 (AC14): 카테고리별 / 리테일러별 카테고리 키워드 검색 결과의 평균
- 측정 주기 (V14): Daily
- 경쟁사 비교 (Z14): Y
- Compliance (AA14): N

## ID7

**GNB 브랜드 카테고리 페이지 도달 단계 수**

출처: S04 `Clinic 진단 항목`, 행 15. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-15)

- 관리 목적 (P15): GNB를 통해 리테일러 홈에서 LG 브랜드/제품 페이지로 쉽게 이동할 수 있도록 하여 브랜드 탐색 여정을 강화
- 점수화 기준 (W15): Home → Brand Page/PCP<br>브랜드페이지 랜딩 단계(depth) 측정
- 최소 진단 단위 (AB15): Retailer
- 집계 규칙 (AC15): 국가별/리테일러별/카테고리별 Depth 횟수
- 측정 주기 (V15): Monthly 
- 경쟁사 비교 (Z15): Y
- Compliance (AA15): N

## ID8

**이미지 크기 상위 10개 이미지의 Alt text 적용 여부**

출처: S04 `Clinic 진단 항목`, 행 16. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-16)

- 관리 목적 (P16): Brand Category Page 이미지 콘텐츠가 검색엔진/AI에 의해 올바르게 인식될 수 있도록 하여, 브랜드 페이지의 검색 친화도와 접근성을 높이기 위함
- 점수화 기준 (W16): 이미지 크기 상위 10개 이미지에  Alt text 존재 여부<br>Y: 모두 적용<br>N: 1개 이상 미적용
- 최소 진단 단위 (AB16): Image
- 집계 규칙 (AC16): 국가별/카테고리별/리테일러별 Brand Category Page 내 이미지 크기 상위 10개 이미지의 Alt text 적용(Y) 비중
- 측정 주기 (V16): Monthly
- 경쟁사 비교 (Z16): Y
- Compliance (AA16): Y

## ID9

**Brand Category Page 내 메타데이터 포함 여부**

출처: S04 `Clinic 진단 항목`, 행 17. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-17)

- 관리 목적 (P17): Brand Category Page의 핵심 정보가 검색엔진/AI에 명확히 전달되도록 하여, 브랜드 페이지의 검색 친화도와 접근성을 높이기 위함
- 점수화 기준 (W17): Y: 모두 적용<br>N: 1개 이상 미적용
- 최소 진단 단위 (AB17): Brand Category Page
- 집계 규칙 (AC17): 국가별/카테고리별/리테일러별 Title, Meta Description, H1, Robots Meda 태그 포함(Y) Brand Page 비중
- 측정 주기 (V17): Monthly
- 경쟁사 비교 (Z17): Y
- Compliance (AA17): Y

## ID10

**Brand Category Page 내 Canonical URL 적용 여부**

출처: S04 `Clinic 진단 항목`, 행 18. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-18)

- 관리 목적 (P18): Brand Category Page의 대표 URL을 명확히 지정하여, 중복 URL로 인한 검색 신호 분산과 페이지 인식 오류를 방지하기 위함
- 점수화 기준 (W18): Y: Canonical URL이Brand Category Page에 적용됨<br>N: Canonical URL이Brand Category Page에 미적용됨
- 최소 진단 단위 (AB18): Brand Category Page
- 집계 규칙 (AC18): 국가별/카테고리별/리테일러별 Canonical URL이 적용된Brand Category Page 비중
- 측정 주기 (V18): Monthly
- 경쟁사 비교 (Z18): Y
- Compliance (AA18): Y

## ID23

**Brand Category Page 내 FAQ 존재 여부**

출처: S04 `Clinic 진단 항목`, 행 19. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-19)

- 관리 목적 (P19): Brand Category Page 내 자사 제품군 정보를 구조화된 텍스트 형태로 제공함으로써, AI 및 검색 엔진의 이해도와 검색 노출 가능성을 높이기 위함
- 점수화 기준 (W19): Y: 구조화된 텍스트 형식으로 존재<br>N: FAQ 없거나 이미지 형태로 존재
- 최소 진단 단위 (AB19): Brand Category Page
- 집계 규칙 (AC19): 국가별/카테고리별/리테일러별 브랜드 및 카테고리 관련 FAQ가 구조화된 텍스트 형태로 존재(Y) Brand Category Page 비중
- 측정 주기 (V19): Monthly
- 경쟁사 비교 (Z19): Y
- Compliance (AA19): Y

## ID11

**LG 브랜드 필터가 첫 화면에 노출되는 PLP의 비중**

출처: S04 `Clinic 진단 항목`, 행 20. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-20)

- 관리 목적 (P20): 제품 리스트 탐색 고객이 브랜드 필터를 통해 LG 제품만 빠르게 선별할 수 있도록 하여, 탐색 효율과 제품 비교 편의성을 높이기 위함
- 점수화 기준 (W20): Y: PLP 첫 화면에 필터 항목으로 노출<br>N: PLP 첫 화면에 필터 항목으로 미노출/부재
- 최소 진단 단위 (AB20): Product Category
- 집계 규칙 (AC20): 카테고리별/리테일러별/카테고리별 PLP 중 자사 브랜드 필터 적용 비중
- 측정 주기 (V20): Monthly 
- 경쟁사 비교 (Z20): Y
- Compliance (AA20): Y

## ID12

**PDP 상위 10개 이미지 Alt text 적용 비중**

출처: S04 `Clinic 진단 항목`, 행 21. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-21)

- 관리 목적 (P21): PDP 이미지 콘텐츠가 검색엔진/AI에 의해 올바르게 인식될 수 있도록 하여, 제품 상세 페이지의 검색 친화도와 접근성을 높이기 위함
- 점수화 기준 (W21): 이미지 크기 상위 10개 이미지에  Alt text 존재 여부<br>(전체 이미지는 최대 10개까지만 보고, 이미지 개수와 Alt text 적용 이미지 개수가 같은지 여부가 중요)<br>Y: 모두 적용<br>N: 1개 이상 미적용
- 최소 진단 단위 (AB21): Product Detail Page
- 집계 규칙 (AC21): 국가별/카테고리별/리테일러별 PDP 내 이미지 크기 상위 10개 이미지의 Alt text 적용(Y) 비중
- 측정 주기 (V21): Monthly
- 경쟁사 비교 (Z21): Y
- Compliance (AA21): Y

## ID13

**Canonical URL이 올바르게 적용된 PDP 비중**

출처: S04 `Clinic 진단 항목`, 행 22. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-22)

- 관리 목적 (P22): PDP의 대표 URL을 명확히 지정하여 중복 인식 및 검색 신호 분산을 방지하고, 잘못 지정된 Canonical URL(상이 제품 랜딩·404)로 인한 색인 누락을 예방하기 위함
- 점수화 기준 (W22): (A) PDP URL과 (B) Canonical URL 일치 여부 및 Canonical URL 유효성으로 점수화<br>정상: (A)와 (B)가 일치, 혹은 불일치해도 Canonical URL이 동일 제품의 정상 페이지로 랜딩<br>개선대상: (A)와 (B)가 불일치 + Canonical URL이 부재·상이 제품 랜딩·404 중 하나 이상
- 최소 진단 단위 (AB22): Product Detail Page
- 집계 규칙 (AC22): 카테고리별/리테일러별 Canonical URL이 올바르게 적용된 PDP 페이지 비중
- 측정 주기 (V22): Monthly
- 경쟁사 비교 (Z22): Y
- Compliance (AA22): Y

## ID14

**순환 유입 경로 보유 SKU 비중**

출처: S04 `Clinic 진단 항목`, 행 23. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-23)

- 관리 목적 (P23): PDP 방문 고객이 LG 브랜드 페이지 또는 관련 자사 제품 페이지로 이어서 탐색할 수 있도록 하여, 리테일러 내 자사 제품 체류와 비교 기회를 확대하기 위함
- 점수화 기준 (W23): Y: 브랜드 페이지 또는 자사 제품 페이지 이동 링크 존재(PCP)<br>N: 경로 부재 / 오류 (비정상)
- 최소 진단 단위 (AB23): Product Detail Page
- 집계 규칙 (AC23): 카테고리별/리테일러별 PDP 순환유입경로 존재(Y)하는 PDP 비중
- 측정 주기 (V23): Monthly
- 경쟁사 비교 (Z23): Y
- Compliance (AA23): Y

## ID18

**Brand Category Page 내 Hero Banner 존재 여부**

출처: S04 `Clinic 진단 항목`, 행 24. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-24)

- 관리 목적 (P24): Brand Category Page 진입 고객에게 브랜드 또는 제품군의 핵심 메시지를 첫 화면에서 효과적으로 전달하여, 제품 페이지 탐색을 유도하기 위함
- 점수화 기준 (W24): Y: 존재<br>N: 부재
- 최소 진단 단위 (AB24): Brand Category Page
- 집계 규칙 (AC24): 국가별/카테고리별/리테일러별 Hero Banner 존재(Y) Brand Category Page 비중
- 측정 주기 (V24): Monthly
- 경쟁사 비교 (Z24): Y
- Compliance (AA24): Y

## ID19

**Brand Category Page 내 Why LG 블록 존재 여부**

출처: S04 `Clinic 진단 항목`, 행 25. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-25)

- 관리 목적 (P25): Brand Category Page 탐색 고객에게 LG를 선택해야 하는 이유와 브랜드 차별성을 제공하여, 브랜드 신뢰와 선호를 유도하기 위함
- 점수화 기준 (W25): Y: 존재<br>N: 부재
- 최소 진단 단위 (AB25): Brand Category Page
- 집계 규칙 (AC25): 국가별/카테고리별/리테일러별 Why LG 블록 존재(Y) Brand Category Page 비중
- 측정 주기 (V25): Monthly
- 경쟁사 비교 (Z25): Y
- Compliance (AA25): Y

## ID20

**Brand Category Page 내 USP 블록 존재 여부**

출처: S04 `Clinic 진단 항목`, 행 26. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-26)

- 관리 목적 (P26): Brand Category Page 탐색 고객이 제품군별 핵심 기술과 사용 가치를 쉽게 이해할 수 있도록 하여, 제품에 대한 관심과 상세 탐색을 유도하기 위함
- 점수화 기준 (W26): Y: 존재<br>N: 부재
- 최소 진단 단위 (AB26): Brand Category Page
- 집계 규칙 (AC26): 국가별/카테고리별/리테일러별 핵심 USP 블록 존재(Y) Brand Category Page 비중
- 측정 주기 (V26): Monthly
- 경쟁사 비교 (Z26): Y
- Compliance (AA26): Y

## ID21

**Brand Category Page 내 Category Navigator 존재 여부**

출처: S04 `Clinic 진단 항목`, 행 27. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-27)

- 관리 목적 (P27): Brand Category Page 탐색 고객이 관심 제품군으로 빠르게 이동할 수 있도록 하여, 브랜드 페이지 내 탐색 편의성과 PDP 유입을 높이기 위함
- 점수화 기준 (W27): Y: CTA 존재, 정상 작동<br>N: CTA 부재 / CTA 존재하나 작동 불가
- 최소 진단 단위 (AB27): Brand Category Page
- 집계 규칙 (AC27): 국가별/카테고리별/리테일러별 Navigator 존재 및 정상 작동(Y) Brand Category Page 비중
- 측정 주기 (V27): Monthly
- 경쟁사 비교 (Z27): Y
- Compliance (AA27): Y

## ID22

**Brand Category Page 내 Product List 존재 여부**

출처: S04 `Clinic 진단 항목`, 행 28. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-28)

- 관리 목적 (P28): Brand Category Page에서 고객이 제품 상세 페이지로 바로 진입 가능한 CTA를 제공하여, 탐색 편의성과 PDP 유입을 높이기 위함
- 점수화 기준 (W28): Y: PDP 유입 CTA 존재 (Clickable)<br>N: PDP 유입 CTA 부재 (Non-clickable)
- 최소 진단 단위 (AB28): Brand Category Page
- 집계 규칙 (AC28): 국가별/카테고리별/리테일러별 PDP로 이동 가능한 Product List 와 CTA 존재(Y) Brand Category Page 비중
- 측정 주기 (V28): Monthly
- 경쟁사 비교 (Z28): Y
- Compliance (AA28): Y

## ID15

**정상 접속되는 PDP URL 비중**

출처: S04 `Clinic 진단 항목`, 행 29. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-29)

- 관리 목적 (P29): PDP URL이 정상 동작하도록 관리하여, 고객의 제품 탐색 및 구매 여정이 오류로 중단되지 않도록 하기 위함
- 점수화 기준 (W29): Y: 접속/유입 가능 (정상)<br>N: PDP 및 링크 불일치/오류 (비정상)
- 최소 진단 단위 (AB29): Product Detail Page
- 집계 규칙 (AC29): 카테고리별/리테일러별 PDP 정상 링크(Y) 비중
- 측정 주기 (V29): Monthly
- 경쟁사 비교 (Z29): Y
- Compliance (AA29): Y

## ID24

**PDP 타이틀 내 USP 키워드를 하나 이상 포함하는 PDP 비중**

출처: S04 `Clinic 진단 항목`, 행 30. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-30)

- 관리 목적 (P30): PDP 방문 고객이 제품명만으로 핵심 스펙을 빠르게 인지할 수 있도록 하여, 제품 이해와 타이틀 매력도를 높이기 위함
- 점수화 기준 (W30): Y: 핵심 USP 키워드 포함<br>N: 핵심 USP 키워드 미포함
- 최소 진단 단위 (AB30): Product Detail Page
- 집계 규칙 (AC30): 카테고리별/리테일러별 USP 키워드 포함(Y) PDP 비중
- 측정 주기 (V30): Monthly
- 경쟁사 비교 (Z30): N
- Compliance (AA30): Y

## ID29

**PDP Asset 해상도 기준(가로 1,200px) 충족 이미지 비중**

출처: S04 `Clinic 진단 항목`, 행 31. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-31)

- 관리 목적 (P31): PDP 본문 탐색 고객이 제품 기능과 사용 가치를 선명한 이미지로 확인할 수 있도록 하여, 제품 신뢰도와 이해도를 높이기 위함
- 점수화 기준 (W31): 이미지 규격 충족 점수<br>Top 10 이미지 중 권장 해상도 이상 이미지 개수 비중(%)
- 최소 진단 단위 (AB31): Asset Image
- 집계 규칙 (AC31): 국가별/리테일러별/카테고리별 전체 모수 중 PDP Asset 이미지 해상도 기준 충족 비율(%) 평균
- 측정 주기 (V31): Monthly
- 경쟁사 비교 (Z31): Y
- Compliance (AA31): Y

## ID44

**PDP Gallery 해상도 기준(가로 1,200px) 충족 이미지 비중**

출처: S04 `Clinic 진단 항목`, 행 32. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-32)

- 관리 목적 (P32): PDP Gallery 탐색 고객이 제품 기능과 사용 가치를 선명한 이미지로 확인할 수 있도록 하여, 제품 신뢰도와 이해도를 높이기 위함
- 점수화 기준 (W32): 이미지 규격 충족 점수<br>Top 10 이미지 중 권장 해상도 이상 이미지 개수 비중(%)
- 최소 진단 단위 (AB32): Asset Image
- 집계 규칙 (AC32): 국가별/리테일러별/카테고리별 전체 모수 중 PDP Gallery 이미지 해상도 기준 충족 비율(%) 평균
- 측정 주기 (V32): Monthly
- 경쟁사 비교 (Z32): Y
- Compliance (AA32): Y

## ID33

**갤러리 내 제품 내외부 이미지가 5개 이상인 PDP의 비중**

출처: S04 `Clinic 진단 항목`, 행 33. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-33)

- 관리 목적 (P33): PDP 방문 고객이 제품의 외관, 내부, 주요 각도를 충분히 확인할 수 있도록 하여, 비대면 구매 환경에서도 제품 이해도를 높이기 위함
- 점수화 기준 (W33): Y: 내/외부 이미지 개수 5개 이상일 경우<br>N: 내/외부 이미지 개수 5개 미만일 경우
- 최소 진단 단위 (AB33): Product Detail Page
- 집계 규칙 (AC33): 카테고리별/리테일러별<br>PDP 갤러리 내 제품 이미지 개수의 평균
- 측정 주기 (V33): Monthly
- 경쟁사 비교 (Z33): N
- Compliance (AA33): Y

## ID25

**PDP 갤러리 내 USP 이미지를 1개 이상 포함하는 PDP 비중**

출처: S04 `Clinic 진단 항목`, 행 34. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-34)

- 관리 목적 (P34): PDP 방문 고객이 갤러리 영역에서 제품 핵심 USP를 즉시 확인할 수 있도록 하여, 초기 구매 관심과 타사 제품 대비 차별화 인식을 높이기 위함
- 점수화 기준 (W34): Y: 갤러리 내 USP 존재<br>N: 갤러리 내 USP 부재
- 최소 진단 단위 (AB34): Product Detail Page
- 집계 규칙 (AC34): 카테고리별/리테일러별 USP 이미지 보유(Y) PDP 비중
- 측정 주기 (V34): Monthly
- 경쟁사 비교 (Z34): N
- Compliance (AA34): Y

## ID35

**PDP 갤러리 첫 세트에 USP 카드를 1개 이상 노출하는 PDP 비중**

출처: S04 `Clinic 진단 항목`, 행 35. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-35)

- 관리 목적 (P35): PDP 방문 고객이 추가 클릭 없이 초기 갤러리 화면에서 핵심 USP를 확인할 수 있도록 하여, 주요 메시지 도달률을 높이기 위함
- 점수화 기준 (W35): Y: USP 카드 포함<br>N: USP 카드 미포함
- 최소 진단 단위 (AB35): Product Detail Page
- 집계 규칙 (AC35): 카테고리별/리테일러별 갤러리 첫 세트 내 USP 이미지 존재(Y) PDP 비중
- 측정 주기 (V35): Monthly
- 경쟁사 비교 (Z35): N
- Compliance (AA35): Y

## ID45

**닷컴에 정의된 USP 대비 PDP 내 노출된 USP 이미지 반영률**

출처: S04 `Clinic 진단 항목`, 행 36. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-36)

- 관리 목적 (P36): PDP 내 제품 탐색 과정에서 핵심 USP가 충분히 설명되도록 하여, 자사 제품 차별성과 구매 설득력을 강화하기 위함
- 점수화 기준 (W36): 제품별 USP 반영률에 따라 점수 부여: (노출된 표준 USP 수 ÷ 사전 정의된 표준 USP 수) × 10점
- 최소 진단 단위 (AB36): Product Detail Page
- 집계 규칙 (AC36): 카테고리별/리테일러별 PDP의 정의된 핵심 USP 대비 리테일러 내 노출된 USP 이미지 비중
- 측정 주기 (V36): Monthly
- 경쟁사 비교 (Z36): N
- Compliance (AA36): N

## ID34

**제품 관련 비디오 콘텐츠를 보유한 PDP 비중**

출처: S04 `Clinic 진단 항목`, 행 37. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-37)

- 관리 목적 (P37): PDP 방문 고객이 영상 콘텐츠를 통해 제품 기능이나 사용 방식을 직관적으로 이해할 수 있도록 하여, 제품 이해도와 구매 확신을 높이기 위함
- 점수화 기준 (W37): Y: 1개 이상의 제품 관련 영상 존재<br>N: Video 없음
- 최소 진단 단위 (AB37): Product Detail Page
- 집계 규칙 (AC37): 카테고리별/리테일러별 갤러리 내 비디오 콘텐츠 존재(Y) PDP 비중
- 측정 주기 (V37): Monthly
- 경쟁사 비교 (Z37): Y
- Compliance (AA37): Y

## ID39

**Warranty 이미지를 갤러리 또는 본문에 포함하는 PDP 비중**

출처: S04 `Clinic 진단 항목`, 행 38. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-38)

- 관리 목적 (P38): PDP 방문 고객이 보증 정보를 쉽게 확인할 수 있도록 하여, 제품 신뢰도와 구매 안정감을 높이기 위함
- 점수화 기준 (W38): Y: Warranty 이미지 존재<br>N: Warranty 이미지 부재
- 최소 진단 단위 (AB38): Product Detail Page
- 집계 규칙 (AC38): 카테고리별/리테일러별 Warranty 이미지 보유(Y) PDP 비중
- 측정 주기 (V38): Monthly
- 경쟁사 비교 (Z38): Y
- Compliance (AA38): Y

## ID40

**갤러리 내 Dimension 이미지를 보유한 PDP 비중**

출처: S04 `Clinic 진단 항목`, 행 39. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-39)

- 관리 목적 (P39): PDP 방문 고객이 제품 크기와 설치 가능 여부를 사전에 판단할 수 있도록 하여, 구매 전 불확실성과 반품 리스크를 낮추기 위함
- 점수화 기준 (W39): Y: Dimension 이미지 존재<br>N: Dimension 이미지 부재
- 최소 진단 단위 (AB39): Product Detail Page
- 집계 규칙 (AC39): 카테고리별/리테일러별 갤러리 내 Dimension 이미지 보유(Y) PDP 비중
- 측정 주기 (V39): Monthly
- 경쟁사 비교 (Z39): Y
- Compliance (AA39): Y

## ID46

**PDP Asset 영역에 Dimension 이미지를 보유한 PDP 비중**

출처: S04 `Clinic 진단 항목`, 행 40. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-40)

- 관리 목적 (P40): PDP 방문 고객이 제품 크기와 설치 가능 여부를 사전에 판단할 수 있도록 하여, 구매 전 불확실성과 반품 리스크를 낮추기 위함
- 점수화 기준 (W40): Y: Dimension 이미지 존재<br>N: Dimension 이미지 부재
- 최소 진단 단위 (AB40): Product Detail Page
- 집계 규칙 (AC40): 카테고리별/리테일러별 PDP 본문 영역 내 Dimension 이미지 보유(Y) PDP 비중
- 측정 주기 (V40): Monthly
- 경쟁사 비교 (Z40): Y
- Compliance (AA40): Y

## ID37

**리뷰 평점 3.0 이상 SKU 비중**

출처: S04 `Clinic 진단 항목`, 행 41. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-41)

- 관리 목적 (P41): 사용자 리뷰 평점으로 인해 구매 저항이 우려되는 PDP URL을 식별·모니터링하여, 개선 조치가 가능하도록 관리하기 위함
- 점수화 기준 (W41): 리뷰 평점 3.0 이상 비중 (%)
- 최소 진단 단위 (AB41): Product Detail Page
- 집계 규칙 (AC41): 국가별/리테일러별/카테고리별 기준치 이상 비중(%)
- 측정 주기 (V41): Daily
- 경쟁사 비교 (Z41): N
- Compliance (AA41): Y

## ID38

**리뷰 5개 이상 보유 SKU 비중**

출처: S04 `Clinic 진단 항목`, 행 42. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-42)

- 관리 목적 (P42): 리뷰의 충분한 모수가 확보되었는지 확인하여, 사용자 평점의 대표성과 신뢰도를 판단하기 위함
- 점수화 기준 (W42): 리뷰 개수 5 이상 비중 (%)
- 최소 진단 단위 (AB42): Product Detail Page
- 집계 규칙 (AC42): 국가별/리테일러별/카테고리별 기준치 이상 비중(%)
- 측정 주기 (V42): Daily
- 경쟁사 비교 (Z42): N
- Compliance (AA42): Y

## ID42

**HTML내 Flixmedia 코드 포함된 SKU 비중**

출처: S04 `Clinic 진단 항목`, 행 43. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-43)

- 관리 목적 (P43): Flixmedia 연동 대상 PDP의 HTML 내에 Flixmedia 코드가 포함되는지 확인하여 Flixmedia로 제공되는 컨텐츠가 정상적으로 연동·노출되기 위한 선행 조건을 점검하기 위함
- 점수화 기준 (W43): Y: 연동<br>N: 미연동 오류
- 최소 진단 단위 (AB43): Product Detail Page
- 집계 규칙 (AC43): 국가별/리테일러별/카테고리별 Flixmedia 정상 연동 비율(%) 평균
- 측정 주기 (V43): Monthly
- 경쟁사 비교 (Z43): Y
- Compliance (AA43): Y

## ID43

**Flixmedia 컨텐츠 정상 렌더링 SKU 비중**

출처: S04 `Clinic 진단 항목`, 행 44. [전체 원문](sources/S04-assessment-criteria/sheet-01.md#row-44)

- 관리 목적 (P44): Flixmedia 콘텐츠가 PDP에서 정상 로딩·표시되도록 관리하여, 고객이 공식 제품 정보를 오류 없이 확인할 수 있도록 하기 위함
- 점수화 기준 (W44): 닷컴과 PDP간 콘텐츠 일치율(%)
- 최소 진단 단위 (AB44): Product Detail Page
- 집계 규칙 (AC44): 국가별/리테일러별/카테고리별 Flixmedia 콘텐츠 일치율(%)
- 측정 주기 (V44): Monthly
- 경쟁사 비교 (Z44): N
- Compliance (AA44): N
