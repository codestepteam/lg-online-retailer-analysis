import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/parse_bcp_for_jev.py'
spec = importlib.util.spec_from_file_location('jev_parser', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def blocks(html, **kwargs):
    doc = m.Document()
    doc.feed(html)
    doc.finish()
    return m.block_records(doc, 'https://example.com/lg/', **kwargs)


class ParserTests(unittest.TestCase):
    def test_body_without_english_keywords_and_nested_header(self):
        out = blocks('<header>GLOBAL</header><main><section><header>DoorCooling</header>'
                     '<p>Koude lucht houdt je eten langer vers.</p><img alt="LG koelkast" src="a.jpg">'
                     '</section></main><footer>LEGAL</footer><script>SECRET</script>')
        text = ' '.join(b['text'] for b in out)
        self.assertIn('DoorCooling Koude lucht', text)
        for word in ('GLOBAL', 'LEGAL', 'SECRET'):
            self.assertNotIn(word, text)
        self.assertEqual(out[0]['images'][0]['alt_raw'], 'LG koelkast')

    def test_missing_empty_alt_and_no_surrounding_substitution(self):
        out = blocks('<section><p>LG fridge</p><img src="a"><img alt="" src="b"></section>')
        a, b = out[0]['images']
        self.assertFalse(a['alt_present'])
        self.assertIsNone(a['alt_raw'])
        self.assertTrue(b['alt_present'])
        self.assertEqual(b['alt_raw'], '')

    def test_hidden_descendant_is_separated(self):
        out = blocks('<section><p>Visible</p><div hidden>Hidden answer</div></section>')
        self.assertEqual([(b['text'], b['hidden_hint']) for b in out], [('Visible', False), ('Hidden answer', True)])
        self.assertTrue(all(b['rendered_visibility'] == 'not_measured' for b in out))

    def test_heading_order_on_minified_html(self):
        out = blocks('<main><h2>FIRST</h2><p>first body</p><h2>SECOND</h2><p>second body</p></main>')
        self.assertEqual(out[1]['preceding_heading_hint'], 'FIRST')
        self.assertEqual(out[3]['preceding_heading_hint'], 'SECOND')

    def test_large_text_is_preserved_and_links_not_verified(self):
        text = '가나다라마' * 2000
        out = blocks('<section><p>' + text + '</p><a href="../product">상품</a></section>')
        actual = ''.join(b['text'] for b in out if b['direct_text_only'])
        self.assertEqual(actual, text)
        link = [l for b in out for l in b['links']][0]
        self.assertEqual(link['url'], 'https://example.com/product')
        self.assertFalse(link['destination_verified'])

    def fixture(self, root, failed=False):
        page = root / 'batch/pages/shop/brand-category'
        page.mkdir(parents=True)
        (page / 'raw.html').write_text('<main><section><h2>Why LG?</h2><p>LG cools food evenly.</p></section>'
                                     '<div hidden>Secret FAQ</div></main>')
        response = {'ok': not failed, 'requested_url': 'https://example.com/lg',
                    'final_url': 'https://example.com/lg?page=2', 'captured_at': '2026-09-28'}
        state = {'ready': True, 'pageType': 'brand-category', 'images': [], 'cookieRemaining': [],
                 'initialMetadata': {'url': response['requested_url'], 'robots': ['index, follow']},
                 'metadata': {'robots': ['noindex']}}
        for name, value in [('capture-state.json', state), ('response.json', response)]:
            (page / name).write_text(json.dumps(value))
        return page

    def test_initial_metadata_and_drafts_never_assessed(self):
        with tempfile.TemporaryDirectory() as td:
            page = self.fixture(Path(td))
            data, jobs = m.parse_page(page, 'LG', 'refrigerators')
        self.assertEqual(data['metadata']['selected']['robots'], ['index, follow'])
        self.assertEqual(data['metadata']['final_snapshot']['robots'], ['noindex'])
        self.assertTrue(data['metadata']['requested_url_verified'])
        self.assertEqual(len(jobs), 1)
        self.assertEqual(set(jobs[0]['payload']['questions']), {'ID19', 'ID20', 'ID23'})
        self.assertIn('one named model', jobs[0]['payload']['questions']['ID19']['criteria']['does_not_match'])
        self.assertIn('Retailer delivery', jobs[0]['payload']['questions']['ID20']['criteria']['does_not_match'])
        self.assertEqual(jobs[0]['status'], 'draft_not_sent')
        self.assertTrue(all(a['value'] is None for a in data['assessment'].values()))
        self.assertFalse(data['quality']['jev_called'])
        self.assertFalse(data['quality']['absence_verdict_allowed'])

    def test_failed_capture_creates_no_drafts(self):
        with tempfile.TemporaryDirectory() as td:
            page = self.fixture(Path(td), failed=True)
            data, jobs = m.parse_page(page)
        self.assertEqual(jobs, [])
        self.assertIn('capture_not_successful', data['quality']['capture_issues'])

    def test_metadata_drift_without_initial_is_unverified(self):
        self.assertFalse(m.metadata_for_request({'metadata': {}}, {'requested_url': 'a', 'final_url': 'b'})['requested_url_verified'])

    def test_output_is_separate_and_input_unchanged_across_runs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            page = self.fixture(root)
            before = {p: m.digest(p) for p in page.iterdir()}
            with patch.object(m, 'ROOT', root):
                first = m.run(root / 'batch', 'LG', 'refrigerators')
                second = m.run(root / 'batch', 'LG', 'refrigerators')
            self.assertNotEqual(first, second)
            self.assertTrue((first / 'shop/jev-evidence.json').exists())
            self.assertEqual(before, {p: m.digest(p) for p in page.iterdir()})
            self.assertFalse(json.loads((first / 'manifest.json').read_text())['api_called'])


if __name__ == '__main__':
    unittest.main()
