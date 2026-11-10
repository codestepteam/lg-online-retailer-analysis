"""리테일러별 판매자 함수 목록. 어느 리테일러가 어느 함수를 쓰는지는 retailer_rules.json의 sellers.functions에 적는다."""
from . import group1, group2, group3, group4
from .mediamarkt_screen import mediamarkt_screen

FUNCTIONS = {
    "mediamarkt_screen": mediamarkt_screen,
    "boulanger": group1.boulanger, "darty": group1.darty, "el_corte_ingles": group1.el_corte_ingles, "mediamarkt_es_nl": group1.mediamarkt_es_nl, "worten": group1.worten, "coolblue": group1.coolblue,
    "mediamarkt_saturn": group2.mediamarkt_saturn, "mediamarkt_de": group2.mediamarkt_de, "otto": group2.otto, "unieuro": group2.unieuro,
    "alza": group3.alza, "datart": group3.datart, "media_expert": group3.media_expert, "rtv_euro_agd": group3.rtv_euro_agd, "elgiganten": group3.elgiganten, "currys": group3.currys, "ao": group3.ao,
    "appliance_online": group4.appliance_online, "costco": group4.costco, "cairo_sales": group4.cairo_sales, "electroplanet": group4.electroplanet, "extra": group4.extra, "sharaf": group4.sharaf,
    "liverpool": group4.liverpool, "lazada": group4.lazada, "dienmayxanh": group4.dienmayxanh, "falabella": group4.falabella, "magalu": group4.magalu,
}
# 다른 페이지에서 모은 값이 필요한 함수: (판정 함수, 먼저 돌릴 수집 함수)
CONTEXT_FUNCTIONS = {"amazon": (group2.amazon, group2.amazon_collect), "momo": (group4.momo, group4.momo_collect)}
