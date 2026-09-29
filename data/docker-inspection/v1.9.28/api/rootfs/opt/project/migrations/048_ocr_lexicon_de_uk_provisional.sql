-- Migration 048: ocr_lexicon DE/UK 임시(예시) 시딩 — ⚠️ 확정 아님
--
-- 배경 (2026-08-21, DE/UK 5개 리테일러 pdp 온보딩)
--   warranty/dimension/certification 판정 사전에 DE·UK 행이 전무 — 배치 20260821_ukde
--   수집분 파싱 전 임시로 채운다. **본 시딩은 에이전트 제안 예시이며 EY/내부 확정 전**
--   (표기 변형 임의 추가 금지 원칙[usp_master 규약]과 동일선상 — 확정본 수령 시 교체).
--
--   설계 원칙:
--   · EN 공통 행(depth/height/width/unit/REVERSIBLE DOOR/cert_mark)은 UK 를 이미 커버.
--   · 신규 행은 전부 **국가 스코프(DE/UK)** — EN 공통에 넣으면 기존 7개국 판정이
--     소급 변동되므로 금지 (확정 단계에서 EN 승격 여부 별도 판단).
--   · 악센트는 기존 SE/PL 시드 전례대로 ASCII 접힌 형태로 적재 (Höhe→HOHE —
--     비교기 _term_re 가 접기 수행).
--   · 독일어 Maße(→MASSE)는 Masse(질량)와 충돌해 제외 (ROZM*/MATT* 오탐경계 교훈).
--     reversible_door 는 TURANSCHLAG*(Türanschlag …wechselbar 스펙 블록) 접두 —
--     오탐/미탐 경계는 첫 배치 실측으로 재평가.
--
-- 실행: mysql --default-character-set=utf8mb4 -u <user> -p lg_clinic \
--         < migrations/048_ocr_lexicon_de_uk_provisional.sql
-- 멱등: (metric,slot,cntry_cd,term) 부재 시에만 INSERT.

INSERT INTO ocr_lexicon (metric, slot, cntry_cd, term)
SELECT * FROM (
    SELECT 'warranty' AS metric, 'warranty' AS slot, 'DE' AS cntry_cd, 'GARANTIE' AS term UNION ALL
    SELECT 'dimension', 'dim_word',        'DE', 'ABMESSUNG*'   UNION ALL
    SELECT 'dimension', 'depth',           'DE', 'TIEFE'        UNION ALL
    SELECT 'dimension', 'height',          'DE', 'HOHE'         UNION ALL
    SELECT 'dimension', 'width',           'DE', 'BREITE'       UNION ALL
    SELECT 'dimension', 'reversible_door', 'DE', 'TURANSCHLAG*' UNION ALL
    SELECT 'certification', 'cert_phrase', 'DE', 'ZERTIFIZIERUNG' UNION ALL
    SELECT 'warranty',  'warranty',        'UK', 'WARRANTY'     UNION ALL
    SELECT 'warranty',  'warranty',        'UK', 'GUARANTEE'    UNION ALL
    SELECT 'dimension', 'dim_word',        'UK', 'DIMENSION*'   UNION ALL
    SELECT 'certification', 'cert_phrase', 'UK', 'CERTIFICATION'
) t
WHERE NOT EXISTS (
    SELECT 1 FROM ocr_lexicon o
    WHERE o.metric = t.metric AND o.slot = t.slot
      AND o.cntry_cd = t.cntry_cd AND o.term = t.term
);
