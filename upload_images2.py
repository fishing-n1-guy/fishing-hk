#!/usr/bin/env python3
"""Upload all remaining fish images. Fix for the syntax error."""
import sys, urllib.request, urllib.error, json, base64, os, glob

DIR = '/opt/data/fishing-hk'
IMG_DIR = os.path.join(DIR, 'fish_pdf_images')
REPO_PATH = 'images/fish'

import subprocess
r = subprocess.run(["git", "remote", "get-url", "origin"], cwd=DIR, capture_output=True, text=True, timeout=5)
url = r.stdout.strip()
# Extract token from URL
if "ghp_" not in url:
    print("❌ No token")
    sys.exit(1)
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
    print("❌ Branch not found"); sys.exit(1)

# Get all images
images = sorted(glob.glob(os.path.join(IMG_DIR, '*.jpg')), key=lambda f: -os.path.getsize(f))

# Upload in batches of 20
for batch_start in range(20, len(images), 20):
    batch = images[batch_start:batch_start + 20]
    entries = []
    for img_path in batch:
        fname = os.path.basename(img_path)
        with open(img_path, 'rb') as f:
            content = f.read()
        if len(content) < 3000:
            continue
        blob = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/blobs',
                   {'content': base64.b64encode(content).decode(), 'encoding': 'base64'})
        if blob:
            entries.append({'path': f'{REPO_PATH}/{fname}', 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
    if not entries:
        continue
    tree = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/trees',
               {'base_tree': ref['object']['sha'], 'tree': entries})
    if not tree: continue
    commit = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/commits', {
        'message': f'📸 Fish images batch {batch_start//20 + 1}',
        'tree': tree['sha'], 'parents': [ref['object']['sha']]
    })
    if commit:
        r2 = api('PATCH', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/main',
                 {'sha': commit['sha'], 'force': True})
        if r2:
            print(f"✅ Batch {batch_start//20 + 1}: {len(entries)} images")
            ref = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/main')

print(f"\n🎉 Done! https://github.com/{USERNAME}/{REPO_NAME}/tree/main/{REPO_PATH}")
