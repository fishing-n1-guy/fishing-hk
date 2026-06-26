#!/usr/bin/env python3
"""Search for Captain Pikachu card images from Bulbapedia."""
import urllib.request, json, ssl, re

ctx = ssl.create_default_context()

# Get the Bulbapedia Captain Pikachu page
url = "https://bulbapedia.bulbagarden.net/wiki/Captain_Pikachu"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode()
    
    # Find all TCG card images
    imgs = []
    for m in re.finditer(r'src="(https://archives\.bulbagarden\.net/media/upload[^"]*(?:jpg|png))"', html):
        url = m.group(1)
        # Skip icons and small sprites
        if any(k in url for k in ['icon', 'logo', 'sprite', 'Bag_', 'HOME', '20px', '24px']):
            continue
        imgs.append(url)
    
    print(f"Found {len(imgs)} card images")
    for img in imgs[:10]:
        print(f"  {img}")
        # Download the first few to check
        if imgs.index(img) < 3:
            fname = f"/opt/data/fishing-hk/captain_pika_{imgs.index(img)}.jpg"
            dl = urllib.request.Request(img, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(dl, timeout=15) as f:
                data = f.read()
            with open(fname, 'wb') as f:
                f.write(data)
            print(f"    ✅ Downloaded ({len(data)} bytes)")
    
    # Also check "船長皮卡丘" specific page
    print("\n=== 船長皮卡丘 ===")
    url2 = "https://wiki.52poke.com/wiki/%E8%88%B9%E9%95%BF%E7%9A%AE%E5%8D%A1%E4%B8%98"
    req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req2, timeout=15) as r:
            html2 = r.read().decode('utf-8', errors='replace')
        for m in re.finditer(r'src="(https?://[^"]*\.(?:jpg|png))"', html2):
            url = m.group(1)
            if any(k in url for k in ['pikachu', 'captain', '船長', '皮卡']):
                print(f"  {url}")
    except Exception as e:
        print(f"  Error: {e}")
        
except Exception as e:
    print(f"Error: {e}")
