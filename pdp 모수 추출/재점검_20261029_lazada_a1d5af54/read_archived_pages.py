"""기존 브라우저 저장본에서 그 상품 자체의 판매자 영역만 확인한다. 번호별 이름 전파 없음."""
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent


class SellerModule(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.finished = False
        self.parts, self.text, self.links = [], [], []
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.finished:
            return
        if not self.depth:
            if tag != 'div' or attrs.get('id') != 'module_seller_info':
                return
            self.depth = 1
        elif tag == 'div':
            self.depth += 1
        self.parts.append(self.get_starttag_text())
        if tag == 'a':
            self.anchor = {'text': '', 'href': attrs.get('href'), 'className': attrs.get('class', '')}

    def handle_endtag(self, tag):
        if not self.depth or self.finished:
            return
        self.parts.append(f'</{tag}>')
        if tag == 'a' and self.anchor is not None:
            self.anchor['text'] = self.anchor['text'].strip()
            self.links.append(self.anchor)
            self.anchor = None
        if tag == 'div':
            self.depth -= 1
            self.text.append('\n')
            if self.depth == 0:
                self.finished = True

    def handle_data(self, data):
        if not self.depth or self.finished:
            return
        self.parts.append(html.escape(data, quote=False))
        self.text.append(data)
        if self.anchor is not None:
            self.anchor['text'] += data

    def name(self):
        matches = [a['text'] for a in self.links if 'seller-name-v2__detail-name' in a['className'].split()]
        return matches[0] if len(matches) == 1 else ''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='기존 zyte_full 폴더')
    args = parser.parse_args()
    # 다른 영역의 이름·뒤쪽 추천 영역을 판매자 영역으로 잘못 읽지 않는 가짜 입력.
    fake = SellerModule()
    fake.feed('<div>Samsung</div><div id="module_seller_info"><div><a class="seller-name-v2__detail-name" href="//example/shop/lg/">LG</a></div></div><div>Other</div>')
    assert fake.name() == 'LG' and 'Samsung' not in ''.join(fake.text) and 'Other' not in ''.join(fake.text)
    empty = SellerModule()
    empty.feed('<div>판매자 영역 없음</div>')
    assert not empty.name()
    jobs = {(r['country'], r['itemId']): r for r in json.loads((OUT / 'page_jobs.json').read_text())}
    live = {(r['country'], r['itemId']) for r in map(json.loads, (OUT / 'live_pages.jsonl').open()) if r['ok']}
    facts, failures = [], []
    source_records = args.source / 'results_codex_lazada_sellers.jsonl'
    saved_dir = OUT / 'archived_html'
    saved_dir.mkdir(exist_ok=True)
    for record in map(json.loads, source_records.open()):
        if not record.get('ok'):
            continue
        item = re.search(r'-i(\d+)', record['실제URL'])[1]
        key = record['국가'], item
        if key in live or key not in jobs:
            continue
        source_html = args.source / 'html_codex_lazada' / record['HTML파일']
        raw = source_html.read_bytes()
        text = gzip.decompress(raw).decode('utf-8')
        module = SellerModule()
        module.feed(text)
        primary = re.search(r'"primaryKey":(\{.*?\}),"requestHost"', text)
        identity = json.loads(primary[1]) if primary else None
        if not identity or identity['itemId'] != item or module.name() != record['판매자이름']:
            failures.append({'country': key[0], 'itemId': item, 'sourceHtml': str(source_html),
                             'reason': '본 상품 ID 또는 화면 이름 대조 불일치'})
            continue
        saved_html = saved_dir / f'{key[0]}-{item}.html.gz'
        if saved_html.exists():
            assert saved_html.read_bytes() == raw, '다른 저장본이 이미 있어 덮어쓰지 않는다'
        else:
            saved_html.write_bytes(raw)
        facts.append({**jobs[key], 'checkedAt': datetime.now(timezone.utc).isoformat(),
                      'method': 'saved-html-product-seller-module', 'actualUrl': record['실제URL'],
                      'title': record['제목'], 'sellerName': module.name(),
                      'sellerText': ''.join(module.text).strip(), 'sellerHtml': ''.join(module.parts),
                      'shopLinks': module.links,
                      'identifiers': [{'primaryKey': identity, 'subIds': re.findall(r'seller_sub_id=(\d+)', text)}],
                      'sourceRecordFile': str(source_records), 'sourceHtmlFile': str(saved_html.resolve()),
                      'originalSourceHtmlFile': str(source_html),
                      'sourceHtmlSha256': hashlib.sha256(raw).hexdigest(),
                      'captureTimestampNotRecorded': True, 'ok': True})
    (OUT / 'archived_pages.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in facts))
    (OUT / 'archived_pages_summary.json').write_text(json.dumps({'confirmed_exact_products': len(facts),
        'failures': failures, 'synthetic_cases': 2,
        'limit': '기존 브라우저 저장본을 확인한 결과다. 이번에 새로 페이지를 연 결과와 구분한다. 대표 페이지의 이름을 다른 상품에 전파하지 않는다.'}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'archived_exact_products': len(facts), 'failures': failures,
                      'names_different_from_existing': [r['itemId'] for r in facts if r['oldSeller'] != r['sellerName']]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
