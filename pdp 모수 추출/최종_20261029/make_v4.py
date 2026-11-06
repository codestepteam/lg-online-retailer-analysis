"""Apply the three 2026-11-05 retailer review CSVs to shared PDP v3."""

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
V3 = HERE / "PDP모수_공유용_v3_EY검토반영_25개국_35개리테일러_전체판정_55997행_20261031.csv"
V4 = HERE / "PDP모수_공유용_v4_두레이157-159제외반영_25개국_35개리테일러_전체판정_55997행_20261106.csv"

REVIEWS = (
    (
        "Sharaf DG", "UAE", "Sharaf DG", 9,
        ROOT / "outputs/sharaf-157-20261105/SharafDG_v3포함_외부판매자9건_포함에서제외_변경대상_20261105.csv",
    ),
    (
        "eXtra", "Saudi Arabia", "EXTRA", 129,
        ROOT / "outputs/extra-158-20261105/eXtra_v3포함_화면품절문구129건_포함에서제외_변경대상_20261105.csv",
    ),
    (
        "DIENMAYXANH", "Vietnam", "DIENMAYXANH", 183,
        ROOT / "outputs/dienmayxanh-v3-all-included-closed-20261105-20261105-112819/Dienmayxanh_v3포함_판매중단183건_포함에서제외_변경대상_20261105.csv",
    ),
)


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def append_memo(row, text):
    row["메모"] = "; ".join(part for part in (row["메모"], text) if part)


def main():
    columns, rows = read_csv(V3)
    assert len(rows) == 55_997 and len(columns) == 26
    assert len({row["행번호"] for row in rows}) == len(rows)
    by_number = {row["행번호"]: row for row in rows}
    before = Counter(row["모수 포함 여부"] for row in rows)
    assert before == {"포함": 10_549, "제외": 45_448}

    changed = set()
    counts = Counter()
    for label, country, retailer, expected, source in REVIEWS:
        review_columns, review_rows = read_csv(source)
        assert review_columns[:26] == columns, source
        assert len(review_rows) == expected, (label, len(review_rows))
        for review in review_rows:
            number = review["행번호"]
            assert number not in changed, number
            assert number in by_number, number
            row = by_number[number]
            assert all(review[column] == row[column] for column in columns), number
            assert row["국가"] == country and row["리테일러"] == retailer, number
            assert row["모수 포함 여부"] == "포함", number
            assert review["변경요청_모수 포함 여부"] == "제외", number

            row["모수 포함 여부"] = "제외"
            if label == "Sharaf DG":
                seller = review["현재_본상품_판매자"].strip()
                assert seller and seller.casefold() != "sharaf dg", number
                row["제외단계"] = "③리리부"
                row["제외사유"] = f"외부 판매자 ({seller}; 두레이 #157, 2026-11-05 화면 확인)"
                row["판매자"] = seller
                row["판매자구분"] = "외부판매자"
                row["판매자근거"] = f"2026-11-05 정확한 상품 URL의 본 상품 Sold by {seller} (내부 브라우저 확인)"
                append_memo(row, "두레이 #157: 2026-11-05 본 상품 판매자 재확인으로 포함→제외; 10월 당시 판매자는 미확인")
            elif label == "eXtra":
                assert review["상품화면_확인문구"] == "هذا المنتج حاليًا / غير متوفر حاليًا", number
                assert review["상품화면_장바구니버튼"] == "N", number
                row["제외단계"] = "④품절"
                row["제외사유"] = "2026-11-05 상품 화면에 품절 두 문구 표시(두레이 #158)"
                append_memo(row, "두레이 #158: 2026-11-05 상품 화면 품절 문구 직접 확인으로 포함→제외; 10월 당시 상태는 미확인")
            else:
                assert "NGƯNG KINH DOANH" in review["현재_중단문구_원문"], number
                row["제외단계"] = "④판매중단"
                row["제외사유"] = "2026-11-05 상품 판매 영역에 NGƯNG KINH DOANH 표시(두레이 #159)"
                append_memo(row, "두레이 #159: 2026-11-05 상품 화면 판매 중단 표시로 포함→제외; 10월 당시 상태는 미확인")
            changed.add(number)
            counts[label] += 1

    assert counts == {"Sharaf DG": 9, "eXtra": 129, "DIENMAYXANH": 183}
    assert len(changed) == 321
    after = Counter(row["모수 포함 여부"] for row in rows)
    assert after == {"포함": 10_228, "제외": 45_769}
    assert not V4.exists(), f"v4 already exists: {V4}"
    with V4.open("x", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)
    print(f"created {V4}: {len(rows)} rows, {len(columns)} columns, changed={dict(counts)}, status={dict(after)}")


if __name__ == "__main__":
    main()
