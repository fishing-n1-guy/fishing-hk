#!/usr/bin/env python3
"""Search Pokemon TCG API for Mario Pikachu card."""
import json, urllib.request

url = "https://api.pokemontcg.io/v2/cards?q=name:Mario*Pikachu"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    cards = data.get('data', [])
    print(f"Found {len(cards)} cards")
    for c in cards[:5]:
        name = c.get('name', '')
        set_name = c.get('set', {}).get('name', '')
        img = c.get('images', {}).get('large', '')
        print(f"\n{name} ({set_name})")
        print(f"Image: {img}")
except Exception as e:
    print(f"Error: {e}")
