-- Migration 029: gnb_depth_list 신설 — ID7(GNB depth) 타깃 소스 분리
--
-- 배경 (2026-07-21 사용자 결정)
--   mig 028 로 brand_target_list 가 category 그룹(WM/REF)+sub_category(한글) 2단
--   구조로 바뀌었는데, ID7 측정(core/gnb_depth.py)의 전략 키(EXTRA_KEYWORDS /
--   UNIEURO_CAT_MENU)와 저장 폴더(depth_{CAT})는 구 flat 코드 체계다.
--   home 트랙 개편 전까지 임시로, 구 brand_target_list 구조 그대로의 별도 마스터
--   (gnb_depth_list)를 두고 crawl.run_gnb_depth 가 이 테이블만 보게 분리한다.
--   ("나중에 수정" — home 개편 시 이 테이블 폐기·통합 예정.)
--
--   시딩은 현 brand_target_list 의 Brand Category Page 행을 한글 sub_category →
--   flat 코드로 접어 복제 (78행, URL 35행). 이후 두 테이블은 독립 관리 —
--   brand_target_list 갱신이 자동 반영되지 않음에 주의.
--
-- 실행: docker exec -i <mysql> mysql --default-character-set=utf8mb4 \
--         -u<user> -p<pw> lg_clinic < migrations/029_add_gnb_depth_list.sql

CREATE TABLE IF NOT EXISTS gnb_depth_list (
    id              INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    brand_page_type VARCHAR(20)       NULL DEFAULT 'Brand Category Page'
        COMMENT '구 brand_target_list 호환 — ID7 대상은 전부 Brand Category Page',
    rtlr_name  VARCHAR(64)   NOT NULL COMMENT '내부 리테일러 순수명 (예: Amazon, Coolblue).',
    cntry_cd   CHAR(2)       NOT NULL COMMENT '국가 코드 대문자 (예: NL)',
    brand      VARCHAR(64)   NOT NULL DEFAULT 'LG' COMMENT '브랜드 (기본 LG)',
    category   VARCHAR(16)   NOT NULL DEFAULT ''
        COMMENT '구 flat 코드 (WM/DR/WD/REF/FZ/FF) — gnb_depth 전략 키·depth_{CAT} 폴더명',
    brand_url  VARCHAR(2048)     NULL COMMENT '측정 목적지 URL. NULL 이면 측정 제외 (notes 참조)',
    notes      VARCHAR(255)      NULL,
    created_at TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_gnb_depth (rtlr_name, cntry_cd, brand, category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  COMMENT='ID7 GNB depth 타깃 마스터 (mig 029 — brand_target_list 개편에서 분리, 임시)';

-- 시딩: brand_target_list Brand Category Page 행 → flat 코드 변환 복제
INSERT INTO gnb_depth_list
    (brand_page_type, rtlr_name, cntry_cd, brand, category, brand_url, notes)
SELECT b.brand_page_type, b.rtlr_name, b.cntry_cd, b.brand,
       CASE b.sub_category
            WHEN '세탁기'             THEN 'WM'
            WHEN '건조기'             THEN 'DR'
            WHEN '세탁건조기(일체형)' THEN 'WD'
            WHEN '냉장고'             THEN 'REF'
            WHEN '냉동고'             THEN 'FZ'
            WHEN '냉장냉동고'         THEN 'FF'
       END,
       b.brand_url, b.notes
FROM brand_target_list b
WHERE b.brand_page_type = 'Brand Category Page'
ON DUPLICATE KEY UPDATE brand_url = VALUES(brand_url), notes = VALUES(notes);
