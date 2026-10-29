"""추가한 상품별 화면 기록에서 조사 범위·실패·이름 차이를 갱신한다. 원본 CSV 수정 없음."""
import csv
from collections import Counter
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def is_no_product_screen(record):
    page = record.get('pageEvidence') or {}
    title = page.get('title', '').strip()
    explicit = title.lower().startswith('sorry! this product is no longer available') or 'ไม่พบรายการสินค้า' in title or title == 'ค้นหาหน้าไม่พบ'
    return bool(explicit and 'Oops' in page.get('bodyText', '') and not page.get('heading')
                and not any(d.get('primaryKey') for d in record.get('identifiers', [])))


def save_csv(name, rows, columns):
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main():
    jobs = json.loads((OUT / 'page_jobs.json').read_text())
    seen, successes, live_seen, live_successes = {}, {}, {}, {}
    files = [OUT / 'archived_pages.jsonl', OUT / 'live_pages.jsonl']
    combined = []
    for source in files:
        if not source.exists():
            continue
        for line in source.open():
            record = json.loads(line)
            combined.append(record)
            key = record['country'], record['itemId']
            seen[key] = record
            if record['ok']:
                successes[key] = record
            if source.name == 'live_pages.jsonl':
                live_seen[key] = record
                if record['ok']:
                    live_successes[key] = record
    (OUT / 'product_evidence.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in combined))
    coverage = []
    for job in jobs:
        key = job['country'], job['itemId']
        record = successes.get(key) or seen.get(key)
        if key in live_successes:
            status = '상품별 확인'
        elif key in successes:
            status = '저장화면 확인'
        elif record and is_no_product_screen(record):
            status = '상품없음 화면(판매자미확인)'
        elif record and '/_____tmd_____/' in record.get('actualUrl', ''):
            status = '보안 확인 차단'
        elif record:
            status = '판매자 검증 미완료'
        else:
            status = '미방문'
        coverage.append({
            '국가': job['country'], '상품ID': job['itemId'], 'URL': job['url'],
            '연결된CSV행수': job['sourceRows'], '상태': status, '기존판매자': job['oldSeller'],
            '확인방법': '이번 브라우저 확인' if key in live_successes else ('그 상품의 기존 저장화면 확인' if key in successes else ''),
            '확인판매자': record.get('sellerName', '') if record else '',
            '확인매장': next((a['href'].split('?')[0] for a in record.get('shopLinks', [])
                              if a['text'] == record.get('sellerName') and a['href']), '') if record else '',
        })
    columns = list(coverage[0])
    save_csv('상품별_확인범위.csv', coverage, columns)
    success_states = ('상품별 확인', '저장화면 확인')
    failed = [r for r in coverage if r['상태'] not in (*success_states, '미방문')]
    save_csv('재확인실패_목록.csv', failed, columns)
    differences = [r for r in coverage if r['상태'] in success_states and r['기존판매자'] != r['확인판매자']]
    save_csv('상품별_이름차이.csv', differences, columns)
    applied_receipt = OUT / '적용_3eac9d79/적용검증.json'
    applied = False
    if applied_receipt.exists():
        receipt = json.loads(applied_receipt.read_text())
        applied = receipt.get('status') == 'PASS' and receipt.get('apply_executed') is True
    summary = {
        '대상상품ID': len(jobs), '대상URL행': sum(j['sourceRows'] for j in jobs),
        '실제방문상품ID': len(live_seen), '근거검토상품ID': len(seen), '확인성공상품ID': len(successes),
        '이번브라우저확인상품ID': len(live_successes), '기존저장화면확인상품ID': len(successes) - len(live_successes),
        '확인성공URL행': sum(r['연결된CSV행수'] for r in coverage if r['상태'] in success_states),
        '실패상품ID': len(seen) - len(successes), '미방문상품ID': len(jobs) - len(seen),
        '상태별상품수': dict(Counter(r['상태'] for r in coverage)),
        '국가별확인성공': dict(Counter(r['국가'] for r in coverage if r['상태'] in success_states)),
        '모든대상근거검토완료': len(seen) == len(jobs),
        '상품없음화면상품ID': sum(r['상태'] == '상품없음 화면(판매자미확인)' for r in coverage),
        '상품없음화면URL행': sum(r['연결된CSV행수'] for r in coverage if r['상태'] == '상품없음 화면(판매자미확인)'),
        '이름차이상품ID': len(differences), '이름차이URL행': sum(r['연결된CSV행수'] for r in differences),
        '확정오류': {'상품ID': 16, 'CSV행': 30, '수정': 'Samsung → LG', '판정': '기존 제외 유지'},
        '실제CSV적용': applied,
        '적용검증': '적용_3eac9d79/적용검증.json' if applied else None,
        '비고': '이번 브라우저 확인과 그 상품 자체의 기존 저장화면 확인을 구분한다. 사용자 요청으로 2개에서 3개, 최종 5개 탭으로 병렬 확인했다. 판매자 번호가 같다는 이유로 다른 상품에 이름을 전파하지 않는다. 상품없음 화면의 3상품은 판매자를 확인한 것으로 세지 않는다.',
    }
    (OUT / '확인범위_요약.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
