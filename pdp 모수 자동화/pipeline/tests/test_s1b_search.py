"""S1b: 기본 실행은 호출하지 않고, 키는 산출물에 남지 않으며, 카드 규칙·페이지 넘김·멈춤·이어받기가 맞는지 본다."""
import base64
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock
from urllib.parse import parse_qs, urlsplit

import common
import s1b_search as s1b

RUN = common.RunPaths("2026-11")
FAKE_KEY = "FAKE-KEY-FOR-TEST"


class Plan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = common.load_config(RUN, "search_urls")
        cls.planned = s1b.plan_requests(common.load_config(RUN, "search_terms")["terms"], cls.settings)
        cls.pricing = common.load_config(RUN, "zyte_pricing")

    def test_each_retailer_gets_three_ways_within_limit(self):
        self.assertEqual(len(self.planned), 36)
        self.assertEqual(len({item["key"] for item in self.planned}), 36)
        self.assertEqual(len({(item["country"], item["retailer"]) for item in self.planned}), 12)
        self.assertEqual({item["mode"] for item in self.planned}, {"H", "B0", "B1"})

    def test_every_request_names_a_country_and_one_way(self):
        for item in self.planned:
            self.assertRegex(item["payload"]["geolocation"], r"^[A-Z]{2}$")
            self.assertEqual(sum(field in item["payload"] for field in s1b.HTML_FIELDS), 1)

    def test_only_b1_has_actions(self):
        self.assertEqual({item["mode"] for item in self.planned if "actions" in item["payload"]}, {"B1"})

    def test_keyword_is_encoded_into_url(self):
        retailer = self.settings["retailers"]["Netherlands|MEDIAMARKT"]
        self.assertEqual(s1b.start_url(retailer, "Koel- vriescombinaties"), "https://www.mediamarkt.nl/nl/search.html?query=Koel-%20vriescombinaties&marketplace=MediaMarkt")

    def test_too_many_requests_stop(self):
        small = {**self.settings, "probe": {**self.settings["probe"], "max_requests": 35}}
        with self.assertRaises(common.ConfigError):
            s1b.plan_requests(common.load_config(RUN, "search_terms")["terms"], small)

    def test_estimate_uses_cheapest_and_dearest_tiers(self):
        http, browser, low, high = s1b.estimate(self.planned, self.pricing)
        self.assertEqual((http, browser), (12, 24))
        self.assertAlmostEqual(low, (12 * 0.13 + 24 * 1.01) / 1000)
        self.assertAlmostEqual(high, (12 * 1.27 + 24 * 16.08) / 1000)

    def test_preview_says_why_what_and_how_much(self):
        text = s1b.render_preview("2026-11", self.planned, self.settings, self.pricing)
        for expected in ("왜 부르나", "보내는 값", "규모·비용", "최소치", "--probe --run", "mediamarkt.nl"):
            self.assertIn(expected, text)


