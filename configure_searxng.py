#!/usr/bin/env python3
"""Fix SearXNG config and try to start it."""
import sys, os, json
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')
os.environ['GIT_DISCOVERY_ACROSS_FILESYSTEM'] = '1'

# Minimal settings for SearXNG
settings = {
    "general": {"instance_name": "小婷 Search", "debug": False, "privacypolicy_url": False, "contact_url": False, "enable_metrics": False},
    "search": {"safe_search": 0, "autocomplete": "", "default_lang": "", "formats": ["html", "json"]},
    "server": {"secret_key": "xiaoting-secret-key-2026", "port": 8888, "bind_address": "0.0.0.0", "open_url": True},
    "engines": [
        {"name": "google images", "engine": "google_images", "shortcut": "gi", "disabled": False},
        {"name": "bing images", "engine": "bing_images", "shortcut": "bi", "disabled": False},
        {"name": "duckduckgo", "engine": "duckduckgo", "shortcut": "ddg", "disabled": False},
        {"name": "wikipedia", "engine": "wikipedia", "shortcut": "wp", "disabled": False},
    ],
    "outgoing": {"request_timeout": 10.0, "max_request_timeout": 15.0},
}

with open('/opt/data/searxng/settings.yml', 'w') as f:
    import yaml
    yaml.dump(settings, f, default_flow_style=False)

os.environ['SEARXNG_SETTINGS_PATH'] = '/opt/data/searxng/settings.yml'

# Try to import and list engines
try:
    from searx.engines import engines
    print(f"Engines loaded: {len(engines)}")
    for name, engine in engines.items():
        print(f"  {name}: {'✅' if not engine.disabled else '❌'}")
except Exception as e:
    print(f"Error loading engines: {e}")

# Try to start webapp  
try:
    from searx.webapp import app
    print(f"Webapp loaded! Routes: {len(list(app.url_map.iter_rules()))}")
except Exception as e:
    print(f"Webapp: {e}")
