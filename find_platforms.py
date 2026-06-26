#!/usr/bin/env python3
"""Search for Chinese Pokemon card trading platforms."""
import urllib.request, re, ssl

ctx = ssl.create_default_context()

# Search for the specific platforms
for domain in ["jihuanshe.com", "xiewang.net", "xiewang.com", "xiewang.cn", "xdora.com", "pkmnchina.com"]:
    url = f"https://www.{domain}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=8, context=ctx) as r:
            html = r.read().decode('utf-8', errors='replace')[:500]
        title = re.search(r'<title>([^<]*)</title>', html)
        title_txt = title.group(1)[:40] if title else "no title"
        print(f"✅ {domain}: {title_txt}")
    except Exception as e:
        err = str(e)[:30]
        print(f"❌ {domain}: {err}")
