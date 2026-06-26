#!/usr/bin/env python3
"""Search Pokemon TCG API for specific Pikachu cards."""
import json, urllib.request, urllib.parse

# Try various search queries
queries = [
    "name:Pikachu set:sm*",
    "name:Pikachu set:xy*",
    "name:Pikachu set:swsh*",
    "name:PIKACHUUNION",
]

for q in queries:
    url = f"https://api.pokemontcg.io/v2/cards?q={urllib.parse.quote(q)}&pageSize=5"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        cards = data.get('data', [])
        print(f"\n=== {q}: {data.get('totalCount',0)} total ===")
        for c in cards[:3]:
            n = c.get('name','')
            s = c.get('set',{}).get('name','')
            sn = c.get('set',{}).get('series','')
            img = c.get('images',{}).get('large','')
            print(f"  {n} [{sn}:{s}]")
            if img: print(f"    {img}")
    except Exception as e:
        print(f"\n=== {q}: Error: {e}")
