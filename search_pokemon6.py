#!/usr/bin/env python3
"""Search for Mario/ninja/crossover Pikachu cards."""
import json, urllib.request, urllib.parse

# Mario crossover specific search
url = "https://api.pokemontcg.io/v2/cards?q=name:Mario*&pageSize=20"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    cards = data.get('data', [])
    print(f"Mario cards: {data.get('totalCount',0)} total")
    for c in cards:
        print(f"  {c.get('name','')} ({c.get('set',{}).get('name','')})")
        print(f"    {c.get('images',{}).get('large','')}")
except Exception as e:
    print(f"Error: {e}")

print("\n---")

# Also try searching by name containing Pikachu for all pages
# Try a few pages
for page in [1, 2, 3, 4]:
    url = f"https://api.pokemontcg.io/v2/cards?q=name:Pikachu&page={page}&pageSize=250"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        for c in data.get('data', []):
            n = c.get('name','')
            if any(k in n.lower() for k in ['mario','ninja','crossover','costume','cosplay','dress','disguise']):
                print(f"\n>>> MATCH: {n} ({c.get('set',{}).get('name','')})")
                print(f"  {c.get('images',{}).get('large','')}")
                print(f"  Subtypes: {c.get('subtypes',[])}")
    except Exception as e:
        print(f"Page {page}: Error: {e}")
