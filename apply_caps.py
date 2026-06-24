#!/usr/bin/env python3
"""Update FISH_IMG mapping with Jay's cap images."""
import json

BASE = 'https://raw.githubusercontent.com/fishing-n1-guy/fishing-hk/main/images/fish_caps'

# Fish name -> cap image file
caps = {
    '石斑': '01_石斑.jpg',
    '芝麻斑': '02_芝麻斑.jpg',
    '青斑': '03_青斑.jpg',
    '東星斑': '04_東星斑.jpg',
    '火點': '06_火點.jpg',
    '黃腳鱲': '07_黃腳鱲.jpg',
    '真鯛': '10_真鯛.jpg',
    '白鱲': '11_白鱲.jpg',
    '金古': '12_金古.jpg',
    '星鱸': '13_星鱸.jpg',
    '盲曹': '14_盲曹.jpg',
    '紅鮋': '15_紅鮋.jpg',
    '泥鯭': '16_泥鯭.jpg',
    '牙帶': '17_牙帶.jpg',
    '黃花魚': '18_黃花魚.jpg',
    '沙鑽': '19_沙鑽.jpg',
    '魷魚': '20_魷魚.jpg',
    '鯆魚': '21_鯆魚.jpg',
    '左口': '22_左口.jpg',
    '雞魚': '23_雞魚.jpg',
    '細鱗': '24a_細鱗.jpg',
    '青衣': '25_青衣.jpg',
    '紅杉': '26_紅杉.jpg',
    '大眼雞': '27_大眼雞.jpg',
    '馬友': '28_馬友.jpg',
    '烏頭': '29_烏頭.jpg',
    '池魚': '31_池魚.jpg',
    '梳羅': '32_梳羅.jpg',
    '三鬚': '33_三鬚.jpg',
    '赤筆': '34_赤筆.jpg',
    '沙鯭': '35_沙鯭.jpg',
    '雞泡魚': '36_雞泡魚.jpg',
    '剝皮魚': 'xx_剝皮魚.jpg',
}

with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# Find the FISH_IMG object
start = html.find('const FISH_IMG = {')
end = html.find('};', start) + 2
old_img = html[start:end]

# Build new FISH_IMG object
# Keep existing entries, override with caps
import re
# Extract existing entries
existing = {}
pattern = r'"([^"]+)":\s*"([^"]*)"'
for m in re.finditer(pattern, old_img):
    existing[m.group(1)] = m.group(2)

# Update with caps
for fish_name, cap_file in caps.items():
    existing[fish_name] = f'{BASE}/{cap_file}'

# Also set 細鱗 to use 24a (first type)
existing['細鱗'] = f'{BASE}/24a_細鱗.jpg'

# Build new JS object
new_img = 'const FISH_IMG = {\n'
for name, url in sorted(existing.items()):
    new_img += f'  "{name}": "{url}",\n'
new_img += '};\n'

html = html[:start] + new_img + html[end:]
with open('/opt/data/fishing-hk/index.html', 'w') as f:
    f.write(html)

print(f'✅ Updated FISH_IMG with {len(caps)} cap images')
print(f'Total fish in FISH_IMG: {len(existing)}')
