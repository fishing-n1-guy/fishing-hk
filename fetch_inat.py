#!/usr/bin/env python3
"""Fetch fish images from iNaturalist API (CC-BY photos)."""
import json, urllib.request, urllib.parse, time

FISH = [
    ("石斑", "grouper"),
    ("芝麻斑", "Epinephelus fuscoguttatus"),
    ("青斑", "Epinephelus coioides"),
    ("東星斑", "Plectropomus leopardus"),
    ("紅斑", "Epinephelus akaara"),
    ("火點", "Epinephelus merra"),
    ("黃腳鱲", "Acanthopagrus latus"),
    ("黑鱲", "Acanthopagrus schlegelii"),
    ("立魚", "Pagrus pagrus"),
    ("真鯛", "Pagrus major"),
    ("白鱲", "Gymnocranius griseus"),
    ("星鱸", "Lateolabrax japonicus"),
    ("盲曹", "Lates calcarifer"),
    ("紅鮋", "Chelidonichthys lucerna"),
    ("泥鯭", "Siganus canaliculatus"),
    ("牙帶", "Lepidopus caudatus"),
    ("黃花魚", "Larimichthys crocea"),
    ("沙鑽", "Sillago sihama"),
    ("魷魚", "Loligo vulgaris"),
    ("鯆魚", "Dasyatis pastinaca"),
    ("左口", "Paralichthys olivaceus"),
    ("雞魚", "Pomadasys kaakan"),
    ("細鱗", "Cheilodactylus zonatus"),
    ("青衣", "Halichoeres hortulanus"),
    ("紅杉", "Priacanthus macracanthus"),
    ("馬友", "Eleutheronema tetradactylum"),
    ("烏頭", "Mugil cephalus"),
    ("金古", "Gnathanodon speciosus"),
    ("梳羅", "Sphyraena barracuda"),
    ("三鬚", "Plectorhinchus cinctus"),
    ("赤筆", "Mullus barbatus"),
    ("剝皮魚", "Stephanolepis hispidus"),
    ("雞泡魚", "Takifugu rubripes"),
    ("鱸魚", "Lateolabrax japonicus"),
    ("牛鰍", "Conger conger"),
    ("門鱔", "Muraenesox cinereus"),
    ("石狗公", "Scorpaena notata"),
    ("黃鰭鮪", "Thunnus albacares"),
    ("杉斑", "Epinephelus areolatus"),
    ("坑鰜", "Cheilinus trilobatus"),
    ("黃衣", "Seriola lalandi"),
    ("黑毛", "Acanthurus nigrofuscus"),
    ("龍躉", "Epinephelus lanceolatus"),
    ("皇帝魚", "Lethrinus nebulosus"),
    ("紅曹", "Lutjanus erythropterus"),
    ("金鼓", "Siganus guttatus"),
    ("石蚌", "Alectis indica"),
    ("飛魚", "Exocoetus volitans"),
    ("海鱺", "Rachycentron canadum"),
    ("水針", "Tylosurus acus"),
    ("墨魚", "Sepia officinalis"),
    ("八爪魚", "Octopus vulgaris"),
    ("瀨尿蝦", "Oratosquilla oratoria"),
    ("花蟹", "Portunus pelagicus"),
    ("牛屎", "Acanthopagrus butcheri"),
    ("白𩶘", "Rhabdosargus sarba"),
    ("金絲䱽", "Nemipterus hexodon"),
    ("花鱸", "Oplegnathus fasciatus"),
    ("石釘", "Sebastes steindachneri"),
    ("黃祥", "Caesio cuning"),
    ("白杉", "Epinephelus akaara"),
]

def search_inaturalist(query):
    """Search iNaturalist for photos of a species."""
    url = f"https://api.inaturalist.org/v1/taxa?q={urllib.parse.quote(query)}&rank=species&per_page=1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fishing-hk-bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        if data.get("total_results", 0) > 0:
            taxon = data["results"][0]
            taxon_id = taxon["id"]
            # Get a photo for this taxon
            photo_url = f"https://api.inaturalist.org/v1/taxa/{taxon_id}?photo_license=cc-by"
            req2 = urllib.request.Request(photo_url, headers={"User-Agent": "fishing-hk-bot/1.0"})
            with urllib.request.urlopen(req2, timeout=10) as r2:
                data2 = json.loads(r2.read())
            if data2.get("results") and data2["results"][0].get("default_photo"):
                photo = data2["results"][0]["default_photo"]
                if photo.get("medium_url"):
                    return photo["medium_url"]
                elif photo.get("url"):
                    return photo["url"]
    except Exception as e:
        pass
    return ""

# Try a few fish
for name, sci in FISH[:10]:  # Test first 10
    # Try scientific name first
    img = search_inaturalist(sci)
    if not img:
        img = search_inaturalist(name)
    status = "✅" if img else "❌"
    print(f"{status} {name}: {img[:100] if img else 'NO IMAGE'}")
    time.sleep(1)
