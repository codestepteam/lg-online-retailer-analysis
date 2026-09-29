-- Migration 022: ocr_lexicon 재구성 — Warranty/Certification 확정 어휘 + dimension 기준 유지
--
-- 배경 (2026-07-15 확정)
--   Warranty/Certification 판별 어휘가 EY 확정 리스트(기준 키워드 × 7개국 로컬 키워드,
--   국가당 1어)로 좁혀졌다. 기존 warranty 슬롯 세분(year_unit/component_*/lifetime)·
--   certification EN 공통(TUV 등)·awards 행은 폐기, dimension 기준 어휘(ID40/46/33)는
--   기존 그대로 유지. 실행 전 ~/Downloads/ocr_lexicon_backup_20260715.xlsx 백업 완료.
--
-- 의미 규칙
--   - 국가는 국가명이 아니라 cntry_cd 2자리 코드 (판정이 parsed.cntry_cd 와
--     `cntry_cd IN (국가,'EN')` 매칭 — refdata.ocr_terms). CZ(체코) 신규 —
--     단 dimension 은 CZ 확정 어휘 미수령, 수치+단위 패턴만으로 동작.
--   - term 은 저장 규약(대문자 + 분음부호 제거) 유지: GARANTIA/CERTIFICACION/ZARUKA.
--     악센트 원문(Garantía 등) OCR 매칭은 eval._lexicon_scan 이 스캔 텍스트를
--     같은 규약으로 접어서(NFKD 분음부호 제거) 흡수한다 (이 migration 과 세트).
--   - slot: warranty→'warranty'(확정 계층 — 단독 인정), certification→'cert_phrase',
--     dimension→height/width/depth/unit/reversible_door (기존 유지).
--     warranty 보조 계층(year_unit/component_*/tech_*) 행은 더 이상 없다 —
--     ID39 는 확정 어휘 단독 판정.
--   - is_verified(확정 리스트라 무의미)·notes 컬럼 제거 — refdata.ocr_terms 조건 동시 제거.
--   - metric enum 의 awards 값은 유지 (v1.4 제외 지표 — 값 제거 시 strict mode
--     오류 위험, 행만 비움).
--
-- 실행: mysql -u <user> -p <db> < migrations/022_ocr_lexicon_warranty_cert_only.sql

DELETE FROM ocr_lexicon;

ALTER TABLE ocr_lexicon
    DROP COLUMN is_verified,
    DROP COLUMN notes,
    MODIFY slot varchar(32) NOT NULL
        COMMENT '역할: warranty→warranty(확정—단독 인정) · certification→cert_phrase · dimension→height/width/depth/unit/reversible_door (mig 022)';

INSERT INTO ocr_lexicon (metric, slot, cntry_cd, term) VALUES
    ('warranty',      'warranty',    'ES', 'GARANTIA'),
    ('warranty',      'warranty',    'FR', 'GARANTIE'),
    ('warranty',      'warranty',    'IT', 'GARANZIA'),
    ('warranty',      'warranty',    'NL', 'GARANTIE'),
    ('warranty',      'warranty',    'SE', 'GARANTI'),
    ('warranty',      'warranty',    'PL', 'GWARANCJA'),
    ('warranty',      'warranty',    'CZ', 'ZARUKA'),
    ('certification', 'cert_phrase', 'ES', 'CERTIFICACION'),
    ('certification', 'cert_phrase', 'FR', 'CERTIFICATION'),
    ('certification', 'cert_phrase', 'IT', 'CERTIFICAZIONE'),
    ('certification', 'cert_phrase', 'NL', 'CERTIFICERING'),
    ('certification', 'cert_phrase', 'SE', 'CERTIFIERING'),
    ('certification', 'cert_phrase', 'PL', 'CERTYFIKACJA'),
    ('certification', 'cert_phrase', 'CZ', 'CERTIFIKACE');

-- dimension 기준 어휘 — 기존 유지 (백업 원본 그대로 재적재. CZ 는 확정 어휘 미수령)
INSERT INTO ocr_lexicon (metric, slot, cntry_cd, term) VALUES
    ('dimension', 'depth',           'EN', 'DEPTH'),
    ('dimension', 'height',          'EN', 'HEIGHT'),
    ('dimension', 'reversible_door', 'EN', 'REVERSIBLE DOOR'),
    ('dimension', 'unit',            'EN', 'MM'),
    ('dimension', 'unit',            'EN', 'CM'),
    ('dimension', 'width',           'EN', 'WIDTH'),
    ('dimension', 'depth',           'ES', 'FONDO'),
    ('dimension', 'depth',           'ES', 'PROFUNDIDAD'),
    ('dimension', 'height',          'ES', 'ALTO'),
    ('dimension', 'height',          'ES', 'ALTURA'),
    ('dimension', 'reversible_door', 'ES', 'PUERTA REVERSIBLE'),
    ('dimension', 'width',           'ES', 'ANCHO'),
    ('dimension', 'width',           'ES', 'ANCHURA'),
    ('dimension', 'depth',           'FR', 'PROFONDEUR'),
    ('dimension', 'height',          'FR', 'HAUTEUR'),
    ('dimension', 'reversible_door', 'FR', 'PORTE REVERSIBLE'),
    ('dimension', 'width',           'FR', 'LARGEUR'),
    ('dimension', 'depth',           'IT', 'PROFONDITA'),
    ('dimension', 'height',          'IT', 'ALTEZZA'),
    ('dimension', 'reversible_door', 'IT', 'PORTA REVERSIBILE'),
    ('dimension', 'width',           'IT', 'LARGHEZZA'),
    ('dimension', 'depth',           'NL', 'DIEPTE'),
    ('dimension', 'height',          'NL', 'HOOGTE'),
    ('dimension', 'reversible_door', 'NL', 'OMKEERBARE DEUR'),
    ('dimension', 'width',           'NL', 'BREEDTE'),
    ('dimension', 'depth',           'PL', 'GLEBOKOSC'),
    ('dimension', 'height',          'PL', 'WYSOKOSC'),
    ('dimension', 'reversible_door', 'PL', 'DRZWI DWUKIERUNKOWE'),
    ('dimension', 'width',           'PL', 'SZEROKOSC'),
    ('dimension', 'depth',           'SE', 'DJUP'),
    ('dimension', 'height',          'SE', 'HOJD'),
    ('dimension', 'reversible_door', 'SE', 'OMHANGBAR DORR'),
    ('dimension', 'width',           'SE', 'BREDD');
