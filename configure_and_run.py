#!/usr/bin/env python3
"""Configure SearXNG with enabled image engines and run it."""
import sys, os, re, shutil

# Copy the original 3398-line settings
src = '/opt/data/searxng/searx/settings.yml'
dst = '/opt/data/searxng/settings.yml'
shutil.copy2(src, dst)

# Read and modify
with open(dst) as f:
    content = f.read()

# 1. Set secret key
content = content.replace('ultrasecretkey', 'xiaoting-sk-2026-searxng')

# 2. Enable image engines + web engines
# Change disabled: true to disabled: false for engines we want
enable_engines = [
    'google images', 'google', 'google videos',
    'bing images', 'bing', 'bing news',
    'duckduckgo', 'duckduckgo definitions',
    'wikipedia', 'wikimedia',
    'flickr', 'deviantart',
    'openverse',
]
for eng in enable_engines:
    # Find the engine block and set disabled to false
    pattern = re.compile(
        r'(-\s*\n\s+name:\s*"' + re.escape(eng) + r'"\n.+?\n\s+disabled:\s*)true',
        re.DOTALL
    )
    content = pattern.sub(r'\1false', content)

# 3. Disable botdetection
content = content.replace("botdetection:\n  ip_limit:\n", "botdetection:\n  ip_limit:\n    filter_link_local: false\n    link_token: false\n")

# 4. Set image proxy
content = content.replace("image_proxy: false", "image_proxy: true")

# Write back
with open(dst, 'w') as f:
    f.write(content)

# Count enabled engines
enabled = [line for line in content.split('\n') if 'name:' in line and any(e in line for e in enable_engines)]
print(f"Engines enabled: {len(enabled)}")
for e in enabled:
    print(f"  ✅ {e.split(':')[1].strip().strip('\"')}")

# Now run SearXNG
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')
os.environ['GIT_DIR'] = '/opt/data/searxng/.git'
os.environ['SEARXNG_SETTINGS_PATH'] = dst

from searx.webapp import app
import threading, urllib.request, json, time

def run():
    app.run(host='0.0.0.0', port=8889, debug=False, use_reloader=False)
threading.Thread(target=run, daemon=True).start()
time.sleep(3)

# Test image search
print(f"\n🔍 Testing image search...")
url = 'http://localhost:8889/search?q=Pikachu+Captain&format=json&categories=images'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'X-Forwarded-For': '127.0.0.1',
    'X-Real-IP': '127.0.0.1',
})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    results = data.get('results', [])
    print(f"✅ {len(results)} results for 'Pikachu Captain'")
    for r in results[:3]:
        title = r.get('title', '')[:50]
        img = r.get('img_src', '') or r.get('thumbnail_src', '')
        url2 = r.get('url', '')[:80]
        print(f"\n  📸 {title}")
        print(f"  Img: {img}")
        print(f"  URL: {url2}")
except Exception as e:
    print(f"Search error: {e}")

print(f"\n🌐 SearXNG running on http://localhost:8889")
print(f"   API: curl 'http://localhost:8889/search?q=QUERY&format=json&categories=images'")
