-- Migration 016: home_keywords 유니크 키에 kywd_type 포함 (동일 키워드 home/category 공존)
--
-- 배경 (search_keywords_2.xlsx, 2026-07):
--   LG HS 팀 신규 키워드 파일은 `category` 컬럼이 채워진 행의 키워드가
--   home 트랙 검색(kywd_type='home')과 GNB 카테고리 매핑(kywd_type='category')
--   **양쪽에 모두** 속한다 (category ⊆ home). 기존 uq_keyword
--   (rtlr_name, cntry_cd, loc_srch_kywd_info) 는 한 키워드 1행만 허용해
--   이 이중 소속을 표현할 수 없음 → kywd_type 을 키에 포함.
--
-- 소비처 영향:
--   · repo.load_home_targets  — kywd_type 무관 전체 조인이라 이중 행이 검색 타깃을
--     중복 방출 → SELECT DISTINCT 로 방어 (같은 커밋에서 수정).
--   · make_report._load_home_keywords_lookup — 키워드당 1행 가정 dict → 타입 set 으로
--     변경, 이중 키워드는 ID1·ID2 양쪽에 기재하되 ID4(합집합)에는 1회만.
--   · repo.load_plp_targets('home') / load_home_gnb_targets('category') — 타입별
--     정확히 1행씩이라 영향 없음.
--
-- 실행: mysql -u <user> -p <db> < migrations/016_home_keywords_dual_type.sql

ALTER TABLE home_keywords
    DROP INDEX uq_keyword,
    ADD UNIQUE KEY uq_keyword (rtlr_name, cntry_cd, loc_srch_kywd_info, kywd_type);
