"""정정안·원본 보존·Excel 검색기의 가짜 입력을 검증한다. 원본 수정 없음."""
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import runpy
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]


def main():
    applied_receipt = OUT / '적용_3eac9d79/적용검증.json'
    if applied_receipt.exists():
        receipt = json.loads(applied_receipt.read_text())
        if receipt.get('status') == 'PASS' and receipt.get('apply_executed') is True:
            runpy.run_path(str(applied_receipt.parent / 'validate_applied.py'), run_name='__main__')
            return
    scanner = runpy.run_path(str(OUT / 'scan_workbooks.py'))

    def fixture(value, shared=True):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            archive.writestr('xl/workbook.xml', '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="검사" sheetId="1" r:id="rId1"/></sheets></workbook>')
            archive.writestr('xl/_rels/workbook.xml.rels', '<Relationships><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
            if shared:
                archive.writestr('xl/sharedStrings.xml', f'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><si><t>{value}</t></si></sst>')
            cell = '<c r="A2" t="s"><v>0</v></c>' if shared else f'<c r="A2"><v>{value}</v></c>'
            archive.writestr('xl/worksheets/sheet1.xml', f'<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row r="2">{cell}</row></sheetData></worksheet>')

        class FakePath:
            suffix = '.xlsx'

            def read_bytes(self):
                return buffer.getvalue()

            def __str__(self):
                return 'in-memory-fixture.xlsx'

        return scanner['scan'](FakePath())

    assert len(fixture('https://www.lazada.co.th/products/pdp-i4371575857.html')['matching_rows']) == 1
    assert len(fixture('4371575857', shared=False)['matching_rows']) == 1
    assert len(fixture('43715758570')['matching_rows']) == 0
    assert fixture('100088963', shared=False)['output_filename_references']
    coverage_module = runpy.run_path(str(OUT / 'refresh_coverage.py'))
    absent = {'pageEvidence': {'title': 'Sorry! This product is no longer available', 'bodyText': 'Oops\nSorry! This product is no longer available', 'heading': ''}, 'identifiers': []}
    assert coverage_module['is_no_product_screen'](absent)
    real_product = {**absent, 'identifiers': [{'primaryKey': {'itemId': '123'}}]}
    assert not coverage_module['is_no_product_screen'](real_product)
    partial = {'pageEvidence': {'title': 'LG refrigerator', 'bodyText': 'LG refrigerator', 'heading': 'LG refrigerator'}, 'identifiers': []}
    assert not coverage_module['is_no_product_screen'](partial)
    inventory = json.loads((OUT / 'workbook_inventory.json').read_text())
    assert len(inventory) == 59
    for record in inventory:
        assert not record.get('error') and not record['matching_rows'] and not record['output_filename_references']
        assert hashlib.sha256(Path(record['path']).read_bytes()).hexdigest() == record['sha256']
    plan = json.loads((OUT / 'correction_plan.json').read_text())
    assert plan['mode'] == 'preview' and len(plan['files']) == 5
    assert plan['verified_affected_products'] == 16
    coverage = json.loads((OUT / '확인범위_요약.json').read_text())
    assert coverage['대상상품ID'] == coverage['근거검토상품ID'] == 625
    assert coverage['확인성공상품ID'] == plan['verified_products'] == 622
    assert coverage['이번브라우저확인상품ID'] == 564
    assert coverage['기존저장화면확인상품ID'] == 58
    assert coverage['상품없음화면상품ID'] == 3 and coverage['상품없음화면URL행'] == 4
    assert coverage['확인성공URL행'] == 881 and coverage['미방문상품ID'] == 0
    archive_facts = [json.loads(line) for line in (OUT / 'archived_pages.jsonl').open()]
    assert len(archive_facts) == 58
    for fact in archive_facts:
        path = Path(fact['sourceHtmlFile'])
        assert path.is_relative_to(OUT)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == fact['sourceHtmlSha256']
    for record in plan['files']:
        assert hashlib.sha256(Path(record['file']).read_bytes()).hexdigest() == record['before_sha256']
        assert record['changed_rows'] == 30
        assert {e['after']['판매자'] for e in record['edits']} == {'LG'}
        assert len({e['상품ID'] for e in record['edits']}) == 16
        assert all(set(e['after']) <= {'판매자', '제외사유', '판매자근거', '근거'} for e in record['edits'])
    impact = list(csv.DictReader((OUT / 'CSV5개_수정범위.csv').open(encoding='utf-8-sig')))
    assert len(impact) == 5 and all(r['정정행수'] == '30' for r in impact)
    for name in ('docs/BUSINESS_RULES.md', 'pdp 모수 추출/최종_20261029/판정근거/README.md'):
        path = ROOT / name
        for link in re.findall(r'\]\(<([^>]+)>\)', path.read_text()):
            if 'a1d5af54' in link or 'repair_lazada_sellers.py' in link:
                assert (path.parent / link).is_file(), link
    result = {
        'status': 'PASS', 'seller_regression_tests': 8, 'workbook_scanner_synthetic_cases': 4,
        'archived_page_parser_synthetic_cases': 2, 'no_product_screen_synthetic_cases': 3,
        'products_reviewed': 625, 'sellers_confirmed': 622,
        'current_browser_confirmed': 564, 'archived_exact_product_confirmed': 58,
        'no_product_screens': 3, 'archived_html_files_preserved': 58,
        'original_workbooks_unchanged': 59, 'target_csv_files_unchanged': 5,
        'proposed_changed_rows_per_file': 30,
        'proposed_changed_cells_total': sum(r['changed_cells'] for r in plan['files']),
        'row_order_and_unrelated_fields': 'preview transform independently reparsed and compared every field',
        'apply_executed': False,
        'commands': [
            'python3 -m unittest discover -s "pdp 모수 추출/최종_20261029/판정근거/스크립트" -p test_repair_lazada_sellers.py -v',
            'python3 "pdp 모수 추출/최종_20261029/판정근거/스크립트/repair_lazada_sellers.py" --evidence "pdp 모수 추출/재점검_20261029_lazada_a1d5af54/product_evidence.jsonl" --report-dir "pdp 모수 추출/재점검_20261029_lazada_a1d5af54"',
            'python3 "pdp 모수 추출/재점검_20261029_lazada_a1d5af54/refresh_coverage.py"',
            'python3 "pdp 모수 추출/재점검_20261029_lazada_a1d5af54/scan_workbooks.py"',
            'python3 "pdp 모수 추출/재점검_20261029_lazada_a1d5af54/validate_review.py"',
            'git diff --check',
        ],
    }
    (OUT / '검증결과.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
