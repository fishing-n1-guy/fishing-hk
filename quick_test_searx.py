#!/usr/bin/env python3
"""Quick test SearXNG webapp."""
import sys, os
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')
os.environ['GIT_DIR'] = '/opt/data/searxng/.git'
os.environ['SEARXNG_SETTINGS_PATH'] = '/opt/data/searxng/settings.yml'

from searx.webapp import app
print(f"OK: {len(list(app.url_map.iter_rules()))} routes")
