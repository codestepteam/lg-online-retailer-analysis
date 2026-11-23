"""extracted/ 의 값으로 쌍 판정을 하고 values.csv 를 쓴다. 엑셀과 두레이 글 초안은 이 결과만 읽어 만든다.

판정 (쌍마다 하나)
- 확인 못 함: 한쪽이라도 상품 화면을 읽지 못함
- 같음: 항목 1~14의 글자가 모두 같음
- 다름: 하나라도 다름
평점과 리뷰 수(9), 표시 가격(10), 구매 가능 상태(12)는 시간이 지나며 바뀔 수 있어,
처음 비교에서 다르면 두 주소를 바로 다시 수집(r- 작업)해 두 번째 값으로 판정하고 두 번의 값을 모두 남긴다.
"""
import csv
import difflib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from extract_values import FIELDS, NONE  # noqa: E402

EXT = HERE / "extracted"
SRC = HERE.parents[1] / "pdp 모수 추출/최종_20261029/PDP모수_공유용_v8.1_1P3P구분추가_25개국_35개리테일러_전체판정_55129행_20261118.csv"
VOLATILE = ("f10", "f11", "f13")
LONG = ("f06", "f08", "f09")
BOTH_NONE = "양쪽 모두 없음"
# 사이트가 "Product not available!" 안내만 보여 준 행은 124행 시트에 '확인 못 함' 대신 이 말을 적는다(11-21 사용자 요청).
NA = "Product not available"


def drop_issue_no(reason):
    """엑셀에 적는 제외사유. v8.1 글에서 내부 이슈 번호(", #119")를 떼고 "상품 번호"를 "PDP 식별자"로 바꾼다(11-21 사용자 요청). 나머지 글자는 v8.1 그대로다."""
    return reason.replace(", #119)", ")").replace("주소의 상품 번호 같음", "주소의 PDP 식별자 같음")


def unread_label(e):
    """값을 읽지 못한 행에 적을 말."""
    return NA if any("Product not available" in x for x in problems(e)) else "확인 못 함"
KST = timezone(timedelta(hours=9))


def load(name):
    f = EXT / f"{name}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def kst(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(KST).strftime("%Y-%m-%d %H:%M:%S")


def problems(e):
    """값을 읽을 수 없는 수집본이면 그 이유를 돌려준다."""
    if e is None:
        return ["수집본 없음"]
    out, m, x = [], e["meta"], e["extra"]
    if m["http_status"] != 200:
        out.append(f"응답 상태 {m['http_status']}")
    if not x.get("is_product_page"):
        note = x.get("page_notice") or m.get("title") or ""
        note = {"Product not available!": "Product not available! (상품을 볼 수 없음)"}.get(note, note)
        out.append("상품 화면이 열리지 않음" + (f" (화면에 나온 글: {note})" if note else ""))
    return out


def quality(e):
    """판정 전에 다시 수집해야 하는 수집 상태 문제."""
    out, m, x = [], e["meta"], e["extra"]
    if m["final_url"] != m["requested_url"]:
        out.append("주소가 바뀜")
    if "vis_start visible" not in m["notes"] or "vis_end visible" not in m["notes"]:
        out.append("탭이 가려진 상태")
    if x.get("f08_expects_syndigo") and not x.get("f08_has_syndigo"):
        out.append("제조사 설명이 뜨지 않음")
    if x.get("f08_frame_read") is False:
        out.append("제조사 설명 문서를 아직 읽지 못함")
    if x.get("f08_vendor") == "FlixMedia" and not x.get("f08_flix_chars"):
        out.append("제조사 설명(FlixMedia)이 뜨지 않음")
    if "imgs_pending 0" not in m["notes"]:
        out.append("사진이 다 뜨기 전에 찍힘")
    return out


def slug_of(url):
    parts = urlsplit(url).path.rstrip("/").split("/")
    return parts[-2], parts[-1]


def slug_diff(a, b):
    """두 주소의 상품명 부분에서 서로 다른 낱말을 각각 돌려준다."""
    sa, sb = slug_of(a)[0], slug_of(b)[0]

    def expand(s, i, j):
        while i > 0 and s[i - 1] != "-":
            i -= 1
        while j < len(s) and s[j] != "-":
            j += 1
        return i, j

    ra, rb = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        a1, a2 = expand(sa, i1, i2)
        b1, b2 = expand(sb, j1, j2)
        ra.append((a1, a2))
        rb.append((b1, b2))

    def merge(s, rs):
        out, cur = [], None
        for x, y in sorted(rs):
            if cur and x <= cur[1] + 1:
                cur = (cur[0], max(cur[1], y))
            else:
                if cur:
                    out.append(cur)
                cur = (x, y)
        if cur:
            out.append(cur)
        return ", ".join(s[x:y] for x, y in out) or "(다른 글자 없음)"

    return merge(sa, ra), merge(sb, rb)


