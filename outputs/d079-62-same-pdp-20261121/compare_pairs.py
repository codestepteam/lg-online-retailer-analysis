"""extracted/ 의 값을 쌍끼리 글자 단위로 비교한다. 글자가 완전히 같아야 '일치'다."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_values import FIELDS, NONE

HERE = Path(__file__).resolve().parent
EXT = HERE / "extracted"

def load(name):
    f = EXT / f"{name}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None

def problems(e):
    """값을 읽을 수 없는 수집본인지 본다. 이유 목록을 돌려준다."""
    out = []
    m, x = e["meta"], e["extra"]
    if m["http_status"] != 200: out.append(f"응답 상태 {m['http_status']}")
    if not x.get("is_product_page"): out.append("상품 화면 아님")
    if m["final_url"] != m["requested_url"]: out.append("주소가 바뀜")
    if "vis_start visible" not in m["notes"] or "vis_end visible" not in m["notes"]: out.append("탭이 가려진 상태에서 수집")
    if x.get("f08_expects_syndigo") and not x.get("f08_has_syndigo"): out.append("제조사 설명이 뜨지 않음")
    if e["values"]["f11"] == NONE and x.get("price_unavailable_notice") is not None and e["values"]["f13"].find("Add") >= 0: out.append("가격이 뜨지 않음")
    return out

def compare(a, b):
    diff = [k for k, _ in FIELDS if a["values"][k] != b["values"][k]]
    cond = []
    if a["meta"]["viewport"] != b["meta"]["viewport"]: cond.append("화면 크기 다름")
    return diff, cond

if __name__ == "__main__":
    jobs = json.loads((HERE / "jobs.json").read_text(encoding="utf-8"))
    kind = sys.argv[1] if len(sys.argv) > 1 else "m"
    n = 0
    for p in jobs["pairs"]:
        a, b = load(f"{kind}-{p['rep']}"), load(f"{kind}-{p['dup']}")
        if not a or not b: continue
        n += 1
        diff, cond = compare(a, b)
        pa, pb = problems(a), problems(b)
        if diff or cond or pa or pb:
            print(p["pair"], p["rep"], p["dup"], "다른 항목:", diff, cond, "| 대표 행 문제:", pa, "| 중복제거 행 문제:", pb)
    print("비교한 쌍", n)
