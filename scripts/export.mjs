// No-GPS fallback exports per route: ordered M3U playlist, numbered zip, printable cue sheet,
// and a podcast RSS feed (Apple Podcasts → Follow a Show by URL). Output: site/exports/.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { Network, xy } from '../site/js/engine.js';

const BASE = process.env.SITE_URL || 'https://mstra09.github.io/california-road-trip/';
const { routes } = JSON.parse(fs.readFileSync('site/data/routes.json', 'utf8'));
const { clips } = JSON.parse(fs.readFileSync('site/data/clips.json', 'utf8'));
const byId = Object.fromEntries(clips.map(c => [c.id, c]));
fs.mkdirSync('site/exports', { recursive: true });

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[c]));
const fmtMin = s => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;

const index = { routes: [] };
for (const r of routes) {
  // Treat the route as a one-segment network and project every clip onto it.
  const net = new Network([{ id: r.id, name: r.name, kind: 'route', pts: r.pts }]);
  const seg = net.segs[0];
  const timeAt = s => { // OSRM time at distance s along route
    let i = seg.cum.findIndex(c => c >= s); if (i <= 0) return 0;
    const f = (s - seg.cum[i - 1]) / ((seg.cum[i] - seg.cum[i - 1]) || 1);
    return r.time[i - 1] + f * (r.time[i] - r.time[i - 1]);
  };
  const items = [];
  for (const c of clips) {
    if (c.kind === 'more' || c.lat == null) continue;
    const n = net.nearestOn(seg, xy(c.lat, c.lon));
    const reach = c.kind === 'story' ? Math.min(c.radius || 20000, 15000) : 3000;
    if (n.d > reach) continue;
    // stories are placed slightly after their nearest point so they don't crowd the local stops
    items.push({ c, s: n.s + (c.kind === 'story' ? 1500 : 0), off: n.d });
  }
  // keep stories only if the route spends time in their area; dedupe intro ordering
  items.sort((a, b) => a.s - b.s);
  const ordered = [];
  for (const it of items) {
    ordered.push(it);
    if (it.c.more && byId[it.c.more]) ordered.push({ c: byId[it.c.more], s: it.s, more: true });
  }
  const total = ordered.reduce((a, x) => a + (x.c.dur || 0), 0);
  const dir = `site/exports/${r.id}`;
  fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });

  // M3U (relative paths, playable from the site or the unzipped folder layout)
  const m3u = ['#EXTM3U', `#PLAYLIST:${r.name}`];
  ordered.forEach((x, i) => { m3u.push(`#EXTINF:${Math.round(x.c.dur || 0)},${String(i + 1).padStart(2, '0')} ${x.c.title}`); m3u.push('../../' + x.c.audio); });
  fs.writeFileSync(`site/exports/${r.id}.m3u`, m3u.join('\n') + '\n');

  // Numbered zip
  const tmp = fs.mkdtempSync('build/zip-');
  const zm3u = ['#EXTM3U'];
  ordered.forEach((x, i) => {
    const name = `${String(i + 1).padStart(2, '0')} - ${x.c.title.replace(/[\/\\:*?"<>|]/g, '').slice(0, 70)}.m4a`;
    if (fs.existsSync('site/' + x.c.audio)) fs.copyFileSync('site/' + x.c.audio, path.join(tmp, name));
    zm3u.push(`#EXTINF:${Math.round(x.c.dur || 0)},${x.c.title}`, name);
  });
  fs.writeFileSync(path.join(tmp, '00 - playlist.m3u'), zm3u.join('\n') + '\n');
  const zipPath = path.resolve(`site/exports/${r.id}.zip`);
  fs.rmSync(zipPath, { force: true });
  execFileSync('zip', ['-q', '-0', '-r', zipPath, '.'], { cwd: tmp });
  fs.rmSync(tmp, { recursive: true });

  // Cue sheet (printable)
  const rows = ordered.map((x, i) => {
    const mi = x.s / 1609.34, t = timeAt(x.s);
    const where = x.more ? 'straight after the previous clip, if you want more'
      : x.c.cue ? x.c.cue
      : x.c.kind === 'story' ? `any time around here (a long story for this stretch)`
      : `as you approach mile ${mi.toFixed(0)}${x.off > 800 ? ` (${(x.off / 1609.34).toFixed(1)} mi off the road)` : ''}`;
    return `<tr class="${x.c.kind}"><td class="n">${i + 1}</td><td class="m">${mi.toFixed(0)} mi<br><span>~${Math.round(t / 60)} min</span></td><td><b>${esc(x.c.title)}</b><br><span>Play ${esc(where)} · ${fmtMin(x.c.dur || 0)}</span></td></tr>`;
  }).join('\n');
  fs.writeFileSync(`site/exports/${r.id}-cues.html`, `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cue sheet: ${esc(r.id)}</title><style>
body{font:14px/1.35 -apple-system,system-ui,sans-serif;margin:16px;color:#111;background:#fff}h1{font-size:20px;margin:0 0 4px}p{margin:0 0 10px;color:#444}
table{border-collapse:collapse;width:100%}td{border-bottom:1px solid #ddd;padding:5px 6px;vertical-align:top}td.n{font-weight:700;width:2em;text-align:right}
td.m{white-space:nowrap;width:4.5em;color:#333}td span{color:#555;font-size:12px}tr.story td{background:#f4f6f8}tr.more td{color:#555}
@media print{body{margin:8mm;font-size:11px}a{display:none}}</style></head><body>
<h1>${esc(r.name)}</h1><p>${ordered.length} clips · ${Math.round(total / 60)} min of audio · ~${Math.round(r.time.at(-1) / 60)} min of driving. Mileage counted from Sacramento (Tower Bridge). Files are numbered to match the zip and the podcast feed. <a href="javascript:print()">Print</a></p>
<table>${rows}</table></body></html>`);

  // Podcast RSS (serial show; episode numbers keep route order)
  const now = Date.parse('2026-10-22T12:00:00Z');
  const itemsXml = ordered.map((x, i) => {
    const bytes = fs.existsSync('site/' + x.c.audio) ? fs.statSync('site/' + x.c.audio).size : 0;
    return `<item><title>${String(i + 1).padStart(2, '0')}. ${esc(x.c.title)}</title><description>${esc(x.c.text.slice(0, 600))}</description>
<enclosure url="${BASE}${x.c.audio}" length="${bytes}" type="audio/x-m4a"/><guid isPermaLink="false">${r.id}-${x.c.id}</guid>
<pubDate>${new Date(now + i * 60000).toUTCString()}</pubDate><itunes:episode>${i + 1}</itunes:episode><itunes:episodeType>full</itunes:episodeType><itunes:duration>${Math.round(x.c.dur || 0)}</itunes:duration></item>`;
  }).join('\n');
  fs.writeFileSync(`site/exports/${r.id}.xml`, `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"><channel>
<title>Road Guide: ${esc(r.name.split(':')[0])} route</title><link>${BASE}</link><language>en-us</language>
<description>${esc(r.name)}. Play episodes in order as you drive.</description>
<itunes:author>Wine Country Road Guide</itunes:author><itunes:type>serial</itunes:type><itunes:explicit>false</itunes:explicit>
<itunes:image href="${BASE}icons/icon-1400.png"/><itunes:category text="Places &amp; Travel"/>
${itemsXml}
</channel></rss>`);
  index.routes.push({ id: r.id, name: r.name, count: ordered.length, minutes: total / 60,
    m3u: `exports/${r.id}.m3u`, zip: `exports/${r.id}.zip`, cues: `exports/${r.id}-cues.html`, rss: `exports/${r.id}.xml` });
  fs.rmSync(dir, { recursive: true, force: true });
  console.log(`${r.id.padEnd(20)} ${ordered.length} clips, ${Math.round(total / 60)} min, zip ${(fs.statSync(zipPath).size / 1e6).toFixed(1)} MB`);
}
fs.writeFileSync('site/exports/index.json', JSON.stringify(index, null, 1));