class RunMode(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.run_paths = common.RunPaths("2026-11", Path(folder.name)).create()
        for name in ("search_urls", "search_terms", "zyte_pricing"):
            shutil.copy(RUN.sub("config") / f"{name}.json", self.run_paths.sub("config") / f"{name}.json")
        for target, value in (("get_logger", mock.Mock()), ("RunPaths", self.run_paths), ("read_secret", FAKE_KEY)):
            patcher = mock.patch.object(s1b, target, return_value=value)
            setattr(self, target, patcher.start())
            self.addCleanup(patcher.stop)

    def main(self, *arguments, answer=None):
        answer = answer or (200, {"url": "https://x/final", "statusCode": 200, "browserHtml": "<html>ok</html>", "httpResponseBody": base64.b64encode(b"<html>ok</html>").decode()})
        with mock.patch.object(s1b, "zyte_post", return_value=answer) as post, mock.patch("builtins.print"):
            s1b.main(["--month", "2026-11", "--probe", *arguments])
        return post

    def report(self):
        return (self.run_paths.sub("logs") / s1b.REPORT_NAME).read_text(encoding="utf-8")

    def test_default_makes_no_call_and_reads_no_key(self):
        self.main().assert_not_called()
        self.read_secret.assert_not_called()
        self.assertIn("왜 부르나", self.report())

    def test_run_sends_each_request_once_and_saves_html(self):
        self.assertEqual(self.main("--run").call_count, 36)
        self.assertEqual(len(list((self.run_paths.sub("html") / s1b.HTML_FOLDER).glob("*.html"))), 36)
        self.assertIn("실험 결과", self.report())

    def test_rerun_does_not_pay_twice_even_after_failure(self):
        self.main("--run", answer=(520, {"title": "Website Ban"}))
        self.main("--run").assert_not_called()
        self.assertEqual(self.main("--run", "--force").call_count, 36)

    def test_failure_is_recorded_not_raised(self):
        self.main("--run", answer=(520, {"title": "Website Ban"}))
        report = self.report()
        self.assertIn("Website Ban", report)
        self.assertIn("아니오", report)

    def test_key_is_not_left_in_outputs(self):
        self.main("--run")
        for path in self.run_paths.directory.rglob("*"):
            if path.is_file() and path.suffix in (".md", ".jsonl", ".log"):
                self.assertNotIn(FAKE_KEY, path.read_text(encoding="utf-8"), path)


class Check(unittest.TestCase):
    settings = common.load_config(RUN, "search_urls")["probe"]

    def probe(self, html):
        item = {"key": "a", "country": "c", "retailer": "r", "mode": "H", "october_links": ["https://x/p/1", "https://x/p/2"], "payload": {}}
        with tempfile.TemporaryDirectory() as folder, mock.patch.object(s1b, "zyte_post", return_value=(200, {"browserHtml": html})):
            return s1b.probe_one(item, "k", self.settings, Path(folder))

    def test_small_captcha_page_is_blocked(self):
        self.assertTrue(self.probe("<html>Just a moment</html>")["blocked"])

    def test_big_page_with_word_is_not_blocked(self):
        self.assertFalse(self.probe("captcha" + "x" * self.settings["block_max_size"])["blocked"])

    def test_counts_october_links_found(self):
        self.assertEqual(self.probe('<a href="/p/1">a</a>')["links_seen"], 1)


SETTINGS = common.load_config(RUN, "search_urls")
TERMS = common.load_config(RUN, "search_terms")["terms"]
# 11-18 방식 실험(--probe)에서 받은 검색 1페이지 36개. 11월 연습 회차를 옮긴 폴더에 있다(2026-11-23). 카드 규칙 회귀 검사용.
HTML_FOLDER = common.RUNS_ROOT / "2026-11_연습" / "html" / s1b.HTML_FOLDER
LIMIT = SETTINGS["card_limit"]


def shop(key):
    return SETTINGS["retailers"][key]


def term(row=98, country="Netherlands", retailer="MEDIAMARKT", keyword="kw"):
    return {"excel_row": row, "country": country, "retailer": retailer, "category": "Refrigerator", "keyword": keyword, "english": "e"}


class Addresses(unittest.TestCase):
    def test_set_param_keeps_other_text(self):
        self.assertEqual(s1b.set_param("https://x/a?q=a%20b&page=4&z=1", "page", 2), "https://x/a?q=a%20b&z=1&page=2")
        self.assertEqual(s1b.set_param("https://x/a?page=4", "page", None), "https://x/a")
        self.assertEqual(s1b.set_param("https://x/a#f", "page", 2), "https://x/a?page=2#f")

    def test_mediamarkt_starts_from_arrival_without_page_and_keeps_filter(self):
        self.assertEqual(s1b.term_start(shop("Netherlands|MEDIAMARKT"), term(98)), "https://www.mediamarkt.nl/nl/category/amerikaanse-koelkasten-621.html?query=Amerikaanse%20koelkasten&marketplace=MediaMarkt")

    def test_appliance_online_keeps_explicit_first_page(self):
        url = s1b.term_start(shop("Australia|Appliance Online"), term(345, "Australia", "Appliance Online"))
        self.assertIn("/filter/washers-and-dryers/washing-machines/front-loading/", url)
        self.assertIn("currentpage=1", url)
        self.assertNotIn("currentpage=6", url)

    def test_new_row_without_october_arrival_uses_template(self):
        self.assertEqual(s1b.term_start(shop("Netherlands|MEDIAMARKT"), term(9999, keyword="a b")), "https://www.mediamarkt.nl/nl/search.html?query=a%20b&marketplace=MediaMarkt")

    def test_query_page_goes_on_arrival(self):
        self.assertEqual(s1b.page_url(shop("Portugal|Worten"), term(), 3, "https://s/start", "https://s/arrive?query=x"), "https://s/arrive?query=x&page=3")

    def test_alza_path_suffix(self):
        self.assertEqual(s1b.page_url(shop("Czech Republic|ALZA"), term(), 2, "s", "https://www.alza.cz/search.htm?exps=a+b"), "https://www.alza.cz/search-p2.htm?exps=a+b")

    def test_rtv_template_uses_keyword(self):
        self.assertEqual(s1b.page_url(shop("Poland|RTV_EURO_AGD"), term(keyword="lodówka"), 2, "s", "a"), "https://www.euro.com.pl/search2,strona-2.bhtml?keyword=lod%C3%B3wka")


class SharafDirect(unittest.TestCase):
    retailer = shop("UAE|Sharaf DG")

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name)
        self.log = common.ResumeLog(self.path / "pages.jsonl", "page_key")

    def assert_direct(self, url):
        query = parse_qs(urlsplit(url).query)
        self.assertEqual(query['dFR[promotion_offer_json.seller_code][0]'], ['sdg'])
        self.assertEqual(query['dFR[promotion_offer_json.seller_code][1]'], ['sdg_online_excl'])

    def selected_term(self):
        return next(t for t in TERMS if t['excel_row']==157)

    def test_all_nine_search_terms_and_probe_payloads_are_direct(self):
        terms = [t for t in TERMS if t['country']=='UAE' and t['retailer']=='Sharaf DG']
        self.assertEqual(len(terms),9)
        for item in terms:
            url = s1b.term_start(self.retailer,item)
            self.assert_direct(url)
            self.assertEqual(parse_qs(urlsplit(url).query)['q'],[item['keyword']])
        for planned in s1b.plan_requests(TERMS,SETTINGS):
            if planned['retailer']=='Sharaf DG':
                self.assert_direct(planned['payload']['url'])
                self.assertNotEqual(planned['key'], 'UAE_Sharaf_DG_'+planned['mode'])

    def test_next_page_repairs_missing_or_encoded_wrong_filter(self):
        start = s1b.term_start(self.retailer,self.selected_term())
        arrival = 'https://uae.sharafdg.com/?q=bottom%20freezer%20refrigerator&dFR%5Bpromotion_offer_json.seller_code%5D%5B0%5D=marketplace&post_type=product'
        url = s1b.page_url(self.retailer,self.selected_term(),2,start,arrival)
        self.assert_direct(url)
        self.assertEqual(parse_qs(urlsplit(url).query)['page_number'],['2'])

    def test_old_arrival_cannot_bypass_filter(self):
        retailer = {**self.retailer,'start_from_arrival':True}
        self.assert_direct(s1b.term_start(retailer,self.selected_term()))

    def test_collection_preserves_offer_promo_and_resumes_only_direct_records(self):
        product = 'https://uae.sharafdg.com/product/bosch-kiv87nse0m/?promo='
        self.log.append({'page_key':'157|1',**page_record([card(999)],has_next=False)})
        calls=[]
        def fetch(url,retailer,page):
            self.assert_direct(url)
            calls.append(url)
            return {**page_record([{'name':'Bosch refrigerator','link':product+str(page),'ad':'표시 없음'}],has_next=page==1,total=2),
                    'url':url,'final_url':url}
        first=s1b.collect_term(self.retailer,self.selected_term(),SETTINGS,fetch,self.log)
        self.assertEqual(len(calls),2)
        self.assertEqual([r['카드PDP링크'] for r in s1b.card_rows(first)],[product+'1',product+'2'])
        calls.clear()
        again=s1b.collect_term(self.retailer,self.selected_term(),SETTINGS,fetch,self.log)
        self.assertEqual(calls,[])
        self.assertEqual(first['cards'],again['cards'])

    def test_changed_filter_does_not_reuse_previous_filter_cache(self):
        url=s1b.term_start(self.retailer,self.selected_term())
        self.assertNotEqual(s1b.request_cache_key('157|1',self.retailer,url),
                            s1b.request_cache_key('157|1',self.retailer,url+'&q=changed'))

    def test_request_and_response_filter_and_parser_preserve_promo(self):
        url=s1b.term_start(self.retailer,self.selected_term())
        html='<main><h3>refrigerator(1)</h3><div id="hits"><div class="algolia-item"><h4 class="name">Bosch refrigerator</h4><a class="product-link" href="/product/bosch-kiv87nse0m/?promo=4037795">product</a></div></div></main>'
        post=mock.Mock(return_value=(200,{'url':url,'statusCode':200,'browserHtml':html}))
        record=s1b.fetch_page('https://uae.sharafdg.com/?q=refrigerator',self.retailer,1,SETTINGS,'fake',post)
        self.assertTrue(record['ok'])
        self.assert_direct(post.call_args.args[0]['url'])
        self.assertEqual(record['cards'][0]['link'],'https://uae.sharafdg.com/product/bosch-kiv87nse0m/?promo=4037795')

    def test_response_losing_direct_filter_is_failure_not_unfiltered_success(self):
        post=mock.Mock(return_value=(200,{'url':'https://uae.sharafdg.com/?q=refrigerator','statusCode':200,'browserHtml':'<main>result</main>'}))
        record=s1b.fetch_page('https://uae.sharafdg.com/?q=refrigerator',self.retailer,1,SETTINGS,'fake',post)
        self.assertFalse(record['ok'])
        self.assertIn('직판',record['problem'])
        self.assertEqual(record['cards'],[])
        self.assertEqual(post.call_count,SETTINGS['collection']['retries']+1)

    def test_unfiltered_finished_csv_is_not_reused_or_modified(self):
        path=self.path/'cards.csv'
        row={'국가':'UAE','리테일러':'Sharaf DG','최종검색결과URL':'https://uae.sharafdg.com/?q=refrigerator'}
        common.write_csv(path,list(row),[row])
        before=path.read_bytes()
        with self.assertRaises(common.ConfigError):
            s1b.validate_existing_cards(path,SETTINGS)
        self.assertEqual(path.read_bytes(),before)
        row['최종검색결과URL']=s1b.term_start(self.retailer,self.selected_term())
        common.write_csv(path,list(row),[row],overwrite=True)
        s1b.validate_existing_cards(path,SETTINGS)


