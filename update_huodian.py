#!/usr/bin/env python3
import json, urllib.request, base64, os, subprocess
DIR = '/opt/data/fishing-hk'
r = subprocess.run(["git", "remote", "get-url", "origin"], cwd=DIR, capture_output=True, text=True, timeout=5)
url = r.stdout.strip()
if "ghp_" not in url: print("❌ No token"); exit(1)
ts = url.index("ghp_"); te = url.index("@", ts)
TOKEN=url[to...= "fishing-n1-guy"; REPO = "fishing-hk"
def api(m, p, d=None):
    u = f'https://api.github.com{p}'
    h = {'User-Agent':'bot','Accept':'application/vnd.github.v3+json','Authorization':f'Bearer {TOKEN}'}
    if d: h['Content-Type']='application/json'
    b = json.dumps(d).encode() if d else None
    req = urllib.request.Request(u, data=b, headers=h, method=m)
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read())
    except: return None

ref = api('GET', f'/repos/{USERNAME}/{REPO}/git/refs/heads/main')
if not ref: print("❌ No ref"); exit(1)

with open(f'{DIR}/fish_caps/06_火點.jpg', 'rb') as f:
    content = f.read()

blob = api('POST', f'/repos/{USERNAME}/{REPO}/git/blobs',
           {'content': base64.b64encode(content).decode(), 'encoding': 'base64'})
if not blob: print("❌ Blob"); exit(1)
print(f"✅ New 火點 image: {len(content)} bytes")

tree = api('POST', f'/repos/{USERNAME}/{REPO}/git/trees', {
    'base_tree': ref['object']['sha'],
    'tree': [{'path': 'images/fish_caps/06_火點.jpg', 'mode': '100644', 'type': 'blob', 'sha': blob['sha']}]
})
if not tree: print("❌ Tree"); exit(1)
commit = api('POST', f'/repos/{USERNAME}/{REPO}/git/commits', {
    'message': '🔄 Update 火點 photo',
    'tree': tree['sha'], 'parents': [ref['object']['sha']]
})
if not commit: print("❌ Commit"); exit(1)
api('PATCH', f'/repos/{USERNAME}/{REPO}/git/refs/heads/main', {'sha': commit['sha'], 'force': True})
print("✅ Done! 火點 updated 🌙")
