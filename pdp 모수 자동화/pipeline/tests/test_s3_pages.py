"""S3: 기본 실행은 호출하지 않고, 방식 전환·상태 판정·이어받기가 맞는지 본다. 11월 저장 HTML로 eXtra·DIENMAYXANH 상태를 전수 대조한다."""
import base64
import contextlib
import gzip
import io
import json
import logging
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

import common
import s2_filter as s2
import s3_pages as s3

RUN = common.RunPaths("2026-11")
FAKE_KEY = "FAKE-KEY-FOR-TEST"
PATCHER = mock.patch("urllib.request.urlopen", side_effect=AssertionError("테스트에서 실제 호출이 나갔습니다"))


def setUpModule():
    PATCHER.start()


def tearDownModule():
    PATCHER.stop()


COMMON = common.load_config(RUN, "retailer_rules")["common"]
RULES, FETCH = COMMON["page_status"], COMMON["page_fetch"]
PADDING = "<div>" + "x" * 70000 + "</div>"
GOOD = f"<html><title>Fridge</title>{PADDING}</html>"
BLOCK = "<html><title>Just a moment</title>captcha</html>"


def item(retailer="SHOP", browser=False):
    return {"url": "https://x/1", "country": "C", "retailer": retailer, "geolocation": "DE", "browser_first": browser}


def fake_post(*responses):
    calls = []
    queue = list(responses)

    def post(payload, key, api_url, timeout):
        calls.append(payload)
        return queue.pop(0)

    post.calls = calls
    return post


def http_body(html, code=200, url="https://x/final"):
    return 200, {"httpResponseBody": base64.b64encode(html.encode()).decode(), "statusCode": code, "url": url}


def browser_body(html, code=200, url="https://x/final"):
    return 200, {"browserHtml": html, "statusCode": code, "url": url}


class Status(unittest.TestCase):
    def status(self, html, code=200, retailer="SHOP"):
        return s3.judge_status(html, code, retailer, RULES)[0]

    def test_big_page_with_captcha_word_is_normal(self):
        self.assertEqual(self.status(GOOD + "captcha"), s3.NORMAL)

    def test_small_block_page(self):
        self.assertEqual(self.status(BLOCK), s3.BLOCKED)

    def test_small_page_without_title_is_blocked(self):
        self.assertEqual(self.status("<html>hello</html>"), s3.BLOCKED)

    def test_small_normal_page(self):
        self.assertEqual(self.status("<html><title>Fridge</title>ok</html>"), s3.NORMAL)

    def test_not_found_codes(self):
        self.assertEqual(self.status(GOOD, 404), "없음(404)")
        self.assertEqual(self.status(GOOD, 410), "없음(410)")

    def test_410_with_title_and_sold_out_is_permanent(self):
        self.assertEqual(self.status(GOOD + "dauerhaft ausverkauft", 410), "영구품절")

    def test_404_with_sold_out_stays_missing(self):
        self.assertEqual(self.status(GOOD + "ausverkauft", 404), "없음(404)")

    def test_title_not_found(self):
        self.assertEqual(self.status(f"<html><title>Page not found</title>{PADDING}</html>"), "없음(제목)")

    def test_shell_page_is_blocked_even_when_big(self):
        shell = '<link id="canonicalLink" rel="canonical" href="https://www.appliancesonline.com.au/">'
        self.assertEqual(self.status(f"<html><title>Home</title>{shell}{PADDING}</html>", retailer="Appliance Online"), s3.BLOCKED)
        self.assertEqual(self.status(f"<html><title>Home</title>{shell}{PADDING}</html>"), s3.NORMAL)

    def test_retailer_size_limit(self):
        rules = {**RULES, "block_max_size_by_retailer": {"SHOP": 100}}
        self.assertEqual(s3.judge_status(BLOCK + "x" * 200, 200, "SHOP", rules)[0], s3.NORMAL)

    def test_dienmayxanh_text(self):
        self.assertEqual(self.status(GOOD + "NGƯNG KINH DOANH", retailer="DIENMAYXANH"), "판매중단")
        self.assertEqual(self.status(GOOD + "NGƯNG KINH DOANH"), s3.NORMAL)

    def test_momoshop_unavailable_notice(self):
        notice = '<html><title>momo購物網 -- Mobile管理訊息</title><p>很抱歉！網頁無法顯示。可能的原因是：</p><ul><li>商品目前無展售</li><li>網頁不存在</li></ul></html>'
        self.assertEqual(self.status(notice, retailer="MOMOSHOP"), "없음(商品目前無展售)")
        self.assertEqual(self.status(GOOD, retailer="MOMOSHOP"), s3.NORMAL)

    def test_extra_stock_code(self):
        page = GOOD + 'var pdpDetails = {"stock":{"stockLevelStatus":{"code":"%s"}}};'
        self.assertEqual(self.status(page % "outOfStock", retailer="EXTRA"), "품절")
        self.assertEqual(self.status(page % "inStock", retailer="EXTRA"), s3.NORMAL)

    def test_extra_broken_json_is_reported(self):
        status, note = s3.judge_status(GOOD + "var pdpDetails = {broken};", 200, "EXTRA", RULES)
        self.assertEqual(status, s3.NORMAL)
        self.assertIn("품절 여부", note)


