#!/usr/bin/env python3
"""Search images via Openverse and download one."""
import urllib.request, json, ssl, sys

query = sys.argv[1] if len(sys.argv) > 1 else "pikachu mario card"

ctx = ssl.create_default_context()
req = urllib.request.Request(
    f"https://api.openverse.org/v1/images/?q={urllib.parse.quote(query)}&page_size=5",
    headers={'User-Agent': 'Mozilla/5.0'}
)
with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
    data = json.loads(r.read())

results = data.get('results', [])
print(f"Found {len(results)} images")

for i, r in enumerate(results):
    title = r.get('title', 'untitled')
    thumb = r.get('thumbnail', '')
    url = r.get('url', '')
    print(f"\n{i+1}. {title}")
    print(f"   URL: {url[:100]}")
    print(f"   Thumb: {thumb[:100]}")
    
    if i == 0 and url:
        # Download the first image
        try:
            img_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(img_req, timeout=15) as img_r:
                img_data = img_r.read()
            ext = url.split('.')[-1].split('?')[0][:4]
            fname = f"/opt/data/fishing-hk/search_result.{ext}"
            with open(fname, 'wb') as f:
                f.write(img_data)
            print(f"   ✅ Downloaded: {fname} ({len(img_data)} bytes)")
        except Exception as e:
            print(f"   ❌ Download failed: {e}")
