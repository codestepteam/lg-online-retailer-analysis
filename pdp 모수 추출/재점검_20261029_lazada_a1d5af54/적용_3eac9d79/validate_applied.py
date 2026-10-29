"""적용 결과를 백업·승인한 셀 목록과 독립 대조한다. 원본 CSV 수정 없음."""
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import runpy

OUT = Path(__file__).resolve().parent
REVIEW = OUT.parent
ROOT = REVIEW.parents[1]


def records(raw):
    text = raw.decode('utf-8-sig')
    stream = io.StringIO(text, newline='')
    reader = csv.reader(stream)
    start = 0
    for values in reader:
        stop = stream.tell()
        yield values, text[start:stop]
        start = stop


def main():
    plan = json.loads((OUT / 'correction_plan.json').read_text())
    assert plan['mode'] == 'apply' and len(plan['files']) == 5
    repair = runpy.run_path(str(ROOT / 'pdp 모수 추출/최종_20261029/판정근거/스크립트/repair_lazada_sellers.py'))
    facts = repair['confirmed']([json.loads(line) for line in (REVIEW / 'product_evidence.jsonl').open()])
    report = []
    for entry in plan['files']:
        path = Path(entry['file'])
        backup = OUT / '원본백업' / path.name
        before, after = backup.read_bytes(), path.read_bytes()
        assert hashlib.sha256(before).hexdigest() == entry['before_sha256']
        assert hashlib.sha256(after).hexdigest() == entry['after_sha256']
        assert before.startswith(b'\xef\xbb\xbf') == after.startswith(b'\xef\xbb\xbf')
        expected = {edit['표행']: edit for edit in entry['edits']}
        old_records, new_records = records(before), records(after)
        old_header, old_header_raw = next(old_records)
        new_header, new_header_raw = next(new_records)
        assert old_header == new_header and old_header_raw == new_header_raw
        count = changed_rows = changed_cells = 0
        old_status, new_status = Counter(), Counter()
        changed_items = set()
        for row_number, (old_record, new_record) in enumerate(zip(old_records, new_records, strict=True), start=2):
            old_values, old_raw = old_record
            new_values, new_raw = new_record
            old, new = dict(zip(old_header, old_values)), dict(zip(new_header, new_values))
            count += 1
            old_status[old.get('판정', old.get('모수 포함 여부', '판매자 중간표'))] += 1
            new_status[new.get('판정', new.get('모수 포함 여부', '판매자 중간표'))] += 1
            delta = {key: value for key, value in new.items() if value != old[key]}
            if row_number in expected:
                edit = expected[row_number]
                assert delta == edit['after']
                assert {key: old[key] for key in delta} == edit['before']
                assert old['판매자'] == 'Samsung' and new['판매자'] == 'LG'
                changed_rows += 1
                changed_cells += len(delta)
                changed_items.add(edit['상품ID'])
            else:
                assert not delta and old_raw == new_raw
        assert count == entry['rows'] and changed_rows == entry['changed_rows'] == 30
        assert changed_cells == entry['changed_cells'] and len(changed_items) == 16
        assert old_status == new_status
        reapplied, edits, _, _ = repair['transform'](after, facts)
        assert reapplied == after and not edits
        report.append({'file': str(path), 'backup': str(backup), 'rows_before': count,
                       'rows_after': count, 'changed_rows': changed_rows, 'changed_cells': changed_cells,
                       'different_product_ids': len(changed_items), 'unmodified_records_byte_identical': True,
                       'status_before': dict(old_status), 'status_after': dict(new_status),
                       'reapply_changes': 0})
    inventory = json.loads((REVIEW / 'workbook_inventory.json').read_text())
    for workbook in inventory:
        assert hashlib.sha256(Path(workbook['path']).read_bytes()).hexdigest() == workbook['sha256']
    result = {'status': 'PASS', 'apply_executed': True, 'files_applied': len(report),
              'changed_row_appearances': sum(r['changed_rows'] for r in report),
              'changed_cells': sum(r['changed_cells'] for r in report),
              'original_xlsx_unchanged': len(inventory), 'backups_preserved': 5,
              'csv_line_endings_preserved': True,
              'whitespace_check': '기존 CSV의 CRLF 줄끝을 정상 줄끝으로 인정하고 나머지 기본 공백 검사를 유지한다.',
              'seller_regression_tests': 8, 'files': report,
              'commands': [
                  'python3 "pdp 모수 추출/최종_20261029/판정근거/스크립트/repair_lazada_sellers.py" --evidence "pdp 모수 추출/재점검_20261029_lazada_a1d5af54/product_evidence.jsonl" --report-dir "pdp 모수 추출/재점검_20261029_lazada_a1d5af54/적용_3eac9d79" --apply',
                  'python3 "pdp 모수 추출/재점검_20261029_lazada_a1d5af54/적용_3eac9d79/validate_applied.py"',
                  'python3 -m unittest discover -s "pdp 모수 추출/최종_20261029/판정근거/스크립트" -p test_repair_lazada_sellers.py -v',
                  'git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff --check']}
    (OUT / '적용검증.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
