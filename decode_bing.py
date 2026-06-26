#!/usr/bin/env python3
"""Decode Bing search URLs to find trading platforms."""
import re, urllib.parse

with open('/tmp/bing_jihuan2.html') as f:
    html = f.read()

# Extract Bing redirect URLs
for m in re.finditer(r'href="(https://www\.bing\.com/ck/a[^"]*)"', html):
    url = m.group(1)
    # Extract the actual URL from the 'u' parameter
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    if 'u' in params:
        actual = params['u'][0]
        if any(k in actual for k in ['jihuan', 'xie', '鞋', '集换', 'trade', 'card']):
            print(actual)
    break  # Just get first matching one

print("---")
# Also try to find 鞋網 references
for m in re.finditer(r'鞋網|携網|協網', html):
    start = max(0, m.start()-50)
    end = min(len(html), m.end()+50)
    print(f"...around '鞋網': {html[start:end]}")
