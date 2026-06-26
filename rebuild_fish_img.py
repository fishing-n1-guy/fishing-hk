#!/usr/bin/env python3
"""Rebuild FISH_IMG with correct GitHub Pages URLs."""
import json, re

BASE = 'https://fishing-n1-guy.github.io/fishing-hk/images/fish_caps'

# Fish names that have cap images
caps = {
    '石斑':'01_石斑.jpg','芝麻斑':'02_芝麻斑.jpg','青斑':'03_青斑.jpg',
    '東星斑':'04_東星斑.jpg','火點':'06_火點.jpg','黃腳鱲':'07_黃腳鱲.jpg',
    '真鯛':'10_真鯛.jpg','白鱲':'11_白鱲.jpg','金古':'12_金古.jpg',
    '星鱸':'13_星鱸.jpg','盲曹':'14_盲曹.jpg','紅鮋':'15_紅鮋.jpg',
    '泥鯭':'16_泥鯭.jpg','牙帶':'17_牙帶.jpg','黃花魚':'18_黃花魚.jpg',
    '沙鑽':'19_沙鑽.jpg','魷魚':'20_魷魚.jpg','鯆魚':'21_鯆魚.jpg',
    '左口':'22_左口.jpg','雞魚':'23_雞魚.jpg','細鱗':'24a_細鱗.jpg',
    '青衣':'25_青衣.jpg','紅杉':'26_紅杉.jpg','大眼雞':'27_大眼雞.jpg',
    '馬友':'28_馬友.jpg','烏頭':'29_烏頭.jpg','池魚':'31_池魚.jpg',
    '梳羅':'32_梳羅.jpg','三鬚':'33_三鬚.jpg','赤筆':'34_赤筆.jpg',
    '沙鯭':'35_沙鯭.jpg','雞泡魚':'36_雞泡魚.jpg','鱸魚':'37_鱸魚.jpg',
    '牛鰍':'38_牛鰍.jpg','門鱔':'39_門鱔.jpg','石狗公':'40_石狗公.jpg',
    '黃鰭鮪':'41_黃鰭鮪.jpg','杉斑':'42_杉斑.jpg','坑鰜':'43_坑鰜.jpg',
    '剝皮魚':'xx_剝皮魚.jpg','石崇魚':'xx_石崇魚.jpg',
}

with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# Find and rebuild FISH_IMG
start = html.find('const FISH_IMG = {')
end = html.find('};', start) + 2

# Extract existing entries from the broken JSON
lines = html[start:end].split('\n')
entries = {}
for line in lines:
    line = line.strip().rstrip(',')
    if ':' in line and line.startswith('"'):
        idx = line.index(':')
        name = line[1:idx-1]  # Remove quotes
        # Skip broken entries (where value is just a URL)
        val = line[idx+1:].strip().strip('"').strip("'")
        if val.startswith('http') or val == '':
            entries[name] = val
    elif line.startswith("'https"):
        # Broken line - skip
        pass

# Override with cap images
for name, cap_file in caps.items():
    entries[name] = f'{BASE}/{cap_file}'

# Rebuild FISH_IMG JS object
new_img = 'const FISH_IMG = {\n'
for name in sorted(entries.keys()):
    val = entries[name]
    new_img += f'  "{name}": "{val}",\n'
new_img += '};\n'

html = html[:start] + new_img + html[end:]
with open('/opt/data/fishing-hk/index.html', 'w') as f:
    f.write(html)

print(f'✅ Rebuilt FISH_IMG with {len(entries)} entries')
print(f'   Cap images: {len(caps)}')
