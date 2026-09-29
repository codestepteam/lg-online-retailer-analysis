-- Migration 027: ocr_lexicon metric='etc' 신설 — ID33 기타 텍스트 확정 문구 (2026-07-16)
--
-- 배경 (요건 변경 2026-07-16)
--   ID33 '기타텍스트'가 "텍스트 有·미분류 전부(전 국가)" → "확정 문구 화이트리스트"로
--   변경. 아래 NL/PL 문구와 일치하는 갤러리 콘텐츠 이미지만 기타 텍스트로 계상하고,
--   타 국가(어휘 없음)·문구 미일치는 어느 버킷에도 계상하지 않는다
--   (eval.metric_33 + _norm_phrase 가 이 migration 과 세트).
--
-- 의미 규칙
--   - term 저장 규약은 mig 022 와 동일: 대문자 + 분음부호 제거 (Twoją→TWOJA, wygodę→WYGODE).
--   - 매칭은 eval._norm_phrase 어절 시퀀스 — 문장부호('!'·구분 슬래시)를 공백으로 접어
--     OCR 이 부호를 흘리거나 오독해도 맞는다. '/'로 묶인 NL 소음 스케일 4단계 라벨은
--     행 분리(이미지가 어느 라벨을 노출하든 인정). GEMIDDELD/LUID 단독 라벨은 일반어라
--     오탐 여지가 있으나 확정 리스트 그대로 적재 — 경계 매칭이 GELUID 류 합성어는 차단.
--   - EN(공통) 행 없음 → NL/PL 외 국가는 refdata.ocr_terms('etc', cntry) 가 빈 리스트.
--
-- 실행: mysql -u <user> -p <db> < migrations/027_ocr_lexicon_etc_other_text.sql

ALTER TABLE ocr_lexicon
    MODIFY metric enum('warranty','dimension','certification','awards','etc') NOT NULL
        COMMENT 'OCR 지표. warranty/certification=mig 022 확정 리스트(국가당 1어), dimension=기존 기준 유지, awards=enum 값만(행 없음, v1.4 제외), etc=ID33 기타 텍스트 확정 문구(mig 027, NL/PL)',
    MODIFY slot varchar(32) NOT NULL
        COMMENT '역할: warranty→warranty(확정—단독 인정) · certification→cert_phrase · dimension→height/width/depth/unit/reversible_door · etc→color_notice/noise_level/service_visit/comfort (mig 027)';

INSERT INTO ocr_lexicon (metric, slot, cntry_cd, term) VALUES
    ('etc', 'color_notice',  'NL', 'LET OP! DE KLEUR AAN DE VOORKANT VERSCHILT VAN DE ZIJKANT'),
    ('etc', 'noise_level',   'NL', 'VEEL STILLER DAN GEMIDDELD'),
    ('etc', 'noise_level',   'NL', 'STILLER DAN GEMIDDELD'),
    ('etc', 'noise_level',   'NL', 'GEMIDDELD'),
    ('etc', 'noise_level',   'NL', 'LUID'),
    ('etc', 'service_visit', 'PL', 'WSZYSTKO PRZY JEDNEJ WIZYCIE!'),
    ('etc', 'comfort',       'PL', 'DBAMY O TWOJA WYGODE!');
