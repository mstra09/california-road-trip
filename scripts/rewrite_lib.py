"""Shared helper for the persona rewrite scripts: replace clip texts by id ('id' or 'id.more')."""
import json

def apply(path, texts):
    d = json.load(open(path))
    done = set()
    for c in d['clips']:
        if c['id'] in texts:
            c['text'] = texts[c['id']].strip(); done.add(c['id'])
        if c.get('more') and c['id'] + '.more' in texts:
            c['more']['text'] = texts[c['id'] + '.more'].strip(); done.add(c['id'] + '.more')
    missing = set(texts) - done
    if missing: raise SystemExit(f'{path}: unknown ids {missing}')
    json.dump(d, open(path, 'w'), indent=1, ensure_ascii=False)
    print(f'{path}: rewrote {len(done)} texts')
