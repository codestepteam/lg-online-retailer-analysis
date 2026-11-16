"""Shared PDP v7 -> v8: replace MomoShop with the fixed OSM query and point Darty rows at original URLs.

MomoShop: 1,936 products from the fixed OSM query (2026-10-26, product-number grouping,
brand-prefix match). Judgments come from, in order: 11-12 search run, 11-03 run, the
2026-11-16 check of the 129 never-judged products. Store-in-store (/TP/) products keep
their v7 seller judgment, else the 11-12 one, else the /TP/ rule.
Darty: the 152 rows whose v7 URL was an outside-seller offer (?ofmp=) take the original
product URL and the 2026-11-13 recheck judgment. All other rows are copied from v7 as is.
"""

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
EVID = HERE / "판정근거/v8_MomoShopDarty_OSM쿼리수정교체"
V7 = HERE / "PDP모수_공유용_v7_SharafDG직판재조사교체_25개국_35개리테일러_전체판정_54443행_20261110.csv"
OSM = EVID / "momo_pid_detail.jsonl"
NEW129 = EVID / "momo_judge129_20261116.json"
S12 = ROOT / "outputs/momoshop-search-pdp-20261112-4ab49c5f/momoshop_all_judgments_26_columns.csv"
C03 = ROOT / "outputs/momoshop-final-pdp-20261103-51e01084/candidate_judgments.csv"
DARTY = ROOT / "outputs/darty-original-url-20261113/darty_원래주소_152개_확인결과_20261113.csv"
TAG = "D142"
OSM_FILE = "momo_pid_detail.jsonl (OSM 쿼리 수정, 2026-10-26 자료)"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def pid(url):
    match = (re.search(r"goodsDetail/(TP\d+)", url, re.I) or re.search(r"/product/(\d+)", url)
             or re.search(r"i_code=(\d+)", url))
    return match.group(1).upper() if match else None


def memo(*parts):
    return "; ".join(part for part in parts if part)


def seller_fields(seller, kind, basis):
    """11-12/11-03 seller wording -> v7 MomoShop wording (직판 / 외부판매자)."""
    if kind == "직판 추정" or seller == "momo (추정)":
        return "momo", "직판", f"[추정] {basis}" if basis and not basis.startswith("[추정]") else basis
    if kind == "입점 상점":
        return seller, "외부판매자", basis
    return seller, kind, basis


def osm_row(template, rep, number):
    row = {key: "" for key in template}
    row.update({
        "행번호": number, "흐름": "OSM", "국가": "Taiwan", "리테일러": "MOMOSHOP", "제품군": rep["DIV"],
        "브랜드": rep["BRAND_NORM"], "제품코드": (rep["MPC"] or "").upper(), "OSM브랜드": rep["BRAND_RAW"],
        "상품명": rep["PRODUCT_DESC"] or "", "확인 요청 URL": rep["URL"], "원본 상품 URL": rep["URL"],
        "기준일": "2026-10-26", "출처파일": OSM_FILE,
    })
    return row


