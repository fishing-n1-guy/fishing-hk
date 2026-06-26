#!/usr/bin/env python3
"""Start SearXNG webapp."""
import sys, os
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')
os.environ['GIT_DIR'] = '/opt/data/searxng/.git'
os.environ['SEARXNG_SETTINGS_PATH'] = '/opt/data/searxng/settings.yml'

# Remove bad limiter config
limiter_path = '/opt/data/searxng/limiter.toml'
if os.path.exists(limiter_path):
    os.remove(limiter_path)
# Copy the proper one
import shutil
shutil.copy('/opt/data/searxng/searx/limiter.toml', limiter_path)

from searx.webapp import app
print(f"OK: {len(list(app.url_map.iter_rules()))} routes")

# Start the server
import threading, urllib.request, json
def run():
    app.run(host='0.0.0.0', port=8889, debug=False)
threading.Thread(target=run, daemon=True).start()

# Test it
import time
time.sleep(2)
url = 'http://localhost:8889/search?q=Pikachu+Captain&format=json&categories=images'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    results = data.get('results', [])
    print(f"Search results: {len(results)}")
    for r in results[:3]:
        img = r.get('img_src', '') or r.get('thumbnail_src', '')
        print(f"  {r.get('title','')[:30]}")
        if img: print(f"  {img[:80]}")
except Exception as e:
    print(f"Search error: {e}")
