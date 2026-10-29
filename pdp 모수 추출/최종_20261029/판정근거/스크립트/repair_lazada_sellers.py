"""Lazada 상품별 화면 근거로 판매자 이름을 정정한다. 기본은 미리 보기이며 외부 호출은 없다."""
import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'pdp 모수 추출/최종_20261029'
NAMES = [
    'PDP모수_25개국_35개리테일러_전체판정_55997행_20261029.csv',
    'PDP모수_공유용_25개국_35개리테일러_전체판정_55997행_20261029.csv',
    'PDP모수_전체판정_B판_프랑스는OSM_v2.2목록_55997행_20261029.csv',
    'PDP모수_전체판정_A판_프랑스는두레이58_8월74개_56071행_20261029.csv',
    '판정근거/판매자판정/seller_lazada.csv',
]


def item_id(url):
    match = re.search(r'-i(\d+)(?=[-.?/]|$)', url.split('___')[0])
    return match[1] if match else ''


def confirmed(evidence):
    """판매자 번호 대신 국가+본 상품 ID로 연결하고, 화면 이름과 매장 링크를 함께 검사한다."""
    records = defaultdict(list)
    for r in evidence:
        if not r.get('ok'):
            continue
        host = {'Thailand': 'www.lazada.co.th', 'Singapore': 'www.lazada.sg'}[r['country']]
        if urlparse(r['actualUrl']).hostname != host or item_id(r['actualUrl']) != r['itemId']:
            raise ValueError('요청 상품과 다른 화면')
        primary = [d['primaryKey'] for d in r['identifiers'] if d.get('primaryKey')]
        if not any(p['itemId'] == r['itemId'] for p in primary):
            raise ValueError('본 상품 primaryKey 불일치')
        shop_links = [a['href'] for a in r['shopLinks'] if a['text'] == r['sellerName'] and a.get('href')]
        if not shop_links or not r.get('sellerHtml') or not r.get('sellerText'):
            raise ValueError('화면 판매자 이름 또는 매장 링크 누락')
        link = shop_links[0]
        shop = ('https:' + link if link.startswith('//') else link).split('?')[0]
        if urlparse(shop).hostname != host or not urlparse(shop).path.startswith('/shop/'):
            raise ValueError('본 국가의 매장 링크 아님')
        records[(r['country'], r['itemId'])].append({**r, 'shop': shop})
    result = {}
    for key, rs in records.items():
        if len({(r['sellerName'], r['shop']) for r in rs}) != 1:
            raise ValueError(f'같은 상품의 화면 근거 충돌: {key}')
        result[key] = rs[-1]
    return result


def change_for(row, facts):
    country = row.get('국가', '')
    url = row.get('요청URL', row.get('URL', row.get('확인 요청 URL', '')))
    fact = facts.get((country, item_id(url)))
    if not fact or row.get('리테일러') != 'LAZADA':
        return {}
    # 이번 확정 오류만 수정한다. 다른 판매자명 차이·상품 상태 변화는 자동 판정하지 않는다.
    if not (fact['sellerId'] == '100088963' and fact['subId'] == '1000007717'
            and fact['sellerName'] == 'LG' and '/shop/lg-official-store1/' in fact['shop']):
        return {}
    if row['판매자'] not in ('Samsung', 'LG'):
        raise ValueError('예상과 다른 기존 판매자')
    evidence_column = '근거' if '요청URL' in row else '판매자근거'
    changes = {'판매자': 'LG', evidence_column:
               f"상품별 확인(2026-10-29): 판매자 LG, {fact['shop']}; 상품ID {fact['itemId']}; sellerId 단독 연결 사용 안 함"}
    if '제외사유' in row:
        if row['판매자구분'] != '브랜드공식점' or row.get('판정', row.get('모수 포함 여부')) != '제외':
            raise ValueError('이름 외 판정 검토가 필요한 행')
        old = row['제외사유']
        if not old.endswith((' (Samsung)', ' (LG)')):
            raise ValueError('예상과 다른 제외 사유')
        changes['제외사유'] = re.sub(r' \((Samsung|LG)\)$', ' (LG)', old)
    return {k: v for k, v in changes.items() if row[k] != v}


