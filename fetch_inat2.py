#!/usr/bin/env python3
"""Batch fetch fish images from iNaturalist API."""
import json, urllib.request, urllib.parse, time

FISH = [
    ("石斑", "Epinephelus marginatus"),
    ("芝麻斑", "Epinephelus fuscoguttatus"),
    ("青斑", "Epinephelus coioides"),
    ("東星斑", "Plectropomus leopardus"),
    ("紅斑", "Epinephelus akaara"),
    ("火點", "Epinephelus merra"),
    ("黃腳鱲", "Acanthopagrus latus"),
    ("黑鱲", "Acanthopagrus schlegelii"),
    ("真鯛", "Pagrus major"),
    ("星鱸", "Lateolabrax japonicus"),
    ("盲曹", "Lates calcarifer"),
    ("紅鮋", "Chelidonichthys lucerna"),
    ("泥鯭", "Siganus canaliculatus"),
    ("黃花魚", "Larimichthys crocea"),
    ("魷魚", "Loligo vulgaris"),
    ("鯆魚", "Dasyatis pastinaca"),
    ("左口", "Paralichthys olivaceus"),
    ("雞魚", "Pomadasys kaakan"),
    ("青衣", "Halichoeres hortulanus"),
    ("馬友", "Eleutheronema tetradactylum"),
    ("烏頭", "Mugil cephalus"),
    ("金古", "Gnathanodon speciosus"),
    ("梳羅", "Sphyraena barracuda"),
    ("雞泡魚", "Takifugu rubripes"),
    ("鱸魚", "Lateolabrax japonicus"),
    ("牛鰍", "Conger conger"),
    ("門鱔", "Muraenesox cinereus"),
    ("石狗公", "Scorpaena notata"),
    ("黃鰭鮪", "Thunnus albacares"),
    ("杉斑", "Epinephelus areolatus"),
    ("衣", "Seriola lalandi"),
    ("龍躉", "Epinephelus lanceolatus"),
    ("皇帝魚", "Lethrinus nebulosus"),
    ("紅曹", "Lutjanus erythropterus"),
    ("金鼓", "Siganus guttatus"),
    ("飛魚", "Exocoetus volitans"),
    ("海鱺", "Rachycentron canadum"),
    ("墨魚", "Sepia officinalis"),
    ("八爪魚", "Octopus vulgaris"),
    ("瀨尿蝦", "Oratosquilla oratoria"),
    ("花蟹", "Portunus pelagicus"),
    ("牛屎", "Acanthopagrus butcheri"),
]

def get_inaturalist_img(sci_name):
    """Search iNaturalist for a taxon and get photo."""
    url = f"https://api.inaturalist.org/v1/taxa?q={urllib.parse.quote(sci_name)}&rank=species&per_page=1&order=desc&order_by=observations_count"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fishing-hk-bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        if data.get("total_results", 0) > 0 and data["results"]:
            taxon = data["results"][0]
            if taxon.get("default_photo") and taxon["default_photo"].get("medium_url"):
                return taxon["default_photo"]["medium_url"]
    except:
        pass
    return ""

print("const FISH_IMG = {")
for cn, sci in FISH:
    img = get_inaturalist_img(sci)
    status = "✅" if img else "❌"
    print(f'  "{cn}": "{img}", // {status}')
    time.sleep(1.5)  # Rate limit
print("};")
