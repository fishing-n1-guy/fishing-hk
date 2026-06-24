#!/usr/bin/env python3
with open('/opt/data/fishing-hk/index.html') as f:
    c = f.read()

fixes = [
    ('"金古": "https://inaturalist-open-data.s3.amazonaws.com/photos/334218799/medium.jpg"', '"金古": ""'),
    ('"火點": "https://inaturalist-open-data.s3.amazonaws.com/photos/5921949/medium.jpg"', '"火點": ""'),
]

for old, new in fixes:
    if old in c:
        c = c.replace(old, new)
        print(f"✅ Fixed: {old[:30]}...")
    else:
        print(f"❌ Not found: {old[:30]}...")

with open('/opt/data/fishing-hk/index.html', 'w') as f2:
    f2.write(c)
