"""Audit actual LG clicks and brand-page arrivals; never edit source results."""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
BRAND = 'https://www.mediaworld.it/it/brand/lg'


def confirmed(r):
    return (r.get('status') == 'success' and r.get('clicked') is True
            and r.get('product', {}).get('title')
            and r.get('destination', {}).get('url') == BRAND
            and 'LG' in r.get('destination', {}).get('headings', []))


def main():
    fake = {'status': 'success', 'clicked': True, 'product': {'title': '상품'},
            'destination': {'url': BRAND, 'headings': ['LG']}}
    assert confirmed(fake)
    assert not confirmed({**fake, 'clicked': False})
    assert not confirmed({**fake, 'destination': {'url': BRAND, 'headings': ['다른 페이지']}})
    assert not confirmed({**fake, 'destination': {'url': 'https://www.mediaworld.it/', 'headings': ['LG']}})
    targets = json.loads((OUT / 'targets.json').read_text())
    histories = defaultdict(list)
    if (OUT / 'click-results.jsonl').exists():
        for line in (OUT / 'click-results.jsonl').read_text().splitlines():
            r = json.loads(line)
            histories[r['row']].append(r)
    rows = []
    for item in targets:
        history = histories[item['row']]
        good = [r for r in history if confirmed(r)]
        evidence = good[-1] if good else history[-1] if history else {}
        for filename in ('beforeScreenshot', 'afterScreenshot'):
            if good:
                assert (OUT / evidence[filename]).is_file(), (item['row'], filename)
        rows.append({
            '행번호': item['row'], '제품코드': item['model'], '요청URL': item['url'],
            'v3판정': item['old'], 'v3제외사유': item['oldReason'],
            '이번확인': '직접 클릭·LG 브랜드 페이지 도착 확인' if good else '미확인',
            '실제클릭': 'Y' if evidence.get('clicked') else 'N',
            '클릭전상품URL': evidence.get('product', {}).get('url', ''),
            '클릭전상품명': evidence.get('product', {}).get('title', ''),
            '클릭후URL': evidence.get('destination', {}).get('url', ''),
            '클릭후제목': '|'.join(evidence.get('destination', {}).get('headings', [])),
            '클릭전이미지': evidence.get('beforeScreenshot', ''),
            '클릭후이미지': evidence.get('afterScreenshot', ''),
            '확인시각UTC': evidence.get('finishedAt', ''),
            '미확인사유': '' if good else evidence.get('error', '미방문'),
            '범위': '2026-11-02 현재 화면 클릭 검증; v3 포함·제외는 변경하지 않음',
        })
    hashes = json.loads((OUT / 'original-hashes.json').read_text())
    assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == value for path, value in hashes.items())
    assert len(rows) == 84 and len({r['행번호'] for r in rows}) == 84
    for filename, records in [('84개_실제클릭_검증.csv', rows),
                              ('미확인목록.csv', [r for r in rows if r['이번확인'] == '미확인'])]:
        with (OUT / filename).open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(records)
    summary = {'targets': 84, 'selfchecks': 4,
               'results': dict(Counter(r['이번확인'] for r in rows)),
               'original_csv_unchanged': True, 'original_csv_count': len(hashes)}
    (OUT / '검증요약.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
