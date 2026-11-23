"""Compare the two saved captures of each control or slug experiment without scoring target pairs."""

import json

from lxml import html
from PIL import Image

from inspect_pilot import OUT, RAW, costco


def read(stem):
    meta = json.loads((RAW / f"{stem}.json").read_text())
    doc = html.fromstring((RAW / f"{stem}.html").read_text())
    notices = doc.xpath('//*[@aria-labelledby="product_details"]//*[@id="flix-privacy-policy"]/..')
    removed = []
    for notice in notices:
        if not notice.text_content().strip().startswith("This content uses cookies to improve your experience."):
            continue
        if "flixmedia.com/privacy" in notice.text_content() and not notice.xpath(".//h1|.//h2|.//h3"):
            removed.append({"text": notice.text_content().strip(), "pictures": notice.xpath(".//img/@src")})
            notice.drop_tree()
    observed = costco(doc)
    # Bundles can place the stock and shipping information outside the standalone item's card.
    observed["화면 배송 위치"] = doc.xpath('//*[@aria-label and contains(@aria-label,"current delivery location")]/@aria-label')
    observed["묶음 구매 상태"] = [t.strip() for t in doc.xpath(
        '//*[not(*) and contains(translate(text(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"in this bundle is out of stock")]/text()'
    )]
    shot = OUT / "screenshots" / f"{stem}-product.jpg"
    with Image.open(shot) as im:
        pixels = im.size
        im.verify()
    return {"meta": meta, "pixels": pixels, "observations": observed, "excluded_cookie_notice": removed}


def compare(stems):
    a, b = [read(stem) for stem in stems]
    unequal = [k for k in a["observations"] if a["observations"][k] != b["observations"][k]]
    return {"captures": [a, b], "unequal_observations": unequal,
            "same_dimensions": a["meta"]["viewport"] == b["meta"]["viewport"] and a["pixels"] == b["pixels"]}


def verify():
    s = json.loads((RAW / "selection.json").read_text())
    controls = []
    for i, c in enumerate([c for c in s["controls"] if c["retailer"] == "COSTCO"]):
        ids = [r["행번호"] for r in c["rows"]]
        rounds = [1, 2, 3] if i == 1 else [1, 2]
        captures = [compare([f"control-iab-{j}-{n}" for n in ids]) for j in rounds]
        comparable = [v for v in captures if v["same_dimensions"]]
        assert len(comparable) >= 2
        for result in comparable:
            assert {"상품명", "화면 품목 번호와 모델", "대표 주소"} <= set(result["unequal_observations"])
            for r, origin in zip(result["captures"], c["rows"]):
                assert r["meta"]["url"] == origin["접속 후 URL"]
            left, right = result["captures"]
            assert left["observations"]["화면 배송 위치"] == right["observations"]["화면 배송 위치"]
            assert any("M4V 2H7" in item for item in left["observations"]["화면 배송 위치"])
        controls.append({"row_ids": ids, "rounds": captures})
    slugs = []
    for pair in (p for p in s["pairs"] if p["pilot"] and p["rows"][0]["리테일러"] == "COSTCO"):
        origin = pair["rows"][0]
        row = origin["행번호"]
        result = compare([f"slug-iab-{row}-{kind}" for kind in ["original", "altered"]])
        assert result["same_dimensions"]
        one, two = result["captures"]
        original = one["meta"]["url"]
        assert original == origin["접속 후 URL"]
        before, name, after = original.rsplit("/", 2)
        assert two["meta"]["url"] == f"{before}/pdp-study-example/{after}"
        assert one["observations"]["배송 우편번호"] == two["observations"]["배송 우편번호"] == ["M4V 2H7"]
        slugs.append({"row": row, **result})
    target = RAW / "costco-controls-and-slug-experiments.json"
    target.write_text(json.dumps({"controls": controls, "slug_experiments": slugs}, ensure_ascii=False, indent=2))
    print("Controls with replicated differences in product name, item/model and canonical:", len(controls))
    print("Slug experiments, differing observed fields:", [(e["row"], e["unequal_observations"]) for e in slugs])


if __name__ == "__main__":
    verify()
