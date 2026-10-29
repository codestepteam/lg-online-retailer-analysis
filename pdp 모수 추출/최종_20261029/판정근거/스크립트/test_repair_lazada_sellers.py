import copy
import csv
import io
import unittest

from repair_lazada_sellers import change_for, confirmed, item_id, transform


class RepairTest(unittest.TestCase):
    def setUp(self):
        self.fact = {'ok': True, 'country': 'Thailand', 'itemId': '4371575857',
                     'actualUrl': 'https://www.lazada.co.th/products/pdp-i4371575857.html',
                     'sellerName': 'LG', 'sellerId': '100088963', 'subId': '1000007717',
                     'sellerText': 'LG\nคะแนนร้านค้า 98%', 'sellerHtml': '<a>LG</a>',
                     'shopLinks': [{'text': 'LG', 'href': '//www.lazada.co.th/shop/lg-official-store1/?itemId=4371575857'}],
                     'identifiers': [{'primaryKey': {'itemId': '4371575857'}}]}
        self.facts = confirmed([self.fact])
        self.row = {'행번호': '3', '국가': 'Thailand', '리테일러': 'LAZADA',
                    'URL': self.fact['actualUrl'], '판매자': 'Samsung', '판매자구분': '브랜드공식점',
                    '판정': '제외', '제외사유': '브랜드 공식점(외부 판매자) (Samsung)', '판매자근거': '번호 연결',
                    '메모': '원문 보존, 두 줄\n둘째 줄'}

    def raw(self, rows):
        buffer = io.StringIO(newline='')
        writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator='\r\n')
        writer.writeheader()
        writer.writerows(rows)
        return b'\xef\xbb\xbf' + buffer.getvalue().encode()

    def test_same_number_does_not_change_other_product(self):
        other = {**self.row, 'URL': 'https://www.lazada.co.th/products/pdp-i160586162.html'}
        self.assertEqual(change_for(other, self.facts), {})

    def test_country_is_part_of_key(self):
        self.assertEqual(change_for({**self.row, '국가': 'Singapore'}, self.facts), {})

    def test_failed_page_does_not_supply_a_name(self):
        self.assertEqual(confirmed([{**self.fact, 'ok': False}]), {})

    def test_conflicting_store_blocks_changes(self):
        conflict = copy.deepcopy(self.fact)
        conflict['sellerName'] = 'Other'
        conflict['shopLinks'] = [{'text': 'Other', 'href': '//www.lazada.co.th/shop/other/'}]
        with self.assertRaises(ValueError):
            confirmed([self.fact, conflict])

    def test_wrong_product_blocks_changes(self):
        bad = copy.deepcopy(self.fact)
        bad['identifiers'][0]['primaryKey']['itemId'] = '111'
        with self.assertRaises(ValueError):
            confirmed([bad])

    def test_preserves_status_order_and_multiline_records(self):
        other = {**self.row, '행번호': '4', 'URL': 'https://www.lazada.co.th/products/pdp-i160586162.html'}
        raw = self.raw([self.row, other])
        changed, edits, count, status = transform(raw, self.facts)
        rows = list(csv.DictReader(io.StringIO(changed.decode('utf-8-sig'))))
        self.assertEqual((count, status, len(edits)), (2, {'제외': 2}, 1))
        self.assertEqual(rows[0]['판매자'], 'LG')
        self.assertEqual(rows[0]['메모'], self.row['메모'])
        self.assertEqual(rows[1], other)
        original_record = self.raw([other]).decode('utf-8-sig').split('\r\n', 1)[1].encode()
        self.assertTrue(changed.endswith(original_record))
        self.assertTrue(changed.startswith(b'\xef\xbb\xbf'))

    def test_reapply_is_idempotent(self):
        once, _, _, _ = transform(self.raw([self.row]), self.facts)
        twice, edits, _, _ = transform(once, self.facts)
        self.assertEqual(twice, once)
        self.assertEqual(edits, [])

    def test_url_suffix_does_not_merge_other_items(self):
        self.assertEqual(item_id(self.row['URL'] + '___{compress->test}'), '4371575857')
        self.assertNotEqual(item_id(self.row['URL'].replace('4371575857', '43715758570')), '4371575857')


if __name__ == '__main__':
    unittest.main()
