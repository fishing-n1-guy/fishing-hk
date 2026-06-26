#!/usr/bin/env python3
"""Use SearXNG with its default settings."""
import sys, os, shutil

# Use the original settings file directly
settings_src = '/opt/data/searxng/searx/settings.yml'
settings_dst = '/opt/data/searxng/settings.yml'
shutil.copy2(settings_src, settings_dst)

sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')
os.environ['GIT_DIR'] = '/opt/data/searxng/.git'
os.environ['SEARXNG_SETTINGS_PATH'] = settings_dst

# Ensure proper limiter
limiter_src = '/opt/data/searxng/searx/limiter.toml'
shutil.copy2(limiter_src, '/opt/data/searxng/limiter.toml')

from searx.webapp import app
import threading, urllib.request, json

def run():
    app.run(host='0.0.0.0', port=8889, debug=False)
threading.Thread(target=run, daemon=True).start()

import time; time.sleep(3)

# Test
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
    print(f"✅ {len(results)} results!")
    for r in results[:3]:
        img = r.get('img_src', '') or r.get('thumbnail_src', '')
        print(f"  {r.get('title','')[:40]}")
        print(f"  {img[:100]}")
    print(f"\nAPI URL: http://localhost:8889/search?q=QUERY&format=json&categories=images")
except Exception as e:
    print(f"Search error: {e}")
