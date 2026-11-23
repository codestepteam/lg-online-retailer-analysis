"""Offline request preview. This script never makes a network request."""

import json
from uuid import NAMESPACE_URL, uuid5

from select_rows import OUT, select


def preview():
    planned = []
    for pair in select()["pairs"]:
        if not pair["pilot"]:
            continue
        session = str(uuid5(NAMESPACE_URL, f"{OUT.name}/pilot/{pair['pair']}"))
        for attempt in (1, 2):
            for row in pair["rows"]:
                request = {
                    "url": row["접속 후 URL"],
                    "browserHtml": True,
                    "screenshot": True,
                    "screenshotOptions": {"fullPage": False},
                    "session": {"id": session},
                }
                if row["리테일러"] == "COSTCO":
                    request["geolocation"] = "CA"
                planned.append({"row": row["행번호"], "pair": pair["pair"], "attempt": attempt, "request": request})
    assert len(planned) == 24 and len({p["row"] for p in planned}) == 12
    return planned


if __name__ == "__main__":
    planned = preview()
    target = OUT / "raw" / "paid-pilot-request-preview.json"
    target.write_text(json.dumps(planned, ensure_ascii=False, indent=2))
    print("24 requests previewed locally. 0 requests sent.")