@unittest.skipUnless(HTML_FOLDER.exists(), "실험 HTML이 없습니다")
class SavedPages(unittest.TestCase):
    """WP1-1에서 받아 둔 실제 화면에 카드 규칙을 적용한다. 호출 없음."""

    def parse(self, key, name):
        return s1b.parse_page((HTML_FOLDER / name).read_text(encoding="utf-8"), shop(key)["parser"], "https://example.test/", 1)

    def test_card_counts_and_every_card_complete(self):
        expected = {("Netherlands|MEDIAMARKT", "Netherlands_MEDIAMARKT_H.html"): 12, ("Hungary|Mediamarkt", "Hungary_Mediamarkt_H.html"): 12, ("Czech Republic|ALZA", "Czech_Republic_ALZA_B0.html"): 24, ("Poland|MEDIAEXPERT", "Poland_MEDIAEXPERT_H.html"): 30,
                    ("Poland|RTV_EURO_AGD", "Poland_RTV_EURO_AGD_B0.html"): 20, ("UAE|Sharaf DG", "UAE_Sharaf_DG_B0.html"): 48, ("Portugal|Worten", "Portugal_Worten_B0.html"): 48, ("Peru|FALABELLA", "Peru_FALABELLA_B0.html"): 48,
                    ("Egypt|Cairo Sales", "Egypt_Cairo_Sales_H.html"): 2, ("Morocco|Electroplanet", "Morocco_Electroplanet_B0.html"): 2}
        for (key, name), count in expected.items():
            with self.subTest(key):
                cards = self.parse(key, name)["cards"]
                self.assertEqual(len(cards), count)
                self.assertTrue(all(card["name"] and card["link"] for card in cards))

    def test_alza_ad_mark(self):
        self.assertEqual(sum(card["ad"] == "예" for card in self.parse("Czech Republic|ALZA", "Czech_Republic_ALZA_B0.html")["cards"]), 1)

    def test_falabella_says_not_an_ad(self):
        self.assertEqual({card["ad"] for card in self.parse("Peru|FALABELLA", "Peru_FALABELLA_B0.html")["cards"]}, {"아니오"})

    def test_total_and_next(self):
        page = self.parse("Poland|MEDIAEXPERT", "Poland_MEDIAEXPERT_H.html")
        self.assertEqual((page["total"], page["has_next"]), (1054, True))

    def test_open_ended_total_has_no_number(self):
        page = self.parse("Portugal|Worten", "Portugal_Worten_B0.html")
        self.assertEqual((page["total_display"], page["total"]), ("1000+", None))

    def test_last_page_has_no_next(self):
        self.assertFalse(self.parse("Egypt|Cairo Sales", "Egypt_Cairo_Sales_H.html")["has_next"])

    def test_landing_page_carousels_are_not_counted(self):
        """Appliance Online 분류 첫 화면의 추천 줄은 본 목록이 아니다."""
        self.assertEqual(self.parse("Australia|Appliance Online", "Australia_Appliance_Online_B1.html")["cards"], [])


