#!/usr/bin/env python3
"""Try SearXNG MCP client with different public instances."""
import sys, os, json, urllib.request

sys.path.insert(0, '/opt/data/stt-packages')

# Try different public SearXNG instances
instances = [
    "https://searx.be",
    "https://search.sapti.me",
    "https://searx.work",
    "https://searx.rhscz.eu",
    "https://priv.au",
]

for instance in instances:
    q = "Pikachu Captain card"
    url = f"{instance}/search?q={q.replace(' ', '%20')}&format=json&categories=images"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/json'
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        results = data.get('results', [])
        print(f"\n{instance}: {len(results)} results")
        for r in results[:3]:
            print(f"  {r.get('title','')[:40]}")
            print(f"  {r.get('img_src','')[:80]}")
            print(f"  {r.get('url','')[:80]}")
    except urllib.error.HTTPError as e:
        print(f"{instance}: HTTP {e.code}")
    except Exception as e:
        print(f"{instance}: {e}")
