#!/usr/bin/env python3
"""Test SearXNG can search for images."""
import sys, os
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')

os.environ['SEARXNG_SETTINGS_PATH'] = '/opt/data/searxng/searx/settings.yml'

try:
    from searx.search import SearchWithPlugins
    from searx.engines import get_engine, get_engine_list
    from searx.preferences import Preferences
    
    print("SearXNG imports OK!")
    
    # List available engines
    engines = get_engine_list()
    print(f"Available engines: {len(engines)}")
    for e in engines[:10]:
        print(f"  - {e.name} ({e.shortcut})")
    
except Exception as e:
    print(f"Error: {e}")
    
# Also try just importing the webapp
try:
    from searx import webapp
    print("Webapp import OK!")
except Exception as e:
    print(f"Webapp: {e}")
