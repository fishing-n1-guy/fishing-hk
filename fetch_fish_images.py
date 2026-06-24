#!/usr/bin/env python3
"""Look up fish images from Wikipedia API."""
import json, urllib.request, urllib.parse, time

# (Chinese, English, sci_name) for each fish we want images for
FISH_SCI = [
    ("石斑", "Grouper", "Epinephelus marginatus"),
    ("芝麻斑", "Brown-marbled Grouper", "Epinephelus fuscoguttatus"),
    ("青斑", "Orange-spotted Grouper", "Epinephelus coioides"),
    ("東星斑", "Coral Trout", "Plectropomus leopardus"),
    ("紅斑", "Red Grouper", "Epinephelus akaara"),
    ("火點", "Spotty Grouper", "Epinephelus merra"),
    ("黃腳鱲", "Yellowfin Bream", "Acanthopagrus latus"),
    ("黑鱲", "Black Bream", "Acanthopagrus schlegelii"),
    ("立魚", "Sea Bream", "Pagrus pagrus"),
    ("真鯛", "Red Sea Bream", "Pagrus major"),
    ("白鱲", "White Snapper", "Gymnocranius griseus"),
    ("星鱸", "Spotted Sea Bass", "Lateolabrax japonicus"),
    ("盲曹", "Barramundi", "Lates calcarifer"),
    ("紅鮋", "Red Gurnard", "Chelidonichthys lucerna"),
    ("泥鯭", "Rabbitfish", "Siganus canaliculatus"),
    ("牙帶", "Ribbonfish", "Lepidopus caudatus"),
    ("黃花魚", "Yellow Croaker", "Larimichthys crocea"),
    ("沙鑽", "Sand Whiting", "Sillago sihama"),
    ("魷魚", "Squid", "Loligo vulgaris"),
    ("鯆魚", "Ray", "Dasyatis pastinaca"),
    ("左口", "Flatfish", "Paralichthys olivaceus"),
    ("雞魚", "Javelin Grunter", "Pomadasys kaakan"),
    ("細鱗", "Red Morwong", "Cheilodactylus zonatus"),
    ("青衣", "Green Wrasse", "Halichoeres hortulanus"),
    ("紅杉", "Red Bigeye", "Priacanthus macracanthus"),
    ("大眼雞", "Bigeye", "Heteropriacanthus cruentatus"),
    ("馬友", "Fourfinger Threadfin", "Eleutheronema tetradactylum"),
    ("烏頭", "Grey Mullet", "Mugil cephalus"),
    ("金古", "Golden Trevally", "Gnathanodon speciosus"),
    ("池魚", "Horse Mackerel", "Trachurus trachurus"),
    ("梳羅", "Barracuda", "Sphyraena barracuda"),
    ("三鬚", "Three-lined Grunt", "Plectorhinchus cinctus"),
    ("赤筆", "Red Mullet", "Mullus barbatus"),
    ("剝皮魚", "Filefish", "Stephanolepis hispidus"),
    ("雞泡魚", "Pufferfish", "Takifugu rubripes"),
    ("鱸魚", "Japanese Sea Bass", "Lateolabrax japonicus"),
    ("牛鰍", "Conger Eel", "Conger conger"),
    ("門鱔", "Pike Eel", "Muraenesox cinereus"),
    ("石狗公", "Scorpionfish", "Scorpaena notata"),
    ("黃鰭鮪", "Yellowfin Tuna", "Thunnus albacares"),
    ("杉斑", "Areolate Grouper", "Epinephelus areolatus"),
    ("花頭梅", "Half-banded Seaperch", "Hypodytes rubicundus"),
    ("坑鰜", "Wrasse", "Cheilinus trilobatus"),
    ("黃衣", "Yellowtail", "Seriola lalandi"),
    ("白花", "White Croaker", "Pennahia argentata"),
    ("紅衫", "Golden Thread", "Nemipterus virgatus"),
    ("黑鮋", "Black Scorpionfish", "Sebastiscus marmoratus"),
    ("冚畢", "Snubnose Pompano", "Trachinotus blochii"),
    ("斑𩶘", "Blackspot Tuskfish", "Choerodon schoenleinii"),
    ("海鱺", "Cobia", "Rachycentron canadum"),
    ("水針", "Needlefish", "Tylosurus acus"),
    ("沙鯭", "Lizardfish", "Synodus saurus"),
    ("花利", "Flathead", "Platycephalus indicus"),
    ("金山鯽", "Tilapia", "Oreochromis mossambicus"),
    ("塘虱", "Walking Catfish", "Clarias batrachus"),
    ("墨魚", "Cuttlefish", "Sepia officinalis"),
    ("八爪魚", "Octopus", "Octopus vulgaris"),
    ("瀨尿蝦", "Mantis Shrimp", "Oratosquilla oratoria"),
    ("花蟹", "Flower Crab", "Portunus pelagicus"),
    ("牛屎(黑鱲)", "Southern Black Bream", "Acanthopagrus butcheri"),
    ("黑沙(黑鱲)", "Black Sea Bream", "Acanthopagrus schlegelii"),
    ("白𩶘", "White Bream", "Rhabdosargus sarba"),
    ("金絲䱽", "Golden Threadfin", "Nemipterus hexodon"),
    ("花鱸", "Barred Knifejaw", "Oplegnathus fasciatus"),
    ("石釘", "Rockfish", "Sebastes steindachneri"),
    ("黑毛", "Black Surgeonfish", "Acanthurus nigrofuscus"),
    ("龍躉", "Giant Grouper", "Epinephelus lanceolatus"),
    ("皇帝魚", "Spangled Emperor", "Lethrinus nebulosus"),
    ("紅曹", "Red Snapper", "Lutjanus erythropterus"),
    ("金鼓", "Golden Rabbitfish", "Siganus guttatus"),
    ("石蚌", "Diamond Trevally", "Alectis indica"),
    ("飛魚", "Flying Fish", "Exocoetus volitans"),
    ("煙管魚", "Flutemouth", "Fistularia commersonii"),
    ("藍旗𩶘", "Blue-lined Bream", "Stenotomus chrysops"),
    ("紅𩶘", "Red Bream", "Pagellus erythrinus"),
    ("青龍", "Green Wrasse", "Halichoeres hortulanus"),
    ("黃祥", "Yellowtail Fusilier", "Caesio cuning"),
    ("白杉", "White Grouper", "Epinephelus akaara"),
]

def get_image(sci_name):
    """Get Wikipedia image URL for a scientific name."""
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(sci_name)}&prop=pageimages&format=json&pithumbsize=200"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fishing-hk-bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if "thumbnail" in page:
                return page["thumbnail"]["source"]
    except:
        pass
    return ""

# Try each fish, only print those with images
results = []
for cn, en, sci in FISH_SCI:
    img = get_image(sci)
    status = "✅" if img else "❌"
    print(f"{status} {cn}: {sci} -> {img[:80] if img else 'NO IMAGE'}")
    results.append((cn, en, sci, img))
    time.sleep(0.3)  # Be nice to API

print("\n\n=== Summary ===")
print(f"Total: {len(results)}, With images: {sum(1 for r in results if r[3])}")