def card(number):
    return {"name": f"n{number}", "link": f"https://x/p/{number}", "ad": "표시 없음"}


def page_record(cards, has_next=True, total=None, display="", zero=False):
    return {"ok": True, "url": "u", "final_url": "https://x/final", "attempts": 1, "problem": "", "collected_at": "2026-11-30T00:00:00Z", "cards": cards, "total_display": display or (str(total) if total is not None else ""), "total": total, "has_next": has_next, "zero": zero, "loading": 0}


class Collect(unittest.TestCase):
    retailer = shop("Portugal|Worten")

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.log = common.ResumeLog(Path(folder.name) / "p.jsonl", "page_key")

    def run_pages(self, pages, **kwargs):
        self.calls = []

        def fetch(url, retailer, page):
            self.calls.append(url)
            return pages[page - 1]
        return s1b.collect_term(self.retailer, term(261, "Portugal", "Worten"), SETTINGS, fetch, self.log, **kwargs)

    def test_stops_when_site_has_no_next(self):
        outcome = self.run_pages([page_record([card(1)]), page_record([card(2)], has_next=False, total=2)])
        self.assertEqual((outcome["stop"], len(outcome["cards"]), len(self.calls)), ("end", 2, 2))
        self.assertEqual(s1b.judge_outcome(outcome, LIMIT)[0], "끝 도달")

    def test_cap_trims_to_limit(self):
        outcome = self.run_pages([page_record([card(index) for index in range(start, start + 300)]) for start in range(0, 1500, 300)])
        self.assertEqual((outcome["stop"], len(outcome["cards"]), len(self.calls)), ("limit", LIMIT, 4))
        self.assertEqual(s1b.judge_outcome(outcome, LIMIT)[0], "상한 적용")

    def test_load_more_page_repeating_front_is_cut(self):
        outcome = self.run_pages([page_record([card(1), card(2)]), page_record([card(1), card(2), card(3), card(4)], has_next=False, total=4)])
        self.assertEqual([item["link"][-1] for item in outcome["cards"]], list("1234"))
        self.assertEqual([item["page"] for item in outcome["cards"]], [1, 1, 2, 2])

    def test_duplicates_elsewhere_are_kept(self):
        outcome = self.run_pages([page_record([card(1), card(2)]), page_record([card(2), card(3)], has_next=False)])
        self.assertEqual(len(outcome["cards"]), 4)

    def test_same_page_again_stops(self):
        outcome = self.run_pages([page_record([card(1)]), page_record([card(1)]), page_record([card(9)])])
        self.assertEqual((outcome["stop"], len(outcome["cards"]), len(self.calls)), ("repeat", 1, 2))

    def test_failed_page_is_reported_and_needs_manual(self):
        failure = {**page_record([], has_next=False), "ok": False, "problem": "차단 화면"}
        outcome = self.run_pages([failure])
        status, result = s1b.judge_outcome(outcome, LIMIT)
        self.assertEqual(status, "수집 실패")
        self.assertIn("차단 화면", result)

    def test_site_zero_is_not_failure(self):
        outcome = self.run_pages([page_record([], has_next=False, zero=True)])
        self.assertEqual(s1b.judge_outcome(outcome, LIMIT)[0], "원문 0건")

    def test_count_difference_is_recorded_not_refetched(self):
        outcome = self.run_pages([page_record([card(1)], has_next=False, total=5)])
        self.assertEqual((s1b.judge_outcome(outcome, LIMIT)[0], len(self.calls)), ("수 불일치", 1))

    def test_page_guard(self):
        outcome = self.run_pages([page_record([card(index)]) for index in range(5)], max_pages=2)
        self.assertEqual((outcome["stop"], len(self.calls)), ("max_pages", 2))

    def test_second_run_does_not_pay_again(self):
        pages = [page_record([card(1)]), page_record([card(2)], has_next=False)]
        first = self.run_pages(pages)
        again = self.run_pages(pages)
        self.assertEqual(self.calls, [])
        self.assertEqual(len(again["cards"]), len(first["cards"]))

    def test_failed_page_is_tried_again_next_run(self):
        failure = {**page_record([], has_next=False), "ok": False, "problem": "x"}
        self.run_pages([failure])
        outcome = self.run_pages([page_record([card(1)], has_next=False)])
        self.assertEqual((len(self.calls), len(outcome["cards"])), (1, 1))

    def test_output_shapes(self):
        outcome = self.run_pages([page_record([card(1)]), page_record([card(2)], has_next=False, total=2)])
        rows = s1b.card_rows(outcome)
        self.assertEqual(tuple(rows[0]), s1b.CARD_COLUMNS)
        self.assertEqual([row["카드순번"] for row in rows], [1, 2])
        summary = s1b.reconcile_row(outcome, LIMIT)
        self.assertEqual(tuple(summary), s1b.RECONCILE_COLUMNS)
        self.assertEqual((len(s1b.CARD_COLUMNS), len(s1b.RECONCILE_COLUMNS)), (14, 27))
        self.assertEqual(summary["접속근거"], "Zyte geolocation=PT")
        self.assertEqual((summary["최종저장카드수"], summary["대조결과"]), (2, "표시 수와 실제 카드 수 일치"))

    def test_columns_cover_what_s2_reads(self):
        self.assertLessEqual({"국가", "리테일러", "F열제품군", "상품명", "카드PDP링크", "수집시각", "J열검색어", "엑셀행번호", "광고여부"}, set(s1b.CARD_COLUMNS))


