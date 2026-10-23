// App: UI, audio, GPS, wake lock, offline cache, simulator. Decisions live in engine.js.
import { Network, Engine, haversine } from './engine.js';

const $ = id => document.getElementById(id);
const store = {
  get(k, d) { try { const v = localStorage.getItem('rt.' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem('rt.' + k, JSON.stringify(v)); } catch (e) {} },
};
const settings = Object.assign({ talk: 'normal', rate: '1', mode: 'B', simSpeed: '30' }, store.get('settings', {}));
const saveSettings = () => store.set('settings', settings);

let net, clips, byId, routes, engine, manifest;
const played = new Set(store.get('played', []));
const savePlayed = () => store.set('played', [...played]);
const nowSec = () => performance.now() / 1000;

// ---------------------------------------------------------------- data
async function getJSON(url) {
  try { const r = await fetch(url, { cache: 'no-cache' }); if (r.ok) return await r.json(); } catch (e) {}
  const c = await caches.match(url, { ignoreSearch: true });
  if (c) return c.json();
  throw new Error('cannot load ' + url);
}

// ---------------------------------------------------------------- offline cache
const CACHE = 'rt-files-v1';
const cacheState = { have: 0, total: 0, bytes: 0, totalBytes: 0, running: false };
function renderCache() {
  const { have, total, bytes, totalBytes } = cacheState;
  const pct = total ? Math.round(100 * have / total) : 0;
  $('cacheLine').textContent = `Offline ready: ${have}/${total} files (${(bytes / 1e6).toFixed(0)} of ${(totalBytes / 1e6).toFixed(0)} MB)`;
  $('cacheBar').style.width = pct + '%';
  const chip = $('chipOffline');
  chip.textContent = total && have === total ? 'offline ✓' : `offline ${pct}%`;
  chip.className = 'chip ' + (total && have === total ? 'ok' : 'warn');
}
async function precacheAll() {
  if (cacheState.running || !('caches' in window)) return;
  cacheState.running = true;
  try {
    manifest = await getJSON('precache.json');
    const cache = await caches.open(CACHE);
    const metaRes = await cache.match('__meta');
    const meta = metaRes ? await metaRes.json() : {};
    const files = manifest.files;
    cacheState.total = files.length; cacheState.totalBytes = files.reduce((a, f) => a + f.bytes, 0);
    cacheState.have = 0; cacheState.bytes = 0;
    const todo = [];
    for (const f of files) {
      if (meta[f.url] === f.hash && await cache.match(f.url)) { cacheState.have++; cacheState.bytes += f.bytes; }
      else todo.push(f);
    }
    renderCache();
    let i = 0, failed = 0;
    const worker = async () => {
      while (i < todo.length) {
        const f = todo[i++];
        try {
          const r = await fetch(f.url, { cache: 'reload' });
          if (!r.ok) throw new Error(r.status);
          await cache.put(f.url, r);
          meta[f.url] = f.hash; cacheState.have++; cacheState.bytes += f.bytes;
          if (cacheState.have % 10 === 0) await cache.put('__meta', new Response(JSON.stringify(meta)));
        } catch (e) { failed++; }
        renderCache();
      }
    };
    await Promise.all([worker(), worker(), worker(), worker()]);
    // drop files no longer in the manifest
    const keep = new Set(files.map(f => new URL(f.url, location.href).href));
    for (const req of await cache.keys()) if (!keep.has(req.url) && !req.url.endsWith('__meta')) await cache.delete(req);
    await cache.put('__meta', new Response(JSON.stringify(meta)));
    $('cacheDetail').textContent = failed ? `${failed} files failed to download — connect to Wi-Fi and tap “Re-check offline files”.` : (cacheState.have === cacheState.total ? 'Everything is stored on this phone. No signal needed.' : '');
  } catch (e) {
    $('cacheDetail').textContent = 'Could not check the offline files: ' + e.message;
  } finally { cacheState.running = false; renderCache(); }
}

// ---------------------------------------------------------------- audio
const el = $('player');
let currentClip = null, currentUrl = null, speechUtter = null, clipStartedAt = 0, endTimer = null;
const SESSION = { A: null, B: 'transient', C: 'transient-solo', D: 'playback', E: null, F: 'ambient' };
function setSession(type) {
  if (!('audioSession' in navigator)) return;
  try { navigator.audioSession.type = type || 'auto'; } catch (e) {}
}
async function unlockAudio() {
  setSession(SESSION[settings.mode]);
  el.src = 'audio/silence.m4a';
  try { await el.play(); } catch (e) {}
  try { const u = new SpeechSynthesisUtterance(' '); u.volume = 0; speechSynthesis.speak(u); } catch (e) {}
}
function release() {
  // Hand audio back to other apps as cleanly as a web page can.
  try { el.pause(); } catch (e) {}
  el.removeAttribute('src');
  try { el.load(); } catch (e) {}
  if (currentUrl) { URL.revokeObjectURL(currentUrl); currentUrl = null; }
  if (settings.mode !== 'A') setSession(null);
}
async function sourceFor(clip) {
  if (!clip.audio) return null;
  try {
    const hit = await caches.match(clip.audio, { ignoreSearch: true });
    if (hit) { const b = await hit.blob(); currentUrl = URL.createObjectURL(b); return currentUrl; }
  } catch (e) {}
  return clip.audio;
}
const sim = { on: false, audio: true, mult: 1, t: 0 };
function speak(clip) {
  try {
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(clip.tts || clip.text);
    u.rate = +settings.rate; u.lang = 'en-US';
    u.onend = () => { if (speechUtter === u) clipFinished(); };
    u.onerror = () => { if (speechUtter === u) clipFinished(); };
    speechUtter = u; speechSynthesis.speak(u);
  } catch (e) { clipFinished(); }
}
async function playClip(clip, reason) {
  currentClip = clip; clipStartedAt = clock(); showNow(clip, reason);
  clearTimeout(endTimer);
  if (sim.on && !sim.audio) {   // silent simulator: time the clip in simulated seconds
    sim.clipEnd = sim.t + (clip.dur || 60) / +settings.rate;
    return;
  }
  if (settings.mode === 'E') return speak(clip);
  setSession(SESSION[settings.mode]);
  const src = await sourceFor(clip);
  if (!src) return speak(clip);
  el.src = src; el.playbackRate = +settings.rate;
  el.onerror = () => { if (currentClip === clip) { release(); speak(clip); } };
  try { await el.play(); hideTap(); }
  catch (e) { if (e.name === 'NotAllowedError') showTap(); else { release(); speak(clip); } }
}
el.addEventListener('ended', () => clipFinished());
function clipFinished() {
  if (!currentClip) return;
  speechUtter = null; release();
  currentClip = null; $('nowBar').style.width = '100%';
  engine.ended(clock());
  setTimeout(() => { if (!engine.playing) $('nowTitle').textContent = 'Waiting for the next story…'; }, 4000);
  renderClips();
}
function showTap() { $('tapOverlay').classList.remove('hidden'); }
function hideTap() { $('tapOverlay').classList.add('hidden'); }
$('tapOverlay').onclick = async () => { hideTap(); try { await el.play(); } catch (e) { showTap(); } };

// ---------------------------------------------------------------- clock (real or simulated)
function clock() { return sim.on ? sim.t : nowSec(); }

// ---------------------------------------------------------------- now playing UI
function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
function showNow(clip, reason) {
  $('nowArea').textContent = [clip.areaName, clip.category, reason === 'story' ? 'long story' : reason === 'more' ? 'tell me more' : ''].filter(Boolean).join(' · ');
  $('nowTitle').textContent = clip.title;
  $('nowText').textContent = clip.text;
  $('nowText').scrollTop = 0;
  $('nowSources').innerHTML = (clip.sources || []).map((u, i) => `<a href="${esc(u)}" target="_blank" rel="noopener">source ${i + 1}</a>`).join(' · ');
  $('btnMore').disabled = !clip.more;
  $('btnPause').firstChild.textContent = '⏸';
}
setInterval(() => {
  if (currentClip) {
    const d = (currentClip.dur || 60) / +settings.rate;
    const p = el.src && !isNaN(el.duration) && el.duration ? el.currentTime / el.duration : (clock() - clipStartedAt) / d;
    $('nowBar').style.width = Math.min(100, p * 100) + '%';
  }
}, 500);

$('btnPause').onclick = () => {
  if (!currentClip) { engine.paused = !engine.paused; $('btnPause').firstChild.textContent = engine.paused ? '▶' : '⏸'; return; }
  if (settings.mode === 'E' || !el.src) {
    if (speechSynthesis.paused) speechSynthesis.resume(); else speechSynthesis.pause();
    $('btnPause').firstChild.textContent = speechSynthesis.paused ? '▶' : '⏸'; return;
  }
  if (el.paused) { el.play().catch(showTap); $('btnPause').firstChild.textContent = '⏸'; }
  else { el.pause(); $('btnPause').firstChild.textContent = '▶'; }
};
$('btnSkip').onclick = () => { if (currentClip) { speechSynthesis.cancel(); clipFinished(); } };
$('btnReplay').onclick = () => {
  const last = currentClip || byId[engine.history.at(-1)?.id];
  if (!last) return;
  if (currentClip) { speechSynthesis.cancel(); release(); currentClip = null; }
  engine.playing = last; playClip(last, 'replay');
};
$('btnMore').onclick = () => {
  const base = currentClip || byId[engine.history.at(-1)?.id];
  const m = base?.more && byId[base.more];
  if (!m) return;
  if (currentClip) { speechSynthesis.cancel(); release(); currentClip = null; }
  engine.playNow(m.id, clock()); savePlayed();
};
$('btnNearest').onclick = () => {
  const c = engine.nearest(); if (!c) return;
  if (currentClip) { speechSynthesis.cancel(); release(); currentClip = null; }
  engine.playNow(c.id, clock()); savePlayed();
};

function fmtDist(m) { const mi = m / 1609.34; return mi < 0.2 ? `${Math.round(m * 3.28084 / 50) * 50} ft` : `${mi.toFixed(mi < 10 ? 1 : 0)} mi`; }
function renderUpcoming() {
  const ul = $('upcoming');
  const items = engine.upcoming.filter(x => x.ds > -100).slice(0, 6);
  ul.innerHTML = items.length ? items.map(x => `<li><span>${esc(x.c.title)}</span><span class="d">${x.ds < 50 ? 'now' : fmtDist(x.ds)}</span></li>`).join('')
    : '<li class="dim">Nothing close on this road yet. Area stories fill the gaps.</li>';
}

// ---------------------------------------------------------------- status chips
let wakeState = '—';
function renderStatus(fix) {
  const g = $('chipGps');
  if (sim.on) { g.textContent = 'SIMULATOR'; g.className = 'chip warn'; }
  else if (fix) { g.textContent = `GPS ±${Math.round(fix.acc)} m`; g.className = 'chip ' + (fix.acc <= 50 ? 'ok' : fix.acc <= 150 ? 'warn' : 'bad'); }
  const mph = engine.tracker.speed * 2.23694;
  $('chipSpeed').textContent = `${Math.round(mph)} mph`;
  const m = engine.match;
  $('chipRoad').textContent = m ? net.byId[m.seg].name.split(/[:→(]/)[0].trim() : 'off-network';
  $('chipRoad').className = 'chip ' + (m ? 'ok' : 'warn');
  $('chipWake').textContent = 'screen ' + wakeState; $('chipWake').className = 'chip ' + (wakeState === 'on' ? 'ok' : 'warn');
  $('diag').textContent = `Played ${played.size}/${clips.length} · ${m ? `${(m.s / 1000).toFixed(1)} km along, ${Math.round(m.off)} m off road` : 'no road match'} · heading ${engine.tracker.heading == null ? '—' : Math.round(engine.tracker.heading) + '°'}`;
  renderUpcoming();
}

// ---------------------------------------------------------------- GPS
let watchId = null, lastFix = null;
function startGPS() {
  if (!('geolocation' in navigator)) { $('chipGps').textContent = 'no GPS'; return; }
  watchId = navigator.geolocation.watchPosition(p => {
    if (sim.on) return;
    const c = p.coords;
    lastFix = { lat: c.latitude, lon: c.longitude, acc: c.accuracy, speed: c.speed, heading: c.heading, t: nowSec() };
    const r = engine.position(lastFix);
    if (!r.ok && r.why === 'accuracy') { $('chipGps').textContent = `GPS weak ±${Math.round(c.accuracy)} m`; $('chipGps').className = 'chip bad'; }
    savePlayed(); renderStatus(lastFix);
  }, err => { $('chipGps').textContent = 'GPS: ' + (err.code === 1 ? 'permission denied' : 'no fix'); $('chipGps').className = 'chip bad'; },
  { enableHighAccuracy: true, maximumAge: 2000, timeout: 30000 });
}
// keep the engine ticking (pacing/fillers) even when fixes pause
setInterval(() => { if (engine && !sim.on) { engine.tick(nowSec()); renderUpcoming(); } }, 3000);

// ---------------------------------------------------------------- wake lock (+ NoSleep-style fallback)
let wakeLock = null, noSleepVideo = null;
async function keepAwake() {
  try {
    if ('wakeLock' in navigator) {
      wakeLock = await navigator.wakeLock.request('screen');
      wakeState = 'on';
      wakeLock.addEventListener('release', () => { wakeState = 'off'; renderStatus(lastFix); });
      return;
    }
  } catch (e) {}
  // Fallback: a tiny muted looping video keeps iOS from sleeping.
  try {
    noSleepVideo = document.createElement('video');
    Object.assign(noSleepVideo, { muted: true, loop: true, playsInline: true, src: 'media/nosleep.mp4' });
    noSleepVideo.setAttribute('playsinline', ''); noSleepVideo.style.cssText = 'position:fixed;width:1px;height:1px;opacity:0.01;bottom:0';
    document.body.appendChild(noSleepVideo);
    await noSleepVideo.play(); wakeState = 'on (video)';
  } catch (e) { wakeState = 'off — set Auto-Lock: Never'; }
}
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && started) keepAwake(); });