class Extract(unittest.TestCase):
    def test_breadcrumb_path(self):
        data = {"@type": "BreadcrumbList", "itemListElement": [{"name": "AGD"}, {"item": {"name": "Akcesoria AGD"}}]}
        html = f'<script type="application/ld+json">{json.dumps(data)}</script>'
        self.assertEqual(s3.category_path_of(html), "AGD > Akcesoria AGD")

    def test_breadcrumb_inside_graph(self):
        data = {"@graph": [{"@type": "Product"}, {"@type": "BreadcrumbList", "itemListElement": [{"name": "A"}]}]}
        self.assertEqual(s3.category_path_of(f'<script type="application/ld+json">{json.dumps(data)}</script>'), "A")

    def test_no_breadcrumb(self):
        self.assertEqual(s3.category_path_of('<script type="application/ld+json">{broken</script>'), "")

    def test_visible_breadcrumbs_when_structured_path_has_only_the_product(self):
        data = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "item": {"name": "MAL WW90 SAMSUNG"}, "position": 1}]}
        html = (f'<script type="application/ld+json">{json.dumps(data)}</script>'
                '<div class="breadcrumbs"><ul class="items"><li class="item home"><a href="/">Accueil</a></li>'
                '<li class="item"><a href="/g">Gros electrom&eacute;nager</a></li><li class="item"><strong>Machine à laver</strong></li></ul></div>')
        self.assertEqual(s3.category_path_of(html), "Accueil > Gros electroménager > Machine à laver")
        self.assertEqual(s3.visible_path_of('<ol class="breadcrumbs"><li>Strona główna ›</li><li>›</li><li>AGD /</li></ol>'), "Strona główna > AGD")

    def test_canonical_and_title(self):
        html = '<title>  A\n B </title><link rel="canonical" href="https://x/c">'
        self.assertEqual((s3.title_of(html), s3.canonical_of(html)), ("A B", "https://x/c"))


