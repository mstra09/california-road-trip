// Trigger engine: map-matching to the road network, look-ahead, queueing and pacing.
// Pure logic with an injected clock, so the same code runs in the app, the in-page simulator,
// and the Node test harness (scripts/simulate.mjs).

const LAT0 = 38.45, LON0 = -122.4;
const K_LAT = 110574, K_LON = 111320 * Math.cos(LAT0 * Math.PI / 180);
export const xy = (lat, lon) => [(lon - LON0) * K_LON, (lat - LAT0) * K_LAT];
export function haversine(a, b) {
  const R = 6371000, r = Math.PI / 180;
  const dLa = (b[0] - a[0]) * r, dLo = (b[1] - a[1]) * r;
  const s = Math.sin(dLa / 2) ** 2 + Math.cos(a[0] * r) * Math.cos(b[0] * r) * Math.sin(dLo / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}
const angDiff = (a, b) => { const d = Math.abs(((a - b) % 360 + 540) % 360 - 180); return d; };
const bearingXY = (dx, dy) => (Math.atan2(dx, dy) * 180 / Math.PI + 360) % 360;

// Pacing presets (seconds). minGap: quiet time after a clip before the next ordinary clip.
// fillAfter: silence after which an area long-story may start. lead: seconds of look-ahead.
export const TALK = {
  sparse: { minGap: 240, fillAfter: 600, lead: 40, minPriority: 2 },
  normal: { minGap: 75, fillAfter: 330, lead: 45, minPriority: 1 },
  chatty: { minGap: 12, fillAfter: 150, lead: 55, minPriority: 1 },
};
const IMPORTANT = 4;        // priority at/above which a clip may jump the pacing gap
const IMPORTANT_GAP = 6;    // seconds of breathing room even for important clips

export class Network {
  constructor(segments) {
    this.segs = segments.map(s => {
      const P = s.pts.map(([la, lo]) => xy(la, lo));
      const cum = [0];
      for (let i = 1; i < P.length; i++) cum.push(cum[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]));
      let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      for (const [x, y] of P) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
      return { id: s.id, name: s.name, kind: s.kind, P, cum, len: cum[cum.length - 1], bbox: [x0, y0, x1, y1] };
    });
    this.byId = Object.fromEntries(this.segs.map(s => [s.id, s]));
  }
  // Nearest point on one segment: {s (m along), d (m off), brg (deg of road at that point)}
  nearestOn(seg, p) {
    let best = { d: Infinity };
    const P = seg.P;
    for (let i = 1; i < P.length; i++) {
      const ax = P[i - 1][0], ay = P[i - 1][1], bx = P[i][0], by = P[i][1];
      const dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy;
      let t = L2 ? ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2 : 0;
      t = t < 0 ? 0 : t > 1 ? 1 : t;
      const qx = ax + t * dx, qy = ay + t * dy;
      const d = Math.hypot(p[0] - qx, p[1] - qy);
      if (d < best.d) best = { d, s: seg.cum[i - 1] + t * Math.sqrt(L2), brg: bearingXY(dx, dy), i };
    }
    return best;
  }
  // Match a position (+ optional heading) to the network. Returns {seg, s, dir, off} or null.
  match(lat, lon, heading, prevSegId, maxOff = 90) {
    const p = xy(lat, lon);
    let best = null;
    for (const seg of this.segs) {
      const [x0, y0, x1, y1] = seg.bbox;
      if (p[0] < x0 - maxOff || p[0] > x1 + maxOff || p[1] < y0 - maxOff || p[1] > y1 + maxOff) continue;
      const n = this.nearestOn(seg, p);
      if (n.d > maxOff) continue;
      let score = n.d, dir = 1;
      if (heading != null) {
        const a = angDiff(heading, n.brg);
        dir = a <= 90 ? 1 : -1;
        score += Math.min(a, 180 - a) * 0.8;
      }
      if (seg.id === prevSegId) score -= 20;          // stickiness: don't flap between overlapping roads
      if (!best || score < best.score) best = { seg: seg.id, s: n.s, dir, off: n.d, score, brg: n.brg };
    }
    return best;
  }
}

// Compute where a clip sits along each road it applies to: [[segId, s, offset], ...]
export function anchorsFor(network, lat, lon, reach) {
  const p = xy(lat, lon), out = [];
  for (const seg of network.segs) {
    const [x0, y0, x1, y1] = seg.bbox;
    if (p[0] < x0 - reach || p[0] > x1 + reach || p[1] < y0 - reach || p[1] > y1 + reach) continue;
    const n = network.nearestOn(seg, p);
    if (n.d <= reach) out.push([seg.id, Math.round(n.s), Math.round(n.d)]);
  }
  return out;
}

