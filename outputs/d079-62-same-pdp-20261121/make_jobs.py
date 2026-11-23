"""v8.1에서 대상 124행, 대조군, 주소 글자 실험 주소를 골라 jobs.json 으로 쓴다.
접속 후 URL은 글자 하나도 바꾸지 않는다(주소 글자 실험의 바꾼 주소만 예외로 새로 만든다)."""
import csv, json, re, hashlib
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from urllib.parse import urlsplit

OUT = Path(__file__).resolve().parent
SRC = OUT.parents[1] / "pdp 모수 추출/최종_20261029/PDP모수_공유용_v8.1_1P3P구분추가_25개국_35개리테일러_전체판정_55129행_20261118.csv"

def tail(u):
    n = urlsplit(u).path.rstrip("/").rsplit("/", 1)[-1]
    return n

rows = list(csv.DictReader(SRC.open(encoding="utf-8-sig", newline="")))
by = {r["행번호"]: r for r in rows}
assert len(rows) == len(by) == 55129
exc = [r for r in rows if r["제외단계"] == "④중복" and "주소의 상품 번호 같음" in r["제외사유"]]
cnt = Counter(r["리테일러"] for r in exc)
assert cnt == {"COSTCO": 43, "FALABELLA": 19}, cnt
pairs = []
for i, b in enumerate(exc, 1):
    m = re.findall(r"대표 행 (\d+)", b["제외사유"]); assert len(m) == 1
    a = by[m[0]]
    assert a["모수 포함 여부"] == "포함" and b["모수 포함 여부"] == "제외"
    assert a["리테일러"] == b["리테일러"]
    pairs.append({"pair": i, "retailer": a["리테일러"], "rep": a["행번호"], "dup": b["행번호"]})
ids = [x for p in pairs for x in (p["rep"], p["dup"])]
assert len(set(ids)) == 124
# 대조군: 같은 리테일러, 같은 제품코드, 주소 끝 상품 번호가 다르고 둘 다 포함 (대상 124행 제외, 원본 순서로 처음 3쌍)
controls = []
for ret in ("COSTCO", "FALABELLA"):
    g = defaultdict(list)
    for r in rows:
        if r["리테일러"] == ret and r["모수 포함 여부"] == "포함" and r["제품코드"].strip() and r["행번호"] not in ids and tail(r["접속 후 URL"]).isdigit():
            g[(r["국가"], r["브랜드"], r["제품코드"])].append(r)
    n = 0
    for grp in g.values():
        pr = next(((a, b) for a, b in combinations(grp, 2) if tail(a["접속 후 URL"]) != tail(b["접속 후 URL"])), None)
        if pr:
            controls.append({"retailer": ret, "a": pr[0]["행번호"], "b": pr[1]["행번호"]}); n += 1
        if n == 3: break
# 주소 글자 실험: 리테일러별 처음, 가운데, 끝 쌍의 대표 행
slug = []
for ret in ("COSTCO", "FALABELLA"):
    ps = [p for p in pairs if p["retailer"] == ret]
    for p in (ps[0], ps[len(ps)//2], ps[-1]):
        u = by[p["rep"]]["접속 후 URL"]
        sp = urlsplit(u); parts = sp.path.split("/")
        parts[-2] = "pdp-study-example"
        alt = u.replace(sp.path, "/".join(parts))
        slug.append({"retailer": ret, "row": p["rep"], "orig": u, "alt": alt})
jobs = {"source_sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(), "pairs": pairs, "controls": controls, "slug": slug,
        "urls": {i: by[i]["접속 후 URL"] for i in set(ids) | {c[k] for c in controls for k in ("a", "b")}}}
(OUT / "jobs.json").write_text(json.dumps(jobs, ensure_ascii=False, indent=1), encoding="utf-8")
print("pairs", len(pairs), dict(cnt), "controls", len(controls), "slug", len(slug))
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for p in pairs:
            if p["retailer"] == sys.argv[1]:
                print(p["pair"], p["rep"], by[p["rep"]]["접속 후 URL"]); print(p["pair"], p["dup"], by[p["dup"]]["접속 후 URL"])
        for c in controls:
            if c["retailer"] == sys.argv[1]: print("C", c["a"], by[c["a"]]["접속 후 URL"]); print("C", c["b"], by[c["b"]]["접속 후 URL"])
        for s in slug:
            if s["retailer"] == sys.argv[1]: print("S", s["row"], s["alt"])
