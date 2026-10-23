"""Fact-check helpers.

  python3 scripts/factcheck.py numbers      -> every number/year in each clip must appear in its cited sources
  python3 scripts/factcheck.py sample N SEED -> print N random clips, sentence by sentence, each with the
                                               best-matching sentence from its sources, for manual review
"""
import json, os, re, sys, random, urllib.parse, glob

pages = {}
for f in glob.glob('cache/wiki/pages/*.json'):
    d = json.load(open(f))
    key = urllib.parse.unquote(d['url'].split('/wiki/')[-1]).replace('_', ' ').lower()
    pages[key] = d['text']
    pages[d['title'].lower()] = d['text']
geo = json.load(open('cache/geo/macrostrat.json'))

def source_text(url):
    if 'macrostrat.org' in url:
        m = re.search(r'lat=([\d.-]+)&lng=([\d.-]+)', url)
        la, lo = float(m.group(1)), float(m.group(2))
        b = min(geo, key=lambda x: (x['lat'] - la) ** 2 + (x['lon'] - lo) ** 2)
        return f"{b['name']}. {b.get('descrip') or ''} {b.get('b')} {b.get('t')} {b.get('lith') or ''}"
    key = urllib.parse.unquote(url.split('/wiki/')[-1]).replace('_', ' ').lower()
    return pages.get(key, '')

clips = []
for f in sorted(glob.glob('content/[0-9]*.json')):
    doc = json.load(open(f))
    for c in doc['clips']:
        clips.append(c)
        if c.get('more'):
            m = dict(c['more']); m.setdefault('id', c['id'] + '_more'); m.setdefault('sources', c['sources']); clips.append(m)

WORDNUM = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12,
           'thirteen': 13, 'fifteen': 15, 'sixteen': 16, 'eighteen': 18, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
           'seventy-five': 75, 'eighty': 80, 'ninety': 90, 'hundred': 100, 'thousand': 1000}

def nums(text):
    out = set()
    for m in re.finditer(r'(?<![\w.])(\d[\d,]*(?:\.\d+)?)', text):
        out.add(m.group(1).replace(',', ''))
    return out

def mode_numbers():
    bad = 0
    for c in clips:
        src = ' '.join(source_text(u) for u in c.get('sources', []))
        srcn = set(x.replace(',', '') for x in re.findall(r'\d[\d,]*(?:\.\d+)?', src))
        missing = [n for n in nums(c['text']) if n not in srcn and n.rstrip('0').rstrip('.') not in srcn]
        if missing:
            bad += 1
            print(f"{c['id']:24s} not found in sources: {', '.join(sorted(missing))}")
    print(f'\n{bad} clips with numbers not found verbatim in their sources (review each: some are derived, e.g. unit conversions or arithmetic)')

def mode_sample(n, seed):
    random.seed(seed)
    for c in random.sample(clips, n):
        src = ' '.join(source_text(u) for u in c.get('sources', []))
        ss = [s.strip() for s in re.split(r'(?<=[.!?])\s+', src) if len(s) > 20]
        print('=' * 100); print(f"[{c['id']}] {c['title']}")
        for sent in re.split(r'(?<=[.!?])\s+', c['text'].replace('\n', ' ')):
            if len(sent) < 25: continue
            words = set(w.lower() for w in re.findall(r'[A-Za-z]{4,}|\d+', sent))
            best = max(ss, key=lambda s: len(words & set(w.lower() for w in re.findall(r'[A-Za-z]{4,}|\d+', s))), default='')
            print(f"  CLIP: {sent}\n   SRC: {best[:300]}")

if sys.argv[1] == 'numbers': mode_numbers()
else: mode_sample(int(sys.argv[2]), int(sys.argv[3]))
