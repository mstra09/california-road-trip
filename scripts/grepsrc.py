"""Print paragraphs of a cached source article that match any keyword. Usage: grepsrc.py title kw1 kw2 ..."""
import json, re, sys
def slug(t): return re.sub(r'^_|_$', '', re.sub(r'[^\w]+', '_', t))
d = json.load(open(f'cache/wiki/pages/{slug(sys.argv[1])}.json'))
print(f"### {d['title']} <{d['url']}>")
for para in d['text'].split('\n'):
    if any(k.lower() in para.lower() for k in sys.argv[2:]): print('-', para.strip()[:1500])
