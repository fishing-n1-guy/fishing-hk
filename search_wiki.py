#!/usr/bin/env python3
"""Search Wikipedia for Pokemon card images."""
import urllib.request, json, ssl

ctx = ssl.create_default_context()

# Search Wikipedia for Mario Pikachu
query = "Mario Pikachu Pokemon card"
url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.request.quote(query)}&format=json&srlimit=10"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
    data = json.loads(r.read())

pages = data.get('query', {}).get('search', [])
print(f"Wikipedia search: {len(pages)} results")
for p in pages[:5]:
    title = p.get('title', '')
    # Get page image
    img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.request.quote(title)}&prop=pageimages&format=json&pithumbsize=500"
    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(img_req, timeout=10, context=ctx) as r:
            img_data = json.loads(r.read())
        pages_data = img_data.get('query', {}).get('pages', {})
        for pid, pinfo in pages_data.items():
            thumb = pinfo.get('thumbnail', {}).get('source', '')
            print(f"\n  {title}")
            print(f"  Thumb: {thumb}")
            if thumb:
                # Download it
                dl = urllib.request.Request(thumb, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(dl, timeout=15, context=ctx) as f:
                    img = f.read()
                fname = f"/opt/data/fishing-hk/wiki_{title.replace(' ','_')[:20]}.jpg"
                with open(fname, 'wb') as f:
                    f.write(img)
                print(f"  ✅ Downloaded: {fname} ({len(img)} bytes)")
    except Exception as e:
        print(f"\n  {title}: Error - {e}")
