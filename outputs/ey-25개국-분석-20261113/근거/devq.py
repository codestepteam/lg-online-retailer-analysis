"""개발 GCP Cloud SQL 읽기 전용 조회 (대시보드의 read_only_session 재사용). 사용: devq.py "<SELECT ...>" [out.jsonl]"""
import json, os, sys
D = '/Users/codestepseunghee/codestep/lge-hs-clinic-dashboard/backend'
for line in open(D + '/.env', encoding='utf-8'):
    line = line.strip()
    if line and not line.startswith('#') and '=' in line:
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'").strip('"') if not v.strip().startswith('{') else v.strip())
sys.path.insert(0, D)
from app.data.db import read_only_session
sql = sys.argv[1]
assert sql.lstrip().lower().startswith(('select', 'with')), '읽기 전용 SELECT만'
with read_only_session() as cur:
    cur.execute(sql)
    rows = cur.fetchall(); cols = [d[0] for d in cur.description]
if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(dict(zip(cols, r)), default=str, ensure_ascii=False) + '\n')
    print(len(rows), 'rows ->', sys.argv[2])
else:
    print(' | '.join(cols))
    for r in rows[:200]:
        print(' | '.join('' if v is None else str(v) for v in r))
    print(f'({len(rows)}행)')
