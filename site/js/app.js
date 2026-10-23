// App: UI, audio, GPS, wake lock, offline cache, simulator. Decisions live in engine.js.
import { Network, Engine, haversine } from './engine.js';
import * as S from './speech.js';

const $ = id => document.getElementById(id);
const store = {
  get(k, d) { try { const v = localStorage.getItem('rt.' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem('rt.' + k, JSON.stringify(v)); } catch (e) {} },
};
const settings = Object.assign({ talk: 'normal', rate: '1', mode: 'G', simSpeed: '30', voice: '', awake: 'both' }, store.get('settings', {}));
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
const CACHE = 'rt-files-v2';   // must match sw.js
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
    await cache.put('precache.json', new Response(JSON.stringify(manifest), { headers: { 'Content-Type': 'application/json' } }));
    const metaRes = await cache.match('__meta');
    const meta = metaRes ? await metaRes.json() : {};
    const hadMeta = Object.keys(meta).length > 0;
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
        let ok = false;
        for (let attempt = 0; attempt < 4 && !ok; attempt++) {   // hotel Wi-Fi and CDNs drop requests; retry
          try {
            if (attempt) await new Promise(r => setTimeout(r, 1500 * attempt));
            // ?v= makes the service worker pass this straight to the network (never the old cache)
            const r = await fetch(f.url + (f.url.includes('?') ? '&' : '?') + 'v=' + f.hash, { cache: 'reload' });
            if (!r.ok) throw new Error(r.status);
            await cache.put(f.url, r);
            ok = true;
          } catch (e) {}
        }
        if (ok) {
          meta[f.url] = f.hash; cacheState.have++; cacheState.bytes += f.bytes;
          if (cacheState.have % 10 === 0) await cache.put('__meta', new Response(JSON.stringify(meta)));
        } else failed++;
        renderCache();
      }
    };
    await Promise.all([worker(), worker(), worker(), worker()]);
    // drop files no longer in the manifest
    const keep = new Set(files.map(f => new URL(f.url, location.href).href));
    for (const req of await cache.keys()) if (!keep.has(req.url) && !req.url.endsWith('__meta')) await cache.delete(req);
    await cache.put('__meta', new Response(JSON.stringify(meta)));
    $('cacheDetail').textContent = failed ? `${failed} files failed to download — connect to Wi-Fi and tap “Re-check offline files”.` : (cacheState.have === cacheState.total ? 'Everything is stored on this phone. No signal needed.' : '');
    // A newer version of the app itself was just downloaded: offer a reload (never while a clip plays).
    if (hadMeta && todo.some(f => !f.url.startsWith('audio/') && meta[f.url] === f.hash)) showUpdateBanner();
  } catch (e) {
    $('cacheDetail').textContent = 'Could not check the offline files: ' + e.message;
  } finally { cacheState.running = false; renderCache(); }
}

function showUpdateBanner() {
  if (document.getElementById('updBanner')) return;
  const b = document.createElement('button');
  b.id = 'updBanner'; b.className = 'primary'; b.style.cssText = 'position:fixed;left:16px;right:16px;top:calc(env(safe-area-inset-top) + 6px);z-index:20;font-size:17px;min-height:48px';
  b.textContent = 'New version downloaded — tap to reload';
  b.onclick = () => { if (!currentClip) location.reload(); };
  document.body.appendChild(b);
}

