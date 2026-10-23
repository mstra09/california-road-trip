# Wine Country Road Guide

A GPS-triggered audio tour from Sacramento to Guerneville, covering the whole road network between them
(I-80, I-505/SR 128 via Lake Berryessa, Jameson Canyon, Carneros, SR 29, the Silverado Trail, the
Mayacamas cross-roads, the Sonoma Valley, Alexander Valley, US 101, River Road, Westside Road, SR 116,
Guerneville Road and the Bohemian Highway). It runs as a home-screen web app on an iPhone and works fully
offline once cached.

- **App:** https://mstra09.github.io/california-road-trip/
- **Audio behaviour test:** https://mstra09.github.io/california-road-trip/audio-test/
- **No-GPS backups** (also linked from the app's Backup tab):
  | Route | Cue sheet | Playlist | Zip | Podcast feed |
  |---|---|---|---|---|
  | Main: I-80 → Jameson → SR 29 → Calistoga → Mark West → River Rd | [cues](https://mstra09.github.io/california-road-trip/exports/main-cues.html) | [m3u](https://mstra09.github.io/california-road-trip/exports/main.m3u) | [zip](https://mstra09.github.io/california-road-trip/exports/main.zip) | `https://mstra09.github.io/california-road-trip/exports/main.xml` |
  | Lake Berryessa: I-505 → SR 128 → Calistoga → Alexander Valley → Healdsburg → Westside Rd | [cues](https://mstra09.github.io/california-road-trip/exports/berryessa-cues.html) | [m3u](https://mstra09.github.io/california-road-trip/exports/berryessa.m3u) | [zip](https://mstra09.github.io/california-road-trip/exports/berryessa.zip) | `https://mstra09.github.io/california-road-trip/exports/berryessa.xml` |
  | Sonoma: Carneros → Sonoma → Kenwood → Santa Rosa → Sebastopol → SR 116 | [cues](https://mstra09.github.io/california-road-trip/exports/sonoma-cues.html) | [m3u](https://mstra09.github.io/california-road-trip/exports/sonoma.m3u) | [zip](https://mstra09.github.io/california-road-trip/exports/sonoma.zip) | `https://mstra09.github.io/california-road-trip/exports/sonoma.xml` |
  | Silverado Trail → Calistoga Rd → Santa Rosa → Bohemian Hwy | [cues](https://mstra09.github.io/california-road-trip/exports/silverado_bohemian-cues.html) | [m3u](https://mstra09.github.io/california-road-trip/exports/silverado_bohemian.m3u) | [zip](https://mstra09.github.io/california-road-trip/exports/silverado_bohemian.zip) | `https://mstra09.github.io/california-road-trip/exports/silverado_bohemian.xml` |

  Podcast: Apple Podcasts → Library → ⋯ → *Follow a Show by URL* → paste the feed URL. Episodes are numbered in
  driving order (serial show), so play them from #1.

## Tonight (hotel Wi-Fi)
1. Open the app URL in **Safari** → Share → **Add to Home Screen**.
2. Open it **from the home screen icon** (the home-screen app has its own storage, separate from Safari).
3. Wait on the start screen until it says **Offline ready: N/N files** (about 80 MB).
4. Settings → **Open the audio test page** (from inside the home-screen app), start Spotify, and try modes
   A–F with *Play in 20s*. Record what Spotify does with the result buttons.
5. Back in Settings, pick the **music mode** that behaved best (default is B).
6. Settings → Simulator → pick a route, 30× or 60×, tick or untick real audio → **Start simulator**. Watch
   clips fire, then **Stop**. The simulator keeps its own history, so it never uses up tomorrow's clips.
   (If you ever do want a clean slate: Settings → Reset played history.)

## Tomorrow
1. iPhone: Settings → Display & Brightness → **Auto-Lock: Never**. Phone on the **charger**, connected to the car.
2. Ring/silent switch **off silent** (some music modes respect it).
3. Open the app from the home screen **before leaving Sacramento**, check the chip says **offline ✓**, tap **▶ Start**,
   allow location. Leave the app in front: iOS pauses web apps (and their GPS) in the background.
4. Passenger controls: pause / skip / replay / tell me more / nearest; the Clips tab lists everything by area,
   including anything you missed. If the screen flashes **TAP TO PLAY**, one tap fixes it.

## How it works
- **Road network** (`scripts/fetch-roads.mjs`): waypoints in `data/roads.src.json` (on-road points checked with
  the OpenStreetMap Overpass API) routed through the public OSRM server → 19 road segments plus 4 full route
  variants with per-point travel time. Hardcoded waypoints are the fallback if OSRM is down.
- **Sources** (`scripts/fetch-sources.mjs`, `scripts/fetch-articles.mjs`): every road sampled every ~1 km;
  Wikipedia GeoSearch (10 km radius) found 812 nearby articles; Macrostrat gave bedrock geology at 456 points;
  ~320 Wikipedia articles were fetched in full and cached in `cache/` (git-ignored).
- **Narration** (`content/*.json`): 118 clips (75 place clips, 8 area intros, 23 long stories, 12 "tell me more"
  follow-ups), written only from the cached sources, each listing its source URLs. See
  [docs/FACTCHECK.md](docs/FACTCHECK.md) for the checking process and the 20-clip re-check.
- **Pronunciation**: `content/pronounce.json` respells names only in the TTS text (Guerneville → "Gurn-vill",
  St. Helena → "Saint Huh-lee-nuh", Suisun → "Suh-soon", Carneros, Wappo, Patwin, Vacaville, …).
- **Voice**: [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), open-weight, run locally in `.venv`
  (no API key). Six voices were rendered for comparison in `voice-samples/` (also in the app's Settings).
  **Default: `af_heart`** (American female), the voice rated highest in Kokoro's own voice quality grades, with a
  warm, unhurried delivery suited to narration. Audio is loudness-normalised (EBU R128, −16 LUFS, −1.5 dBTP),
  has short fades, and is mono AAC 64 kbps: ~78 MB total.
- **Build** (`scripts/build.sh`): content → TTS jobs → Kokoro render (skips unchanged clips; filenames carry a
  content hash) → app data with each clip's position along every road it applies to → exports → precache list.
- **Engine** (`site/js/engine.js`): map-matches each GPS fix to the road network, works out direction from
  progress along the road, and looks ahead 45 s at current speed (250 m–2.6 km). One queue, never overlapping;
  higher priority first; a minimum quiet gap between ordinary clips (sparse 4 min / normal 75 s / chatty 12 s);
  long stories fill silences (after 5.5 min in normal); an emergency tier guarantees nothing longer than ~10 min.
  Fixes worse than 150 m are ignored; jumps over 250 km/h are rejected unless confirmed; heading uses a 60 m
  baseline. Played history persists in localStorage, so a reload never repeats a clip.
- **App** (`site/js/app.js`): one persistent `<audio>` element unlocked by the Start tap; clips are played from
  the offline cache as blob URLs; on a missing file it falls back to `speechSynthesis`. After every clip the
  element is emptied and the audio session handed back. Wake Lock with a muted-video fallback;
  `navigator.storage.persist()`; Media Session metadata, so the clip title shows on CarPlay and the steering-wheel
  buttons pause or skip.
- **Offline**: the page downloads every file in `precache.json` into Cache Storage with a progress bar; the service
  worker serves everything cache-first and answers Range requests with 206 (Safari needs this for audio).

### Re-render with another voice
```bash
VOICE=bm_george scripts/build.sh && scripts/deploy.sh
```
Voices: `af_heart`, `af_bella`, `am_michael`, `am_fenrir`, `am_puck`, `bf_emma`, `bf_isabella`, `bm_george`,
`bm_fable`, `bm_lewis` (downloaded into `models/kokoro/voices/`). British voices start with `b`.

### Hosting
GitHub Pages, public repo `mstra09/california-road-trip`. `scripts/deploy.sh` publishes `site/` as a single
orphan commit on `gh-pages`, so audio never bloats the main branch history. No backend, no keys, no cost.

## Verification (run `npm test`, i.e. `node scripts/verify.mjs`)
- **Audio**: all 118 files exist, decode, are 20 s–4 min long, and measure −16 ±1 LUFS.
- **Simulator in headless Chrome** (the real page and engine) over all 4 routes and all 19 road segments, in
  sparse, normal and chatty modes: clips in order, no repeats, no overlaps, no silence over 12 minutes.
  Normal mode per route: main 186 min of driving, 64 min of narration, 47 clips, longest silence 5.6 min;
  Berryessa 260/70/51, 6.4; Sonoma 178/61/46, 5.6; Silverado–Bohemian 215/74/53, 5.5.
  `node scripts/simulate.mjs normal --noisy` repeats this with GPS jitter, weak fixes, dropouts and jumps.
- **Deployed site**: loaded in headless Chrome, precached in full, network cut, reloaded: the app starts, audio
  and pages are served from cache (including 206 Range responses), and the simulator runs.
- **Facts**: see [docs/FACTCHECK.md](docs/FACTCHECK.md).

## Known limitations
- **Spotify behaviour per mode was not tested on a real iPhone** (I can't drive one from here). That's what the
  audio test page is for. What each mode asks iOS for:
  - **A plain** and **D playback**: a media-playback session; expect Spotify to **pause**, and it may not resume
    on its own.
  - **B transient** (default): WebKit's hint for short announcements; the hope is Spotify **keeps playing,
    ducked or mixed**. If it does, nothing needs to "resume". If you hear nothing, check the silent switch.
  - **C transient-solo**: asks other audio to stop while we speak; whether Spotify resumes afterwards depends on
    iOS and Spotify.
  - **E speech**: the robotic built-in voice; usually ducks other audio. Ignores the recorded files.
  - **F ambient**: mixes with music at full volume and may be muted by the silent switch.
  After each clip the app empties the audio element and resets the session, which is the most a web page can do
  to let Spotify resume.
- The app must stay **on screen**. iOS suspends web apps in the background, which stops GPS and audio. Auto-Lock
  Never plus the Wake Lock handles this; don't switch to Maps full-screen for long.
- If you pass a place while another clip is playing, its clip may be skipped (it's never lost: it's in the Clips
  tab, marked unplayed). In normal mode the engine allows short gaps for important places.
- OSRM travel times drive the simulator; real traffic will be slower, which only means more room between clips.
- Coverage is densest on the four routes. The cross-roads (Oakville Grade, Spring Mountain, Calistoga Rd,
  Guerneville Rd) have a few clips each, plus area stories.
- Old Faithful Geyser of California is not covered (no fetchable source). Sources are mostly Wikipedia; where
  Wikipedia hedges, the narration hedges too.
