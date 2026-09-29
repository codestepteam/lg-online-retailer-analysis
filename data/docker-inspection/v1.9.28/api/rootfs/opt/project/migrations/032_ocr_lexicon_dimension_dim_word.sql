-- Migration 032: ocr_lexicon dimension 'dim_word' 슬롯 신설 — 치수 명사 단독 인정 (2026-07-22)
--
-- 배경 (2026-07-22 지시)
--   치수 이미지 판정(ID40/46, ID33 dimension 버킷) 조건 1을
--   "길이 표기(숫자+cm/mm) 2개 이상" → "길이 표기 2개 이상 OR 치수 명사 포함" 으로 확장.
--   국가별 치수 명사(ES/IT/FR dimension·NL afmeting·SE mått·PL wymiar·CZ rozm)를
--   ocr_lexicon 행으로 관리 — 행 추가/수정만으로 코드 수정 없이 판정 어휘가 바뀐다.
--   조건 2(에너지라벨 아님)는 그대로 — dim_word 매칭이어도 에너지라벨이면 제외
--   (eval._dimension_evidence 가 이 migration 과 세트).
--
-- 의미 규칙
--   - term 저장 규약(mig 022: 대문자+분음부호 제거)에 신규 '*' 접미 규약 추가 =
--     **접두 매칭** (eval._term_re 가 '*' 인식 — 좌측 영숫자 경계만 강제, 우측 개방).
--     굴절 흡수: DIMENSION*→Dimensiones/Dimensioni/Dimensions, AFMETING*→Afmetingen,
--     MATT*→Mått/Måtten, WYMIAR*→Wymiary/Wymiarach, ROZM*→Rozměry.
--     '*' 미인식 구버전 eval 에는 이 행들이 사실상 불활성(리터럴 '*' 매칭) — 배포 격차 안전.
--   - slot='dim_word' 는 **단독 근거(확정 계층)** — 기존 height/width/depth 슬롯
--     (ALTO 상투구 오탐으로 0719 라벨 보조 격하)과 계층이 다르다.
--   - ⚠️ CZ 'ROZM*' 는 rozmrazování(성에 제거 — 냉장고 콘텐츠 상용어) 접두와 충돌
--     소지. 지시 그대로 적재하되, 오탐 확인 시 이 행만 'ROZMER*' 로 UPDATE 하면
--     코드 수정 없이 교정된다. SE 'MATT*' 도 matta(매트/카펫) 접두 충돌 소지 동일.
--
-- 실행: mysql -u <user> -p <db> < migrations/032_ocr_lexicon_dimension_dim_word.sql

ALTER TABLE ocr_lexicon
    MODIFY slot varchar(32) NOT NULL
        COMMENT '역할: warranty→warranty(확정—단독 인정) · certification→cert_phrase · dimension→height/width/depth/unit/reversible_door(라벨 보조)+dim_word(확정—단독 인정, mig 032, *=접두 매칭) · etc→color_notice/noise_level/service_visit/comfort';

INSERT INTO ocr_lexicon (metric, slot, cntry_cd, term) VALUES
    ('dimension', 'dim_word', 'ES', 'DIMENSION*'),
    ('dimension', 'dim_word', 'IT', 'DIMENSION*'),
    ('dimension', 'dim_word', 'FR', 'DIMENSION*'),
    ('dimension', 'dim_word', 'NL', 'AFMETING*'),
    ('dimension', 'dim_word', 'SE', 'MATT*'),
    ('dimension', 'dim_word', 'PL', 'WYMIAR*'),
    ('dimension', 'dim_word', 'CZ', 'ROZM*');
