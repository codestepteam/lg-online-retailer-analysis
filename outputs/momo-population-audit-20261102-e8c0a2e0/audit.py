"""Read-only CSV audit and offline SQL reproduction. No external requests."""
import csv
import hashlib
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RAW = ROOT / 'pdp 모수 추출/OSM_추가9개리테일러_PDP후보_4942건_20261028.csv'
SHARED = ROOT / 'pdp 모수 추출/최종_20261029/PDP모수_공유용_v3_EY검토반영_25개국_35개리테일러_전체판정_55997행_20261031.csv'
SQL = ROOT / 'pdp 모수 추출/osm_target_extract_global9.sql'
SAMPLES = [
    ('14085039', 1, 1, 'WT-IBN15M'),
    ('14085036', 1, 2, 'WT-IBN13W'),
    ('15755779', 1, 3, 'WR-100VW'),
    ('9917329', 1, 4, 'WD-S13VCW'),
    ('12737933', 1, 5, 'WT-VDN17M'),
    ('15755081', 1, 6, 'WT-TD15OB'),
    ('12305064', 1, 7, 'WD-S13VCW+WR-100VW'),
    ('13106229', 1, 8, 'WD-S15NW'),
    ('13106228', 1, 9, 'WR-20DW'),
    ('14702484', 1, 10, 'WT-TD18HG'),
    ('13321581', 2, 1, 'WD-S15NDB'),
    ('9917711', 2, 3, 'WD-S13VDW'),
]


def ids_from_url(url):
    parts = urlsplit(url)
    product = re.fullmatch(r'/product/(\d+)/?', parts.path)
    if product:
        return product.group(1)
    if parts.path.lower() == '/goods/goodsdetail.jsp':
        return parse_qs(parts.query).get('i_code', [None])[0]
    return None  # TP identifiers are intentionally not equated to regular product IDs.


