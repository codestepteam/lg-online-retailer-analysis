"""엑셀 파일을 만든 스크립트와 따로, 엑셀을 다시 열어 처음부터 대조하는 점검.
A. 스크린샷 시트의 그림이 맞는 행 자리에 들어갔는지 (그림 픽셀을 원본 그림과 비교, 수집 시각 순서 확인)
B. 124행 시트의 숫자와 표시 값을 원본(raw)에서 다른 방법으로 다시 세어 비교
C. 요약 시트와 두레이 초안의 숫자
"""
import csv, gzip, io, json, re, sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit
from openpyxl import load_workbook
from PIL import Image, ImageChops, ImageStat
Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
XLSX = next(HERE.glob("Costco_Falabella_*.xlsx"))
SRC = HERE.parents[1] / "pdp 모수 추출/최종_20261029/PDP모수_공유용_v8.1_1P3P구분추가_25개국_35개리테일러_전체판정_55129행_20261118.csv"
bad = []
def check(name, ok, detail=""):
    print(("통과" if ok else "실패"), "|", name, "|", detail)
    if not ok: bad.append(name)
def raw(name): return json.loads(gzip.open(HERE / "raw" / f"{name}.json.gz", "rt", encoding="utf-8").read())
def ms(iso): return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()

src = {r["행번호"]: r for r in csv.DictReader(SRC.open(encoding="utf-8-sig", newline=""))}
wb = load_workbook(XLSX)
ws, wsS = wb["124행"], wb["스크린샷"]
head = [c.value for c in ws[1]]
rows = [{h: c for h, c in zip(head, r)} for r in ws.iter_rows(min_row=2)]
val = lambda r, k: r[k].value

# ── A. 그림 자리 ──
headers = {}  # (열, 줄) -> 행번호
for row in wsS.iter_rows():
    for c in row:
        if isinstance(c.value, str) and c.value.startswith("v8.1 행번호 "):
            headers[(c.column, c.row)] = re.search(r"행번호 (\d+)", c.value).group(1)
by_row = {}
for im in wsS._images:
    col, r = im.anchor._from.col + 1, im.anchor._from.row + 1
    hr = max(hrow for (hc, hrow) in headers if hc == col and hrow <= r)
    by_row.setdefault(headers[(col, hr)], []).append((r, im))
check("A1 스크린샷 시트의 행 제목 124개, 그림이 붙은 행 124개", len(headers) == 124 and len(by_row) == 124, f"제목 {len(headers)}, 그림 있는 행 {len(by_row)}")
# 제목 아래 주소가 v8.1의 그 행 주소인지
url_bad = [n for (c, r), n in headers.items() if wsS.cell(row=r + 1, column=c).value != src[n]["접속 후 URL"]]
check("A2 그림 제목 아래 주소 = v8.1의 그 행 접속 후 URL", not url_bad, str(url_bad[:5]))
# 124행 시트 링크가 그 행의 제목 칸으로 가는지
link_bad = []
for r in rows:
    loc = r["스크린샷"].hyperlink.location if r["스크린샷"].hyperlink else ""
    m = re.search(r"!([A-Z]+)(\d+)$", loc or "")
    if not m or str(val(r, "v8.1 행번호")) not in str(wsS[f"{m.group(1)}{m.group(2)}"].value) or r["스크린샷"].value != "전체 페이지 보기":
        link_bad.append(val(r, "v8.1 행번호"))
check("A3 '전체 페이지 보기' 링크 124개가 시트 안 위치 링크이고 같은 행번호 제목 칸으로 감", not link_bad, str(link_bad[:5]))
# 그림 픽셀: 엑셀에 든 조각을 이어 붙여 원본 전체 그림(폭 800으로 줄인 것)과 비교. 짝 행의 그림과도 비교한다.
pair_of = {}
for i in range(0, len(rows), 2):
    a, b = str(val(rows[i], "v8.1 행번호")), str(val(rows[i + 1], "v8.1 행번호")); pair_of[a], pair_of[b] = b, a
def expected(n):
    im = Image.open(HERE / "screenshots" / f"f-{n}.jpg").convert("RGB"); w, h = im.size
    return im.resize((800, int(h * 800 / w)))
def diff(a, b):
    if a.size != b.size: return 999.0
    return sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3