class Fetch(unittest.TestCase):
    retailer = shop("Egypt|Cairo Sales")
    good = '<div id="center_column"><ul class="product_list"><li><a class="product-name" href="/p/1">a</a></li></ul></div>'

    def fetch(self, answers, page=1):
        with mock.patch("builtins.print"):
            post = mock.Mock(side_effect=answers)
            return s1b.fetch_page("https://x/s", self.retailer, page, SETTINGS, "k", post), post

    def body(self, html, status=200):
        return 200, {"url": "https://x/f", "statusCode": status, "httpResponseBody": base64.b64encode(html.encode()).decode()}

    def test_success_first_time(self):
        record, post = self.fetch([self.body(self.good)])
        self.assertEqual((record["ok"], record["cards"][0]["link"], post.call_count), (True, "https://x/p/1", 1))

    def test_block_then_success(self):
        record, post = self.fetch([self.body("Just a moment"), self.body(self.good)])
        self.assertEqual((record["ok"], record["attempts"], post.call_count), (True, 2, 2))

    def test_gives_up_after_three_retries(self):
        record, post = self.fetch([(520, {"title": "Website Ban"})] * 4)
        self.assertEqual((record["ok"], post.call_count), (False, 4))
        self.assertIn("Website Ban", record["problem"])

    def test_first_page_without_cards_is_a_problem(self):
        record, post = self.fetch([self.body("<html></html>")] * 4)
        self.assertFalse(record["ok"])
        self.assertIn("카드 없음", record["problem"])

    def test_later_empty_page_is_a_normal_end_after_retries(self):
        record, post = self.fetch([self.body("<html></html>")] * 4, page=2)
        self.assertEqual((record["ok"], record["cards"], post.call_count), (True, [], 4))

    def test_later_empty_page_is_fetched_again(self):
        record, post = self.fetch([self.body("<html></html>"), self.body(self.good)], page=2)
        self.assertEqual((record["ok"], len(record["cards"]), post.call_count), (True, 1, 2))

    def test_page_with_loading_slots_is_fetched_again(self):
        retailer = shop("Poland|MEDIAEXPERT")
        card = '<div class="offer-box" data-product-sku="1"><h3><a href="/p/{0}" aria-label="n{0}">n</a></h3></div>'
        partial = '<div data-cy="offersList">' + card.format(1) + '<div class="skeleton"></div></div>'
        full = '<div data-cy="offersList">' + card.format(1) + card.format(2) + '</div>'
        with mock.patch("builtins.print"):
            post = mock.Mock(side_effect=[self.body(partial), self.body(full)])
            record = s1b.fetch_page("https://x/s", retailer, 1, SETTINGS, "k", post)
        self.assertEqual((record["ok"], len(record["cards"]), post.call_count), (True, 2, 2))
        with mock.patch("builtins.print"):
            post = mock.Mock(side_effect=[self.body(partial)] * 4)
            record = s1b.fetch_page("https://x/s", retailer, 1, SETTINGS, "k", post)
        self.assertEqual((record["ok"], len(record["cards"]), record["loading"], post.call_count), (True, 1, 1, 4))

    def test_site_says_zero(self):
        record, post = self.fetch([self.body('<div id="center_column">لم يتم العثور</div>')])
        self.assertEqual((record["ok"], record["zero"], post.call_count), (True, True, 1))

    def test_site_error_is_retried(self):
        record, post = self.fetch([self.body(self.good, 503), self.body(self.good)])
        self.assertEqual((record["ok"], post.call_count), (True, 2))


