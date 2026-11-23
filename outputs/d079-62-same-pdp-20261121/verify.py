"""끝 검증. 하나라도 어긋나면 '실패'를 출력한다.

검증 2: 엑셀 124행 시트의 모든 칸 = values.csv = v8.1 원본, 그리고 raw 원본에서 다시 뽑은 값 = values.csv 원문
검증 3: 행 수 124, 쌍 수 62, 쌍마다 포함 1행과 중복제거 1행, 행번호 중복 없음, 접속 후 URL이 v8.1과 글자까지 같음
검증 4(자동 부분): 스크린샷 124장이 있고, 그림 속 글자에서 그 행의 상품명과 상품 번호가 읽힘
검증 6: 판정 합계 62, 요약 시트와 두레이 글 초안의 숫자가 124행 시트와 같음
"""
import csv, gzip, json, re, subprocess, sys
from collections import Counter
from pathlib import Path
from openpyxl import load_workbook

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import extract_values as X
import judge as J
import build_excel as B

fails = []
def check(name, ok, detail=""):
    print(("통과" if ok else "실패"), "|", name, "|", detail)
    if not ok: fails.append(name)

def raw_payload(name):
    for d in ("raw", "raw2"):
        f = HERE / d / f"{name}.json.gz"
        if f.exists(): return json.loads(gzip.open(f, "rt", encoding="utf-8").read())
        f = HERE / d / f"{name}.json"
        if f.exists(): return json.loads(f.read_text(encoding="utf-8"))
    return None

