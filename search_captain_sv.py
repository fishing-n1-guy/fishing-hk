#!/usr/bin/env python3
"""Try to find the card via Japanese or Simplified Chinese sets."""
import urllib.request, json, re

# Try searching for the card in Japanese sets
# Captain Pikachu is from the anime, and might be in the "SV" sets
# Try different search patterns
searches = [
    "name:Pikachu set.id:sv*",
    "name:Pikachu set.ptcgoCode:SVI",
]

for q in searches:
    url = f"https://api.pokemontcg.io/v2/cards?q={q.replace(' ', '%20')}&pageSize=50"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        cards = data.get('data', [])
        print(f"\n{q}: {data.get('totalCount',0)} cards")
        for c in cards[:5]:
            n = c.get('name','')
            s = c.get('set',{}).get('name','')
            sn = c.get('set',{}).get('series','')
            img = c.get('images',{}).get('large','')
            print(f"  {n} [{sn}:{s}]")
            if img: print(f"    {img}")
    except Exception as e:
        print(f"{q}: {e}")
