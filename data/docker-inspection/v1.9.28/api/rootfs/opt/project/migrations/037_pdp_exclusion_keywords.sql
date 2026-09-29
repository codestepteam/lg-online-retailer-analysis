-- Migration 037: pdp_exclusion_keywords 신설 — PDP Product Name 제외판정 키워드 마스터
--
-- 배경 (2026-08-04 EY 주간미팅 확정, 김준형 메일)
--   리퍼비시(Refurbished)/리셀(Resell)/부품(Parts) 상품을 [Product Name] 텍스트로
--   판별해 PDP 리포트에 3컬럼([판정] 유지/제외, [구분] 리퍼비시/리셀/부품/정상,
--   [제외 Keyword])을 추가한다. 행은 유지하고 표기만 한다 (EY 측이 필터) —
--   brand≠manufacturer 게이트(5be7c4c, 행 제거)와는 별개 레이어.
--
-- 의미 규칙
--   - term 은 **EY 리스트 원문 그대로** 적재 (2026-08-04 사용자 확정 "받은대로").
--     ocr_lexicon 의 접기 규약(대문자+분음부호 제거, mig 022)을 따르지 않는다 —
--     EY 가 reconditionné(악센트)/reconditionne(무악센트)를 별도 항목으로 둘 다
--     보낸 것이 EY 매처가 리터럴 방식이라는 증거이며, 접으면 두 행이 충돌하고
--     EY 제공 통계치와 숫자가 어긋난다. 매칭은 eval.classify_exclusion 이
--     소문자+아포스트로피 통일 평면에서 **부분포함(contains)** 으로 수행.
--   - EY 원문 9번 'kit d&#39;encastrement' 는 HTML 엔티티만 디코드해 적재
--     (표기 훼손이 아니라 전송 인코딩 복원).
--   - ex_type 은 [구분] 정본(한글) — 리포트에 매핑 없이 그대로 방출
--     (brand_target_list.sub_category 한글 정본 방식과 동일).
--   - priority = EY 리스트 번호. 다중 히트 시 최소 priority 의 ex_type 이 [구분].
--   - cntry_cd 'EN'=전 국가 공통 (ocr_lexicon 과 동일 규약). 현재 전 행 EN —
--     추후 특정 국가 오탐 시 스키마 변경 없이 국가 한정으로 좁히기 위한 컬럼.
--
-- 실행: mysql -u <user> -p <db> < migrations/037_pdp_exclusion_keywords.sql
--   ⚠️ 로컬 docker + 용산 lg_clinic 양쪽 모두 적용할 것 (ocr_lexicon 배포 사각
--     전례 — mig 034 가 그 뒷수습). 미적용 시 전 행이 조용히 '유지' 처리된다
--     (refdata 로더가 빈 테이블을 경고 로그 후 흡수).

CREATE TABLE pdp_exclusion_keywords (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    ex_type    VARCHAR(16) NOT NULL
        COMMENT '[구분] 정본(한글): 리퍼비시/리셀/부품 — 리포트에 그대로 방출',
    cntry_cd   VARCHAR(2)  NOT NULL DEFAULT 'EN'
        COMMENT '적용 국가. EN=전 국가 공통 (ocr_lexicon 규약)',
    -- COLLATE utf8mb4_bin 필수: DB 기본(utf8mb4_0900_ai_ci)은 악센트 무시(ai)라
    -- reconditionné = reconditionne 로 접혀 UNIQUE 키가 충돌한다 (2026-08-04 용산
    -- 적용 중 실측 ERROR 1062). EY 리터럴 규약(두 변형이 별도 행)의 DB 층 대응.
    term       VARCHAR(64) COLLATE utf8mb4_bin NOT NULL
        COMMENT 'EY 리스트 원문 그대로(리터럴) — [제외 Keyword] 표기 겸용. 매칭은 소문자 contains (eval.classify_exclusion)',
    priority   INT NOT NULL
        COMMENT '다중 히트 시 [구분] 결정 우선순위 — EY 리스트 번호(작을수록 우선)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_cntry_term (cntry_cd, term)
) COMMENT='PDP Product Name 제외판정 키워드 마스터 (EY 2026-08-04 주간미팅 확정)';

-- 시드: EY 리스트 10건 원문 (1~10 = EY 번호 = priority)
INSERT INTO pdp_exclusion_keywords (ex_type, cntry_cd, term, priority) VALUES
    ('리퍼비시', 'EN', 'reacondicionado',      1),
    ('리퍼비시', 'EN', 'reconditionné',        2),
    ('리퍼비시', 'EN', 'reconditionne',        3),
    ('리퍼비시', 'EN', 'ricondizionato',       4),
    ('리퍼비시', 'EN', 'refurbished',          5),
    ('리셀',     'EN', 'outlet',               6),
    ('부품',     'EN', 'accesorio',            7),
    ('부품',     'EN', 'kit de superposition', 8),
    ('부품',     'EN', 'kit d''encastrement',  9),
    ('부품',     'EN', 'accessori',           10);