def display(key, e, same, mate_none):
    """엑셀 칸에 적을 글. 긴 값은 개수와 일치 여부만 적는다."""
    v, x = e["values"][key], e["extra"]
    if v == NONE:
        return BOTH_NONE if mate_none else NONE
    tail = "쌍 일치" if same else "쌍 불일치"
    if key == "f06":
        return f"사진 {x.get('f06_photos', 0)}장, 영상 {x.get('f06_videos', 0)}개 (사진 경로와 순서 {tail})"
    if key == "f08":
        return f"글 {x.get('f08_chars', 0):,}자, 본문 속 그림 {x.get('f08_imgs', 0)}개 (글 전체와 그림 목록 {tail})"
    if key == "f09":
        return f"{x.get('f09_rows', 0)}항목 (항목 이름과 값 전체 {tail})"
    return v.replace("\n", " / ")


MAIN = "f"  # 본 수집 작업 이름의 앞 글자. f = 전체 페이지 그림과 함께 다시 수집한 것(11-21 두 번째 수집)


def judge_pair(a_name, b_name, kind=MAIN, recheck="r"):
    ea, eb = load(f"{kind}-{a_name}"), load(f"{kind}-{b_name}")
    res = {"a": ea, "b": eb, "ra": None, "rb": None, "need": [], "diff": [], "first_diff": [], "reason": ""}
    pa, pb = problems(ea), problems(eb)
    if pa or pb:
        res["verdict"] = "확인 못 함"
        res["reason"] = "; ".join(([f"행 {a_name}: {', '.join(pa)}"] if pa else []) + ([f"행 {b_name}: {', '.join(pb)}"] if pb else []))
        # 배송지를 바꿔 다시 연 기록(v-, v2- 작업)이 있고 그때도 상품 화면이 아니었으면 그 사실을 덧붙인다.
        retry = [(k, z) for k, z in (("v", "V6B 1A1"), ("v2", "T2P 1J9")) if load(f"{k}-{a_name}") and load(f"{k}-{b_name}")
                 and problems(load(f"{k}-{a_name}")) and problems(load(f"{k}-{b_name}"))]
        if retry:
            res["reason"] += "; 배송지 우편번호를 " + ", ".join(z for _, z in retry) + "(으)로 바꿔 두 주소를 다시 열어도 같은 안내"
        return res
    for n, e in ((a_name, ea), (b_name, eb)):
        q = quality(e)
        if q:
            res["need"].append(f"{kind}-{n} 다시 수집 필요: {', '.join(q)}")
    if ea["meta"]["viewport"] != eb["meta"]["viewport"]:
        res["need"].append(f"{kind}-{a_name}/{b_name} 화면 크기가 서로 다름")
    diff = [k for k, _ in FIELDS if ea["values"][k] != eb["values"][k]]
    res["first_diff"] = list(diff)
    if any(k in VOLATILE for k in diff):
        ra, rb = load(f"{recheck}-{a_name}"), load(f"{recheck}-{b_name}")
        if ra is None or rb is None or problems(ra) or problems(rb):
            res["need"].append(f"{recheck}-{a_name}, {recheck}-{b_name} 재수집 필요 (9, 10, 12 중 다른 항목)")
        else:
            res["ra"], res["rb"] = ra, rb
            diff = [k for k in diff if k not in VOLATILE] + [k for k in VOLATILE if ra["values"][k] != rb["values"][k]]
            diff.sort()
    res["diff"] = diff
    res["verdict"] = "같음" if not diff else "다름"
    return res


LABEL = dict(FIELDS)


