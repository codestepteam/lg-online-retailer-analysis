"""기존 판매자 판정 함수를 호출하지 않고 헝가리 원문·판매 상태·버전 파일을 대조한다."""
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
from collections import Counter

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FINAL = ROOT / "pdp 모수 추출/최종_20261029"


def extract(page, url, title_pattern):
    soup = BeautifulSoup(page, "lxml")
    pid = re.search(r"-(\d+)\.html", url).group(1)
    heading = soup.find("h1")
    title = re.sub(r"\s+", " ", heading.get_text(" ", strip=True)) if heading else ""
    selected = soup.select_one('[data-test="mms-pdp-offer-selection"]')
    price = soup.select_one('[data-test="mms-product-price"]')
    visible = selected.get_text(" ", strip=True) if selected else ""
    state_pattern = r'"id":"[A-Za-z]+:hu:' + pid + r'","isAvailableForDelivery".{0,500}?"onlineStatus":"([A-Z_]+)"'
    states = sorted({m.group(1) for m in re.finditer(state_pattern, page)})
    products = []
    for script in soup.select('script[type="application/ld+json"]'):
        data = json.loads(script.string or script.get_text())
        for node in data if isinstance(data, list) else [data]:
            if not isinstance(node, dict):
                continue
            product = node.get("object") if node.get("@type") == "BuyAction" else node
            if isinstance(product, dict) and product.get("@type") in ("Product", "ProductGroup") and str(product.get("sku")) == pid:
                products.append(product)
    offers = []
    for product in products:
        value = product.get("offers", [])
        offers.extend(value if isinstance(value, list) else [value])
    return {"본문제목": title, "상품번호": pid, "본상품가격영역존재": price is not None,
            "제목제외단어": [m.group() for m in re.finditer(title_pattern, title, re.I)],
            "본상품판매자링크": [{"이름": a.get_text(" ", strip=True), "주소": a.get("href")} for a in price.select('a[href*="/marketplace/seller/"]')] if price else [],
            "선택영역의리퍼판매자관련표현": [m.group() for m in re.finditer(r'felújított|refurbished|használt|\bused\b|outlet|újracsomagolt|értékesítő|forgalmaz|\beladó\b|marketplace', visible, re.I)],
            "본상품판매상태": states[0] if len(states) == 1 else "확인불가",
            "직접연결상품요약수": len(products),
            "신품상태값": [o.get("itemCondition") for o in offers],
            "요약재고값": [o.get("availability") for o in offers],
            "영구품절화면문구": "Ez a termék végleg elfogyott" if "Ez a termék végleg elfogyott" in visible else "",
            "현재구매불가화면문구": "Online jelenleg nem elérhető" if "Online jelenleg nem elérhető" in visible else ""}


def version_path(version):
    files = [p for p in FINAL.glob("*.csv") if "_공유용_" + version + "_" in unicodedata.normalize("NFC", p.name)]
    assert len(files) == 1, version
    return files[0]


