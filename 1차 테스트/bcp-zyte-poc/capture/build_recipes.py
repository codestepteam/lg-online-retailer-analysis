"""Compile inspected retailer/page settings into standalone Zyte API requests."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COUNTRIES = {'eci':'ES','mediamarkt-es':'ES','darty':'FR','boulanger':'FR','mediaworld':'IT','amazon-it':'IT','unieuro':'IT','coolblue':'NL','mediamarkt-nl':'NL','elgiganten':'SE','media-expert':'PL','rtv-euro-agd':'PL','datart':'CZ','alza':'CZ'}

def build():
    configs = {}
    for path in sorted(ROOT.glob('configs-*.json')):
        configs.update(json.loads(path.read_text()))
    entries = json.loads((ROOT.parent/'output/_poc_zyte/url-manifest.json').read_text())['entries']
    load = (ROOT/'load.js').read_text().replace('const cfg = CONFIG;', 'const cfg = window.__lgConfig;')
    evidence = (ROOT/'evidence.js').read_text()
    count = 0
    for entry in entries:
        retailer, page_type = entry['retailer_slug'], entry['page_type']
        if page_type not in configs.get(retailer, {}):
            continue
        config = dict(configs[retailer][page_type])
        config.update(retailer=retailer, page_type=page_type)
        cookies = config.pop('cookies', [])
        config['cookie_checks'] = cookies
        cookie_actions = []
        if cookies:
            cookie_source = (ROOT/'cookies.js').read_text().replace('COOKIE_STEPS', json.dumps(cookies,ensure_ascii=False))
            cookie_actions = [{'action':'evaluate','source':cookie_source}, {'action':'waitForTimeout','timeout':1.5}]
        initial_metadata_actions = [{'action':'evaluate','source':(ROOT/'initial-metadata.js').read_text()}] if page_type == 'brand-category' else []
        faq_actions = ([{'action':'evaluate','source':(ROOT/'faq_expand.js').read_text()}]
                       if retailer == 'mediamarkt-es' and page_type == 'brand-category' else [])
        actions = cookie_actions + [
            {'action':'evaluate','source':'window.__lgConfig = '+json.dumps(config,ensure_ascii=False)+';'},
        ] + initial_metadata_actions + [
            {'action':'evaluate','source':load},
        ] + faq_actions + [
            {'action':'evaluate','source':evidence},
            {'action':'evaluate','source':(ROOT/'prepare.js').read_text()},
        ]
        target_url = config.get('url',entry['url'])
        if config.get('entry_url'):
            actions = cookie_actions + [{'action':'goto','url':target_url,'options':{'waitUntil':'load','timeout':25}}, {'action':'waitForTimeout','timeout':2}] + actions
        assert all(len(a.get('source','')) <= 6000 for a in actions)
        recipe = {'retailer':retailer,'page_type':page_type,'evidence':config.get('evidence','See output/offline-review browser observations.'),
                  'request':{'url':(config.get('entry_url') or target_url), 'browserHtml':True, 'screenshot':True, 'viewport':{'width':1920,'height':1080},
                             'screenshotOptions':{'fullPage':True,'format':'jpeg'}, 'geolocation':config.get('geolocation',COUNTRIES[retailer]), 'actions':actions}}
        if config.get('entry_url'):
            recipe['target_url'] = target_url
        if config.get('geolocation', COUNTRIES[retailer]) is None:
            recipe['request'].pop('geolocation', None)
        path = ROOT/'recipes'/retailer/(page_type+'.json')
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(recipe,ensure_ascii=False,indent=2)+'\n')
        count += 1
    print(f'Compiled {count} recipes')

if __name__ == '__main__':
    build()
