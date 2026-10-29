"""LG 작업 폴더와 Downloads/Desktop의 Excel을 읽기 전용으로 검색한다."""
import csv
import hashlib
import io
import json
import os
import re
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
ROOTS = [Path('/Users/codestepseunghee/codestep') / name for name in
         ('lg-online-retailer-analysis', 'lg-pipeline', 'lge-hs-clinic-dashboard')]
ROOTS += [Path('/Users/codestepseunghee/Downloads'), Path('/Users/codestepseunghee/Desktop')]
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
JOBS = json.loads((OUT / 'page_jobs.json').read_text())
AFFECTED = {j['itemId'] for j in JOBS if j['priority'] == 0 and j['subId'] == '1000007717'}
PAT = re.compile(r'(?<!\d)(' + '|'.join(sorted(AFFECTED)) + r')(?!\d)')


def values(cell, strings):
    kind = cell.get('t')
    if kind == 's':
        return strings[int(cell.find('s:v', NS).text)]
    if kind == 'inlineStr':
        return ''.join(cell.itertext())
    return ''.join(cell.itertext())


def scan(path):
    raw = path.read_bytes()
    result = {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(),
              'size': len(raw), 'affected_item_ids': [], 'matching_rows': [],
              'output_filename_references': [], 'sheets': []}
    if path.suffix.lower() == '.xls':
        result['error'] = '옛 XLS 이진 형식: ZIP XML 검사 대상 아님'
        return result
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            for _, elem in ET.iterparse(archive.open('xl/sharedStrings.xml'), events=('end',)):
                if elem.tag == '{' + NS['s'] + '}si':
                    strings.append(''.join(elem.itertext()))
                    elem.clear()
        workbook = ET.fromstring(archive.read('xl/workbook.xml'))
        rels = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
        targets = {e.get('Id'): e.get('Target') for e in rels}
        for sheet in workbook.find('s:sheets', NS):
            target = targets[sheet.get('{' + NS['r'] + '}id')]
            member = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            result['sheets'].append(sheet.get('name'))
            headers = []
            for _, row in ET.iterparse(archive.open(member), events=('end',)):
                if row.tag != '{' + NS['s'] + '}row':
                    continue
                cells = {c.get('r'): values(c, strings) for c in row}
                for ref, text in cells.items():
                    if 'PDP모수_' in text or 'seller_lazada.csv' in text or '100088963' in text:
                        result['output_filename_references'].append(f"{sheet.get('name')}!{ref}: {text[:300]}")
                if int(row.get('r', '0')) <= 5:
                    headers.append(cells)
                matches = [(ref, text, PAT.findall(text)) for ref, text in cells.items() if PAT.search(text)]
                if matches:
                    result['matching_rows'].append({'sheet': sheet.get('name'), 'row': row.get('r'),
                                                    'matched_cells': matches, 'row_cells': cells,
                                                    'top_rows': headers})
                row.clear()
        result['affected_item_ids'] = sorted({item for row in result['matching_rows']
                                             for _, _, items in row['matched_cells'] for item in items})
        result['output_filename_references'].extend(s[:300] for s in strings if 'PDP모수_' in s or 'seller_lazada.csv' in s or '100088963' in s)
        for member in archive.namelist():
            if 'externalLink' in member and member.endswith(('.xml', '.rels')):
                data = archive.read(member).decode('utf-8')
                if 'PDP모수_' in data or 'seller_lazada' in data:
                    result['output_filename_references'].append(member)
    return result


def main():
    files = []
    for root in ROOTS:
        for parent, dirs, names in os.walk(root):
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '.venv', '__pycache__'}]
            files.extend(Path(parent) / n for n in names if Path(n).suffix.lower() in {'.xlsx', '.xlsm', '.xls'} and not n.startswith('~$'))
    results = []
    for path in sorted(set(files)):
        try:
            result = scan(path)
        except Exception as exc:
            result = {'path': str(path), 'error': str(exc)}
        results.append(result)
        print(json.dumps({'file': str(path), 'matching_rows': len(result.get('matching_rows', [])),
                          'error': result.get('error')}, ensure_ascii=False), flush=True)
    (OUT / 'workbook_inventory.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    with (OUT / '엑셀파일_영향점검.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['파일', '검사상태', '해당상품ID수', '해당행수', '이번CSV참조수', '판단'])
        for r in results:
            n = len(r.get('matching_rows', []))
            writer.writerow([r['path'], r.get('error', '검색완료'), len(r.get('affected_item_ids', [])), n,
                             len(r.get('output_filename_references', [])),
                             '내용 추가 확인' if n or r.get('output_filename_references') else '이번 판매자 이름 오류 연결 없음'])
    print('WORKBOOK_SCAN_COMPLETE', len(results))


if __name__ == '__main__':
    main()
