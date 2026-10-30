"""Compare the four final CSVs (v1, v2, 공유용, 공유용 v2) and validate their READ.md without changing CSVs."""

import ast
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'pdp 모수 추출' / '최종_20261029'
RENAMES = {
    'URL': '확인 요청 URL',
    '원본URL': '원본 상품 URL',
    '실제URL': '접속 후 URL',
    '판정': '모수 포함 여부',
    '페이지상태': '페이지 접속 확인 결과',
}
STATUSES = {'남김': '포함', '제외': '제외', '확인 필요': '검토 필요'}
DROPPED = {'OSM_RK', 'OSM_SOURCE_TYPE'}
WORDING = {
    'Codex 내부 브라우저': '브라우저',
    'Codex 화면': '수집한 상품 화면',
    'Codex에서 상품을 열지 못함': '브라우저에서 상품을 열지 못함',
    '부품 의심 단어(시트 밖, AI 추가)': '부품 의심 단어(공식 제외키워드 외 추가 검토)',
}


def indexed(rows):
    result = {row['행번호']: row for row in rows}
    assert len(result) == len(rows), 'Duplicate row IDs must not be overwritten'
    return result


def compare(before, after):
    old, new = indexed(before), indexed(after)
    changes = []
    for key, row in new.items():
        if key not in old:
            continue
        fields = {
            column: {'before': old[key].get(column), 'after': row.get(column)}
            for column in sorted(old[key].keys() | row.keys())
            if old[key].get(column) != row.get(column)
        }
        if fields:
            changes.append({'행번호': key, 'fields': fields})
    return {
        'removed': [row for key, row in old.items() if key not in new],
        'added': [row for key, row in new.items() if key not in old],
        'changes': changes,
    }


def shared_row(row, rewrite_wording=False):
    result = {}
    for column, value in row.items():
        if column in DROPPED:
            continue
        if column == '판정':
            value = STATUSES.get(value, value)
        if rewrite_wording and column in {'메모', '판매자근거'}:
            for source, replacement in WORDING.items():
                value = value.replace(source, replacement)
        result[RENAMES.get(column, column)] = value
    return result


NEW_COLUMNS = ['브랜드', '제품코드']
# D083: 저장 페이지 카테고리 재확인으로 남김 → 제외가 된 41행
D083_ROWS = set('''21370 21373 21374 21380 21382 21387 21422 27333 27462 27856 27861 27894 28049 29614
    55304 29612 29618 29626 55108 55112 55117 55119 55121 55763 55764 55765 55766 55772 55773 55777
    55794 55812 55318 55322 55329 55391 55401 55441 55663 55664 55913'''.split())


def share_v2_cells_equal(share, share_v2):
    return len(share) == len(share_v2) and all(
        all(a[c] == b.get(c) for c in a) for a, b in zip(share, share_v2))


def synthetic_checks():
    row = {'행번호': '1', '판정': '남김', 'URL': 'same', '메모': ''}
    assert compare([row], [dict(row)])['changes'] == []
    assert len(compare([row], [])['removed']) == 1
    assert len(compare([], [row])['added']) == 1
    changed = compare([row], [dict(row, 판정='제외')])['changes']
    assert changed[0]['fields'] == {'판정': {'before': '남김', 'after': '제외'}}
    assert '메모' in compare([row], [dict(row, 메모='0')])['changes'][0]['fields']
    try:
        compare([row, dict(row)], [row])
    except AssertionError:
        pass
    else:
        raise AssertionError('Duplicate IDs were silently ignored')
    source = dict(row, OSM_RK='1', OSM_SOURCE_TYPE='test',
                  메모='부품 의심 단어(시트 밖, AI 추가)', 판매자근거='Codex 화면')
    expected = {'행번호': '1', '모수 포함 여부': '포함', '확인 요청 URL': 'same',
                '메모': '부품 의심 단어(공식 제외키워드 외 추가 검토)',
                '판매자근거': '수집한 상품 화면'}
    assert shared_row(source, rewrite_wording=True) == expected
    base = {'행번호': '1', '제품군': 'WM', '상품명': 'x'}
    good = dict(base, 브랜드='LG', 제품코드='A1')
    assert share_v2_cells_equal([base], [good])
    assert not share_v2_cells_equal([base], [dict(good, 상품명='y')])
    assert not share_v2_cells_equal([base, dict(base, 행번호='2')], [dict(good, 행번호='2'), good])
    assert not share_v2_cells_equal([base], [])
    return 11