// ---------------------------------------------------------------- clip browser
function renderClips() {
  const q = ($('clipSearch').value || '').toLowerCase();
  const groups = {};
  for (const c of clips) {
    if (q && !(c.title + ' ' + c.text + ' ' + (c.areaName || '')).toLowerCase().includes(q)) continue;
    (groups[c.areaName || 'Other'] ||= []).push(c);
  }
  $('clipList').innerHTML = Object.entries(groups).map(([a, cs]) => `<div class="card area"><h3>${esc(a)} <span class="dim small">(${cs.length})</span></h3>` +
    cs.map(c => `<div class="clip ${played.has(c.id) ? 'played' : ''}"><div class="t">${esc(c.title)}</div><div class="meta">${esc(c.category)} · ${Math.round((c.dur || 0) / 60 * 10) / 10} min${c.kind === 'story' ? ' · long story' : c.kind === 'more' ? ' · follow-up' : ''}</div>
      <details><summary>Transcript</summary>${esc(c.text)}<div class="small">${(c.sources || []).map((u, i) => `<a href="${esc(u)}" target="_blank" rel="noopener">source ${i + 1}</a>`).join(' · ')}</div></details>
      <button data-play="${c.id}">▶ Play</button></div>`).join('') + '</div>').join('');
}
$('clipSearch').oninput = renderClips;
$('clipList').onclick = e => {
  const id = e.target.dataset?.play; if (!id) return;
  if (currentClip) { speechSynthesis.cancel(); release(); currentClip = null; }
  engine.playNow(id, clock()); savePlayed(); showTab('nowView');
};

