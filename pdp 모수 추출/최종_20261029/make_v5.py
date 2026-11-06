"""Apply the verified 2026-11-06 German MediaMarkt review to shared PDP v4."""

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
V4 = HERE / "PDP모수_공유용_v4_두레이157-159제외반영_25개국_35개리테일러_전체판정_55997행_20261106.csv"
V5 = HERE / "PDP모수_공유용_v5_독일MediaMarkt13건제외반영_25개국_35개리테일러_전체판정_55997행_20261106.csv"
REVIEW = ROOT / "outputs/mediamarkt-de-v4-20261106/독일_MediaMarkt_v4_포함에서제외_변경대상_20261106.csv"
EXPECTED = {"5367", "5377", "5378", "5680", "5710", "5712", "5724", "5822", "6165", "6176", "6198", "6256", "6287"}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def main():
    columns, rows = read_csv(V4)
    review_columns, reviews = read_csv(REVIEW)
    assert len(columns) == 26 and len(rows) == 55_997
    assert review_columns[:26] == columns
    assert len(reviews) == len(EXPECTED) == 13
    assert {review["행번호"] for review in reviews} == EXPECTED
    assert len({row["행번호"] for row in rows}) == len(rows)
    assert Counter(row["모수 포함 여부"] for row in rows) == {"포함": 10_228, "제외": 45_769}

    by_number = {row["행번호"]: row for row in rows}
    for review in reviews:
        number = review["행번호"]
        row = by_number[number]
        assert all(review[column] == row[column] for column in columns), number
        assert row["국가"] == "Germany" and row["리테일러"] == "MEDIAMARKT", number
        assert row["모수 포함 여부"] == "포함" and review["변경요청_모수 포함 여부"] == "제외", number
        assert review["확인상태"] == "제외" and review["현재_제목"], number
        seller = review["현재_본상품_판매자"].strip()
        link = review["현재_판매자링크"].strip()
        assert seller and "/marketplace/seller/" in link, number
        assert review["현재_접속후URL"].startswith("https://www.mediamarkt.de/de/product/"), number

        row["모수 포함 여부"] = "제외"
        row["제외단계"] = "③리리부"
        row["판매자"] = seller
        row["접속 후 URL"] = review["현재_접속후URL"]
        if seller == "MediaMarktSaturn geprüft":
            row["제외사유"] = "리퍼·중고 (MediaMarktSaturn geprüft; 2026-11-06 본 상품 화면 확인, D103)"
            row["판매자구분"] = "리퍼·중고"
            row["판매자근거"] = f"2026-11-06 본 상품 Verkauf und Versand durch {seller}; 본 상품 Refurbished 상태 표시; {link}"
        else:
            row["제외사유"] = f"외부 판매자 ({seller}; 2026-11-06 본 상품 화면 확인, D103)"
            row["판매자구분"] = "외부판매자"
            row["판매자근거"] = f"2026-11-06 본 상품 Verkauf und Versand durch {seller}; {link}"
        row["메모"] = "; ".join(part for part in (row["메모"], "D103: 2026-11-06 현재 화면 재확인으로 포함→제외; OSM 기준일 2026-10-26 당시 판매자는 별도 확인하지 않음") if part)

    assert Counter(row["모수 포함 여부"] for row in rows) == {"포함": 10_215, "제외": 45_782}
    assert Counter(by_number[number]["판매자구분"] for number in EXPECTED) == {"외부판매자": 10, "리퍼·중고": 3}
    assert not V5.exists(), f"v5 already exists: {V5}"
    with V5.open("x", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)
    print(f"created {V5}: {len(rows)} rows, {len(columns)} columns, changed=13, status={dict(Counter(row['모수 포함 여부'] for row in rows))}")


if __name__ == "__main__":
    main()
