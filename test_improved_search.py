#!/usr/bin/env python3
"""Test improved search with Pixabay + other APIs."""
import urllib.request, json, ssl, sys, os

ctx = ssl.create_default_context()
key = "56441428-36c1a798c00ef130b61ebd03e"

searches = [
    ("Pikachu Captain Pokemon card", "pikachu+captain+pokemon"),
    ("三牙魚 紅牙䱛", "三牙魚"),
    ("香港釣魚", "hong+kong+fishing"),
]

for search_name, search_q in searches:
    print(f"\n=== {search_name} ===")
    url = f"https://pixabay.com/api/?key={key}&q={search_q}&per_page=3&image_type=photo&safesearch=true"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            data = json.loads(r.read())
        hits = data.get('hits', [])
        print(f"  Pixabay: {data.get('totalHits',0)} results")
        for h in hits[:2]:
            img = h.get('webformatURL', '')
            tags = h.get('tags', '')[:40]
            page = h.get('pageURL', '')[:60]
            print(f"  🏷️ {tags}")
            print(f"  🖼️ {img[:80]}")
            # Download first image
            if hits.index(h) == 0 and img:
                fname = f"/opt/data/fishing-hk/search_{search_q.replace('+','_')[:20]}.jpg"
                dl = urllib.request.Request(img, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://pixabay.com/'})
                with urllib.request.urlopen(dl, timeout=15, context=ctx) as r:
                    with open(fname, 'wb') as f:
                        f.write(r.read())
                print(f"  ✅ Downloaded: {fname}")
    except Exception as e:
        print(f"  Error: {e}")
