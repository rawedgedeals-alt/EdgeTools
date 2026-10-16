#!/usr/bin/env python3
"""Commit crawlable directory HTML whenever tools.json is changed."""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]


def render():
    products = sorted(json.loads((ROOT / 'tools.json').read_text()), key=lambda p: p['name'].lower())
    e = html.escape
    cards = []
    for p in products:
        if not p['url'].startswith('https://'):
            raise ValueError('Provider links must use HTTPS')
        cards.append(
            '<article class="card"><span class="tag">' + e(p['category'].upper()) + '</span>'
            '<h3>' + e(p['name']) + '</h3><div class="best">GOOD FOR: ' + e(p.get('bestFor', '')) + '</div>'
            '<p>' + e(p['description']) + '</p><a href="' + e(p['url'], quote=True) + '" '
            'target="_blank" rel="noopener noreferrer" aria-label="Visit ' + e(p['name'], quote=True) +
            ' website in a new tab">EXPLORE ' + e(p['name'].upper()) + ' →</a></article>')
    path = ROOT / 'index.html'
    text = path.read_text()
    for marker, content in [('DIRECTORY', '\n'.join(cards)), ('COUNT', f'{len(products)} of {len(products)} tools')]:
        pattern = rf'<!-- {marker}:START -->.*?<!-- {marker}:END -->'
        text, count = re.subn(pattern, lambda _: f'<!-- {marker}:START -->{content}<!-- {marker}:END -->', text, flags=re.S)
        if count != 1:
            raise ValueError(f'Expected one {marker} placeholder')
    path.write_text(text)


if __name__ == '__main__':
    render()
