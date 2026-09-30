#!/usr/bin/env python3
"""Create a source-linked assessment ledger for every URL-list row.

This script never converts unreviewed content candidates or collection failures
to Y/N. It can reuse the independently reviewed LG BCP decisions only when the
saved capture bytes are identical to the reviewed batch. A dated, URL-locked
manual browser check can resolve an ID22 REVIEW without changing that capture.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

from assess_bcp_evidence import assess_id9, assess_id10, assess_id10_hrefs
from audit_id8_images import audit_page


METRICS = ("ID8", "ID9", "ID10", "ID18", "ID19", "ID20", "ID21", "ID22", "ID23")
CONTENT = METRICS[3:]
FIELDS = ("엑셀 행", "국가", "리테일러", "페이지 유형", "브랜드", "제품군", "URL", "수집", *METRICS, "주의")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verdict(status: str, reason: str, evidence: dict | None = None) -> dict:
    return {"status": status, "reason": reason, "evidence": evidence or {}}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_conflicts(batch: Path, records: list[dict]) -> dict[int, str]:
    by_url: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_url[str(record["url"])].append(record)
    issues = {}
    for group in by_url.values():
        if len({str(record["brand"]).casefold() for record in group}) < 2:
            continue
        observed = ""
        for candidate in group:
            page_type = "brand-category" if candidate["pageType"] == "Brand Category Page" else "brand"
            state_path = batch / "pages" / candidate["pageKey"] / page_type / "capture-state.json"
            if state_path.is_file():
                state = read_json(state_path)
                observed = str(state.get("title") or state.get("metadata", {}).get("title") or "")
                if observed:
                    break
        matching = [record for record in group if re.search(r"(?<![A-Za-z])" + re.escape(str(record["brand"])) + r"(?![A-Za-z])", observed, re.I)]
        valid_brand = matching[0]["brand"] if len({record["brand"] for record in matching}) == 1 else None
        for record in group:
            if valid_brand and record["brand"] == valid_brand:
                continue
            other = [item for item in group if item is not record]
            issues[int(record["sourceRow"])] = (
                "같은 주소가 원본 목록의 다른 브랜드에도 배정됨: "
                + ", ".join(f"엑셀 {item['sourceRow']}행 {item['brand']}" for item in other)
                + (f"; 수집 페이지 제목은 {observed}" if observed else "")
            )
    return issues


def redirected_brand_issues(batch: Path, records: list[dict]) -> dict[int, str]:
    """Flag a branded URL that demonstrably lands on an unbranded mixed list."""
    issues = {}
    brands = {str(record["brand"]).casefold() for record in records}
    for record in records:
        if record["pageType"] != "Brand Category Page":
            continue
        page = batch / "pages" / record["pageKey"] / "brand-category"
        if not (page / "capture-state.json").is_file() or not (page / "response.json").is_file():
            continue
        state, response = read_json(page / "capture-state.json"), read_json(page / "response.json")
        requested = urlsplit(str(record["url"]))
        final = urlsplit(str(response.get("final_url") or state.get("url") or ""))
        brand = str(record["brand"]).casefold()
        if not re.search(r"(?<![a-z])" + re.escape(brand) + r"(?![a-z])", requested.path.casefold()):
            continue
        if re.search(r"(?<![a-z])" + re.escape(brand) + r"(?![a-z])", final.path.casefold()):
            continue
        if requested.path == final.path:
            continue
        heading = " ".join([str(state.get("title") or ""), *map(str, state.get("metadata", {}).get("h1", []))]).casefold()
        if re.search(r"(?<![a-z])" + re.escape(brand) + r"(?![a-z])", heading):
            continue
        visible_alts = " ".join(str(item.get("alt") or "") for item in state.get("images", [])
                                if isinstance(item, dict) and item.get("visible") is True)
        other_brands = [name for name in brands - {brand} if re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", visible_alts.casefold())]
        if len(other_brands) >= 2:
            issues[int(record["sourceRow"])] = (
                f"요청한 {record['brand']} 제품군 주소가 일반 목록으로 이동하고, 화면의 상품 이미지 설명에는 "
                f"여러 다른 브랜드가 보임: {response.get('final_url')}; 다른 브랜드 예: {', '.join(sorted(other_brands)[:3])}"
            )
    return issues


def prior_lg_reviews(batch: Path, prior: Path | None) -> dict[int, dict]:
    if not prior:
        return {}
    manifest = read_json(batch / "manifest.json")
    old_manifest = read_json(prior / "manifest.json")
    if manifest["sourceWorkbookSha256"] != old_manifest["sourceWorkbookSha256"]:
        raise ValueError("LG 검토본과 현재 목록 파일의 버전이 다름")
    old = {int(item["sourceWorkbookRow"]): item for item in json.loads((prior / "판정_최종_상세.json").read_text())}
    verified = {}
    for record in manifest["records"]:
        row = int(record["sourceRow"])
        if row not in old or record["url"] != old[row]["url"]:
            continue
        key = record["pageKey"]
        current = batch / "pages" / key / "brand-category"
        former = prior / "pages" / key / "brand-category"
        if all(current.joinpath(name).is_file() and former.joinpath(name).is_file()
               and sha256(current / name) == sha256(former / name)
               for name in ("raw.html", "capture-state.json")):
            verified[row] = old[row]
    return verified


def metadata_checks(record: dict, page: Path) -> tuple[dict, dict]:
    state = read_json(page / "capture-state.json")
    response = read_json(page / "response.json")
    html = (page / "raw.html").read_text(encoding="utf-8", errors="replace")
    requested = str(record["url"])
    final = str(response.get("final_url") or state.get("url") or "")
    changed = bool(final and requested.rstrip("/") != final.rstrip("/"))
    initial = state.get("initialMetadata")
    initial_url = str(initial.get("url") or "") if isinstance(initial, dict) else ""
    source_brand = str(record["brand"])
    requested_path, final_path = urlsplit(requested).path, urlsplit(final).path
    alza_alias = (record["retailerSlug"] == "alza" and requested_path.split("/")[-1] == final_path.split("/")[-1]
                  and re.search(r"(?<![A-Za-z])" + re.escape(source_brand) + r"(?![A-Za-z])", final_path, re.I))
    datart_alias = (record["retailerSlug"] == "datart" and requested_path.replace("/filter/", ".html/filter/") == final_path)
    landing_redirect = changed and initial_url.rstrip("/") == final.rstrip("/") and (alza_alias or datart_alias)
    preserved_requested = changed and initial_url.rstrip("/") == requested.rstrip("/")
    if changed and not (preserved_requested or landing_redirect):
        reason = "스크롤·펼치기 후 주소가 달라졌고 요청 페이지의 태그가 별도로 보존되지 않음"
        return verdict("REVIEW", reason, {"requestedUrl": requested, "finalUrl": final}), verdict(
            "REVIEW", reason, {"requestedUrl": requested, "finalUrl": final})
    metadata = initial if changed else state.get("metadata")
    if not isinstance(metadata, dict):
        return verdict("REVIEW", "메타데이터 저장값 없음"), verdict("REVIEW", "메타데이터 저장값 없음")
    id9 = assess_id9(metadata)
    id10 = assess_id10_hrefs(metadata.get("canonical", [])) if changed else assess_id10(html)
    for result in (id9, id10):
        result["evidence"]["requestedUrl"] = requested
        result["evidence"]["capturedFinalUrl"] = final
        result["evidence"]["moment"] = "landing_after_http_redirect" if landing_redirect else "before_scroll" if changed else "final_capture"
    return id9, id10


def product_check(batch: Path, record: dict) -> dict:
    """Assess the checked first two same-brand product cards, not every card."""
    key = str(record["pageKey"])
    # A later browser check is separate from the original Zyte capture. It may
    # resolve a collection-limited REVIEW, but must never be presented as data
    # that was present in the saved HTML.
    live_path = batch / "product-link-check-live" / f"{key}.json"
    if live_path.is_file():
        live = read_json(live_path)
        checks = live.get("checkedCards", [])
        if (live.get("pageKey") == key and live.get("sourceWorkbookRow") == int(record["sourceRow"])
                and live.get("sourceUrl") == record["url"]
                and live.get("verificationMethod") == "manual_browser_click"
                and live.get("observedDateKST") and len(checks) >= 2
                and len({item.get("productUrl") for item in checks}) == len(checks)
                and all(item.get("clicked") is True
                        and item.get("cardLabel") and item.get("landingTitle")
                        and item.get("modelCode")
                        and str(item["modelCode"]).casefold() in str(item["cardLabel"]).casefold()
                        and str(item["modelCode"]).casefold() in str(item["landingTitle"]).casefold()
                        and re.search(r"(?<![A-Za-z])" + re.escape(str(record["brand"])) + r"(?![A-Za-z])",
                                      str(item["landingTitle"]), re.I)
                        and urlsplit(str(item["productUrl"])).netloc == urlsplit(str(record["url"])).netloc
                        and "/product/" in urlsplit(str(item["productUrl"])).path.casefold()
                        for item in checks)):
            return verdict("Y", f"{live['observedDateKST']} 실제 브라우저에서 상품 카드 {len(checks)}개를 눌러 동일 브랜드·모델의 상품 상세 페이지로 이동 확인", {
                "verificationFile": str(live_path.relative_to(batch)),
                "verificationMethod": live["verificationMethod"],
                "observedDateKST": live["observedDateKST"],
                "checkedCards": checks,
                "originalCheckFile": f"product-link-check/{key}.json",
                "originalExtraRetryFile": f"{key}-extra-retry.json",
                "originalCaptureNotReplaced": True,
            })
        return verdict("REVIEW", "별도 브라우저 확인 기록이 현재 URL 또는 상세 페이지 확인 조건과 일치하지 않음", {
            "verificationFile": str(live_path.relative_to(batch))})
    path = batch / "product-link-check" / f"{key}.json"
    if not path.is_file():
        return verdict("REVIEW", "제품 카드 도착 페이지 검사 자료가 없음")
    data = read_json(path)
    targets = data.get("targets", [])
    if not targets:
        evidence = {"checkFile": str(path.relative_to(batch))}
        extra_retry = batch / f"{key}-extra-retry.json"
        if extra_retry.is_file():
            evidence["extraRetryFile"] = str(extra_retry.relative_to(batch))
            return verdict("REVIEW", "저장 화면의 상품 목록이 로딩 상태이고 60초 추가 대기 재수집도 사이트 차단으로 실패해 상품 상세 이동을 확인하지 못함", evidence)
        return verdict("REVIEW", "저장 화면에서 브랜드 상품 카드 링크를 선택하지 못함", evidence)
    direct_path = batch / "product-link-check-direct" / f"{key}.json"
    direct = read_json(direct_path) if direct_path.is_file() else {}
    direct_by_url = {item.get("url"): item for item in direct.get("results", [])}
    initial_by_url = {item.get("url"): item for item in data.get("results", [])}
    evaluated = []
    for target in targets:
        url = str(target["url"])
        result = direct_by_url.get(url) if direct_by_url.get(url, {}).get("status") == 200 else initial_by_url.get(url, {})
        title = str(result.get("title") or "")
        h1 = str(result.get("h1") or "")
        brand = str(record["brand"])
        brand_matches = bool(re.search(r"(?<![A-Za-z])" + re.escape(brand) + r"(?![A-Za-z])", title + " " + h1, re.I))
        final_url = str(result.get("finalUrl") or url)
        path_lower = urlsplit(final_url).path.casefold()
        is_product = (any(part in path_lower for part in ("/product/", "/products/", "/produkt/", "/produit/", "/prodotto/", "/ref/", "/dp/"))
                      or record["retailerSlug"] == "alza" and bool(re.search(r"-d\d+\.htm$", path_lower))
                      or record["retailerSlug"] == "datart" and bool(re.search(r"/(?:automaticka-|pracka-|susicka-|chladnicka-|lednice-|americka-lednice-|mrazak-|mraznicka-|mycka-|mycka-nadobi-)[^/]+", path_lower)))
        evaluated.append({"url": url, "status": result.get("status"), "title": title,
                          "h1": h1, "finalUrl": final_url, "brandMatches": brand_matches,
                          "productUrl": is_product, "error": result.get("error")})
    evidence = {"checked": evaluated, "coverage": "처음 찾은 서로 다른 동일 브랜드 상품 카드 최대 2개",
                "checkFile": str(path.relative_to(batch))}
    if direct_path.is_file():
        evidence["directRetryFile"] = str(direct_path.relative_to(batch))
    if all(item["status"] == 200 and item["brandMatches"] and item["productUrl"] for item in evaluated):
        return verdict("Y", f"선정한 상품 카드 {len(evaluated)}개가 동일 브랜드 상품 상세 페이지로 열림", evidence)
    if any(item["status"] == 200 and (not item["brandMatches"] or not item["productUrl"]) for item in evaluated):
        return verdict("N", "선정한 상품 카드 중 브랜드가 다르거나 상품 상세 페이지가 아닌 목적지가 있음", evidence)
    return verdict("REVIEW", "제품 카드 목적지 검사가 차단되거나 실패하여 판정 불가", evidence)


def sidebar_nav_check(batch: Path, record: dict, raw_sha: str) -> dict | None:
    """Keep legacy direct-URL visits as context, never as proof of a card click."""
    path = batch / "navigator-sidebar-check" / f"{record['pageKey']}.json"
    if not path.is_file():
        return None
    data = read_json(path)
    if data.get("sourceRawHtmlSha256") != raw_sha:
        return verdict("REVIEW", "제품군 탐색 검사와 현재 저장 HTML의 버전이 다름")
    targets, results = data.get("targets", []), data.get("results", [])
    evidence = {"checkFile": str(path.relative_to(batch)), "targets": targets, "results": results}
    return verdict("REVIEW", "기존 검사는 카드 클릭이 아닌 도착 주소의 별도 접속이므로 ID21 정상 작동을 입증하지 못함", evidence)


def id21_click_check(batch: Path, record: dict, raw_sha: str) -> dict | None:
    """Use only source-locked, successful browser clicks and landing-lineup reviews."""
    path = batch / "navigator-click-check" / record["pageKey"] / "id21-click-review.json"
    if not path.is_file():
        return None
    data = read_json(path)
    evidence = {"checkFile": str(path.relative_to(batch)), "results": data.get("results", []),
                "verificationMethod": data.get("verificationMethod")}
    if (data.get("sourceWorkbookRow") != int(record["sourceRow"])
            or data.get("sourceUrl") != record["url"]
            or data.get("sourceRawHtmlSha256") != raw_sha
            or data.get("verificationMethod") != "zyte_browser_click_then_jev_semantic_review"):
        return verdict("REVIEW", "ID21 클릭 검사 기록이 현재 URL 또는 저장 HTML과 일치하지 않음", evidence)
    results = data.get("results", [])
    if not isinstance(results, list) or not results:
        return verdict("REVIEW", "제품군 탐색 카드의 클릭 검사가 없음", evidence)
    if any(item.get("captureValid") is True and item.get("jevChoice") == "different_lineup" for item in results):
        return verdict("N", "클릭된 탐색 카드 중 도착한 제품군이 다른 카드가 있음", evidence)
    urls = [item.get("card", {}).get("url") for item in results]
    if (len(results) != data.get("expectedCardCount") or data.get("checkedCardCount") != len(results)
            or not all(urls) or len(set(urls)) != len(urls)):
        return verdict("REVIEW", "제품군 탐색 카드 중 클릭·도착 확인을 마치지 않은 것이 있음", evidence)
    if all(item.get("captureValid") is True and item.get("jevChoice") == "matching_lineup" for item in results):
        return verdict("Y", f"제품군 탐색 카드 {len(results)}개를 모두 실제 클릭해 해당 제품군 목록 도착을 확인함", evidence)
    return verdict("REVIEW", "일부 카드의 클릭·상품 목록 수집 또는 도착 제품군 판단 근거가 부족함", evidence)


def assess(batch: Path, lg_prior: Path | None) -> tuple[list[dict], list[dict]]:
    records = read_json(batch / "manifest.json")["records"]
    conflicts = {**source_conflicts(batch, records), **redirected_brand_issues(batch, records)}
    old_lg = prior_lg_reviews(batch, lg_prior)
    review_path = batch / "본문_항목_AI검수.json"
    reviews = read_json(review_path).get("pages", {}) if review_path.is_file() else {}
    image_review_path = batch / "ID8_전체검수.json"
    image_reviews = read_json(image_review_path).get("pages", {}) if image_review_path.is_file() else {}
    details = []
    rows = []
    for record in records:
        row_num = int(record["sourceRow"])
        key = record["pageKey"]
        page_type = "brand-category" if record["pageType"] == "Brand Category Page" else "brand"
        page = batch / "pages" / key / page_type
        collection = record.get("collectionStatus", "pending")
        results = {}
        notes = []
        if collection not in {"captured", "seeded", "reused"} or not all(
            (page / name).is_file() for name in ("raw.html", "capture-state.json", "response.json")
        ):
            for metric in METRICS:
                results[metric] = verdict("COLLECTION_ERROR", "정상 수집본 없음", {"collectionStatus": collection})
        elif row_num in old_lg:
            results = old_lg[row_num]["results"]
            notes.append("동일 HTML·화면 상태의 기존 LG 24개 AI 검토 판정을 재사용")
        else:
            try:
                audit, _ = audit_page(batch, key, page_type)
                id8 = verdict(audit["status"], audit["reason"], {
                    "selectedImages": audit["top10"], "selectedCount": audit["selectedCount"],
                    "sourceCaptureStateSha256": sha256(page / "capture-state.json"),
                    "sourceRawHtmlSha256": sha256(page / "raw.html"),
                })
                if row_num in {43, 44} and id8["status"] == "REVIEW":
                    id8["reason"] = "Datart 일반 브랜드 페이지 본문의 이미지가 두 차례 수집에서 표시되지 않아, 보이는 공통 매장·수상 아이콘만으로 상위 브랜드 이미지를 정할 수 없음"
                    id8["evidence"]["secondCapture"] = f"retries/datart-brand/pages/{key}/brand/"
                id9, id10 = metadata_checks(record, page)
                results.update({"ID8": id8, "ID9": id9, "ID10": id10})
                review = reviews.get(key)
                review_matches = (isinstance(review, dict)
                                  and review.get("sourceRawHtmlSha256") == sha256(page / "raw.html")
                                  and (not review.get("sourceScreenshotSha256")
                                       or review["sourceScreenshotSha256"] == sha256(page / "screenshot.jpg")))
                for metric in CONTENT:
                    if not isinstance(review, dict) or metric not in review.get("results", {}):
                        reason = "이 URL의 해당 항목에 대한 검토 기록이 없음"
                    elif not review_matches:
                        reason = "해당 항목의 검토 기록이 현재 수집 화면과 일치하지 않음"
                    else:
                        reason = "해당 항목의 검토 기록을 판정에 적용하지 못함"
                    results[metric] = verdict("REVIEW", reason, {
                        "rawHtml": str((page / "raw.html").relative_to(batch)),
                        "captureState": str((page / "capture-state.json").relative_to(batch)),
                    })
                image_review = image_reviews.get(key)
                if isinstance(image_review, dict) and image_review.get("sourceRawHtmlSha256") == sha256(page / "raw.html") and image_review.get("sourceCaptureStateSha256") == sha256(page / "capture-state.json"):
                    result = image_review.get("result", {})
                    if result.get("status") in {"Y", "N"} and result.get("reason"):
                        results["ID8"] = result
                if review_matches:
                    for metric, result in review.get("results", {}).items():
                        if metric in CONTENT and result.get("status") in {"Y", "N", "REVIEW"} and result.get("reason"):
                            results[metric] = result
                if page_type == "brand-category" and results["ID22"]["status"] == "REVIEW":
                    results["ID22"] = product_check(batch, record)
                if page_type == "brand-category" and results["ID21"]["status"] == "REVIEW":
                    nav = sidebar_nav_check(batch, record, sha256(page / "raw.html"))
                    if nav:
                        results["ID21"] = nav
                if page_type == "brand-category":
                    clicked = id21_click_check(batch, record, sha256(page / "raw.html"))
                    if clicked:
                        results["ID21"] = clicked
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
                for metric in METRICS:
                    results[metric] = verdict("COLLECTION_ERROR", f"저장본 검사 실패: {exc}")
        if page_type == "brand":
            for metric in CONTENT:
                results[metric] = verdict("NOT_APPLICABLE", "일반 브랜드 페이지는 이 화면 콘텐츠 진단의 대상이 아님")
        if row_num in conflicts:
            # A duplicated address with different brands is an input identity problem,
            # not evidence that either brand fails the page-content criteria.
            for metric in METRICS[:3] if page_type == "brand" else METRICS:
                results[metric] = verdict("SOURCE_MISMATCH", conflicts[row_num], {"url": record["url"]})
            notes.append(conflicts[row_num])
        detail = {"sourceWorkbookRow": row_num, "pageKey": key, "country": record["country"],
                  "retailer": record["retailer"], "pageType": record["pageType"],
                  "brand": record["brand"], "categoryCode": record["categoryCode"],
                  "subcategory": record["subcategory"], "url": record["url"],
                  "collectionStatus": collection, "notes": notes, "results": results}
        details.append(detail)
        rows.append({"엑셀 행": row_num, "국가": record["country"], "리테일러": record["retailer"],
                     "페이지 유형": record["pageType"], "브랜드": record["brand"],
                     "제품군": record["subcategory"] or "", "URL": record["url"], "수집": collection,
                     **{metric: results[metric]["status"] for metric in METRICS}, "주의": "; ".join(notes)})
    return details, rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--lg-reviewed", type=Path)
    args = parser.parse_args()
    batch = args.batch.resolve()
    details, rows = assess(batch, args.lg_reviewed.resolve() if args.lg_reviewed else None)
    (batch / "전체_URL_판정_진행상태_상세.json").write_text(json.dumps(details, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (batch / "전체_URL_판정_진행상태.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    counts = {metric: Counter(item["results"][metric]["status"] for item in details) for metric in METRICS}
    lines = ["# URL 목록 전체 159개 행 판정 진행상태", "",
             "`Brand_BCP_1차_테스트_URL_목록.xlsx`의 `URL 목록` 탭 기준이다. 이 파일은 모든 URL의 상태를 빠짐없이 표시하되, REVIEW를 최종 Y/N으로 주장하지 않는다.",
             "일반 브랜드 페이지는 ID8·9·10만 대상이며 ID18~23은 비대상이다. 수집 실패와 원본 주소 충돌은 N이 아니다.", "",
             "| 항목 | Y | N | 검토 필요 | 수집 오류 | 원본 충돌 | 비대상 |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for metric, counter in counts.items():
        lines.append("| " + metric + " | " + " | ".join(str(counter[status]) for status in
                     ("Y", "N", "REVIEW", "COLLECTION_ERROR", "SOURCE_MISMATCH", "NOT_APPLICABLE")) + " |")
    lines += ["", "검토 필요는 Y/N 근거가 부족하거나 판정 경계가 정해지지 않은 상태다. 원본 충돌은 URL 목록 자체가 다른 브랜드를 가리키거나 일반 목록으로 이동하는 경우이며, 페이지 콘텐츠의 N으로 취급하지 않는다.",
              "", "## 아직 확정하지 않은 URL", "",
              "| 원본 목록 행 | 리테일러·브랜드 | 항목·상태와 이유 |", "| --- | --- | --- |"]
    for detail in details:
        unresolved = [(metric, result) for metric, result in detail["results"].items()
                      if result["status"] in {"REVIEW", "SOURCE_MISMATCH", "COLLECTION_ERROR"}]
        if not unresolved:
            continue
        grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
        for metric, result in unresolved:
            grouped[(result["status"], result["reason"])].append(metric)
        issues = "; ".join(f"{', '.join(metrics)} {status}: {reason}"
                           for (status, reason), metrics in grouped.items())
        lines.append(f"| {detail['sourceWorkbookRow']} | {detail['retailer']} · {detail['brand']} | {issues} |")
    lines += ["", "각 행의 URL·브랜드·제품군·항목별 상태는 `전체_URL_판정_진행상태.csv`, 판단 이유와 이미지·태그 근거는 `전체_URL_판정_진행상태_상세.json`을 참조한다."]
    (batch / "전체_URL_판정_진행상태.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(batch / "전체_URL_판정_진행상태.md")
    print(json.dumps({metric: dict(counter) for metric, counter in counts.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
