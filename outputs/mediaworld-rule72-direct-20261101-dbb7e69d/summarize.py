"""Summarize actual IAB DOM observations without changing any previous CSV."""
import collections
import csv
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
PRIOR = ROOT / 'outputs/mediaworld-lg-html-audit-20261101-77dee0f9'


def linked(observation):
    return bool(observation.get('title')) and any(
        b['text'] == 'LG' and b['visible'] and b['href'] == '/it/brand/lg'
        and b['pointerEvents'] != 'none' for b in observation.get('brandSpans', []))


def main():
    fake = {'title': '상품', 'brandSpans': [{'text': 'LG', 'visible': True, 'href': '/it/brand/lg', 'pointerEvents': 'auto'}]}
    assert linked(fake)
    assert not linked({'title': '상품', 'brandSpans': [{**fake['brandSpans'][0], 'href': ''}]})
    assert not linked({'title': '상품', 'brandSpans': [{**fake['brandSpans'][0], 'visible': False}]})
    assert not linked({'title': '상품', 'brandSpans': [{**fake['brandSpans'][0], 'text': 'LG ELECTRONICS'}]})
    source = list(csv.DictReader((PRIOR / 'HTML판단보류_141개.csv').open(encoding='utf-8-sig')))
    observations = [json.loads(line) for line in (OUT / 'live-evidence.jsonl').open()]
    by_row = collections.defaultdict(list)
    for observation in observations:
        by_row[observation['row']].append(observation)
    result = []
    for row in source:
        history = by_row[row['행번호']]
        positives = [o for o in history if linked(o)]
        evidence = positives[-1] if positives else history[-1] if history else None
        result.append({
            '행번호': row['행번호'], '제품코드': row['제품코드'], '원본URL': row['URL'],
            'v3판정': row['v3판정'], 'v3제외사유': row['v3제외사유'],
            '실제화면72번분류': 'LG' if positives else '미확인',
            '72번판매자조건': '충족' if positives else '미확인(로딩·요청제한 등)',
            'v3와차이': ('제외→LG대상(판매자 조건 충족)' if row['v3판정'] == '제외' else '포함 유지') if positives else '보류',
            '브랜드링크': 'https://www.mediaworld.it/it/brand/lg' if positives else '',
            '실제도착URL': evidence['url'] if evidence else '',
            '상품번호': '|'.join(evidence['articleNumbers']) if evidence else '',
            '확인시각UTC': evidence['checkedAt'] if evidence else '',
            '주의': '2026-11-01 실제 화면 기준. 수집 당시 클릭 동작을 소급 검증한 것은 아님.',
        })
    prior_hashes = json.loads((PRIOR / '검증.json').read_text())['original_csv_sha256']
    for path, expected in prior_hashes.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    assert len(result) == 141 and len({r['행번호'] for r in result}) == 141
    for filename, rows in [
        ('실제화면_141개_대조.csv', result),
        ('실제화면_v3제외와다른상품.csv', [r for r in result if r['v3와차이'].startswith('제외→')]),
        ('실제화면_미확인.csv', [r for r in result if r['v3와차이'] == '보류']),
    ]:
        with (OUT / filename).open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(result[0]))
            writer.writeheader(); writer.writerows(rows)
    summary = {'total': 141, 'opened_unique': len(by_row),
               'synthetic_checks': 4,
               'actual_link_verified': sum(r['72번판매자조건'] == '충족' for r in result),
               'comparison': dict(collections.Counter(r['v3와차이'] for r in result)),
               'old_csv_sha256_unchanged': True,
               'scope': '2026-11-01 live IAB DOM, five tabs; v3 unchanged; not historical click verification'}
    (OUT / '실제화면_검증.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
