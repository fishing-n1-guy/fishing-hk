#!/usr/bin/env python3
"""Copy new fish images from cache and upload."""
import os, shutil, subprocess

DIR = '/opt/data/fishing-hk'
CAPS = os.path.join(DIR, 'fish_caps')
CACHE = '/app/image_cache'
os.makedirs(CAPS, exist_ok=True)

# New fish images from this session
new_images = {
    'img_3c5b41498c49.jpg': '37_鱸魚.jpg',
    'img_8173d0630e8b.jpg': '38_牛鰍.jpg',
    'img_d0a58988a5b0.jpg': '39_門鱔.jpg',
    'img_35449fc442c7.jpg': '40_石狗公.jpg',
    'img_f7b8a33f3de7.jpg': '41_黃鰭鮪.jpg',
    'img_61938e0e7e2d.jpg': '42_杉斑.jpg',
    'img_ec7c7eb37ae6.jpg': '43_坑鰜.jpg',
    'img_19923eb242e7.jpg': 'xx_石崇魚.jpg',
}

for src, dst in new_images.items():
    src_path = os.path.join(CACHE, src)
    if os.path.exists(src_path):
        shutil.copy2(src_path, os.path.join(CAPS, dst))
        print(f'✅ {dst}')
    else:
        print(f'❌ {src} not found')

print('\nNow committing and pushing...')
