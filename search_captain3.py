#!/usr/bin/env python3
"""Search for Simplified Chinese Captain Pikachu TCG card."""
import urllib.request, json, re, ssl

ctx = ssl.create_default_context()

# Try 52poke wiki for the card
url = "https://wiki.52poke.com/zh-hans/%E8%88%B9%E9%95%BF%E7%9A%AE%E5%8D%A1%E4%B8%98"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml'
})
try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        html = r.read().decode('utf-8', errors='replace')
    
    # Find card images
    imgs = []
    for m in re.finditer(r'(https?://media\.52poke\.com[^"\']*\.(?:jpg|png))', html):
        if any(k in m.group(1).lower() for k in ['pikachu', '皮卡', 'cap']):
            imgs.append(m.group(1))
    
    print(f"52poke: {len(imgs)} images")
    for img in imgs[:5]:
        print(f"  {img}")
        
except Exception as e:
    print(f"52poke: Error: {e}")

# Try searching via Pokemon TCG API for Chinese cards
print("\n=== Pokemon TCG API Chinese sets ===")
url2 = "https://api.pokemontcg.io/v2/sets?q=series:Scarlet*Violet"
req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req2, timeout=10) as r:
        data = json.loads(r.read())
    for s in data.get('data', []):
        name = s.get('name', '')
        series = s.get('series', '')
        if 'Chinese' in name or 'SC' in name or 'Simplified' in name:
            print(f"  {name} ({series})")
except Exception as e:
    print(f"  Error: {e}")
