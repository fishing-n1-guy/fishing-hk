#!/usr/bin/env python3
"""Search cards with broader queries."""
import json, urllib.request, urllib.parse

queries = [
    "name:Pikachu",
    "nationalPokedexNumbers:25",
]

for q in queries:
    url = f"https://api.pokemontcg.io/v2/cards?q={urllib.parse.quote(q)}&pageSize=5&page=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        cards = data.get('data', [])
        print(f"\n=== {q}: {data.get('totalCount',0)} total, showing {len(cards)} ===")
        for c in cards[:5]:
            n = c.get('name','')
            s = c.get('set',{}).get('name','')
            img = c.get('images',{}).get('large','')
            subtypes = c.get('subtypes', [])
            print(f"  {n} ({s}) [{','.join(subtypes)}]")
            if img: print(f"    {img}")
    except Exception as e:
        print(f"\n=== {q}: Error: {e}")
