#!/usr/bin/env python3
"""Embed iNaturalist fish images into index.html."""
import json, os

with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# Read the output from fetch_inat_all.py and extract the FISH_IMG mapping
# I'll hardcode it from the output above
fish_img = {
  "三鬚": "https://inaturalist-open-data.s3.amazonaws.com/photos/91052007/medium.jpg",
  "八爪魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/166419253/medium.jpeg",
  "冚畢": "https://inaturalist-open-data.s3.amazonaws.com/photos/177414434/medium.jpg",
  "剝皮魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/403168785/medium.jpg",
  "坑鰜": "https://inaturalist-open-data.s3.amazonaws.com/photos/5683217/medium.jpg",
  "塘虱": "https://inaturalist-open-data.s3.amazonaws.com/photos/184997852/medium.jpeg",
  "墨魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/269553588/medium.jpeg",
  "大眼雞": "https://static.inaturalist.org/photos/49855077/medium.jpeg",
  "左口": "https://static.inaturalist.org/photos/22497934/medium.jpeg",
  "斑𩶘": "https://inaturalist-open-data.s3.amazonaws.com/photos/66293751/medium.jpg",
  "星鱸": "https://inaturalist-open-data.s3.amazonaws.com/photos/67119374/medium.jpg",
  "杉斑": "https://static.inaturalist.org/photos/223274644/medium.jpg",
  "東星斑": "https://static.inaturalist.org/photos/216412385/medium.jpeg",
  "梳羅": "https://static.inaturalist.org/photos/64376618/medium.jpeg",
  "水針": "https://inaturalist-open-data.s3.amazonaws.com/photos/59573265/medium.jpg",
  "池魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/293232824/medium.jpg",
  "沙鑽": "https://inaturalist-open-data.s3.amazonaws.com/photos/550769007/medium.jpg",
  "沙鯭": "https://static.inaturalist.org/photos/55708341/medium.jpeg",
  "泥鯭": "https://inaturalist-open-data.s3.amazonaws.com/photos/508644739/medium.jpg",
  "海鱺": "https://inaturalist-open-data.s3.amazonaws.com/photos/19249056/medium.jpg",
  "瀨尿蝦": "https://static.inaturalist.org/photos/347965071/medium.jpg",
  "火點": "https://inaturalist-open-data.s3.amazonaws.com/photos/5921949/medium.jpg",
  "烏頭": "https://inaturalist-open-data.s3.amazonaws.com/photos/11976021/medium.jpeg",
  "煙管魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/564563445/medium.jpg",
  "牙帶": "https://static.inaturalist.org/photos/73037040/medium.jpg",
  "牛屎(黑鱲)": "https://inaturalist-open-data.s3.amazonaws.com/photos/411406402/medium.jpeg",
  "牛鰍": "https://inaturalist-open-data.s3.amazonaws.com/photos/400873304/medium.jpg",
  "白杉": "https://inaturalist-open-data.s3.amazonaws.com/photos/164870591/medium.jpeg",
  "白花": "https://inaturalist-open-data.s3.amazonaws.com/photos/355943806/medium.jpeg",
  "白鱲": "https://inaturalist-open-data.s3.amazonaws.com/photos/62858904/medium.jpg",
  "白𩶘": "https://inaturalist-open-data.s3.amazonaws.com/photos/522329686/medium.jpg",
  "皇帝魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/5333031/medium.jpeg",
  "盲曹": "https://inaturalist-open-data.s3.amazonaws.com/photos/256218238/medium.jpg",
  "真鯛": "https://inaturalist-open-data.s3.amazonaws.com/photos/655290555/medium.jpg",
  "石斑": "https://inaturalist-open-data.s3.amazonaws.com/photos/576952820/medium.jpg",
  "石狗公": "https://inaturalist-open-data.s3.amazonaws.com/photos/4643920/medium.jpg",
  "石蚌": "https://inaturalist-open-data.s3.amazonaws.com/photos/49869809/medium.jpg",
  "石釘": "https://inaturalist-open-data.s3.amazonaws.com/photos/100750462/medium.jpeg",
  "立魚": "https://static.inaturalist.org/photos/18161210/medium.jpeg",
  "紅斑": "https://inaturalist-open-data.s3.amazonaws.com/photos/377149934/medium.jpg",
  "紅曹": "https://inaturalist-open-data.s3.amazonaws.com/photos/42867947/medium.jpeg",
  "紅杉": "https://inaturalist-open-data.s3.amazonaws.com/photos/269662033/medium.jpg",
  "紅衫": "https://inaturalist-open-data.s3.amazonaws.com/photos/442768330/medium.png",
  "紅鮋": "https://inaturalist-open-data.s3.amazonaws.com/photos/279330602/medium.jpeg",
  "紅𩶘": "https://inaturalist-open-data.s3.amazonaws.com/photos/84255343/medium.jpg",
  "細鱗": "https://inaturalist-open-data.s3.amazonaws.com/photos/82324715/medium.jpg",
  "芝麻斑": "https://inaturalist-open-data.s3.amazonaws.com/photos/2433956/medium.jpg",
  "花利": "https://inaturalist-open-data.s3.amazonaws.com/photos/186724371/medium.jpg",
  "花蟹": "https://inaturalist-open-data.s3.amazonaws.com/photos/4856888/medium.jpg",
  "花鱸": "https://inaturalist-open-data.s3.amazonaws.com/photos/396871759/medium.jpg",
  "藍旗𩶘": "https://static.inaturalist.org/photos/18161210/medium.jpeg",
  "赤筆": "https://inaturalist-open-data.s3.amazonaws.com/photos/240991964/medium.jpeg",
  "金古": "https://inaturalist-open-data.s3.amazonaws.com/photos/334218799/medium.jpg",
  "金山鯽": "https://inaturalist-open-data.s3.amazonaws.com/photos/27229755/medium.jpg",
  "金絲䱽": "https://inaturalist-open-data.s3.amazonaws.com/photos/531678968/medium.jpg",
  "金鼓": "https://static.inaturalist.org/photos/34715173/medium.jpg",
  "門鱔": "https://inaturalist-open-data.s3.amazonaws.com/photos/477039677/medium.jpg",
  "雞泡魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/60989907/medium.jpg",
  "雞魚": "https://static.inaturalist.org/photos/273377366/medium.jpeg",
  "青斑": "https://inaturalist-open-data.s3.amazonaws.com/photos/187446351/medium.jpg",
  "青衣": "https://inaturalist-open-data.s3.amazonaws.com/photos/239664823/medium.jpg",
  "青龍": "https://inaturalist-open-data.s3.amazonaws.com/photos/239664823/medium.jpg",
  "飛魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/356536018/medium.jpeg",
  "馬友": "https://inaturalist-open-data.s3.amazonaws.com/photos/11930136/medium.jpg",
  "魷魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/102663129/medium.jpg",
  "鯆魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/265483902/medium.jpg",
  "鱸魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/67119374/medium.jpg",
  "黃祥": "https://inaturalist-open-data.s3.amazonaws.com/photos/2995124/medium.jpg",
  "黃腳鱲": "https://inaturalist-open-data.s3.amazonaws.com/photos/134294127/medium.jpg",
  "黃花魚": "https://inaturalist-open-data.s3.amazonaws.com/photos/359488548/medium.jpeg",
  "黃衣": "https://inaturalist-open-data.s3.amazonaws.com/photos/5853956/medium.jpg",
  "黃鰭鮪": "https://inaturalist-open-data.s3.amazonaws.com/photos/207078977/medium.jpg",
  "黑毛": "https://inaturalist-open-data.s3.amazonaws.com/photos/11975500/medium.jpeg",
  "黑沙(黑鱲)": "https://inaturalist-open-data.s3.amazonaws.com/photos/347604518/medium.jpg",
  "黑鮋": "https://inaturalist-open-data.s3.amazonaws.com/photos/147015519/medium.jpeg",
  "黑鱲": "https://inaturalist-open-data.s3.amazonaws.com/photos/347604518/medium.jpg",
  "龍躉": "https://inaturalist-open-data.s3.amazonaws.com/photos/11975452/medium.jpeg",
}

