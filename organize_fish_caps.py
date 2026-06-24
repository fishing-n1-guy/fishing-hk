#!/usr/bin/env python3
"""Copy and organize fish cap images from Telegram cache."""
import os, shutil

cache = '/app/image_cache'
dest = '/opt/data/fishing-hk/fish_caps'
os.makedirs(dest, exist_ok=True)

# Mapping: cache filename -> fish number + name
mapping = {
    'img_f4f4c9f24ddf.jpg': '01_石斑',
    'img_0bfb6a5734c2.jpg': '02_芝麻斑',
    'img_5cfde4ee6f51.jpg': '03_青斑', 
    'img_292155f4c505.jpg': '04_東星斑',
    'img_c4a3c7127fd6.jpg': '06_火點',
    'img_dff99c248ceb.jpg': '07_黃腳鱲',
    'img_170a58db4676.jpg': '10_真鯛',
    'img_833073c4b564.jpg': '11_白鱲',
    'img_2cb2ff484dd2.jpg': '12_金古',
    'img_cfc1988b7c26.jpg': '13_星鱸',
    'img_a502f1285df5.jpg': '14_盲曹',
    'img_2fdbcbb4d737.jpg': '15_紅鮋',
    'img_e096fa5b6d2a.jpg': '16_泥鯭',
    'img_5574b738e5e1.jpg': '17_牙帶',
    'img_ab4f650e60a1.jpg': '18_黃花魚',
    'img_4849c0176919.jpg': '19_沙鑽',
    'img_afb6077ace20.jpg': '20_魷魚',
    'img_011b886af7f0.jpg': '21_鯆魚',
    'img_6660526c7ee4.jpg': '22_左口',
    'img_f982f75bbbf2.jpg': '23_雞魚',
    'img_b2f58b3c079d.jpg': '24a_細鱗',
    'img_9ab18e2bd066.jpg': '24b_細鱗',
    'img_6826254ee9da.jpg': '25_青衣',
    'img_5427a1341274.jpg': '26_紅杉',
    'img_7fbee35d9758.jpg': '27_大眼雞',
    'img_94d05e831ae6.jpg': '28_馬友',
    'img_151dd8819bd8.jpg': '29_烏頭',
    'img_6cd933761c8d.jpg': '31_池魚',
    'img_59092309b2b3.jpg': '32_梳羅',
    'img_2cfaa8b5fe3e.jpg': '33_三鬚',
    'img_f352d801eee5.jpg': '34_赤筆',
    'img_10ca831720bb.jpg': '35_沙鯭',
    'img_8b7178e87fce.jpg': 'xx_剝皮魚',
    'img_8dc45fdf49b9.jpg': '36_雞泡魚',
}

copied = 0
for src_name, fish_name in mapping.items():
    src_path = os.path.join(cache, src_name)
    if os.path.exists(src_path):
        ext = os.path.splitext(src_name)[1]
        dst_name = f'{fish_name}{ext}'
        dst_path = os.path.join(dest, dst_name)
        shutil.copy2(src_path, dst_path)
        print(f'✅ {dst_name}')
        copied += 1
    else:
        print(f'❌ {src_name} not found')

print(f'\nCopied {copied}/{len(mapping)} fish images')
print(f'Location: {dest}')