def main():
    src = {r["행번호"]: r for r in csv.DictReader(J.SRC.open(encoding="utf-8-sig", newline=""))}
    vals = list(csv.DictReader((HERE / "values.csv").open(encoding="utf-8-sig", newline="")))
    wb = load_workbook(B.XLSX)
    ws = wb["124행"]
    head = [c.value for c in ws[1]]
    rows = [[c for c in r] for r in ws.iter_rows(min_row=2)]

    # 검증 3
    check("3 행 수 124", len(rows) == 124 and len(vals) == 124, f"엑셀 {len(rows)}, values.csv {len(vals)}")
    ids = [str(r[head.index("v8.1 행번호")].value) for r in rows]
    check("3 행번호 중복 없음", len(set(ids)) == len(ids))
    pairs = Counter(r[head.index("쌍 번호")].value for r in rows)
    check("3 쌍 수 62, 쌍마다 2행", len(pairs) == 62 and set(pairs.values()) == {2})
    okp = True
    for i in range(0, len(rows), 2):
        a, b = rows[i], rows[i + 1]
        g = lambda r, n: r[head.index(n)].value
        sa, sb = src[str(g(a, "v8.1 행번호"))], src[str(g(b, "v8.1 행번호"))]
        if not (g(a, "쌍 번호") == g(b, "쌍 번호") and sa["모수 포함 여부"] == "포함" and sb["모수 포함 여부"] == "제외" and sb["제외단계"] == "④중복"
                and "주소의 상품 번호 같음" in sb["제외사유"] and f"대표 행 {sa['행번호']}," in sb["제외사유"] + ","):
            okp = False; print("   쌍 구성 문제", g(a, "쌍 번호"))
    check("3 쌍마다 포함 1행(먼저)과 중복제거 1행, 제외사유의 대표 행 번호가 짝과 같음", okp)
    bad = [i for i, r in zip(ids, rows) if r[head.index("접속 후 URL")].value != src[i]["접속 후 URL"] or (r[head.index("접속 후 URL")].hyperlink and r[head.index("접속 후 URL")].hyperlink.target != src[i]["접속 후 URL"])]
    check("3 접속 후 URL과 링크가 v8.1과 글자까지 같음", not bad, str(bad[:5]))

    # 검증 2
    mism = 0
    for r, v in zip(rows, vals):
        for name, cell in zip(head, r):
            if name == "스크린샷": continue
            want = v[name]
            got = "" if cell.value is None else str(cell.value)
            if got != want:
                mism += 1
                if mism <= 5: print("   칸 불일치", v["v8.1 행번호"], name, repr(got[:60]), repr(want[:60]))
        s = src[v["v8.1 행번호"]]
        for name in ("리테일러", "국가", "브랜드", "제품코드", "모수 포함 여부", "제외사유", "접속 후 URL"):
            want = s[name].replace(", #119)", ")").replace("주소의 상품 번호 같음", "주소의 PDP 식별자 같음") if name == "제외사유" else s[name]  # 이슈 번호를 떼고 이름만 바꾼다
            if v[name] != want:
                mism += 1; print("   v8.1 불일치", v["v8.1 행번호"], name)
    check("2 엑셀 124행 모든 칸 = values.csv, v8.1 열 = v8.1 원본", mism == 0, f"불일치 {mism}건")
    re_m = 0
    for v in vals:
        if not v["원본 자료 파일"]: continue
        name = Path(v["원본 자료 파일"]).name.replace(".json", "")
        p = raw_payload(name)
        if p is None:
            re_m += 1; print("   원본 없음", name); continue
        e = X.extract(p)
        for k, label in X.FIELDS:
            want = v[f"원문 {label}"].split("\n[2차] ")[0]
            if v[label] in ("확인 못 함", "Product not available"): continue
            if e["values"][k] != want:
                re_m += 1
                if re_m <= 5: print("   다시 뽑은 값 불일치", name, label)
        if p["requested_url"] != v["접속 후 URL"]:
            re_m += 1; print("   연 주소가 v8.1과 다름", name)
        if v["쌍 판정"] not in ("확인 못 함", "Product not available") and p["final_url"] != v["접속 후 URL"]:
            re_m += 1; print("   도착 주소가 v8.1과 다름", name)
    check("2 raw 원본에서 다시 뽑은 값 = values.csv 원문, 연 주소 = v8.1 접속 후 URL", re_m == 0, f"불일치 {re_m}건")

    # 검증 4 (자동): 그림 속 글자
    ocr = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    shots_dir = B.SHOTS
    missing = [v["v8.1 행번호"] for v in vals if v["스크린샷 파일"] and not (shots_dir / Path(v["스크린샷 파일"]).name).exists()]
    check("4 스크린샷 파일이 행마다 있음", not missing, str(missing[:8]))
    if ocr and ocr.exists():
        # 전체 페이지 그림은 매우 길어서, 상품명과 가격이 있는 맨 위 1600픽셀만 잘라 글자를 읽는다.
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        tmp = HERE / "_ocr_top"; tmp.mkdir(exist_ok=True)
        files = []
        for v in vals:
            if v["스크린샷 파일"] and v["v8.1 행번호"] not in missing:
                src = shots_dir / Path(v["스크린샷 파일"]).name
                im = Image.open(src); im.crop((0, 0, im.size[0], min(1600, im.size[1]))).convert("RGB").save(tmp / src.name, quality=90)
                files.append(str(tmp / src.name))
        out = subprocess.run([str(ocr)] + files, capture_output=True, text=True).stdout
        texts = {Path(l.split("\t")[1]).name: l.split("\t", 2)[2] for l in out.splitlines() if l.startswith("##FILE")}
        low = lambda s: re.sub(r"[^a-z0-9áéíóúñü]+", " ", s.lower())
        badn, rep = [], []
        cnt = Counter()
        for v in vals:
            if not v["스크린샷 파일"] or v["v8.1 행번호"] in missing: continue
            raw_t = texts.get(Path(v["스크린샷 파일"]).name, "")
            t = low(raw_t)
            if v["쌍 판정"] in ("확인 못 함", "Product not available"):
                ok = "not available" in t or "bloqueado" in t or "no encontr" in t
                cnt["확인 못 함 행: 안내 화면 글자 읽힘" if ok else "확인 못 함 행: 안내 글자 못 읽음"] += 1
                rep.append((v["v8.1 행번호"], "안내 화면", ok))
                if not ok: badn.append((v["v8.1 행번호"], "안내 화면 글자 없음"))
                continue
            words = [w for w in low(v["4. 상품명"]).split() if len(w) >= 3]
            hit = sum(w in t for w in words) / max(1, len(words))
            code = re.sub(r"\D", "", v["1. 화면에 보이는 제품 번호"])
            code_ok = bool(code) and code in re.sub(r"\s", "", raw_t)
            price = re.sub(r"[^0-9.,]", "", v["10. 표시 가격"].split(" | ")[0].split(" / ")[0].replace("1차: ", ""))
            price_ok = bool(price) and price in re.sub(r"\s", "", raw_t)
            cnt["상품명 읽힘"] += hit >= 0.8; cnt["가격 읽힘"] += price_ok; cnt["상품 번호 읽힘"] += code_ok
            rep.append((v["v8.1 행번호"], round(hit, 2), price_ok, code_ok))
            # 작은 글씨인 상품 번호는 글자 인식이 한두 자 틀릴 수 있어, 상품명과 (가격 또는 상품 번호)가 읽히면 통과로 본다.
            if hit < 0.8 or not (price_ok or code_ok): badn.append((v["v8.1 행번호"], round(hit, 2), price_ok, code_ok))
        (HERE / "screenshot_text_check.json").write_text(json.dumps({"texts": texts, "result": rep}, ensure_ascii=False, indent=1), encoding="utf-8")
        check("4 그림 속 글자에서 그 행의 상품명(낱말 80% 이상)과 가격 또는 상품 번호가 읽힘", not badn, f"{dict(cnt)} 어긋남 {badn[:10]}")
    # 스크린샷 시트 링크
    wsS = wb["스크린샷"]
    link_bad = 0
    for r, v in zip(rows, vals):
        cell = r[head.index("스크린샷")]
        if cell.value == "전체 페이지 보기":
            loc = cell.hyperlink.location or cell.hyperlink.target or ""
            m = re.search(r"!([A-Z]+\d+)$", loc)
            if not m or v["v8.1 행번호"] not in str(wsS[m.group(1)].value): link_bad += 1
    check("3 124행 시트의 그림 링크가 스크린샷 시트의 같은 행번호 자리로 감", link_bad == 0, f"어긋남 {link_bad}")
    n_rows = sum(1 for v in vals if v["스크린샷 파일"] and v["v8.1 행번호"] not in missing)
    check("4 스크린샷 시트에 넣은 그림 조각 수(행마다 1조각 이상)", len(wsS._images) >= n_rows, f"{n_rows}행, 조각 {len(wsS._images)}개")
    # 전체 페이지 그림인지: 그림 높이가 수집 때 잰 페이지 높이와 같아야 한다
    from PIL import Image as _I
    _I.MAX_IMAGE_PIXELS = None
    short = []
    for v in vals:
        if not v["스크린샷 파일"] or v["v8.1 행번호"] in missing: continue
        name = Path(v["스크린샷 파일"]).stem
        meta = shots_dir / f"{name}.full.json"
        if not meta.exists(): short.append((name, "기록 없음")); continue
        m = json.loads(meta.read_text()); w, h = _I.open(shots_dir / f"{name}.jpg").size
        if h != m["height"] or w != m["width"]: short.append((name, h, m["height"]))
    check("4 그림 크기 = 수집 때 잰 페이지 전체 크기", not short, str(short[:6]))

    # 검증 6 (124행 시트의 "Product not available"은 요약에서 "확인 못 함"으로 센다)
    UNK = lambda v: "확인 못 함" if v == "Product not available" else v
    tally = Counter(UNK(vals[i]["쌍 판정"]) for i in range(0, len(vals), 2))
    check("6 판정 합계 62", sum(tally.values()) == 62, dict(tally))
    want = f"같음 {tally.get('같음', 0)}쌍, 다름 {tally.get('다름', 0)}쌍, 확인 못 함 {tally.get('확인 못 함', 0)}쌍, 합계 62쌍"
    summ = " ".join(str(c.value) for r in wb["요약"].iter_rows() for c in r if c.value)
    check("6 요약 시트 숫자 = 124행 시트", want in summ, want)
    draft = B.DRAFT.read_text(encoding="utf-8")
    line = f"| 합계 | {tally.get('같음', 0)} | {tally.get('다름', 0)} | {tally.get('확인 못 함', 0)} | 62 |"
    check("6 두레이 글 초안 숫자 = 124행 시트", line in draft, line)
    by = Counter((vals[i]["리테일러"], UNK(vals[i]["쌍 판정"])) for i in range(0, len(vals), 2))
    for r, nm in (("COSTCO", "Costco 캐나다"), ("FALABELLA", "Falabella 칠레")):
        a, b, c = by.get((r, "같음"), 0), by.get((r, "다름"), 0), by.get((r, "확인 못 함"), 0)
        check(f"6 {nm} 숫자가 요약과 초안에 같음", f"{nm}: 같음 {a}쌍, 다름 {b}쌍, 확인 못 함 {c}쌍" in summ and f"| {nm} | {a} | {b} | {c} | {a + b + c} |" in draft)
    # 글쓰기 규칙
    alltext = summ + draft + " ".join(str(c.value) for n in ("검사 방법", "스크린샷") for r in wb[n].iter_rows() for c in r if c.value)
    banned = [w for w in ("·", "Zyte", "Codex", "Claude", "ChatGPT", "D074", "D079", "D080", "#119") if w in alltext + " ".join(str(c.value) for r in wb["124행"].iter_rows() for c in r if c.value)]
    # 상품명 속 기능 이름 AI(예: Bespoke AI)는 사이트 글자라 그대로 둔다. 설명 글(요약, 검사 방법)에만 없으면 된다.
    prose = summ + " ".join(str(c.value) for r in wb["검사 방법"].iter_rows() for c in r if c.value)
    banned += [w for w in (" AI ", "인공지능") if w in prose]
    check("글쓰기 규칙: 가운뎃점, 도구 이름, 내부 결정 번호 없음", not banned, str(banned))
    # 엑셀 설명 글은 '~다' 문체, '대표 주소' 대신 canonical, 지운 시트 이름 없음 (11-21 사용자 요청)
    xl_text = summ + " ".join(str(c.value) for n in ("검사 방법", "스크린샷", "124행") for r in wb[n].iter_rows() for c in r if c.value) + " ".join(wb.sheetnames)
    old = [w for w in ("상품 번호", "상품번호", "습니다", "니다.", "대표 주소", "주소 글자 실험", "대조군", "시트 읽는 법", "핵심 특징", "사이트 내부 상품") if w in xl_text]
    check("엑셀 문구: 존댓말, 대표 주소, 지운 시트와 항목 이름 없음", not old and wb.sheetnames == ["요약", "124행", "스크린샷", "검사 방법"], str(old) + str(wb.sheetnames))
    print("전체 결과:", "모두 통과" if not fails else f"실패 {len(fails)}건: {fails}")

if __name__ == "__main__":
    main()
