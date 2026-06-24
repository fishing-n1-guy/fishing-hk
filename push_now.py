#!/usr/bin/env python3
"""Quick push via GitHub API."""
import sys, urllib.request, urllib.error, json, base64, os

DIR = os.path.dirname(os.path.abspath(__file__))
# Get token from git remote URL
import subprocess
r = subprocess.run(["git", "remote", "get-url", "origin"], cwd=DIR, capture_output=True, text=True, timeout=5)
url = r.stdout.strip()
# Extract token
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
        err = e.read().decode()[:300]
        print(f"  HTTP {e.code}")
        return None

# Get latest commit SHA
ref = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/git/ref/heads/main')
if not ref:
    print("❌ Branch not found")
    sys.exit(1)

FILES_TO_UPLOAD = ["index.html"]
entries = []
for fname in FILES_TO_UPLOAD:
    fpath = os.path.join(DIR, fname)
    with open(fpath, 'rb') as f:
        content = f.read()
    blob = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/blobs',
               {'content': base64.b64encode(content).decode(), 'encoding': 'base64'})
    if blob:
        entries.append({'path': fname, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
        print(f"  📄 {fname}")

tree = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/trees',
           {'base_tree': ref['object']['sha'], 'tree': entries})
commit = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/commits', {
    'message': '🌤️ 天氣大升級：天氣圖標、吹咩風、分區浪高、日出日落、濕度、UV、降雨機率',
    'tree': tree['sha'], 'parents': [ref['object']['sha']]
})
result = api('PATCH', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/main',
             {'sha': commit['sha'], 'force': True})
if result:
    print(f"\n🎉 Pushed! https://github.com/{USERNAME}/{REPO_NAME}/commit/{commit['sha'][:7]}")
