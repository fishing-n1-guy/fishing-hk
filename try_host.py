#!/usr/bin/env python3
"""Try to host the fishing site on a free service."""
import urllib.request, urllib.error, json, os

# Read the HTML
with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# Try several free hosting services
services = [
    # Bunny CDN free hosting
    {
        'name': 'pastes.io',
        'url': 'https://pastes.io/api/create',
        'data': {'content': html, 'language': 'html', 'expire': '0'},
        'parse': lambda r: r.get('url', '')
    },
]

# Read HTML content and search for a service
print(f"HTML size: {len(html)} bytes")

# Try pastes.io
try:
    data = json.dumps({'content': html, 'language': 'html', 'expire': '0'}).encode()
    req = urllib.request.Request('https://pastes.io/api/create', data=data, 
                                  headers={'Content-Type': 'application/json'},
                                  method='POST')
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read())
    print(f"pastes.io: {result}")
except Exception as e:
    print(f"pastes.io failed: {e}")

# Try another approach - use a free file hosting
print("\nTrying alternative approaches...")

# Check if we can use transfer.sh
try:
    req = urllib.request.Request('https://transfer.sh/fishing.html', 
                                  data=html.encode(), 
                                  headers={'Content-Type': 'text/html'},
                                  method='PUT')
    resp = urllib.request.urlopen(req, timeout=15)
    url = resp.read().decode().strip()
    print(f"transfer.sh: {url}")
except Exception as e:
    print(f"transfer.sh failed: {e}")
