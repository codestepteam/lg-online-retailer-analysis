"""검색 행의 브랜드·제품코드 추출. 어느 리테일러가 어느 함수를 쓰는지는 product_codes.json의 retailers에 적는다."""
from collections import defaultdict

from common import ConfigError

from . import retailers

FUNCTIONS = {name: getattr(retailers, name) for name in ("alza", "datart", "worten", "rtv_euro_agd", "media_expert", "sharaf", "appliance_online", "falabella", "cairo_sales", "electroplanet", "mediamarkt")}


def check_config(config):
    unknown = {item["function"] for item in config["retailers"].values()} - set(FUNCTIONS)
    if unknown:
        raise ConfigError(f"설정에 있는 제품코드 함수가 코드에 없습니다: {sorted(unknown)}")


def extract(rows, read, config):
    """리테일러별로 묶어 추출한다. {행번호: (브랜드, 제품코드, 브랜드 찾은곳, 제품코드 찾은곳)}."""
    check_config(config)
    groups, found = defaultdict(list), {}
    for row in rows:
        groups[f"{row['국가']}|{row['리테일러']}"].append(row)
    for shop, members in groups.items():
        if shop not in config["retailers"]:
            raise ConfigError(f"product_codes.json에 없는 검색 리테일러입니다: {shop}")
        words = {**config["shared"], **config["retailers"][shop]}
        found.update(FUNCTIONS[words["function"]](members, read, words))
    return found
