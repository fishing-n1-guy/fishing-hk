#!/usr/bin/env python3
"""Test various free image search APIs."""
import urllib.request, json

apis = []

# 1. Unsplash (free, no key needed for basic search)
try:
    req = urllib.request.Request(
        "https://api.unsplash.com/search/photos?query=pikachu&per_page=3",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    results = data.get('results', [])
    print(f"Unsplash: {len(results)} results (no API key)")
    for r in results[:2]:
        print(f"  {r.get('urls',{}).get('small','')[:80]}")
except Exception as e:
    print(f"Unsplash: {e}")

# 2. Pixabay (free tier, no key needed for basic?)
try:
    req = urllib.request.Request(
        "https://pixabay.com/api/?q=pikachu&per_page=3&key=48341419-6b7d9e9d1e0b8f5c5a9c7b3a1",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    print(f"\nPixabay: {data.get('total',0)} results (demo key)")
    for h in data.get('hits',[])[:2]:
        print(f"  {h.get('webformatURL','')[:80]}")
except Exception as e:
    print(f"\nPixabay: {e}")

# 3. DuckDuckGo Instant Answer API (free, no key)
try:
    req = urllib.request.Request(
        "https://api.duckduckgo.com/?q=pikachu&format=json&no_html=1",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    topics = data.get('RelatedTopics', [])[:3]
    print(f"\nDDG API: {len(topics)} topics")
    for t in topics:
        icon = t.get('Icon', {}).get('URL', '')
        print(f"  {t.get('Text','')[:50]} - Icon: {icon[:60]}")
except Exception as e:
    print(f"\nDDG API: {e}")
