#!/usr/bin/env python3
"""Update HTML with new fish cap images."""
import json, re

BASE = 'https://raw.githubusercontent.com/fishing-n1-guy/fishing-hk/main/images/fish_caps'

with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# Update FISH_IMG entries
caps_update = {
    '鱸魚': '37_鱸魚.jpg',
    '牛鰍': '38_牛鰍.jpg',
    '門鱔': '39_門鱔.jpg',
    '石狗公': '40_石狗公.jpg',
    '黃鰭鮪': '41_黃鰭鮪.jpg',
    '杉斑': '42_杉斑.jpg',
    '坑鰜': '43_坑鰜.jpg',
}

# Find FISH_IMG object and update entries
for name, cap_file in caps_update.items():
    url = f'{BASE}/{cap_file}'
    old_pattern = f'"{name}": "'
    idx = html.find(old_pattern)
    if idx >= 0:
        end = html.find('"', idx + len(old_pattern))
        old_val = html[idx:end+1]
        new_val = f'"{name}": "{url}"'
        html = html.replace(old_val, new_val)
        print(f'✅ {name} → {cap_file}')
    else:
        print(f'❌ {name} not found in FISH_IMG')

# Add 石崇魚 to FISH array (before the last entry)
fish_end = html.find('];', html.find('const FISH = ['))
new_entry = '  ["石崇魚", "Devil Firefish", "10-25cm", "全年", "中級", "Pterois volitans"],\n'
html = html[:fish_end] + new_entry + html[fish_end:]
print('✅ Added 石崇魚 to FISH array')

# Add 石崇魚 to FISH_IMG (before closing })
img_end = html.rfind('};', 0, html.find('// Load fish images'))
new_img_entry = f'  "石崇魚": "{BASE}/xx_石崇魚.jpg",\n'
html = html[:img_end] + new_img_entry + html[img_end:]
print('✅ Added 石崇魚 to FISH_IMG')

with open('/opt/data/fishing-hk/index.html', 'w') as f:
    f.write(html)

print('\nDone! Ready to push.')