// ---------------------------------------------------------------- audio
const el = $('player');
let currentClip = null, currentUrl = null, clipStartedAt = 0, endTimer = null;
const SESSION = { A: null, B: 'transient', C: 'transient-solo', D: 'playback', E: null, F: 'ambient', G: 'ambient', H: 'transient' };
const DUCK = { G: true, H: true };   // recorded voice + silent speech to make iOS duck other audio
function setSession(type) {
  if (!('audioSession' in navigator)) return;
  try { navigator.audioSession.type = type || 'auto'; } catch (e) {}
}
// Must be called directly from a tap: speech is primed first, synchronously, because iOS ignores
// speech that wasn't started inside a user gesture (an await before it is enough to lose that).
async function unlockAudio() {
  S.prime();
  if (settings.mode === 'E') return;   // speech-only mode never touches the audio element
  setSession(SESSION[settings.mode]);
  el.src = 'audio/silence.m4a';
  try { await el.play(); } catch (e) {}
}
// Any tap re-primes speech if it is idle, so speech keeps working after mode changes, sim starts, etc.
document.addEventListener('click', () => { if (settings.mode === 'E' || DUCK[settings.mode]) S.prime(); }, true);
let speechHandle = null;
function stopSpeech() { speechHandle?.cancel(); speechHandle = null; S.stopDuck(); }
function release() {
  // Hand audio back to other apps as cleanly as a web page can.
  try { el.pause(); } catch (e) {}
  el.removeAttribute('src');
  try { el.load(); } catch (e) {}
  if (currentUrl) { URL.revokeObjectURL(currentUrl); currentUrl = null; }
  if (settings.mode !== 'A') setSession(null);
  S.stopDuck();
  try { if ('mediaSession' in navigator) { navigator.mediaSession.metadata = null; navigator.mediaSession.playbackState = 'none'; } } catch (e) {}
}
function setMediaSession(clip) {
  if (!('mediaSession' in navigator)) return;
  try {
    navigator.mediaSession.metadata = new MediaMetadata({ title: clip.title, artist: 'Wine Country Road Guide', album: clip.areaName || '',
      artwork: [{ src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' }] });
    navigator.mediaSession.playbackState = 'playing';
  } catch (e) {}
}
// Steering-wheel / lock-screen controls while a clip plays: pause, resume, skip.
try {
  if ('mediaSession' in navigator) {
    navigator.mediaSession.setActionHandler('pause', () => { if (currentClip && !el.paused) { el.pause(); $('btnPause').firstChild.textContent = '▶'; } });
    navigator.mediaSession.setActionHandler('play', () => { if (currentClip && el.paused) { el.play().catch(showTap); $('btnPause').firstChild.textContent = '⏸'; } });
    navigator.mediaSession.setActionHandler('nexttrack', () => { if (currentClip) { stopSpeech(); clipFinished(); } });
  }
} catch (e) {}
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
    const h = S.speak(clip.tts || clip.text, { voiceURI: settings.voice, rate: +settings.rate,
      onend: () => { if (speechHandle === h) { speechHandle = null; clipFinished(); } } });
    speechHandle = h;
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
  if (DUCK[settings.mode]) { S.startDuck(clip.tts || clip.text); await new Promise(r => setTimeout(r, 400)); if (currentClip !== clip) return; }
  el.src = src; el.playbackRate = +settings.rate; setMediaSession(clip);
  el.onerror = () => { if (currentClip === clip) { release(); speak(clip); } };
  try { await el.play(); hideTap(); }
  catch (e) { if (e.name === 'NotAllowedError') showTap(); else { release(); speak(clip); } }
}
el.addEventListener('ended', () => clipFinished());
function clipFinished() {
  if (!currentClip) return;
  speechHandle = null; release();
  currentClip = null; $('nowBar').style.width = '100%';
  engine.ended(clock());
  setTimeout(() => { if (!engine.playing) $('nowTitle').textContent = 'Waiting for the next story…'; }, 4000);
  renderClips();
}
function showTap() { $('tapOverlay').classList.remove('hidden'); }
function hideTap() { $('tapOverlay').classList.add('hidden'); }
$('tapOverlay').onclick = async () => { S.prime(); hideTap(); try { await el.play(); } catch (e) { showTap(); } };

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
    if (S.paused()) S.resume(); else S.pause();
    $('btnPause').firstChild.textContent = S.paused() ? '▶' : '⏸'; return;
  }
  if (el.paused) { if (DUCK[settings.mode]) S.startDuck(currentClip.tts); el.play().catch(showTap); $('btnPause').firstChild.textContent = '⏸'; }
  else { el.pause(); if (DUCK[settings.mode]) S.stopDuck(); $('btnPause').firstChild.textContent = '▶'; }
};
$('btnSkip').onclick = () => { if (currentClip) { stopSpeech(); clipFinished(); } };
$('btnReplay').onclick = () => {
  const last = currentClip || byId[engine.history.at(-1)?.id];
  if (!last) return;
  if (currentClip) { stopSpeech(); release(); currentClip = null; }
  engine.playing = last; playClip(last, 'replay');
};
$('btnMore').onclick = () => {
  const base = currentClip || byId[engine.history.at(-1)?.id];
  const m = base?.more && byId[base.more];
  if (!m) return;
  if (currentClip) { stopSpeech(); release(); currentClip = null; }
  engine.playNow(m.id, clock()); savePlayed();
};
$('btnNearest').onclick = () => {
  const c = engine.nearest(); if (!c) return;
  if (currentClip) { stopSpeech(); release(); currentClip = null; }
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
  else if (!fix) { g.textContent = watchId == null ? 'GPS off' : 'GPS —'; g.className = 'chip'; }
  else { g.textContent = `GPS ±${Math.round(fix.acc)} m`; g.className = 'chip ' + (fix.acc <= 50 ? 'ok' : fix.acc <= 150 ? 'warn' : 'bad'); }
  const mph = engine.tracker.speed * 2.23694;
  $('chipSpeed').textContent = `${Math.round(mph)} mph`;
  const m = engine.match;
  $('chipRoad').textContent = m ? net.byId[m.seg].name.split(/[:→(]/)[0].trim() : 'off-network';
  $('chipRoad').className = 'chip ' + (m ? 'ok' : 'warn');
  $('chipWake').textContent = 'screen ' + wakeState; $('chipWake').className = 'chip ' + (wakeState.startsWith('on') ? 'ok' : started ? 'bad' : 'warn');
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
// Two independent ways of keeping the screen on (Auto-Lock may be capped by an organisation):
// the Screen Wake Lock API, and a tiny muted looping video with no audio track (doesn't touch
// the audio session). Re-checked every 15 s and whenever the app comes back to the front.
async function keepAwake() {
  if (!started || document.visibilityState !== 'visible') return;
  try {
    if ('wakeLock' in navigator && (!wakeLock || wakeLock.released)) {
      wakeLock = await navigator.wakeLock.request('screen');
      wakeLock.addEventListener('release', () => { renderWake(); setTimeout(keepAwake, 1000); });
    }
  } catch (e) { wakeLock = null; }
  const lockOk = !!wakeLock && !wakeLock.released;
  if (settings.awake === 'both' || !lockOk) {
    try {
      if (!noSleepVideo) {
        noSleepVideo = document.createElement('video');
        Object.assign(noSleepVideo, { muted: true, loop: true, playsInline: true, src: 'media/nosleep.mp4' });
        noSleepVideo.setAttribute('playsinline', ''); noSleepVideo.setAttribute('muted', '');
        noSleepVideo.style.cssText = 'position:fixed;width:2px;height:2px;opacity:0.02;bottom:0;left:0;pointer-events:none';
        document.body.appendChild(noSleepVideo);
      }
      if (noSleepVideo.paused) await noSleepVideo.play();
    } catch (e) {}
  } else if (noSleepVideo && !noSleepVideo.paused) noSleepVideo.pause();
  renderWake();
}
function renderWake() {
  const lockOk = !!wakeLock && !wakeLock.released, vidOk = !!noSleepVideo && !noSleepVideo.paused;
  wakeState = lockOk && vidOk ? 'on (lock + video)' : lockOk ? 'on' : vidOk ? 'on (video)' : 'OFF: tap screen every few min';
  const c = $('chipWake'); c.textContent = 'screen ' + wakeState; c.className = 'chip ' + (wakeState.startsWith('on') ? 'ok' : 'bad');
}
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') keepAwake(); });
setInterval(keepAwake, 15000);

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
  if (currentClip) { stopSpeech(); release(); currentClip = null; }
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
    E: 'speechSynthesis: the phone’s own voice instead of the recordings. Robotic unless you install an Apple “Premium” voice (see below).',
    G: 'Recommended (your test, 23 Oct): the natural recorded voice; the music ducks while it talks and comes back afterwards. Keep the ring/silent switch OFF in this mode.',
    H: 'Like G (also ducked and restored in your test), with the “transient” session.',
    F: 'ambient: meant to mix with music without ducking; may be silenced by the silent switch.',
  };
  let res = {}; try { res = JSON.parse(localStorage.getItem('audioTestResults') || '{}'); } catch (e) {}
  $('modeHint').textContent = hints[settings.mode] + (res[settings.mode] ? ` Your test result for ${settings.mode}: “${res[settings.mode]}”.` : '');
  renderVoices();
  $('histInfo').textContent = `${played.size} of ${clips.length} clips played (saved on this phone, so a reload never repeats them).`;
}
function renderVoices() {
  const list = S.englishVoices(), cur = S.pickVoice(settings.voice);
  $('voiceSel').innerHTML = list.length ? list.map(v => `<option value="${esc(v.voiceURI)}" ${cur && v.voiceURI === cur.voiceURI ? 'selected' : ''}>${esc(v.name)} (${esc(v.lang)})</option>`).join('')
    : '<option>No voices reported yet — tap Preview</option>';
  $('voiceHint').textContent = S.isGood(cur) ? `Using ${cur.name}: a high-quality Apple voice.`
    : 'No Premium/Enhanced voice found. On the iPhone: Settings → Accessibility → Spoken Content → Voices → English → pick e.g. “Ava (Premium)”, “Zoe (Premium)” or “Evan (Enhanced)” (British: “Serena (Premium)”, “Jamie (Premium)”) and download it (free, ~200–400 MB). Then reopen this app and choose it here.';
}
$('voiceSel').onchange = () => { settings.voice = $('voiceSel').value; saveSettings(); renderVoices(); };
$('btnVoicePreview').onclick = () => {
  S.speak('Welcome to the Napa Valley. On your left, the Mayacamas Mountains; on your right, the Vaca range. Guerneville is still about two hours away.',
    { voiceURI: settings.voice, rate: +settings.rate });
  setTimeout(renderVoices, 500);
};
try { speechSynthesis.addEventListener('voiceschanged', () => { if (!$('setView').classList.contains('hidden')) renderVoices(); }); } catch (e) {}

document.querySelectorAll('.seg').forEach(s => s.onclick = e => {
  const v = e.target.closest('button')?.dataset.v; if (!v) return;
  settings[s.dataset.setting] = v; saveSettings(); renderSettings();
  if (s.dataset.setting === 'talk') engine.setTalk(v);
  if (s.dataset.setting === 'rate' && el.src) el.playbackRate = +v;
  if (s.dataset.setting === 'simSpeed') sim.mult = +v;
  if (s.dataset.setting === 'awake') keepAwake();
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
    if (currentClip) { stopSpeech(); release(); currentClip = null; }
    engine.playing = null; engine.history = []; engine.tracker = new (engine.tracker.constructor)(); engine.match = null; engine.lastEnd = -1e9;
    $('nowTitle').textContent = 'Waiting for the next story…'; renderStatus(lastFix);
  }
}
$('btnSim').onclick = async () => {
  S.prime();
  // this tap also unlocks audio, so the simulator works without pressing Start (GPS stays off)
  if (!started) { started = true; await unlockAudio(); keepAwake(); }
  simStart($('simRoute').value, +settings.simSpeed, $('simAudio').checked); showTab('nowView');
};
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
  if (id === 'nowView' && !started) id = 'startView';
  document.querySelectorAll('.view').forEach(v => v.classList.toggle('hidden', v.id !== id));
  document.querySelectorAll('#tabs button').forEach(b => b.classList.toggle('on', b.dataset.view === id));
  if (id === 'clipsView') renderClips();
  if (id === 'setView') renderSettings();
}
let started = false;
document.querySelectorAll('#tabs button').forEach(b => b.onclick = () => showTab(b.dataset.view));
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
    <a href="${x.cues}" target="_blank">Cue sheet</a><a href="${x.m3u}">M3U playlist</a><a href="${x.zip}">Numbered audio files (zip)</a><a href="${x.rss}">Podcast feed</a>
    <div class="small dim">Podcast URL: <code style="word-break:break-all">${esc(new URL(x.rss, location.href).href)}</code></div></div>`).join('') || '<p class="dim">Not built yet.</p>';
  renderSettings();
  precacheAll();
  window.__rt.ready = true;
}
init().catch(e => { $('cacheDetail').textContent = 'Startup error: ' + e.message; window.__rt.error = e.message; });
