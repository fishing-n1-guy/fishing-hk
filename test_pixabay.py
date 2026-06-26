#!/usr/bin/env python3
"""Test Pixabay API and search for something."""
import urllib.request, json, ssl

ctx = ssl.create_default_context()
key = "56441428-36c1a798c00ef130b61ebd03e"

# Test search
url = f"https://pixabay.com/api/?key={key}&q=pikachu&per_page=3&image_type=photo"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
    data = json.loads(r.read())

total = data.get('totalHits', 0)
hits = data.get('hits', [])
print(f"Pixabay: {total} results for 'pikachu'")
for h in hits[:3]:
    img_url = h.get('webformatURL', '')
    print(f"  {h.get('tags','')[:40]}")
    print(f"  {img_url[:80]}")
    # Download first image
    urllib.request.urlopen(urllib.request.Request(img_url)).read()
    ext = img_url.split('.')[-1].split('?')[0]
    fname = f"/opt/data/fishing-hk/pixabay_test.{ext}"
    with open(fname, 'wb') as f:
        f.write(urllib.request.urlopen(urllib.request.Request(img_url)).read())
    print(f"  ✅ Downloaded to {fname}")
    break

# Also search for HK fishing
print(f"\n=== 香港釣魚 ===")
url2 = f"https://pixabay.com/api/?key={key}&q=fishing+harbour+hk&per_page=3&image_type=photo"
with urllib.request.urlopen(urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'}), timeout=15, context=ctx) as r:
    data2 = json.loads(r.read())
print(f"Fishing: {data2.get('totalHits',0)} results")
for h in data2.get('hits', [])[:2]:
    print(f"  {h.get('tags','')[:40]} - {h.get('webformatURL','')[:80]}")
