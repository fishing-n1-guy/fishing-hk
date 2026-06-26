#!/usr/bin/env python3
"""Tune SearXNG and keep it running."""
import sys, os, re

# Tune outgoing settings for better compatibility  
dst = '/opt/data/searxng/settings.yml'
with open(dst) as f:
    content = f.read()

# Add better outgoing config
outgoing_config = """
outgoing:
  request_timeout: 15.0
  max_request_timeout: 30.0
  max_redirects: 5
  useragent_suffix: ""
  # Use a common browser UA
  useragent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
  # Add delays to avoid rate limiting
  # soft_max_timeout: 10.0
  # hard_max_timeout: 30.0
  
search:
  safe_search: 0
  autocomplete: ""
  default_lang: "zh-HK"
  formats: ["html", "json", "csv"]
  languages:
    - "all"
    - "zh-HK"
    - "zh-CN"
    - "en"
    - "ja"
  
server:
  secret_key: "xiaoting-sk-2026-searxng"
  port: 8889
  bind_address: "0.0.0.0"
  image_proxy: true
  method: "GET"
  # Allow all origins
  cors_headers:
    - "*"
"""

# Replace the outgoing section
content = re.sub(r'^outgoing:.*?(?=^[a-z])', outgoing_config.strip() + '\n', content, flags=re.MULTILINE|re.DOTALL)

# Also add search section before server
content = re.sub(r'^search:\n  safe_search: 0.*?(?=^  [a-z])', 'search:\n  safe_search: 0\n  autocomplete: ""\n  default_lang: "zh-HK"\n  formats: ["html", "json"]\n  languages: ["all", "zh-HK", "zh-CN", "en"]\n', content, flags=re.MULTILINE|re.DOTALL)

with open(dst, 'w') as f:
    f.write(content)

# Create a startup script
startup = """#!/bin/bash
cd /opt/data/searxng
export PYTHONPATH=/opt/data/stt-packages:/opt/data/searxng
export GIT_DIR=/opt/data/searxng/.git
export SEARXNG_SETTINGS_PATH=/opt/data/searxng/settings.yml
exec python3 -c "
import sys; sys.path.insert(0, '/opt/data/stt-packages'); sys.path.insert(0, '/opt/data/searxng')
from searx.webapp import app
app.run(host='0.0.0.0', port=8889, debug=False, use_reloader=False)
"
"""
with open('/opt/data/fishing-hk/run_searxng.sh', 'w') as f:
    f.write(startup)
os.chmod('/opt/data/fishing-hk/run_searxng.sh', 0o755)

print("✅ SearXNG configured!")
print("   Config: /opt/data/searxng/settings.yml")
print("   Port: 8889")
print("   To start: /opt/data/fishing-hk/run_searxng.sh")
