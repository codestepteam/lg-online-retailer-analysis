#!/usr/bin/env python3
"""Review five Coolblue blocks; optionally send only these five to TypeSafe Jev."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = 'https://api.typesafe.ai/v1/systemone'
BLOCKS = {
    'block-00005': '브랜드·제품군 소개와 짧은 냉장 기능 설명',
    'block-00007': '개별 추천 상품 카드',
    'block-00011': 'No Frost·DoorCooling·Fresh Converter 설명',
    'block-00013': '리테일러 배송·설치 안내',
    'block-00016': '질문 제목은 있으나 답변은 외부 도움말 페이지로 연결',
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def api_key() -> str | None:
    key = os.environ.get('TYPESAFE_API_KEY', '').strip()
    if key:
        return key
    config = ROOT.parents[1] / '.env'
    if not config.exists():
        return None
    for line in config.read_text(encoding='utf-8').splitlines():
        name, sep, value = line.partition('=')
        if sep and name.strip() == 'TYPESAFE_API_KEY':
            return value.strip().strip('"\'') or None
    return None


def select(drafts: Path, evidence: Path) -> tuple[list[dict], dict]:
    source = json.loads(evidence.read_text(encoding='utf-8'))
    by_block = {item['block_id']: item for item in source['blocks']}
    if set(BLOCKS) - set(by_block):
        raise ValueError('선택한 Coolblue 영역을 근거 파일에서 찾지 못했습니다')
    if source['page']['retailer'] != 'coolblue' or source['quality']['capture_issues']:
        raise ValueError('Coolblue 정상 수집본만 시험할 수 있습니다')
    jobs = {}
    for line in drafts.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if item['block_id'] in BLOCKS:
            jobs[item['block_id']] = item
    if set(jobs) != set(BLOCKS):
        raise ValueError('선택한 요청 초안이 모두 존재하지 않습니다')
    for block_id in BLOCKS:
        job = jobs[block_id]
        block = by_block[block_id]
        if job['status'] != 'draft_not_sent' or block['hidden_hint'] or not block['text']:
            raise ValueError(f'{block_id}: 전송할 수 없는 영역')
        if job['payload']['state']['block']['text'] != block['text']:
            raise ValueError(f'{block_id}: 요청 초안과 근거 본문이 다릅니다')
        if set(job['payload']['questions']) != {'ID19', 'ID20', 'ID23'}:
            raise ValueError(f'{block_id}: 예상한 세 질문이 아닙니다')
    return [jobs[block_id] for block_id in BLOCKS], source


def request_jev(payload: dict, key: str) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    request = Request(ENDPOINT, data=body, headers={
        'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}, method='POST')
    for attempt in range(3):
        try:
            with urlopen(request, timeout=40) as response:
                result = json.load(response)
            break
        except HTTPError as exc:
            if exc.code in (429, 529) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f'TypeSafe HTTP {exc.code}; 자세한 내용은 공급자 응답에서 확인') from None
        except URLError as exc:
            raise RuntimeError(f'TypeSafe 네트워크 오류: {exc.reason}') from None
    if not isinstance(result, dict) or set(result.get('answers', {})) != set(payload['questions']):
        raise ValueError('TypeSafe 응답에서 세 항목의 답변을 확인하지 못했습니다')
    for name, answer in result['answers'].items():
        allowed = set(payload['questions'][name]['criteria'])
        if answer.get('type') != 'choice' or answer.get('choice') not in allowed:
            raise ValueError(f'TypeSafe {name} 응답 형식이 예상과 다릅니다')
    return result


def run(drafts: Path, evidence: Path, live: bool, output_root: Path | None = None) -> Path:
    jobs, source = select(drafts, evidence)
    key = api_key() if live else None
    if live and not key:
        raise RuntimeError('TYPESAFE_API_KEY가 없습니다. 환경변수 또는 프로젝트 루트 .env에 설정하세요.')
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output = (output_root or ROOT / 'results_jev' / 'coolblue_trial') / run_id
    output.mkdir(parents=True, exist_ok=False)
    (output / 'request-payloads.jsonl').write_text(''.join(
        json.dumps({'block_id': job['block_id'], 'payload': job['payload']}, ensure_ascii=False) + '\n'
        for job in jobs), encoding='utf-8')
    manifest = {
        'created_at_utc': run_id, 'live': live, 'api_called': False, 'status': 'prepared',
        'model_requested': jobs[0]['payload']['model'],
        'source_drafts': str(drafts.resolve()), 'source_drafts_sha256': sha256(drafts),
        'source_evidence': str(evidence.resolve()), 'source_evidence_sha256': sha256(evidence),
        'block_ids': list(BLOCKS), 'request_count': 0, 'no_page_verdict': True,
    }
    manifest_path = output / 'manifest.json'
    def save_manifest():
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    save_manifest()
    rows = []
    for job in jobs:
        block_id = job['block_id']
        try:
            result = request_jev(job['payload'], key) if live else None
        except (RuntimeError, ValueError) as exc:
            manifest['status'] = 'partial_error'
            manifest['error'] = str(exc)
            save_manifest()
            raise
        if result:
            with (output / 'responses.jsonl').open('a', encoding='utf-8') as stream:
                stream.write(json.dumps({'block_id': block_id, 'response': result}, ensure_ascii=False) + '\n')
            manifest['api_called'] = True
            manifest['request_count'] += 1
            manifest['status'] = 'partial'
            save_manifest()
        row = {'block_id': block_id, 'why_selected': BLOCKS[block_id],
               'source_path': job['source_path'], 'text': job['payload']['state']['block']['text'],
               'answers': {name: {'choice': value['choice'], 'confidence': value.get('confidence'),
                                   'probabilities': value.get('probabilities')}
                           for name, value in result['answers'].items()} if result else None}
        rows.append(row)
    (output / 'review.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = ['# Coolblue LG 냉장고: Jev 소량 시험', '',
              f'- 입력 페이지: {source["page"]["requested_url"]}',
              f'- 상태: {"Jev 실제 응답 5개 기록" if live else "요청 5개 준비, API 미호출"}',
              '- 판단 대상: Why LG(ID19), 카테고리 핵심 기술·장점(USP, ID20), 질문·답변(ID23).',
              '- 이 결과는 영역별 의미 분류다. 페이지 전체 Y/N 판정과 사람 검증은 별개다.',
              '- 점검: `block-00016`의 질문 제목은 외부 도움말로 연결되며 이 BCP 본문에는 답이 없다.', '']
    for row in rows:
        report.extend([f'## {row["block_id"]} — {row["why_selected"]}', '',
                       f'- 저장된 HTML 위치: `{row["source_path"]}`',
                       f'- 원문: {row["text"]}', ''])
        if row['answers']:
            for name, answer in row['answers'].items():
                report.append(f'- {name}: `{answer["choice"]}` (모델 confidence {answer["confidence"]})')
            report.append('')
    (output / '검토_결과.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    manifest['status'] = 'completed'
    save_manifest()
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('coolblue_result', type=Path, help='기존 results_jev 실행 결과의 coolblue 폴더')
    parser.add_argument('--live', action='store_true', help='선택한 5개 요청만 Jev에 전송')
    args = parser.parse_args()
    print(run(args.coolblue_result / 'jev-request-drafts.jsonl',
              args.coolblue_result / 'jev-evidence.json', args.live))


if __name__ == '__main__':
    main()