// ---------------------------------------------------------------- settings
function renderSettings() {
  document.querySelectorAll('.seg').forEach(s => s.querySelectorAll('button').forEach(b => b.classList.toggle('on', settings[s.dataset.setting] === b.dataset.v)));
  const hints = {
    A: 'Plain audio element. Usually pauses Spotify; it may not resume by itself.',
    B: 'transient: meant for short announcements, so other audio may keep playing (ducked or mixed). Untested with your phone: run the audio test. If you hear nothing, check the silent switch.',
    C: 'transient-solo: meant to pause other audio while speaking, which may let Spotify resume afterwards.',
    D: 'playback: behaves like a media app — pauses Spotify.',
    E: 'speechSynthesis: robotic built-in voice, ignores the audio files.',
    F: 'ambient: meant to mix with music without ducking; may be silenced by the silent switch.',
  };
  let res = {}; try { res = JSON.parse(localStorage.getItem('audioTestResults') || '{}'); } catch (e) {}
  $('modeHint').textContent = hints[settings.mode] + (res[settings.mode] ? ` Your test result for ${settings.mode}: “${res[settings.mode]}”.` : '');
  $('histInfo').textContent = `${played.size} of ${clips.length} clips played (saved on this phone, so a reload never repeats them).`;
}
document.querySelectorAll('.seg').forEach(s => s.onclick = e => {
  const v = e.target.closest('button')?.dataset.v; if (!v) return;
  settings[s.dataset.setting] = v; saveSettings(); renderSettings();
  if (s.dataset.setting === 'talk') engine.setTalk(v);
  if (s.dataset.setting === 'rate' && el.src) el.playbackRate = +v;
  if (s.dataset.setting === 'simSpeed') sim.mult = +v;
});
$('btnReset').onclick = () => { if (!confirm('Forget which clips have played?')) return; played.clear(); savePlayed(); renderSettings(); renderClips(); };
$('btnRecache').onclick = () => precacheAll();

