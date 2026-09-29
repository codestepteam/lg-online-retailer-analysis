# S05 시트 38 _URL_Calc

원본 파일: `★EY_LGE_Clinic_Assessment Summary_Improvement Tracker_V0.1_20260911 (1).xlsx`

시트: `_URL_Calc` · 상태: `hidden` · 범위: 값이 있는 첫 12행 + 수식 첫 12개 표본

빈 셀은 생략했다. 병합 셀의 값은 시작 셀에만 있으며 자동 채움하지 않았다. 캐시값은 재계산 결과가 아니다.

병합 범위: 없음

숨김 행: 없음

숨김 열 번호: 없음

## Row 1

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A1 | [Retailer 매핑] RawData |  |
| B1 | Improvement Task |  |
| D1 | [Country 매핑] RawData |  |
| E1 | Improvement Task |  |
| G1 | [Category 매핑] RawData |  |
| H1 | Improvement Task |  |
| FO1 | 7197 | =ROWS(_xlfn.ANCHORARRAY(FP3)) |
| GA1 | 7120 | =SUMPRODUCT(--(INDEX(_xlfn.ANCHORARRAY(GB3),,7)&gt;0)) [OOXML {"t": "array", "ref": "GA1"}] |
| GI1 | 433 | =ROWS(_xlfn.ANCHORARRAY('Improvement Task'!B3)) |
| GO1 | 7120 | =ROWS(_xlfn.ANCHORARRAY(GP3)) |
| GY1 | #VALUE! | =_xlfn.LET(_xlpm.a,_xlfn.ANCHORARRAY(GB3),_xlpm.cat,INDEX(_xlpm.a,,3),_xlpm.blank,(_xlpm.cat=0)+(_xlpm.cat=""),_xlpm.f,_xlfn._xlws.FILTER(INDEX(_xlpm.a,,1)&amp;"&#124;"&amp;INDEX(_xlpm.a,,2)&amp;"&#124;"&amp;INDEX(_xlpm.a,,4),_xlpm.blank&gt;0),_xlfn.TEXTJOIN(" ; ",TRUE,_xlfn.UNIQUE(_xlpm.f))) [OOXML {"t": "array", "ref": "GY1"}] |
| HB1 | 433 | =ROWS(_xlfn.ANCHORARRAY('Improvement Task'!$B$3)) |

## Row 2

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A2 | Alza |  |
| B2 | Alza |  |
| D2 | Spain |  |
| E2 | Spain |  |
| G2 | REF |  |
| H2 | REF |  |
| J2 | ID8 |  |
| P2 | ID9 |  |
| V2 | ID10 |  |
| AB2 | ID11 |  |
| AH2 | ID12 |  |
| AN2 | ID13 |  |
| AT2 | ID14 |  |
| AZ2 | ID24 |  |
| BF2 | ID25 |  |
| BL2 | ID33 |  |
| BR2 | ID35 |  |
| BX2 | ID45 |  |
| CD2 | ID43 |  |
| CJ2 | ID34 |  |
| CP2 | ID39 |  |
| CV2 | ID40 |  |
| DB2 | ID46 |  |
| DH2 | ID29 |  |
| DN2 | ID44 |  |
| DT2 | ID37 |  |
| DZ2 | ID38 |  |
| EF2 | ID18 |  |
| EL2 | ID19 |  |
| ER2 | ID20 |  |
| EX2 | ID21 |  |
| FD2 | ID22 |  |
| FJ2 | ID23 |  |
| FP2 | 통합 스택 |  |
| FV2 | URL공백 제외건 |  |
| GA2 | 7197 | =ROWS(_xlfn.ANCHORARRAY(GB3)) |
| GB2 | 정규화+매칭 |  |
| GI2 | ECI | =IFERROR(_xlfn.XLOOKUP("Elcorteingles_electronica",$A$2:$A$15,$B$2:$B$15),"NG") |
| GJ2 | 미매칭 키별 건수 |  |
| GM2 | 미매칭 사유 |  |
| GP2 | 최종 출력 |  |
| HB2 | a-&gt;1 ; b-&gt;2 | =_xlfn.TEXTJOIN(" ; ",TRUE,{"a","b"}&amp;"-&gt;"&amp;{1,2}) [OOXML {"t": "array", "ref": "HB2"}] |