def read_hungary(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, [r for r in reader if r["국가"] == "Hungary" and r["리테일러"].lower() == "mediamarkt"]


def main():
    records = [json.loads(line) for line in (HERE / "requests.jsonl").read_text().splitlines()]
    records = [r for r in records if r["country"] == "Hungary"]
    assert len(records) == len({r["url"] for r in records}) == 268
    pattern = json.loads((HERE / "rules_snapshot.json").read_text())["sellers"]["mediamarkt_screen"]["Hungary"]["refurb_title"]
    pages = []
    for record in records:
        filename = hashlib.sha256(record["url"].encode()).hexdigest()[:20] + ".html.gz"
        raw = gzip.decompress((HERE / "html" / filename).read_bytes())
        assert hashlib.sha256(raw).hexdigest() == record["html_sha256"]
        data = extract(raw.decode(), record["final_url"], pattern)
        assert data["본문제목"] and data["본상품가격영역존재"] and data["본상품판매상태"] != "확인불가"
        pages.append({"행번호": record["row"], "요청URL": record["url"], "도착URL": record["final_url"],
                      "원문수집시각": record["checked_at"], "원문파일": "html/" + filename, "원문SHA256": record["html_sha256"], **data})
    versions, hashes, paths = {}, {}, {}
    for version in ("v5", "v6", "v7"):
        path = version_path(version)
        paths[version] = path
        hashes[version] = hashlib.sha256(path.read_bytes()).hexdigest()
        versions[version] = read_hungary(path)
    columns, original = versions["v5"]
    compared = {}
    for version in ("v6", "v7"):
        cols, rows = versions[version]
        by_id = {r["행번호"]: r for r in rows}
        compared[version] = {"행수": len(rows), "열수": len(cols), "포함": sum(r["모수 포함 여부"] == "포함" for r in rows),
                             "기존값변경행": [r["행번호"] for r in original if r != by_id.get(r["행번호"])],
                             "동일열순서": cols == columns, "동일행순서": [r["행번호"] for r in original] == [r["행번호"] for r in rows]}
    stock = [r for r in pages if r["본상품판매상태"] == "PERMANENTLY_NOT_AVAILABLE"]
    assert len(stock) == 2, "이 고정 수집본의 영구품절 검토 대상 수와 다름"
    latest = {r["행번호"]: r for r in versions["v7"][1]}
    extra = ["검토후_모수 포함 여부", "검토후_제외단계", "검토후_제외사유", "원문_판매상태", "원문_화면문구", "원문_확인시각"]
    changes = []
    for row in stock:
        current = latest[row["행번호"]]
        assert current["모수 포함 여부"] == "포함"
        changes.append({**current, "검토후_모수 포함 여부": "제외", "검토후_제외단계": "④영구품절",
                        "검토후_제외사유": "본 상품 온라인 영구 구매 불가(PERMANENTLY_NOT_AVAILABLE; 기존 D068·D085 기준)",
                        "원문_판매상태": row["본상품판매상태"], "원문_화면문구": row["영구품절화면문구"] or row["현재구매불가화면문구"],
                        "원문_확인시각": row["원문수집시각"]})
    with (HERE / "헝가리_영구품절_정정대상_2건.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns + extra, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(changes)
    result = {"검증명령": str(Path(sys.executable)) + " -B " + str(Path(__file__).relative_to(ROOT)),
              "검증범위": "11월10일 저장된 헝가리268개 HTML 독립 추출. 기존 판매자 판정 함수는 호출하지 않음. 새 사이트 수집은 하지 않음.",
              "상품수": len(pages), "판매상태집계": dict(Counter(r["본상품판매상태"] for r in pages)),
              "제목제외단어건수": sum(bool(r["제목제외단어"]) for r in pages),
              "본상품판매자링크건수": sum(bool(r["본상품판매자링크"]) for r in pages),
              "선택영역리퍼판매자관련표현건수": sum(bool(r["선택영역의리퍼판매자관련표현"]) for r in pages),
              "신품상태집계": dict(Counter(c for r in pages for c in r["신품상태값"])),
              "상품요약없는행": [r["행번호"] for r in pages if r["직접연결상품요약수"] == 0],
              "기존버전헝가리전체행대조": compared, "버전파일SHA256": hashes,
              "영구품절정정대상": stock, "정정대상수": len(changes), "정정시헝가리포함수": 268 - len(changes),
              "모수파일수정여부": False, "새유료수집횟수": 0,
              "한계": "제목·판매자 새 조건으로는 추가 제외0개지만 기존 영구품절 기준까지 적용하면2건 정정대상. 제조사 단종이나 과거10월 상태를 확정하지 않음."}
    (HERE / "hungary_independent_stock_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (HERE / "hungary_independent_pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2) + "\n")
    assert all(hashlib.sha256(path.read_bytes()).hexdigest() == hashes[ver] for ver, path in paths.items())
    print(json.dumps({k: v for k, v in result.items() if k not in ("영구품절정정대상", "버전파일SHA256")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
