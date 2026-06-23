#!/usr/bin/env python3
"""Set up GitHub repo - reads token from .github_token file."""
import sys, urllib.request, urllib.error, json, base64, os

token_file = os.path.join(os.path.dirname(__file__), '.github_token')
with open(token_file) as f:
    TOKEN = f.read().strip()

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
        print(f"HTTP {e.code}")
        return None

user = api('GET', '/user')
if not user: print("❌ Auth failed"); sys.exit(1)
print(f"✅ Logged in as: {user.get('login')}")

repo = api('POST', '/user/repos', {
    'name': REPO_NAME, 'description': '🐟 香港釣魚資訊站 - by 小婷',
    'private': False, 'auto_init': True
})
if not repo: repo = api('GET', f'/repos/{USERNAME}/{REPO_NAME}')
if not repo: print("❌ Repo"); sys.exit(1)
print(f"✅ Repo: {repo.get('html_url')}")

branch = repo.get('default_branch', 'main')
ref = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/git/ref/heads/{branch}')
if not ref: sys.exit(1)

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
commit = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/commits', {
    'message': '🎣 Add fishing site by 小婷',
    'tree': tree['sha'], 'parents': [ref['object']['sha']]
}) if tree else None
if commit:
    api('PATCH', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/{branch}',
        {'sha': commit['sha'], 'force': True})
    print("✅ Files committed!")

pages = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/pages')
if not pages:
    api('POST', f'/repos/{USERNAME}/{REPO_NAME}/pages',
        {'source': {'branch': branch, 'path': '/'}})

print(f"\n🎉 大功告成！")
print(f"🌐 https://{USERNAME}.github.io/{REPO_NAME}")
print(f"📂 https://github.com/{USERNAME}/{REPO_NAME}")
