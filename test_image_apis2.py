#!/usr/bin/env python3
"""Test more free image APIs."""
import urllib.request, json, ssl

# 1. Openverse (WordPress - free, no key for basic)
try:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        "https://api.openverse.org/v1/images/?q=pikachu+mario&page_size=3",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        data = json.loads(r.read())
    results = data.get('results', [])
    print(f"Openverse: {data.get('result_count',0)} results")
    for r in results[:3]:
        print(f"  {r.get('title','')} - {r.get('thumbnail','')[:80]}")
except Exception as e:
    print(f"Openverse: {e}")

# 2. Try a different Bing approach - use the free API
try:
    req = urllib.request.Request(
        "https://api.bing.microsoft.com/v7.0/images/search?q=Pikachu+Mario+Pokemon+card&count=3",
        headers={'Ocp-Apim-Subscription-Key': ''}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    print(f"\nBing API: {data.get('totalEstimatedMatches',0)} matches")
    for v in data.get('value',[])[:2]:
        print(f"  {v.get('name','')[:40]} - {v.get('contentUrl','')[:80]}")
except urllib.error.HTTPError as e:
    print(f"\nBing API: {e.code} - need API key")
except Exception as e:
    print(f"\nBing API: {e}")

# 3. Try Deezer/LastFM approach - search Wikipedia for images
try:
    req = urllib.request.Request(
        "https://en.wikipedia.org/api/rest_v1/page/summary/Pikachu",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    print(f"\nWikipedia: {data.get('title','')}")
    print(f"  Thumbnail: {data.get('thumbnail',{}).get('source','')}")
except Exception as e:
    print(f"\nWikipedia: {e}")
