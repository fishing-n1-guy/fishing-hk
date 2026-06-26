#!/usr/bin/env python3
"""Fix SearXNG to allow direct access without proxy."""
import sys, os, yaml

settings_path = '/opt/data/searxng/settings.yml'
with open(settings_path) as f:
    settings = yaml.safe_load(f)

# Add trusted proxy settings
if 'server' not in settings:
    settings['server'] = {}
settings['server']['secret_key'] = 'xiaoting-sk-2026'
settings['server']['port'] = 8889
settings['server']['bind_address'] = '0.0.0.0'
settings['server']['image_proxy'] = True
settings['server']['method'] = 'GET'

# Add outgoing settings with proper user agents  
settings['outgoing'] = {
    'request_timeout': 10.0,
    'max_request_timeout': 15.0,
    'max_redirects': 5,
    'useragent_suffix': '',
    'traefik': False,
    'source_ips': [],
}

# Disable botdetection limitation
settings['search'] = settings.get('search', {})
settings['search']['safe_search'] = 0

with open(settings_path, 'w') as f:
    yaml.dump(settings, f, default_flow_style=False)

print("Settings fixed!")

# Now test
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')
os.environ['GIT_DIR'] = '/opt/data/searxng/.git'
os.environ['SEARXNG_SETTINGS_PATH'] = settings_path
os.environ['SEARXNG_DEBUG'] = '0'

# Remove limiter entirely by renaming
limiter = '/opt/data/searxng/limiter.toml'
if os.path.exists(limiter):
    os.rename(limiter, limiter + '.bak')

from searx.webapp import app
import threading, urllib.request, json

def run():
    app.run(host='0.0.0.0', port=8889, debug=False)
threading.Thread(target=run, daemon=True).start()

import time; time.sleep(2)

url = 'http://localhost:8889/search?q=Pikachu+Captain&format=json&categories=images'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'X-Forwarded-For': '127.0.0.1',
    'X-Real-IP': '127.0.0.1',
})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    results = data.get('results', [])
    print(f"\n✅ {len(results)} results!")
    for r in results[:5]:
        img = r.get('img_src', '') or r.get('thumbnail_src', '')
        title = r.get('title', '')
        print(f"  {title[:40]}")
        if img: print(f"  {img[:100]}")
except Exception as e:
    print(f"Search error: {e}")