// ---------------------------------------------------------------- simulator
let simTimer = null;
function simStart(routeId, mult, withAudio, startFrac = 0) {
  const r = routes.find(x => x.id === routeId) || net.byId[routeId] && { pts: net.byId[routeId].pts, time: net.byId[routeId].time };
  if (!r) return;
  simStop();
  // The simulator keeps its own played-history so tonight's test runs don't use up tomorrow's clips.
  sim.savedPlayed = engine.played; engine.played = new Set(); engine.history = [];
  sim.on = true; sim.audio = withAudio; sim.mult = mult; sim.route = r; sim.t = 0; sim.clipEnd = null;
  sim.log = []; sim.i = 0; sim.T = r.time.at(-1);
  sim.t0 = r.time[Math.floor(startFrac * (r.time.length - 1))];
  engine.tracker = new (engine.tracker.constructor)(); engine.match = null; engine.lastEnd = -1e9; engine.missed.clear();
  const step = () => {
    if (!sim.on) return;
    const dt = 1;                      // simulated seconds per step
    sim.t += dt;
    const tt = sim.t0 + sim.t;
    if (tt > sim.T) { $('simStatus').textContent = 'Simulator finished.'; simStop(); return; }
    while (sim.i < r.time.length - 2 && r.time[sim.i + 1] < tt) sim.i++;
    const a = r.pts[sim.i], b = r.pts[sim.i + 1], ta = r.time[sim.i], tb = r.time[sim.i + 1];
    const f = tb > ta ? (tt - ta) / (tb - ta) : 0;
    const lat = a[0] + (b[0] - a[0]) * f, lon = a[1] + (b[1] - a[1]) * f;
    engine.position({ lat, lon, acc: 8, speed: null, heading: null, t: sim.t });
    if (sim.clipEnd != null && sim.t >= sim.clipEnd) { sim.clipEnd = null; clipFinished(); }
    if (sim.t % 5 === 0) { renderStatus({ acc: 8 }); $('simStatus').textContent = `Sim ${Math.floor(tt / 60)} / ${Math.floor(sim.T / 60)} min · ${engine.history.length} clips`; }
  };
  sim.step = step;
  simTimer = setInterval(() => { for (let k = 0; k < sim.mult; k++) step(); }, 1000);
}
function simStop() {
  const was = sim.on;
  sim.on = false; clearInterval(simTimer); simTimer = null;
  if (sim.savedPlayed) { engine.played = sim.savedPlayed; sim.savedPlayed = null; }
  if (was) {
    if (currentClip) { speechSynthesis.cancel(); release(); currentClip = null; }
    engine.playing = null; engine.history = []; engine.tracker = new (engine.tracker.constructor)(); engine.match = null; engine.lastEnd = -1e9;
    $('nowTitle').textContent = 'Waiting for the next story…'; renderStatus(lastFix);
  }
}
$('btnSim').onclick = () => { simStart($('simRoute').value, +settings.simSpeed, $('simAudio').checked); showTab('nowView'); };
$('btnSimStop').onclick = () => { simStop(); $('simStatus').textContent = 'Stopped.'; };

