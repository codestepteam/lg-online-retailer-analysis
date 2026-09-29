# S08 collected-pages (1)

원본: [collected-pages (1).csv](<../../관련문서/collected-pages (1).csv>)

이 파일은 기계 추출본이다. 원본의 문구는 사실 확정이나 실행 지시를 뜻하지 않는다.

데이터 행: 7107 · 열: 41

원본 CSV는 구조화 데이터로 유지한다. 아래는 스키마·빈값·분포 프로파일이며 전체 행을 Markdown으로 복제하지 않았다.

열 이름의 업무상 의미와 생성 로직은 코드/명세로 확인해야 한다. URL은 문자열만 점검했으며 외부 저장소를 열지 않았다.

| 열 | 빈 값 수 |
| --- | ---: |
| retailer | 0 |
| site_url | 0 |
| brand | 45 |
| product_name | 150 |
| page_type | 0 |
| best_env | 255 |
| best_quality | 255 |
| best_html_url | 255 |
| best_screenshot_url | 256 |
| best_captured_at_kst | 255 |
| best_outcome | 255 |
| better_reason | 0 |
| recollect | 6602 |
| compare | 0 |
| in_dev_clean_csv | 0 |
| dev_quality | 835 |
| stg_quality | 338 |
| dev_url_id | 835 |
| dev_snapshot_id | 835 |
| dev_captured_at_kst | 835 |
| dev_mode | 835 |
| dev_outcome | 835 |
| dev_block_reason | 6701 |
| dev_anomaly | 6542 |
| dev_attempts | 835 |
| dev_ok_attempts | 835 |
| dev_html_url | 835 |
| dev_screenshot_url | 1315 |
| dev_html_original_url | 835 |
| stg_url_id | 338 |
| stg_snapshot_id | 338 |
| stg_captured_at_kst | 338 |
| stg_mode | 338 |
| stg_outcome | 338 |
| stg_block_reason | 6943 |
| stg_anomaly | 6974 |
| stg_attempts | 338 |
| stg_ok_attempts | 338 |
| stg_html_url | 338 |
| stg_screenshot_url | 341 |
| stg_html_original_url | 338 |

## retailer

| 값 | 행 수 |
| --- | ---: |
| MediaWorld | 956 |
| Amazon | 892 |
| Alza | 729 |
| Media Expert | 701 |
| MediaMarkt | 616 |
| El Corte Inglés | 581 |
| Datart | 561 |
| Elgiganten | 542 |
| Boulanger | 401 |
| RTV EURO AGD | 387 |
| Unieuro | 341 |
| Darty | 205 |
| Coolblue | 195 |

## page_type

| 값 | 행 수 |
| --- | ---: |
| pdp | 7107 |

## best_env

| 값 | 행 수 |
| --- | ---: |
| stg | 6162 |
| dev | 690 |
| (빈 값) | 255 |

## best_outcome

| 값 | 행 수 |
| --- | ---: |
| captured | 6852 |
| (빈 값) | 255 |

## compare

| 값 | 행 수 |
| --- | ---: |
| both_captured | 5499 |
| stg_only_captured | 1092 |
| dev_only_captured | 367 |
| dev_missing | 72 |
| neither_captured | 63 |
| stg_missing | 14 |

## recollect

| 값 | 행 수 |
| --- | ---: |
| (빈 값) | 6602 |
| yes | 505 |

## in_dev_clean_csv

| 값 | 행 수 |
| --- | ---: |
| Y | 5721 |
| N | 1386 |

best_captured_at_kst 문자열 최솟값/최댓값: 2026-09-05 10:26:42 / 2026-09-15 20:08:27

site_url 완전 일치 기준 중복 추가 행: 0. 정규화/모델 단위 중복 여부는 별도 확인 필요.

