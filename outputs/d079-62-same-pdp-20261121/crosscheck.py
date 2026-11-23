"""다른 도구 재확인과 반복 수집 비교를 계산해 crosscheck.json 으로 쓴다.
- 재확인: 수집 전에 난수(시드 20261121)로 고른 10쌍을, 본 수집에 쓰지 않은 도구의 수집본(b- = 앱 내장 브라우저, x- = 별도 Chrome)으로 다시 판정한다.
- 반복: 시험 3쌍을 같은 도구로 두 번 수집한 값(m- 와 p2-, Falabella는 z1- 과 z2-)이 같은지 본다.
"""
import json, random, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import judge as J
from extract_values import FIELDS
LABEL = dict(FIELDS)
jobs = json.loads((HERE / "jobs.json").read_text(encoding="utf-8"))
picks = sorted(random.Random(20261121).sample([p["pair"] for p in jobs["pairs"]], 10))
out = {"picks": picks, "cross": [], "repeat": []}
for p in jobs["pairs"]:
    if p["pair"] not in picks: continue
    main = J.judge_pair(p["rep"], p["dup"])
    kind = "b" if p["retailer"] == "COSTCO" else "m"  # Falabella는 앞서 웹 수집 서비스로 받은 수집본(m-)이 다른 도구 자료다
    a, b = J.load(f"{kind}-{p['rep']}"), J.load(f"{kind}-{p['dup']}")
    rec = {"pair": p["pair"], "retailer": p["retailer"], "rep": p["rep"], "dup": p["dup"], "main": main["verdict"], "other_tool": "앱 내장 브라우저" if kind == "b" else "웹 수집 서비스(Zyte)"}
    if a is None or b is None:
        rec["other"] = "수집본 없음"
    elif J.problems(a) or J.problems(b):
        rec["other"] = "확인 못 함"; rec["why"] = "; ".join(J.problems(a) + J.problems(b))[:200]
    else:
        d = [k for k, _ in FIELDS if a["values"][k] != b["values"][k]]
        rec["other"] = "같음" if not d else "다름"; rec["diff"] = [LABEL[k] for k in d]
        # 도구 사이에 값 자체가 같은지도 본다(참고)
        m = J.load(f"{J.MAIN}-{p['rep']}")
        if not J.problems(m): rec["tool_value_diff"] = [LABEL[k] for k, _ in FIELDS if a["values"][k] != m["values"][k]]
    rec["agree"] = rec["other"] == rec["main"]
    out["cross"].append(rec)
for n in (1, 12, 43):
    p = next(x for x in jobs["pairs"] if x["pair"] == n)
    for row in (p["rep"], p["dup"]):
        a, b = J.load(f"m-{row}"), J.load(f"p2-{row}")
        out["repeat"].append({"retailer": "COSTCO", "row": row, "diff": [LABEL[k] for k, _ in FIELDS if a["values"][k] != b["values"][k]]})
    pa = J.judge_pair(p["rep"], p["dup"], kind="p2", recheck="zz")
    out["repeat"].append({"retailer": "COSTCO", "pair": n, "second_verdict": pa["verdict"], "second_diff": [LABEL[k] for k in pa["diff"]]})
for row in ("8616", "8627", "8668", "8690", "8897", "8911"):
    a, b = J.load(f"z1-{row}"), J.load(f"z2-{row}")
    out["repeat"].append({"retailer": "FALABELLA", "row": row, "diff": [LABEL[k] for k, _ in FIELDS if a["values"][k] != b["values"][k]]})
(HERE / "crosscheck.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for r in out["cross"]: print(r)
for r in out["repeat"]: print(r)
