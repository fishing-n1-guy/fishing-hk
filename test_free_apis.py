#!/usr/bin/env python3
"""Test Pixabay API with different keys."""
import urllib.request, json, ssl

ctx = ssl.create_default_context()

# Pixabay demo/public keys to try
keys = [
    "48341419-6b7d9e9d1e0b8f5c5a9c7b3a1",
    "67536821-c999b81c2e5fc8d9e4f4d7a3a",
]

apis = {
    "Pixabay": lambda k: f"https://pixabay.com/api/?key={k}&q=pikachu&per_page=3",
    "Unsplash": lambda k: f"https://api.unsplash.com/search/photos?query=pikachu&per_page=3",
}

# Test Pixabay first
for key in keys:
    url = apis["Pixabay"](key)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            data = json.loads(r.read())
        total = data.get('totalHits', 0)
        hits = data.get('hits', [])
        if total > 0:
            print(f"Pixabay (key): {total} results")
            for h in hits[:2]:
                print(f"  {h.get('webformatURL','')[:80]}")
                print(f"  Tags: {h.get('tags','')[:50]}")
    except urllib.error.HTTPError as e:
        print(f"Pixabay (key): HTTP {e.code}")
    except Exception as e:
        print(f"Pixabay (key): {e}")

# Test Unsplash without key (might work for limited)
try:
    req = urllib.request.Request(
        "https://api.unsplash.com/search/photos?query=pikachu&per_page=3&client_id=public",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        data = json.loads(r.read())
    print(f"\nUnsplash: {len(data.get('results',[]))} results")
except Exception as e:
    print(f"\nUnsplash: {e}")

# Try Pexels free tier
try:
    req = urllib.request.Request(
        "https://api.pexels.com/v1/search?query=pikachu&per_page=3",
        headers={'Authorization': ''}
    )
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        data = json.loads(r.read())
    print(f"\nPexels: {len(data.get('photos',[]))} photos")
except Exception as e:
    print(f"\nPexels: {e}")
