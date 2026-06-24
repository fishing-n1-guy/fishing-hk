#!/usr/bin/env python3
with open('/opt/data/fishing-hk/index.html') as f:
    c = f.read()

fixes = {
    '"金古": ""': '"金古": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Gnathanodon_speciosus_DubaiMall.jpg/330px-Gnathanodon_speciosus_DubaiMall.jpg"',
    '"火點": ""': '"火點": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Serranidae_-_Epinephelus_merra.JPG/330px-Serranidae_-_Epinephelus_merra.JPG"',
}

for old, new in fixes.items():
    if old in c:
        c = c.replace(old, new)
        print(f"✅ Fixed")
    else:
        print(f"❌ Not found: {old}")

with open('/opt/data/fishing-hk/index.html', 'w') as f2:
    f2.write(c)
