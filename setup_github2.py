#!/usr/bin/env python3
"""Set up GitHub repo using Personal Access Token."""
import sys, urllib.request, urllib.error, json, base64

TOKEN = sys.argv[1]
USERNAME = "fishing-n1-guy"
REPO_NAME = "fishing-hk"

with open('/opt/data/fishing-hk/index.html') as f:
    html_content = f.read()

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
        print(f"HTTP {e.code}: {err}")
        return None

# Test token
print("🔑 Testing token...")
user = api('GET', '/user')
if not user:
    print("❌ Token invalid!"); sys.exit(1)
print(f"✅ Logged in as: {user.get('login')}")

# Create repo
print("\n📦 Creating repository...")
repo = api('POST', '/user/repos', {
    'name': REPO_NAME, 'description': '🐟 香港釣魚資訊站 - by 小婷',
    'private': False, 'auto_init': True
})
if not repo:
    repo = api('GET', f'/repos/{USERNAME}/{REPO_NAME}')
if not repo:
    print("❌ Failed"); sys.exit(1)
print(f"✅ Repo: {repo.get('html_url')}")

branch = repo.get('default_branch', 'main')

# Get ref
ref = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/git/ref/heads/{branch}')
if not ref: print("❌ No ref"); sys.exit(1)

# Upload files
files = {
    'index.html': html_content,
    'README.md': f"# 🐟 香港釣魚資訊站\n\n由小婷為 Jay 製作 🎣\n\n🌐 https://{USERNAME}.github.io/{REPO_NAME}/\n\nPowered by Open-Meteo API"
}
entries = []
for name, content in files.items():
    blob = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/blobs',
               {'content': base64.b64encode(content.encode()).decode(), 'encoding': 'base64'})
    if blob:
        entries.append({'path': name, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
        print(f"  📄 {name}")

tree = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/trees',
           {'base_tree': ref['object']['sha'], 'tree': entries})
if not tree: print("❌ Tree"); sys.exit(1)

commit = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/commits', {
    'message': '🎣 Add fishing site by \u5c0f\u5a37',
    'tree': tree['sha'], 'parents': [ref['object']['sha']]
})
if not commit: print("❌ Commit"); sys.exit(1)

api('PATCH', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/{branch}',
    {'sha': commit['sha'], 'force': True})
print("✅ Files committed!")

# Enable Pages
pages = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/pages')
if not pages:
    pages = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/pages',
                {'source': {'branch': branch, 'path': '/'}})
    if pages:
        print(f"✅ Pages enabled!")

pages_url = f"https://{USERNAME}.github.io/{REPO_NAME}"
print(f"\n🎉 大功告成！")
print(f"🌐 {pages_url}")
print(f"📂 https://github.com/{USERNAME}/{REPO_NAME}")