// Test hook used by Playwright: run a whole route silently at full speed and return the log.
window.__rt = {
  ready: false,
  runRoute(routeId, talk = 'normal') {
    const r = routes.find(x => x.id === routeId) || (net.byId[routeId] && { pts: net.byId[routeId].pts, time: net.byId[routeId].time });
    const savedPlayed = engine.played; engine.played = new Set();
    engine.setTalk(talk);
    sim.on = true; sim.audio = false; sim.t = 0; sim.clipEnd = null; sim.route = r; sim.i = 0; sim.t0 = 0; sim.T = r.time.at(-1);
    engine.tracker = new (engine.tracker.constructor)(); engine.match = null; engine.lastEnd = -1e9; engine.missed.clear(); engine.history = [];
    const log = [];
    const origOnPlay = engine.o.onPlay;
    engine.o.onPlay = (c, why) => { log.push({ id: c.id, t: sim.t, why, dur: c.dur, title: c.title }); origOnPlay(c, why); };
    while (sim.on && sim.t < sim.T) {
      sim.t += 1;
      while (sim.i < r.time.length - 2 && r.time[sim.i + 1] < sim.t) sim.i++;
      const a = r.pts[sim.i], b = r.pts[sim.i + 1], ta = r.time[sim.i], tb = r.time[sim.i + 1];
      const f = tb > ta ? Math.min(1, (sim.t - ta) / (tb - ta)) : 0;
      engine.position({ lat: a[0] + (b[0] - a[0]) * f, lon: a[1] + (b[1] - a[1]) * f, acc: 8, speed: null, heading: null, t: sim.t });
      if (sim.clipEnd != null && sim.t >= sim.clipEnd) { sim.clipEnd = null; clipFinished(); }
    }
    engine.o.onPlay = origOnPlay; sim.on = false;
    engine.played = savedPlayed; engine.history = []; engine.playing = null;
    return { route: routeId, driveSec: sim.T, log };
  },
  cacheState, settings, played,
};

