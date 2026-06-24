#!/usr/bin/env python3
"""Upload fish cap images to GitHub."""
import json, urllib.request, urllib.error, base64, os, glob, subprocess

DIR = '/opt/data/fishing-hk'
CAPS_DIR = os.path.join(DIR, 'fish_caps')

r = subprocess.run(["git", "remote", "get-url", "origin"], cwd=DIR, capture_output=True, text=True, timeout=5)
url = r.stdout.strip()
if "ghp_" not in url:
    print("❌ No token found"); exit(1)
token_start = url.index("ghp_")
token_end = url.index("@", token_start)
TOKEN = url[token_start:token_end]

USERNAME = "fishing-n1-guy"
REPO_NAME = "fishing-hk"

def api(method, path, data=None):
    url = f'https://api.github.com{path}'
    headers = {
        'User-Agent': 'fishing-hk-bot/1.0',
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {TOKEN}'
    }
    body = json.dumps(data).encode() if data else None
    if body: headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return None

ref = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/main')
if not ref:
    print("❌ Branch not found"); exit(1)

entries = []
for fpath in sorted(glob.glob(os.path.join(CAPS_DIR, '*.jpg'))):
    fname = os.path.basename(fpath)
    repo_path = f'images/fish_caps/{fname}'
    with open(fpath, 'rb') as f:
        content = f.read()
    blob = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/blobs',
               {'content': base64.b64encode(content).decode(), 'encoding': 'base64'})
    if blob:
        entries.append({'path': repo_path, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
        print(f'  📄 {fname} ({len(content)} bytes)')

if not entries:
    print("❌ No images to upload"); exit(1)

tree = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/trees',
           {'base_tree': ref['object']['sha'], 'tree': entries})
if not tree:
    print("❌ Tree creation failed"); exit(1)

commit = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/commits', {
    'message': '📸 Add fish cap images from Jay',
    'tree': tree['sha'],
    'parents': [ref['object']['sha']]
})
if not commit:
    print("❌ Commit failed"); exit(1)

result = api('PATCH', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/main',
             {'sha': commit['sha'], 'force': True})
if result:
    print(f'\n🎉 Uploaded {len(entries)} fish images!')
else:
    print("❌ Push failed")