pix_bad, closer_to_mate, size_bad, distinguishable = [], [], [], 0
for n, lst in by_row.items():
    lst.sort(key=lambda x: x[0])
    parts = [Image.open(io.BytesIO(im._data())).convert("RGB") for _, im in lst]
    H = sum(p.size[1] for p in parts); got = Image.new("RGB", (800, H)); y = 0
    for p in parts: got.paste(p, (0, y)); y += p.size[1]
    exp = expected(n)
    if got.size != exp.size: size_bad.append((n, got.size, exp.size)); continue
    d_own = diff(got, exp)
    if d_own > 4: pix_bad.append((n, round(d_own, 2)))
    mate = expected(pair_of[n])
    d_mate = diff(got, mate)
    if d_mate > d_own + 0.5: distinguishable += 1
    if d_mate < d_own - 0.01: closer_to_mate.append((n, round(d_own, 2), round(d_mate, 2)))
    # 조각이 2000픽셀 간격(100줄)으로 빈틈없이 놓였는지
    r0 = lst[0][0]
    if any(r != r0 + 100 * i for i, (r, _) in enumerate(lst)): pix_bad.append((n, "조각 간격"))
check("A4 엑셀 안 그림 크기 = 그 행 원본 전체 그림을 폭 800으로 줄인 크기", not size_bad, str(size_bad[:4]))
check("A5 엑셀 안 그림 픽셀 = 그 행 원본 전체 그림, 조각이 빈틈없이 이어짐", not pix_bad, str(pix_bad[:6]))
check("A6 엑셀 안 그림이 짝 행의 그림보다 자기 행 그림에 더 가깝거나 같음", not closer_to_mate, f"짝과 구별되는 행 {distinguishable}개 / 124, 어긋남 {closer_to_mate[:5]}")
# 수집 기록: 그림을 찍은 시각이 같은 작업의 원본을 담은 시각 바로 뒤이고, 원본의 주소가 그 행의 주소인지
t_bad, u_bad = [], []
times = {}
for n in by_row:
    p = raw(f"f-{n}"); m = json.loads((HERE / "screenshots" / f"f-{n}.full.json").read_text())
    times[n] = (ms(p["started_utc"]), ms(p["collected_utc"]), ms(m["shot_utc"]))
    if p["requested_url"] != src[n]["접속 후 URL"]: u_bad.append(n)
    if not (times[n][0] < times[n][1] < times[n][2] and times[n][2] - times[n][1] < 180): t_bad.append((n, round(times[n][2] - times[n][1])))
for n in by_row:  # 짝 행의 수집 구간과 겹치지 않아야 한다
    a, b = times[n], times[pair_of[n]]
    if not (a[2] <= b[0] or b[2] <= a[0]): t_bad.append((n, "짝과 구간 겹침"))
check("A7 원본의 주소 = 그 행 주소, 그림은 그 원본을 담은 직후(3분 안)에 찍힘, 짝 행과 수집 구간이 겹치지 않음", not t_bad and not u_bad, f"{t_bad[:5]} {u_bad[:5]}")

# ── B. 숫자와 표시 값 ──
KST = timezone(timedelta(hours=9))
errs = Counter(); ex = []
def note(kind, n, a, b):
    errs[kind] += 1
    if len(ex) < 12: ex.append((kind, n, str(a)[:60], str(b)[:60]))
