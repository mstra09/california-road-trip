#!/bin/bash
# Full content build: data -> TTS jobs -> Kokoro audio -> app data -> exports -> precache manifest.
# VOICE=bm_george scripts/build.sh   to re-render everything with another Kokoro voice.
set -euo pipefail
cd "$(dirname "$0")/.."
node scripts/build.mjs jobs
HF_HUB_OFFLINE=1 .venv/bin/python scripts/render_audio.py ${VOICE:+--voice $VOICE}
node scripts/build.mjs
node scripts/export.mjs
node scripts/build.mjs
