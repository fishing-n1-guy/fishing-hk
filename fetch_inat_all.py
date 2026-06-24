#!/usr/bin/env python3
"""Generate complete fish image map from iNaturalist API."""
import json, urllib.request, urllib.parse, time

# ALL fish species
FISH = [
    ("石斑", "Epinephelus marginatus"),
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
    ("大眼雞", "Heteropriacanthus cruentatus"),
    ("馬友", "Eleutheronema tetradactylum"),
    ("烏頭", "Mugil cephalus"),
    ("金古", "Gnathanodon speciosus"),
    ("池魚", "Trachurus trachurus"),
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
    ("黑鮋", "Sebastiscus marmoratus"),
    ("冚畢", "Trachinotus blochii"),
    ("斑𩶘", "Choerodon schoenleinii"),
    ("海鱺", "Rachycentron canadum"),
    ("水針", "Tylosurus acus"),
    ("沙鯭", "Synodus saurus"),
    ("花利", "Platycephalus indicus"),
    ("金山鯽", "Oreochromis mossambicus"),
    ("塘虱", "Clarias batrachus"),
    ("墨魚", "Sepia officinalis"),
    ("八爪魚", "Octopus vulgaris"),
    ("瀨尿蝦", "Oratosquilla oratoria"),
    ("花蟹", "Portunus pelagicus"),
    ("牛屎(黑鱲)", "Acanthopagrus butcheri"),
    ("黑沙(黑鱲)", "Acanthopagrus schlegelii"),
    ("白𩶘", "Rhabdosargus sarba"),
    ("金絲䱽", "Nemipterus hexodon"),
    ("花鱸", "Oplegnathus fasciatus"),
    ("石釘", "Sebastes steindachneri"),
    ("黑毛", "Acanthurus nigrofuscus"),
    ("龍躉", "Epinephelus lanceolatus"),
    ("皇帝魚", "Lethrinus nebulosus"),
    ("紅曹", "Lutjanus erythropterus"),
    ("金鼓", "Siganus guttatus"),
    ("石蚌", "Alectis indica"),
    ("飛魚", "Exocoetus volitans"),
    ("煙管魚", "Fistularia commersonii"),
    ("藍旗𩶘", "Pagrus pagrus"),
    ("紅𩶘", "Pagellus erythrinus"),
    ("青龍", "Halichoeres hortulanus"),
    ("黃祥", "Caesio cuning"),
    ("白杉", "Epinephelus summana"),
    ("花頭梅", "Hypodytes rubicundus"),
    ("白花", "Pennahia argentata"),
    ("紅衫", "Nemipterus virgatus"),
]

results = {}
print("Fetching iNaturalist images...")
for cn, sci in FISH:
    url = f"https://api.inaturalist.org/v1/taxa?q={urllib.parse.quote(sci)}&rank=species&per_page=1&order=desc&order_by=observations_count"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fishing-hk-bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        if data.get("total_results", 0) > 0 and data["results"]:
            taxon = data["results"][0]
            if taxon.get("default_photo") and taxon["default_photo"].get("medium_url"):
                results[cn] = taxon["default_photo"]["medium_url"]
                print(f"  ✅ {cn}")
            else:
                print(f"  ❌ {cn} - no photo")
        else:
            print(f"  ❌ {cn} - not found")
    except Exception as e:
        print(f"  ❌ {cn} - {e}")
    time.sleep(1.5)

# Output as JS
print(f"\n\n// Total: {len(results)}/{len(FISH)} species with images")
print("const FISH_IMG = {")
for cn, img in sorted(results.items()):
    print(f'  "{cn}": "{img}",')
print("};")
