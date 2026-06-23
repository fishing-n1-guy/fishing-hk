#!/usr/bin/env python3
"""Push updated tide files to GitHub via API."""
import sys, urllib.request, urllib.error, json, base64, os

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, '.github_token')) as f:
    TOKEN = f.read().strip()

USERNAME = "fishing-n1-guy"
REPO_NAME = "fishing-hk"

FILES_TO_UPLOAD = [
    "index.html",
    "tide_data.json",
    "fetch_tide.py",
    "cron_update_tide.py",
]

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
        err = e.read().decode()[:500]
        print(f"  HTTP {e.code}: {err}")
        return None

# Auth
user = api('GET', '/user')
if not user:
    print("❌ Auth failed - check token")
    sys.exit(1)
print(f"✅ Logged in as: {user.get('login')}")

# Get repo and latest commit SHA
repo = api('GET', f'/repos/{USERNAME}/{REPO_NAME}')
if not repo:
    print("❌ Repo not found")
    sys.exit(1)
print(f"✅ Repo: {repo.get('html_url')}")

branch = repo.get('default_branch', 'main')
ref = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/git/ref/heads/{branch}')
if not ref:
    print(f"❌ Branch '{branch}' not found")
    sys.exit(1)

# Create blobs for each file
entries = []
for fname in FILES_TO_UPLOAD:
    fpath = os.path.join(DIR, fname)
    if not os.path.exists(fpath):
        print(f"  ⚠️  {fname} not found, skipping")
        continue
    with open(fpath, 'rb') as f:
        content = f.read()
    
    blob = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/blobs',
               {'content': base64.b64encode(content).decode(), 'encoding': 'base64'})
    if blob:
        entries.append({'path': fname, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
        print(f"  📄 {fname} ({len(content)} bytes)")
    else:
        print(f"  ❌ {fname} failed")

if not entries:
    print("❌ No files to commit")
    sys.exit(1)

# Create tree
tree = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/trees',
           {'base_tree': ref['object']['sha'], 'tree': entries})
if not tree:
    print("❌ Tree creation failed")
    sys.exit(1)

# Create commit
commit = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/commits', {
    'message': '🌊 加潮汐漲退流水功能 - 小婷',
    'tree': tree['sha'],
    'parents': [ref['object']['sha']]
})
if not commit:
    print("❌ Commit failed")
    sys.exit(1)

# Update ref
result = api('PATCH', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/{branch}',
             {'sha': commit['sha'], 'force': True})
if result:
    print(f"\n🎉 成功推送潮汐更新！")
    print(f"🌐 https://{USERNAME}.github.io/{REPO_NAME}")
    print(f"📂 https://github.com/{USERNAME}/{REPO_NAME}/commit/{commit['sha'][:7]}")
else:
    print("❌ Push failed")
    sys.exit(1)