for i, r in enumerate(rows):
    n = str(val(r, "v8.1 행번호")); s = src[n]
    for k in ("리테일러", "국가", "브랜드", "제품코드", "모수 포함 여부", "접속 후 URL"):
        if (val(r, k) or "") != s[k]: note("v8.1 열", n, val(r, k), s[k])
    if (val(r, "제외사유") or "") != s["제외사유"].replace(", #119)", ")").replace("주소의 상품 번호 같음", "주소의 PDP 식별자 같음"): note("제외사유", n, val(r, "제외사유"), s["제외사유"])
    if r["접속 후 URL"].hyperlink.target != s["접속 후 URL"]: note("URL 링크", n, r["접속 후 URL"].hyperlink.target, "")
    url = s["접속 후 URL"]; tail = urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
    if str(val(r, "주소 끝 PDP 식별자")) != tail: note("주소 끝 PDP 식별자", n, val(r, "주소 끝 PDP 식별자"), tail)
    slug = urlsplit(url).path.rstrip("/").split("/")[-2]
    for tok in str(val(r, "주소에서 서로 다른 부분")).split(", "):
        if tok not in slug: note("주소에서 다른 부분이 자기 주소에 없음", n, tok, slug)
    mate = rows[i + 1] if i % 2 == 0 else rows[i - 1]
    if val(r, "쌍 번호") != val(mate, "쌍 번호"): note("쌍 번호", n, val(r, "쌍 번호"), val(mate, "쌍 번호"))
    if val(r, "쌍 판정") != val(mate, "쌍 판정"): note("쌍 판정이 짝과 다름", n, "", "")
    if val(r, "쌍 판정") in ("확인 못 함", "Product not available"): continue
    p = raw(f"f-{n}"); h = p["html"]
    want_t = datetime.fromtimestamp(ms(p["collected_utc"]), KST).strftime("%Y-%m-%d %H:%M:%S")
    if val(r, "수집 시각(한국 시각)") != want_t: note("수집 시각", n, val(r, "수집 시각(한국 시각)"), want_t)
    if s["리테일러"] == "COSTCO":
        photos = len(set(re.findall(r'aria-label="View Product Preview (\d+)"', h)))
        m = re.match(r"사진 (\d+)장", str(val(r, "5. 갤러리")))
        if not m or int(m.group(1)) != photos: note("사진 수", n, val(r, "5. 갤러리"), photos)
        spec = len(set(re.findall(r'id="ProductSpecifications-row(\d+)"', h)))
        m = re.match(r"(\d+)항목", str(val(r, "8. 사양표")))
        if not m or int(m.group(1)) != spec: note("사양 항목 수", n, val(r, "8. 사양표"), spec)
        esc = h.replace('\\"', '"')
        mp = re.search(r'"onlinePrice":([\d.]+)', esc)
        shown = float(str(val(r, "10. 표시 가격")).replace("$", "").replace(",", ""))
        if not mp or abs(float(mp.group(1)) - shown) > 0.001: note("가격(원본 데이터의 onlinePrice와 비교)", n, val(r, "10. 표시 가격"), mp.group(1) if mp else None)
        # 리뷰 수: 페이지에 따로 들어 있는 리뷰 요약 정보(reviewCount)와 비교한다.
        # (상품 데이터의 ratingCount 는 사이트가 덜 자주 갱신하는 값이라 화면 숫자와 몇 개 차이 날 수 있어 기준으로 쓰지 않는다.)
        mc = re.search(r'"aggregateRating":\s*\{[^}]*"reviewCount":\s*"?(\d+)', h)
        mr = re.search(r"리뷰 ([\d,]+)", str(val(r, "9. 평점과 리뷰 수")))
        if mc and mr and int(mr.group(1).replace(",", "")) != int(mc.group(1)): note("리뷰 수(리뷰 요약 정보의 reviewCount와 비교)", n, val(r, "9. 평점과 리뷰 수"), mc.group(1))
        if not mc and mr: errs["리뷰 요약 정보 없음(비교 생략)"] += 0
        can = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        if not can or can.group(1) != val(r, "2. canonical"): note("canonical", n, val(r, "2. canonical"), can.group(1) if can else None)
    else:
        nd = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S).group(1))["props"]["pageProps"]["productData"]
        if tail not in str(val(r, "1. 화면에 보이는 제품 번호")) and nd["id"] not in url: note("Falabella 화면의 상품 코드가 주소에 없음", n, val(r, "1. 화면에 보이는 제품 번호"), url[-40:])
        v = next(x for x in nd["variants"] if x["id"] == nd["currentVariant"])
        photos = sum(1 for m_ in v["medias"] if m_["mediaType"] == "image"); vids = len(v["medias"]) - photos
        if not str(val(r, "5. 갤러리")).startswith(f"사진 {photos}장, 영상 {vids}개"): note("사진 수", n, val(r, "5. 갤러리"), (photos, vids))
        spec = len(nd["attributes"]["specifications"])
        if not str(val(r, "8. 사양표")).startswith(f"{spec}항목"): note("사양 항목 수", n, val(r, "8. 사양표"), spec)
        price = next(x for x in v["prices"] if x["type"] == "internetPrice" or not x.get("crossed"))
        if price["price"][0] not in str(val(r, "10. 표시 가격")): note("가격", n, val(r, "10. 표시 가격"), price["price"])
        can = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        if not can or can.group(1) != val(r, "2. canonical"): note("canonical", n, val(r, "2. canonical"), can.group(1) if can else None)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    name = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h1.group(1))).strip()
    import html as _html
    name = re.sub(r"\s+", " ", _html.unescape(name)).strip()  # 줄 바꿈 없는 공백(nbsp)도 일반 공백 한 칸으로 정리한다(엑셀 값과 같은 정리 규칙)
    if name != val(r, "4. 상품명"): note("상품명", n, val(r, "4. 상품명"), name)