## Row 3

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A3 | Amazon |  |
| B3 | Amazon |  |
| D3 | Italy |  |
| E3 | Italy |  |
| G3 | WM |  |
| H3 | W/M |  |
| J3 | 8 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID8'!$A:$A,2,-1)),_xlpm.xc,'ID8'!$C$2:INDEX('ID8'!$C:$C,_xlpm.n),_xlpm.xd,'ID8'!$D$2:INDEX('ID8'!$D:$D,_xlpm.n),_xlpm.xe,'ID8'!$E$2:INDEX('ID8'!$E:$E,_xlpm.n),_xlpm.xf,'ID8'!$F$2:INDEX('ID8'!$F:$F,_xlpm.n),_xlpm.xh,'ID8'!$H$2:INDEX('ID8'!$H:$H,_xlpm.n),_xlpm.xi,'ID8'!$I$2:INDEX('ID8'!$I:$I,_xlpm.n),_xlpm.xj,'ID8'!$J$2:INDEX('ID8'!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xi="Brand Category Page 영역 내 Alt text 적용 여부")*(_xlpm.xj="N"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,8,8),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "J3:N22"}] |
| K3 | Italy |  |
| L3 | Amazon |  |
| M3 | 0 |  |
| N3 | https://www.amazon.it/stores/page/CFD4D966-B596-4662-9305-AE3889DCC47C?ingress=0&amp;visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde |  |
| P3 | 9 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID9'!$A:$A,2,-1)),_xlpm.xc,'ID9'!$C$2:INDEX('ID9'!$C:$C,_xlpm.n),_xlpm.xd,'ID9'!$D$2:INDEX('ID9'!$D:$D,_xlpm.n),_xlpm.xe,'ID9'!$E$2:INDEX('ID9'!$E:$E,_xlpm.n),_xlpm.xf,'ID9'!$F$2:INDEX('ID9'!$F:$F,_xlpm.n),_xlpm.xh,'ID9'!$H$2:INDEX('ID9'!$H:$H,_xlpm.n),_xlpm.xk,'ID9'!$K$2:INDEX('ID9'!$K:$K,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk="N"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,9,9),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "P3:T8"}] |
| Q3 | Italy |  |
| R3 | Amazon |  |
| S3 | 0 |  |
| T3 | https://www.amazon.it/stores/page/CFD4D966-B596-4662-9305-AE3889DCC47C?ingress=0&amp;visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde |  |
| V3 |  | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID10'!$A:$A,2,-1)),_xlpm.xc,'ID10'!$C$2:INDEX('ID10'!$C:$C,_xlpm.n),_xlpm.xd,'ID10'!$D$2:INDEX('ID10'!$D:$D,_xlpm.n),_xlpm.xe,'ID10'!$E$2:INDEX('ID10'!$E:$E,_xlpm.n),_xlpm.xf,'ID10'!$F$2:INDEX('ID10'!$F:$F,_xlpm.n),_xlpm.xh,'ID10'!$H$2:INDEX('ID10'!$H:$H,_xlpm.n),_xlpm.xi,'ID10'!$I$2:INDEX('ID10'!$I:$I,_xlpm.n),_xlpm.xj,'ID10'!$J$2:INDEX('ID10'!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xi="Canonical URL / 페이지 URL 동일 여부")*(_xlpm.xj="N"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,10,10),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "V3:Z3"}] |
| AB3 | 11 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID11'!$A:$A,2,-1)),_xlpm.xc,'ID11'!$C$2:INDEX('ID11'!$C:$C,_xlpm.n),_xlpm.xd,'ID11'!$D$2:INDEX('ID11'!$D:$D,_xlpm.n),_xlpm.xe,'ID11'!$E$2:INDEX('ID11'!$E:$E,_xlpm.n),_xlpm.xf,'ID11'!$F$2:INDEX('ID11'!$F:$F,_xlpm.n),_xlpm.xi,'ID11'!$I$2:INDEX('ID11'!$I:$I,_xlpm.n),_xlpm.xk,'ID11'!$K$2:INDEX('ID11'!$K:$K,_xlpm.n),_xlpm.xl,'ID11'!$L$2:INDEX('ID11'!$L:$L,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk="존재")*(_xlpm.xl="N"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,11,11),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "AB3:AF21"}] |
| AC3 | France |  |
| AD3 | Boulanger |  |
| AE3 | WM |  |
| AF3 | https://www.boulanger.com/resultats?tr=s%C3%A9choir |  |
| AH3 | 12 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID12'!$A:$A,2,-1)),_xlpm.xc,'ID12'!$C$2:INDEX('ID12'!$C:$C,_xlpm.n),_xlpm.xd,'ID12'!$D$2:INDEX('ID12'!$D:$D,_xlpm.n),_xlpm.xe,'ID12'!$E$2:INDEX('ID12'!$E:$E,_xlpm.n),_xlpm.xf,'ID12'!$F$2:INDEX('ID12'!$F:$F,_xlpm.n),_xlpm.xi,'ID12'!$I$2:INDEX('ID12'!$I:$I,_xlpm.n),_xlpm.xk,'ID12'!$K$2:INDEX('ID12'!$K:$K,_xlpm.n),_xlpm.xl,'ID12'!$L$2:INDEX('ID12'!$L:$L,_xlpm.n),_xlpm.xm,'ID12'!$M$2:INDEX('ID12'!$M:$M,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk="PDP 영역 내 Alt text 적용 여부")*(_xlpm.xl="N")*(_xlpm.xm="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,12,12),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "AH3:AL550"}] |
| AI3 | Czech |  |
| AJ3 | Alza |  |
| AK3 | WM |  |
| AL3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| AN3 | 13 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID13'!$A:$A,2,-1)),_xlpm.xc,'ID13'!$C$2:INDEX('ID13'!$C:$C,_xlpm.n),_xlpm.xd,'ID13'!$D$2:INDEX('ID13'!$D:$D,_xlpm.n),_xlpm.xe,'ID13'!$E$2:INDEX('ID13'!$E:$E,_xlpm.n),_xlpm.xf,'ID13'!$F$2:INDEX('ID13'!$F:$F,_xlpm.n),_xlpm.xi,'ID13'!$I$2:INDEX('ID13'!$I:$I,_xlpm.n),_xlpm.xp,'ID13'!$P$2:INDEX('ID13'!$P:$P,_xlpm.n),_xlpm.xr,'ID13'!$R$2:INDEX('ID13'!$R:$R,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xp=1)*(_xlpm.xr="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,13,13),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,_xlfn.HSTACK("","","","",""))) [OOXML {"t": "array", "ref": "AN3:AR18"}] |
| AO3 | Sweden |  |
| AP3 | Elgiganten |  |
| AQ3 | WM |  |
| AR3 | https://www.elgiganten.se/product/outlet/lg-kombinerad-tvattmaskintorktumlare-cv94e7s2ba-116kg/651718 |  |
| AT3 | 14 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID14'!$A:$A,2,-1)),_xlpm.xc,'ID14'!$C$2:INDEX('ID14'!$C:$C,_xlpm.n),_xlpm.xd,'ID14'!$D$2:INDEX('ID14'!$D:$D,_xlpm.n),_xlpm.xe,'ID14'!$E$2:INDEX('ID14'!$E:$E,_xlpm.n),_xlpm.xf,'ID14'!$F$2:INDEX('ID14'!$F:$F,_xlpm.n),_xlpm.xi,'ID14'!$I$2:INDEX('ID14'!$I:$I,_xlpm.n),_xlpm.xk,'ID14'!$K$2:INDEX('ID14'!$K:$K,_xlpm.n),_xlpm.xl,'ID14'!$L$2:INDEX('ID14'!$L:$L,_xlpm.n),_xlpm.xm,'ID14'!$M$2:INDEX('ID14'!$M:$M,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk="PDP 내 순환 경로 존재 여부")*(_xlpm.xl="N")*(_xlpm.xm="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,14,14),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "AT3:AX96"}] |
| AU3 | France |  |
| AV3 | Darty |  |
| AW3 | REF |  |
| AX3 | https://www.darty.com/nav/achat/gros_electromenager/refrigerateur_congelateur-refrigerateur-cong/refrigerateur_congelateur_bas/lg_gbbs322cev.html |  |
| AZ3 | 24 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID24'!$A:$A,2,-1)),_xlpm.xc,'ID24'!$C$2:INDEX('ID24'!$C:$C,_xlpm.n),_xlpm.xd,'ID24'!$D$2:INDEX('ID24'!$D:$D,_xlpm.n),_xlpm.xe,'ID24'!$E$2:INDEX('ID24'!$E:$E,_xlpm.n),_xlpm.xf,'ID24'!$F$2:INDEX('ID24'!$F:$F,_xlpm.n),_xlpm.xi,'ID24'!$I$2:INDEX('ID24'!$I:$I,_xlpm.n),_xlpm.xk,'ID24'!$K$2:INDEX('ID24'!$K:$K,_xlpm.n),_xlpm.xl,'ID24'!$L$2:INDEX('ID24'!$L:$L,_xlpm.n),_xlpm.xn,'ID24'!$N$2:INDEX('ID24'!$N:$N,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk=1)*(_xlpm.xl=0)*(_xlpm.xn="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,24,24),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "AZ3:BD636"}] |
| BA3 | Czech |  |
| BB3 | Alza |  |
| BC3 | WM |  |
| BD3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| BF3 | 25 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID25'!$A:$A,2,-1)),_xlpm.xc,'ID25'!$C$2:INDEX('ID25'!$C:$C,_xlpm.n),_xlpm.xd,'ID25'!$D$2:INDEX('ID25'!$D:$D,_xlpm.n),_xlpm.xe,'ID25'!$E$2:INDEX('ID25'!$E:$E,_xlpm.n),_xlpm.xf,'ID25'!$F$2:INDEX('ID25'!$F:$F,_xlpm.n),_xlpm.xi,'ID25'!$I$2:INDEX('ID25'!$I:$I,_xlpm.n),_xlpm.xj,'ID25'!$J$2:INDEX('ID25'!$J:$J,_xlpm.n),_xlpm.xk,'ID25'!$K$2:INDEX('ID25'!$K:$K,_xlpm.n),_xlpm.xw,'ID25'!$W$2:INDEX('ID25'!$W:$W,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xj=1)*(_xlpm.xk=0)*(_xlpm.xw="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,25,25),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "BF3:BJ292"}] |
| BG3 | Czech |  |
| BH3 | Alza |  |
| BI3 | WM |  |
| BJ3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| BL3 | 33 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID33'!$A:$A,2,-1)),_xlpm.xc,'ID33'!$C$2:INDEX('ID33'!$C:$C,_xlpm.n),_xlpm.xd,'ID33'!$D$2:INDEX('ID33'!$D:$D,_xlpm.n),_xlpm.xe,'ID33'!$E$2:INDEX('ID33'!$E:$E,_xlpm.n),_xlpm.xf,'ID33'!$F$2:INDEX('ID33'!$F:$F,_xlpm.n),_xlpm.xi,'ID33'!$I$2:INDEX('ID33'!$I:$I,_xlpm.n),_xlpm.xl,'ID33'!$L$2:INDEX('ID33'!$L:$L,_xlpm.n),_xlpm.xt,'ID33'!$T$2:INDEX('ID33'!$T:$T,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xl=0)*(_xlpm.xt="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,33,33),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "BL3:BP149"}] |
| BM3 | Czech |  |
| BN3 | Alza |  |
| BO3 | WM |  |
| BP3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| BR3 | 35 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID35'!$A:$A,2,-1)),_xlpm.xc,'ID35'!$C$2:INDEX('ID35'!$C:$C,_xlpm.n),_xlpm.xd,'ID35'!$D$2:INDEX('ID35'!$D:$D,_xlpm.n),_xlpm.xe,'ID35'!$E$2:INDEX('ID35'!$E:$E,_xlpm.n),_xlpm.xf,'ID35'!$F$2:INDEX('ID35'!$F:$F,_xlpm.n),_xlpm.xi,'ID35'!$I$2:INDEX('ID35'!$I:$I,_xlpm.n),_xlpm.xk,'ID35'!$K$2:INDEX('ID35'!$K:$K,_xlpm.n),_xlpm.xo,'ID35'!$O$2:INDEX('ID35'!$O:$O,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk=0)*(_xlpm.xo="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,35,35),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "BR3:BV165"}] |
| BS3 | Czech |  |
| BT3 | Alza |  |
| BU3 | WM |  |
| BV3 | https://www.alza.cz/lg-wt1210bbf-d7850423.htm |  |
| BX3 | 45 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID45'!$A:$A,2,-1)),_xlpm.xc,'ID45'!$C$2:INDEX('ID45'!$C:$C,_xlpm.n),_xlpm.xd,'ID45'!$D$2:INDEX('ID45'!$D:$D,_xlpm.n),_xlpm.xe,'ID45'!$E$2:INDEX('ID45'!$E:$E,_xlpm.n),_xlpm.xf,'ID45'!$F$2:INDEX('ID45'!$F:$F,_xlpm.n),_xlpm.xi,'ID45'!$I$2:INDEX('ID45'!$I:$I,_xlpm.n),_xlpm.xj,'ID45'!$J$2:INDEX('ID45'!$J:$J,_xlpm.n),_xlpm.xk,'ID45'!$K$2:INDEX('ID45'!$K:$K,_xlpm.n),_xlpm.xr,'ID45'!$R$2:INDEX('ID45'!$R:$R,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xj=1)*(_xlpm.xr="유지")*(ISNUMBER(_xlpm.xk))*(_xlpm.xk&lt;1),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,45,45),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "BX3:CB415"}] |
| BY3 | Czech |  |
| BZ3 | Alza |  |
| CA3 | WM |  |
| CB3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| CD3 | 43 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",ID_43!$A:$A,2,-1)),_xlpm.xc,ID_43!$C$2:INDEX(ID_43!$C:$C,_xlpm.n),_xlpm.xd,ID_43!$D$2:INDEX(ID_43!$D:$D,_xlpm.n),_xlpm.xe,ID_43!$E$2:INDEX(ID_43!$E:$E,_xlpm.n),_xlpm.xf,ID_43!$F$2:INDEX(ID_43!$F:$F,_xlpm.n),_xlpm.xj,ID_43!$J$2:INDEX(ID_43!$J:$J,_xlpm.n),_xlpm.xl,ID_43!$L$2:INDEX(ID_43!$L:$L,_xlpm.n),_xlpm.xs,ID_43!$S$2:INDEX(ID_43!$S:$S,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xl=1)*(_xlpm.xs="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,43,43),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xj),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "CD3:CH116"}] |
| CE3 | France |  |
| CF3 | Darty |  |
| CG3 | REF |  |
| CH3 | https://www.darty.com/nav/achat/gros_electromenager/refrigerateur-refrigerateur/refrigerateur_armoire/lg_glm71mccsd.html |  |
| CJ3 | 34 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID34'!$A:$A,2,-1)),_xlpm.xc,'ID34'!$C$2:INDEX('ID34'!$C:$C,_xlpm.n),_xlpm.xd,'ID34'!$D$2:INDEX('ID34'!$D:$D,_xlpm.n),_xlpm.xe,'ID34'!$E$2:INDEX('ID34'!$E:$E,_xlpm.n),_xlpm.xf,'ID34'!$F$2:INDEX('ID34'!$F:$F,_xlpm.n),_xlpm.xi,'ID34'!$I$2:INDEX('ID34'!$I:$I,_xlpm.n),_xlpm.xl,'ID34'!$L$2:INDEX('ID34'!$L:$L,_xlpm.n),_xlpm.xm,'ID34'!$M$2:INDEX('ID34'!$M:$M,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xl=0)*(_xlpm.xm="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,34,34),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "CJ3:CN580"}] |
| CK3 | Czech |  |
| CL3 | Alza |  |
| CM3 | WM |  |
| CN3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| CP3 | 39 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID39'!$A:$A,2,-1)),_xlpm.xc,'ID39'!$C$2:INDEX('ID39'!$C:$C,_xlpm.n),_xlpm.xd,'ID39'!$D$2:INDEX('ID39'!$D:$D,_xlpm.n),_xlpm.xe,'ID39'!$E$2:INDEX('ID39'!$E:$E,_xlpm.n),_xlpm.xf,'ID39'!$F$2:INDEX('ID39'!$F:$F,_xlpm.n),_xlpm.xi,'ID39'!$I$2:INDEX('ID39'!$I:$I,_xlpm.n),_xlpm.xk,'ID39'!$K$2:INDEX('ID39'!$K:$K,_xlpm.n),_xlpm.xm,'ID39'!$M$2:INDEX('ID39'!$M:$M,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk=0)*(_xlpm.xm="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,39,39),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "CP3:CT688"}] |
| CQ3 | Czech |  |
| CR3 | Alza |  |
| CS3 | WM |  |
| CT3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| CV3 | 40 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID40'!$A:$A,2,-1)),_xlpm.xc,'ID40'!$C$2:INDEX('ID40'!$C:$C,_xlpm.n),_xlpm.xd,'ID40'!$D$2:INDEX('ID40'!$D:$D,_xlpm.n),_xlpm.xe,'ID40'!$E$2:INDEX('ID40'!$E:$E,_xlpm.n),_xlpm.xf,'ID40'!$F$2:INDEX('ID40'!$F:$F,_xlpm.n),_xlpm.xi,'ID40'!$I$2:INDEX('ID40'!$I:$I,_xlpm.n),_xlpm.xk,'ID40'!$K$2:INDEX('ID40'!$K:$K,_xlpm.n),_xlpm.xm,'ID40'!$M$2:INDEX('ID40'!$M:$M,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk=0)*(_xlpm.xm="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,40,40),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "CV3:CZ724"}] |
| CW3 | Czech |  |
| CX3 | Alza |  |
| CY3 | WM |  |
| CZ3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| DB3 | 46 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID46'!$A:$A,2,-1)),_xlpm.xc,'ID46'!$C$2:INDEX('ID46'!$C:$C,_xlpm.n),_xlpm.xd,'ID46'!$D$2:INDEX('ID46'!$D:$D,_xlpm.n),_xlpm.xe,'ID46'!$E$2:INDEX('ID46'!$E:$E,_xlpm.n),_xlpm.xf,'ID46'!$F$2:INDEX('ID46'!$F:$F,_xlpm.n),_xlpm.xi,'ID46'!$I$2:INDEX('ID46'!$I:$I,_xlpm.n),_xlpm.xk,'ID46'!$K$2:INDEX('ID46'!$K:$K,_xlpm.n),_xlpm.xn,'ID46'!$N$2:INDEX('ID46'!$N:$N,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk=0)*(_xlpm.xn="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,46,46),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "DB3:DF724"}] |
| DC3 | Czech |  |
| DD3 | Alza |  |
| DE3 | WM |  |
| DF3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| DH3 | 29 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",ID_29!$A:$A,2,-1)),_xlpm.xc,ID_29!$C$2:INDEX(ID_29!$C:$C,_xlpm.n),_xlpm.xd,ID_29!$D$2:INDEX(ID_29!$D:$D,_xlpm.n),_xlpm.xe,ID_29!$E$2:INDEX(ID_29!$E:$E,_xlpm.n),_xlpm.xf,ID_29!$F$2:INDEX(ID_29!$F:$F,_xlpm.n),_xlpm.xi,ID_29!$I$2:INDEX(ID_29!$I:$I,_xlpm.n),_xlpm.xaf,ID_29!$AF$2:INDEX(ID_29!$AF:$AF,_xlpm.n),_xlpm.xaj,ID_29!$AJ$2:INDEX(ID_29!$AJ:$AJ,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xaf="유지")*(ISNUMBER(_xlpm.xaj))*(_xlpm.xaj&lt;1),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,29,29),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "DH3:DL1021"}] |
| DI3 | Czech |  |
| DJ3 | Alza |  |
| DK3 | WM |  |
| DL3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| DN3 | 44 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",ID_44!$A:$A,2,-1)),_xlpm.xc,ID_44!$C$2:INDEX(ID_44!$C:$C,_xlpm.n),_xlpm.xd,ID_44!$D$2:INDEX(ID_44!$D:$D,_xlpm.n),_xlpm.xe,ID_44!$E$2:INDEX(ID_44!$E:$E,_xlpm.n),_xlpm.xf,ID_44!$F$2:INDEX(ID_44!$F:$F,_xlpm.n),_xlpm.xi,ID_44!$I$2:INDEX(ID_44!$I:$I,_xlpm.n),_xlpm.xaf,ID_44!$AF$2:INDEX(ID_44!$AF:$AF,_xlpm.n),_xlpm.xaj,ID_44!$AJ$2:INDEX(ID_44!$AJ:$AJ,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xaf="유지")*(ISNUMBER(_xlpm.xaj))*(_xlpm.xaj&lt;1),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,44,44),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "DN3:DR561"}] |
| DO3 | Czech |  |
| DP3 | Alza |  |
| DQ3 | WM |  |
| DR3 | https://www.alza.cz/lg-rc91v9av4n-d7375112.htm |  |
| DT3 | 37 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",ID_37_38!$A:$A,2,-1)),_xlpm.xa,ID_37_38!$A$2:INDEX(ID_37_38!$A:$A,_xlpm.n),_xlpm.xc,ID_37_38!$C$2:INDEX(ID_37_38!$C:$C,_xlpm.n),_xlpm.xd,ID_37_38!$D$2:INDEX(ID_37_38!$D:$D,_xlpm.n),_xlpm.xe,ID_37_38!$E$2:INDEX(ID_37_38!$E:$E,_xlpm.n),_xlpm.xf,ID_37_38!$F$2:INDEX(ID_37_38!$F:$F,_xlpm.n),_xlpm.xi,ID_37_38!$I$2:INDEX(ID_37_38!$I:$I,_xlpm.n),_xlpm.xj,ID_37_38!$J$2:INDEX(ID_37_38!$J:$J,_xlpm.n),_xlpm.xl,ID_37_38!$L$2:INDEX(ID_37_38!$L:$L,_xlpm.n),_xlpm.xn,ID_37_38!$N$2:INDEX(ID_37_38!$N:$N,_xlpm.n),_xlpm.m,(_xlpm.xa="ID37")*(_xlpm.xf="LG")*(_xlpm.xl=0)*(_xlpm.xn="유지")*(_xlpm.xj&gt;0),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,37,37),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "DT3:DX9"}] |
| DU3 | Italy |  |
| DV3 | Amazon |  |
| DW3 | REF |  |
| DX3 | https://www.amazon.it/dp/B0GVZG972Y |  |
| DZ3 | 38 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",ID_37_38!$A:$A,2,-1)),_xlpm.xa,ID_37_38!$A$2:INDEX(ID_37_38!$A:$A,_xlpm.n),_xlpm.xc,ID_37_38!$C$2:INDEX(ID_37_38!$C:$C,_xlpm.n),_xlpm.xd,ID_37_38!$D$2:INDEX(ID_37_38!$D:$D,_xlpm.n),_xlpm.xe,ID_37_38!$E$2:INDEX(ID_37_38!$E:$E,_xlpm.n),_xlpm.xf,ID_37_38!$F$2:INDEX(ID_37_38!$F:$F,_xlpm.n),_xlpm.xi,ID_37_38!$I$2:INDEX(ID_37_38!$I:$I,_xlpm.n),_xlpm.xm,ID_37_38!$M$2:INDEX(ID_37_38!$M:$M,_xlpm.n),_xlpm.xn,ID_37_38!$N$2:INDEX(ID_37_38!$N:$N,_xlpm.n),_xlpm.m,(_xlpm.xa="ID38")*(_xlpm.xf="LG")*(_xlpm.xm=0)*(_xlpm.xn="유지"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,38,38),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xi),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "DZ3:ED388"}] |
| EA3 | Czech |  |
| EB3 | Alza |  |
| EC3 | WM |  |
| ED3 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| EF3 | 18 | =_xlfn.LET(_xlpm.n,MAX(7,_xlfn.XMATCH("?*",ID18_19_20_21_22_23!$C:$C,2,-1)),_xlpm.xb,ID18_19_20_21_22_23!$B$7:INDEX(ID18_19_20_21_22_23!$B:$B,_xlpm.n),_xlpm.xc,ID18_19_20_21_22_23!$C$7:INDEX(ID18_19_20_21_22_23!$C:$C,_xlpm.n),_xlpm.xd,ID18_19_20_21_22_23!$D$7:INDEX(ID18_19_20_21_22_23!$D:$D,_xlpm.n),_xlpm.xe,ID18_19_20_21_22_23!$E$7:INDEX(ID18_19_20_21_22_23!$E:$E,_xlpm.n),_xlpm.xg,ID18_19_20_21_22_23!$G$7:INDEX(ID18_19_20_21_22_23!$G:$G,_xlpm.n),_xlpm.xh,ID18_19_20_21_22_23!$H$7:INDEX(ID18_19_20_21_22_23!$H:$H,_xlpm.n),_xlpm.xj,ID18_19_20_21_22_23!$J$7:INDEX(ID18_19_20_21_22_23!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xd="LG")*(_xlpm.xb=18)*(_xlpm.xj=0),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,18,18),_xlpm.xc,_xlpm.xe,_xlpm.xg,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "EF3:EJ18"}] |
| EG3 | Czech |  |
| EH3 | Datart |  |
| EI3 | WM |  |
| EJ3 | https://www.datart.cz/susicky-lg.html |  |
| EL3 | 19 | =_xlfn.LET(_xlpm.n,MAX(7,_xlfn.XMATCH("?*",ID18_19_20_21_22_23!$C:$C,2,-1)),_xlpm.xb,ID18_19_20_21_22_23!$B$7:INDEX(ID18_19_20_21_22_23!$B:$B,_xlpm.n),_xlpm.xc,ID18_19_20_21_22_23!$C$7:INDEX(ID18_19_20_21_22_23!$C:$C,_xlpm.n),_xlpm.xd,ID18_19_20_21_22_23!$D$7:INDEX(ID18_19_20_21_22_23!$D:$D,_xlpm.n),_xlpm.xe,ID18_19_20_21_22_23!$E$7:INDEX(ID18_19_20_21_22_23!$E:$E,_xlpm.n),_xlpm.xg,ID18_19_20_21_22_23!$G$7:INDEX(ID18_19_20_21_22_23!$G:$G,_xlpm.n),_xlpm.xh,ID18_19_20_21_22_23!$H$7:INDEX(ID18_19_20_21_22_23!$H:$H,_xlpm.n),_xlpm.xj,ID18_19_20_21_22_23!$J$7:INDEX(ID18_19_20_21_22_23!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xd="LG")*(_xlpm.xb=19)*(_xlpm.xj=0),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,19,19),_xlpm.xc,_xlpm.xe,_xlpm.xg,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "EL3:EP7"}] |
| EM3 | Czech |  |
| EN3 | Datart |  |
| EO3 | WM |  |
| EP3 | https://www.datart.cz/susicky-lg.html |  |
| ER3 | 20 | =_xlfn.LET(_xlpm.n,MAX(7,_xlfn.XMATCH("?*",ID18_19_20_21_22_23!$C:$C,2,-1)),_xlpm.xb,ID18_19_20_21_22_23!$B$7:INDEX(ID18_19_20_21_22_23!$B:$B,_xlpm.n),_xlpm.xc,ID18_19_20_21_22_23!$C$7:INDEX(ID18_19_20_21_22_23!$C:$C,_xlpm.n),_xlpm.xd,ID18_19_20_21_22_23!$D$7:INDEX(ID18_19_20_21_22_23!$D:$D,_xlpm.n),_xlpm.xe,ID18_19_20_21_22_23!$E$7:INDEX(ID18_19_20_21_22_23!$E:$E,_xlpm.n),_xlpm.xg,ID18_19_20_21_22_23!$G$7:INDEX(ID18_19_20_21_22_23!$G:$G,_xlpm.n),_xlpm.xh,ID18_19_20_21_22_23!$H$7:INDEX(ID18_19_20_21_22_23!$H:$H,_xlpm.n),_xlpm.xj,ID18_19_20_21_22_23!$J$7:INDEX(ID18_19_20_21_22_23!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xd="LG")*(_xlpm.xb=20)*(_xlpm.xj=0),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,20,20),_xlpm.xc,_xlpm.xe,_xlpm.xg,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "ER3:EV16"}] |
| ES3 | Czech |  |
| ET3 | Datart |  |
| EU3 | WM |  |
| EV3 | https://www.datart.cz/susicky-lg.html |  |
| EX3 | 21 | =_xlfn.LET(_xlpm.n,MAX(7,_xlfn.XMATCH("?*",ID18_19_20_21_22_23!$C:$C,2,-1)),_xlpm.xb,ID18_19_20_21_22_23!$B$7:INDEX(ID18_19_20_21_22_23!$B:$B,_xlpm.n),_xlpm.xc,ID18_19_20_21_22_23!$C$7:INDEX(ID18_19_20_21_22_23!$C:$C,_xlpm.n),_xlpm.xd,ID18_19_20_21_22_23!$D$7:INDEX(ID18_19_20_21_22_23!$D:$D,_xlpm.n),_xlpm.xe,ID18_19_20_21_22_23!$E$7:INDEX(ID18_19_20_21_22_23!$E:$E,_xlpm.n),_xlpm.xg,ID18_19_20_21_22_23!$G$7:INDEX(ID18_19_20_21_22_23!$G:$G,_xlpm.n),_xlpm.xh,ID18_19_20_21_22_23!$H$7:INDEX(ID18_19_20_21_22_23!$H:$H,_xlpm.n),_xlpm.xj,ID18_19_20_21_22_23!$J$7:INDEX(ID18_19_20_21_22_23!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xd="LG")*(_xlpm.xb=21)*(_xlpm.xj=0),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,21,21),_xlpm.xc,_xlpm.xe,_xlpm.xg,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "EX3:FB10"}] |
| EY3 | Italy |  |
| EZ3 | MEDIAWORLD |  |
| FA3 | WM |  |
| FB3 | https://www.mediaworld.it/it/brand/lg/asciugatrici |  |
| FD3 |  | =_xlfn.LET(_xlpm.n,MAX(7,_xlfn.XMATCH("?*",ID18_19_20_21_22_23!$C:$C,2,-1)),_xlpm.xb,ID18_19_20_21_22_23!$B$7:INDEX(ID18_19_20_21_22_23!$B:$B,_xlpm.n),_xlpm.xc,ID18_19_20_21_22_23!$C$7:INDEX(ID18_19_20_21_22_23!$C:$C,_xlpm.n),_xlpm.xd,ID18_19_20_21_22_23!$D$7:INDEX(ID18_19_20_21_22_23!$D:$D,_xlpm.n),_xlpm.xe,ID18_19_20_21_22_23!$E$7:INDEX(ID18_19_20_21_22_23!$E:$E,_xlpm.n),_xlpm.xg,ID18_19_20_21_22_23!$G$7:INDEX(ID18_19_20_21_22_23!$G:$G,_xlpm.n),_xlpm.xh,ID18_19_20_21_22_23!$H$7:INDEX(ID18_19_20_21_22_23!$H:$H,_xlpm.n),_xlpm.xj,ID18_19_20_21_22_23!$J$7:INDEX(ID18_19_20_21_22_23!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xd="LG")*(_xlpm.xb=22)*(_xlpm.xj=0),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,22,22),_xlpm.xc,_xlpm.xe,_xlpm.xg,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "FD3:FH3"}] |
| FJ3 | 23 | =_xlfn.LET(_xlpm.n,MAX(7,_xlfn.XMATCH("?*",ID18_19_20_21_22_23!$C:$C,2,-1)),_xlpm.xb,ID18_19_20_21_22_23!$B$7:INDEX(ID18_19_20_21_22_23!$B:$B,_xlpm.n),_xlpm.xc,ID18_19_20_21_22_23!$C$7:INDEX(ID18_19_20_21_22_23!$C:$C,_xlpm.n),_xlpm.xd,ID18_19_20_21_22_23!$D$7:INDEX(ID18_19_20_21_22_23!$D:$D,_xlpm.n),_xlpm.xe,ID18_19_20_21_22_23!$E$7:INDEX(ID18_19_20_21_22_23!$E:$E,_xlpm.n),_xlpm.xg,ID18_19_20_21_22_23!$G$7:INDEX(ID18_19_20_21_22_23!$G:$G,_xlpm.n),_xlpm.xh,ID18_19_20_21_22_23!$H$7:INDEX(ID18_19_20_21_22_23!$H:$H,_xlpm.n),_xlpm.xj,ID18_19_20_21_22_23!$J$7:INDEX(ID18_19_20_21_22_23!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xd="LG")*(_xlpm.xb=23)*(_xlpm.xj=0),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,23,23),_xlpm.xc,_xlpm.xe,_xlpm.xg,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "FJ3:FN19"}] |
| FK3 | Czech |  |
| FL3 | Alza |  |
| FM3 | WM |  |
| FN3 | https://www.alza.cz/pracky/lg/18852774-v1357.htm |  |
| FP3 | 8 | =_xlfn.LET(_xlpm.a,_xlfn.VSTACK(IFERROR(_xlfn.ANCHORARRAY(J3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(P3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(V3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AB3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AH3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AN3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AT3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AZ3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(BF3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(BL3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(BR3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(BX3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(CD3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(CJ3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(CP3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(CV3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DB3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DH3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DN3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DT3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DZ3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(EF3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(EL3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(ER3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(EX3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(FD3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(FJ3),_xlfn.HSTACK("","","","",""))),_xlfn._xlws.FILTER(_xlpm.a,INDEX(_xlpm.a,,5)&lt;&gt;"")) [OOXML {"t": "array", "ref": "FP3:FT7199"}] |
| FQ3 | Italy |  |
| FR3 | Amazon |  |
| FS3 | 0 |  |
| FT3 | https://www.amazon.it/stores/page/CFD4D966-B596-4662-9305-AE3889DCC47C?ingress=0&amp;visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde |  |
| FV3 | 14 | =_xlfn.LET(_xlpm.a,_xlfn.VSTACK(IFERROR(_xlfn.ANCHORARRAY(J3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(P3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(V3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AB3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AH3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AN3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AT3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(AZ3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(BF3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(BL3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(BR3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(BX3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(CD3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(CJ3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(CP3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(CV3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DB3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DH3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DN3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DT3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(DZ3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(EF3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(EL3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(ER3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(EX3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(FD3),_xlfn.HSTACK("","","","","")),IFERROR(_xlfn.ANCHORARRAY(FJ3),_xlfn.HSTACK("","","","",""))),_xlpm.b,_xlfn._xlws.FILTER(_xlpm.a,(INDEX(_xlpm.a,,5)="")*(INDEX(_xlpm.a,,1)&lt;&gt;"")),IFERROR(_xlpm.b,"없음")) [OOXML {"t": "array", "ref": "FV3:FZ8"}] |
| FW3 | Italy |  |
| FX3 | Mediaworld |  |
| FY3 | REF |  |
| GB3 | Italy | =_xlfn.LET(<br> _xlpm.a,_xlfn.ANCHORARRAY(FP3),<br> _xlpm.id,INDEX(_xlpm.a,,1), _xlpm.cty,INDEX(_xlpm.a,,2), _xlpm.rtl,INDEX(_xlpm.a,,3), _xlpm.cat,INDEX(_xlpm.a,,4), _xlpm.url,INDEX(_xlpm.a,,5),<br> _xlpm.nc,IFERROR(INDEX($E$2:$E$9,MATCH(_xlpm.cty,$D$2:$D$9,0)),_xlpm.cty),<br> _xlpm.nr,IFERROR(INDEX($B$2:$B$15,MATCH(_xlpm.rtl,$A$2:$A$15,0)),_xlpm.rtl),<br> _xlpm.ng,IF((_xlpm.cat=0)+(_xlpm.cat="")&gt;0,"ALL",IFERROR(INDEX($H$2:$H$5,MATCH(_xlpm.cat,$G$2:$G$5,0)),_xlpm.cat)),<br> _xlpm.tk,_xlfn.ANCHORARRAY('Improvement Task'!$B$3),<br> _xlpm.tfull,INDEX(_xlpm.tk,,1)&amp;"&#124;"&amp;INDEX(_xlpm.tk,,2)&amp;"&#124;"&amp;INDEX(_xlpm.tk,,3)&amp;"&#124;"&amp;INDEX(_xlpm.tk,,4),<br> _xlpm.tcr,INDEX(_xlpm.tk,,1)&amp;"&#124;"&amp;INDEX(_xlpm.tk,,2)&amp;"&#124;"&amp;INDEX(_xlpm.tk,,4),<br> _xlpm.keyf,_xlpm.nc&amp;"&#124;"&amp;_xlpm.nr&amp;"&#124;"&amp;_xlpm.ng&amp;"&#124;"&amp;_xlpm.id,<br> _xlpm.keyc,_xlpm.nc&amp;"&#124;"&amp;_xlpm.nr&amp;"&#124;"&amp;_xlpm.id,<br> _xlpm.m,IF(_xlpm.ng="ALL",IFERROR(MATCH(_xlpm.keyc,_xlpm.tcr,0),0),IFERROR(MATCH(_xlpm.keyf,_xlpm.tfull,0),0)),<br> _xlfn.HSTACK(_xlpm.nc,_xlpm.nr,_xlpm.ng,_xlpm.id,_xlpm.url,_xlpm.keyf,_xlpm.m)) [OOXML {"t": "array", "ref": "GB3:GH7199"}] |
| GC3 | Amazon |  |
| GD3 | ALL |  |
| GE3 | 8 |  |
| GF3 | https://www.amazon.it/stores/page/CFD4D966-B596-4662-9305-AE3889DCC47C?ingress=0&amp;visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde |  |
| GG3 | Italy&#124;Amazon&#124;ALL&#124;8 |  |
| GH3 | 0 |  |
| GI3 | #VALUE! | =_xlfn.TEXTJOIN("&#124;",TRUE,IFERROR(_xlfn.XLOOKUP(INDEX(_xlfn.ANCHORARRAY(FP3),,3),$A$2:$A$15,$B$2:$B$15),"?")) [OOXML {"t": "array", "ref": "GI3"}] |
| GM3 | Czech&#124;Datart&#124;ALL&#124;9 | =_xlfn.LET(_xlpm.a,_xlfn.ANCHORARRAY(GB3),_xlpm.k,INDEX(_xlpm.a,,6),_xlpm.m,INDEX(_xlpm.a,,7),_xlpm.bad,_xlfn._xlws.FILTER(_xlpm.k,_xlpm.m=0),_xlpm.u,_xlfn._xlws.SORT(_xlfn.UNIQUE(_xlpm.bad)),_xlfn.HSTACK(_xlpm.u,_xlfn.MAP(_xlpm.u,_xlfn.LAMBDA(_xlpm.x,SUM(--(_xlpm.bad=_xlpm.x)))))) [OOXML {"t": "array", "ref": "GM3:GN21"}] |
| GN3 | 1 |  |
| GP3 | 1 | =_xlfn.LET(<br> _xlpm.a,_xlfn.ANCHORARRAY(GB3), _xlpm.m,INDEX(_xlpm.a,,7),<br> _xlpm.g,_xlfn._xlws.FILTER(_xlpm.a,_xlpm.m&gt;0),<br> _xlpm.idx,INDEX(_xlpm.g,,7),<br> _xlpm.tk,_xlfn.ANCHORARRAY('Improvement Task'!$B$3),<br> _xlfn.HSTACK(<br>  _xlfn.SEQUENCE(ROWS(_xlpm.g)),<br>  INDEX(_xlpm.g,,1),<br>  INDEX(_xlpm.g,,2),<br>  INDEX(_xlpm.g,,4),<br>  INDEX(INDEX(_xlpm.tk,,6),_xlpm.idx),<br>  INDEX(INDEX(_xlpm.tk,,10),_xlpm.idx),<br>  INDEX(_xlpm.g,,5),<br>  INDEX(INDEX(_xlpm.tk,,14),_xlpm.idx)<br> )) [OOXML {"t": "array", "ref": "GP3:GW7122"}] |
| GQ3 | France |  |
| GR3 | Boulanger |  |
| GS3 | 8 |  |
| GT3 | Alt Text Implementation |  |
| GU3 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV3 | https://www.boulanger.com/marque/lg |  |
| GW3 | N |  |
| HB3 | #VALUE! | =_xlfn.LET(_xlpm.tk,_xlfn.ANCHORARRAY('Improvement Task'!$B$3),_xlpm.tkey,INDEX(_xlpm.tk,,1)&amp;"~"&amp;INDEX(_xlpm.tk,,2)&amp;"~"&amp;INDEX(_xlpm.tk,,4),_xlpm.a,_xlfn.ANCHORARRAY(GB3),_xlpm.cat,INDEX(_xlpm.a,,3),_xlpm.blank,(_xlpm.cat=0)+(_xlpm.cat=""),_xlpm.u,_xlfn.UNIQUE(_xlfn._xlws.FILTER(INDEX(_xlpm.a,,1)&amp;"~"&amp;INDEX(_xlpm.a,,2)&amp;"~"&amp;INDEX(_xlpm.a,,4),_xlpm.blank&gt;0)),_xlfn.TEXTJOIN(" ; ",TRUE,_xlpm.u&amp;"-&gt;"&amp;IFERROR(MATCH(_xlpm.u,_xlpm.tkey,0),0))) [OOXML {"t": "array", "ref": "HB3"}] |

## Row 4

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A4 | Boulanger |  |
| B4 | Boulanger |  |
| D4 | Netherlands |  |
| E4 | Netherlands |  |
| G4 | W/M |  |
| H4 | W/M |  |
| J4 | 8 |  |
| K4 | France |  |
| L4 | Boulanger |  |
| M4 | 0 |  |
| N4 | https://www.boulanger.com/marque/lg |  |
| P4 | 9 |  |
| Q4 | Italy |  |
| R4 | Amazon |  |
| S4 | WM |  |
| T4 | https://www.amazon.it/stores/page/19248ADC-0AFB-4232-AB14-35EE45ABB5A5?ingress=0&amp;visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde |  |
| AB4 | 11 |  |
| AC4 | Italy |  |
| AD4 | Amazon |  |
| AE4 | WM |  |
| AF4 | https://www.amazon.it/s?k=Asciugatrici |  |
| AH4 | 12 |  |
| AI4 | Czech |  |
| AJ4 | Alza |  |
| AK4 | REF |  |
| AL4 | https://www.alza.cz/lg-gbv22ncbep-sleva-d13204773.htm |  |
| AN4 | 13 |  |
| AO4 | Sweden |  |
| AP4 | Elgiganten |  |
| AQ4 | WM |  |
| AR4 | https://www.elgiganten.se/product/outlet/lg-kombinerad-tvattmaskintorktumlare-cv94e7s2qa-116kg/742589 |  |
| AT4 | 14 |  |
| AU4 | France |  |
| AV4 | Darty |  |
| AW4 | WM |  |
| AX4 | https://www.darty.com/nav/achat/gros_electromenager/lave-linge/lave_linge_sechant/lg_f164hp2bst.html |  |
| AZ4 | 24 |  |
| BA4 | Czech |  |
| BB4 | Alza |  |
| BC4 | WM |  |
| BD4 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| BF4 | 25 |  |
| BG4 | Czech |  |
| BH4 | Alza |  |
| BI4 | WM |  |
| BJ4 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| BL4 | 33 |  |
| BM4 | Czech |  |
| BN4 | Alza |  |
| BO4 | WM |  |
| BP4 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| BR4 | 35 |  |
| BS4 | Czech |  |
| BT4 | Alza |  |
| BU4 | WM |  |
| BV4 | https://www.alza.cz/lg-washtower-wt1210wwf-d12518412.htm |  |
| BX4 | 45 |  |
| BY4 | Czech |  |
| BZ4 | Alza |  |
| CA4 | WM |  |
| CB4 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| CD4 | 43 |  |
| CE4 | France |  |
| CF4 | Darty |  |
| CG4 | REF |  |
| CH4 | https://www.darty.com/nav/achat/gros_electromenager/refrigerateur-congelateur-refrigerateur-cong/refrigerateur-congelateur_bas/lg_gbbw322cev.html |  |
| CJ4 | 34 |  |
| CK4 | Czech |  |
| CL4 | Alza |  |
| CM4 | REF |  |
| CN4 | https://www.alza.cz/lg-gbv22ncbep-sleva-d13204773.htm |  |
| CP4 | 39 |  |
| CQ4 | Czech |  |
| CR4 | Alza |  |
| CS4 | REF |  |
| CT4 | https://www.alza.cz/lg-gbbs727aev-d13217257.htm |  |
| CV4 | 40 |  |
| CW4 | Czech |  |
| CX4 | Alza |  |
| CY4 | REF |  |
| CZ4 | https://www.alza.cz/lg-gbv22ncbep-sleva-d13204773.htm |  |
| DB4 | 46 |  |
| DC4 | Czech |  |
| DD4 | Alza |  |
| DE4 | REF |  |
| DF4 | https://www.alza.cz/lg-gbv22ncbep-sleva-d13204773.htm |  |
| DH4 | 29 |  |
| DI4 | Czech |  |
| DJ4 | Alza |  |
| DK4 | REF |  |
| DL4 | https://www.alza.cz/lg-gbv22ncbep-sleva-d13204773.htm |  |
| DN4 | 44 |  |
| DO4 | Czech |  |
| DP4 | Alza |  |
| DQ4 | REF |  |
| DR4 | https://www.alza.cz/lg-gbv22ncbep-sleva-d13204773.htm |  |
| DT4 | 37 |  |
| DU4 | Italy |  |
| DV4 | Amazon |  |
| DW4 | REF |  |
| DX4 | https://www.amazon.it/dp/B0G2M8JT5B?smid=A11IL2PNWYJU7H |  |
| DZ4 | 38 |  |
| EA4 | Czech |  |
| EB4 | Alza |  |
| EC4 | WM |  |
| ED4 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| EF4 | 18 |  |
| EG4 | Czech |  |
| EH4 | Datart |  |
| EI4 | REF |  |
| EJ4 | https://www.datart.cz/lednice-lg.html |  |
| EL4 | 19 |  |
| EM4 | Italy |  |
| EN4 | AMAZON |  |
| EO4 | WM |  |
| EP4 | https://www.amazon.it/stores/page/19248ADC-0AFB-4232-AB14-35EE45ABB5A5?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| ER4 | 20 |  |
| ES4 | Czech |  |
| ET4 | Datart |  |
| EU4 | REF |  |
| EV4 | https://www.datart.cz/lednice-lg.html |  |
| EX4 | 21 |  |
| EY4 | Italy |  |
| EZ4 | MEDIAWORLD |  |
| FA4 | REF |  |
| FB4 | https://www.mediaworld.it/it/brand/lg/frigoriferi |  |
| FJ4 | 23 |  |
| FK4 | Czech |  |
| FL4 | Alza |  |
| FM4 | WM |  |
| FN4 | https://www.alza.cz/susicky/lg/18852767-v1357.htm |  |
| FP4 | 8 |  |
| FQ4 | France |  |
| FR4 | Boulanger |  |
| FS4 | 0 |  |
| FT4 | https://www.boulanger.com/marque/lg |  |
| FV4 | 34 |  |
| FW4 | Italy |  |
| FX4 | Mediaworld |  |
| FY4 | REF |  |
| GB4 | France |  |
| GC4 | Boulanger |  |
| GD4 | ALL |  |
| GE4 | 8 |  |
| GF4 | https://www.boulanger.com/marque/lg |  |
| GG4 | France&#124;Boulanger&#124;ALL&#124;8 |  |
| GH4 | 291 |  |
| GM4 | France&#124;Boulanger&#124;W/M&#124;11 |  |
| GN4 | 1 |  |
| GP4 | 2 |  |
| GQ4 | France |  |
| GR4 | Boulanger |  |
| GS4 | 8 |  |
| GT4 | Alt Text Implementation |  |
| GU4 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV4 | https://www.boulanger.com/c/refrigerateur/brand~lg |  |
| GW4 | N |  |

## Row 5

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A5 | Coolblue |  |
| B5 | Coolblue |  |
| D5 | Netherland |  |
| E5 | Netherlands |  |
| G5 | DW |  |
| H5 | DW |  |
| J5 | 8 |  |
| K5 | France |  |
| L5 | Boulanger |  |
| M5 | REF |  |
| N5 | https://www.boulanger.com/c/refrigerateur/brand~lg |  |
| P5 | 9 |  |
| Q5 | Italy |  |
| R5 | Amazon |  |
| S5 | REF |  |
| T5 | https://www.amazon.it/stores/page/5DE174FF-7426-4856-9BA8-3EF64DA9BCC5?ingress=0&amp;visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde |  |
| AB5 | 11 |  |
| AC5 | Italy |  |
| AD5 | Amazon |  |
| AE5 | WM |  |
| AF5 | https://www.amazon.it/s?k=carica+frontale |  |
| AH5 | 12 |  |
| AI5 | Czech |  |
| AJ5 | Alza |  |
| AK5 | WM |  |
| AL5 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| AN5 | 13 |  |
| AO5 | Sweden |  |
| AP5 | Elgiganten |  |
| AQ5 | WM |  |
| AR5 | https://www.elgiganten.se/product/outlet/lg-kombinerad-tvattmaskintorktumlare-f2dv707s2w1-85kg/745958 |  |
| AT5 | 14 |  |
| AU5 | Spain |  |
| AV5 | MediaMarkt |  |
| AW5 | WM |  |
| AX5 | https://www.mediamarkt.es/es/product/_lavadora-carga-frontal-lg-electronics-f4wr6010agwabwqpes-10-kg-12-programas-inox-139502058.html |  |
| AZ5 | 24 |  |
| BA5 | Czech |  |
| BB5 | Alza |  |
| BC5 | REF |  |
| BD5 | https://www.alza.cz/lg-gbbs727aev-d13217257.htm |  |
| BF5 | 25 |  |
| BG5 | Czech |  |
| BH5 | Alza |  |
| BI5 | WM |  |
| BJ5 | https://www.alza.cz/lg-fsr5a94wl-sleva-d12569671.htm |  |
| BL5 | 33 |  |
| BM5 | Czech |  |
| BN5 | Alza |  |
| BO5 | WM |  |
| BP5 | https://www.alza.cz/lg-fsr7a04pg-bazar-d12747490.htm |  |
| BR5 | 35 |  |
| BS5 | Czech |  |
| BT5 | Alza |  |
| BU5 | REF |  |
| BV5 | https://www.alza.cz/lg-gmg960evee-sleva-d12227924.htm |  |
| BX5 | 45 |  |
| BY5 | Czech |  |
| BZ5 | Alza |  |
| CA5 | REF |  |
| CB5 | https://www.alza.cz/lg-gbbs727aev-d13217257.htm |  |
| CD5 | 43 |  |
| CE5 | France |  |
| CF5 | Darty |  |
| CG5 | WM |  |
| CH5 | https://www.darty.com/nav/achat/gros_electromenager/lavage_sechage/lave-linge_hublot/lg_f34x71whst.html |  |
| CJ5 | 34 |  |
| CK5 | Czech |  |
| CL5 | Alza |  |
| CM5 | WM |  |
| CN5 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| CP5 | 39 |  |
| CQ5 | Czech |  |
| CR5 | Alza |  |
| CS5 | WM |  |
| CT5 | https://www.alza.cz/lg-wt1210bbf-d7850423.htm |  |
| CV5 | 40 |  |
| CW5 | Czech |  |
| CX5 | Alza |  |
| CY5 | WM |  |
| CZ5 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| DB5 | 46 |  |
| DC5 | Czech |  |
| DD5 | Alza |  |
| DE5 | WM |  |
| DF5 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| DH5 | 29 |  |
| DI5 | Czech |  |
| DJ5 | Alza |  |
| DK5 | WM |  |
| DL5 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| DN5 | 44 |  |
| DO5 | Czech |  |
| DP5 | Alza |  |
| DQ5 | WM |  |
| DR5 | https://www.alza.cz/lg-flr5a82ww-sleva-d13437765.htm |  |
| DT5 | 37 |  |
| DU5 | Poland |  |
| DV5 | MediaExpert |  |
| DW5 | WM |  |
| DX5 | https://www.mediaexpert.pl/agd/pralki-i-suszarki/pralko-suszarki/pralko-suszarka-washtower-lg-wt1210egf |  |
| DZ5 | 38 |  |
| EA5 | Czech |  |
| EB5 | Alza |  |
| EC5 | WM |  |
| ED5 | https://www.alza.cz/lg-f4a10s8nwk-levne-d13515802.htm |  |
| EF5 | 18 |  |
| EG5 | France |  |
| EH5 | BOULANGER |  |
| EI5 | REF |  |
| EJ5 | https://www.boulanger.com/c/refrigerateur/brand~lg |  |
| EL5 | 19 |  |
| EM5 | Italy |  |
| EN5 | AMAZON |  |
| EO5 | REF |  |
| EP5 | https://www.amazon.it/stores/page/5DE174FF-7426-4856-9BA8-3EF64DA9BCC5?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| ER5 | 20 |  |
| ES5 | Italy |  |
| ET5 | AMAZON |  |
| EU5 | WM |  |
| EV5 | https://www.amazon.it/stores/page/19248ADC-0AFB-4232-AB14-35EE45ABB5A5?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| EX5 | 21 |  |
| EY5 | Netherlands |  |
| EZ5 | COOLBLUE |  |
| FA5 | WM |  |
| FB5 | https://www.coolblue.nl/was-droogcombinaties/lg |  |
| FJ5 | 23 |  |
| FK5 | Czech |  |
| FL5 | Alza |  |
| FM5 | REF |  |
| FN5 | https://www.alza.cz/lednicky/lg/18852759-v1357.htm |  |
| FP5 | 8 |  |
| FQ5 | France |  |
| FR5 | Boulanger |  |
| FS5 | REF |  |
| FT5 | https://www.boulanger.com/c/refrigerateur/brand~lg |  |
| FV5 | 39 |  |
| FW5 | Italy |  |
| FX5 | Mediaworld |  |
| FY5 | REF |  |
| GB5 | France |  |
| GC5 | Boulanger |  |
| GD5 | REF |  |
| GE5 | 8 |  |
| GF5 | https://www.boulanger.com/c/refrigerateur/brand~lg |  |
| GG5 | France&#124;Boulanger&#124;REF&#124;8 |  |
| GH5 | 291 |  |
| GM5 | France&#124;Darty&#124;ALL&#124;8 |  |
| GN5 | 1 |  |
| GP5 | 3 |  |
| GQ5 | France |  |
| GR5 | Boulanger |  |
| GS5 | 8 |  |
| GT5 | Alt Text Implementation |  |
| GU5 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV5 | https://www.boulanger.com/c/lave-linge/brand~lg |  |
| GW5 | N |  |
| HB5 | 8,9,11,12,13,14,18,19,20,21,23,24,25,29,33,34,35,37,38,39,40,43,44,45,46 | =_xlfn.LET(_xlpm.tk,_xlfn.ANCHORARRAY('Improvement Task'!$B$3),_xlpm.ids,INDEX(_xlpm.tk,,4),_xlfn.TEXTJOIN(",",TRUE,_xlfn._xlws.SORT(_xlfn.UNIQUE(_xlpm.ids)))) |

## Row 6

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A6 | Darty |  |
| B6 | Darty |  |
| D6 | Sweden |  |
| E6 | Sweden |  |
| J6 | 8 |  |
| K6 | France |  |
| L6 | Boulanger |  |
| M6 | WM |  |
| N6 | https://www.boulanger.com/c/lave-linge/brand~lg |  |
| P6 | 9 |  |
| Q6 | Italy |  |
| R6 | Amazon |  |
| S6 | WM |  |
| T6 | https://www.amazon.it/stores/page/999E54C1-41F6-4C23-BD58-C9CFDC61A728?ingress=0&amp;visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde |  |
| AB6 | 11 |  |
| AC6 | Netherlands |  |
| AD6 | Coolblue |  |
| AE6 | WM |  |
| AF6 | https://www.coolblue.nl/zoeken?query=Warmtepompdrogers |  |
| AH6 | 12 |  |
| AI6 | Czech |  |
| AJ6 | Alza |  |
| AK6 | WM |  |
| AL6 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| AN6 | 13 |  |
| AO6 | Sweden |  |
| AP6 | Elgiganten |  |
| AQ6 | WM |  |
| AR6 | https://www.elgiganten.se/product/outlet/lg-serie-signature-tvatttork-lswd100e-127kg/376908 |  |
| AT6 | 14 |  |
| AU6 | Spain |  |
| AV6 | MediaMarkt |  |
| AW6 | REF |  |
| AX6 | https://www.mediamarkt.es/es/product/_frigorifico-combi-lg-gbbsj10dsw-no-frost-186-cm-375-l-doorcoolingtm-multi-air-flowtm-blanco-1604742.html |  |
| AZ6 | 24 |  |
| BA6 | Czech |  |
| BB6 | Alza |  |
| BC6 | WM |  |
| BD6 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| BF6 | 25 |  |
| BG6 | Czech |  |
| BH6 | Alza |  |
| BI6 | WM |  |
| BJ6 | https://www.alza.cz/lg-washtower-wt1716bbf-levne-d13173026.htm |  |
| BL6 | 33 |  |
| BM6 | Czech |  |
| BN6 | Alza |  |
| BO6 | REF |  |
| BP6 | https://www.alza.cz/lg-gbbsj1ccpy-d13121338.htm |  |
| BR6 | 35 |  |
| BS6 | Czech |  |
| BT6 | Alza |  |
| BU6 | WM |  |
| BV6 | https://www.alza.cz/lg-washtower-wt1210egf-d13004313.htm |  |
| BX6 | 45 |  |
| BY6 | Czech |  |
| BZ6 | Alza |  |
| CA6 | WM |  |
| CB6 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| CD6 | 43 |  |
| CE6 | France |  |
| CF6 | Darty |  |
| CG6 | WM |  |
| CH6 | https://www.darty.com/nav/achat/gros_electromenager/lavage_sechage/lave-linge_hublot/lg_f20f12wst.html |  |
| CJ6 | 34 |  |
| CK6 | Czech |  |
| CL6 | Alza |  |
| CM6 | REF |  |
| CN6 | https://www.alza.cz/lg-gbbs727aev-d13217257.htm |  |
| CP6 | 39 |  |
| CQ6 | Czech |  |
| CR6 | Alza |  |
| CS6 | WM |  |
| CT6 | https://www.alza.cz/lg-fa2s8v3gn3w-d7951214.htm |  |
| CV6 | 40 |  |
| CW6 | Czech |  |
| CX6 | Alza |  |
| CY6 | REF |  |
| CZ6 | https://www.alza.cz/lg-gbbs727aev-d13217257.htm |  |
| DB6 | 46 |  |
| DC6 | Czech |  |
| DD6 | Alza |  |
| DE6 | REF |  |
| DF6 | https://www.alza.cz/lg-gbbs727aev-d13217257.htm |  |
| DH6 | 29 |  |
| DI6 | Czech |  |
| DJ6 | Alza |  |
| DK6 | REF |  |
| DL6 | https://www.alza.cz/lg-gbbs727aev-d13217257.htm |  |
| DN6 | 44 |  |
| DO6 | Czech |  |
| DP6 | Alza |  |
| DQ6 | REF |  |
| DR6 | https://www.alza.cz/lg-gbbs727aev-d13217257.htm |  |
| DT6 | 37 |  |
| DU6 | Italy |  |
| DV6 | Mediaworld |  |
| DW6 | WM |  |
| DX6 | https://www.mediaworld.it/it/product/_lg-washtower-wt1210wwf-407407.html |  |
| DZ6 | 38 |  |
| EA6 | Czech |  |
| EB6 | Alza |  |
| EC6 | REF |  |
| ED6 | https://www.alza.cz/lg-gbbw322cpy-bazar-d13495321.htm |  |
| EF6 | 18 |  |
| EG6 | France |  |
| EH6 | BOULANGER |  |
| EI6 | WM |  |
| EJ6 | https://www.boulanger.com/c/lave-linge/brand~lg |  |
| EL6 | 19 |  |
| EM6 | Italy |  |
| EN6 | AMAZON |  |
| EO6 | WM |  |
| EP6 | https://www.amazon.it/stores/page/999E54C1-41F6-4C23-BD58-C9CFDC61A728?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| ER6 | 20 |  |
| ES6 | Italy |  |
| ET6 | AMAZON |  |
| EU6 | REF |  |
| EV6 | https://www.amazon.it/stores/page/5DE174FF-7426-4856-9BA8-3EF64DA9BCC5?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| EX6 | 21 |  |
| EY6 | Netherlands |  |
| EZ6 | COOLBLUE |  |
| FA6 | WM |  |
| FB6 | https://www.coolblue.nl/wasmachines/lg |  |
| FJ6 | 23 |  |
| FK6 | Czech |  |
| FL6 | Datart |  |
| FM6 | WM |  |
| FN6 | https://www.datart.cz/susicky-lg.html |  |
| FP6 | 8 |  |
| FQ6 | France |  |
| FR6 | Boulanger |  |
| FS6 | WM |  |
| FT6 | https://www.boulanger.com/c/lave-linge/brand~lg |  |
| FV6 | 40 |  |
| FW6 | Italy |  |
| FX6 | Mediaworld |  |
| FY6 | REF |  |
| GB6 | France |  |
| GC6 | Boulanger |  |
| GD6 | W/M |  |
| GE6 | 8 |  |
| GF6 | https://www.boulanger.com/c/lave-linge/brand~lg |  |
| GG6 | France&#124;Boulanger&#124;W/M&#124;8 |  |
| GH6 | 307 |  |
| GM6 | France&#124;Darty&#124;W/M&#124;14 |  |
| GN6 | 1 |  |
| GP6 | 4 |  |
| GQ6 | Netherlands |  |
| GR6 | Coolblue |  |
| GS6 | 8 |  |
| GT6 | Alt Text Implementation |  |
| GU6 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV6 | https://www.coolblue.nl/lg |  |
| GW6 | N |  |
| HB6 | Spain~Media Markt~REF ; Spain~Media Markt~W/M ; Spain~Media Markt~DW ; Italy~Media World~REF ; Italy~Media World~W/M ; Italy~Amazon~REF ; Italy~Amazon~W/M ; Netherlands~Coolblue~REF ; Sweden~ELGIGANTEN~REF ; Sweden~ELGIGANTEN~W/M ; France~Boulanger~REF ; France~Boulanger~W/M | =_xlfn.LET(_xlpm.tk,_xlfn.ANCHORARRAY('Improvement Task'!$B$3),_xlpm.f,_xlfn._xlws.FILTER(INDEX(_xlpm.tk,,1)&amp;"~"&amp;INDEX(_xlpm.tk,,2)&amp;"~"&amp;INDEX(_xlpm.tk,,3),(INDEX(_xlpm.tk,,4)=8)+(INDEX(_xlpm.tk,,4)=9)+(INDEX(_xlpm.tk,,4)=10)),_xlfn.TEXTJOIN(" ; ",TRUE,_xlpm.f)) [OOXML {"t": "array", "ref": "HB6"}] |

## Row 7

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A7 | Datart |  |
| B7 | Datart |  |
| D7 | France |  |
| E7 | France |  |
| J7 | 8 |  |
| K7 | Netherlands |  |
| L7 | Coolblue |  |
| M7 | 0 |  |
| N7 | https://www.coolblue.nl/lg |  |
| P7 | 9 |  |
| Q7 | Italy |  |
| R7 | Amazon |  |
| S7 | WM |  |
| T7 | https://www.amazon.it/stores/page/045E563A-5374-463E-BFDB-E7E47BDBC9F6?ingress=0&amp;visitId=123343d5-4ec3-4e5b-8acd-7095f152ddde |  |
| AB7 | 11 |  |
| AC7 | Poland |  |
| AD7 | MediaExpert |  |
| AE7 | REF |  |
| AF7 | https://www.mediaexpert.pl/search?query%5Bquerystring%5D=ch%C5%82odziarko-zamra%C5%BCarka |  |
| AH7 | 12 |  |
| AI7 | Czech |  |
| AJ7 | Alza |  |
| AK7 | WM |  |
| AL7 | https://www.alza.cz/lg-f4a10s8nwk-levne-d13515802.htm |  |
| AN7 | 13 |  |
| AO7 | Sweden |  |
| AP7 | Elgiganten |  |
| AQ7 | WM |  |
| AR7 | https://www.elgiganten.se/product/outlet/lg-tvattmaskin-f4a1009nwh-9kg/1016263 |  |
| AT7 | 14 |  |
| AU7 | Spain |  |
| AV7 | MediaMarkt |  |
| AW7 | WM |  |
| AX7 | https://www.mediamarkt.es/es/product/_lavadora-carga-frontal-lg-f4wr5010a6w-10-kg-1400-rpm-11-programas-ai-direct-drivetm-steamtm-blanco-1576839.html |  |
| AZ7 | 24 |  |
| BA7 | Czech |  |
| BB7 | Alza |  |
| BC7 | WM |  |
| BD7 | https://www.alza.cz/lg-fsr7a04pg-bazar-d12747490.htm |  |
| BF7 | 25 |  |
| BG7 | Czech |  |
| BH7 | Alza |  |
| BI7 | REF |  |
| BJ7 | https://www.alza.cz/lg-gmg860epbe-d12379812.htm |  |
| BL7 | 33 |  |
| BM7 | Czech |  |
| BN7 | Alza |  |
| BO7 | REF |  |
| BP7 | https://www.alza.cz/lg-gbbs322aev-d13191828.htm |  |
| BR7 | 35 |  |
| BS7 | Czech |  |
| BT7 | Alza |  |
| BU7 | WM |  |
| BV7 | https://www.alza.cz/lg-washtower-wt1210egf-sleva-d13528071.htm |  |
| BX7 | 45 |  |
| BY7 | Czech |  |
| BZ7 | Alza |  |
| CA7 | WM |  |
| CB7 | https://www.alza.cz/lg-wt1210bbf-d7850423.htm |  |
| CD7 | 43 |  |
| CE7 | France |  |
| CF7 | Darty |  |
| CG7 | WM |  |
| CH7 | https://www.darty.com/nav/achat/gros_electromenager/lavage_sechage/lave-linge_hublot/lg_f14x71whst.html |  |
| CJ7 | 34 |  |
| CK7 | Czech |  |
| CL7 | Alza |  |
| CM7 | WM |  |
| CN7 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| CP7 | 39 |  |
| CQ7 | Czech |  |
| CR7 | Alza |  |
| CS7 | REF |  |
| CT7 | https://www.alza.cz/lg-gbbsj1ccpy-d13121338.htm |  |
| CV7 | 40 |  |
| CW7 | Czech |  |
| CX7 | Alza |  |
| CY7 | WM |  |
| CZ7 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| DB7 | 46 |  |
| DC7 | Czech |  |
| DD7 | Alza |  |
| DE7 | WM |  |
| DF7 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| DH7 | 29 |  |
| DI7 | Czech |  |
| DJ7 | Alza |  |
| DK7 | WM |  |
| DL7 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| DN7 | 44 |  |
| DO7 | Czech |  |
| DP7 | Alza |  |
| DQ7 | WM |  |
| DR7 | https://www.alza.cz/lg-f2x50s8tbb-sleva-d13352244.htm |  |
| DT7 | 37 |  |
| DU7 | Italy |  |
| DV7 | Mediaworld |  |
| DW7 | REF |  |
| DX7 | https://www.mediaworld.it/it/product/_lg-gmv860epde-instaview-slim-frigorifero-americano-152006384.html |  |
| DZ7 | 38 |  |
| EA7 | Czech |  |
| EB7 | Alza |  |
| EC7 | WM |  |
| ED7 | https://www.alza.cz/lg-washtower-wt1716bbf-levne-d13173026.htm |  |
| EF7 | 18 |  |
| EG7 | Italy |  |
| EH7 | MEDIAWORLD |  |
| EI7 | WM |  |
| EJ7 | https://www.mediaworld.it/it/brand/lg/asciugatrici |  |
| EL7 | 19 |  |
| EM7 | Italy |  |
| EN7 | AMAZON |  |
| EO7 | WM |  |
| EP7 | https://www.amazon.it/stores/page/045E563A-5374-463E-BFDB-E7E47BDBC9F6?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| ER7 | 20 |  |
| ES7 | Italy |  |
| ET7 | AMAZON |  |
| EU7 | WM |  |
| EV7 | https://www.amazon.it/stores/page/999E54C1-41F6-4C23-BD58-C9CFDC61A728?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| EX7 | 21 |  |
| EY7 | Netherlands |  |
| EZ7 | Media Markt |  |
| FA7 | REF |  |
| FB7 | https://www.mediamarkt.nl/nl/category/lg-koelkasten-964.html |  |
| FJ7 | 23 |  |
| FK7 | Czech |  |
| FL7 | Datart |  |
| FM7 | REF |  |
| FN7 | https://www.datart.cz/lednice-lg.html |  |
| FP7 | 8 |  |
| FQ7 | Netherlands |  |
| FR7 | Coolblue |  |
| FS7 | 0 |  |
| FT7 | https://www.coolblue.nl/lg |  |
| FV7 | 46 |  |
| FW7 | Italy |  |
| FX7 | Mediaworld |  |
| FY7 | REF |  |
| GB7 | Netherlands |  |
| GC7 | Coolblue |  |
| GD7 | ALL |  |
| GE7 | 8 |  |
| GF7 | https://www.coolblue.nl/lg |  |
| GG7 | Netherlands&#124;Coolblue&#124;ALL&#124;8 |  |
| GH7 | 177 |  |
| GM7 | Italy&#124;Amazon&#124;ALL&#124;8 |  |
| GN7 | 1 |  |
| GP7 | 5 |  |
| GQ7 | Netherlands |  |
| GR7 | Coolblue |  |
| GS7 | 8 |  |
| GT7 | Alt Text Implementation |  |
| GU7 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV7 | https://www.coolblue.nl/koelkasten/lg |  |
| GW7 | N |  |

## Row 8

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A8 | Elcorteingles_electronica |  |
| B8 | ECI |  |
| D8 | Poland |  |
| E8 | Poland |  |
| J8 | 8 |  |
| K8 | Netherlands |  |
| L8 | Coolblue |  |
| M8 | REF |  |
| N8 | https://www.coolblue.nl/koelkasten/lg |  |
| P8 | 9 |  |
| Q8 | Czech |  |
| R8 | Datart |  |
| S8 | 0 |  |
| T8 | https://www.datart.cz/shop/lg |  |
| AB8 | 11 |  |
| AC8 | Poland |  |
| AD8 | MediaExpert |  |
| AE8 | REF |  |
| AF8 | https://www.mediaexpert.pl/search?query%5Bquerystring%5D=lod%C3%B3wka+70+cm |  |
| AH8 | 12 |  |
| AI8 | Czech |  |
| AJ8 | Alza |  |
| AK8 | WM |  |
| AL8 | https://www.alza.cz/lg-washtower-wt1716bbf-levne-d13173026.htm |  |
| AN8 | 13 |  |
| AO8 | Sweden |  |
| AP8 | Elgiganten |  |
| AQ8 | WM |  |
| AR8 | https://www.elgiganten.se/product/outlet/lg-tvattmaskin-f4x5511tlb-11kg/1126750 |  |
| AT8 | 14 |  |
| AU8 | Spain |  |
| AV8 | MediaMarkt |  |
| AW8 | REF |  |
| AX8 | https://www.mediamarkt.es/es/product/_frigorifico-americano-lg-gslc40swpe-no-frost-179-cm-638-l-blanco-1569330.html |  |
| AZ8 | 24 |  |
| BA8 | Czech |  |
| BB8 | Alza |  |
| BC8 | WM |  |
| BD8 | https://www.alza.cz/lg-fa2s8v3gn3w-d7951214.htm |  |
| BF8 | 25 |  |
| BG8 | Czech |  |
| BH8 | Alza |  |
| BI8 | WM |  |
| BJ8 | https://www.alza.cz/lg-fcr7a06pg-d7917929.htm |  |
| BL8 | 33 |  |
| BM8 | Czech |  |
| BN8 | Alza |  |
| BO8 | WM |  |
| BP8 | https://www.alza.cz/lg-fasr3a04ww-d12518413.htm |  |
| BR8 | 35 |  |
| BS8 | Czech |  |
| BT8 | Alza |  |
| BU8 | WM |  |
| BV8 | https://www.alza.cz/lg-washtower-wt1210bbf-sleva-d12495936.htm |  |
| BX8 | 45 |  |
| BY8 | Czech |  |
| BZ8 | Alza |  |
| CA8 | WM |  |
| CB8 | https://www.alza.cz/lg-fsr7a04pg-bazar-d12747490.htm |  |
| CD8 | 43 |  |
| CE8 | France |  |
| CF8 | Darty |  |
| CG8 | WM |  |
| CH8 | https://www.darty.com/nav/achat/gros_electromenager/lavage_sechage/lave-linge_sechant/lg_f214wt8pb.html |  |
| CJ8 | 34 |  |
| CK8 | Czech |  |
| CL8 | Alza |  |
| CM8 | WM |  |
| CN8 | https://www.alza.cz/lg-f4a10s8nwk-levne-d13515802.htm |  |
| CP8 | 39 |  |
| CQ8 | Czech |  |
| CR8 | Alza |  |
| CS8 | REF |  |
| CT8 | https://www.alza.cz/lg-gmg860epbe-d12379812.htm |  |
| CV8 | 40 |  |
| CW8 | Czech |  |
| CX8 | Alza |  |
| CY8 | WM |  |
| CZ8 | https://www.alza.cz/lg-f4a10s8nwk-levne-d13515802.htm |  |
| DB8 | 46 |  |
| DC8 | Czech |  |
| DD8 | Alza |  |
| DE8 | WM |  |
| DF8 | https://www.alza.cz/lg-f4a10s8nwk-levne-d13515802.htm |  |
| DH8 | 29 |  |
| DI8 | Czech |  |
| DJ8 | Alza |  |
| DK8 | WM |  |
| DL8 | https://www.alza.cz/lg-f4a10s8nwk-levne-d13515802.htm |  |
| DN8 | 44 |  |
| DO8 | Czech |  |
| DP8 | Alza |  |
| DQ8 | WM |  |
| DR8 | https://www.alza.cz/lg-f4a10s8nwk-levne-d13515802.htm |  |
| DT8 | 37 |  |
| DU8 | Poland |  |
| DV8 | RtvEuroAgd |  |
| DW8 | REF |  |
| DX8 | https://www.euro.com.pl/lodowki/lg-gbbw322cev-pelny-no-frost-203cm-komora-swiezosci-zdalne-sterowanie.bhtml |  |
| DZ8 | 38 |  |
| EA8 | Czech |  |
| EB8 | Alza |  |
| EC8 | REF |  |
| ED8 | https://www.alza.cz/lg-gbbs726bev-d13191820.htm |  |
| EF8 | 18 |  |
| EG8 | Italy |  |
| EH8 | MEDIAWORLD |  |
| EI8 | REF |  |
| EJ8 | https://www.mediaworld.it/it/brand/lg/frigoriferi |  |
| ER8 | 20 |  |
| ES8 | Italy |  |
| ET8 | AMAZON |  |
| EU8 | WM |  |
| EV8 | https://www.amazon.it/stores/page/045E563A-5374-463E-BFDB-E7E47BDBC9F6?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| EX8 | 21 |  |
| EY8 | Netherlands |  |
| EZ8 | Media Markt |  |
| FA8 | WM |  |
| FB8 | https://www.mediamarkt.nl/nl/category/lg-wasmachines-968.html |  |
| FJ8 | 23 |  |
| FK8 | France |  |
| FL8 | BOULANGER |  |
| FM8 | REF |  |
| FN8 | https://www.boulanger.com/c/refrigerateur/brand~lg |  |
| FP8 | 8 |  |
| FQ8 | Netherlands |  |
| FR8 | Coolblue |  |
| FS8 | REF |  |
| FT8 | https://www.coolblue.nl/koelkasten/lg |  |
| FV8 | 29 |  |
| FW8 | Italy |  |
| FX8 | Mediaworld |  |
| FY8 | REF |  |
| GB8 | Netherlands |  |
| GC8 | Coolblue |  |
| GD8 | REF |  |
| GE8 | 8 |  |
| GF8 | https://www.coolblue.nl/koelkasten/lg |  |
| GG8 | Netherlands&#124;Coolblue&#124;REF&#124;8 |  |
| GH8 | 177 |  |
| GM8 | Italy&#124;Amazon&#124;W/M&#124;11 |  |
| GN8 | 2 |  |
| GP8 | 6 |  |
| GQ8 | Sweden |  |
| GR8 | ELGIGANTEN |  |
| GS8 | 8 |  |
| GT8 | Alt Text Implementation |  |
| GU8 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV8 | https://www.elgiganten.se/brand/lg |  |
| GW8 | N |  |
| HA8 | ID8 조합 |  |
| HB8 | Spain~Media Markt~REF ; Spain~Media Markt~W/M ; Spain~Media Markt~DW ; Italy~Media World~REF ; Italy~Media World~W/M ; Netherlands~Coolblue~REF ; Sweden~ELGIGANTEN~REF ; Sweden~ELGIGANTEN~W/M ; France~Boulanger~REF ; France~Boulanger~W/M | =_xlfn.LET(_xlpm.tk,_xlfn.ANCHORARRAY('Improvement Task'!$B$3),_xlpm.f,_xlfn._xlws.FILTER(INDEX(_xlpm.tk,,1)&amp;"~"&amp;INDEX(_xlpm.tk,,2)&amp;"~"&amp;INDEX(_xlpm.tk,,3),INDEX(_xlpm.tk,,4)=8),_xlfn.TEXTJOIN(" ; ",TRUE,_xlpm.f)) [OOXML {"t": "array", "ref": "HB8"}] |

## Row 9

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A9 | Elgiganten |  |
| B9 | ELGIGANTEN |  |
| D9 | Czech |  |
| E9 | Czech |  |
| J9 | 8 |  |
| K9 | France |  |
| L9 | Darty |  |
| M9 | 0 |  |
| N9 | https://www.darty.com/nav/q/marque-lg.html |  |
| AB9 | 11 |  |
| AC9 | Poland |  |
| AD9 | MediaExpert |  |
| AE9 | REF |  |
| AF9 | https://www.mediaexpert.pl/search?query%5Bquerystring%5D=lod%C3%B3wka+z+kostkark%C4%85 |  |
| AH9 | 12 |  |
| AI9 | Czech |  |
| AJ9 | Alza |  |
| AK9 | REF |  |
| AL9 | https://www.alza.cz/lg-gbbs322aev-d13191828.htm |  |
| AN9 | 13 |  |
| AO9 | Sweden |  |
| AP9 | Elgiganten |  |
| AQ9 | WM |  |
| AR9 | https://www.elgiganten.se/product/outlet/lg-tvattmaskin-f4x7511tws-11kg/855988 |  |
| AT9 | 14 |  |
| AU9 | Spain |  |
| AV9 | MediaMarkt |  |
| AW9 | DW |  |
| AX9 | https://www.mediamarkt.es/es/product/_lavavajillas-lg-df365fms-14-servicios-10-programas-60-cm-led-tactil-tercera-bandeja-truesteamtm-quadwashtm-acero-negro-grafito-antihuellas-1582774.html |  |
| AZ9 | 24 |  |
| BA9 | Czech |  |
| BB9 | Alza |  |
| BC9 | WM |  |
| BD9 | https://www.alza.cz/lg-fsr5a94wl-sleva-d12569671.htm |  |
| BF9 | 25 |  |
| BG9 | Czech |  |
| BH9 | Alza |  |
| BI9 | REF |  |
| BJ9 | https://www.alza.cz/lg-gsle91mbac-d12316100.htm |  |
| BL9 | 33 |  |
| BM9 | Czech |  |
| BN9 | Alza |  |
| BO9 | WM |  |
| BP9 | https://www.alza.cz/lg-fsr7a04pg-levne-d7995060.htm |  |
| BR9 | 35 |  |
| BS9 | Czech |  |
| BT9 | Alza |  |
| BU9 | REF |  |
| BV9 | https://www.alza.cz/americka-lednice-lg-gmg960evee-d9910674.htm |  |
| BX9 | 45 |  |
| BY9 | Czech |  |
| BZ9 | Alza |  |
| CA9 | WM |  |
| CB9 | https://www.alza.cz/lg-fa2s8v3gn3w-d7951214.htm |  |
| CD9 | 43 |  |
| CE9 | France |  |
| CF9 | Darty |  |
| CG9 | WM |  |
| CH9 | https://www.darty.com/nav/achat/gros_electromenager/lave-linge/lave_linge_sechant/lg_f214wt8wh.html |  |
| CJ9 | 34 |  |
| CK9 | Czech |  |
| CL9 | Alza |  |
| CM9 | REF |  |
| CN9 | https://www.alza.cz/lg-gbbw322cpy-bazar-d13495321.htm |  |
| CP9 | 39 |  |
| CQ9 | Czech |  |
| CR9 | Alza |  |
| CS9 | REF |  |
| CT9 | https://www.alza.cz/lg-gbbs726bev-d13191820.htm |  |
| CV9 | 40 |  |
| CW9 | Czech |  |
| CX9 | Alza |  |
| CY9 | REF |  |
| CZ9 | https://www.alza.cz/lg-gbbw322cpy-bazar-d13495321.htm |  |
| DB9 | 46 |  |
| DC9 | Czech |  |
| DD9 | Alza |  |
| DE9 | REF |  |
| DF9 | https://www.alza.cz/lg-gbbw322cpy-bazar-d13495321.htm |  |
| DH9 | 29 |  |
| DI9 | Czech |  |
| DJ9 | Alza |  |
| DK9 | REF |  |
| DL9 | https://www.alza.cz/lg-gbbw322cpy-bazar-d13495321.htm |  |
| DN9 | 44 |  |
| DO9 | Czech |  |
| DP9 | Alza |  |
| DQ9 | REF |  |
| DR9 | https://www.alza.cz/lg-gbbw322cpy-bazar-d13495321.htm |  |
| DT9 | 37 |  |
| DU9 | Italy |  |
| DV9 | Unieuro |  |
| DW9 | WM |  |
| DX9 | https://www.unieuro.it/online/Lavasciuga/D2R3S08NSWW-Lavasciuga-slim-8-5kg-AI-DD-Classe-E-1200-giri-AI-Wash-Vapore-pidGOLD2R3S08NSWW |  |
| DZ9 | 38 |  |
| EA9 | Czech |  |
| EB9 | Alza |  |
| EC9 | REF |  |
| ED9 | https://www.alza.cz/lg-gbbs322aev-d13191828.htm |  |
| EF9 | 18 |  |
| EG9 | Italy |  |
| EH9 | MEDIAWORLD |  |
| EI9 | WM |  |
| EJ9 | https://www.mediaworld.it/it/brand/lg/lavatrici |  |
| ER9 | 20 |  |
| ES9 | Italy |  |
| ET9 | MEDIAWORLD |  |
| EU9 | WM |  |
| EV9 | https://www.mediaworld.it/it/brand/lg/asciugatrici |  |
| EX9 | 21 |  |
| EY9 | Spain |  |
| EZ9 | Media Markt |  |
| FA9 | DW |  |
| FB9 | https://www.mediamarkt.es/es/brand/lg-electronics/lavavajillas |  |
| FJ9 | 23 |  |
| FK9 | France |  |
| FL9 | BOULANGER |  |
| FM9 | WM |  |
| FN9 | https://www.boulanger.com/c/lave-linge/brand~lg |  |
| FP9 | 8 |  |
| FQ9 | France |  |
| FR9 | Darty |  |
| FS9 | 0 |  |
| FT9 | https://www.darty.com/nav/q/marque-lg.html |  |
| GB9 | France |  |
| GC9 | Darty |  |
| GD9 | ALL |  |
| GE9 | 8 |  |
| GF9 | https://www.darty.com/nav/q/marque-lg.html |  |
| GG9 | France&#124;Darty&#124;ALL&#124;8 |  |
| GH9 | 0 |  |
| GM9 | Netherlands&#124;Media Markt&#124;REF&#124;8 |  |
| GN9 | 1 |  |
| GP9 | 7 |  |
| GQ9 | Sweden |  |
| GR9 | ELGIGANTEN |  |
| GS9 | 8 |  |
| GT9 | Alt Text Implementation |  |
| GU9 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV9 | https://www.elgiganten.se/brand/lg/kylskap-lg |  |
| GW9 | N |  |
| HA9 | ID9 조합 |  |
| HB9 | Italy~Amazon~REF ; Italy~Amazon~W/M | =_xlfn.LET(_xlpm.tk,_xlfn.ANCHORARRAY('Improvement Task'!$B$3),_xlpm.f,_xlfn._xlws.FILTER(INDEX(_xlpm.tk,,1)&amp;"~"&amp;INDEX(_xlpm.tk,,2)&amp;"~"&amp;INDEX(_xlpm.tk,,3),INDEX(_xlpm.tk,,4)=9),_xlfn.TEXTJOIN(" ; ",TRUE,_xlpm.f)) [OOXML {"t": "array", "ref": "HB9"}] |

## Row 10

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A10 | MediaExpert |  |
| B10 | Media Expert |  |
| J10 | 8 |  |
| K10 | Sweden |  |
| L10 | Elgiganten |  |
| M10 | 0 |  |
| N10 | https://www.elgiganten.se/brand/lg |  |
| AB10 | 11 |  |
| AC10 | Poland |  |
| AD10 | MediaExpert |  |
| AE10 | WM |  |
| AF10 | https://www.mediaexpert.pl/search?query%5Bquerystring%5D=suszarka |  |
| AH10 | 12 |  |
| AI10 | Czech |  |
| AJ10 | Alza |  |
| AK10 | WM |  |
| AL10 | https://www.alza.cz/lg-fcr7a06pg-d7917929.htm |  |
| AN10 | 13 |  |
| AO10 | Sweden |  |
| AP10 | Elgiganten |  |
| AQ10 | WM |  |
| AR10 | https://www.elgiganten.se/product/outlet/lg-tvattmaskin-f4x7513tbb-13kg/1013897 |  |
| AT10 | 14 |  |
| AU10 | Spain |  |
| AV10 | MediaMarkt |  |
| AW10 | WM |  |
| AX10 | https://www.mediamarkt.es/es/product/_lavadora-carga-frontal-lg-f4wr5509a1w-serie-550-9-kg-1400-rpm-15-programas-ai-direct-drivetm-autodosificador-de-detergente-blanco-1556461.html |  |
| AZ10 | 24 |  |
| BA10 | Czech |  |
| BB10 | Alza |  |
| BC10 | REF |  |
| BD10 | https://www.alza.cz/lg-gbbsj1ccpy-d13121338.htm |  |
| BF10 | 25 |  |
| BG10 | Czech |  |
| BH10 | Alza |  |
| BI10 | WM |  |
| BJ10 | https://www.alza.cz/lg-fsr5a34wg-d7951216.htm |  |
| BL10 | 33 |  |
| BM10 | Czech |  |
| BN10 | Alza |  |
| BO10 | WM |  |
| BP10 | https://www.alza.cz/lg-fcr7a06pg-d7917929.htm |  |
| BR10 | 35 |  |
| BS10 | Czech |  |
| BT10 | Alza |  |
| BU10 | REF |  |
| BV10 | https://www.alza.cz/lg-gbbsj10dsw-d13121336.htm |  |
| BX10 | 45 |  |
| BY10 | Czech |  |
| BZ10 | Alza |  |
| CA10 | WM |  |
| CB10 | https://www.alza.cz/lg-fsr5a94wl-sleva-d12569671.htm |  |
| CD10 | 43 |  |
| CE10 | France |  |
| CF10 | Darty |  |
| CG10 | WM |  |
| CH10 | https://www.darty.com/nav/achat/gros_electromenager/lave-linge/lave_linge_sechant/lg_f964x76wsta.html |  |
| CJ10 | 34 |  |
| CK10 | Czech |  |
| CL10 | Alza |  |
| CM10 | WM |  |
| CN10 | https://www.alza.cz/lg-wt1210bbf-d7850423.htm |  |
| CP10 | 39 |  |
| CQ10 | Czech |  |
| CR10 | Alza |  |
| CS10 | REF |  |
| CT10 | https://www.alza.cz/lg-gbbs322aev-d13191828.htm |  |
| CV10 | 40 |  |
| CW10 | Czech |  |
| CX10 | Alza |  |
| CY10 | WM |  |
| CZ10 | https://www.alza.cz/lg-fsr7a04pg-bazar-d12747490.htm |  |
| DB10 | 46 |  |
| DC10 | Czech |  |
| DD10 | Alza |  |
| DE10 | WM |  |
| DF10 | https://www.alza.cz/lg-fsr7a04pg-bazar-d12747490.htm |  |
| DH10 | 29 |  |
| DI10 | Czech |  |
| DJ10 | Alza |  |
| DK10 | WM |  |
| DL10 | https://www.alza.cz/lg-wt1210bbf-d7850423.htm |  |
| DN10 | 44 |  |
| DO10 | Czech |  |
| DP10 | Alza |  |
| DQ10 | WM |  |
| DR10 | https://www.alza.cz/lg-wt1210bbf-d7850423.htm |  |
| DZ10 | 38 |  |
| EA10 | Czech |  |
| EB10 | Alza |  |
| EC10 | REF |  |
| ED10 | https://www.alza.cz/lg-gslv71mctd-d7917928.htm |  |
| EF10 | 18 |  |
| EG10 | Netherlands |  |
| EH10 | COOLBLUE |  |
| EI10 | WM |  |
| EJ10 | https://www.coolblue.nl/was-droogcombinaties/lg |  |
| ER10 | 20 |  |
| ES10 | Italy |  |
| ET10 | MEDIAWORLD |  |
| EU10 | REF |  |
| EV10 | https://www.mediaworld.it/it/brand/lg/frigoriferi |  |
| EX10 | 21 |  |
| EY10 | Sweden |  |
| EZ10 | ELGIGANTEN |  |
| FA10 | REF |  |
| FB10 | https://www.elgiganten.se/brand/lg/kylskap-lg |  |
| FJ10 | 23 |  |
| FK10 | Italy |  |
| FL10 | AMAZON |  |
| FM10 | WM |  |
| FN10 | https://www.amazon.it/stores/page/19248ADC-0AFB-4232-AB14-35EE45ABB5A5?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| FP10 | 8 |  |
| FQ10 | Sweden |  |
| FR10 | Elgiganten |  |
| FS10 | 0 |  |
| FT10 | https://www.elgiganten.se/brand/lg |  |
| GB10 | Sweden |  |
| GC10 | ELGIGANTEN |  |
| GD10 | ALL |  |
| GE10 | 8 |  |
| GF10 | https://www.elgiganten.se/brand/lg |  |
| GG10 | Sweden&#124;ELGIGANTEN&#124;ALL&#124;8 |  |
| GH10 | 230 |  |
| GM10 | Netherlands&#124;Media Markt&#124;W/M&#124;8 |  |
| GN10 | 1 |  |
| GP10 | 8 |  |
| GQ10 | Sweden |  |
| GR10 | ELGIGANTEN |  |
| GS10 | 8 |  |
| GT10 | Alt Text Implementation |  |
| GU10 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV10 | https://www.elgiganten.se/brand/lg/lg-tvattmaskin-och-torktumlare |  |
| GW10 | N |  |
| HA10 | ID10 조합 |  |
| HB10 | #VALUE! | =_xlfn.LET(_xlpm.tk,_xlfn.ANCHORARRAY('Improvement Task'!$B$3),_xlpm.f,_xlfn._xlws.FILTER(INDEX(_xlpm.tk,,1)&amp;"~"&amp;INDEX(_xlpm.tk,,2)&amp;"~"&amp;INDEX(_xlpm.tk,,3),INDEX(_xlpm.tk,,4)=10),_xlfn.TEXTJOIN(" ; ",TRUE,_xlpm.f)) [OOXML {"t": "array", "ref": "HB10"}] |

## Row 11

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A11 | MediaMarkt |  |
| B11 | Media Markt |  |
| J11 | 8 |  |
| K11 | Sweden |  |
| L11 | Elgiganten |  |
| M11 | REF |  |
| N11 | https://www.elgiganten.se/brand/lg/kylskap-lg |  |
| AB11 | 11 |  |
| AC11 | Poland |  |
| AD11 | MediaExpert |  |
| AE11 | WM |  |
| AF11 | https://www.mediaexpert.pl/search?query%5Bquerystring%5D=suszarka+slim |  |
| AH11 | 12 |  |
| AI11 | Czech |  |
| AJ11 | Alza |  |
| AK11 | REF |  |
| AL11 | https://www.alza.cz/lg-gslv71mctd-d7917928.htm |  |
| AN11 | 13 |  |
| AO11 | Sweden |  |
| AP11 | Elgiganten |  |
| AQ11 | WM |  |
| AR11 | https://www.elgiganten.se/product/outlet/lg-tvattmaskin-fv34jns0a1-11kg/643636 |  |
| AT11 | 14 |  |
| AU11 | Spain |  |
| AV11 | MediaMarkt |  |
| AW11 | REF |  |
| AX11 | https://www.mediamarkt.es/es/product/_frigorifico-combi-lg-gbbs726cev-altura-2030-mm-negro-167388008.html |  |
| AZ11 | 24 |  |
| BA11 | Czech |  |
| BB11 | Alza |  |
| BC11 | WM |  |
| BD11 | https://www.alza.cz/lg-washtower-wt1716bbf-levne-d13173026.htm |  |
| BF11 | 25 |  |
| BG11 | Czech |  |
| BH11 | Alza |  |
| BI11 | WM |  |
| BJ11 | https://www.alza.cz/lg-fcr7a06pg-sleva-d12647750.htm |  |
| BL11 | 33 |  |
| BM11 | Czech |  |
| BN11 | Alza |  |
| BO11 | REF |  |
| BP11 | https://www.alza.cz/lg-gslv71mctd-d7917928.htm |  |
| BR11 | 35 |  |
| BS11 | Czech |  |
| BT11 | Alza |  |
| BU11 | REF |  |
| BV11 | https://www.alza.cz/lg-gsgv80pyld-d7951209.htm |  |
| BX11 | 45 |  |
| BY11 | Czech |  |
| BZ11 | Alza |  |
| CA11 | REF |  |
| CB11 | https://www.alza.cz/lg-gbbsj1ccpy-d13121338.htm |  |
| CD11 | 43 |  |
| CE11 | France |  |
| CF11 | Darty |  |
| CG11 | WM |  |
| CH11 | https://www.darty.com/nav/achat/gros_electromenager/lavage_sechage/lave-linge_sechant/lg_f214wt8grbe.html |  |
| CJ11 | 34 |  |
| CK11 | Czech |  |
| CL11 | Alza |  |
| CM11 | WM |  |
| CN11 | https://www.alza.cz/lg-fsr7a04pg-bazar-d12747490.htm |  |
| CP11 | 39 |  |
| CQ11 | Czech |  |
| CR11 | Alza |  |
| CS11 | WM |  |
| CT11 | https://www.alza.cz/lg-fasr3a04ww-d12518413.htm |  |
| CV11 | 40 |  |
| CW11 | Czech |  |
| CX11 | Alza |  |
| CY11 | WM |  |
| CZ11 | https://www.alza.cz/lg-fa2s8v3gn3w-d7951214.htm |  |
| DB11 | 46 |  |
| DC11 | Czech |  |
| DD11 | Alza |  |
| DE11 | WM |  |
| DF11 | https://www.alza.cz/lg-fa2s8v3gn3w-d7951214.htm |  |
| DH11 | 29 |  |
| DI11 | Czech |  |
| DJ11 | Alza |  |
| DK11 | WM |  |
| DL11 | https://www.alza.cz/lg-fsr7a04pg-bazar-d12747490.htm |  |
| DN11 | 44 |  |
| DO11 | Czech |  |
| DP11 | Alza |  |
| DQ11 | WM |  |
| DR11 | https://www.alza.cz/lg-fa2s8v3gn3w-d7951214.htm |  |
| DZ11 | 38 |  |
| EA11 | Czech |  |
| EB11 | Alza |  |
| EC11 | WM |  |
| ED11 | https://www.alza.cz/lg-rhx5008tbb-sleva-d13445821.htm |  |
| EF11 | 18 |  |
| EG11 | Netherlands |  |
| EH11 | COOLBLUE |  |
| EI11 | WM |  |
| EJ11 | https://www.coolblue.nl/wasmachines/lg |  |
| ER11 | 20 |  |
| ES11 | Italy |  |
| ET11 | MEDIAWORLD |  |
| EU11 | WM |  |
| EV11 | https://www.mediaworld.it/it/brand/lg/lavatrici |  |
| FJ11 | 23 |  |
| FK11 | Italy |  |
| FL11 | AMAZON |  |
| FM11 | REF |  |
| FN11 | https://www.amazon.it/stores/page/5DE174FF-7426-4856-9BA8-3EF64DA9BCC5?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| FP11 | 8 |  |
| FQ11 | Sweden |  |
| FR11 | Elgiganten |  |
| FS11 | REF |  |
| FT11 | https://www.elgiganten.se/brand/lg/kylskap-lg |  |
| GB11 | Sweden |  |
| GC11 | ELGIGANTEN |  |
| GD11 | REF |  |
| GE11 | 8 |  |
| GF11 | https://www.elgiganten.se/brand/lg/kylskap-lg |  |
| GG11 | Sweden&#124;ELGIGANTEN&#124;REF&#124;8 |  |
| GH11 | 230 |  |
| GM11 | Poland&#124;RTV EURO AGD&#124;REF&#124;11 |  |
| GN11 | 1 |  |
| GP11 | 9 |  |
| GQ11 | Spain |  |
| GR11 | Media Markt |  |
| GS11 | 8 |  |
| GT11 | Alt Text Implementation |  |
| GU11 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV11 | https://www.mediamarkt.es/es/brand/lg-electronics |  |
| GW11 | N |  |

## Row 12

| 셀 | 원문 값 또는 수식 캐시 | 수식 |
| --- | --- | --- |
| A12 | Media Markt |  |
| B12 | Media Markt |  |
| J12 | 8 |  |
| K12 | Sweden |  |
| L12 | Elgiganten |  |
| M12 | WM |  |
| N12 | https://www.elgiganten.se/brand/lg/lg-tvattmaskin-och-torktumlare |  |
| AB12 | 11 |  |
| AC12 | Poland |  |
| AD12 | MediaExpert |  |
| AE12 | WM |  |
| AF12 | https://www.mediaexpert.pl/search?query%5Bquerystring%5D=zestaw+pralka+i+suszarka |  |
| AH12 | 12 |  |
| AI12 | Czech |  |
| AJ12 | Alza |  |
| AK12 | REF |  |
| AL12 | https://www.alza.cz/lg-gsle91mbac-d12316100.htm |  |
| AN12 | 13 |  |
| AO12 | Sweden |  |
| AP12 | Elgiganten |  |
| AQ12 | WM |  |
| AR12 | https://www.elgiganten.se/product/outlet/lg-tvattmaskin-fv94ens2ba-11kg/715577 |  |
| AT12 | 14 |  |
| AU12 | Spain |  |
| AV12 | MediaMarkt |  |
| AW12 | REF |  |
| AX12 | https://www.mediamarkt.es/es/product/_frigorifico-americano-lg-gmv960mbde-no-frost-1787-cm-666-l-instaviewtm-linear-coolingtm-plata-1601366.html |  |
| AZ12 | 24 |  |
| BA12 | Czech |  |
| BB12 | Alza |  |
| BC12 | REF |  |
| BD12 | https://www.alza.cz/lg-gmg860epbe-d12379812.htm |  |
| BF12 | 25 |  |
| BG12 | Czech |  |
| BH12 | Alza |  |
| BI12 | REF |  |
| BJ12 | https://www.alza.cz/lg-gbbsj11dsw-d13525163.htm |  |
| BL12 | 33 |  |
| BM12 | Czech |  |
| BN12 | Alza |  |
| BO12 | REF |  |
| BP12 | https://www.alza.cz/lg-gsle91mbac-d12316100.htm |  |
| BR12 | 35 |  |
| BS12 | Czech |  |
| BT12 | Alza |  |
| BU12 | REF |  |
| BV12 | https://www.alza.cz/lg-gtfn256set-d13087187.htm |  |
| BX12 | 45 |  |
| BY12 | Czech |  |
| BZ12 | Alza |  |
| CA12 | WM |  |
| CB12 | https://www.alza.cz/lg-washtower-wt1716bbf-levne-d13173026.htm |  |
| CD12 | 43 |  |
| CE12 | Italy |  |
| CF12 | Mediaworld |  |
| CG12 | REF |  |
| CH12 | https://www.mediaworld.it/it/product/_lg-gsle91mbac-frigorifero-americano-399927.html |  |
| CJ12 | 34 |  |
| CK12 | Czech |  |
| CL12 | Alza |  |
| CM12 | WM |  |
| CN12 | https://www.alza.cz/lg-fa2s8v3gn3w-d7951214.htm |  |
| CP12 | 39 |  |
| CQ12 | Czech |  |
| CR12 | Alza |  |
| CS12 | WM |  |
| CT12 | https://www.alza.cz/lg-fcr7a06pg-d7917929.htm |  |
| CV12 | 40 |  |
| CW12 | Czech |  |
| CX12 | Alza |  |
| CY12 | WM |  |
| CZ12 | https://www.alza.cz/lg-fsr5a94wl-sleva-d12569671.htm |  |
| DB12 | 46 |  |
| DC12 | Czech |  |
| DD12 | Alza |  |
| DE12 | WM |  |
| DF12 | https://www.alza.cz/lg-fsr5a94wl-sleva-d12569671.htm |  |
| DH12 | 29 |  |
| DI12 | Czech |  |
| DJ12 | Alza |  |
| DK12 | WM |  |
| DL12 | https://www.alza.cz/lg-fa2s8v3gn3w-d7951214.htm |  |
| DN12 | 44 |  |
| DO12 | Czech |  |
| DP12 | Alza |  |
| DQ12 | REF |  |
| DR12 | https://www.alza.cz/lg-gbbsj1ccpy-d13121338.htm |  |
| DZ12 | 38 |  |
| EA12 | Czech |  |
| EB12 | Alza |  |
| EC12 | REF |  |
| ED12 | https://www.alza.cz/lg-gmm42abbeh-bazar-d13516314.htm |  |
| EF12 | 18 |  |
| EG12 | Netherlands |  |
| EH12 | Media Markt |  |
| EI12 | REF |  |
| EJ12 | https://www.mediamarkt.nl/nl/category/lg-koelkasten-964.html |  |
| ER12 | 20 |  |
| ES12 | Netherlands |  |
| ET12 | COOLBLUE |  |
| EU12 | WM |  |
| EV12 | https://www.coolblue.nl/was-droogcombinaties/lg |  |
| FJ12 | 23 |  |
| FK12 | Italy |  |
| FL12 | AMAZON |  |
| FM12 | WM |  |
| FN12 | https://www.amazon.it/stores/page/999E54C1-41F6-4C23-BD58-C9CFDC61A728?ingress=0&amp;visitId=4e7fdec3-2220-4e30-9557-4579dcd29d60 |  |
| FP12 | 8 |  |
| FQ12 | Sweden |  |
| FR12 | Elgiganten |  |
| FS12 | WM |  |
| FT12 | https://www.elgiganten.se/brand/lg/lg-tvattmaskin-och-torktumlare |  |
| GB12 | Sweden |  |
| GC12 | ELGIGANTEN |  |
| GD12 | W/M |  |
| GE12 | 8 |  |
| GF12 | https://www.elgiganten.se/brand/lg/lg-tvattmaskin-och-torktumlare |  |
| GG12 | Sweden&#124;ELGIGANTEN&#124;W/M&#124;8 |  |
| GH12 | 248 |  |
| GM12 | Poland&#124;RTV EURO AGD&#124;W/M&#124;11 |  |
| GN12 | 1 |  |
| GP12 | 10 |  |
| GQ12 | Spain |  |
| GR12 | Media Markt |  |
| GS12 | 8 |  |
| GT12 | Alt Text Implementation |  |
| GU12 | Add alt text to the 10 largest images on the Brand Category Page |  |
| GV12 | https://www.mediamarkt.es/es/brand/lg-electronics/lavavajillas |  |
| GW12 | N |  |
| HB12 | Italy&#124;Amazon&#124;ID8-&gt;0 ; France&#124;Boulanger&#124;ID8-&gt;291 ; Netherlands&#124;Coolblue&#124;ID8-&gt;177 ; France&#124;Darty&#124;ID8-&gt;0 ; Sweden&#124;ELGIGANTEN&#124;ID8-&gt;230 ; Spain&#124;Media Markt&#124;ID8-&gt;34 ; Italy&#124;Media World&#124;ID8-&gt;75 ; Italy&#124;Amazon&#124;ID9-&gt;115 ; Czech&#124;Datart&#124;ID9-&gt;0 | =_xlfn.LET(_xlpm.a,_xlfn.ANCHORARRAY(GB3),_xlpm.cat,INDEX(_xlpm.a,,3),_xlpm.m,INDEX(_xlpm.a,,7),_xlpm.f,_xlfn._xlws.FILTER(_xlfn.HSTACK(INDEX(_xlpm.a,,1),INDEX(_xlpm.a,,2),INDEX(_xlpm.a,,4),_xlpm.m),_xlpm.cat="ALL"),_xlfn.TEXTJOIN(" ; ",TRUE,INDEX(_xlpm.f,,1)&amp;"&#124;"&amp;INDEX(_xlpm.f,,2)&amp;"&#124;ID"&amp;INDEX(_xlpm.f,,3)&amp;"-&gt;"&amp;INDEX(_xlpm.f,,4))) [OOXML {"t": "array", "ref": "HB12"}] |

## 수식 표본

| 셀 | 저장된 캐시 | 수식 |
| --- | --- | --- |
| FO1 | 7197 | =ROWS(_xlfn.ANCHORARRAY(FP3)) |
| GA1 | 7120 | =SUMPRODUCT(--(INDEX(_xlfn.ANCHORARRAY(GB3),,7)&gt;0)) [OOXML {"t": "array", "ref": "GA1"}] |
| GI1 | 433 | =ROWS(_xlfn.ANCHORARRAY('Improvement Task'!B3)) |
| GO1 | 7120 | =ROWS(_xlfn.ANCHORARRAY(GP3)) |
| GY1 | #VALUE! | =_xlfn.LET(_xlpm.a,_xlfn.ANCHORARRAY(GB3),_xlpm.cat,INDEX(_xlpm.a,,3),_xlpm.blank,(_xlpm.cat=0)+(_xlpm.cat=""),_xlpm.f,_xlfn._xlws.FILTER(INDEX(_xlpm.a,,1)&amp;"&#124;"&amp;INDEX(_xlpm.a,,2)&amp;"&#124;"&amp;INDEX(_xlpm.a,,4),_xlpm.blank&gt;0),_xlfn.TEXTJOIN(" ; ",TRUE,_xlfn.UNIQUE(_xlpm.f))) [OOXML {"t": "array", "ref": "GY1"}] |
| HB1 | 433 | =ROWS(_xlfn.ANCHORARRAY('Improvement Task'!$B$3)) |
| GA2 | 7197 | =ROWS(_xlfn.ANCHORARRAY(GB3)) |
| GI2 | ECI | =IFERROR(_xlfn.XLOOKUP("Elcorteingles_electronica",$A$2:$A$15,$B$2:$B$15),"NG") |
| HB2 | a-&gt;1 ; b-&gt;2 | =_xlfn.TEXTJOIN(" ; ",TRUE,{"a","b"}&amp;"-&gt;"&amp;{1,2}) [OOXML {"t": "array", "ref": "HB2"}] |
| J3 | 8 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID8'!$A:$A,2,-1)),_xlpm.xc,'ID8'!$C$2:INDEX('ID8'!$C:$C,_xlpm.n),_xlpm.xd,'ID8'!$D$2:INDEX('ID8'!$D:$D,_xlpm.n),_xlpm.xe,'ID8'!$E$2:INDEX('ID8'!$E:$E,_xlpm.n),_xlpm.xf,'ID8'!$F$2:INDEX('ID8'!$F:$F,_xlpm.n),_xlpm.xh,'ID8'!$H$2:INDEX('ID8'!$H:$H,_xlpm.n),_xlpm.xi,'ID8'!$I$2:INDEX('ID8'!$I:$I,_xlpm.n),_xlpm.xj,'ID8'!$J$2:INDEX('ID8'!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xi="Brand Category Page 영역 내 Alt text 적용 여부")*(_xlpm.xj="N"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,8,8),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "J3:N22"}] |
| P3 | 9 | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID9'!$A:$A,2,-1)),_xlpm.xc,'ID9'!$C$2:INDEX('ID9'!$C:$C,_xlpm.n),_xlpm.xd,'ID9'!$D$2:INDEX('ID9'!$D:$D,_xlpm.n),_xlpm.xe,'ID9'!$E$2:INDEX('ID9'!$E:$E,_xlpm.n),_xlpm.xf,'ID9'!$F$2:INDEX('ID9'!$F:$F,_xlpm.n),_xlpm.xh,'ID9'!$H$2:INDEX('ID9'!$H:$H,_xlpm.n),_xlpm.xk,'ID9'!$K$2:INDEX('ID9'!$K:$K,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xk="N"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,9,9),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "P3:T8"}] |
| V3 |  | =_xlfn.LET(_xlpm.n,MAX(2,_xlfn.XMATCH("?*",'ID10'!$A:$A,2,-1)),_xlpm.xc,'ID10'!$C$2:INDEX('ID10'!$C:$C,_xlpm.n),_xlpm.xd,'ID10'!$D$2:INDEX('ID10'!$D:$D,_xlpm.n),_xlpm.xe,'ID10'!$E$2:INDEX('ID10'!$E:$E,_xlpm.n),_xlpm.xf,'ID10'!$F$2:INDEX('ID10'!$F:$F,_xlpm.n),_xlpm.xh,'ID10'!$H$2:INDEX('ID10'!$H:$H,_xlpm.n),_xlpm.xi,'ID10'!$I$2:INDEX('ID10'!$I:$I,_xlpm.n),_xlpm.xj,'ID10'!$J$2:INDEX('ID10'!$J:$J,_xlpm.n),_xlpm.m,(_xlpm.xf="LG")*(_xlpm.xi="Canonical URL / 페이지 URL 동일 여부")*(_xlpm.xj="N"),_xlfn._xlws.FILTER(_xlfn.HSTACK(IF(_xlpm.m,10,10),_xlpm.xc,_xlpm.xd,_xlpm.xe,_xlpm.xh),_xlpm.m,IF(1,_xlfn.HSTACK("","","","","")))) [OOXML {"t": "array", "ref": "V3:Z3"}] |