class CollectionPlan(unittest.TestCase):
    def test_full_plan_covers_every_term_with_about_two_thousand_requests(self):
        planned, manual = s1b.plan_collection(TERMS, SETTINGS, sample=False)
        self.assertEqual((len(planned), manual), (126, []))
        self.assertTrue(1000 < sum(item["pages"] for item in planned) < 3000)

    def test_sample_is_one_term_per_retailer_and_two_pages(self):
        planned, _ = s1b.plan_collection(s1b.sample_terms(TERMS, SETTINGS), SETTINGS, sample=True)
        self.assertEqual(len(planned), 12)
        self.assertLessEqual(max(item["pages"] for item in planned), 2)

    def test_manual_retailer_is_not_called(self):
        changed = {**SETTINGS, "retailers": {**SETTINGS["retailers"], "Portugal|Worten": {**shop("Portugal|Worten"), "search_method": "manual"}}}
        planned, manual = s1b.plan_collection(TERMS, changed, sample=False)
        self.assertEqual((len(planned), len(manual)), (117, 9))
        self.assertIn("수동 수집", s1b.render_collection_preview("2026-11", planned, manual, changed, common.load_config(RUN, "zyte_pricing"), False))

    def test_empty_method_stops(self):
        changed = {**SETTINGS, "retailers": {**SETTINGS["retailers"], "Portugal|Worten": {**shop("Portugal|Worten"), "search_method": None}}}
        with self.assertRaises(common.ConfigError):
            s1b.plan_collection(TERMS, changed, sample=False)