check("B1 124행 시트 값이 v8.1, 주소, 원본에서 다른 방법으로 다시 센 값과 같음", not errs, f"{dict(errs)} {ex}")
# 쌍 일치 표시와 판정: values.csv 원문으로 다시 계산
vals = list(csv.DictReader((HERE / "values.csv").open(encoding="utf-8-sig", newline="")))
labels = [h for h in head if re.match(r"\d+\. ", str(h))]
vbad = []
for i in range(0, len(vals), 2):
    a, b = vals[i], vals[i + 1]
    if a["쌍 판정"] in ("확인 못 함", "Product not available"):
        if not all(a[l] == a["쌍 판정"] for l in labels): vbad.append((a["쌍 번호"], "확인 못 함 표시"))
        continue
    d = [l for l in labels if a[f"원문 {l}"] != b[f"원문 {l}"]]
    if (a["쌍 판정"] == "같음") != (not d): vbad.append((a["쌍 번호"], d))
    for l in ("5. 갤러리", "7. 상세 설명 본문", "8. 사양표"):
        same = a[f"원문 {l}"] == b[f"원문 {l}"]
        for x in (a, b):
            if ("쌍 일치" in x[l]) != same and x[l] not in ("양쪽 모두 없음", "없음"): vbad.append((a["쌍 번호"], l, "일치 표시"))
    # 표시 값이 양쪽 같아야 '같음'
    if a["쌍 판정"] == "같음" and any(a[l] != b[l] for l in labels): vbad.append((a["쌍 번호"], "표시 값이 짝과 다름"))
check("B2 쌍 판정과 '쌍 일치' 표시가 원문을 다시 비교한 결과와 같음, '같음' 쌍은 두 줄의 표시 값이 같음", not vbad, str(vbad[:6]))

# ── C. 요약, 초안 ──
UNK = lambda v: "확인 못 함" if v == "Product not available" else v
tally = Counter(UNK(val(rows[i], "쌍 판정")) for i in range(0, len(rows), 2))
byr = Counter((val(rows[i], "리테일러"), UNK(val(rows[i], "쌍 판정"))) for i in range(0, len(rows), 2))
summ = " ".join(str(c.value) for r in wb["요약"].iter_rows() for c in r if c.value)
draft = (HERE / "두레이_글_초안.md").read_text(encoding="utf-8")
ok = f"같음 {tally['같음']}쌍, 다름 {tally['다름']}쌍, 확인 못 함 {tally['확인 못 함']}쌍, 합계 62쌍" in summ and f"| 합계 | {tally['같음']} | {tally['다름']} | {tally['확인 못 함']} | 62 |" in draft
for ret, nm in (("COSTCO", "Costco 캐나다"), ("FALABELLA", "Falabella 칠레")):
    a, b, c = byr[(ret, "같음")], byr[(ret, "다름")], byr[(ret, "확인 못 함")]
    ok = ok and f"{nm}: 같음 {a}쌍, 다름 {b}쌍, 확인 못 함 {c}쌍" in summ and f"| {nm} | {a} | {b} | {c} | {a + b + c} |" in draft
check("C1 요약 시트와 두레이 초안의 판정 숫자 = 124행 시트를 다시 센 숫자", ok, dict(tally))
# 초안의 대표 예 값이 124행 시트와 같은지
m = re.search(r"대표 예 \(쌍 (\d+)", draft); pr = [r for r in rows if str(val(r, "쌍 번호")) == m.group(1)]
ex_ok = all(str(val(pr[0], k)) in draft for k in ("접속 후 URL", "4. 상품명", "1. 화면에 보이는 제품 번호", "2. canonical", "10. 표시 가격", "9. 평점과 리뷰 수")) and str(val(pr[1], "접속 후 URL")) in draft
check("C4 두레이 초안의 대표 예 값 = 124행 시트의 그 쌍 값", ex_ok, f"쌍 {m.group(1)}")
unk = [str(val(rows[i], "쌍 번호")) for i in range(0, len(rows), 2) if val(rows[i], "쌍 판정") != "같음"]
check("C5 두레이 초안의 '다름, 확인 못 함' 표에 그 쌍이 모두 있고 다른 쌍은 없음", sorted(re.findall(r"^\| (\d+) \| ", draft, re.M)) == sorted(unk), str(unk))
print("전체:", "모두 통과" if not bad else f"실패 {len(bad)}건 {bad}")