def main():
    columns, rows = read_csv(V7)
    assert len(columns) == 26 and len(rows) == 54_443
    assert len({row["행번호"] for row in rows}) == len(rows)
    next_number = max(int(row["행번호"]) for row in rows) + 1
    v7_momo = [row for row in rows if row["리테일러"] == "MOMOSHOP"]
    assert len(v7_momo) == 1_250
    v7_by_pid = {pid(row["원본 상품 URL"]): row for row in v7_momo}
    assert len(v7_by_pid) == 1_250 and None not in v7_by_pid

    osm = [json.loads(line) for line in OSM.open()]
    assert len(osm) == 1_936 and len({r["PID"].upper() for r in osm}) == 1_936
    _, s12 = read_csv(S12)
    s12_by_pid = {}
    for row in s12:
        key = pid(row["원본 상품 URL"])
        if key not in s12_by_pid or s12_by_pid[key]["제외단계"] == "④중복":
            s12_by_pid[key] = row
    _, c03 = read_csv(C03)
    c03_by_pid = {r["candidate_key"][6:]: r for r in c03 if r["candidate_key"].startswith("goods:")}
    new129 = json.loads(NEW129.read_text())
    assert len(new129) == 129

    momo, source = [], Counter()
    for rep in osm:
        key = rep["PID"].upper()
        old = v7_by_pid.get(key)
        number = old["행번호"] if old else str(next_number)
        if not old:
            next_number += 1
        if rep["URL_TYPE"] == "TP":
            if old:
                row = dict(old)
                row["메모"] = memo(row["메모"], f"{TAG}: OSM 쿼리 수정 후에도 같은 상품번호, v7 판정 유지")
                source["TP v7"] += 1
            else:
                row = osm_row(columns, rep, number)
                done = s12_by_pid.get(key)
                if done:
                    seller, kind, basis = seller_fields(done["판매자"], done["판매자구분"], done["판매자근거"])
                    row.update({"모수 포함 여부": "제외", "제외단계": "③리리부",
                                "제외사유": done["제외사유"] if done["제외단계"] == "③리리부" else "mo店+ 입점 상점 상품(/TP/ 경로)",
                                "페이지 접속 확인 결과": done["페이지 접속 확인 결과"], "접속 후 URL": done["접속 후 URL"],
                                "판매자": seller, "판매자구분": kind, "판매자근거": basis,
                                "메모": f"{TAG}: 판정은 2026-11-12 검색어 수집 판정을 상품번호로 붙임"})
                    source["TP 11-12"] += 1
                else:
                    row.update({"모수 포함 여부": "제외", "제외단계": "③리리부", "제외사유": "mo店+ 입점 상점 상품(/TP/ 경로)",
                                "판매자구분": "외부판매자", "판매자근거": "주소가 /TP/ 입점 상점 경로",
                                "메모": f"{TAG}: 이전 판정 없음, /TP/ 경로 규칙으로 제외(상세 페이지 미확인)"})
                    source["TP 경로 규칙"] += 1
            momo.append(row)
            continue

        row = osm_row(columns, rep, number)
        if key in s12_by_pid:
            done = s12_by_pid[key]
            seller, kind, basis = seller_fields(done["판매자"], done["판매자구분"], done["판매자근거"])
            row.update({key2: done[key2] for key2 in ("모수 포함 여부", "제외단계", "제외사유", "페이지 접속 확인 결과", "접속 후 URL")})
            row.update({"판매자": seller, "판매자구분": kind, "판매자근거": basis,
                        "메모": memo(done["메모"], f"{TAG}: 판정은 2026-11-12 검색어 수집 판정을 상품번호로 붙임")})
            if row["모수 포함 여부"] == "검토 필요":
                row.update({"모수 포함 여부": "제외",
                            "메모": memo(row["메모"], "D134: 품절 검토 대상은 제외")})
            source["일반 11-12"] += 1
        elif key in c03_by_pid:
            done = c03_by_pid[key]
            seller, kind, basis = seller_fields(done["seller"], "", done["seller_basis"])
            row.update({"모수 포함 여부": done["decision"], "제외단계": done["exclusion_stage"], "제외사유": done["reason"],
                        "페이지 접속 확인 결과": "정상" if done["decision"] == "포함" else "",
                        "접속 후 URL": done["final_url"], "판매자": seller, "판매자구분": kind, "판매자근거": basis,
                        "메모": f"{TAG}: 판정은 2026-11-03 MomoShop 판정을 상품번호로 붙임"})
            assert done["decision"] in ("포함", "제외"), key
            source["일반 11-03"] += 1
        else:
            done = new129[key]
            included = done["decision"] == "포함"
            row.update({"모수 포함 여부": done["decision"], "제외단계": done["stage"], "제외사유": done["reason"],
                        "페이지 접속 확인 결과": "페이지 없음" if done["stage"] == "④페이지없음" else "정상",
                        "접속 후 URL": f"https://www.momoshop.com.tw/product/{key}",
                        "판매자": "momo" if included or done["seller"] else "",
                        "판매자구분": "직판" if included or done["seller"] else "",
                        "판매자근거": f"[추정] {done['seller_basis']}" if done["seller_basis"] else "",
                        "메모": memo(f"{TAG}: 2026-11-16 상세 페이지 새로 확인", done["memo"])})
            source["일반 11-16 신규"] += 1
        if old:
            source["  (그중 v7 행번호 재사용)"] += 1
        momo.append(row)

    dropped = set(v7_by_pid) - {r["PID"].upper() for r in osm}

    # Darty: original product URL + recheck judgment.
    _, darty = read_csv(DARTY)
    assert len(darty) == 152
    by_url = {row["원본 상품 URL"]: row for row in rows if row["리테일러"] == "DARTY"}
    for check in darty:
        row = by_url[check["지금 v7이 쓰는 URL (ofmp 붙은 주소)"]]
        url = check["확인할 URL (원래 상품 주소)"]
        kind = check["판매자 구분 (직판/외부판매자/리퍼·중고/확인불가)"]
        seller = check["판매자 (확인 결과)"]
        note = check["메모"]
        if check["판정 (포함/제외)"] == "포함":
            stage, reason = "", ""
        elif kind == "외부판매자":
            stage, reason = "③리리부", f"외부 판매자 ({seller})"
        elif kind == "리퍼·중고":
            stage, reason = "③리리부", f"리퍼·중고 ({seller})"
        elif check["재고 (있음/품절)"] == "품절":
            stage, reason = "③리리부", "외부 판매자(Vendu et installé par Darty 없음, 품절로 판매자 표시 없음)"
        else:
            stage, reason = "④영구품절", "판매 종료 (상품 페이지 없음)"
        row.update({"확인 요청 URL": url, "원본 상품 URL": url, "접속 후 URL": url,
                    "모수 포함 여부": check["판정 (포함/제외)"], "제외단계": stage, "제외사유": reason,
                    "페이지 접속 확인 결과": "정상", "판매자": seller, "판매자구분": kind,
                    "판매자근거": f"2026-11-13 원래 상품 주소 화면 확인: {note}",
                    "메모": f"{TAG}: v7 주소가 외부 판매자 상품 주소(?ofmp=)라 원래 상품 주소로 교체 후 재판정"})

    start = next(i for i, row in enumerate(rows) if row["리테일러"] == "MOMOSHOP")
    out = [row for row in rows if row["리테일러"] != "MOMOSHOP"]
    out[start:start] = momo
    assert len({row["행번호"] for row in out}) == len(out)
    status = Counter(r["모수 포함 여부"] for r in out)
    assert set(status) == {"포함", "제외"}, status
    target = HERE / f"PDP모수_공유용_v8_MomoShopDarty_OSM쿼리수정교체_25개국_35개리테일러_전체판정_{len(out)}행_20261116.csv"
    assert not target.exists(), f"v8 already exists: {target}"
    with target.open("x", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(out)
    print(f"created {target.name}: {len(out)} rows")
    print("momo sources", dict(source), "| v7 momo products not in fixed OSM:", len(dropped))
    print("status", dict(status))


if __name__ == "__main__":
    main()
