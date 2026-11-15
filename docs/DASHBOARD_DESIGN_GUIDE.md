# LG 대시보드 디자인 가이드 정리

EY 최하은이 2026년 11월 11일에 보낸 PowerPoint **`[LGE] Dashboard Design Guide_261110.pptx`** 24장을 정리했다. 이 가이드는 현재 개발된 대시보드의 화면 배치, 공통 요소, 색상과 숫자 표기를 통일하기 위한 자료다. [두레이 메일과 첨부 원본](https://codestep.dooray.com/mail/systems/inbox/4463206556762037995)

[24장 적용 전후와 로컬 검증 결과](../outputs/ey-design-guide-report/index.html)

[PPT 1~24장 원문 바로가기](#5-ppt-124장-원문)

## 1. 공통 화면 배치

가이드의 디자인 작업 환경은 Adobe Photoshop, 데스크톱 웹 가로 **1920px**, 해상도 **72ppi**(인치당 픽셀 수)다. 3장 `Design Working Specification`에 적혀 있다.

| 영역 | 디자인 규칙 | PPT 위치 |
| --- | --- | --- |
| 상단 헤더 | 페이지 최상단에 고정하고 모든 탭에서 같은 구조를 유지한다. 왼쪽에 LG전자 로고와 대시보드 이름, 오른쪽에 `Glossary`(용어집) 버튼 등 기능을 둔다. 배경은 `#000000`에서 `#A50034`로 이어지는 그라데이션이다. 제목에는 H2 규격인 LG 스마트체 Bold 34px을 쓴다. | 4장 `Header` |
| 탭 | 흰색 배경에 `Overview`(개요), `LG Analysis`(LG 분석), `Competitor Analysis`(경쟁사 분석), `Raw Table`(원시 데이터 표)을 가로로 균등 배치한다. **활성 탭 글자**는 `Body 1 / LG 스마트체 / semiold / 28px / #A50034`(원문 표기), **기본 탭 글자**는 `Body 1 / LG 스마트체 / SemiBold / 28px / #000000`이다. 활성 탭 하단 강조선에도 `#A50034`를 쓴다. | 5장 `Tab` |
| 조회 필터 | 콘텐츠 위에 균등하게 배치하고 콘텐츠와 필터 사이에 구분선을 둔다. 탭마다 항목은 달라질 수 있으며 입력창의 디자인과 배치 규칙, 선택창의 레이아웃은 통일한다. 영역 배경 `#F0ECE4`, 입력창 배경 `#F7F6F4`, 테두리 `#D9D6D1`, 모서리 반경 15px이다. 필터 이름은 LG 스마트체 Bold 24px `#8C8C8C`, 입력창 글자는 SemiBold 22px `#000000`으로 표기돼 있다. | 6장 `Filter`, 16장 `Component Guide` |
| 콘텐츠 영역 | 페이지 배경은 `#F0ECE4`, 콘텐츠 상자는 흰색, 모서리 반경은 25px이다. 카드에 별도 제목이 있으면 `#F7F6F4`의 헤더를 붙이고, 개별 제목이 없으면 흰색 상자만 사용한다. 두 유형의 기본 스타일과 모서리 규격은 같으며 두 예시 모두 사방 여백은 48px이다. 섹션 제목은 LG 스마트체 Bold 34px이다. | 7~9장 `Content Area` |

탭의 분석 목적에 맞게 핵심 성과 지표(KPI), 표, 차트를 배치한다. 콘텐츠별 배치는 달라질 수 있으며 여백·정렬·공통 요소의 디자인 규칙을 유지한다. 정보 순서는 **제목 → 참고 설명과 부가 정보 → 필터와 범례 → 표·차트 및 설명**이다. 섹션 제목 아래 흰색 상자 안에 해석 문구, 필터, 주요 수치, 표와 차트를 둔다. (7~12장)

4장 헤더 그림에는 `Home Appliance Solution Retail Clinic Dashboard`(생활가전 솔루션 리테일 클리닉 대시보드)라는 제목이 보인다. 6장 그림에서는 `Country`(국가)의 예시 값이 스페인, `Month`(월)의 예시 값이 2026년 10월이다. 국가 선택창에는 체크박스, `Select all`(전체 선택), `Apply`(적용) 버튼이 보인다. 8장 그림에는 `KPI Status`(핵심 성과 지표 현황) 아래 `Conversion`(전환) 헤더가 있고, 9장 `Overview`(개요) 그림에는 흰색 콘텐츠 상자에 별도 헤더가 없다.

| 화면 예시 | 그림에서 확인한 배치 | PPT 위치 |
| --- | --- | --- |
| 콘텐츠 하나 | 상자 상단 왼쪽에 `Insight / Description`(해석·설명), 오른쪽에 필터를 두고, 아래에 표나 차트를 배치한다. | 10장 `텍스트 입력 가능 영역` |
| 콘텐츠에 개별 제목이 있음 | 섹션 제목은 상자 위에, 개별 제목은 상자 안쪽의 연한 회색 헤더에 둔다. 설명·필터·데이터는 그 아래에 배치한다. | 11장 `텍스트 입력 가능 영역` |
| 여러 콘텐츠가 설명과 필터를 공유함 | 바깥쪽 흰색 상자 상단에 공통 설명과 필터를 둔다. 예시에서는 그 아래 두 콘텐츠를 나란히 배치하고 각 콘텐츠의 제목, 설명 또는 필터, 데이터 영역을 표시한다. | 12장 `텍스트 입력 가능 영역` |

## 2. 공통 요소 디자인

| 요소 | 디자인 규칙 | PPT 위치 |
| --- | --- | --- |
| KPI 카드 | 같은 형태의 사각형 카드에 모서리 반경 25px을 적용한다. 상단 `#F7F6F4` 영역에 지표명을 넣고 본문은 흰색으로 둔다. 내부 여백은 공통 콘텐츠 영역을 따른다. 카드 안에서는 지표명 → 참고 설명과 부가 정보 → 필터와 범례 → 표·차트 순으로 배치한다. 글자는 공통 글자와 데이터 색상 기준을 따르고, 주요 수치와 보조 정보의 배치를 통일한다. | 14장 `KPI 카드` |
| 표 | 헤더 배경은 `#F7F6F4`이며 상하 여백을 통일한다. 행 높이와 간격, 같은 행의 상하 여백, 구분선 두께를 일관되게 적용한다. 콘텐츠별로 셀 크기와 사방 여백을 통일한다. 숫자는 오른쪽 또는 중앙, 그 외 텍스트는 왼쪽 또는 중앙에 정렬한다. | 15장 `표` |
| 차트 | 헤더 배경은 `#F7F6F4`이며 상하 여백을 통일한다. 보조 문구는 헤더 바로 아래나 오른쪽에, 범례는 보조 문구 바로 아래나 오른쪽에, 필터는 콘텐츠 영역 맨 오른쪽에 둔다. 데이터 선의 굵기와 연결 방식, 범례 배치와 차트 사이 간격, 구분선 두께를 통일한다. 값 레이블은 툴팁(데이터에 대한 작은 안내 상자)으로 표시한다. | 16장 `차트` |
| 필터 | 필터 이름 아래에 입력창을 두고 모서리 반경 15px을 적용한다. | 16장 `필터` |
| 범례 | 지름 15px의 원으로 색상을 표시하고 가로로 배치한다. | 17장 `범례` |
| 툴팁 | 흰색 바탕에 기본 테두리 `#626262`를 사용한다. 차트나 그래프에 비교할 데이터가 많으면 각 데이터 색상에 맞춰 테두리색을 바꾼다. 글자는 왼쪽 정렬하고 항목은 줄바꿈으로 구분한다. | 17장 `툴팁` |
| 빈 상태 | 표시할 콘텐츠가 없을 때 안내 문구를 중앙에 둔다. | 17장 `빈 상태` |

## 3. 색상·글자·숫자·간격

### 색상

| 용도 | 색상 | PPT 위치 |
| --- | --- | --- |
| 브랜드와 활성 상태 | 본사 브랜드, 주요 메뉴와 선택 요소의 활성 상태에 헤리티지 레드 `#A50034`를 쓴다. 원색과 불투명도 20% 견본을 제시한다. | 19장 `주요 색상` |
| 기본·보조 글자 | 기본 검정 `#000000`, 보조 회색 `#8C8C8C` | 19장 `텍스트 색상` |
| 테두리와 구분선 | 옅은 회색 `#D9D6D1` | 19장 `테두리색상` |
| 배경 | 연한 베이지 `#F0ECE4`, 연한 회색 `#F7F6F4`, 흰색 `#FFFFFF` | 20장 `배경 및 영역 색상` |
| 데이터 테두리·채우기 견본 | 기본 테두리 `#626262`, 청록 계열 테두리 `#8CBFC0`와 채우기 `#EFF6F6` | 20장 `데이터 색상` |

20장과 21장은 데이터 종류와 상태를 구분하는 다섯 색을 각각 불투명도 100%와 20%로 제시한다. 아래 적용 기준은 21장에 적혀 있다.

| 색상 | 적용 기준 |
| --- | --- |
| 초록 `#279300` | 80% 초과(`Above 80%`), `Yes`(예), 증가·상승, 비교군 |
| 노랑 `#FFC100` | `50–80%` 구간, 비교군 |
| 빨강 `#C00000` | 50% 미만(`Below 50%`), `No`(아니오), 감소·하락 |
| 파랑 `#0059BF` | 비교군 |
| 회색 `#C4C4C4` | 데이터 없음(`-`), `N/A`(해당 없음), 변동 없음 |

### 글자

22장 `타이포그래피`는 LG 스마트체의 Bold, SemiBold, Regular, Light 네 굵기를 소개하고, 제목·본문·보조 문구 등 용도에 따라 아래 규격을 적용하도록 한다.

| 종류 | 굵기 | 크기 |
| --- | --- | --- |
| H1 | Bold | 50px |
| H2 | Bold | 34px |
| H3 | Bold | 30px |
| Body 1 | Bold | 28px |
| Body 2 | SemiBold | 24px |
| Caption | SemiBold | 24px |

### 숫자 표기

| 구분 | 규칙과 예시 |
| --- | --- |
| 정수 | 소수점 없이 표시한다. `10`, `278` |
| 천 단위 | 1,000 단위마다 쉼표를 넣는다. `1,000`, `10,000` |
| 소수 | 소수점 첫째 자리까지 표시한다. `12.5`, `85.3` |
| 퍼센트 | 숫자 뒤에 `%` 기호를 붙인다. `85.2%` |
| 실제 0 | 정수는 `0`, 퍼센트 예시는 `0.0%`다. |
| 데이터 없음 | 대시 `-`로 표시한다. |
| 단위 표기 | 숫자와 단위 사이를 띄우지 않는다. `25.5%` |

출처는 23장 `Number Format System`이다.

### 간격

24장 `Spacing`은 **XS 12px, S 24px, M 36px, L 48px, XL 60px, XXL 72px**을 제시한다. 같은 유형의 요소에는 같은 간격을 사용한다. 관련된 요소끼리는 가깝게 두고 콘텐츠 영역 사이에는 넓은 간격을 둔다.

## 4. 적용 전에 확인할 원문 차이

| 항목 | 가이드 안의 차이 또는 빈칸 |
| --- | --- |
| 탭 이름과 굵기 | 5장 본문은 `Competitor Analysis`(경쟁사 분석), 같은 장의 화면 예시는 `Competitor`(경쟁사)로 표시한다. 5장의 활성 탭은 `semiold`, 기본 탭은 `semibold`, 22장 공통표의 Body 1은 Bold로 적혀 있다. 조회 탭에는 5장의 `semiold`를 오타로 보고 활성·기본 모두 SemiBold를 적용한다. [사용자 결정](DECISIONS.md#2026-11-11-ey-디자인-가이드-순차-적용) |
| 필터 글자 규격 | 6장은 필터 이름에 Body 2 Bold 24px, 입력창 글자에 Caption SemiBold 22px을 지정한다. 22장 공통표에서는 Body 2가 SemiBold 24px, Caption이 SemiBold 24px이다. |
| 데이터 색상 선택 | 21장은 초록·노랑·파랑을 모두 비교군에 쓸 수 있다고 표기한다. 어떤 비교군에 어떤 색을 고정할지와 불투명도 100%·20%를 각각 어디에 쓸지는 가이드에 명시돼 있지 않다. |
| 툴팁 동작 | 16장과 17장은 표시 방식과 디자인을 규정한다. 툴팁을 여는 조작은 지정하지 않는다. |

### 색상 표기와 견본의 차이

위 규격표는 슬라이드에 **글자로 적힌 색상 코드**를 옮겼다. 6장과 7장의 `##f0ece4`는 20장의 `#f0ece4` 표기와 대조해 `#F0ECE4`로 적었다. 19~21장 색상 견본 도형에 실제로 지정된 값과 비교하면 다음 항목이 다르다.

| 항목 | 슬라이드 표기 | 견본에 지정된 값 | PPT 위치 |
| --- | --- | --- | --- |
| 헤리티지 레드 | `#A50034` | `#A50434` | 19장 `주요 색상` |
| 옅은 회색 구분선 | `#D9D6D1` | `#CECBC6` | 19장 `테두리색상` |
| 노랑 | `#FFC100` | `#FFC000` | 20~21장 `데이터 색상` |
| 파랑 | `#0059BF` | `#0058BF` | 20~21장 `데이터 색상` |
| 데이터 회색 | `#C4C4C4` | `#C3C4C4` | 20~21장 `데이터 색상` |
| 빨강 | `#C00000` | `#C10000` | 21장 `데이터 색상 적용 기준` |
| 기본 테두리 | `#626262` | `#616261` | 20장 `데이터 색상` |
| 청록 계열 테두리 | `#8CBFC0` | `#8BBFC0` | 20장 `데이터 색상` |
| 청록 계열 채우기 | `#EFF6F6` | `#F0F7F8` | 20장 `데이터 색상` |
| 연한 베이지 | `#F0ECE4` | `#F0ECE5` | 20장 `배경 및 영역 색상` |
| 연한 회색 배경 | `#F7F6F4` | `#E9E9E6` | 20장 `배경 및 영역 색상` |

20장의 빨강 견본은 글자와 같은 `#C00000`이다. 화면 예시는 PPT에 실린 그림에서 확인했다. 실제 대시보드의 적용 상태는 별도 확인이 필요하다.

### 5장 Tab 적용 전후

[EY 대시보드 디자인 가이드 5장](#05장)의 기준을 1920px 로컬 화면과 비교했다.

| 항목 | PPT 5장 기준 | 적용 전 | 적용 후 |
| --- | --- | --- | --- |
| 메뉴 | Overview, LG Analysis, Competitor Analysis, Raw Table | 본문과 같은 4개 메뉴 | 유지 |
| 배경 | 흰색 `#FFFFFF` | 흰색 `#FFFFFF` | 유지 |
| 배치 | 가로형 | 가로 한 줄 | 유지 |
| 활성 글자 | LG 스마트체, 원문 `semiold`, 28px, `#A50034` | LG 스마트체 Bold 13px, `#A50034` | LG 스마트체 SemiBold 28px, `#A50034` |
| 기본 글자 | LG 스마트체 SemiBold 28px, `#000000` | LG 스마트체 Bold 13px, `#5C5A56` | LG 스마트체 SemiBold 28px, `#000000` |
| 활성 표시 | 하단 강조선 `#A50034` | 하단 강조선 `#A50034` | 유지 |
| 간격 | 균등한 간격, 수치 지정 없음 | 메뉴 사이 38px씩 | 유지 |

활성 글자의 `semiold`는 사용자 결정에 따라 SemiBold로 적용했다. 그림 예시의 `Competitor`와 달리 실제 메뉴는 PPT 본문의 `Competitor Analysis`를 유지했다. 좁은 창에서는 글자 크기를 줄이고 필요한 경우 탭 줄을 가로로 스크롤할 수 있다.

[적용 전 확인](updates/2026-11-11/6011f6464d041a275937d9575be57896.md) · [적용 후 검증](updates/2026-11-11/9682b21d43fa43bb6bc9abdb4fb98041.md)

### 6장 Filter 적용 전후

1920px 로컬 화면에서 공통 조회 필터를 확인했다. [EY 대시보드 디자인 가이드 6장](#06장)

| 항목 | PPT 6장 기준 | 적용 전 | 적용 후 |
| --- | --- | --- | --- |
| 위치 | 콘텐츠 상단 | 탭 바로 아래 | 같은 위치 |
| 필터 항목 구성 | 탭의 데이터에 따라 달라질 수 있음. 그림 예시는 `Country`(국가)와 `Month`(월) | 탭별 구성은 아래 표 참고 | 같은 구성 |
| 필터 배치 | 탭별로 같은 입력창 디자인과 배치 규칙 사용 | 필터 이름 위, 입력창 아래. 단일·다중 입력값의 글자 크기가 달랐음 | 이름 아래에 단일·다중 입력창을 같은 크기로 나란히 배치 |
| 배경 | 페이지 배경 `#F0ECE4` | `#F0ECE4` | 같은 색 |
| 필터 항목의 이름 (예: `Country`) | Body 2, LG 스마트체 Bold 24px, `#8C8C8C` | LG 스마트체 Bold 9.5px, `#9B9993` | LG 스마트체 Bold 24px, `#8C8C8C` |
| 필터 입력창 (예: `Spain`이 들어 있는 상자) | 테두리 `#D9D6D1`, 배경 `#F7F6F4`, 모서리 15px | 테두리 `#D6D4CF`, 배경 `#F7F6F4`, 모서리 4px | 테두리 `#D9D6D1`, 배경 `#F7F6F4`, 모서리 15px |
| 필터 입력창 글자 (예: `Spain`) | Caption, LG 스마트체 SemiBold 22px, 검정 `#000000` | LG 스마트체 Regular 12~12.5px, `#141413` | LG 스마트체 SemiBold 22px, `#000000` |
| 필터 사이 간격 | 균등한 간격 | 10px씩 | 24px씩 |
| 콘텐츠 구분선 | 필터와 콘텐츠 사이에 구분선 | 하단 1px, `#D6D4CF` | 하단 1px, `#D9D6D1` |
| 선택 창 | 예시와 같은 레이아웃. 다중 선택 예시에 체크박스, `Select all`, `Apply` 표시 | 다중 선택에 세 요소가 있었고 단일 선택은 브라우저 기본 목록 | 다중 선택에 흰색 목록, 하단 구분선과 버튼 행 적용. 지원 브라우저의 단일 선택도 같은 목록 스타일 적용 |
| 선택지 글자 (예: 펼친 목록의 `France`) | 그림 2에 표시, 글자 크기 수치 없음 | 6장 첫 적용 때 SemiBold 15px | 입력값과 같은 LG 스마트체 SemiBold 22px |
| 선택 창 하단 버튼 글자 | 그림 2의 `Select all`(전체 선택), `Apply`(적용). 글자 크기 수치 없음 | 6장 첫 적용 때 Bold 14px | 선택지와 같은 크기의 LG 스마트체 Bold 22px. 좁은 창에서는 함께 줄이고 필요하면 버튼을 두 줄에 배치 |

| 조회 탭 | 콘텐츠 상단 필터 항목 (적용 전후 동일) |
| --- | --- |
| Overview | Country(국가), Month(월) |
| LG Analysis | Country(국가), Product(제품군), Retailer(리테일러), Month(월) |
| Competitor Analysis | Country(국가), Product(제품군), Retailer(리테일러), Month(월) |
| Raw Table | Country(국가), Product(제품군), Retailer(리테일러), Start Month(시작 월), End Month(종료 월) |

[로컬 대시보드 Overview](http://127.0.0.1:5173/)의 탭 바로 아래에서 확인할 수 있다. `Country`는 필터 이름, `Spain`을 감싼 상자는 입력창, `Spain`은 입력값이다. 내부 브라우저에서 `Country`에 LG Smart Bold, `Spain`에 LG Smart SemiBold가 실제로 렌더링된 것을 확인했다.

6장 표의 `필터 항목`은 그림 1에서 입력창 위에 회색으로 표시된 이름(`Country`, `Month`)으로 해석했다. 그림 2의 `Spain`, `France`, `Italy` 등은 선택 창을 열었을 때의 선택지다. 그림 2는 목록 배치를 보여 주며 선택지 글자 크기나 색상 코드는 따로 지정하지 않는다. 로컬에서 스타일을 적용한 선택 창의 선택지 글자는 SemiBold 15px에서 입력값과 같은 22px로 조정했다. 글자색은 `#626262`이다. 좁은 창에서도 입력값과 선택지 글자 크기가 함께 줄어든다. [선택지 글자 검증 기록](updates/2026-11-11/ddfd6fbb1d47e564fca0927573d5d58b.md)

6장 상세표의 글자 규격을 적용했다. PPT 그림의 `October 2026`은 예시 값이며 로컬 공개 자료에는 2026년 8월만 있어 월 목록을 열어 표시를 확인했다. 목록 꾸미기를 지원하지 않는 브라우저의 단일 선택에는 브라우저 기본 목록을 사용한다. 화면 폭이 800px 이하이면 글자와 입력창 크기를 조정하고 필요할 때 줄을 바꾼다. [로컬 검증 기록](updates/2026-11-11/49c74853fcd9ad9f3f295e86d89bf5e3.md)

### 7장 Content Area 적용 전후

1920px에서 네 조회 탭의 콘텐츠 영역을 대조했다. [EY 대시보드 디자인 가이드 7장](#07장)

| 항목 | PPT 7장 기준 | 적용 전 | 적용 후 |
| --- | --- | --- | --- |
| 페이지 배경 | `#F0ECE4` | `#F0ECE4` | 같은 색 |
| 별도 카드 제목이 있는 경우 | 연회색 제목 띠 `#F7F6F4`, 흰 본문 `#FFFFFF` | LG Analysis·경쟁사 하위 카드에 연회색 제목 띠와 흰 본문 | LG Analysis의 Conversion 등과 경쟁사 하위 카드에 같은 색 규격 적용 |
| 별도 카드 제목이 없는 경우 | 흰 카드 `#FFFFFF`만 사용. 두 유형은 기본 스타일과 모서리 규격을 공유 | Overview·경쟁사 일부는 흰 카드, Raw Table은 큰 제목이 연회색 띠에 있었음 | Overview·경쟁사 일부·Raw Table은 큰 제목 아래 흰 카드. 두 유형 모두 같은 모서리 규격 |
| 큰 제목 | 카드 밖에 LG 스마트체 Bold 34px | 14~15px. Raw Table은 카드 안 | 네 탭 모두 카드 밖에 LG 스마트체 Bold 34px |
| 모서리 | 25px | 12px | 25px |
| 정보 순서 | 제목 → 참고 설명·부가 정보 → 필터·범례 → 표·차트와 설명. 제목 외에는 카드 안 | Overview URL 섹션의 설명·필터, 경쟁사 설명, Raw Table 표 종류 선택이 카드 밖 | 설명과 콘텐츠별 필터를 카드 안의 표·차트 위에 배치. 6장의 탭 공통 필터는 콘텐츠 위에 위치 |
| 배치·정렬 | 탭별 분석 목적에 맞게 지표·표·차트를 구성하고 공통 여백·정렬 적용 | 탭별 단일·다열 배치와 카드별 안쪽 여백 | 탭별 지표·표·차트 배치를 사용하고 카드 안쪽 좌우 여백을 공통 적용. 좁은 창에서 제목과 여백을 조정 |

1920px과 390px에서 네 탭을 열어 제목, 카드, 데이터 표시를 확인했다. Raw Table의 Conversion·Visibility 전환도 확인했다. 8·9장의 사방 48px은 다음 장의 별도 규격이다. [로컬 검증 기록](updates/2026-11-11/b99245979804594a67bbb0fdafd36e76.md)

## 5. PPT 1~24장 원문

표지와 구분 장을 포함해 원본 순서대로 옮겼다. 철자, 대소문자, 문장부호, 색상 코드와 반복 문구를 유지했다. 표에서 `│`는 셀 경계, `↵`는 같은 셀 안의 줄바꿈이다. 그림에 인쇄된 글자도 각 장 아래에 옮겼다. 슬라이드 위에서 편집할 수 있는 그림 설명과 영역 이름은 슬라이드 본문에 들어 있다. [두레이 메일과 첨부 원본](https://codestep.dooray.com/mail/systems/inbox/4463206556762037995)

### 01장

```text
Dashboard Design Guide
```

### 02장

```text
Dashboard Design Guide
1. 공통 레이아웃
```

### 03장

```text
Design Working Specification
1. 제작 프로그램 : Adobe Photoshop
2. 작업 기준 해상도 : 가로 1920px
3. 해상도 : 72ppi
4. 기준화면 : Desktop Web (가로 1920px)
Dashboard Design Guide
```

### 04장

```text
Layout System  공통 레이아웃
1. Header
* 모든 탭에서 동일한 헤더 구조를 유지하며, 브랜드 로고와 대시보드 타이틀을 좌측에 배치하고 Glossary 등 기능을 우측에 배치
Dashboard Design Guide
 │ 디자인 규칙 │ 비고
위치 │ 페이지 최상단 고정 │
Background color │ Gradient │ Color #000000 - #A50034 그라데이션
Logo │ LG Electronic 로고 배치 │
Title │ Dashboard 명칭 표시 │ *H2 : LG스마트체 / Bold / 34px
Utility │ 우측 Glossary 버튼 배치 │
```

**그림 1에 적힌 글자**

```text
LG Electronics | Home Appliance Solution Retail Clinic Dashboard
Glossary
```

### 05장

```text
Layout System  공통 레이아웃
2. Tab
* Overview, LG Analysis, Competitor Analysis, Raw Table의 주요 메뉴를 표시합니다.
  선택된 탭은 Primary Accent Color(#A50034)와 하단 강조선을 적용하여 활성 상태를 구분합니다.
Dashboard Design Guide
 │ 디자인 규칙 │ 비고
Background color │ White │ Color #ffffff
Layout │ 가로형 │
활성 Text │ Primary Accent Color │ *Body 1 : LG스마트체 / semiold / 28px / #A50034
기본 Text │ 주요 텍스트 컬러 │ *Body 1 : LG스마트체 /semibold / 28px / #000000
활성 Indicator │ 하단 강조선 │ #A50034
간격 │ 균등한 간격 │
```

**그림 1에 적힌 글자**

```text
Overview
LG Analysis
Competitor
Raw Table
```

### 06장

```text
Layout System  공통 레이아웃
3. Filter
* 데이터 조회에 필요한 필터를 배치합니다.
   각 탭의 데이터 특성에 따라 필터 항목은 달라질 수 있으나 입력창의 디자인과 레이아웃 규칙은 동일하게 유지합니다.
* 필터와 콘텐츠 영역 사이 구분선 추가 필요
Dashboard Design Guide
 │ 디자인 규칙 │ 비고
위치 │ 콘텐츠 상단에 배치 │
Background color │ Page Backround Color │ Color ##f0ece4
필터 항목 │  │ *Body 2 : LG스마트체 / Bold / 24px / #8c8c8c
필터 입력창 │ Border : #d9d6d1 ↵ Fill : #f7f6f4 │ Radius : 15px
필터 입력창 Text │ 주요 텍스트 컬러 │ * Caption : LG스마트체 / Semi Bold / 22px /      #000000
간격 │ 균등한 간격 │
* 필터 선택 창
  위 레이아웃으로 통일
```

**그림 1에 적힌 글자**

```text
Country
Month
Spain
October 2026
```

**그림 2에 적힌 글자**

```text
Spain
France
Italy
Netherlands
Sweden
Poland
Czech
Select all
Apply
```

### 07장

```text
Layout System  공통 레이아웃
4. Content Area
* 각 탭의 분석 목적에 따라 KPI, 차트, 테이블 등의 콘텐츠를 구성합니다.
  콘텐츠별 배치는 유동적으로 적용하되 공통적인 여백, 정렬 및 컴포넌트 디자인 기준을 유지합니다.
Dashboard Design Guide
 │ 디자인 규칙 │ 비고
Background color │ Page Backround Color │ Color ##f0ece4
Content Surface │ Header : #f7f6f4 ↵ Content : #ffffff │ 콘텐츠별 제목이 있는 경우 별도 Header 영역 적용 ↵ 별도 제목이 없는 경우 Header없이 White Color Content Surface 사용 ↵ 두 유형 모두 콘텐츠영역의 기본 스타일과 모서리 규격을 동일하게 유지
Title │ *H2 : LG스마트체 / Bold / 34px │ Title을 제외한 콘텐츠의 모든 요소들은 Content Surface Box 내에 기입
Radius │ 25px │
정보 배치 순서 │ 1. 콘텐츠 제목 ↵ 2. 참고설명 및 부가정보 ↵ 3. 필터 및 범례 ↵ 4. 데이터 영역 (Table&Chart) 및 설명 │
Layout │ 콘텐츠 특성에 따른 유동 배치 │
```

### 08장

```text
Layout System  공통 레이아웃
4. Content Area
(1) With Header
사방여백 : 48px
Dashboard Design Guide
```

**그림 1에 적힌 글자**

```text
KPI Status
Conversion
Contents Area
```

**그림 2에 적힌 글자**

```text
KPI Status
Conversion
Contents Area
```

### 09장

```text
Layout System  공통 레이아웃
4. Content Area
(2) Without Header
사방여백 : 48px
Dashboard Design Guide
```

**그림 1에 적힌 글자**

```text
Overview
Contents Area
```

### 10장

```text
Layout System  공통 레이아웃
4-1. Content Area – 텍스트 입력 가능 영역 (단일 콘텐츠가 단일 Insight/Descipt 및 필터를 사용하는 경우)
모든 텍스트(insignt/Description, 필터, 주요수치 등)는 타이틀을 제외하고 콘텐츠 영역(흰색 박스) 안에 배치하는 것을 원칙으로 합니다.
Dashboard Design Guide
제목 영역
Insight / Description
Filter
콘텐츠 영역
Content (Table / Chart etc.)
```

**그림 1에 적힌 글자**

```text
Title Area
```

### 11장

```text
Layout System  공통 레이아웃
4-1. Content Area – 텍스트 입력 가능 영역 (콘텐츠에 별도의 타이틀이 있는 경우)
모든 텍스트(insignt/Description, 필터, 주요수치 등)는 타이틀을 제외하고 콘텐츠 영역(흰색 박스) 안에 배치하는 것을 원칙으로 합니다.
Dashboard Design Guide
제목 영역
Insight / Description
Filter
콘텐츠 영역
Content (Table / Chart etc.)
```

**그림 1에 적힌 글자**

```text
Title1 Area
Title 2
```

### 12장

```text
Layout System  공통 레이아웃
4-1. Content Area – 텍스트 입력 가능 영역 (여러 콘텐츠가 하나의 Insight/Descipt 및 필터를 공유하는 경우)
모든 텍스트(insignt/Description, 필터, 주요수치 등)는 타이틀을 제외하고 콘텐츠 영역(흰색 박스) 안에 배치하는 것을 원칙으로 합니다.
Dashboard Design Guide
제목 영역
Filter
Insight / Description
Insight / Description / Filter
Insight / Description / Filter
콘텐츠 영역
Content (Table / Chart etc.)
Content (Table / Chart etc.)
```

**그림 1에 적힌 글자**

```text
Title1 Area
Title 2
Title 3
```

### 13장

```text
Dashboard Design Guide
2. 컴포넌트 가이드
```

### 14장

```text
Component Guide  컴포넌트 가이드
1. KPI 카드
Dashboard Design Guide
 │ 디자인 규칙 │ 비고
card color │ 상단 : #f7f6f4 ↵ 내용(주 배경) : #ffffff │ 카드 상단에 지표명을 기입
container │ 동일한 카드 형태 및 모서리 규격 적용 │ 사각형 형태 ↵ Radius : 25px
padding │ 카드 내부 여백 통일 │ 공통 레이아웃 content area 참고
정보 배치 순서 │ 1. 콘텐츠 제목 ↵ 2. 참고설명 및 부가정보 ↵ 3. 필터 및 범례 ↵ 4. 데이터 영역 (Table&Chart) │
text │ Typography Scale Usage와 ↵ Data Color System에 맞게 사용 │
레이아웃 │ 주요 수치 및 보조 정보의 레이아웃 기준 통일 │
```

### 15장

```text
Component Guide  컴포넌트 가이드
2. 표
Dashboard Design Guide
 │ 디자인 규칙 │ 비고
헤더 │ 헤더 배경색 및 상하 여백 통일 │ 헤더 배경색 : #f7f6f4
행 │ 행 높이 및 행 간격 통일 │ 같은 행 안에서는 동일한 상하여백을 유지
각 셀 │ 셀 내부 여백 및 정렬 기준 적용 │ 각 콘텐츠 별로 셀 크기와 사방여백은 동일하게 유지
정렬 기준 │ 숫자 : 우측정렬 또는 중앙정렬 ↵ 숫자 외 텍스트 : 좌측정렬 또는 중앙정렬 │
구분선 │ 동일한 두께의 구분선 사용 │
```

### 16장

```text
Component Guide  컴포넌트 가이드
3. 차트
Dashboard Design Guide
 │ 디자인 규칙 │ 비고
헤더 │ 헤더 배경색 및 상하 여백 통일 │ 헤더 배경색 : #f7f6f4
차트 내  요소 위치 │ 보조문구 : 헤더 바로 아래 또는 우측에 위치 │
 │ 범례 : 보조문구 바로 아래 또는 우측에 위치 │
 │ 필터 : 콘텐츠 영역의 가장 우측에 위치 │
데이터 구성 요소 │ 선 : 선 굵기 및 연결 형태 통일 │
 │ 레이블 : 툴팁으로 표시 │
 │ 범례 : 차트와 범례 간 배치 및 간격 통일 │
구분선 │ 동일한 두께의 구분선 사용 │
4. 필터
 │ 디자인 규칙 │ 비고
모서리 반경 │ Radius : 15px │
필터 항목 텍스트 위치 │ 필터 항목 텍스트 아래에 필터가 위치 │
```

### 17장

```text
Component Guide  컴포넌트 가이드
5. 범례
Dashboard Design Guide
 │ 디자인 규칙 │ 비고
컬러표시 요소 크기 │ 원형 지름 15px │
레이아웃 │ 가로형 │
6. 툴팁
 │ 디자인 규칙 │ 비고
색상 │ fill #ffffff ↵ 기본 Border #626262 │ 차트 및 그래프에 비교할 데이터가 많은 경우 ↵ Border는 각 데이터의 색상에 따라 변경
레이아웃 │ 좌측 정렬 ↵ 줄바꿈을 적용하여 정보 구분 │
7. 빈 상태
 │ 디자인 규칙 │ 비고
안내 문구 │ 중앙정렬 │
```

### 18장

```text
Dashboard Design Guide
3. 스타일 기준
```

### 19장

```text
Color System  컬러팔레트 및 사용규칙
주요 색상
본사 브랜드, 주요 메뉴 및 선택 요소의 활성 상태를 강조하기 위한 포인트
Dashboard Design Guide
헤리티지 레드
#A50034
헤리티지 레드
Opacity 20%
텍스트 색상
일반 텍스트 및 보조정보 기재 시 사용
검정색
#000000
회색
#8c8c8c
테두리색상
테두리 및 구분선
옅은 회색
#d9d6d1
```

### 20장

```text
Color System  컬러팔레트 및 사용규칙
데이터 색상
데이터 구분 및 데이터의 추가적인 속성 및 조건 표시
Dashboard Design Guide
빨강색
#c00000
노란색
#ffc100
초록색
#279300
파랑색
#0059bf
회색
#c4c4c4
빨강색
Opacity 20%
노란색
Opacity 20%
초록색
Opacity 20%
파랑색
Opacity 20%
회색
Opacity 20%
Border
#626262
Border
#8cbfc0
Fill
#eff6f6
배경 및 영역 색상
전체 배경 및 콘텐츠 영역, 필터 영역 색상
연한 베이지
#f0ece4
연한 회색
#f7f6f4
흰색
#ffffff
```

### 21장

```text
Color System  컬러팔레트 및 사용규칙
데이터 색상 적용 기준
Dashboard Design Guide

초록 #279300
opacity
100%
opacity
20%
적용 기준
1) Above 80%
2) Yes
3) 증가 · 상승
4) 비교군

노랑 #ffc100
opacity
100%
opacity
20%
적용 기준
1) 50-80%
2) 비교군

빨강 #c00000
opacity
100%
opacity
20%
적용 기준
1) Below 50%
2) No
3) 감소 · 하락

파랑 #0059bf
opacity
100%
opacity
20%
적용 기준
1) 비교군

회색 #c4c4c4
opacity
100%
opacity
20%
적용 기준
1) No data (-)
2) N/A
3) 변동없음
```

### 22장

```text
Typhography Guide 타이포그래피
타이포그래피
상황별로 알맞은 타입 스타일을 적용하여 사용
Dashboard Design Guide
LG 스마트체 │ Bold / SemiBold / Regular / light │
H1 │ LG 스마트체 Bold │ 50px
H2 │ LG 스마트체 Bold │ 34px
H3 │ LG 스마트체 Bold │ 30px
Body 1 │ LG 스마트체 Bold │ 28px
Body 2 │ LG 스마트체 Semibold │ 24px
Caption │ LG 스마트체 SemiBold │ 24px
```

### 23장

```text
Number Format System 숫자표기
숫자 표기
상황별로 알맞은 타입 스타일을 적용하여 사용
Dashboard Design Guide
 │ 표기규칙 │ 예시
정수 │ 소수점없이 표시 │ 10 / 278
천 단위 구분 │ 1,000 단위마다 쉼표(,) 사용 │ 1,000 / 10,000
소수점 │ 소수점 첫째 자리까지 표기 │ 12.5 / 85.3
퍼센트 │ 숫자 뒤에 % 기호 사용 │ 85.2%
0값 │ 실제 데이터가 0인 경우 0으로 표시 │ 0 / 0.0%
데이터 없음 │ 데이터가 없는 경우 대시(-) 표시 │ -
단위 표기 │ 숫자와 단위 사이 간격 없음 │ 25.5%
```

### 24장

```text
Spacing 간격
간격
요소의 크기와 배치에 따라 XS부터 XXL까지 단계별 간격을 사용
동일한 유형의 컴포넌트는 일관된 간격을 유지
관련성이 높은 요소는 좁은 간격을, 서로 다른 콘텐츠의 영역은 넓은 간격 적용
Dashboard Design Guide
XS
12px
S
24px
M
36px
L
48px
XL
60px
XXL
72px
```
