import collections
import csv
import json
import re
from pathlib import Path


root = Path(__file__).resolve().parents[2]
source = root / 'pdp 모수 추출/최종_20261029/PDP모수_공유용_v3_EY검토반영_25개국_35개리테일러_전체판정_55997행_20261031.csv'
with source.open(encoding='utf-8-sig', newline='') as handle:
    rows = list(csv.DictReader(handle))

matched = [
    row for row in rows
    if row['모수 포함 여부'] == '제외'
    and row['제외단계'] == '③리리부'
    and '제외키워드 시트' in row['제외사유']
]
detail_by_key = {}
for row in matched:
    match = re.fullmatch(r'(.+) 단어 "(.+)"\(제외키워드 시트\)', row['제외사유'])
    if not match:
        raise ValueError(f"Unexpected exclusion reason in row {row['행번호']}")
    key = (row['국가'], row['리테일러'], row['확인 요청 URL'])
    detail_by_key.setdefault(key, match.group(2))
    if detail_by_key[key] != match.group(2):
        raise ValueError(f'Conflicting matched keywords for {key}')

countries = sorted({row['국가'] for row in rows})
country_counts = collections.Counter(country for country, _, _ in detail_by_key)
countries.sort(key=lambda country: (-country_counts[country], country))
details = [list(key) + [word] for key, word in detail_by_key.items()]
country_order = {country: index for index, country in enumerate(countries)}
details.sort(key=lambda row: (country_order[row[0]], row[1], row[2]))

payload = {
    'countries': countries,
    'details': details,
    'matched_rows': len(matched),
    'duplicate_rows': len(matched) - len(details),
    'source': source.name,
}
target = Path('/tmp/riribu-keyword-effect-d0bfd680.json')
target.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
print(f"{len(details)} unique URLs; {len(matched)} source rows; {len(countries)} countries")
