"""Validate the #140 documentation record and preserve previous CSV results."""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PREFIX = Path(__file__).with_name('5a17277a688b0062066f905c41974c7c')


def has_rule(text):
    normalized = re.sub(r'\s|[*`]', '', text)
    return 'LG브랜드링크가있어도외부판매자상품이면제외' in normalized


def main():
    assert has_rule('LG 브랜드 링크가 있어도 외부 판매자 상품이면 제외')
    assert not has_rule('LG 브랜드 링크가 있으면 외부판매자 상품도 포함')
    documents = ['docs/DECISIONS.md', 'docs/BUSINESS_RULES.md', 'docs/SOURCES.md',
                 'pdp 모수 추출/README.md', 'pdp 모수 추출/최종_20261029/READ.md']
    for filename in documents:
        text = (ROOT / filename).read_text()
        assert has_rule(text) and 'D089' in text, filename
    decisions = (ROOT / documents[0]).read_text()
    assert len(re.findall(r'\*\*D089\b', decisions)) == 1
    guide = (ROOT / documents[3]).read_text().split('### 이탈리아 MediaWorld')[1].split('### ')[0]
    assert "왼쪽 위 'LG'가 클릭되는 링크면 LG 직판이다" not in guide
    note = PREFIX.with_suffix('.md')
    assert note.is_file()
    source = json.loads(Path(str(PREFIX) + '-source.json').read_text())
    assert source['taskNumber'] == 'LGE-HS-온라인-리테일-마케팅/140'
    assert source['commentId'] == '4456840619520127592'
    assert source['createdAt'] == '2026-11-02T15:26:44+09:00'
    assert has_rule(source['body']) and '[EY 하민주]' in source['body']
    hashes = json.loads((ROOT / 'outputs/mediaworld-all84-clicks-20261102-5850b120/original-hashes.json').read_text())
    assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
               for path, digest in hashes.items())
    checked = list(csv.DictReader((ROOT / 'outputs/mediaworld-all84-clicks-20261102-5850b120/84개_실제클릭_검증.csv').open(encoding='utf-8-sig')))
    v3 = next((ROOT / 'pdp 모수 추출/최종_20261029').glob('*v3*csv'))
    by_row = {r['행번호']: r for r in csv.DictReader(v3.open(encoding='utf-8-sig'))}
    assert len(checked) == 84
    assert all(by_row[r['행번호']]['모수 포함 여부'] == '제외' for r in checked)
    report = {'documents_checked': documents, 'synthetic_inputs': 2,
              'source_comment_verified': source['commentId'],
              'original_csv_unchanged': len(hashes), 'v3_existing_excluded_rows_preserved': 84}
    Path(str(PREFIX) + '-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