// GPS conditioning: accuracy gate, jump rejection, speed/heading smoothing.
export class Tracker {
  constructor() { this.last = null; this.speed = 0; this.heading = null; this.pending = []; this.lastGood = 0; this.trail = []; }
  // fix: {lat, lon, acc, speed (m/s|null), heading (deg|null), t (s)}
  push(f) {
    if (f.acc != null && f.acc > 150) return { ok: false, why: 'accuracy' };
    if (this.last) {
      const dt = Math.max(0.2, f.t - this.last.t);
      const d = haversine([this.last.lat, this.last.lon], [f.lat, f.lon]);
      const v = d / dt;
      if (v > 70 && dt < 60) {   // >250 km/h: probably a jump. Accept only if the next fixes agree.
        this.pending.push(f);
        if (this.pending.length < 3) return { ok: false, why: 'jump' };
      }
      this.pending = [];
      const gpsV = f.speed != null && f.speed >= 0 ? f.speed : v;
      const a = dt > 20 ? 1 : 0.35;                      // after a dropout, reset smoothing
      this.speed = this.speed * (1 - a) + gpsV * a;
      let h = f.heading != null && !isNaN(f.heading) && gpsV > 2 ? f.heading : null;
      if (h == null && v > 2) {
        // bearing over a longer baseline (>= 60 m back, within 20 s) so GPS jitter doesn't swing it
        const p1 = xy(f.lat, f.lon);
        for (let k = this.trail.length - 1; k >= 0; k--) {
          const q = this.trail[k]; if (f.t - q.t > 20) break;
          const p0 = xy(q.lat, q.lon), dx = p1[0] - p0[0], dy = p1[1] - p0[1];
          if (Math.hypot(dx, dy) >= 60) { h = bearingXY(dx, dy); break; }
        }
      }
      if (h != null) {
        if (this.heading == null || dt > 20) this.heading = h;
        else { // circular smoothing
          const r = Math.PI / 180, k = 0.5;
          const x = Math.cos(this.heading * r) * (1 - k) + Math.cos(h * r) * k, y = Math.sin(this.heading * r) * (1 - k) + Math.sin(h * r) * k;
          this.heading = (Math.atan2(y, x) / r + 360) % 360;
        }
      }
      if (this.speed < 1 && d < 5) { /* stationary: keep last heading */ }
    } else {
      this.speed = f.speed != null && f.speed >= 0 ? f.speed : 0;
      this.heading = f.heading != null && !isNaN(f.heading) ? f.heading : null;
    }
    this.last = f; this.lastGood = f.t;
    this.trail.push(f); if (this.trail.length > 30) this.trail.shift();
    return { ok: true };
  }
}

export class Engine {
  // clips: array from clips.json. opts: {talk, played:Set, now:()=>seconds, onPlay(clip, reason)}
  constructor(network, clips, opts) {
    this.net = network; this.clips = clips; this.byId = Object.fromEntries(clips.map(c => [c.id, c]));
    this.o = opts; this.played = opts.played || new Set(); this.missed = new Map();
    this.tracker = new Tracker(); this.match = null; this.pos = null;
    this.playing = null; this.lastEnd = -1e9; this.lastStart = -1e9; this.paused = false;
    this.history = [];   // [{id, t, reason}]
    this.upcoming = [];
  }
  get talk() { return TALK[this.o.talk || 'normal']; }
  setTalk(t) { this.o.talk = t; }

  position(fix) {
    const r = this.tracker.push(fix);
    if (!r.ok) return r;
    this.pos = fix;
    const h = this.tracker.speed > 2 ? this.tracker.heading : null;
    const prev = this.match;
    const m = this.net.match(fix.lat, fix.lon, h, prev?.seg);
    // Direction of travel along the road comes from our progress along it, which is far steadier
    // than a heading estimate; heading only decides it when we first join a road.
    if (m && prev && m.seg === prev.seg) {
      m.anchorS = prev.anchorS ?? prev.s;
      const ds = m.s - m.anchorS;
      if (Math.abs(ds) > 40) { m.dir = Math.sign(ds); m.anchorS = m.s; } else m.dir = prev.dir;
    } else if (m) m.anchorS = m.s;
    this.match = m;
    this.tick(fix.t);
    return r;
  }

  // Distance ahead (m) to a clip along the current road, or straight-line fallback.
  ahead(c) {
    const m = this.match;
    if (m && c.anchors) {
      for (const [seg, s] of c.anchors) if (seg === m.seg) return { ds: (s - m.s) * m.dir, onRoad: true };
    }
    if (!this.pos || c.lat == null) return null;
    const d = haversine([this.pos.lat, this.pos.lon], [c.lat, c.lon]);
    if (d > c.radius) return null;
    // off the anchored road (or no anchor): treat as in-window if roughly ahead or very close
    const h = this.tracker.heading;
    if (h != null && this.tracker.speed > 2) {
      const p0 = xy(this.pos.lat, this.pos.lon), p1 = xy(c.lat, c.lon);
      const a = angDiff(h, bearingXY(p1[0] - p0[0], p1[1] - p0[1]));
      if (a > 110 && d > c.radius * 0.4) return { ds: -d, onRoad: false };
    }
    return { ds: d * 0.5, onRoad: false };
  }

