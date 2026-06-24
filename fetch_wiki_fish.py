#!/usr/bin/env python3
"""Replace fish images with Wikipedia article images where available."""
import json, urllib.request, urllib.parse, time, os

# Read current HTML
with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# Extract the FISH array
# Find all fish entries by looking for the array
start = html.find('const FISH = [')
end = html.find('];', start) + 2
fish_section = html[start:end]

# Parse fish entries (simple approach)
fish_entries = []
for line in fish_section.split('\n'):
    line = line.strip()
    if line.startswith('//') or line.startswith('const') or line.startswith('];'):
        continue
    if line.startswith('['):
        try:
            entry = json.loads(line.rstrip(','))
            fish_entries.append(entry)
        except:
            pass

print(f"Found {len(fish_entries)} fish entries")

# For each fish, try to find Wikipedia image
def search_wiki_image(english_name):
    """Search Wikipedia for an English fish name and get image."""
    # Search for the English name
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(english_name + ' fish')}&format=json&origin=*&srlimit=3"
    try:
        req = urllib.request.Request(search_url, headers={"User-Agent": "fishing-hk-bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        
        results = data.get("query", {}).get("search", [])
        for result in results:
            title = result["title"]
            # Get page image
            img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&origin=*&pithumbsize=300"
            req2 = urllib.request.Request(img_url, headers={"User-Agent": "fishing-hk-bot/1.0"})
            with urllib.request.urlopen(req2, timeout=10) as r2:
                data2 = json.loads(r2.read())
            pages = data2.get("query", {}).get("pages", {})
            for pid, page in pages.items():
                if page.get("thumbnail"):
                    return page["thumbnail"]["source"]
    except:
        pass
    return None

# Build mapping: fish Chinese name → Wikipedia image URL
wiki_images = {}
for entry in fish_entries:
    cn = entry[0]
    en = entry[1]
    print(f"Searching {cn} ({en})...", end=" ")
    img = search_wiki_image(en)
    if img:
        wiki_images[cn] = img
        print(f"✅ Found")
    else:
        print(f"❌ Not found")
    time.sleep(0.5)

print(f"\n\nTotal: {len(wiki_images)}/{len(fish_entries)} with Wikipedia images")

# Generate JS object
print("\nconst FISH_IMG_WIKI = {")
for cn, img in sorted(wiki_images.items()):
    print(f'  "{cn}": "{img}",')
print("};")
