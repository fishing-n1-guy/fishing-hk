#!/usr/bin/env python3
"""Use text search to find Mario Pikachu card page, then extract image."""
import urllib.request, json, ssl, re

# Use DuckDuckGo lite to search for the card
query = "Mario+Pikachu+Pokemon+card"
url = f"https://lite.duckduckgo.com/lite/?q={query}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode()
    # Extract links
    links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>', html)
    print(f"Found {len(links)} links")
    for href, text in links[:10]:
        if any(k in href.lower() for k in ['pokemon','pikachu','mario','card','tcg','bulbapedia']):
            print(f"  {text.strip()[:50]}")
            print(f"  {href[:100]}")
except Exception as e:
    print(f"DuckDuckGo: {e}")

# Try Bing web search directly via URL
print("\n--- Bing ---")
url2 = f"https://www.bing.com/search?q=Mario+Pikachu+Pokemon+card+image"
req2 = urllib.request.Request(url2, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml'
})
try:
    with urllib.request.urlopen(req2, timeout=15) as r:
        html2 = r.read().decode('utf-8', errors='replace')
    # Find image URLs
    imgs = re.findall(r'<img[^>]*src="([^"]*)"', html2)
    print(f"Found {len(imgs)} images on Bing")
    for img in imgs[:10]:
        if any(k in img for k in ['th?', 'OIP', 'th?id']):
            print(f"  {img[:100]}")
except Exception as e:
    print(f"Bing: {e}")
