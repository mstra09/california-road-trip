// End-to-end verification.
//  1. Audio: every clip's file exists, decodes, has sane duration and loudness.
//  2. Simulator in a real (headless) browser: every route and road segment, both directions
//     where it matters, through the in-page engine. Asserts order, no repeats, gaps <= 12 min.
//  3. Deployed site: load, precache everything, go offline, reload, confirm it still works.
// Usage: node scripts/verify.mjs [--skip-audio] [--skip-local] [--skip-deployed] [--url URL]
import fs from 'node:fs';
import { execFileSync, spawn, spawnSync } from 'node:child_process';
import { chromium } from 'playwright';

const args = process.argv.slice(2);
const URL_DEPLOYED = args.includes('--url') ? args[args.indexOf('--url') + 1] : 'https://mstra09.github.io/california-road-trip/';
const { clips } = JSON.parse(fs.readFileSync('site/data/clips.json', 'utf8'));
let failures = 0;
const fail = m => { failures++; console.log('  ✗ ' + m); };
const launch = () => chromium.launch({ channel: 'chrome', headless: true });

// ---------------------------------------------------------------- 1. audio
if (!args.includes('--skip-audio')) {
  console.log('\n[1] Audio files');
  const louds = [];
  for (const c of clips) {
    const f = 'site/' + c.audio;
    if (!fs.existsSync(f)) { fail(`${c.id}: missing ${f}`); continue; }
    const run = spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', f, '-af', 'ebur128', '-f', 'null', '-']);
    const out = run.stderr.toString();
    if (run.status !== 0) { fail(`${c.id}: does not decode`); continue; }
    const I = +(out.match(/I:\s+(-?[\d.]+) LUFS/g) || []).pop()?.match(/-?[\d.]+/)[0];
    const dur = +execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).toString();
    louds.push(I);
    if (!(dur > 15 && dur < 260)) fail(`${c.id}: odd duration ${dur}s`);
    if (!(I > -15 && I < -11)) fail(`${c.id}: loudness ${I} LUFS outside -15..-11`);
  }
  const mb = clips.reduce((a, c) => a + (fs.existsSync('site/' + c.audio) ? fs.statSync('site/' + c.audio).size : 0), 0) / 1e6;
  louds.sort((a, b) => a - b);
  console.log(`  ${clips.length} files, ${mb.toFixed(1)} MB, loudness ${louds[0]} to ${louds.at(-1)} LUFS (median ${louds[Math.floor(louds.length / 2)]})`);
}

// ---------------------------------------------------------------- 2. simulator in browser
if (!args.includes('--skip-local')) {
  console.log('\n[2] Simulator (headless Chrome, real page + engine)');
  const srv = spawn('python3', ['-m', 'http.server', '8766', '--directory', 'site'], { stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 800));
  const browser = await launch();
  const page = await browser.newPage();
  page.on('pageerror', e => fail('page error: ' + e.message));
  await page.goto('http://localhost:8766/', { waitUntil: 'load' });
  await page.waitForFunction(() => window.__rt?.ready, null, { timeout: 30000 });
  const { segments } = JSON.parse(fs.readFileSync('site/data/network.json', 'utf8'));
  const { routes } = JSON.parse(fs.readFileSync('site/data/routes.json', 'utf8'));
  const ids = [...routes.map(r => r.id), ...segments.map(s => s.id)];
  for (const talk of ['normal', 'sparse', 'chatty']) {
    console.log(`  talkativeness: ${talk}`);
    for (const id of ids) {
      const res = await page.evaluate(([id, talk]) => window.__rt.runRoute(id, talk), [id, talk]);
      const log = res.log, T = res.driveSec;
      let prevEnd = 0, maxGap = 0, at = 0, narr = 0, ordered = true;
      for (let i = 0; i < log.length; i++) {
        const e = log[i];
        if (i && e.t < log[i - 1].t) ordered = false;
        if (i && e.t < log[i - 1].t + (log[i - 1].dur || 0) - 1) fail(`${id}/${talk}: overlap at ${Math.round(e.t / 60)} min`);
        if (e.t - prevEnd > maxGap) { maxGap = e.t - prevEnd; at = prevEnd; }
        prevEnd = e.t + (e.dur || 0); narr += e.dur || 0;
      }
      if (T - prevEnd > maxGap && T - prevEnd > 0) { maxGap = T - prevEnd; at = prevEnd; }
      const idsHeard = log.map(e => e.id), rep = idsHeard.filter((x, i) => idsHeard.indexOf(x) !== i);
      if (rep.length) fail(`${id}/${talk}: repeats ${rep}`);
      if (!ordered) fail(`${id}/${talk}: clips out of order`);
      if (maxGap > 720) fail(`${id}/${talk}: gap ${(maxGap / 60).toFixed(1)} min at ${Math.round(at / 60)} min`);
      if (talk === 'normal' || id.length < 20 && routes.some(r => r.id === id))
        console.log(`    ${id.padEnd(20)} drive ${String(Math.round(T / 60)).padStart(3)} min  narration ${String(Math.round(narr / 60)).padStart(3)} min  clips ${String(log.length).padStart(3)}  max gap ${(maxGap / 60).toFixed(1)} min`);
    }
  }
  await browser.close(); srv.kill();
}

