"""판정, values.csv, 엑셀, 두레이 글 초안을 한 번에 만든다.

실행: python make_all.py
앞 단계: extract_values.py (raw 원본 → extracted 값)
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from extract_values import FIELDS, NONE  # noqa: E402
import judge as J  # noqa: E402
import build_excel as B  # noqa: E402

LABEL = dict(FIELDS)


def main():
    jobs = json.loads((HERE / "jobs.json").read_text(encoding="utf-8"))
    src = {r["행번호"]: r for r in csv.DictReader(J.SRC.open(encoding="utf-8-sig", newline=""))}
    need = []

    # 1) 62쌍 판정
    records, verdicts = [], []
    for p in jobs["pairs"]:
        res = J.judge_pair(p["rep"], p["dup"])
        need += res["need"]
        verdicts.append((p, res))
        ua, ub = src[p["rep"]]["접속 후 URL"], src[p["dup"]]["접속 후 URL"]
        records.append(J.row_record(src[p["rep"]], p["pair"], "대표 행", res["a"], res["b"], res, ub, res["ra"], res["rb"]))
        records.append(J.row_record(src[p["dup"]], p["pair"], "중복제거 행", res["b"], res["a"], res, ua, res["rb"], res["ra"]))
    with (HERE / "values.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)

    tally = Counter(res["verdict"] for _, res in verdicts)
    by_ret = Counter((p["retailer"], res["verdict"]) for p, res in verdicts)
    result = {"tally": dict(tally), "by_retailer": {f"{k[0]}|{k[1]}": v for k, v in by_ret.items()}, "need": need,
              "not_same": [{"pair": p["pair"], "retailer": p["retailer"], "rep": p["rep"], "dup": p["dup"], "verdict": res["verdict"],
                            "diff": [LABEL[k] for k in res["diff"]], "reason": res["reason"]} for p, res in verdicts if res["verdict"] != "같음"]}
    (HERE / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "not_same"}, ensure_ascii=False))
    for n in result["not_same"]:
        print("  ", n)
    if "--excel" in sys.argv:
        import texts as T
        summary, draft = T.compose(result, records)
        B.TEXTS.update(T.STATIC)
        postals = sorted({(J.load(f"{J.MAIN}-{p['rep']}") or {}).get("extra", {}).get("postal", "").replace("Delivery Location ", "") for p in jobs["pairs"] if p["retailer"] == "COSTCO"} - {""})
        B.TEXTS["method_intro"] = [[x.replace("COSTCO_POSTAL", "우편번호 " + ", ".join(postals)) for x in line] for line in B.TEXTS["method_intro"]]
        B.build(records, summary)
        B.DRAFT.write_text(draft, encoding="utf-8")
        print("엑셀", B.XLSX.name, round(B.XLSX.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
