#!/usr/bin/env python3
"""Try to find fish images via Wikipedia English name search."""
import json, urllib.request, urllib.parse, time

FISH_LOOKUP = [
    ("石斑", "Grouper"),
    ("芝麻斑", "Brown-marbled grouper"),
    ("青斑", "Orange-spotted grouper"),
    ("東星斑", "Leopard coral trout"),
    ("紅斑", "Red grouper"),
    ("火點", "Honeycomb grouper"),
    ("黃腳鱲", "Yellowfin seabream"),
    ("黑鱲", "Blackhead seabream"),
    ("立魚", "Red seabream"),
    ("真鯛", "Red seabream"),
    ("白鱲", "Grey large-eye bream"),
    ("星鱸", "Japanese sea bass"),
    ("盲曹", "Barramundi"),
    ("紅鮋", "Red gurnard"),
    ("泥鯭", "Rabbitfish"),
    ("牙帶", "Ribbonfish"),
    ("黃花魚", "Yellow croaker"),
    ("沙鑽", "Sand whiting"),
    ("魷魚", "Common squid"),
    ("鯆魚", "Common stingray"),
    ("左口", "Bastard halibut"),
    ("雞魚", "Javelin grunter"),
    ("細鱗", "Red morwong"),
    ("青衣", "Green wrasse"),
    ("紅杉", "Red bigeye"),
    ("大眼雞", "Glasseye"),
    ("馬友", "Fourfinger threadfin"),
    ("烏頭", "Flathead grey mullet"),
    ("金古", "Golden trevally"),
    ("池魚", "Atlantic horse mackerel"),
    ("梳羅", "Great barracuda"),
    ("三鬚", "Three-lined grunt"),
    ("赤筆", "Red mullet"),
    ("剝皮魚", "Filefish"),
    ("雞泡魚", "Japanese pufferfish"),
    ("鱸魚", "Japanese seaperch"),
    ("牛鰍", "European conger"),
    ("門鱔", "Pike eel"),
    ("石狗公", "Scorpionfish"),
    ("黃鰭鮪", "Yellowfin tuna"),
    ("杉斑", "Areolate grouper"),
    ("坑鰜", "Bumphead wrasse"),
    ("黃衣", "Yellowtail amberjack"),
    ("黑鮋", "Marbled rockfish"),
    ("冚畢", "Silver pompano"),
    ("斑𩶘", "Blackspot tuskfish"),
    ("海鱺", "Cobia"),
    ("水針", "Needlefish"),
    ("花利", "Bartail flathead"),
    ("金山鯽", "Mozambique tilapia"),
    ("塘虱", "Walking catfish"),
    ("墨魚", "Cuttlefish"),
    ("八爪魚", "Common octopus"),
    ("瀨尿蝦", "Japanese mantis shrimp"),
    ("花蟹", "Blue swimmer crab"),
    ("牛屎(黑鱲)", "Southern black bream"),
    ("黑沙(黑鱲)", "Black seabream"),
    ("白𩶘", "Silver seabream"),
    ("金絲䱽", "Ornate threadfin bream"),
    ("花鱸", "Barred knifejaw"),
    ("石釘", "Rockfish"),
    ("黑毛", "Brown surgeonfish"),
    ("龍躉", "Giant grouper"),
    ("皇帝魚", "Spangled emperor"),
    ("紅曹", "Crimson snapper"),
    ("金鼓", "Orange-spotted rabbitfish"),
    ("石蚌", "Indian threadfish"),
    ("飛魚", "Flying fish"),
    ("煙管魚", "Blue-spotted cornetfish"),
    ("藍旗𩶘", "Scup"),
    ("紅𩶘", "Blackspot seabream"),
    ("黃祥", "Redbelly yellowtail fusilier"),
    ("白杉", "Red grouper"),
]

def search_wiki(query):
    """Search Wikipedia for a page and get its image."""
    # First search for the page
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query + ' fish')}&format=json&srlimit=1"
    try:
        req = urllib.request.Request(search_url, headers={"User-Agent": "fishing-hk-bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        pages = data.get("query", {}).get("search", [])
        if pages:
            title = pages[0]["title"]
            # Get image for this page
            img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages&format=json&pithumbsize=200"
            req2 = urllib.request.Request(img_url, headers={"User-Agent": "fishing-hk-bot/1.0"})
            with urllib.request.urlopen(req2, timeout=10) as r2:
                data2 = json.loads(r2.read())
            for pid, page in data2.get("query", {}).get("pages", {}).items():
                if "thumbnail" in page:
                    return page["thumbnail"]["source"]
    except:
        pass
    return ""

results = []
for cn, en in FISH_LOOKUP:
    img = search_wiki(en)
    status = "✅" if img else "❌"
    print(f"{status} {cn} ({en})")
    if img:
        print(f"     {img[:100]}")
    results.append((cn, en, img))
    time.sleep(0.3)

print("\n\n=== SUMMARY ===")
total = len(results)
with_img = sum(1 for r in results if r[2])
print(f"Total: {total}, With images: {with_img} ({with_img/total*100:.0f}%)")