class Plan(unittest.TestCase):
    def test_skips_excluded_and_repeated_urls(self):
        targets = [{"country": "Germany", "retailer": "OTTO", "zyte_geolocation": None, "console_country_codes": ["DE"]}]
        rows = [{"판정": s2.EXCLUDE, "URL": "a", "국가": "Germany", "리테일러": "OTTO"}, {"판정": s2.KEEP, "URL": "b", "국가": "Germany", "리테일러": "OTTO"}, {"판정": s2.CHECK, "URL": "b", "국가": "Germany", "리테일러": "OTTO"}]
        self.assertEqual([entry["url"] for entry in s3.plan_pages(rows, targets, RULES, FETCH)], ["b"])

    def test_tail_urls_are_attached_only_where_reopening_is_set(self):
        """D158: 같은 일반 주소 행들의 꼬리 주소를 모두 중복 없이 붙인다. 설정에 없는 곳, 제외된 행, 원본URL이 같은 행은 붙이지 않는다."""
        targets = [{"country": "France", "retailer": "DARTY", "zyte_geolocation": None, "console_country_codes": ["FR"]},
                   {"country": "Germany", "retailer": "OTTO", "zyte_geolocation": None, "console_country_codes": ["DE"]}]
        row = lambda url, raw, retailer="DARTY", country="France", verdict=s2.KEEP: {"판정": verdict, "URL": url, "원본URL": raw, "국가": country, "리테일러": retailer}
        rows = [row("d1", "d1"), row("d1", "d1?ofmp=1"), row("d1", "d1?ofmp=2"), row("d1", "d1?ofmp=1"), row("d2", "d2?ofmp=9", verdict=s2.EXCLUDE), row("d2", "d2"),
                row("o1", "o1?x=1", "OTTO", "Germany")]
        planned = {entry["url"]: entry for entry in s3.plan_pages(rows, targets, RULES, FETCH, {("France", "DARTY")})}
        self.assertEqual(list(planned), ["d1", "d2", "o1"])
        self.assertEqual(planned["d1"]["fallback_urls"], ["d1?ofmp=1", "d1?ofmp=2"])
        self.assertNotIn("fallback_urls", planned["d2"])
        self.assertNotIn("fallback_urls", planned["o1"])

    def test_reopening_is_set_for_darty_and_two_amazons_only(self):
        shops = s3.fallback_shops(common.load_config(RUN, "osm_query"))
        self.assertEqual(shops, {("France", "DARTY"), ("Germany", "AMAZON"), ("Italy", "AMAZON")})
        names = {(target["country"], target["retailer"]) for target in common.load_config(RUN, "targets")["targets"]}
        self.assertLessEqual(shops, names)

    def test_unknown_retailer_stops(self):
        with self.assertRaises(common.ConfigError):
            s3.plan_pages([{"판정": s2.KEEP, "URL": "b", "국가": "X", "리테일러": "Y"}], [], RULES, FETCH)

    def test_every_target_gets_a_zyte_country_code(self):
        for target in common.load_config(RUN, "targets")["targets"]:
            code = s3.geolocation_of(target, FETCH)
            self.assertRegex(code, r"^[A-Z]{2}$")
            self.assertNotEqual(code, "UK")

    def test_browser_required_retailers_exist_in_targets(self):
        names = {target["retailer"] for target in common.load_config(RUN, "targets")["targets"]}
        self.assertLessEqual(set(RULES["browser_required"]), names)
        self.assertLessEqual(set(RULES["retailer_markers"]), names)