def row_record(src_row, pair_no, role, e, mate, res, other_url, recheck_e=None, recheck_mate=None):
    rec = {
        "쌍 번호": pair_no, "리테일러": src_row["리테일러"], "국가": src_row["국가"], "브랜드": src_row["브랜드"],
        "제품코드": src_row["제품코드"], "v8.1 행번호": src_row["행번호"], "모수 포함 여부": src_row["모수 포함 여부"],
        "제외사유": drop_issue_no(src_row["제외사유"]), "접속 후 URL": src_row["접속 후 URL"],
    }
    mine, _ = slug_diff(src_row["접속 후 URL"], other_url)
    rec["주소에서 서로 다른 부분"] = mine
    rec["주소 끝 PDP 식별자"] = slug_of(src_row["접속 후 URL"])[1]
    for k, label in FIELDS:
        if e is None or problems(e):
            rec[label] = unread_label(e)
            continue
        if mate is None or problems(mate):
            same, mate_none = False, False
            txt = display(k, e, same, mate_none).replace(" (사진 경로와 순서 쌍 불일치)", "").replace(" (글 전체와 그림 목록 쌍 불일치)", "").replace(" (항목 이름과 값 전체 쌍 불일치)", "")
        else:
            same = e["values"][k] == mate["values"][k]
            txt = display(k, e, same, mate["values"][k] == NONE)
        if k in VOLATILE and recheck_e is not None and (e["values"][k] != mate["values"][k]):
            txt = f"1차: {txt} / 2차: {display(k, recheck_e, True, recheck_mate['values'][k] == NONE)}"
        rec[label] = txt
    ok = e is not None and not problems(e)
    rec["수집 시각(한국 시각)"] = kst(e["meta"]["collected_utc"]) if e is not None else ""
    if recheck_e is not None:
        rec["수집 시각(한국 시각)"] += f" / 2차 {kst(recheck_e['meta']['collected_utc'])}"
    rec["쌍 판정"] = res["verdict"]
    if res["verdict"] == "확인 못 함" and all(unread_label(x) == NA for x in (res["a"], res["b"])):
        rec["쌍 판정"] = NA
    if res["verdict"] == "다름":
        rec["다른 항목"] = ", ".join(LABEL[k] for k in res["diff"])
    elif res["verdict"] == "확인 못 함":
        rec["다른 항목"] = res["reason"]
    else:
        rec["다른 항목"] = ""
        if res["ra"] is not None:
            rec["다른 항목"] = "없음 (1차에서 다르게 읽힌 " + ", ".join(LABEL[k] for k in res["first_diff"] if k in VOLATILE) + " 항목은 바로 다시 수집해 같음을 확인)"
    for k, label in FIELDS:
        rec[f"원문 {label}"] = e["values"][k] if ok else ""
        if recheck_e is not None and k in VOLATILE:
            rec[f"원문 {label}"] += f"\n[2차] {recheck_e['values'][k]}"
    rec["역할"] = role
    rec["도착 주소"] = e["meta"]["final_url"] if e is not None else ""
    rec["응답 상태"] = e["meta"]["http_status"] if e is not None else ""
    rec["화면 크기"] = f"{e['meta']['viewport']['w']}x{e['meta']['viewport']['h']}" if e is not None else ""
    rec["원본 자료 파일"] = f"raw/{e['meta']['name']}.json" if e is not None else ""
    rec["스크린샷 파일"] = f"screenshots/{e['meta']['name']}.jpg" if e is not None else ""
    return rec


def main():
    jobs = json.loads((HERE / "jobs.json").read_text(encoding="utf-8"))
    src = {r["행번호"]: r for r in csv.DictReader(SRC.open(encoding="utf-8-sig", newline=""))}
    only = sys.argv[1] if len(sys.argv) > 1 else None
    records, need, tally = [], [], {}
    for p in jobs["pairs"]:
        if only and p["retailer"] != only:
            continue
        res = judge_pair(p["rep"], p["dup"])
        need += res["need"]
        tally[res["verdict"]] = tally.get(res["verdict"], 0) + 1
        ua, ub = src[p["rep"]]["접속 후 URL"], src[p["dup"]]["접속 후 URL"]
        records.append(row_record(src[p["rep"]], p["pair"], "대표 행", res["a"], res["b"], res, ub, res["ra"], res["rb"]))
        records.append(row_record(src[p["dup"]], p["pair"], "중복제거 행", res["b"], res["a"], res, ua, res["rb"], res["ra"]))
    with (HERE / "values.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)
    print("쌍 판정:", tally, "| 행", len(records))
    for n in need:
        print("  필요:", n)
    for r in records:
        if r["쌍 판정"] != "같음" and r["역할"] == "대표 행":
            print("  ", r["쌍 번호"], r["v8.1 행번호"], r["쌍 판정"], r["다른 항목"])


if __name__ == "__main__":
    main()
