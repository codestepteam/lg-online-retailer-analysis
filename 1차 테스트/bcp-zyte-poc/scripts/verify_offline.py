#!/usr/bin/env python3
"""Audit static offline references without opening local files in a browser."""
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from offline_assets import CSS_IMPORT_RE, CSS_URL_RE, _split_srcset


def verify(view):
    view = view.resolve()
    issues = set()
    checked = set()

    def reference(value, parent):
        value = (value or '').strip()
        if not value or value.startswith(('#', 'data:', 'about:')):
            return
        u = urlsplit(value)
        if u.scheme or u.netloc:
            issues.add(('external_resource', str(parent.relative_to(view)), value[:240]))
            return
        target = (parent.parent/unquote(u.path)).resolve()
        if not target.is_relative_to(view):
            issues.add(('outside_view', str(parent.relative_to(view)), value))
        elif not target.is_file():
            issues.add(('missing_file', str(parent.relative_to(view)), value))
        else:
            checked.add(target)

    def css(text, parent):
        for match in CSS_URL_RE.finditer(text):
            reference(match.group('url'), parent)
        for match in CSS_IMPORT_RE.finditer(text):
            reference(match.group(3), parent)

    class Parser(HTMLParser):
        def __init__(self, path):
            super().__init__()
            self.path, self.in_style = path, False

        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            if tag == 'style':
                self.in_style = True
            if any(k.startswith('on') for k in a):
                issues.add(('event_handler', str(self.path.relative_to(view)), tag))
            script_type = (a.get('type') or '').lower().strip()
            if tag == 'script' and (not script_type or script_type in {'module','speculationrules','text/jscript','text/livescript'} or 'javascript' in script_type or 'ecmascript' in script_type):
                issues.add(('active_script', str(self.path.relative_to(view)), a.get('type','inline')))
            if tag == 'base':
                issues.add(('base_tag', str(self.path.relative_to(view)), str(a.get('href'))))
            resource_attrs = {
                'img':['src'], 'source':['src'], 'iframe':['src'], 'video':['src','poster'],
                'audio':['src'], 'track':['src'], 'embed':['src'], 'object':['data'],
                'image':['href','xlink:href'], 'use':['href','xlink:href'], 'feimage':['href','xlink:href'],
            }.get(tag, [])
            if tag == 'input' and a.get('type') == 'image':
                resource_attrs = ['src']
            if tag == 'link' and set((a.get('rel') or '').split()) & {'stylesheet','icon','apple-touch-icon','mask-icon','preload','modulepreload','prefetch'}:
                resource_attrs = ['href']
            for key in resource_attrs:
                reference(a.get(key), self.path)
            for key in ['srcset','imagesrcset']:
                for src, _ in _split_srcset(a.get(key) or ''):
                    reference(src, self.path)
            for value in a.values():
                if value and 'url(' in value:
                    css(value, self.path)

        handle_startendtag = handle_starttag

        def handle_endtag(self, tag):
            if tag == 'style':
                self.in_style = False

        def handle_data(self, data):
            if self.in_style:
                css(data, self.path)

    index = view/'index.html'
    if not index.exists():
        return {'view':str(view),'ok':False,'issues':[['missing_index','','']]}
    for path in [index, *sorted((view/'frames').glob('*.html'))]:
        Parser(path).feed(path.read_text())
    for path in (view/'assets').glob('*.css'):
        css(path.read_text(),path)
    manifest = json.loads((view/'manifest.json').read_text())
    for failure in manifest.get('failures', []):
        if failure.get('kind') == 'stylesheet' or urlsplit(failure.get('url','')).path.lower().endswith('.css'):
            issues.add(('missing_stylesheet', 'manifest.json', failure.get('url','')[:240]))
    for asset in manifest['assets']:
        path = view/asset['path']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != asset['sha256']:
            issues.add(('asset_hash_mismatch',asset['path'],''))
    result = {'view':str(view),'ok':not issues,'references_checked':len(checked),
              'asset_download_failures':manifest['stats']['failure_count'],'issues':[list(i) for i in sorted(issues)],
              'browser_visual_verified':False}
    (view/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('view',type=Path,nargs='+')
    args=parser.parse_args()
    results=[verify(p) for p in args.view]
    print(json.dumps([{**r,'issues':r['issues'][:8]} for r in results],ensure_ascii=False,indent=2))
    raise SystemExit(0 if all(r['ok'] for r in results) else 1)
