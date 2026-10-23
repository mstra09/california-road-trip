// Sample every road segment every ~1 km; query Wikipedia GeoSearch (10 km radius) and the
// Macrostrat geologic map API at each sample. Results cached under cache/.
// Output: cache/wiki/candidates.json, cache/geo/macrostrat.json
import fs from 'node:fs';
const roads = JSON.parse(fs.readFileSync('data/roads.json', 'utf8'));
fs.mkdirSync('cache/wiki', { recursive: true }); fs.mkdirSync('cache/geo', { recursive: true });
const UA = { 'User-Agent': 'california-road-trip-audio-guide/1.0 (personal non-commercial; github.com/mstra09/california-road-trip)' };
const sleep = ms => new Promise(r => setTimeout(r, ms));

function hav(a, b) { const R = 6371000, r = Math.PI / 180; const dLa = (b[0] - a[0]) * r, dLo = (b[1] - a[1]) * r; const s = Math.sin(dLa / 2) ** 2 + Math.cos(a[0] * r) * Math.cos(b[0] * r) * Math.sin(dLo / 2) ** 2; return 2 * R * Math.asin(Math.sqrt(s)); }
function samples(seg, step) {
  const out = []; let next = 0;
  for (let i = 0; i < seg.pts.length; i++) if (seg.dist[i] >= next) { out.push({ p: seg.pts[i], s: seg.dist[i] }); next = seg.dist[i] + step; }
  return out;
}
async function getJSON(url, tries = 4) {
  for (let i = 0; i < tries; i++) {
    try { const r = await fetch(url, { headers: UA }); if (r.ok) return await r.json(); console.error('HTTP', r.status, url.slice(0, 100)); }
    catch (e) { console.error('ERR', e.message); }
    await sleep(1500 * (i + 1));
  }
  return null;
}
async function pool(items, n, fn) { let i = 0; await Promise.all(Array.from({ length: n }, async () => { while (i < items.length) { const k = i++; await fn(items[k], k); } })); }

const allSamples = [];
for (const seg of roads.segments) for (const x of samples(seg, 1000)) allSamples.push({ seg: seg.id, ...x });
console.log('samples', allSamples.length);

// --- Wikipedia GeoSearch
const pages = {};
await pool(allSamples, 6, async (x) => {
  const url = `https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord=${x.p[0]}|${x.p[1]}&gsradius=10000&gslimit=100&format=json&formatversion=2`;
  const j = await getJSON(url);
  for (const g of j?.query?.geosearch || []) {
    const pg = pages[g.pageid] ||= { pageid: g.pageid, title: g.title, lat: g.lat, lon: g.lon, segs: {} };
    pg.segs[x.seg] = Math.min(pg.segs[x.seg] ?? 1e9, Math.round(g.dist));
  }
});
console.log('unique wiki pages', Object.keys(pages).length);
// intro extracts + description + length, 20 at a time
const ids = Object.keys(pages);
const batches = []; for (let i = 0; i < ids.length; i += 20) batches.push(ids.slice(i, i + 20));
await pool(batches, 3, async (b) => {
  const url = `https://en.wikipedia.org/w/api.php?action=query&prop=extracts|description|info&exintro=1&explaintext=1&exlimit=20&pageids=${b.join('|')}&format=json&formatversion=2`;
  const j = await getJSON(url);
  for (const p of j?.query?.pages || []) { const pg = pages[p.pageid]; if (!pg) continue; pg.desc = p.description || ''; pg.len = p.length || 0; pg.intro = (p.extract || '').slice(0, 1500); }
});
fs.writeFileSync('cache/wiki/candidates.json', JSON.stringify(Object.values(pages)));

// --- Macrostrat bedrock geology
const geo = [];
await pool(allSamples, 4, async (x) => {
  const url = `https://macrostrat.org/api/v2/geologic_units/map?lat=${x.p[0]}&lng=${x.p[1]}&scale=large`;
  const j = await getJSON(url);
  const u = (j?.success?.data || [])[0];
  if (u) geo.push({ seg: x.seg, s: x.s, lat: x.p[0], lon: x.p[1], name: u.name, strat: u.strat_name, age: u.age, lith: u.lith, descrip: u.descrip, b: u.b_int_name, t: u.t_int_name, src: u.source_id, map_id: u.map_id });
});
geo.sort((a, b) => a.seg.localeCompare(b.seg) || a.s - b.s);
fs.writeFileSync('cache/geo/macrostrat.json', JSON.stringify(geo));
console.log('geo samples', geo.length);
