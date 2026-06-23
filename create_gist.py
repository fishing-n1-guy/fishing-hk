#!/usr/bin/env python3
"""Create an anonymous GitHub Gist with the fishing site."""
import urllib.request, urllib.error, json

with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# Create a GitHub Gist (anonymous)
gist = {
    "description": "🐟 香港釣魚資訊站 - by 小婷",
    "public": True,
    "files": {
        "index.html": {
            "content": html
        },
        "README.md": {
            "content": "# 香港釣魚資訊站\n\n由小婷為Jay製作 🎣\n\n天氣資料來自 Open-Meteo API\n每次開頁自動更新\n\n🌐 GitHub Pages URL:\nhttps://YOUR_USERNAME.github.io/fishing-hk/"
        }
    }
}

data = json.dumps(gist).encode()
req = urllib.request.Request('https://api.github.com/gists', data=data,
                              headers={'Content-Type': 'application/json',
                                      'User-Agent': 'fishing-hk-bot/1.0'},
                              method='POST')
try:
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read())
    print(f"Gist URL: {result.get('html_url')}")
    print(f"Raw URL: {result.get('files',{}).get('index.html',{}).get('raw_url')}")
    
    # Also get the gist ID for cloning
    gist_id = result.get('id')
    print(f"Gist ID: {gist_id}")
    
    # The raw URL to the file
    raw_url = result.get('files',{}).get('index.html',{}).get('raw_url')
    print(f"\n🌐 公開網站網址 (GitHub Raw):")
    print(f"   {raw_url}")
    print(f"\n或者用 GitHub Pages (要你自己開):")
    print(f"   https://YOUR_USERNAME.github.io/fishing-hk/")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(e.read().decode()[:500])
except Exception as e:
    print(f"Error: {e}")