def transform(raw, facts):
    """바뀌지 않은 CSV 레코드의 바이트를 그대로 보존한다. 행 제거·순서 변경 없음."""
    bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    text = raw[len(bom):].decode('utf-8')
    physical = text.splitlines(keepends=True)
    reader = csv.reader(io.StringIO(text, newline=''))
    header = next(reader)
    cursor = reader.line_num
    output = physical[:cursor]
    changes = []
    status = Counter()
    row_count = 0
    for logical_row, values in enumerate(reader, start=2):
        stop = reader.line_num
        original = ''.join(physical[cursor:stop])
        cursor = stop
        if len(values) != len(header):
            raise ValueError('CSV 열 수 불일치')
        row = dict(zip(header, values))
        updates = change_for(row, facts)
        status[row.get('판정', row.get('모수 포함 여부', '판매자 중간표'))] += 1
        row_count += 1
        if not updates:
            output.append(original)
            continue
        updated = {**row, **updates}
        buffer = io.StringIO(newline='')
        end = '\r\n' if original.endswith('\r\n') else '\n'
        writer = csv.writer(buffer, lineterminator=end)
        writer.writerow([updated[c] for c in header])
        output.append(buffer.getvalue())
        url = row.get('요청URL', row.get('URL', row.get('확인 요청 URL', '')))
        changes.append({'표행': logical_row, '행번호': row.get('행번호', ''), '국가': row['국가'],
                        '상품ID': item_id(url), 'URL': url,
                        'before': {k: row[k] for k in updates}, 'after': updates})
    return bom + ''.join(output).encode('utf-8'), changes, row_count, dict(status)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--report-dir', type=Path, required=True)
    parser.add_argument('--apply', action='store_true', help='미리 보기 내용을 실제 로컬 CSV 5개에 적용. 원본 백업 보존')
    args = parser.parse_args()
    evidence = [json.loads(l) for l in args.evidence.open()]
    facts = confirmed(evidence)
    args.report_dir.mkdir(parents=True, exist_ok=True)
    plan = []
    staged = []
    for name in NAMES:
        path = BASE / name
        raw = path.read_bytes()
        changed, edits, count, status = transform(raw, facts)
        # 독립 재파싱으로 허용된 셀 외 내용·순서·판정·행 수가 보존되는지 확인한다.
        before = list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
        after = list(csv.DictReader(io.StringIO(changed.decode('utf-8-sig'))))
        assert len(before) == len(after) == count
        assert [list(r) for r in before[:1]] == [list(r) for r in after[:1]]
        changed_indices = {e['표행'] - 2: e for e in edits}
        for index, (old, new) in enumerate(zip(before, after)):
            allowed = changed_indices.get(index, {}).get('after', {})
            assert {k: v for k, v in new.items() if v != old[k]} == allowed
        entry = {'file': str(path), 'rows': count, 'changed_rows': len(edits),
                 'changed_cells': sum(len(e['after']) for e in edits),
                 'before_sha256': hashlib.sha256(raw).hexdigest(),
                 'after_sha256': hashlib.sha256(changed).hexdigest(),
                 'status_before_and_after': status, 'edits': edits}
        plan.append(entry)
        staged.append((path, raw, changed))
    report = {'mode': 'apply' if args.apply else 'preview', 'verified_products': len(facts),
              'verified_affected_products': sum(r['priority'] == 0 and r['sellerName'] == 'LG' for r in facts.values()),
              'files': plan, 'original_xlsx_modified': False, 'network_calls': 0}
    (args.report_dir / 'correction_plan.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    with (args.report_dir / '판매자정정_파일별전후.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['파일', '엑셀에서 보이는 행', '원본 행번호', '국가', '상품ID', '항목', '수정 전', '수정 후'])
        for entry in plan:
            for edit in entry['edits']:
                for key in edit['after']:
                    writer.writerow([entry['file'], edit['표행'], edit['행번호'], edit['국가'], edit['상품ID'],
                                     key, edit['before'][key], edit['after'][key]])
    if args.apply:
        backup = args.report_dir / '원본백업'
        backup.mkdir(exist_ok=True)
        for path, raw, changed in staged:
            if raw == changed:
                continue
            if path.read_bytes() != raw:
                raise RuntimeError('미리 보기 이후 원본 파일이 변경됨: 적용 중단')
            old_path = backup / path.name
            if old_path.exists():
                assert old_path.read_bytes() == raw, '다른 백업이 이미 있음'
            else:
                old_path.write_bytes(raw)
            path.write_bytes(changed)
            assert path.read_bytes() == changed
    print(json.dumps({'mode': report['mode'], 'verified_products': len(facts),
                      'files': [{k: e[k] for k in ('file', 'rows', 'changed_rows', 'changed_cells')} for e in plan]},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