// ---------------------------------------------------------------- 3. deployed + offline
if (!args.includes('--skip-deployed')) {
  console.log(`\n[3] Deployed site offline test: ${URL_DEPLOYED}`);
  const browser = await launch();
  const ctx = await browser.newContext({ permissions: ['geolocation'], geolocation: { latitude: 38.5803, longitude: -121.5085 } });
  const page = await ctx.newPage();
  page.on('pageerror', e => fail('page error: ' + e.message));
  await page.goto(URL_DEPLOYED, { waitUntil: 'load' });
  await page.waitForFunction(() => window.__rt?.ready, null, { timeout: 60000 });
  await page.evaluate(() => navigator.serviceWorker.ready);
  const t0 = Date.now();
  await page.waitForFunction(() => { const c = window.__rt.cacheState; return c.total > 0 && c.have === c.total && !c.running; }, null, { timeout: 600000, polling: 1000 });
  const cs = await page.evaluate(() => window.__rt.cacheState);
  console.log(`  precached ${cs.have}/${cs.total} files, ${(cs.bytes / 1e6).toFixed(1)} MB in ${Math.round((Date.now() - t0) / 1000)} s`);
  // reload once online so the service worker controls the page, then cut the network
  await page.reload({ waitUntil: 'load' });
  await page.waitForFunction(() => !!navigator.serviceWorker.controller, null, { timeout: 30000 });
  await ctx.setOffline(true);
  await page.reload({ waitUntil: 'load' });
  await page.waitForFunction(() => window.__rt?.ready || window.__rt?.error, null, { timeout: 30000 });
  await page.waitForFunction(() => document.getElementById('chipOffline').textContent.includes('✓'), null, { timeout: 30000 }).catch(() => fail('offline chip never showed ✓'));
  const off = await page.evaluate(async () => {
    const clips = (await (await fetch('data/clips.json')).json()).clips;
    const pick = [clips[0], clips[Math.floor(clips.length / 2)], clips.at(-1)];
    const audio = [];
    for (const c of pick) { const r = await fetch(c.audio); audio.push([c.id, r.status, (await r.arrayBuffer()).byteLength]); }
    const ranged = await fetch(pick[0].audio, { headers: { Range: 'bytes=0-1023' } });
    const run = window.__rt.runRoute('main');
    return { ready: window.__rt.ready, err: window.__rt.error, offlineChip: document.getElementById('chipOffline').textContent,
      audio, range: [ranged.status, ranged.headers.get('content-range')], simClips: run.log.length,
      pages: await Promise.all(['exports/main-cues.html', 'audio-test/', 'icons/icon-192.png'].map(async u => [u, (await fetch(u)).status])) };
  });
  console.log('  offline:', JSON.stringify(off));
  if (!off.ready) fail('app did not start offline');
  if (off.audio.some(a => a[1] !== 200 || a[2] < 1000)) fail('audio not served offline');
  if (off.range[0] !== 206) fail('range request not served as 206');
  if (off.pages.some(p => p[1] !== 200)) fail('some pages not available offline');
  if (off.simClips < 20) fail('simulator did not run offline');
  await browser.close();
}

console.log(failures ? `\n${failures} FAILURE(S)` : '\nALL CHECKS PASSED');
process.exitCode = failures ? 1 : 0;
