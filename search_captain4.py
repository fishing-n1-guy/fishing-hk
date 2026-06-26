#!/usr/bin/env python3
"""Find Captain Pikachu card via multiple APIs."""
import urllib.request, json, re, ssl, time

ctx = ssl.create_default_context()

# Try the official Pokemon TCG API for all cards named Pikachu
# Check the first 200 Pikachu cards for any Captain variant
url = "https://api.pokemontcg.io/v2/cards?q=name:Pikachu&pageSize=250"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    cards = data.get('data', [])
    print(f"Total Pikachu cards: {data.get('totalCount',0)}")
    found = False
    for c in cards:
        n = c.get('name','')
        s = c.get('set',{}).get('name','')
        series = c.get('set',{}).get('series','')
        if any(k in n.lower() for k in ['captain', '船長', 'capt', 'sailor', 'pirate']):
            print(f">>> {n} ({s} - {series})")
            img = c.get('images',{}).get('large','')
            print(f"    {img}")
            found = True
    if not found:
        print("No Captain Pikachu found in international TCG API")
except Exception as e:
    print(f"TCG API Error: {e}")

# Try Japanese sets
print("\n=== Japanese cards ===")
url2 = "https://api.pokemontcg.io/v2/cards?q=set.ptcgoCode:SMP&pageSize=250"
try:
    with urllib.request.urlopen(url2, timeout=15) as r:
        data = json.loads(r.read())
    for c in data.get('data', []):
        n = c.get('name','')
        if 'CAPTAIN' in n.upper() or 'CAP' in n.upper():
            print(f"  {n}")
            print(f"  {c.get('images',{}).get('large','')}")
except Exception as e:
    print(f"  Error: {e}")

# Try Openverse for 船長皮卡丘
print("\n=== Openverse ===")
time.sleep(2)
url3 = f"https://api.openverse.org/v1/images/?q={urllib.parse.quote('船長皮卡丘 TCG card')}&page_size=5"
req3 = urllib.request.Request(url3, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req3, timeout=15, context=ctx) as r:
        data = json.loads(r.read())
    for r in data.get('results', [])[:5]:
        title = r.get('title','')
        url = r.get('url','')
        print(f"  {title} - {url[:100]}")
except Exception as e:
    print(f"  Error: {e}")
