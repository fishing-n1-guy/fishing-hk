#!/usr/bin/env python3
"""Upload all PDF fish images to GitHub repo."""
import sys, urllib.request, urllib.error, json, base64, os, glob

DIR = '/opt/data/fishing-hk'
IMG_DIR = os.path.join(DIR, 'fish_pdf_images')
REPO_PATH = 'images/fish'  # Where to put images in the repo

# Get token from git remote
import subprocess
r = subprocess.run(["git", "remote", "get-url", "origin"], cwd=DIR, capture_output=True, text=True, timeout=5)
url = r.stdout.strip()
if "ghp_" in url:
    token_start = url.index("ghp_")
    token_end = url.index("@", token_start)
    TOKEN = url[token_start:token_end]
else:
    print("❌ No token found")
    sys.exit(1)

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
        err = e.read().decode()[:200]
        print(f"  HTTP {e.code}")
        return None

# Get latest commit
ref = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/main')
if not ref:
    print("❌ Branch not found")
    sys.exit(1)

# Get all images sorted by size (largest first = most likely fish photos)
images = sorted(glob.glob(os.path.join(IMG_DIR, '*.jpg')), key=lambda f: -os.path.getsize(f))
print(f"Found {len(images)} images to upload")

# Upload images in batches of 10 to avoid rate limits
entries = []
for img_path in images[:20]:  # Upload top 20 largest images first
    fname = os.path.basename(img_path)
    repo_fname = f'{REPO_PATH}/{fname}'
    
    with open(img_path, 'rb') as f:
        content = f.read()
    
    # Skip very small images (likely not fish photos)
    if len(content) < 10000:
        print(f"  ⏭️  {fname} ({len(content)} bytes) - too small")
        continue
    
    blob = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/blobs',
               {'content': base64.b64encode(content).decode(), 'encoding': 'base64'})
    if blob:
        entries.append({'path': repo_fname, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
        print(f"  📄 {fname} ({len(content)} bytes)")
    else:
        print(f"  ❌ {fname} failed")

if not entries:
    print("❌ No images uploaded")
    sys.exit(1)

# Create tree
tree = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/trees',
           {'base_tree': ref['object']['sha'], 'tree': entries})
if not tree:
    print("❌ Tree creation failed")
    sys.exit(1)

# Create commit
commit = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/commits', {
    'message': '📸 Add fish identification images from PDF guide',
    'tree': tree['sha'],
    'parents': [ref['object']['sha']]
})
if not commit:
    print("❌ Commit failed")
    sys.exit(1)

# Update ref
result = api('PATCH', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/main',
             {'sha': commit['sha'], 'force': True})
if result:
    print(f"\n🎉 Uploaded {len(entries)} images to https://github.com/{USERNAME}/{REPO_NAME}/tree/main/{REPO_PATH}")
    print(f"View images at: https://github.com/{USERNAME}/{REPO_NAME}/tree/main/{REPO_PATH}")
else:
    print("❌ Push failed")
