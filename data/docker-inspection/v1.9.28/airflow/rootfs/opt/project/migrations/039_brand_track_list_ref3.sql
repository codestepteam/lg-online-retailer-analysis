-- Migration 039 (2026-08-04): brand_track_list 참고3 개정
--
-- 참고3 잔여 컬럼 건은 EY 회신(2026-08-04)으로 해소 — 적용 확정.
--   적용 시점 = 다음 pdp/home 배치 전.
--
-- 소스: EY 'LGE_경쟁사 Brand_Brand Category Page_v0.1_260804.xlsx' 참고3
--   (클리닉 대상 브랜드, 업데이트 2026-08-03). mig 024 대비 변경 3건:
--   · IT W/M 5위: HAIER → CANDY 교체
--   · SE W/M 5위: HISENSE 신규 (4개→5개)
--   · CZ W/M·REF 개정 (⚠️ CZ REF 1위가 GORENJE)
--
-- [해소 — EY 회신 2026-08-04] 참고3 J·L 잔여 브랜드 열은 무시 확정
--   ("체코 참고3 신규 추가 브랜드 신경 안 씀") — 본 랭크 그대로 확정.
-- [영향] pdp 크롤 진입 필터(crawl.filter_brand_track) + ID1/2/4/12 브랜드 판정
--   + 요건4 rank_sum_points 브랜드 세트.
-- ⚠️ 실측(2026-08-04 devtools): CZ 는 "기존 테이블에 없음"이 아니라 CZ 온보딩
--   임시 세트(PL 유사 — WM 5위 HAIER, SAMSUNG 부재)가 이미 있었다 → 단순
--   INSERT 는 PK(cntry_cd,cat_cd,brand_name) 충돌로 중단. 아래는 재실행 안전한
--   DELETE-후-INSERT 형태로 개정 (devtools 는 동치의 정정 3문으로 적용 완료).

-- ── 1) IT W/M 5위 교체: HAIER → CANDY ────────────────────────────────────────
UPDATE brand_track_list SET brand_name='CANDY'
 WHERE cntry_cd='IT' AND cat_cd='WM' AND brand_name='HAIER';

-- ── 2) SE W/M 5위 신설: HISENSE (재실행 안전) ────────────────────────────────
INSERT INTO brand_track_list (cntry_cd, cat_cd, brand_name, brand_rank) VALUES
('SE','WM','HISENSE',5)
ON DUPLICATE KEY UPDATE brand_rank=5;

-- ── 3) CZ 개정 (W/M + REF — 기존 임시 세트 전체 교체) ────────────────────────
DELETE FROM brand_track_list WHERE cntry_cd='CZ';
INSERT INTO brand_track_list (cntry_cd, cat_cd, brand_name, brand_rank) VALUES
('CZ','WM','LG',1),('CZ','WM','AEG',2),('CZ','WM','BOSCH',3),
('CZ','WM','SAMSUNG',4),('CZ','WM','GORENJE',5),
('CZ','REF','GORENJE',1),('CZ','REF','SAMSUNG',2),('CZ','REF','LG',3),
('CZ','REF','HISENSE',4),('CZ','REF','BOSCH',5);