// ---------------------------------------------------------------- tabs, start
function showTab(id) {
  document.querySelectorAll('.view').forEach(v => v.classList.toggle('hidden', v.id !== id));
  document.querySelectorAll('#tabs button').forEach(b => b.classList.toggle('on', b.dataset.view === id));
  if (id === 'clipsView') renderClips();
  if (id === 'setView') renderSettings();
}
document.querySelectorAll('#tabs button').forEach(b => b.onclick = () => showTab(b.dataset.view));

let started = false;
$('btnStart').onclick = async () => {
  started = true;
  await unlockAudio();
  startGPS();
  keepAwake();
  try { if (navigator.storage?.persist) await navigator.storage.persist(); } catch (e) {}
  showTab('nowView');
  precacheAll();
  renderStatus(null);
};

async function init() {
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});
  const [n, c, r] = await Promise.all([getJSON('data/network.json'), getJSON('data/clips.json'), getJSON('data/routes.json')]);
  net = new Network(n.segments);
  net.segs.forEach((s, i) => { s.pts = n.segments[i].pts; s.time = n.segments[i].time; });
  clips = c.clips; byId = Object.fromEntries(clips.map(x => [x.id, x])); routes = r.routes;
  engine = new Engine(net, clips, { talk: settings.talk, played, onPlay: (clip, why) => { savePlayed(); playClip(clip, why); } });
  $('simRoute').innerHTML = routes.map(x => `<option value="${x.id}">Route: ${esc(x.name)}</option>`).join('') +
    n.segments.map(s => `<option value="${s.id}">Road: ${esc(s.name)}</option>`).join('');
  sim.mult = +settings.simSpeed;
  const exp = await getJSON('exports/index.json').catch(() => ({ routes: [] }));
  $('expList').innerHTML = exp.routes.map(x => `<div class="exp"><b>${esc(x.name)}</b><div class="small dim">${x.count} clips · ${Math.round(x.minutes)} min of audio</div>
    <a href="${x.cues}" target="_blank">Cue sheet</a><a href="${x.m3u}">M3U playlist</a><a href="${x.zip}">Numbered MP3/M4A zip</a><a href="${x.rss}">Podcast feed</a>
    <div class="small dim">Podcast URL: <code>${esc(new URL(x.rss, location.href).href)}</code></div></div>`).join('') || '<p class="dim">Not built yet.</p>';
  renderSettings();
  precacheAll();
  window.__rt.ready = true;
}
init().catch(e => { $('cacheDetail').textContent = 'Startup error: ' + e.message; window.__rt.error = e.message; });
