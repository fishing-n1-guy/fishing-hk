#!/usr/bin/env python3
"""Find clean Captain Pikachu TCG card image from Bulbapedia."""
import urllib.request, json, re, ssl

ctx = ssl.create_default_context()

# Search for the Captain Pikachu TCG card on Bulbapedia
# It might have a different page name
searches = [
    "Captain_Pikachu_(TCG)",
    "Pikachu_(Captain_Pikachu)",
    "Pikachu_(Captain)",
    "Captain_Pikachu",
]

for page in searches:
    url = f"https://bulbapedia.bulbagarden.net/wiki/{page}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode()
        
        # Find TCG card images (usually PNG with card framing)
        imgs = []
        for m in re.finditer(r'src="(https://archives\.bulbagarden\.net/media/upload[^"]*\.(?:png|jpg))"', html):
            u = m.group(1)
            # Skip non-card images
            if any(k in u for k in ['20px', '24px', '25px', 'icon', 'logo', 'Bag_', 'HOME', 'sprite']):
                continue
            # TCG card images usually have larger dimensions in the URL
            if 'px-' in u or 'px/' in u:
                imgs.append(u)
        
        print(f"\n{page}: {len(imgs)} candidate images")
        for img in imgs[:5]:
            print(f"  {img}")
            # Download the first good card image
            if imgs.index(img) < 3 and 'TCG' in img or 'card' in img.lower():
                fname = f"/opt/data/fishing-hk/captain_clean_{imgs.index(img)}.jpg"
                dl = urllib.request.Request(img, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(dl, timeout=15) as f:
                    with open(fname, 'wb') as f2:
                        f2.write(f.read())
                print(f"    ✅ Saved!")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"{page}: Not found")
        else:
            print(f"{page}: Error {e.code}")
    except Exception as e:
        print(f"{page}: {e}")
