-- 036: image_asset.first_batch/last_batch VARCHAR(20) → VARCHAR(32)
--
-- 배경(2026-07-31 실측): 검증·복구용 suffix 배치 id("20260731_pipelinecheck" 22자,
-- "20260731_recrawl_full" 21자)가 20자 컬럼을 넘어 캐시 저장이 전건
-- "(1406, Data too long for column 'first_batch')" 로 실패했다 — 코드가 경고 후
-- 무시하므로 파이프라인은 돌지만, 해당 배치 이미지 전부가 L2 캐시(배치 간
-- dedup·OCR 재사용)를 못 탄다. 날짜(8) + '_' + 접미 여유로 32자면 충분.
ALTER TABLE image_asset
  MODIFY COLUMN first_batch VARCHAR(32) NULL,
  MODIFY COLUMN last_batch  VARCHAR(32) NULL;
