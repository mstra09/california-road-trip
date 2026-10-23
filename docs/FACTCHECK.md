# Fact-check log

Narration is written only from sources fetched by the build scripts (Wikipedia full-text extracts in
`cache/wiki/pages/`, Macrostrat geologic-map units in `cache/geo/macrostrat.json`). Every clip lists its
source URLs in `content/*.json` and in the app ("source 1, 2…" links under the transcript).

## Method
1. **While writing**: each clip was checked against its sources sentence by sentence; unsupported claims were
   cut or reworded (examples removed: "Croatian-born" Grgich, Calistoga mud baths, the Tubbs Lane–Montelena link,
   "Solano County is named after Chief Solano", a "star" on the Bear Flag, "hurricane-force" winds,
   "tilted" Great Valley beds, Nagasawa's nationality, several invented Macrostrat citation points).
2. **Numbers sweep** (`python3 scripts/factcheck.py numbers`): every number in every clip must appear in that
   clip's own sources. 18 flags, all benign (road numbers like "Highway 128", decades like "1980s",
   rounding like "over 67,000 acres" for 67,484, and geologic-stage ages derived from the cited stage).
3. **Random re-check of 20 clips** (`python3 scripts/factcheck.py sample 20 2026`): each sentence printed beside
   its best-matching source sentence and reviewed by hand.

## Random sample (seed 2026) and outcome
| Clip | Result |
|---|---|
| fairfield | OK |
| fires_story | **Fixed**: "evacuated for the second time in three years" → "second time since 2017" (source says "in four years") |
| berryessa_monument | OK |
| franciscan_sage | OK |
| santa_rosa | OK |
| goldrush_story | OK |
| travis | OK |
| farm_labour_story | OK |
| napa_geology | OK |
| ag_preserve_story | OK |
| haraszthy | OK |
| jack_london | OK |
| schellville | OK |
| guerneville (more: Armstrong Redwoods) | OK |
| camp_meeker | OK |
| sonoma_intro (more: Blue Wing Inn) | OK |
| bliss | OK |
| spring_mtn_district | OK |
| westside_blueschist | OK |
| occidental | **Fixed**: Gottlieb bought the land in 1966 but opened it to all comers in 1967 |

## Known soft spots
- Wikipedia is the main source; where Wikipedia itself is uncertain the narration says so ("the story goes",
  "is said to", "according to").
- General geology definitions (ophiolite, serpentinite, blueschist) are sourced from the matching Wikipedia
  articles, which were fetched for that purpose.
- Old Faithful Geyser of California was dropped: no fetchable source.
