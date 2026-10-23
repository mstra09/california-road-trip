// Drive every route (and each road segment, both directions) through the real engine with
// simulated playback, and report coverage: drive minutes, narration minutes, clips, max gap.
// Usage: node scripts/simulate.mjs [talk=normal] [--verbose routeId]
import fs from 'node:fs';
import { Network, Engine } from '../site/js/engine.js';

const talk = process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : 'normal';
const verbose = process.argv.includes('--verbose') ? process.argv[process.argv.indexOf('--verbose') + 1] : null;
const { segments } = JSON.parse(fs.readFileSync('site/data/network.json', 'utf8'));
const { routes } = JSON.parse(fs.readFileSync('site/data/routes.json', 'utf8'));
const { clips } = JSON.parse(fs.readFileSync('site/data/clips.json', 'utf8'));
const net = new Network(segments);

const noisy = process.argv.includes('--noisy');
let seed = 42; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const gauss = () => Math.sqrt(-2 * Math.log(rnd() + 1e-9)) * Math.cos(2 * Math.PI * rnd());
export function drive(r, talkLevel = talk) {
  const played = new Set();
  let clipEnd = null, t = 0, i = 0;
  const log = [];
  const eng = new Engine(net, clips, { talk: talkLevel, played, onPlay: (c, why) => { log.push({ id: c.id, title: c.title, t, why, dur: c.dur }); clipEnd = t + c.dur; } });
  const T = r.time.at(-1);
  while (t < T) {
    t += 1;
    while (i < r.time.length - 2 && r.time[i + 1] < t) i++;
    const a = r.pts[i], b = r.pts[i + 1], ta = r.time[i], tb = r.time[i + 1];
    const f = tb > ta ? Math.min(1, (t - ta) / (tb - ta)) : 0;
    let lat = a[0] + (b[0] - a[0]) * f, lon = a[1] + (b[1] - a[1]) * f, acc = 8;
    if (noisy) {
      // ~12 m jitter, weak fixes, a 90 s dropout every ~20 min, and an occasional 5 km jump
      if (t % 1200 > 1110) { if (clipEnd != null && t >= clipEnd) { clipEnd = null; eng.ended(t); } eng.tick(t); continue; }
      lat += gauss() * 12 / 111000; lon += gauss() * 12 / 87000; acc = 5 + rnd() * 50;
      if (rnd() < 0.03) acc = 200 + rnd() * 500;
      if (rnd() < 0.002) lat += 0.05;
    }
    eng.position({ lat, lon, acc, speed: null, heading: null, t });
    if (clipEnd != null && t >= clipEnd) { clipEnd = null; eng.ended(t); }
  }
  // gaps: silence between clip end and next clip start (incl. start and end of trip)
  let maxGap = 0, gapAt = 0, prevEnd = 0;
  for (const e of log) { const g = e.t - prevEnd; if (g > maxGap) { maxGap = g; gapAt = prevEnd; } prevEnd = e.t + e.dur; }
  if (T - prevEnd > maxGap) { maxGap = T - prevEnd; gapAt = prevEnd; }
  const ids = log.map(e => e.id);
  const repeats = ids.filter((x, k) => ids.indexOf(x) !== k);
  const overlaps = log.filter((e, k) => k && e.t < log[k - 1].t + log[k - 1].dur);
  return { T, log, maxGap, gapAt, repeats, overlaps, narr: log.reduce((a, e) => a + e.dur, 0) };
}

const reverse = r => { const T = r.time.at(-1); return { ...r, id: r.id + '(rev)', pts: [...r.pts].reverse(), time: [...r.time].reverse().map(x => T - x) }; };
const rows = [];
const all = [...routes.map(r => ({ ...r, label: 'ROUTE ' + r.id })), ...segments.map(s => ({ ...s, label: s.id })), ...segments.map(s => ({ ...reverse(s), label: s.id + ' (rev)' }))];
let fail = 0;
for (const r of all) {
  const res = drive(r);
  const ok = res.maxGap <= 12 * 60 && !res.repeats.length && !res.overlaps.length;
  if (!ok) fail++;
  rows.push(`${ok ? '  ' : '✗ '}${r.label.padEnd(26)} drive ${(res.T / 60).toFixed(0).padStart(4)} min  narration ${(res.narr / 60).toFixed(0).padStart(3)} min (${Math.round(100 * res.narr / res.T)}%)  clips ${String(res.log.length).padStart(3)}  max gap ${(res.maxGap / 60).toFixed(1)} min @${(res.gapAt / 60).toFixed(0)}m${res.repeats.length ? '  REPEATS ' + res.repeats : ''}${res.overlaps.length ? '  OVERLAP' : ''}`);
  if (verbose && r.id === verbose) for (const e of res.log) console.log(`  ${(e.t / 60).toFixed(1).padStart(6)}m  ${e.why.padEnd(5)} ${(e.dur / 60).toFixed(1)}m  ${e.title}`);
}
console.log(`Coverage report (talkativeness: ${talk})\n` + rows.join('\n'));
const used = new Set(); for (const r of routes) for (const e of drive(r).log) used.add(e.id);
console.log(`\nClips heard on at least one of the ${routes.length} routes: ${used.size}/${clips.length}`);
if (fail) { console.log(`${fail} drives exceed limits`); process.exitCode = 1; }
