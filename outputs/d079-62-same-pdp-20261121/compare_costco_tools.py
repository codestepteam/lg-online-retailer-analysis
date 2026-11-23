"""Summarise only what the two tools actually saved for the six pilot rows."""

import json
from collections import Counter

from lxml import html
from PIL import Image

from inspect_pilot import OUT, RAW, costco


def compare():
    source = json.loads((RAW / "selection.json").read_text())
    targets = {r["행번호"]: r["접속 후 URL"] for p in source["pairs"]
               if p["pilot"] and p["rows"][0]["리테일러"] == "COSTCO" for r in p["rows"]}
    iab = {r["row"]: r for r in json.loads((RAW / "iab-pilot-observations.json").read_text())
           if r["round"] == 5 and r["row"] in targets}
    report = []
    for row, url in targets.items():
        for attempt in (1, 2):
            stem = f"zyte-{attempt}-{row}"
            meta_path = RAW / f"{stem}.meta.json"
            record = {"row": row, "attempt": attempt, "url": url}
            if not meta_path.exists():
                report.append({**record, "state": "not-sent"})
                continue
            meta = json.loads(meta_path.read_text())
            assert meta["url"] == url and iab[row]["url"] == url
            record.update(meta)
            if meta["state"] == "received":
                resp = json.loads((RAW / f"{stem}.response.json").read_text())
                assert resp["url"] == meta["landed"] and resp["statusCode"] == meta["page_status"]
                doc = html.fromstring(resp["browserHtml"])
                record["page_title"] = doc.xpath("string(//title)")
                record["visible_notice"] = doc.xpath("//main//p/text()")[:2] if meta["page_status"] != 200 else []
                shot = OUT / "screenshots" / meta["screenshot"]
                with Image.open(shot) as im:
                    record["image_size"] = im.size
                    im.verify()
                record["product_heading"] = [n.text_content().strip() for n in doc.xpath('//*[@id="productDescriptionDesktop"]//h1')]
                record["browser_product_heading"] = iab[row]["observations"]["상품명"]
                if record["product_heading"]:
                    try:
                        record["observations"] = costco(doc)
                    except (ValueError, IndexError, KeyError, TypeError) as exc:
                        record["unreadable"] = type(exc).__name__
            report.append(record)
    assert len(report) == 12
    (RAW / "costco-tool-comparison.json").write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print("Request states", dict(Counter(r["state"] for r in report)))
    print("Retailer status", dict(Counter(r.get("page_status") for r in report if "page_status" in r)))
    print("Product headings in paid responses", sum(bool(r.get("product_heading")) for r in report))


if __name__ == "__main__":
    compare()
