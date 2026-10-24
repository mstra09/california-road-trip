#!/bin/bash
# Publish ./site to the gh-pages branch as a single orphan commit (keeps repo history small;
# audio files never enter main's history).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE="$(git -C "$ROOT" remote get-url origin)"
TMP="$(mktemp -d)"
rsync -a --delete --exclude '.DS_Store' "$ROOT/site/" "$TMP/"
touch "$TMP/.nojekyll"
cd "$TMP"
git init -q -b gh-pages
git add -A
git -c user.name="deploy" -c user.email="deploy@localhost" commit -q -m "Deploy $(date -u +%FT%TZ)"
git -c http.postBuffer=524288000 push -q -f "$REMOTE" gh-pages
rm -rf "$TMP"
echo "Deployed."
