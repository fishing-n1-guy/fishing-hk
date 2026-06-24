#!/usr/bin/env python3
"""Add image zoom lightbox and sea area info."""
import json

with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# 1. Lightbox CSS
lb_css = '\n.lightbox{display:none;position:fixed;z-index:9999;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);justify-content:center;align-items:center;cursor:pointer}\n.lightbox.act{display:flex}\n.lightbox img{max-width:90%;max-height:90%;object-fit:contain;border-radius:8px}'
style_end = html.rfind('</style>')
html = html[:style_end] + lb_css + '\n' + html[style_end:]

# 2. Lightbox HTML
lb_html = '<div class="lightbox" id="fishLightbox" onclick="closeLightbox()"><img id="fishLightboxImg" src="" alt=""></div>\n'
script_start = html.find('<script>')
html = html[:script_start] + lb_html + html[script_start:]

# 3. Lightbox JS
lb_js = '\nfunction openLightbox(s){document.getElementById("fishLightboxImg").src=s;document.getElementById("fishLightbox").classList.add("act");}\nfunction closeLightbox(){document.getElementById("fishLightbox").classList.remove("act");}\n'
func_idx = html.find('async function loadFishImages')
html = html[:func_idx] + lb_js + html[func_idx:]

# 4. Update img to have cursor pointer and onclick
html = html.replace(
  'style="width:100%;height:100%;object-fit:contain" alt="',
  'style="width:100%;height:100%;object-fit:contain;cursor:pointer" onclick="openLightbox(this.src)" alt="'
)

# 5. Sea area data
sea = {
    '石斑':'東水,西貢,南水','芝麻斑':'東水,西貢','青斑':'東水,南水,西貢',
    '東星斑':'東水,南水','紅斑':'東水,西貢','火點':'東水,南水',
    '黃腳鱲':'全海域','真鯛':'東水,南水','白鱲':'東水,南水,西貢',
    '金古':'全海域','星鱸':'東水,西貢,南水','盲曹':'西水,北水',
    '紅鮋':'西水,南水','泥鯭':'全海域','牙帶':'東水,南水',
    '黃花魚':'南水,西水','沙鑽':'西水,南水','魷魚':'全海域',
    '鯆魚':'西水,南水','左口':'西水,南水','雞魚':'東水,西貢,南水',
    '細鱗':'東水,西貢','青衣':'東水,西貢,南水','紅杉':'東水,南水',
    '大眼雞':'東水,南水','馬友':'西水,北水','烏頭':'西水,北水',
    '池魚':'全海域','梳羅':'全海域','三鬚':'東水,西貢,南水',
    '赤筆':'東水,南水','剝皮魚':'東水,西貢','雞泡魚':'全海域',
    '鱸魚':'東水,西貢,南水','牛鰍':'東水,西貢','門鱔':'東水,西貢',
    '石狗公':'東水,西貢','黃鰭鮪':'東水,南水','杉斑':'東水,南水,西貢',
    '坑鰜':'東水,西貢','黃衣':'東水,南水','黑鮋':'東水,西貢',
    '冚畢':'西水,南水','斑𩶘':'東水,西貢','海鱺':'東水,南水',
    '水針':'全海域','沙鯭':'西水,南水','花利':'西水,南水',
    '金山鯽':'北水,西水','塘虱':'北水','墨魚':'東水,西貢',
    '八爪魚':'東水,西貢','瀨尿蝦':'西水,南水','花蟹':'西水,南水',
    '牛屎(黑鱲)':'東水,西貢','黑沙(黑鱲)':'東水,西貢',
    '白𩶘':'東水,南水','金絲䱽':'東水,南水','花鱸':'東水,西貢,南水',
    '石釘':'東水,西貢','黑毛':'東水,西貢','龍躉':'東水,南水,西貢',
    '皇帝魚':'東水,南水','紅曹':'東水,南水','金鼓':'東水,西貢',
    '石蚌':'東水,南水','飛魚':'東水,南水','煙管魚':'東水,南水',
    '藍旗𩶘':'東水,南水','紅𩶘':'東水,南水','青龍':'東水,西貢',
    '黃祥':'東水,南水','白杉':'東水,西貢','花頭梅':'東水,西貢',
    '白花':'南水,西水','紅衫':'東水,南水','石崇魚':'東水,西貢',
}

# 6. Add sea area as 7th field to FISH array
fish_start = html.find('const FISH = [')
fish_end = html.find('];', fish_start) + 2
fish_section = html[fish_start:fish_end]

new_fish_lines = []
for line in fish_section.split('\n'):
    stripped = line.strip()
    if stripped.startswith('//') or stripped.startswith('const') or stripped.startswith('];'):
        new_fish_lines.append(line)
        continue
    if stripped.startswith('['):
        try:
            entry = json.loads(stripped.rstrip(','))
            name = entry[0]
            entry.append(sea.get(name, '待補充'))
            indent = line[:len(line)-len(line.lstrip())]
            new_line = indent + json.dumps(entry, ensure_ascii=False)
            if stripped.endswith(','):
                new_line += ','
            new_fish_lines.append(new_line)
        except:
            new_fish_lines.append(line)
    else:
        new_fish_lines.append(line)

html = html[:fish_start] + '\n'.join(new_fish_lines) + html[fish_end:]

# 7. Update fish card rendering to show sea area
# Find the badge line and add sea area after it
badge_end_marker = "difficulty:'+FISH[i][4]+'</span></div></div>';"
sea_area_marker = "h += '<div style=\"font-size:9px;color:#667;margin-top:2px\">'+FISH[i][6]+'</div></div></div>';"

old_badge = badge_end_marker
new_badge = "difficulty:'+FISH[i][4]+'</span>" + sea_area_marker

if old_badge in html:
    html = html.replace(old_badge, new_badge)
    print('Badge replacement OK')
else:
    print('Badge NOT found, trying to find it...')
    idx = html.find('FISH[i][4]')
    if idx >= 0:
        print(f'Found FISH[i][4] at {idx}: {html[idx:idx+80]}')

with open('/opt/data/fishing-hk/index.html', 'w') as f:
    f.write(html)

print('Done!')
