"""Offline evidence audit only. Reads saved HTML and v3; writes new audit artifacts."""
import collections
import csv
import gzip
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = ROOT / 'pdp 모수 추출/최종_20261029'
HTML_ROOT = Path('/private/tmp/claude-501/-Users-codestepseunghee-codestep-lg-online-retailer-analysis/253f8734-8060-4ddc-8899-4a7f6bf91733/scratchpad/zyte_full')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Node:
    def __init__(self, tag, attrs=(), parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children = []

    def text(self):
        return ' '.join(''.join(c.text() if isinstance(c, Node) else c for c in self.children).split())

    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.walk()


class Tree(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def inspect(html, url):
    tree = Tree(html).root
    headers = [n for n in tree.walk() if n.attrs.get('data-test') == 'mms-select-details-header']
    h1s = [n.text() for n in tree.walk() if n.tag == 'h1']
    evidence = []
    for header in headers:
        articles = [n.text() for n in header.walk() if n.attrs.get('data-test') == 'pdp-article-number']
        # Exact leaf text in the product header, never global menu, recommendations or JSON.
        brands = [n for n in header.walk() if n.tag in {'span', 'a', 'div'}
                  and n.text() in {'LG', 'LG ELECTRONICS'}
                  and not any(isinstance(c, Node) and c.text() == n.text() for c in n.children)]
        for n in brands:
            chain, p = [], n
            while p is not None:
                chain.append(p)
                if p is header:
                    break
                p = p.parent
            links = [{'href': urljoin(url, p.attrs['href']), 'tag': p.tag}
                     for p in chain if p.tag == 'a' and p.attrs.get('href')
                     and urlparse(urljoin(url, p.attrs['href'])).scheme in {'https', 'http'}
                     and not p.attrs['href'].startswith('#')
                     and p.attrs.get('aria-disabled') != 'true' and 'disabled' not in p.attrs]
            evidence.append({'text': n.text(), 'tag': n.tag, 'ancestor_tags': [p.tag for p in chain],
                             'links': links, 'article_numbers': articles,
                             'header_text': header.text()[:350]})
    labels = {e['text'] for e in evidence}
    if not h1s or not evidence or len(labels) != 1:
        result, reason = 'HTML만으로 판단 불가', '상품 상단 브랜드 영역 누락 또는 표기 충돌'
    elif labels == {'LG ELECTRONICS'}:
        result, reason = 'Marketplace', '상품 상단에 LG가 아닌 LG ELECTRONICS 명시(#72)'
    elif all(e['links'] for e in evidence):
        result, reason = 'LG(HTML 링크 확인)', '상품 상단 LG 표기에 HTTP(S) 링크 있음; 실제 클릭 동작은 미검증'
    else:
        result, reason = 'HTML만으로 판단 불가', 'LG 표기는 있으나 HTML 상위 요소에 링크 없음; 자바스크립트 연결 여부 미검증'
    return result, reason, evidence, h1s


def selfcheck():
    def sample(markup):
        return '<div data-test="mms-select-details-header">' + markup + '<h1>상품</h1></div>'
    assert inspect(sample('<a href="/it/brand/lg"><span>LG</span></a>'), 'https://www.mediaworld.it')[0] == 'LG(HTML 링크 확인)'
    assert inspect(sample('<span>LG ELECTRONICS</span>'), 'https://www.mediaworld.it')[0] == 'Marketplace'
    assert inspect(sample('<span>LG</span>'), 'https://www.mediaworld.it')[0] == 'HTML만으로 판단 불가'
    assert inspect('<nav><a href="/it/brand/lg">LG</a></nav><h1>商品</h1>', 'https://www.mediaworld.it')[0] == 'HTML만으로 판단 불가'
    assert inspect(sample('<span>LG</span><span>LG ELECTRONICS</span>'), 'https://www.mediaworld.it')[0] == 'HTML만으로 판단 불가'
    assert inspect(sample('<a href="#" onclick="go()">LG</a>'), 'https://www.mediaworld.it')[0] == 'HTML만으로 판단 불가'


def main():
    selfcheck()
    original_files = sorted(BASE.glob('*.csv'))
    hashes_before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in original_files}
    v3 = next(BASE.glob('*v3*csv'))
    rows = [r for r in csv.DictReader(v3.open(encoding='utf-8-sig')) if r['리테일러'] == 'MEDIAWORLD' and r['브랜드'] == 'LG']
    by = {r['요청URL']: r for r in map(json.loads, (BASE / '판정근거/페이지확인/pages_best.jsonl').open())}
    assert len(rows) == 148
    output, details = [], []
    for r in rows:
        d = by[r['확인 요청 URL']]
        path = HTML_ROOT / (d.get('_dir') or 'html') / d['HTML파일']
        raw = path.read_bytes()
        html = gzip.decompress(raw).decode('utf-8')
        result, reason, evidence, titles = inspect(html, d.get('실제URL') or r['확인 요청 URL'])
        # Separate string-level corroboration for this site's saved header structure.
        # Failure stops the audit rather than silently broadening the search to menus.
        assert len(titles) == 1 and len(evidence) == 2, r['행번호']
        labels = {e['text'] for e in evidence}
        assert len(labels) == 1, r['행번호']
        start = html.index('data-test="mms-select-details-header"')
        end = html.index('<h1', start)
        header_source = html[start:end]
        assert re.search(r'>\s*' + re.escape(next(iter(labels))) + r'\s*</span>', header_source), r['행번호']
        assert '<a ' not in header_source, r['행번호']
        expected = '제외' if result == 'Marketplace' else ('포함' if result == 'LG(HTML 링크 확인)' else '')
        # An LG link only resolves the #72 seller criterion, not other exclusion reasons.
        comparison = ('판단 보류' if not expected else
                      '제외 방향 일치' if expected == '제외' and r['모수 포함 여부'] == '제외' else
                      'v3 포함과 충돌' if expected == '제외' else
                      '포함 방향 일치' if r['모수 포함 여부'] == '포함' else 'v3 다른 제외사유 확인 필요')
        item = {'행번호': r['행번호'], '제품코드': r['제품코드'], 'URL': r['확인 요청 URL'],
                'v3판정': r['모수 포함 여부'], 'v3제외사유': r['제외사유'], 'v3판매자근거': r['판매자근거'],
                '상단브랜드표기': '|'.join(sorted({e['text'] for e in evidence})),
                '브랜드링크': '|'.join(sorted({a['href'] for e in evidence for a in e['links']})),
                '72번HTML대조': result, 'v3와비교': comparison, '판단근거와한계': reason,
                '저장HTML': str(path), '저장HTML_SHA256': hashlib.sha256(raw).hexdigest()}
        output.append(item)
        details.append({**item, 'header_evidence': evidence, 'product_titles': titles, 'capture_record': d})
    hashes_after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in original_files}
    assert hashes_before == hashes_after
    with (OUT / '전체148개_대조.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(output[0]))
        w.writeheader(); w.writerows(output)
    for name, subset in [
        ('HTML판단보류_141개.csv', [r for r in output if r['v3와비교'] == '판단 보류']),
        ('제외방향일치_7개.csv', [r for r in output if r['v3와비교'] == '제외 방향 일치']),
        ('확정충돌_0개.csv', [r for r in output if r['v3와비교'] == 'v3 포함과 충돌']),
    ]:
        with (OUT / name).open('w', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(output[0]))
            w.writeheader(); w.writerows(subset)
    (OUT / '상단영역_근거.json').write_text(json.dumps(details, ensure_ascii=False, indent=2))
    summary = {'total': len(rows), 'selfcheck_cases': 6, 'original_csv_unchanged': True,
               'independent_header_source_check': 148,
               'scope': 'Saved httpResponseBody HTML only; no JavaScript execution, live clicks, new collection, or v3 edits.',
               'brand_text_counts': dict(collections.Counter(r['상단브랜드표기'] for r in output)),
               'original_csv_sha256': hashes_before,
               'by_result_and_v3': dict(collections.Counter(f"{r['72번HTML대조']} / v3 {r['v3판정']}" for r in output)),
               'by_comparison': dict(collections.Counter(r['v3와비교'] for r in output))}
    (OUT / '검증.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
