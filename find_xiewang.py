#!/usr/bin/env python3
"""Find '鞋網' Chinese Pokemon card platform."""
import urllib.request, re, ssl, urllib.parse

ctx = ssl.create_default_context()

# Search for 鞋網 in context of Pokemon cards
query = urllib.parse.quote("鞋網 寶可夢 卡牌 交易平台")
url = f"https://www.bing.com/search?q={query}"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml'
})
try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        html = r.read().decode('utf-8', errors='replace')
    
    # Find all links
    for m in re.finditer(r'<a[^>]*href="(https?://[^"]*)"[^>]*>([^<]*)</a>', html):
        href = m.group(1)
        text = m.group(2)
        if any(k in href.lower()+text.lower() for k in ['鞋', 'xie', 'pokemon', '卡牌', '交易']):
            if 'bing' not in href and 'microsoft' not in href:
                print(f"  {text.strip()[:40]}")
                print(f"  {href[:100]}")
except Exception as e:
    print(f"Error: {e}")
