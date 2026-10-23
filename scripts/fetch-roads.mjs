// Fetch road geometry from the public OSRM demo server for every segment and route variant.
// Responses are cached in cache/osrm/. Output: data/roads.json (segments + routes with
// polylines, cumulative distance and per-point OSRM time, used by the engine and simulator).
import fs from 'node:fs';
const src = JSON.parse(fs.readFileSync('data/roads.src.json', 'utf8'));
fs.mkdirSync('cache/osrm', { recursive: true });

async function osrm(wp, key) {
  const f = `cache/osrm/${key}.json`;
  if (fs.existsSync(f)) return JSON.parse(fs.readFileSync(f, 'utf8'));
  const coords = wp.map(([la, lo]) => `${lo},${la}`).join(';');
  // optional third element = required travel bearing at that waypoint (for divided highways)
  const bearings = wp.some(p => p[2] != null) ? '&bearings=' + wp.map(p => p[2] != null ? `${p[2]},45` : '').join(';') : '';
  const url = `https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson&steps=true&annotations=duration,distance&continue_straight=true${bearings}`;
  for (let i = 0; i < 4; i++) {
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'california-road-trip-audio-guide (personal, non-commercial)' } });
      const j = await r.json();
      if (j.code === 'Ok') { fs.writeFileSync(f, JSON.stringify(j)); return j; }
      console.error(key, j.code, j.message);
    } catch (e) { console.error(key, e.message); }
    await new Promise(r => setTimeout(r, 2000 * (i + 1)));
  }
  return null;
}

function hav(a, b) {
  const R = 6371000, r = Math.PI / 180;
  const dLa = (b[0] - a[0]) * r, dLo = (b[1] - a[1]) * r;
  const s = Math.sin(dLa / 2) ** 2 + Math.cos(a[0] * r) * Math.cos(b[0] * r) * Math.sin(dLo / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}

// Build [lat,lon] polyline with cumulative distance (m) and time (s).
function build(j, wp) {
  if (!j) { // fallback: straight lines between waypoints at a guessed 60 km/h
    const pts = wp.map(p => [p[0], p[1]]);
    let d = 0, t = 0; const dist = [0], time = [0];
    for (let i = 1; i < pts.length; i++) { const s = hav(pts[i - 1], pts[i]) * 1.3; d += s; t += s / 16.7; dist.push(Math.round(d)); time.push(Math.round(t)); }
    return { pts, dist, time, names: [], fallback: true };
  }
  const route = j.routes[0];
  const pts = route.geometry.coordinates.map(([lo, la]) => [+la.toFixed(5), +lo.toFixed(5)]);
  const durs = route.legs.flatMap(l => l.annotation.duration);
  const dists = route.legs.flatMap(l => l.annotation.distance);
  // legs share endpoints: geometry has N points, annotations N-1 entries
  const dist = [0], time = [0]; let d = 0, t = 0;
  for (let i = 1; i < pts.length; i++) { d += dists[i - 1] ?? hav(pts[i - 1], pts[i]); t += durs[i - 1] ?? 0; dist.push(Math.round(d)); time.push(Math.round(t)); }
  const names = [];
  for (const l of route.legs) for (const s of l.steps) { const n = [s.ref, s.name].filter(Boolean).join(' '); if (n && names[names.length - 1] !== n && s.distance > 300) names.push(n); }
  return { pts, dist, time, names };
}

function slice(spec) {
  const m = spec.match(/^(\w+)(?:\[(-?\d*):(-?\d*)\])?$/);
  const seg = src.segments.find(s => s.id === m[1]);
  const a = m[2] ? +m[2] : 0, b = m[3] ? +m[3] : seg.wp.length;
  return seg.wp.slice(a, b);
}

const out = { segments: [], routes: [] };
for (const s of src.segments) {
  const j = await osrm(s.wp, 'seg_' + s.id);
  const g = build(j, s.wp);
  out.segments.push({ id: s.id, name: s.name, kind: s.kind, ...g });
  console.log(`${s.id.padEnd(18)} ${(g.dist.at(-1) / 1000).toFixed(1)} km ${(g.time.at(-1) / 60).toFixed(0)} min${g.fallback ? ' FALLBACK' : ''}\n    ${g.names.join(' | ')}`);
  await new Promise(r => setTimeout(r, 300));
}
for (const r of src.routes) {
  let wp = [];
  for (const sp of r.segs) for (const p of slice(sp)) { const last = wp[wp.length - 1]; if (!last || hav(last, p) > 50) wp.push(p); }
  const j = await osrm(wp, 'route_' + r.id);
  const g = build(j, wp);
  out.routes.push({ id: r.id, name: r.name, ...g });
  console.log(`ROUTE ${r.id.padEnd(18)} ${(g.dist.at(-1) / 1000).toFixed(1)} km ${(g.time.at(-1) / 60).toFixed(0)} min${g.fallback ? ' FALLBACK' : ''}\n    ${g.names.join(' | ')}`);
  await new Promise(r => setTimeout(r, 300));
}
fs.writeFileSync('data/roads.json', JSON.stringify(out));
