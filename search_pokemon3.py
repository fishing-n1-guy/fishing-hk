#!/usr/bin/env python3
"""Search Pokemon TCG API for Pikachu cards with images."""
import json, urllib.request, urllib.parse

query = urllib.parse.quote("name:Pikachu")
url = f"https://api.pokemontcg.io/v2/cards?q={query}&pageSize=10"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    cards = data.get('data', [])
    print(f"Found {len(cards)} Pikachu cards")
    for c in cards:
        n = c.get('name','')
        s = c.get('set',{}).get('name','')
        img = c.get('images',{}).get('large','')
        if 'Mario' in n or 'mario' in n:
            print(f"\n>>> MATCH: {n} ({s})")
        print(f"  {n} ({s})")
        if img: print(f"  Image: {img}")
except Exception as e:
    print(f"Error: {e}")
