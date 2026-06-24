#!/usr/bin/env python3
with open('/opt/data/fishing-hk/index.html') as f:
    c = f.read()

# Remove 黑鱲 entry from FISH array
old1 = '  ["黑鱲", "Black Bream", "20-45cm", "冬季", "初級", "Acanthopagrus schlegelii"],\n'
if old1 in c:
    c = c.replace(old1, '')
    print("✅ Removed 黑鱲 from FISH array")
else:
    print("❌ 黑鱲 not found in FISH array")

# Remove 立魚 entry from FISH array
old2 = '  ["立魚", "Sea Bream", "20-60cm", "秋冬季", "初級", "Pagrus pagrus"],\n'
if old2 in c:
    c = c.replace(old2, '')
    print("✅ Removed 立魚 from FISH array")
else:
    print("❌ 立魚 not found in FISH array")

with open('/opt/data/fishing-hk/index.html', 'w') as f2:
    f2.write(c)
