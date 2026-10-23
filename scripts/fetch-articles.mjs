// Fetch full plain-text Wikipedia articles listed in content/sources.txt (one title per line;
// "#" comments). Saved to cache/wiki/pages/<slug>.json as {title, url, text}. Uses curl.
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
const UA = 'california-road-trip-audio-guide/1.0 (https://github.com/mstra09/california-road-trip)';
fs.mkdirSync('cache/wiki/pages', { recursive: true });
const titles = fs.readFileSync('content/sources.txt', 'utf8').split('\n').map(s => s.replace(/#.*/, '').trim()).filter(Boolean);
export const slug = t => t.replace(/[^\w]+/g, '_').replace(/^_|_$/g, '');
let n = 0, miss = [];
for (const t of [...new Set(titles)]) {
  const f = `cache/wiki/pages/${slug(t)}.json`;
  if (fs.existsSync(f)) continue;
  const url = `https://en.wikipedia.org/w/api.php?action=query&prop=extracts|info&inprop=url&explaintext=1&exsectionformat=wiki&redirects=1&titles=${encodeURIComponent(t)}&format=json&formatversion=2`;
  let j = null;
  for (let i = 0; i < 4 && !j; i++) {
    try { j = JSON.parse(execFileSync('curl', ['-s', '--max-time', '40', '-A', UA, url], { maxBuffer: 64e6 }).toString()); }
    catch (e) { execFileSync('sleep', [String(3 * (i + 1))]); }
  }
  const p = j?.query?.pages?.[0];
  if (!p || p.missing || !p.extract) { miss.push(t); continue; }
  fs.writeFileSync(f, JSON.stringify({ title: p.title, url: p.fullurl || `https://en.wikipedia.org/wiki/${encodeURIComponent(p.title.replace(/ /g, '_'))}`, text: p.extract }));
  n++;
  execFileSync('sleep', ['0.3']);
}
console.log(`fetched ${n}; missing: ${miss.join(' | ') || 'none'}`);
