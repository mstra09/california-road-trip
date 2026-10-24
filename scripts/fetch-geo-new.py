"""Add Macrostrat bedrock samples (every 1.5 km) for segments not yet in cache/geo/macrostrat.json."""
import json, subprocess, math
from concurrent.futures import ThreadPoolExecutor
roads = json.load(open('data/roads.json')); geo = json.load(open('cache/geo/macrostrat.json'))
have = {g['seg'] for g in geo}
samples = []
for s in roads['segments']:
    if s['id'] in have: continue
    nxt = 0
    for p, d in zip(s['pts'], s['dist']):
        if d >= nxt: samples.append((s['id'], d, p)); nxt = d + 1500
def get(x):
    seg, d, p = x
    url = f'https://macrostrat.org/api/v2/geologic_units/map?lat={p[0]}&lng={p[1]}&scale=large'
    for _ in range(4):
        try:
            j = json.loads(subprocess.run(['curl', '-s', '--max-time', '30', url], capture_output=True).stdout)
            u = (j.get('success', {}).get('data') or [None])[0]
            if not u: return None
            return {'seg': seg, 's': d, 'lat': p[0], 'lon': p[1], 'name': u['name'], 'strat': u.get('strat_name'), 'age': u.get('age'), 'lith': u.get('lith'),
                    'descrip': u.get('descrip'), 'b': u.get('b_int_name'), 't': u.get('t_int_name'), 'src': u.get('source_id'), 'map_id': u.get('map_id')}
        except Exception: pass
with ThreadPoolExecutor(4) as ex: new = [g for g in ex.map(get, samples) if g]
geo += new; geo.sort(key=lambda a: (a['seg'], a['s']))
json.dump(geo, open('cache/geo/macrostrat.json', 'w'))
print(len(samples), 'samples,', len(new), 'added')
