#!/usr/bin/env python3
"""Search for Captain Pikachu card using multiple sources."""
import urllib.request, json, ssl

ctx = ssl.create_default_context()

# 1. Try Pokemon TCG API
queries = ["name:Pikachu*Captain", "name:Pikachu", "name:CAPTAINPIKACHU"]
for q in queries:
    url = f"https://api.pokemontcg.io/v2/cards?q={urllib.parse.quote(q)}&pageSize=5"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        cards = data.get('data', [])
        if cards:
            print(f"\n=== {q}: {data.get('totalCount',0)} total ===")
            for c in cards[:5]:
                n = c.get('name','')
                s = c.get('set',{}).get('name','')
                img = c.get('images',{}).get('large','')
                print(f"  {n} ({s}) - {img}")
    except Exception as e:
        print(f"{q}: Error")

# 2. Try Bulbapedia
print("\n=== Bulbapedia ===")
for page in ["Captain_Pikachu", "Pikachu_(Captain)"]:
    url = f"https://bulbapedia.bulbagarden.net/wiki/{page}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode()
        imgs = []
        for m in __import__('re').finditer(r'src="(https://archives\.bulbagarden\.net[^"]*(?:jpg|png))"', html):
            if 'icon' not in m.group(1) and 'logo' not in m.group(1) and 'sprite' not in m.group(1):
                imgs.append(m.group(1))
        print(f"  {page}: {len(imgs)} images")
        for img in imgs[:3]:
            print(f"    {img}")
    except Exception as e:
        print(f"  {page}: {e}")

# 3. Try Wikipedia
print("\n=== Wikipedia ===")
for term in ["Captain_Pikachu", "Pikachu"]:
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={term}&prop=pageimages&format=json&pithumbsize=500"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            data = json.loads(r.read())
        pages = data.get('query', {}).get('pages', {})
        for pid, info in pages.items():
            thumb = info.get('thumbnail', {}).get('source', '')
            if thumb:
                print(f"  {term}: {thumb}")
    except Exception as e:
        print(f"  {term}: {e}")
