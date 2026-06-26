#!/usr/bin/env python3
"""Find Captain Pikachu card - search all Pikachu cards and Japanese sets."""
import urllib.request, json, re

# Search for Pikachu cards with 'CAPTAIN' in the name
url = "https://api.pokemontcg.io/v2/cards?q=name:*Captain*&pageSize=250"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    cards = data.get('data', [])
    print(f"Cards with 'Captain': {data.get('totalCount',0)}")
    for c in cards:
        n = c.get('name','')
        s = c.get('set',{}).get('name','')
        img = c.get('images',{}).get('large','')
        print(f"  {n} ({s})")
        if img: print(f"    {img}")
except Exception as e:
    print(f"Error: {e}")

# Try with 'Pikachu' in name
print("\n=== Checking Pikachu cards for variants ===")
url2 = "https://api.pokemontcg.io/v2/cards?q=name:Pikachu&pageSize=250"
req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req2, timeout=15) as r:
        data = json.loads(r.read())
    for c in data.get('data', []):
        n = c.get('name','')
        if n != 'Pikachu' and n != 'Detective Pikachu':
            s = c.get('set',{}).get('name','')
            img = c.get('images',{}).get('large','')
            print(f"  {n} ({s})")
            if img: print(f"    {img}")
except Exception as e:
    print(f"Error: {e}")
