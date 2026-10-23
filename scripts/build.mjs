// Build app data from content/*.json + data/roads.json.
//   node scripts/build.mjs jobs   -> build/tts-jobs.json (what audio needs rendering)
//   node scripts/build.mjs        -> site/data/{network,routes,clips}.json + site/precache.json
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { Network, anchorsFor } from '../site/js/engine.js';

const MODE = process.argv[2] || 'final';
const VOICE = process.env.VOICE || 'af_heart';
const roads = JSON.parse(fs.readFileSync('data/roads.json', 'utf8'));
fs.mkdirSync('build', { recursive: true });
fs.mkdirSync('site/data', { recursive: true });

// --- simplify polylines (Douglas–Peucker, ~6 m) while keeping cumulative time
function simplify(pts, time, tol = 6) {
  const K_LAT = 110574, K_LON = 111320 * Math.cos(38.45 * Math.PI / 180);
  const P = pts.map(([la, lo]) => [lo * K_LON, la * K_LAT]);
  const keep = new Uint8Array(P.length); keep[0] = keep[P.length - 1] = 1;
  const stack = [[0, P.length - 1]];
  while (stack.length) {
    const [a, b] = stack.pop(); let md = 0, mi = -1;
    const [ax, ay] = P[a], [bx, by] = P[b], dx = bx - ax, dy = by - ay, L = Math.hypot(dx, dy) || 1;
    for (let i = a + 1; i < b; i++) { const d = Math.abs((P[i][0] - ax) * dy - (P[i][1] - ay) * dx) / L; if (d > md) { md = d; mi = i; } }
    if (md > tol) { keep[mi] = 1; stack.push([a, mi], [mi, b]); }
  }
  const op = [], ot = [];
  for (let i = 0; i < P.length; i++) if (keep[i]) { op.push(pts[i]); ot.push(time[i]); }
  return { pts: op, time: ot };
}
const segments = roads.segments.map(s => ({ id: s.id, name: s.name, kind: s.kind, ...simplify(s.pts, s.time) }));
const routes = roads.routes.map(r => ({ id: r.id, name: r.name, ...simplify(r.pts, r.time, 4) }));
const net = new Network(segments);

