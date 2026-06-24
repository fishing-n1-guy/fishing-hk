#!/usr/bin/env python3
import json, urllib.request, base64, os, subprocess
DIR = '/opt/data/fishing-hk'
CAPS = os.path.join(DIR, 'fish_caps')
r = subprocess.run(["git", "remote", "get-url", "origin"], cwd=DIR, capture_output=True, text=True, timeout=5)
url = r.stdout.strip()
if "ghp_" not in url: print("No token"); exit(1)
ts = url.index("ghp_"); te = url.index("@", ts)
TOKEN=*** "fishing-n1-guy"; REPO = "fishing-hk"
def api(m, p, d=None):
    u = f'https://api.github.com{p}'
    h = {'User-Agent':'bot','Accept':'application/vnd.github.v3+json','Authorization':f'Bearer {TOKEN}'}
    if d: h['Content-Type']='application/json'
    b = json.dumps(d).encode() if d else None
    return json.loads(urllib.request.Request(u,data=b,headers=h,method=m).open().read())

ref = api('GET', f'/repos/{USERNAME}/{REPO}/git/refs/heads/main')
entries = []
for fname in ['37_鱸魚.jpg','38_牛鰍.jpg','39_門鱔.jpg','40_石狗公.jpg','41_黃鰭鮪.jpg','42_杉斑.jpg','43_坑鰜.jpg','xx_石崇魚.jpg']:
    path = os.path.join(CAPS, fname)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            content = f.read()
        blob = api('POST', f'/repos/{USERNAME}/{REPO}/git/blobs',
                   {'content': base64.b64encode(content).decode(), 'encoding': 'base64'})
        if blob:
            entries.append({'path': f'images/fish_caps/{fname}', 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
            print(f'  {fname} ({len(content)} bytes)')

tree = api('POST', f'/repos/{USERNAME}/{REPO}/git/trees',
           {'base_tree': ref['object']['sha'], 'tree': entries})
commit = api('POST', f'/repos/{USERNAME}/{REPO}/git/commits', {
    'message': 'Upload new fish cap images 37-43, 石崇魚',
    'tree': tree['sha'], 'parents': [ref['object']['sha']]
})
api('PATCH', f'/repos/{USERNAME}/{REPO}/git/refs/heads/main',
    {'sha': commit['sha'], 'force': True})
print(f'Uploaded {len(entries)} images!')