def main():
    synthetic_count = synthetic_checks()
    files = {}
    for path in BASE.glob('*.csv'):
        name = unicodedata.normalize('NFC', path.name)
        if name.startswith('PDP모수_공유용_v2_'):
            tag = 'share_v2'  # D082: 공유용에 브랜드·제품코드 열을 넣은 판
        else:
            tag = 'v1' if name.endswith('_v1.csv') else 'v2' if name.endswith('_v2.csv') else 'share'
        assert tag not in files, f'Unexpected additional CSV: {path}'
        files[tag] = path
    assert set(files) == {'v1', 'v2', 'share', 'share_v2'}
    rows, metadata = {}, {}
    expected = {
        'v1': (56071, 26, {'남김': 9763, '제외': 46072, '확인 필요': 236}),
        'v2': (55997, 26, {'남김': 9717, '제외': 46044, '확인 필요': 236}),
        'share': (55997, 24, {'포함': 9717, '제외': 46044, '검토 필요': 236}),
        'share_v2': (55997, 26, {'포함': 9717, '제외': 46044, '검토 필요': 236}),
    }
    for tag, path in files.items():
        with path.open(encoding='utf-8-sig', newline='') as stream:
            rows[tag] = list(csv.DictReader(stream))
        indexed(rows[tag])
        status_column = '모수 포함 여부' if tag.startswith('share') else '판정'
        counts = dict(Counter(row[status_column] for row in rows[tag]))
        assert (len(rows[tag]), len(rows[tag][0]), counts) == expected[tag]
        metadata[tag] = {'file': str(path.relative_to(ROOT)), 'rows': len(rows[tag]),
                         'columns': len(rows[tag][0]), 'counts': counts,
                         'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

    v1, v2, share = rows['v1'], rows['v2'], rows['share']
    assert list(v1[0]) == list(v2[0])
    result = compare(v1, v2)
    assert not result['added'] and len(result['removed']) == 74
    assert {r['행번호'] for r in result['removed']} == {str(n) for n in range(55998, 56072)}
    assert all(r['판정'] == '제외' and r['흐름'] == '#58' for r in result['removed'])
    assert Counter(r['리테일러'] for r in result['removed']) == {'BOULANGER': 49, 'DARTY': 25}
    assert len(result['changes']) == 155
    v2_index = indexed(v2)
    categories = Counter()
    for change in result['changes']:
        row = v2_index[change['행번호']]
        fields = change['fields']
        if change['행번호'] in D083_ROWS:
            assert set(fields) == {'판정', '제외단계', '제외사유', '메모'}
            assert fields['판정'] == {'before': '남김', 'after': '제외'} and '(D083)' in row['메모']
            categories['category_recheck'] += 1
        elif '판정' in fields:
            assert row['리테일러'] == 'DARTY'
            assert fields['판정'] == {'before': '남김', 'after': '제외'}
            categories['darty_judgement'] += 1
        elif '판매자' in fields:
            assert row['국가'] == 'Thailand' and row['리테일러'] == 'LAZADA'
            assert fields['판매자'] == {'before': 'Samsung', 'after': 'LG'}
            assert set(fields) == {'판매자', '판매자근거', '제외사유'} and row['판정'] == '제외'
            categories['lazada_seller'] += 1
        else:
            assert set(fields) == {'제외사유'} and row['판정'] == '제외'
            categories['duplicate_reason'] += 1
    assert categories == {'darty_judgement': 5, 'lazada_seller': 30, 'duplicate_reason': 79, 'category_recheck': 41}
    duplicate_retailers = Counter(v2_index[r['행번호']]['리테일러']
                                 for r in result['changes'] if set(r['fields']) == {'제외사유'})
    assert duplicate_retailers == {'COSTCO': 43, 'FALABELLA': 19, 'ALZA': 17}
    assert {r['행번호'] for r in result['changes'] if '판정' in r['fields']} == {'337', '508', '519', '915', '968'} | D083_ROWS
    u1 = {r['URL'] for r in v1 if r['판정'] == '남김'}
    u2 = {r['URL'] for r in v2 if r['판정'] == '남김'}
    assert len(u1 - u2) == 46 and not u2 - u1 and len(u1 & u2) == 9717

    assert [r['행번호'] for r in v2] == [r['행번호'] for r in share]
    assert list(shared_row(v2[0])) == list(share[0])
    share_diff = compare([shared_row(r) for r in v2], share)
    assert not share_diff['added'] and not share_diff['removed']
    assert len(share_diff['changes']) == 1655
    changed_columns = Counter(c for r in share_diff['changes'] for c in r['fields'])
    assert changed_columns == {'판매자근거': 1556, '메모': 107}
    assert all(shared_row(a, rewrite_wording=True) == b for a, b in zip(v2, share))

    # 공유용 → 공유용 v2: 제품군 뒤에 브랜드·제품코드만 들어가고 기존 24열은 모든 셀이 같아야 한다.
    share_v2 = rows['share_v2']
    share_columns = list(share[0])
    cut = share_columns.index('제품군') + 1
    assert list(share_v2[0]) == share_columns[:cut] + NEW_COLUMNS + share_columns[cut:]
    assert share_v2_cells_equal(share, share_v2)
    share_v2_lg = sum(r['브랜드'] == 'LG' and r['모수 포함 여부'] == '포함' for r in share_v2)

    doc_path = BASE / 'READ.md'
    doc = doc_path.read_text()
    for label, values in [('v1', expected['v1']), ('v2', expected['v2']), ('공유용', expected['share']),
                          ('공유용 v2', expected['share_v2'])]:
        count, width, counts = values
        included = counts.get('남김', counts.get('포함'))
        pending = counts.get('확인 필요', counts.get('검토 필요'))
        assert f'| {label} | {count:,} | {included:,} | {counts["제외"]:,} | {pending:,} | {width} |' in doc
    assert '1,655행의 1,663셀' in doc and sum(changed_columns.values()) == 1663
    assert '74개를 제거하고, 남은 행 중 155개' in doc
    for row_id in ['337', '508', '519', '915', '968']:
        row = v2_index[row_id]
        model = row['상품명'].replace('Lg ', 'LG ')
        assert f'| {row_id} | {model} | 남김 | 제외 |' in doc
    links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', doc)
    for link in links:
        target = (doc_path.parent / unquote(link.strip('<>'))).resolve()
        if target.name == 'verification.json' and target.parent == Path(__file__).resolve().parent:
            continue  # Written immediately below after all checks succeed.
        assert target.exists(), f'Broken documentation link: {link}'
    assert all(line == line.rstrip() for line in doc.splitlines())
    decisions = (ROOT / 'docs/DECISIONS.md').read_text()
    assert '**D081:**' in decisions and '**D082:**' in decisions and '**D083:**' in decisions
    assert all(f'{n}' in doc for n in ['21370', '29626', '55913'])
    assert f'포함인 행: {share_v2_lg:,}행' in doc
    ast.parse(Path(__file__).read_text())
    assert all(hashlib.sha256(files[tag].read_bytes()).hexdigest() == meta['sha256']
               for tag, meta in metadata.items()), 'A source CSV changed during verification'
    report = {'status': 'passed', 'files': metadata, 'synthetic_checks': synthetic_count,
              'v1_to_v2': result, 'change_categories': dict(categories),
              'v2_to_share_changed_rows': 1655, 'v2_to_share_changed_columns': dict(changed_columns),
              'v2_to_share_all_cells_equal_after_documented_replacements': True,
              'source_hashes_unchanged_during_verification': True,
              'share_to_share_v2_old_cells_equal': True, 'share_v2_lg_included_rows': share_v2_lg,
              'read_summary_and_darty_tables_checked': True, 'read_links_checked': len(links)}
    output = Path(__file__).with_name('verification.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    assert output.exists()
    print(json.dumps({k: report[k] for k in ['status', 'synthetic_checks', 'change_categories',
                                          'v2_to_share_changed_rows', 'read_links_checked']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
