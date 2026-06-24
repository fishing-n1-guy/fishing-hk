#!/usr/bin/env python3
with open('/opt/data/fishing-hk/index.html') as f:
    c = f.read()
old = '"青龍": "https://inaturalist-open-data.s3.amazonaws.com/photos/239664823/medium.jpg"'
new = '"青龍": ""'
if old in c:
    c = c.replace(old, new)
    with open('/opt/data/fishing-hk/index.html', 'w') as f2:
        f2.write(c)
    print("✅ Fixed 青龍")
else:
    # Search for 青龍 in the file
    idx = c.find('青龍')
    if idx >= 0:
        print(f"Found 青龍 at position {idx}")
        print(f"Context: {c[idx-10:idx+80]}")
    else:
        print("❌ 青龍 not found")
