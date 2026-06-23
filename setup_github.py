#!/usr/bin/env python3
"""Set up GitHub repo with fishing site and enable Pages.
Usage: python3 setup_github.py <username> <password> <email>
"""
import sys, urllib.request, urllib.error, json, base64

if len(sys.argv) < 3:
    print("Usage: setup_github.py <username> <password> <email>")
    sys.exit(1)

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
EMAIL = sys.argv[3] if len(sys.argv) > 3 else f"{USERNAME}@users.noreply.github.com"
REPO_NAME = "fishing-hk"

with open('/opt/data/fishing-hk/index.html') as f:
    html_content = f.read()

auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm=None, uri='https://api.github.com',
                          user=USERNAME, passwd=PASSWORD)
opener = urllib.request.build_opener(auth_handler)

def api(method, path, data=None):
    url = f'https://api.github.com{path}'
    headers = {'User-Agent': 'fishing-hk-bot/1.0', 'Accept': 'application/vnd.github.v3+json'}
    body = json.dumps(data).encode() if data else None
    if body: headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with opener.open(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:300]
        print(f"HTTP {e.code}: {err}")
        return None

print("📦 Creating repository...")
repo = api('POST', '/user/repos', {
    'name': REPO_NAME, 'description': '🐟 香港釣魚資訊站 - by 小婷',
    'private': False, 'auto_init': True
})
if not repo:
    repo = api('GET', f'/repos/{USERNAME}/{REPO_NAME}')
if not repo:
    print("❌ Failed to create repo"); sys.exit(1)

branch = repo.get('default_branch', 'main')
print(f"✅ Repo: {repo.get('html_url')} (branch: {branch})")

ref = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/git/ref/heads/{branch}')
if not ref: print("❌ No ref"); sys.exit(1)
sha = ref['object']['sha']

# Upload files
files_data = {
    'index.html': html_content,
    'README.md': f"# 🐟 香港釣魚資訊站\n\n由小婷為 Jay 製作 🎣\n\n🌐 https://{USERNAME}.github.io/{REPO_NAME}/\n\nPowered by Open-Meteo API\n每次開頁自動更新天氣"
}
entries = []
for fname, fcontent in files_data.items():
    encoded = base64.b64encode(fcontent.encode()).decode()
    blob = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/blobs',
               {'content': encoded, 'encoding': 'base64'})
    if blob:
        entries.append({'path': fname, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
        print(f"  ✅ {fname}")

new_tree = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/trees',
               {'base_tree': sha, 'tree': entries})
if not new_tree: print("❌ Tree failed"); sys.exit(1)

commit = api('POST', f'/repos/{USERNAME}/{REPO_NAME}/git/commits', {
    'message': '🎣 Initial fishing site by 小婷',
    'tree': new_tree['sha'], 'parents': [sha]
})
if not commit: print("❌ Commit failed"); sys.exit(1)

api('PATCH', f'/repos/{USERNAME}/{REPO_NAME}/git/refs/heads/{branch}',
    {'sha': commit['sha'], 'force': True})

# Enable Pages
pages = api('GET', f'/repos/{USERNAME}/{REPO_NAME}/pages')
if not pages:
    api('POST', f'/repos/{USERNAME}/{REPO_NAME}/pages',
        {'source': {'branch': branch, 'path': '/'}})

pages_url = f"https://{USERNAME}.github.io/{REPO_NAME}"
print(f"\n🎉 完成！")
print(f"🌐 {pages_url}")
print(f"📂 https://github.com/{USERNAME}/{REPO_NAME}")
