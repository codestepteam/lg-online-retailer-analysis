-- migrations/003_backfill_product_id.sql
-- pdp_target_list 에서 product_id 가 NULL 인 기존 행을 URL 패턴으로 채운다.
-- 실행: DB 클라이언트에서 직접 붙여넣거나
--       mysql -u clinic_user -p lg_clinic < migrations/003_backfill_product_id.sql

-- Elgiganten / nya.elgiganten: 경로 끝 숫자 세그먼트
UPDATE pdp_target_list
SET product_id = SUBSTRING_INDEX(SUBSTRING_INDEX(url, '/', -1), '?', 1)
WHERE product_id IS NULL
  AND retailer = 'Elgiganten';

-- Darty: 경로 끝 .html 파일명 (확장자 제거)
UPDATE pdp_target_list
SET product_id = TRIM(TRAILING '.html' FROM
                   SUBSTRING_INDEX(SUBSTRING_INDEX(url, '/', -1), '?', 1))
WHERE product_id IS NULL
  AND retailer = 'Darty_FR';

-- Boulanger: /ref/<숫자>
UPDATE pdp_target_list
SET product_id = SUBSTRING_INDEX(url, '/ref/', -1)
WHERE product_id IS NULL
  AND retailer = 'Boulanger';

-- RtvEuroAgd (euro.com.pl): 경로 끝 .bhtml 파일명 (확장자 제거)
UPDATE pdp_target_list
SET product_id = TRIM(TRAILING '.bhtml' FROM
                   SUBSTRING_INDEX(SUBSTRING_INDEX(url, '/', -1), '?', 1))
WHERE product_id IS NULL
  AND retailer = 'RtvEuroAgd_PL';

-- MediaExpert: 경로 끝 세그먼트 (확장자 없음)
UPDATE pdp_target_list
SET product_id = SUBSTRING_INDEX(SUBSTRING_INDEX(url, '/', -1), '?', 1)
WHERE product_id IS NULL
  AND retailer = 'MediaExpert_PL';

-- 결과 확인
SELECT retailer, COUNT(*) AS total,
       SUM(product_id IS NULL) AS still_null
FROM pdp_target_list
GROUP BY retailer
ORDER BY retailer;
