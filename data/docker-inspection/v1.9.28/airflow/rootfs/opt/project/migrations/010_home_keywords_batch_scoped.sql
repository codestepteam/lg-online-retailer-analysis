-- Migration 010: home_keywords 배치-스코프화 + cntry_code 통일
-- 실행: mysql -u <user> -p <db> < migrations/010_home_keywords_batch_scoped.sql
--
-- 배경
--   home 트랙 독립성 원칙: pdp/plp/home/brand 각 트랙은 서로 의존 없이 실행되고
--   report_date 축에서만 수렴한다. 이전엔 home_keywords 가 배치 무관 고정 테이블이라
--   home 트랙이 pdp batch_id 에 편승해야 실행 가능했다 (독립성 위반).
--
--   ▶ home_target_list (URL 스킴 — 리뉴얼 시에만 바뀜) = 배치 무관 마스터 유지
--   ▶ home_keywords    (배치별 LG HS 팀 지시 키워드)   = batch_id 스코프로 승격
--
-- 흐름 (upload 후)
--   /batches/upload/home  (report_date + 파일)
--     → repo.new_batch_id(report_date, page_type="home")  = 'YYYYMMDD'
--     → home_keywords 에 (batch_id, report_date, ...) 로 UPSERT
--   crawl.py --batch-id <B> --page-type home
--     → load_home_targets(batch_id=B) — 해당 batch 키워드만 조립
--
-- ⚠️ 왜 home_target_list 는 여전히 batch 무관인가
--   URL 스킴은 리테일러가 리뉴얼할 때만 변경 (연 1~2회). 매 배치마다 12행 복제할
--   가치 낮음. 키워드는 배치별로 다르게 오므로 스냅샷 가치 큼.
--
-- 변경 요약
--   1) instance → cntry_code (pdp_target_list/home_target_list 와 명명 통일)
--   2) batch_id VARCHAR(20) NOT NULL + report_date DATE NOT NULL 추가
--   3) UNIQUE KEY 재정의: (batch_id, retailer, cntry_code, keyword)
--   4) 조회 인덱스: (batch_id), (batch_id, cntry_code, retailer)

-- ── 1) 기존 데이터 백필용 상수 (선반영: 이번 배포부터 batch_id 필수) ────────
--    기존 home_keywords 에 배치가 없었으므로 legacy 데이터에 임시 batch_id 부여.
--    실 운영은 새 upload 로 덮어쓰므로 legacy 로우는 사실상 오프라인 시드용.
ALTER TABLE home_keywords
    ADD COLUMN batch_id    VARCHAR(20) NOT NULL DEFAULT 'legacy'   AFTER id,
    ADD COLUMN report_date DATE        NOT NULL DEFAULT '2000-01-01' AFTER batch_id,
    CHANGE COLUMN instance cntry_code CHAR(2) NOT NULL COMMENT '국가 코드 대문자 (예: NL) — home_target_list.cntry_code 와 통일';

-- 기본값은 스키마 자체엔 남기지 않는다 (신규 삽입 시 명시 강제)
ALTER TABLE home_keywords
    ALTER COLUMN batch_id    DROP DEFAULT,
    ALTER COLUMN report_date DROP DEFAULT;

-- ── 2) 인덱스 재정비 ────────────────────────────────────────────────────────
ALTER TABLE home_keywords DROP INDEX uq_keyword;
ALTER TABLE home_keywords
    ADD UNIQUE KEY uq_keyword (batch_id, retailer, cntry_code, keyword),
    ADD INDEX      idx_batch  (batch_id),
    ADD INDEX      idx_filter (batch_id, cntry_code, retailer);
