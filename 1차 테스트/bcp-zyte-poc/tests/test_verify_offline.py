import json
import sys
import tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from verify_offline import verify

with tempfile.TemporaryDirectory() as directory:
    view=Path(directory)
    (view/'assets').mkdir()
    (view/'assets/pixel.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
    (view/'manifest.json').write_text(json.dumps({'assets':[],'stats':{'failure_count':0}}))
    (view/'index.html').write_text('<img src="assets/pixel.svg"><script type="application/json">{}</script>')
    assert verify(view)['ok']
    (view/'index.html').write_text('<img src="missing.png"><link rel="preload" as="script" href="https://example.org/app.js"><script>alert(1)</script>')
    failures={item[0] for item in verify(view)['issues']}
    assert failures=={'missing_file','external_resource','active_script'},failures
print('offline reference audit: ok')