class Fetch(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name)
        self.sleeps = []

    def check(self, post, entry=None):
        return s3.check_url(entry or item(), RULES, FETCH, FAKE_KEY, self.path, post, self.sleeps.append)

    def test_good_html_uses_html_only_with_country(self):
        post = fake_post(http_body(GOOD))
        record = self.check(post)
        self.assertEqual((record["status"], record["method"], len(post.calls)), (s3.NORMAL, s3.METHOD_HTML, 1))
        self.assertEqual((post.calls[0]["geolocation"], record["geolocation"]), ("DE", "DE"))
        self.assertEqual(gzip.decompress((self.path / record["html_file"]).read_bytes()).decode(), GOOD)

    def test_blocked_html_moves_to_browser_with_country(self):
        post = fake_post(http_body(BLOCK), browser_body(GOOD))
        record = self.check(post)
        self.assertEqual((record["status"], record["method"]), (s3.NORMAL, s3.METHOD_BROWSER))
        self.assertEqual(post.calls[1]["geolocation"], "DE")
        self.assertTrue(post.calls[1]["browserHtml"])

    def test_browser_required_skips_html(self):
        post = fake_post(browser_body(GOOD))
        record = self.check(post, item(browser=True))
        self.assertEqual((record["method"], len(post.calls)), (s3.METHOD_BROWSER, 1))

    def test_both_blocked_keeps_browser_result(self):
        record = self.check(fake_post(http_body(BLOCK), browser_body(BLOCK)))
        self.assertEqual((record["status"], record["method"], record["ok"]), (s3.BLOCKED, s3.METHOD_BROWSER, True))

    def test_blocked_html_and_failed_browser_keeps_block(self):
        record = self.check(fake_post(http_body(BLOCK), (422, {"title": "bad"})))
        self.assertEqual((record["status"], record["method"]), (s3.BLOCKED, s3.METHOD_HTML))

    def test_retries_on_temporary_error_then_succeeds(self):
        post = fake_post((520, {"title": "ban"}), (503, {}), http_body(GOOD))
        record = self.check(post)
        self.assertEqual((record["status"], record["tries"][0]["attempts"]), (s3.NORMAL, 3))
        self.assertEqual(self.sleeps, [5, 20])

    def test_network_error_is_retried(self):
        record = self.check(fake_post((0, {"title": "URLError"}), http_body(GOOD)))
        self.assertEqual(record["status"], s3.NORMAL)

    def test_permanent_api_error_is_not_retried(self):
        post = fake_post((422, {"title": "bad"}), (422, {"title": "bad"}))
        record = self.check(post)
        self.assertEqual((len(post.calls), record["status"], record["ok"]), (2, s3.FAILED, False))

    def test_gives_up_after_all_retries_on_both_ways(self):
        post = fake_post(*[(520, {"title": "ban"})] * 8)
        record = self.check(post)
        self.assertEqual((len(post.calls), record["status"]), (8, s3.FAILED))
        self.assertIn("520", record["problem"])

    def test_site_404_is_not_a_failure(self):
        record = self.check(fake_post(http_body(GOOD, 404)))
        self.assertEqual(record["status"], "없음(404)")

    TAILS = ["https://a/dp/B1?smid=S1", "https://a/dp/B1?smid=S2"]

    def tail_item(self):
        return {**item("AMAZON"), "url": "https://a/dp/B1", "fallback_urls": list(self.TAILS)}

    def check_item(self, post, entry=None, done=None):
        return s3.check_item(entry or self.tail_item(), RULES, FETCH, FAKE_KEY, self.path, done, post, self.sleeps.append)

    def test_missing_plain_page_opens_every_tail_url_separately(self):
        """D158: 일반 주소가 페이지 없음이면 꼬리 주소를 모두 하나씩 열어 각자 기록한다. 일반 주소 기록은 페이지 없음 그대로다."""
        post = fake_post(http_body(GOOD, 404, url="https://a/dp/B1"), http_body(GOOD, url=self.TAILS[0]), http_body(GOOD, 410, url=self.TAILS[1]))
        plain, first, second = self.check_item(post)
        self.assertEqual([call["url"] for call in post.calls], ["https://a/dp/B1", *self.TAILS])
        self.assertEqual((plain["url"], plain["status"]), ("https://a/dp/B1", "없음(404)"))
        self.assertNotIn("fallback_from_status", plain)
        self.assertEqual((first["url"], first["status"], first["final_url"], first["fallback_url"], first["fallback_from_status"]), (self.TAILS[0], s3.NORMAL, self.TAILS[0], self.TAILS[0], "없음(404)"))
        self.assertEqual(first["html_file"], common.html_filename(self.TAILS[0]))
        self.assertEqual((second["url"], second["status"]), (self.TAILS[1], "없음(410)"))

    def test_found_or_blocked_plain_page_is_not_reopened(self):
        """외부 판매자 화면이어도 일반 주소가 열렸으면 다시 열지 않는다(06 문서 2-7a). 차단도 페이지 없음이 아니므로 다시 열지 않는다."""
        for responses, status in (((http_body(GOOD),), s3.NORMAL), ((http_body(BLOCK), browser_body(BLOCK)), s3.BLOCKED)):
            post = fake_post(*responses)
            records = self.check_item(post)
            self.assertEqual([record["status"] for record in records], [status])
            self.assertEqual(len(post.calls), len(responses))

    def test_missing_without_tail_url_is_not_reopened(self):
        post = fake_post(http_body(GOOD, 404))
        self.assertEqual(([record["status"] for record in self.check_item(post, item())], len(post.calls)), (["없음(404)"], 1))

    def test_blocked_or_failed_tail_stays_for_manual_check(self):
        """꼬리 주소가 차단이나 수집실패면 그 결과를 그대로 남긴다(일반 주소의 페이지 없음으로 되돌리지 않는다)."""
        post = fake_post(http_body(GOOD, 404), http_body(BLOCK), browser_body(BLOCK), (400, {"title": "bad"}), (400, {"title": "bad"}))
        _, blocked, failed = self.check_item(post)
        self.assertEqual((blocked["status"], blocked["fallback_from_status"]), (s3.BLOCKED, "없음(404)"))
        self.assertEqual((failed["status"], failed["ok"], failed["fallback_url"]), (s3.FAILED, False, self.TAILS[1]))

    def test_finished_urls_are_not_called_again(self):
        plain = {"url": "https://a/dp/B1", "ok": True, "status": "없음(404)"}
        post = fake_post(http_body(GOOD))
        records = self.check_item(post, done={plain["url"]: plain, self.TAILS[0]: {"url": self.TAILS[0], "ok": True, "status": s3.NORMAL}})
        self.assertEqual(([call["url"] for call in post.calls], [record["url"] for record in records]), ([self.TAILS[1]], [self.TAILS[1]]))

    def test_key_never_in_record(self):
        record = self.check(fake_post((520, {"title": "ban"}), *[(520, {})] * 7))
        self.assertNotIn(FAKE_KEY, json.dumps(record))