  candidates(t) {
    const v = Math.max(this.tracker.speed, 4);
    const L = Math.min(Math.max(v * this.talk.lead, 250), 2600);
    const out = [];
    for (const c of this.clips) {
      if (c.kind !== 'poi' && c.kind !== 'intro') continue;
      if (this.played.has(c.id) || this.missed.has(c.id)) continue;
      const a = this.ahead(c);
      if (!a) continue;
      const back = Math.max(150, c.radius * 0.5);
      if (a.ds < -back) { if (a.onRoad && a.ds > -back - 3000) this.missed.set(c.id, t); continue; }
      out.push({ c, ds: a.ds, eta: a.ds / v, due: a.ds <= L + (c.kind === 'intro' ? 400 : 0) });
    }
    out.sort((x, y) => x.eta - y.eta);
    return out;
  }

  tick(t) {
    for (const [id, tm] of this.missed) if (t - tm > 1800) this.missed.delete(id);
    const cands = this.candidates(t);
    this.upcoming = cands.slice(0, 8);
    if (this.playing || this.paused) return;
    const gap = t - this.lastEnd;
    const due = cands.filter(x => x.due && x.c.priority >= this.talk.minPriority);
    if (due.length) {
      // highest priority first, then soonest; intros win ties so the area is set up first
      due.sort((a, b) => (b.c.priority + (b.c.kind === 'intro' ? 0.5 : 0)) - (a.c.priority + (a.c.kind === 'intro' ? 0.5 : 0)) || a.eta - b.eta);
      const top = due[0];
      const important = top.c.priority >= IMPORTANT || top.c.kind === 'intro';
      const needGap = important ? IMPORTANT_GAP : this.talk.minGap;
      // If we're about to pass it (ds small) allow a shorter gap so it isn't lost entirely.
      const urgent = top.ds < Math.max(200, top.c.radius * 0.3);
      if (gap >= needGap || (urgent && gap >= Math.min(needGap, 25))) return this.start(top.c, t, 'poi');
      return;
    }
    if (gap >= this.talk.fillAfter) this.fill(t, cands);
  }

  // Area long stories (and "tell me more" follow-ups) as gap fillers.
  fill(t, cands) {
    if (!this.pos) return;
    const v = Math.max(this.tracker.speed, 4);
    const busyAhead = (dur) => cands.some(x => x.c.priority >= 3 && x.ds > 0 && x.ds / v < dur + 30);
    const here = [this.pos.lat, this.pos.lon];
    const stories = this.clips.filter(c => c.kind === 'story' && !this.played.has(c.id) &&
      (c.roads?.length ? (this.match && c.roads.includes(this.match.seg)) || haversine(here, [c.lat, c.lon]) < c.radius : haversine(here, [c.lat, c.lon]) < c.radius));
    stories.sort((a, b) => b.priority - a.priority || haversine(here, [a.lat, a.lon]) - haversine(here, [b.lat, b.lon]));
    for (const s of stories) if (!busyAhead(s.dur || 120)) return this.start(s, t, 'story');
    // otherwise: a follow-up of something played in the last 40 minutes
    for (let i = this.history.length - 1; i >= 0; i--) {
      const h = this.history[i]; if (t - h.t > 2400) break;
      const c = this.byId[h.id]; const m = c?.more && this.byId[c.more];
      if (m && !this.played.has(m.id) && !busyAhead(m.dur || 90)) return this.start(m, t, 'more');
    }
    // Emergency tier, so silence never runs much past ~10 minutes: a story from further afield,
    // then any unplayed follow-up of anything heard today.
    if (t - this.lastEnd < 540) return;
    const far = this.clips.filter(c => c.kind === 'story' && !this.played.has(c.id) && haversine(here, [c.lat, c.lon]) < c.radius * 2.5)
      .sort((a, b) => haversine(here, [a.lat, a.lon]) / a.radius - haversine(here, [b.lat, b.lon]) / b.radius);
    if (far.length) return this.start(far[0], t, 'story');
    for (let i = this.history.length - 1; i >= 0; i--) {
      const c = this.byId[this.history[i].id]; const m = c?.more && this.byId[c.more];
      if (m && !this.played.has(m.id)) return this.start(m, t, 'more');
    }
  }

  start(c, t, reason) {
    this.playing = c; this.lastStart = t;
    this.played.add(c.id); this.history.push({ id: c.id, t, reason });
    this.o.onPlay?.(c, reason);
  }
  ended(t) { this.playing = null; this.lastEnd = t; }
  // Manual controls
  playNow(id, t) { const c = this.byId[id]; if (!c) return; this.playing = c; this.played.add(c.id); this.history.push({ id, t, reason: 'manual' }); this.o.onPlay?.(c, 'manual'); }
  nearest() {
    if (!this.pos) return null;
    const here = [this.pos.lat, this.pos.lon];
    let best = null;
    for (const c of this.clips) {
      if (c.kind !== 'poi' || this.played.has(c.id)) continue;
      const d = haversine(here, [c.lat, c.lon]);
      if (!best || d < best.d) best = { c, d };
    }
    return best?.c || null;
  }
}