// --- pronunciation: respellings used only in tts text
const pron = JSON.parse(fs.readFileSync('content/pronounce.json', 'utf8'));
const pronKeys = Object.keys(pron).sort((a, b) => b.length - a.length);
function toTTS(text) {
  let t = text;
  for (const k of pronKeys) t = t.replace(new RegExp(`\\b${k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'g'), pron[k]);
  return t.replace(/—/g, ', ').replace(/–/g, ' to ').replace(/\s+/g, ' ').trim();
}

// --- radius / reach by road type
const RADIUS = { freeway: 1600, highway: 1000, rural: 700, mountain: 500 };
const kindOf = id => net.byId[id]?.kind || 'rural';

// --- load content
const files = fs.readdirSync('content').filter(f => f.endsWith('.json') && f !== 'pronounce.json').sort();
const clips = [];
for (const f of files) {
  const doc = JSON.parse(fs.readFileSync(path.join('content', f), 'utf8'));
  for (const c of doc.clips) {
    const base = { area: doc.area.id, areaName: doc.area.name, kind: 'poi', priority: 2, category: 'history', ...c };
    if (c.more) { base.more = c.more.id = c.more.id || c.id + '_more'; }
    clips.push(base);
    if (c.more) clips.push({ area: doc.area.id, areaName: doc.area.name, priority: 1, category: base.category, lat: c.lat, lon: c.lon, sources: c.sources, ...c.more, kind: 'more', title: c.more.title || (c.title + ' — more') });
  }
}
const ids = new Set();
for (const c of clips) { if (ids.has(c.id)) throw new Error('duplicate id ' + c.id); ids.add(c.id); }

for (const c of clips) {
  c.tts = toTTS(c.tts || c.text);
  c.words = c.text.split(/\s+/).length;
  if (c.lat != null && c.kind !== 'more') {
    const reach = c.reach || (c.kind === 'story' ? 0 : 2500);
    if (c.kind !== 'story') {
      c.anchors = c.roads ? anchorsFor(net, c.lat, c.lon, 60000).filter(a => c.roads.includes(a[0])) : anchorsFor(net, c.lat, c.lon, reach);
      if (c.onlyRoads) c.anchors = c.anchors.filter(a => c.onlyRoads.includes(a[0]));
      c.roads = [...new Set(c.anchors.map(a => a[0]))];
      const k = c.roads.length ? c.roads.map(kindOf).sort((a, b) => RADIUS[b] - RADIUS[a])[0] : 'rural';
      c.radius = c.radius || RADIUS[k];
    } else {
      c.radius = c.radius || 20000;
    }
  }
  const h = crypto.createHash('sha1').update(VOICE + '|' + c.tts).digest('hex').slice(0, 8);
  c.audio = `audio/${c.id}-${h}.m4a`;
}

if (MODE === 'jobs') {
  fs.writeFileSync('build/tts-jobs.json', JSON.stringify({ voice: VOICE, jobs: clips.map(c => ({ id: c.id, tts: c.tts, out: 'site/' + c.audio })) }, null, 1));
  console.log('jobs', clips.length);
  process.exit(0);
}

// --- durations from rendered audio
const durs = fs.existsSync('build/durations.json') ? JSON.parse(fs.readFileSync('build/durations.json', 'utf8')) : {};
let missing = 0;
for (const c of clips) {
  const d = durs['site/' + c.audio];
  if (d) c.dur = Math.round(d * 10) / 10; else { c.dur = Math.round(c.words / 2.55); missing++; delete c.audioMissing; if (!fs.existsSync('site/' + c.audio)) c.audioMissing = true; }
}
const unanchored = clips.filter(c => (c.kind === 'poi' || c.kind === 'intro') && !c.anchors?.length);
if (unanchored.length) console.warn('WARNING: clips not near any road:', unanchored.map(c => c.id).join(', '));

const out = clips.map(c => { const o = { ...c }; delete o.words; delete o.reach; delete o.onlyRoads; return o; });
fs.writeFileSync('site/data/clips.json', JSON.stringify({ voice: VOICE, built: new Date().toISOString(), clips: out }));
fs.writeFileSync('site/data/network.json', JSON.stringify({ segments }));
fs.writeFileSync('site/data/routes.json', JSON.stringify({ routes }));

// --- remove stale audio files no longer referenced
const used = new Set(clips.map(c => path.basename(c.audio)));
for (const f of fs.readdirSync('site/audio')) if (f.endsWith('.m4a') && f !== 'silence.m4a' && !used.has(f)) fs.unlinkSync(path.join('site/audio', f));

// --- precache manifest: every file in site/ except the test page's own assets and exports zips
const files2 = [];
(function walk(dir) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f), rel = path.relative('site', p).split(path.sep).join('/');
    if (fs.statSync(p).isDirectory()) { walk(p); continue; }
    if (f.startsWith('.') || rel === 'precache.json' || rel.endsWith('.zip') || rel.startsWith('voice-samples/')) continue;
    if (rel.endsWith('.m4a') && rel.startsWith('audio/') && !used.has(f) && f !== 'silence.m4a') continue;
    const buf = fs.readFileSync(p);
    files2.push({ url: rel, bytes: buf.length, hash: crypto.createHash('sha1').update(buf).digest('hex').slice(0, 10) });
  }
})('site');
files2.push({ url: './', bytes: fs.statSync('site/index.html').size, hash: files2.find(f => f.url === 'index.html').hash });
const total = files2.reduce((a, f) => a + f.bytes, 0);
fs.writeFileSync('site/precache.json', JSON.stringify({ built: new Date().toISOString(), files: files2 }));
const by = k => clips.filter(c => c.kind === k).length;
console.log(`clips ${clips.length} (poi ${by('poi')}, intro ${by('intro')}, story ${by('story')}, more ${by('more')}), audio missing ${missing}, precache ${files2.length} files ${(total / 1e6).toFixed(1)} MB`);