class Resume(unittest.TestCase):
    def test_failed_url_is_retried_and_done_url_is_not(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            log = common.ResumeLog(folder / "log.jsonl", "url")
            done = {**item(), "url": "https://x/done", "browser_first": False}
            failed = {**item(), "url": "https://x/failed"}
            log.append({"url": done["url"], "ok": True, "status": s3.NORMAL})
            log.append({"url": failed["url"], "ok": False, "status": s3.FAILED})
            post = fake_post(http_body(GOOD))
            s3.run_checks([done, failed], RULES, FETCH, common.ResumeLog(folder / "log.jsonl", "url"), FAKE_KEY, folder, logging.getLogger("t"), post, lambda _: None)
            again = common.ResumeLog(folder / "log.jsonl", "url")
            self.assertEqual(len(post.calls), 1)
            self.assertEqual(post.calls[0]["url"], failed["url"])
            self.assertEqual(again.records[failed["url"]]["status"], s3.NORMAL)


    def test_only_failed_tail_is_called_again(self):
        """D158: 일반 주소가 페이지 없음으로 끝났고 꼬리 주소 하나만 실패했으면, 다시 실행할 때 그 꼬리 주소만 부른다."""
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            log = common.ResumeLog(folder / "log.jsonl", "url")
            entry = {**item("AMAZON"), "url": "https://a/dp/B1", "fallback_urls": ["https://a/dp/B1?smid=S1", "https://a/dp/B1?smid=S2"]}
            log.append({"url": entry["url"], "ok": True, "status": "없음(404)"})
            log.append({"url": "https://a/dp/B1?smid=S1", "ok": True, "status": s3.NORMAL})
            log.append({"url": "https://a/dp/B1?smid=S2", "ok": False, "status": s3.FAILED})
            post = fake_post(http_body(GOOD))
            s3.run_checks([entry], RULES, FETCH, common.ResumeLog(folder / "log.jsonl", "url"), FAKE_KEY, folder, logging.getLogger("t"), post, lambda _: None)
            self.assertEqual([call["url"] for call in post.calls], ["https://a/dp/B1?smid=S2"])
            again = common.ResumeLog(folder / "log.jsonl", "url")
            self.assertEqual((again.records["https://a/dp/B1?smid=S2"]["status"], again.records["https://a/dp/B1?smid=S2"]["fallback_from_status"]), (s3.NORMAL, "없음(404)"))
            post = fake_post()
            s3.run_checks([entry], RULES, FETCH, again, FAKE_KEY, folder, logging.getLogger("t"), post, lambda _: None)
            self.assertEqual(post.calls, [])

class Pages(unittest.TestCase):
    def page(self, url="a", status=s3.NORMAL, method=s3.METHOD_HTML):
        return {"url": url, "country": "C", "retailer": "R", "status": status, "method": method, "problem": "", "note": "", "final_url": "", "title": "", "html_file": "", "ok": True}

    def test_manual_overrides_and_marks_method(self):
        entry = {"요청URL": "a", "상태": "차단화면", "제목": "Oops!", "실제URL": "", "HTML파일": ""}
        page = s3.apply_manual([self.page()], [entry])[0]
        self.assertEqual((page["status"], page["method"], page["final_url"]), ("차단화면", s3.METHOD_MANUAL, "a"))

    def test_manual_unknown_url_stops(self):
        with self.assertRaises(common.ConfigError):
            s3.apply_manual([self.page()], [{"요청URL": "b", "상태": "정상", "제목": "", "실제URL": ""}])

    def test_outputs_list_only_unresolved(self):
        with tempfile.TemporaryDirectory() as name:
            run = common.RunPaths("2026-11", root=Path(name)).create()
            pages = [self.page("a"), self.page("b", s3.BLOCKED), self.page("c", s3.FAILED, ""), self.page("d", s3.BLOCKED, s3.METHOD_MANUAL)]
            pending = s3.write_outputs(run, pages)
            self.assertEqual([row["요청URL"] for row in pending], ["b", "c"])
            self.assertEqual(len((run.sub("judgments") / s3.PAGES_NAME).read_text(encoding="utf-8").splitlines()), 4)

    def test_report_lists_reopened_pages(self):
        reopened = {**self.page("https://a/dp/B1?smid=S"), "fallback_url": "https://a/dp/B1?smid=S", "fallback_from_status": "없음(404)"}
        text = s3.render_report([self.page("https://a/dp/B1", "없음(404)"), reopened])
        self.assertIn("원래 꼬리 주소로 다시 연 페이지 1건", text)
        self.assertIn("| C | R | https://a/dp/B1?smid=S | 없음(404) | 정상 |", text)
        self.assertNotIn("다시 연 페이지", s3.render_report([self.page()]))

    def test_reopened_tail_records_follow_their_plain_record(self):
        planned = [{"url": "a", "fallback_urls": ["a?t=1", "a?t=2"]}, {"url": "b", "fallback_urls": ["b?t=1"]}]
        log = mock.Mock(records={"a": {"url": "a", "status": "없음(404)", "tries": []}, "a?t=1": {"url": "a?t=1", "status": s3.NORMAL}, "a?t=2": {"url": "a?t=2", "status": s3.BLOCKED},
                                 "b": {"url": "b", "status": s3.NORMAL}})
        self.assertEqual([page["url"] for page in s3.build_pages(planned, log)], ["a", "a?t=1", "a?t=2", "b"])
        del log.records["a?t=2"]
        with self.assertRaises(common.ConfigError):
            s3.build_pages(planned, log)

    def test_tries_are_left_out_of_pages(self):
        log = mock.Mock(records={"a": {"url": "a", "tries": [1], "status": s3.NORMAL}})
        self.assertNotIn("tries", s3.build_pages([{"url": "a"}], log)[0])

    def test_missing_url_stops(self):
        with self.assertRaises(common.ConfigError):
            s3.build_pages([{"url": "a"}], mock.Mock(records={}))


class DryRun(unittest.TestCase):
    def test_default_run_never_calls_and_lists_shops(self):
        columns = list(common.load_output_spec(RUN).internal_columns)
        with tempfile.TemporaryDirectory() as name:
            run = common.RunPaths("2026-11", root=Path(name)).create()
            for config in ("retailer_rules", "targets", "zyte_pricing", "osm_query"):
                source = RUN.sub("config") / f"{config}.json"
                (run.sub("config") / source.name).write_bytes(source.read_bytes())
            rows = [{**dict.fromkeys(columns, ""), "판정": s2.KEEP, "URL": "https://x/1", "국가": "Peru", "리테일러": "FALABELLA"}, {**dict.fromkeys(columns, ""), "판정": s2.KEEP, "URL": "https://x/2", "국가": "Germany", "리테일러": "OTTO"},
                    {**dict.fromkeys(columns, ""), "판정": s2.KEEP, "URL": "https://a/dp/B1", "원본URL": "https://a/dp/B1?smid=S", "국가": "Italy", "리테일러": "AMAZON"}]
            common.write_csv(run.sub("judgments") / "step1.csv", columns, rows)
            output = io.StringIO()
            with mock.patch.object(s3, "RunPaths", return_value=run), mock.patch.object(s3, "zyte_post", side_effect=AssertionError("호출됨")), mock.patch.object(s3, "read_secret", side_effect=AssertionError("키를 읽음")), contextlib.redirect_stdout(output):
                self.assertEqual(s3.main(["--month", "2026-11"]), 0)
            text = output.getvalue()
            self.assertIn("주소 3개(HTML 시작 2, 브라우저 시작 1)", text)
            self.assertIn("꼬리 주소로 다시 여는 건 최대 1건 추가", text)
            self.assertIn("대상 꼬리 주소 1개(D158)", text)
            self.assertIn("| Peru | FALABELLA | 1 | 브라우저만 | PE |", text)
            self.assertIn("| Germany | OTTO | 1 | HTML → 막히면 브라우저 | DE |", text)


class SavedHtml(unittest.TestCase):
    """11월에 사람이 전수 확인한 저장 HTML로 상태 판정을 대조한다(05 문서 WP5 완료 기준)."""

    def compare(self, folder, csv_name, retailer, expected_of):
        base = common.REPO_ROOT / "outputs" / folder
        if not base.exists():
            self.skipTest("저장 HTML 없음")
        counts, wrong = Counter(), []
        for row in common.read_csv(base / csv_name)[1]:
            path = base / "html" / Path(row["저장HTML"]).name
            html = (gzip.open(path, "rt", encoding="utf-8", errors="replace") if path.suffix == ".gz" else path.open(encoding="utf-8", errors="replace")).read()
            status = s3.judge_status(html, int(row["HTTP상태"]), retailer, RULES)[0]
            counts[status] += 1
            if status != expected_of(row):
                wrong.append((row["저장HTML"], status, expected_of(row)))
        return counts, wrong

    def test_dienmayxanh_453(self):
        counts, wrong = self.compare("dienmayxanh-v3-all-included-closed-20261105-20261105-112819", "Dienmayxanh_v3포함453_영업중단_전수조사_20261105.csv", "DIENMAYXANH", lambda row: "판매중단" if "NGƯNG" in row["현재화면_분류"] else s3.NORMAL)
        self.assertEqual(wrong, [])
        self.assertEqual(counts, Counter({"판매중단": 183, s3.NORMAL: 270}))

    def test_extra_272(self):
        def expected(row):
            if row["HTTP상태"] == "404":
                return "없음(404)"
            return "품절" if row["현재_재고코드"] == "outOfStock" else s3.NORMAL
        counts, wrong = self.compare("extra-158-20261105", "eXtra_v3포함272_상품화면_품절문구_전수확인_20261105.csv", "EXTRA", expected)
        self.assertEqual(wrong, [])
        self.assertEqual(counts, Counter({"품절": 129, "없음(404)": 3, s3.NORMAL: 140}))


class Scheduling(unittest.TestCase):
    def test_slow_retailer_does_not_hold_back_others(self):
        """느린 곳은 자기 동시 수 안에서만 돌고, 다른 곳 주소는 그 사이에 모두 끝난다."""
        import threading, time
        slow_started, release = threading.Event(), threading.Event()
        finished = []

        def fake_check(entry, *args):
            if entry["retailer"] == "SLOW":
                slow_started.set()
                release.wait(5)
            else:
                finished.append(entry["url"])
            return {"url": entry["url"], "ok": True, "status": s3.NORMAL}

        planned = [{**item(), "retailer": "SLOW", "url": f"https://s/{i}"} for i in range(4)] + [{**item(), "retailer": "FAST", "url": f"https://f/{i}"} for i in range(6)]
        fetch = {**FETCH, "workers": 3, "workers_per_retailer": 1, "log_every": 100}
        with tempfile.TemporaryDirectory() as name, mock.patch.object(s3, "check_url", side_effect=fake_check):
            runner = threading.Thread(target=s3.run_checks, args=(planned, RULES, fetch, common.ResumeLog(Path(name) / "log.jsonl", "url"), FAKE_KEY, Path(name), logging.getLogger("t")))
            runner.start()
            slow_started.wait(5)
            deadline = time.time() + 5
            while len(finished) < 6 and time.time() < deadline:
                time.sleep(0.01)
            self.assertEqual(len(finished), 6)  # 느린 곳 첫 주소가 붙잡힌 동안 빠른 곳 6개가 다 끝남
            release.set()
            runner.join(5)

    def test_every_retailer_gets_a_turn_while_others_are_busy(self):
        """앞 곳 주소가 많아도 뒤 곳 주소가 처음부터 함께 돈다."""
        import threading
        started, gate = [], threading.Event()

        def fake_check(entry, *args):
            started.append(entry["retailer"])
            gate.wait(5)
            return {"url": entry["url"], "ok": True, "status": s3.NORMAL}

        planned = [{**item(), "retailer": "A", "url": f"https://a/{i}"} for i in range(5)] + [{**item(), "retailer": "B", "url": f"https://b/{i}"} for i in range(5)] + [{**item(), "retailer": "C", "url": "https://c/0"}]
        fetch = {**FETCH, "workers": 3, "workers_per_retailer": 3, "log_every": 100}
        with tempfile.TemporaryDirectory() as name, mock.patch.object(s3, "check_url", side_effect=fake_check):
            runner = threading.Thread(target=s3.run_checks, args=(planned, RULES, fetch, common.ResumeLog(Path(name) / "log.jsonl", "url"), FAKE_KEY, Path(name), logging.getLogger("t")))
            runner.start()
            import time
            deadline = time.time() + 5
            while len(started) < 3 and time.time() < deadline:
                time.sleep(0.01)
            self.assertEqual(sorted(started[:3]), ["A", "B", "C"])
            gate.set()
            runner.join(5)
