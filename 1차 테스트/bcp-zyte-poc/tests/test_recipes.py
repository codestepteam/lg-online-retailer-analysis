"""Runnable checks for the 14 x 5 standalone Zyte request contract."""
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from zyte_capture import _recipe_request, _capture_state, _capture_state_errors

files = list((ROOT/'capture/recipes').glob('*/*.json'))
assert len(files) == 70, f'Expected 70 recipes, found {len(files)}'
expected = {'home','brand','brand-category','plp','pdp'}
retailers = {p.parent.name for p in files}
assert len(retailers) == 14
for retailer in retailers:
    assert {p.stem for p in files if p.parent.name == retailer} == expected
for path in files:
    recipe = json.loads(path.read_text())
    request = recipe['request']
    assert urlsplit(request['url']).scheme == 'https'
    assert request['browserHtml'] and request['screenshot']
    assert request == _recipe_request(recipe, ROOT), 'Standalone request differs from runner request'
    actions = request['actions']
    assert actions[-1]['source'] == (ROOT/'capture/prepare.js').read_text()
    assert actions[-2]['source'] == (ROOT/'capture/evidence.js').read_text()
    hero = [i for i, action in enumerate(actions) if 'id18-candidates-v1' in action.get('source', '')]
    if path.stem == 'brand-category':
        load = next(i for i, action in enumerate(actions) if 'window.__lgCapture = log' in action.get('source', ''))
        assert len(hero) == 2 and hero[0] < load < hero[1] < len(actions) - 2
        assert 'const phase = "before_scroll"' in actions[hero[0]]['source']
        assert 'const phase = "after_scroll"' in actions[hero[1]]['source']
    else:
        assert not hero, 'ID18 evidence belongs to Brand Category Pages only'
    assert any('window.__lgConfig =' in a.get('source','') for a in actions)
    assert all(len(a.get('source','')) <= 6000 for a in actions)
    assert not any('const cfg = CONFIG;' in a.get('source','') for a in actions)
    assert not any('const steps = COOKIE_STEPS;' in a.get('source','') for a in actions)
state = {'ready': True, 'finishedAt': '2026-09-22T00:00:00Z',
         'required': [{'selector': '.specification-details', 'expected': 'visible', 'present': False}]}
state_html = lambda: '<script id="lg-capture-state">' + json.dumps(state) + '</script>'
assert _capture_state_errors(state_html()), 'Hidden required content must reject the capture'
state['required'][0]['present'] = True
assert not _capture_state_errors(state_html())
state['steps'] = [{'panel': 'reviews', 'status': 'missing'}]
assert _capture_state_errors(state_html()), 'A loading-only panel must not be accepted'
state['steps'] = []
state['error'] = 'Viewport narrower than required'
assert _capture_state_errors(state_html()), 'Wrong viewport must reject the capture'
state['error'] = None
state['requireScrollBottom'] = True
state['scroll'] = {'reachedBottom': False}
assert _capture_state_errors(state_html()), 'Incomplete required scrolling must reject the capture'
state['scroll']['reachedBottom'] = True
assert not _capture_state_errors(state_html())
assert _capture_state(state_html())['scroll']['reachedBottom'] is True
print('70 standalone Zyte recipes and visible-content completion contract: ok')