# Generate JS
fish_img_js = "const FISH_IMG = " + json.dumps(fish_img, ensure_ascii=False) + ";"

# Replace in HTML
# Find where to insert: after the FISH array
start_marker = "// Wikipedia fish image cache"
end_marker = "async function loadFishImages()"

new_section = fish_img_js + "\n\n// Load fish images from iNaturalist\nasync function loadFishImages() {\n  var g = document.getElementById('fishGrid');\n  if (!g) return;\n  var cards = g.querySelectorAll('.fi');\n  for (var i = 0; i < FISH.length && i < cards.length; i++) {\n    var existing = cards[i].querySelector('.fi-img-wrap');\n    if (!existing) continue;\n    var imgUrl = FISH_IMG[FISH[i][0]];\n    if (imgUrl) {\n      existing.innerHTML = '<img src=\"'+imgUrl+'\" style=\"width:100%;height:100%;object-fit:contain\" alt=\"'+FISH[i][0]+'\">';\n    } else {\n      existing.innerHTML = '';\n    }\n  }\n}"

# Replace the old function
old_start = html.find(start_marker)
old_end = html.find("// Render fish cards", old_start)

new_html = html[:old_start] + new_section + "\n\n" + html[old_end:]

with open('/opt/data/fishing-hk/index.html', 'w') as f:
    f.write(new_html)

print("✅ Updated index.html with iNaturalist fish images")
print(f"File size: {len(new_html)} bytes")
