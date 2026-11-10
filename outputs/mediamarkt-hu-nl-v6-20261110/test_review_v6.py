"""v6 작성 범위·원본 보존·미확인 시 생성 차단을 가짜 입력으로 검증한다."""
import copy
import unittest
import review_v6 as review


class ApplyV6(unittest.TestCase):
    def setUp(self):
        self.columns, real, _ = review.source_rows()
        self.source = []
        for number, country, retailer, status in [("1", "Hungary", "Mediamarkt", "포함"), ("2", "Netherlands", "MEDIAMARKT", "포함"), ("3", "Germany", "MEDIAMARKT", "포함"), ("4", "Hungary", "Mediamarkt", "제외")]:
            row = dict(real[0])
            row.update({"행번호": number, "국가": country, "리테일러": retailer, "모수 포함 여부": status})
            self.source.append(row)
        self.reviews = [{"row": "1", "status": "제외", "reason": "본 상품 제목 리퍼·중고 표현: felújított", "seller": "", "kind": "리퍼·중고", "final_url": "https://www.mediamarkt.hu/hu/product/_lg-1.html", "checked_at": "2026-11-10T00:00:00Z"},
                        {"row": "2", "status": "유지"}]

    def test_only_confirmed_exclusion_changes_and_source_is_not_mutated(self):
        before = copy.deepcopy(self.source)
        output = review.apply_results(self.columns, self.source, self.reviews)
        self.assertEqual(self.source, before)
        self.assertEqual(output[0]["모수 포함 여부"], "제외")
        self.assertEqual(output[0]["제외단계"], "③리리부")
        self.assertEqual(output[0]["상품명"], before[0]["상품명"])
        self.assertEqual(output[0]["기준일"], before[0]["기준일"])
        self.assertEqual(output[1:], before[1:])

    def test_unknown_blocks_v6(self):
        self.reviews[0]["status"] = "확인불가"
        with self.assertRaisesRegex(AssertionError, "unverified"):
            review.apply_results(self.columns, self.source, self.reviews)

    def test_missing_review_blocks_v6(self):
        with self.assertRaises(AssertionError):
            review.apply_results(self.columns, self.source, self.reviews[:1])

    def test_duplicate_review_blocks_v6(self):
        with self.assertRaises(AssertionError):
            review.apply_results(self.columns, self.source, [self.reviews[0], self.reviews[0]])

    def test_unrelated_country_cannot_be_changed(self):
        self.reviews.append(dict(self.reviews[0], row="3"))
        with self.assertRaises(AssertionError):
            review.apply_results(self.columns, self.source, self.reviews)


if __name__ == "__main__":
    unittest.main()
