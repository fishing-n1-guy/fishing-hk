#!/usr/bin/env python3
"""Search Pokemon TCG API for Pikachu promos."""
import json, urllib.request

searches = [
    "name:Pikachu*",
    "name:PIKACHU",
]
for q in searches:
    url = f"https://api.pokemontcg.io/v2/cards?q={urllib.parse.quote(q)}&pageSize=5"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        cards = data.get('data', [])
        print(f"\n=== {q}: {len(cards)} cards ===")
        for c in cards[:5]:
            n = c.get('name','')
            s = c.get('set',{}).get('name','')
            img = c.get('images',{}).get('large','')
            print(f"  {n} ({s})")
            if img: print(f"    {img}")
    except Exception as e:
        print(f"  Error: {e}")
