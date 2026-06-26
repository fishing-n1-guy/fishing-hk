#!/usr/bin/env python3
"""Fix limiter config and try to run SearXNG."""
import sys, os
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')
os.environ['GIT_DIR'] = '/opt/data/searxng/.git'
os.environ['SEARXNG_SETTINGS_PATH'] = '/opt/data/searxng/settings.yml'

# Create proper limiter.toml
import toml
config = {
    "botdetection": {
        "ip_limit": 200,
        "ip_lists": {
            "pass_secret_key": False,
            "pass_ip": []
        }
    }
}
with open('/opt/data/searxng/limiter.toml', 'w') as f:
    toml.dump(config, f)

# Now try to run the webapp
from searx.webapp import app
print(f"Webapp loaded with {len(list(app.url_map.iter_rules()))} routes")

# Try starting it
import threading
def run():
    app.run(host='0.0.0.0', port=8889, debug=False)
    
t = threading.Thread(target=run, daemon=True)
t.start()
print("SearXNG running on http://localhost:8889")
print("Testing...")

import urllib.request, json
url = 'http://localhost:8889/search?q=Pikachu+Captain&format=json&categories=images&engines=google_images,bing_images'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    print(f"Results: {len(data.get('results', []))}")
    for r in data.get('results', [])[:3]:
        print(f"  {r.get('title','')[:40]}")
        print(f"  Img: {r.get('img_src','')[:80]}")
except Exception as e:
    print(f"Search error: {e}")