def load(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def main():
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (RAW, SHARED, SQL)}
    raw = [r for r in load(RAW) if r['RTLR_NAME'] == 'MOMOSHOP']
    shared = [r for r in load(SHARED) if r['리테일러'] == 'MOMOSHOP']
    comparisons = []
    for pid, page, oid, model in SAMPLES:
        raw_hits = [r for r in raw if r['RPC'] == pid or any(
            ids_from_url(r[k]) == pid for k in ('RAW_URL', 'CRAWL_URL'))]
        shared_hits = [r['행번호'] for r in shared if any(
            ids_from_url(r[k]) == pid for k in ('확인 요청 URL', '원본 상품 URL', '접속 후 URL'))]
        comparisons.append(dict(product_id=pid, browser_page=page,
                                browser_organic_oid=oid, model=model,
                                extracted_osm_hits=len(raw_hits), shared_row_ids=shared_hits))

    # Reproduce the relevant BigQuery expressions in SQLite. Fixtures are artificial,
    # not evidence that these products existed in the original OSM source tables.
    db = sqlite3.connect(':memory:')
    db.create_function('REGEXP_REPLACE', 3, lambda s, pattern, repl: re.sub(pattern, repl, s))
    db.execute('CREATE TABLE fixture(CNTRY,RTLR_NAME,DIV,BRAND,RAW_URL)')
    fixture = [
        ('Taiwan', 'MOMOSHOP', 'W/M', 'LG', 'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=14085039'),
        ('Taiwan', 'MOMOSHOP', 'W/M', 'LG', 'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=14085036'),
        ('Taiwan', 'MOMOSHOP', 'W/M', 'LG', 'https://www.momoshop.com.tw/TP/TP0003952/goodsDetail/TP00039520005537'),
    ]
    db.executemany('INSERT INTO fixture VALUES (?,?,?,?,?)', fixture)
    query = r'''WITH base AS (
      SELECT *, REGEXP_REPLACE(RAW_URL, '[\?#].*$', '') AS CAT_URL_ADDR FROM fixture
    ), ranked AS (
      SELECT *, ROW_NUMBER() OVER (
        PARTITION BY UPPER(CNTRY), UPPER(RTLR_NAME), DIV, UPPER(BRAND), UPPER(CAT_URL_ADDR)
        ORDER BY RAW_URL ASC
      ) AS duplicate_rank FROM base
    ), deduped AS (SELECT * FROM ranked WHERE duplicate_rank=1), capped AS (
      SELECT *, ROW_NUMBER() OVER (
        PARTITION BY UPPER(CNTRY), DIV, UPPER(RTLR_NAME) ORDER BY RAW_URL
      ) AS cap_rank FROM deduped
    ) SELECT RAW_URL,CAT_URL_ADDR FROM capped WHERE cap_rank<=? ORDER BY RAW_URL'''
    repro = {str(cap): db.execute(query, (cap,)).fetchall() for cap in (1000, 2000)}
    db.close()
    assert len(fixture) == 3 and len(repro['1000']) == len(repro['2000']) == 2
    assert repro['1000'] == repro['2000']
    assert ids_from_url('https://www.momoshop.com.tw/product/14085039?Area=search') == '14085039'
    assert ids_from_url('https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=14085039&Area=search') == '14085039'
    assert len(comparisons) == 12 and all(r['extracted_osm_hits'] == 0 and not r['shared_row_ids'] for r in comparisons)
    assert len(raw) == len(shared) == 1250
    assert {r['흐름'] for r in shared} == {'OSM'}
    assert {r['기준일'] for r in shared} == {'2026-10-26'}
    counts = Counter((r['브랜드'], r['제품군'], r['모수 포함 여부']) for r in shared)
    assert sum(r['모수 포함 여부'] == '포함' for r in shared) == 10
    assert sum(r['브랜드'] == 'LG' and r['모수 포함 여부'] == '포함' for r in shared) == 3
    assert all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == digest for p, digest in hashes.items())
    report = dict(
        observed_date='2026-11-02 Asia/Seoul', sources_sha256=hashes,
        browser_source='User-provided LG 樂金 search URL, brand and category filters retained; pages 1 and 2 read with Codex in-app browser.',
        browser_scope='Search card links and model names verified. Individual PDP availability and seller status were not all verified. oid is the site organic counter, not the position including TP cards.',
        targets=comparisons, extracted_osm_rows=len(raw), shared_momo_rows=len(shared),
        shared_flow='OSM', osm_date='2026-10-26', included_total=10, included_lg=3,
        counts=[dict(brand=k[0],category=k[1],verdict=k[2],count=v) for k,v in counts.items()],
        included_rows=[r for r in shared if r['모수 포함 여부']=='포함'],
        raw_regular_rows=[r for r in raw if 'GoodsDetail.jsp' in r['RAW_URL']],
        sql_limit=dict(value=2000,scope='country / category / retailer, after duplicate removal'),
        fixture_input=fixture, fixture_query=query, fixture_output_by_cap=repro,
        reproduction_limit='SQLite reproduces the URL expression and partition. Source priority/date/rank are equal in the fixture. BigQuery source tables were not queried.',
        unverified=['Presence of the 12 IDs in original OSM tables before extraction',
                    'Historical or current generic Search Term rankings for all 12',
                    'Source file and operation used by the reported dashboard count of 3',
                    'Effect of a corrected query on the full OSM dataset'],
        validation='All read-only audit assertions passed; all three source hashes unchanged.'
    )
    (OUT / 'investigation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('extracted_osm_rows','shared_momo_rows','included_total','included_lg','validation')},ensure_ascii=False))
    print('12 target IDs absent from both CSVs; all 12 observed on supplied search pages 1–2.')
    print('Offline fixture: 3 distinct products -> 2 after deduplication, unchanged at caps 1000 and 2000.')


if __name__ == '__main__':
    main()
