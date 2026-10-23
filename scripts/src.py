"""Print cached source articles, trimmed of boilerplate sections. Usage: src.py [-n MAXWORDS] title..."""
import json, re, sys, os
args = sys.argv[1:]; maxw = 1400
if args and args[0] == '-n': maxw = int(args[1]); args = args[2:]
DROP = re.compile(r'^(References|External links|See also|Notes|Further reading|Gallery|Demographics|Education|Notable people|Sister cities|Government|Politics|Sports|Climate|Media|Census|20\d\d census|Bibliography|Sources|Footnotes|Citations|Twin towns.*|In popular culture|Awards|Infrastructure|Public safety|Schools|Libraries|Notable residents|Arts and culture|Parks and recreation|Representation|Economy|Wines|Wineries|Producers|Rankings)$', re.I)
def slug(t): return re.sub(r'^_|_$', '', re.sub(r'[^\w]+', '_', t))
for t in args:
    f = f'cache/wiki/pages/{slug(t)}.json'
    if not os.path.exists(f): print(f'### {t}: NOT CACHED\n'); continue
    d = json.load(open(f)); out = []; skip = False
    for line in d['text'].split('\n'):
        m = re.match(r'^(=+)\s*(.*?)\s*=+$', line)
        if m:
            lvl = len(m.group(1)); skip = bool(DROP.match(m.group(2))) if lvl == 2 else (skip or bool(DROP.match(m.group(2))))
            if not skip: out.append('## ' + m.group(2))
            continue
        if not skip and line.strip(): out.append(line.strip())
    words = ' \n'.join(out).split(' ')
    print(f"### {d['title']}  <{d['url']}>\n" + ' '.join(words[:maxw]) + ('' if len(words) <= maxw else ' […]') + '\n')