class CollectionRun(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.run_paths = common.RunPaths("2026-11", Path(folder.name)).create()
        for name in ("search_urls", "search_terms", "zyte_pricing"):
            shutil.copy(RUN.sub("config") / f"{name}.json", self.run_paths.sub("config") / f"{name}.json")
        for target, value in (("get_logger", mock.Mock()), ("RunPaths", self.run_paths), ("read_secret", FAKE_KEY)):
            patcher = mock.patch.object(s1b, target, return_value=value)
            setattr(self, target, patcher.start())
            self.addCleanup(patcher.stop)

    def main(self, *arguments):
        answer = (520, {"title": "Website Ban"})
        with mock.patch.object(s1b, "zyte_post", return_value=answer) as post, mock.patch("builtins.print") as shown:
            code = s1b.main(["--month", "2026-11", *arguments])
        return post, shown, code

    def test_default_full_run_calls_nothing(self):
        post, shown, _ = self.main()
        post.assert_not_called()
        self.read_secret.assert_not_called()
        self.assertIn("왜 부르나", shown.call_args[0][0])
        self.assertFalse((self.run_paths.sub("candidates") / s1b.CARDS_NAME).exists())

    def test_probe_and_sample_cannot_mix(self):
        with self.assertRaises(common.ConfigError):
            s1b.main(["--month", "2026-11", "--probe", "--sample"])

    def test_failed_full_run_lists_every_term_and_returns_error(self):
        post, _, code = self.main("--run")
        columns, rows = common.read_csv(self.run_paths.sub("candidates") / s1b.RECONCILE_NAME)
        self.assertEqual(code, 1)
        self.assertEqual((tuple(columns), len(rows), {row["완료구분"] for row in rows}), (s1b.RECONCILE_COLUMNS, 126, {"수집 실패"}))
        self.assertEqual(post.call_count, 126 * 4)

    def test_one_retailer_preview_lists_only_that_retailer(self):
        post, shown, _ = self.main("--retailer", "Netherlands|MEDIAMARKT")
        post.assert_not_called()
        text = shown.call_args[0][0]
        self.assertIn("--retailer 'Netherlands|MEDIAMARKT'", text)
        self.assertIn("| Netherlands | MEDIAMARKT | 8 |", text)
        self.assertNotIn("| Czech Republic |", text)

    def test_retailer_name_alone_must_be_unique(self):
        self.assertEqual(s1b.retailer_key("alza", SETTINGS), "Czech Republic|ALZA")
        with self.assertRaises(common.ConfigError):
            s1b.retailer_key("MEDIAMARKT", SETTINGS)  # 네덜란드와 헝가리 두 곳
        with self.assertRaises(common.ConfigError):
            s1b.main(["--month", "2026-11", "--retailer", "ALZA", "--sample"])

    def test_one_retailer_run_replaces_only_its_rows(self):
        _, _, code = self.main("--retailer", "Czech Republic|ALZA", "--run")
        self.assertEqual(code, 1)
        _, _, _ = self.main("--retailer", "Czech Republic|DATART", "--run")
        folder = self.run_paths.sub("candidates")
        _, rows = common.read_csv(folder / s1b.RECONCILE_NAME)
        self.assertEqual(Counter(row["리테일러"] for row in rows), Counter({"ALZA": 9, "DATART": 9}))
        post, _, code = self.main("--retailer", "Czech Republic|ALZA", "--run")
        self.assertEqual((post.call_count, code), (0, 0))  # 이미 있으면 다시 부르지 않음
        post, _, _ = self.main("--retailer", "Czech Republic|ALZA", "--run", "--force")
        self.assertEqual(post.call_count, 9 * 4)
        _, rows = common.read_csv(folder / s1b.RECONCILE_NAME)
        self.assertEqual(Counter(row["리테일러"] for row in rows), Counter({"ALZA": 9, "DATART": 9}))

    def test_sample_makes_no_candidate_files_and_leaves_no_key(self):
        self.main("--sample", "--run")
        self.assertFalse((self.run_paths.sub("candidates") / s1b.CARDS_NAME).exists())
        self.assertTrue((self.run_paths.sub("logs") / s1b.SAMPLE_REPORT).exists())
        for path in self.run_paths.directory.rglob("*"):
            if path.is_file() and path.suffix in (".md", ".jsonl", ".log"):
                self.assertNotIn(FAKE_KEY, path.read_text(encoding="utf-8"), path)


if __name__ == "__main__":
    unittest.main()


class InterleavedOrder(unittest.TestCase):
    def test_retailers_take_turns_and_every_item_once(self):
        planned = [{"retailer": {"retailer": name}} for name in ["A", "A", "A", "B", "C", "C"]]
        order = s1b.interleaved_order(planned)
        self.assertEqual(order, [0, 3, 4, 1, 5, 2])
        self.assertEqual(sorted(order), list(range(len(planned))))
