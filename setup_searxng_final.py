#!/usr/bin/env python3
"""Create proper SearXNG config and test it."""
import sys, os, json, yaml
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')

# Create proper settings
settings = {
    "general": {"instance_name": "小婷 Search", "debug": False, "privacypolicy_url": False, "contact_url": False, "enable_metrics": False},
    "search": {"safe_search": 0, "autocomplete": "", "default_lang": "", "formats": ["html", "json"]},
    "server": {"secret_key": "xiaoting-sk-2026", "port": 8889, "bind_address": "0.0.0.0", "open_url": True, "image_proxy": True},
    "engines": [
        {"name": "google images", "engine": "google_images", "shortcut": "gi", "disabled": False},
        {"name": "bing images", "engine": "bing_images", "shortcut": "bi", "disabled": False},
        {"name": "duckduckgo", "engine": "duckduckgo", "shortcut": "ddg", "disabled": False},
        {"name": "google", "engine": "google", "shortcut": "g", "disabled": False},
        {"name": "sogou images", "engine": "sogou_images", "shortcut": "sgi", "disabled": False},
    ],
    "outgoing": {"request_timeout": 10.0, "max_request_timeout": 15.0},
}

with open('/opt/data/searxng/settings.yml', 'w') as f:
    yaml.dump(settings, f, default_flow_style=False)

os.environ['SEARXNG_SETTINGS_PATH'] = '/opt/data/searxng/settings.yml'

# Import engines
try:
    from searx.engines import engines as searx_engines
    import searx.search
    print(f"✅ Engines loaded: {len(searx_engines)}")
    for name, e in searx_engines.items():
        print(f"  {name}: {'✅' if not e.disabled else '❌ disabled'}")
except Exception as e:
    print(f"❌ Engine load error: {e}")

# Test search capability
print("\n🔍 Testing search...")
try:
    from searx.search import SearchWithPlugins
    from searx.preferences import Preferences
    
    prefs = Preferences(["json"], searx_engines)
    search = SearchWithPlugins("Pikachu Captian", prefs, searx_engines, ["google images", "bing images"])
    results = search.search()
    for r in results[:5]:
        print(f"  {r.get('title','')[:50]}")
except Exception as e:
    print(f"  Search error: {e}")
    
print("\n✅ SearXNG config ready at port 8889!")
