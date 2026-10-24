"""Incremental deploy of ./site to gh-pages using the GitHub git-data API.

Only files whose git blob hash differs from what's live are uploaded, so it works on slow or
flaky connections where pushing the whole ~80 MB site times out. Files no longer in ./site
are deleted from the live branch. Usage: python3 scripts/deploy_incremental.py
"""
import json, os, subprocess, sys, base64, tempfile

REPO = 'repos/mstra09/california-road-trip'
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')

def gh(path, method='GET', data=None, retries=4):
    for attempt in range(retries):
        cmd = ['gh', 'api', path, '-X', method]
        inp = None
        if data is not None:
            cmd += ['--input', '-']; inp = json.dumps(data).encode()
        r = subprocess.run(cmd, input=inp, capture_output=True)
        if r.returncode == 0:
            return json.loads(r.stdout or b'null')
        print('  retry', path, r.stderr.decode()[:120], file=sys.stderr)
    raise SystemExit(f'gh api failed: {path}')

def local_files():
    out = {}
    for d, _, fs in os.walk(ROOT):
        for f in fs:
            if f.startswith('.') and f != '.nojekyll': continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
            sha = subprocess.run(['git', 'hash-object', p], capture_output=True, text=True).stdout.strip()
            out[rel] = (p, sha)
    return out

base = gh(f'{REPO}/git/ref/heads/gh-pages')['object']['sha']
base_tree = gh(f'{REPO}/git/commits/{base}')['tree']['sha']
live = {e['path']: e['sha'] for e in gh(f'{REPO}/git/trees/{base_tree}?recursive=1')['tree'] if e['type'] == 'blob'}
open(os.path.join(ROOT, '.nojekyll'), 'a').close()
local = local_files()

changed = [rel for rel, (_, sha) in local.items() if live.get(rel) != sha]
deleted = [rel for rel in live if rel not in local]
mb = sum(os.path.getsize(local[r][0]) for r in changed) / 1e6
print(f'{len(changed)} changed/new files ({mb:.1f} MB), {len(deleted)} to delete')
if not changed and not deleted:
    print('Nothing to deploy.'); sys.exit(0)

entries = []
for i, rel in enumerate(sorted(changed), 1):
    with open(local[rel][0], 'rb') as fh:
        blob = gh(f'{REPO}/git/blobs', 'POST', {'encoding': 'base64', 'content': base64.b64encode(fh.read()).decode()})
    entries.append({'path': rel, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
    if i % 10 == 0 or i == len(changed): print(f'  uploaded {i}/{len(changed)}')
entries += [{'path': rel, 'mode': '100644', 'type': 'blob', 'sha': None} for rel in deleted]
tree = gh(f'{REPO}/git/trees', 'POST', {'base_tree': base_tree, 'tree': entries})['sha']
commit = gh(f'{REPO}/git/commits', 'POST', {'message': f'Incremental deploy: {len(changed)} changed, {len(deleted)} deleted', 'tree': tree, 'parents': [base]})['sha']
gh(f'{REPO}/git/refs/heads/gh-pages', 'PATCH', {'sha': commit, 'force': False})
print('Deployed', commit[:7])
