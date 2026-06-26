#!/usr/bin/env python3
"""Test Pixabay and download an image."""
import urllib.request, json, ssl

ctx = ssl.create_default_context()
key = "56441428-36c1a798c00ef130b61ebd03e"

url = f"https://pixabay.com/api/?key={key}&q=pikachu&per_page=3&image_type=photo"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
    data = json.loads(r.read())

h = data['hits'][0]
img_url = h['webformatURL']
tags = h['tags']

print(f"Tags: {tags}")
print(f"URL: {img_url}")

# Download with proper headers
dl = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://pixabay.com/'})
with urllib.request.urlopen(dl, timeout=15, context=ctx) as r:
    img_data = r.read()

fname = '/opt/data/fishing-hk/pixabay_pikachu.jpg'
with open(fname, 'wb') as f:
    f.write(img_data)
print(f"Downloaded: {len(img_data)} bytes to {fname}")
