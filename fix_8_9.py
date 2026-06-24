#!/usr/bin/env python3
with open('/opt/data/fishing-hk/index.html') as f:
    c = f.read()

# Fix 黑鱲 (fish #8) - remove image
old = '"黑鱲": "https://inaturalist-open-data.s3.amazonaws.com/photos/347604518/medium.jpg"'
new = '"黑鱲": ""'
if old in c:
    c = c.replace(old, new)
    print("✅ 黑鱲 removed")
else:
    print("❌ 黑鱲 not found")

# Fix 立魚 (fish #9) - remove image
old2 = '"立魚": "https://static.inaturalist.org/photos/18161210/medium.jpeg"'
new2 = '"立魚": ""'
if old2 in c:
    c = c.replace(old2, new2)
    print("✅ 立魚 removed")
else:
    print("❌ 立魚 not found")

with open('/opt/data/fishing-hk/index.html', 'w') as f2:
    f2.write(c)
