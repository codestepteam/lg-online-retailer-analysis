"""저장 HTML만 읽어 Lazada 판매자 번호 연결을 점검한다. 외부 호출·원본 수정 없음."""
import argparse
import collections
import csv
import gzip
import json
import re
from pathlib import Path


def extract(html):
    primary = re.search(r'"primaryKey":(\{.*?\}),"requestHost"', html)
    if not primary:
        raise ValueError('본 상품 primaryKey 없음')
    key = json.loads(primary[1])
    sub = re.findall(r'seller_sub_id=(\d+)', html)
    if len(set(sub)) > 1:
        raise ValueError('seller_sub_id 복수 값')
    first = re.search(r'"sellerId":"(\d+)"', html)
    return key['itemId'], key['sellerId'], sub[0] if sub else '', first[1] if first else ''


def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='임시 작업 zyte_full 폴더')
    args = parser.parse_args()
    out = Path(__file__).resolve().parent
    evidence = out.parent / '최종_20261029' / '판정근거'
    # 가짜 입력: 추천 상품 번호가 앞에 있어도 본 상품을 고르고, 공유 번호를 구분한다.
    fake = '"sellerId":"999";"primaryKey":{"itemId":"1","sellerId":"100"},"requestHost":"test";seller_sub_id=200'
    assert extract(fake) == ('1', '100', '200', '999')
    assert extract(fake.replace('sub_id=200', 'sub_id=201'))[:2] == extract(fake)[:2]
    assert extract(fake.replace('sub_id=200', 'sub_id=201'))[2] != extract(fake)[2]
    old_sellers = {r['요청URL']: r for r in csv.DictReader((evidence / '판매자판정/seller_lazada.csv').open(encoding='utf-8-sig'))}
    final_file = next((out.parent / '최종_20261029').glob('*56071*.csv'))
    final_rows = list(csv.DictReader(final_file.open(encoding='utf-8-sig')))
    final_lazada = [r for r in final_rows if r['리테일러'] == 'LAZADA']
    rows = []
    for line in (evidence / '페이지확인/pages_best.jsonl').open():
        d = json.loads(line)
        if d['리테일러'] != 'LAZADA' or d['페이지상태'] != '정상':
            continue
        source = args.source / (d.get('_dir') or 'html') / d['HTML파일']
        html = gzip.open(source, 'rt', encoding='utf-8').read()
        error = ''
        try:
            item, seller, sub, first = extract(html)
        except ValueError as exc:
            item = re.search(r'-i(\d+)', d['요청URL'])[1]
            seller = sub = first = ''
            error = str(exc)
        assert re.search(r'-i(\d+)', d['요청URL'])[1] == item
        old = old_sellers.get(d['요청URL'], {})
        rows.append({'국가': d['국가'], '요청URL': d['요청URL'], '상품ID': item,
                     'sellerId': seller, 'seller_sub_id': sub,
                     '처음찾은sellerId': first, '기존판매자': old.get('판매자', ''),
                     '기존구분': old.get('판매자구분', ''), '제목': d['제목'],
                     '원본HTML파일': str(source), '번호추출오류': error})
    groups = collections.defaultdict(list)
    for row in rows:
        groups[(row['국가'], row['sellerId'])].append(row)
    collisions = []
    for (country, seller), members in groups.items():
        subs = {r['seller_sub_id'] for r in members if r['seller_sub_id']}
        if len(subs) > 1:
            collisions.append({'국가': country, 'sellerId': seller, 'URL행수': len(members),
                               '별도번호별': [{'seller_sub_id': sub,
                                                'URL행수': sum(r['seller_sub_id'] == sub for r in members),
                                                '상품ID수': len({r['상품ID'] for r in members if r['seller_sub_id'] == sub})}
                                               for sub in sorted(subs)]})
    affected = [r for r in rows if r['국가'] == 'Thailand' and r['sellerId'] == '100088963']
    summary = {
        '점검일': '2026-10-29', '검증방식': 'Python 표준 라이브러리로 저장 HTML primaryKey·seller_sub_id와 기존 판매자 CSV·최종 CSV 대조',
        '가짜입력검증': '추천 상품 번호 배제·같은 sellerId의 다른 sub 값 식별 3개 assertion 통과',
        '정상페이지URL행수': len(rows), '국가별': dict(collections.Counter(r['국가'] for r in rows)),
        '국가와sellerId묶음수': len(groups),
        '유효번호묶음수': sum(bool(key[1]) for key in groups),
        '빈번호묶음수': sum(not key[1] for key in groups),
        '본상품번호추출성공': sum(not r['번호추출오류'] for r in rows),
        '본상품번호추출실패': [{'요청URL': r['요청URL'], '원인': r['번호추출오류'], '제목': r['제목']} for r in rows if r['번호추출오류']],
        '처음찾은번호와본상품번호불일치': sum(r['sellerId'] != r['처음찾은sellerId'] for r in rows),
        '별도번호존재행수': sum(bool(r['seller_sub_id']) for r in rows),
        '여러별도번호가섞인묶음': collisions,
        '문제묶음기존판매자': dict(collections.Counter(r['기존판매자'] for r in affected)),
        '최종표문제번호행수': sum('sellerId 100088963,' in r['판매자근거'] for r in final_lazada),
        '최종표문제번호브랜드별': dict(collections.Counter(r['OSM브랜드'] for r in final_lazada if 'sellerId 100088963,' in r['판매자근거'])),
        '한계': ['상품별 실시간 화면은 LG 4371575857과 Samsung 160586162 두 개만 확인했다.',
                 'LG쪽 별도번호의 나머지 15개 상품 ID는 화면 판매자 미확인이다.',
                 'seller_sub_id는 46행에만 있으며 839행에는 없다. 이것만으로 전체 오류를 탐지할 수 없다. 기존 정상 분류 중 페이지 없음 1행은 본 상품 번호도 없다.',
                 'sellerId와 seller_sub_id의 Lazada 공식 업무상 정의는 확인하지 못했다.',
                 '이 스크립트는 기존 최종표·판매자 CSV를 수정하지 않는다.'],
        '검증결과': 'PASS'
    }
    assert len(rows) == 885 and len(groups) == 89 and len(affected) == 46
    assert summary['처음찾은번호와본상품번호불일치'] == 0
    assert summary['최종표문제번호브랜드별'] == {'LG': 30, 'SAMSUNG': 16}
    write_csv(out / '전체885주소_번호대조.csv', rows)
    write_csv(out / '문제번호46주소.csv', affected)
    (out / '점검결과.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
