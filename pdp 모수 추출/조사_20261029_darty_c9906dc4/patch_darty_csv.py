"""Apply artifact-authored rows while preserving every other CSV record byte for byte."""
import collections
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTPUT = HERE / '정정_1f5465cf'
FINAL = ROOT / 'pdp 모수 추출/최종_20261029'
TARGETS = {'337', '508', '519', '915', '968'}
ALLOWED = {'판정', '모수 포함 여부', '제외단계', '제외사유', '메모',
           '페이지상태', '페이지 접속 확인 결과', '실제URL', '접속 후 URL',
           '판매자', '판매자구분', '판매자근거'}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def records(raw):
    """Return original physical spans, including quoted multiline fields and BOM."""
    lines = raw.splitlines(keepends=True)
    reader = csv.reader(io.StringIO(raw.decode('utf-8-sig'), newline=''))
    previous = 0
    result = []
    for cells in reader:
        end = reader.line_num
        result.append((cells, b''.join(lines[previous:end])))
        previous = end
    assert previous == len(lines)
    return result


def splice(raw, replacements):
    parsed = records(raw)
    header = parsed[0][0]
    result = [parsed[0][1]]
    hits = set()
    for cells, original in parsed[1:]:
        row = dict(zip(header, cells, strict=True))
        rid = row['행번호']
        if rid not in replacements:
            result.append(original)
            continue
        assert rid not in hits
        replacement = replacements[rid]
        assert set(replacement) == set(row)
        changed = {k for k in row if row[k] != replacement[k]}
        assert changed <= ALLOWED, changed
        line_ending = '\r\n' if original.endswith(b'\r\n') else '\n'
        stream = io.StringIO(newline='')
        writer = csv.writer(stream, lineterminator=line_ending)
        writer.writerow([replacement[k] for k in header])
        result.append(stream.getvalue().encode('utf-8'))
        hits.add(rid)
    assert hits == set(replacements)
    return b''.join(result)


def fake_input_check():
    raw = '\ufeff행번호,판정,상품명,메모\r\n1,남김,"가짜, 상품","첫째\r\n둘째"\r\n2,제외,그대로,유지\r\n'.encode()
    old = records(raw)
    replacement = dict(zip(old[0][0], old[1][0], strict=True))
    replacement['판정'] = '제외'
    after = records(splice(raw, {'1': replacement}))
    assert after[0][1] == old[0][1] and after[2][1] == old[2][1]
    assert after[1][0][1] == '제외' and after[1][0][3] == '첫째\r\n둘째'


def prepare():
    OUTPUT.mkdir(exist_ok=True)
    report = json.loads((HERE / 'investigation.json').read_text())
    observations = {x['행번호']: x for x in report['8행_대조'] if x['행번호'] in TARGETS}
    files = []
    for path in sorted(FINAL.glob('*.csv')):
        raw = path.read_bytes()
        parsed = records(raw)
        header = parsed[0][0]
        rows = [dict(zip(header, x[0], strict=True)) for x in parsed[1:]]
        chosen = [r for r in rows if r['행번호'] in TARGETS]
        assert len(chosen) == 5
        source_url = '원본 상품 URL' if '원본 상품 URL' in header else '원본URL'
        assert all(r['리테일러'] == 'DARTY' and r[source_url] == observations[r['행번호']]['원본_URL'] for r in chosen)
        key = '모수 포함 여부' if '모수 포함 여부' in header else '판정'
        files.append({'path': str(path), 'name': path.name, 'sha256': digest(raw),
                      'row_count': len(rows), 'headers': header, 'rows': chosen,
                      'a_version': '_A판_' in path.name,
                      'before_counts': dict(collections.Counter(r[key] for r in rows))})
    assert len(files) == 4
    payload = {'files': files, 'observations': observations}
    (OUTPUT / 'inputs.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps([{'name': f['name'], 'rows_to_patch': len(f['rows']),
                       'before_counts': f['before_counts']} for f in files], ensure_ascii=False, indent=2))


def apply():
    source = json.loads((OUTPUT / 'inputs.json').read_text())
    authored = json.loads((OUTPUT / 'authored_rows.json').read_text())
    pending = []
    for spec, edit in zip(source['files'], authored['files'], strict=True):
        assert spec['path'] == edit['path']
        path = Path(spec['path'])
        before = path.read_bytes()
        assert digest(before) == spec['sha256'], f'Concurrent change: {path}'
        patches = {r['행번호']: r for r in edit['rows']}
        assert set(patches) == TARGETS
        after = splice(before, patches)
        pending.append((spec, path, before, after))
    # Prepare and validate all four files before any original is changed.
    for spec, path, before, after in pending:
        backup = OUTPUT / (path.name + '.before')
        assert not backup.exists(), f'Backup already exists: {backup}'
        backup.write_bytes(before)
    for spec, path, before, after in pending:
        assert digest(path.read_bytes()) == spec['sha256']
        path.write_bytes(after)
    verify()


def verify():
    source = json.loads((OUTPUT / 'inputs.json').read_text())
    result = []
    for spec in source['files']:
        path = Path(spec['path'])
        before = records((OUTPUT / (path.name + '.before')).read_bytes())
        after = records(path.read_bytes())
        assert len(before) == len(after) == spec['row_count'] + 1
        header = before[0][0]
        assert before[0] == after[0]
        key = '모수 포함 여부' if '모수 포함 여부' in header else '판정'
        changes = []
        counts = collections.Counter()
        for (old, old_raw), (new, new_raw) in zip(before[1:], after[1:], strict=True):
            a, b = dict(zip(header, old, strict=True)), dict(zip(header, new, strict=True))
            counts[b[key]] += 1
            if a['행번호'] not in TARGETS:
                assert old_raw == new_raw
                continue
            changed = {k: {'before': a[k], 'after': b[k]} for k in header if a[k] != b[k]}
            assert changed and set(changed) <= ALLOWED
            assert b[key] == '제외'
            if spec['a_version']:
                assert all(a[k] == b[k] for k in (key, '제외단계', '제외사유'))
            elif a['행번호'] == '519':
                assert b['제외단계'] == '④영구품절'
            else:
                assert b['제외단계'] == '③리리부' and b['판매자'] == 'Electro Store'
            changes.append({'행번호': a['행번호'], '상품명': a['상품명'], 'fields': changed})
        assert len(changes) == 5
        expected = dict(spec['before_counts'])
        if not spec['a_version']:
            expected['포함' if key == '모수 포함 여부' else '남김'] -= 5
            expected['제외'] += 5
        assert dict(counts) == expected
        result.append({'file': str(path), 'row_count': spec['row_count'], 'changed_rows': 5,
                       'before_counts': spec['before_counts'], 'after_counts': dict(counts),
                       'unrelated_records_byte_identical': True, 'changes': changes,
                       'after_sha256': digest(path.read_bytes())})
    bfile = next(Path(f['path']) for f in source['files'] if '_B판_' in f['name'])
    main = next(Path(f['path']) for f in source['files'] if f['name'].startswith('PDP모수_25개국'))
    assert bfile.read_bytes() == main.read_bytes()
    report = {'files': result, 'fake_multiline_input_check': 'passed',
              'b_and_main_byte_identical': True, 'row_deletion': 0}
    (OUTPUT / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps([{k: v for k, v in f.items() if k not in ('changes', 'after_sha256')} for f in result], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    fake_input_check()
    {'prepare': prepare, 'apply': apply, 'verify': verify}[sys.argv[1]]()
