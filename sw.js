// Offline-first service worker. The page itself fills the cache (with progress) from
// precache.json; this worker serves from that cache, handling Range requests for iOS audio.
const CACHE = 'rt-files-v2';   // bump to force a clean re-download on every phone
self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil((async () => {
  for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
  await self.clients.claim();
})()));

async function rangeResponse(req, res) {
  const range = req.headers.get('range');
  if (!range) return res;
  const buf = await res.arrayBuffer();
  const m = /bytes=(\d*)-(\d*)/.exec(range);
  const size = buf.byteLength;
  let start = m && m[1] ? +m[1] : 0, end = m && m[2] ? +m[2] : size - 1;
  if (m && !m[1] && m[2]) { start = size - +m[2]; end = size - 1; }
  end = Math.min(end, size - 1);
  return new Response(buf.slice(start, end + 1), { status: 206, headers: {
    'Content-Type': res.headers.get('Content-Type') || 'audio/mp4',
    'Content-Range': `bytes ${start}-${end}/${size}`, 'Content-Length': String(end - start + 1), 'Accept-Ranges': 'bytes' } });
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;
  if (url.searchParams.has('v')) return;   // precache downloads (?v=hash) always go to the network
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    // precache.json and exports index: network first so updates are noticed, cache as fallback
    if (url.pathname.endsWith('/precache.json')) {
      try { const r = await fetch(req, { cache: 'no-store' }); if (r.ok) return r; } catch (err) {}
    }
    let hit = await cache.match(req, { ignoreSearch: true });
    if (!hit && req.mode === 'navigate') hit = await cache.match(new URL(url.pathname.endsWith('/') ? url.pathname + 'index.html' : url.pathname, location.href).href) || await cache.match('./index.html');
    if (!hit && url.pathname.endsWith('/')) hit = await cache.match(url.pathname + 'index.html');
    if (hit) return rangeResponse(req, hit);
    try { return await fetch(req); }
    catch (err) { return new Response('Offline and not cached', { status: 503 }); }
  })());
});
