-- MySQL 초기화 스크립트 (docker-entrypoint-initdb.d 에서 자동 실행)
-- 실행 순서: 01_init.sql → 02_schema.sql

-- ── 데이터베이스 생성 ─────────────────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS lg_clinic
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Airflow 메타데이터 DB (Airflow 가 직접 스키마를 생성 — 여기선 DB만 만든다)
CREATE DATABASE IF NOT EXISTS airflow
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ── 사용자 권한 ───────────────────────────────────────────────────────────────
-- MYSQL_USER 로 생성된 clinic_user 에게 두 DB 모두 권한 부여
GRANT ALL PRIVILEGES ON lg_clinic.* TO 'clinic_user'@'%';
GRANT ALL PRIVILEGES ON airflow.*   TO 'clinic_user'@'%';
FLUSH PRIVILEGES;
