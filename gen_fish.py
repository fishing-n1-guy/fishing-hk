#!/usr/bin/env python3
"""Generate fish species data for HK fishing site."""
import json

FISH = [
    # (Chinese, English, Size, Season, Difficulty, ImageURL)
    
    # 石斑類 Groupers
    ("石斑", "Grouper", "30-100cm", "全年", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Epinephelus_marginatus.jpg/200px-Epinephelus_marginatus.jpg"),
    ("芝麻斑", "Brown-marbled Grouper", "30-80cm", "夏秋", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Epinephelus_fuscoguttatus.jpg/200px-Epinephelus_fuscoguttatus.jpg"),
    ("青斑", "Orange-spotted Grouper", "25-60cm", "夏季", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Epinephelus_coioides.jpg/200px-Epinephelus_coioides.jpg"),
    ("東星斑", "Coral Trout", "20-60cm", "夏季", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Plectropomus_leopardus.jpg/200px-Plectropomus_leopardus.jpg"),
    ("紅斑", "Red Grouper", "20-50cm", "秋冬", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Epinephelus_marginatus_2.jpg/200px-Epinephelus_marginatus_2.jpg"),
    ("火點", "Spotty Grouper", "20-40cm", "夏季", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Epinephelus_merra.jpg/200px-Epinephelus_merra.jpg"),
    
    # 立魚類 Breams
    ("黃腳鱲", "Yellowfin Bream", "20-50cm", "秋冬", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Acanthopagrus_latus.jpg/200px-Acanthopagrus_latus.jpg"),
    ("黑鱲", "Black Bream", "20-45cm", "冬季", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Acanthopagrus_schlegelii.jpg/200px-Acanthopagrus_schlegelii.jpg"),
    ("立魚(普通)", "Sea Bream", "20-60cm", "秋冬季", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Pagrus_pagrus.jpg/200px-Pagrus_pagrus.jpg"),
    ("真鯛", "Red Sea Bream", "25-60cm", "冬季", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Pagrus_major.jpg/200px-Pagrus_major.jpg"),
    ("白鱲", "White Snapper", "25-50cm", "秋冬", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Gymnocranius_griseus.jpg/200px-Gymnocranius_griseus.jpg"),
    
    # 鱸魚類
    ("星鱸", "Spotted Sea Bass", "30-80cm", "秋冬", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Lateolabrax_japonicus.jpg/200px-Lateolabrax_japonicus.jpg"),
    ("盲曹", "Barramundi", "30-100cm", "夏季", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Barramundi_%2836945357715%29.jpg/200px-Barramundi_%2836945357715%29.jpg"),
    
    # 其他常見魚類
    ("紅鮋", "Red Gurnard", "15-35cm", "夏秋", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Chelidonichthys_lucerna.jpg/200px-Chelidonichthys_lucerna.jpg"),
    ("泥鯭", "Rabbitfish", "15-30cm", "夏季", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Siganus_canaliculatus.jpg/200px-Siganus_canaliculatus.jpg"),
    ("牙帶", "Ribbonfish", "50-120cm", "秋冬", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Lepidopus_caudatus.jpg/200px-Lepidopus_caudatus.jpg"),
    ("黃花魚", "Yellow Croaker", "20-50cm", "春季", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Larimichthys_crocea.jpg/200px-Larimichthys_crocea.jpg"),
    ("沙鑽", "Sand Whiting", "15-30cm", "全年", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Sillago_sihama.jpg/200px-Sillago_sihama.jpg"),
    ("魷魚", "Squid", "15-40cm", "夏秋", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Loligo_vulgaris.jpg/200px-Loligo_vulgaris.jpg"),
    ("鯆魚", "Ray", "50-150cm", "夏秋", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Dasyatis_pastinaca.jpg/200px-Dasyatis_pastinaca.jpg"),
    ("左口", "Flatfish", "20-50cm", "全年", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Paralichthys_olivaceus.jpg/200px-Paralichthys_olivaceus.jpg"),
    
    # 更多魚種
    ("雞魚", "Javelin Grunter", "20-40cm", "夏秋", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Pomadasys_kaakan.jpg/200px-Pomadasys_kaakan.jpg"),
    ("細鱗", "Red Morwong", "20-50cm", "冬季", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Cheilodactylus_zonatus.jpg/200px-Cheilodactylus_zonatus.jpg"),
    ("青衣", "Green Wrasse", "20-50cm", "夏季", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Halichoeres_hortulanus.jpg/200px-Halichoeres_hortulanus.jpg"),
    ("紅杉", "Red Bigeye", "15-30cm", "全年", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Priacanthus_macracanthus.jpg/200px-Priacanthus_macracanthus.jpg"),
    ("大眼雞", "Bigeye", "15-30cm", "全年", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Heteropriacanthus_cruentatus.jpg/200px-Heteropriacanthus_cruentatus.jpg"),
    ("馬友", "Fourfinger Threadfin", "30-80cm", "夏季", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Eleutheronema_tetradactylum.jpg/200px-Eleutheronema_tetradactylum.jpg"),
    ("烏頭", "Grey Mullet", "20-60cm", "秋冬", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Mugil_cephalus.jpg/200px-Mugil_cephalus.jpg"),
    ("金古", "Golden Trevally", "20-60cm", "夏季", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Gnathanodon_speciosus.jpg/200px-Gnathanodon_speciosus.jpg"),
    ("池魚", "Horse Mackerel", "15-30cm", "全年", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Trachurus_trachurus.jpg/200px-Trachurus_trachurus.jpg"),
    ("梳羅", "Barracuda", "40-120cm", "夏季", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Barracuda_%28Sphyraena_barracuda%29.jpg/200px-Barracuda_%28Sphyraena_barracuda%29.jpg"),
    ("三鬚", "Three-lined Grunt", "15-30cm", "全年", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Plectorhinchus_cinctus.jpg/200px-Plectorhinchus_cinctus.jpg"),
    ("赤筆", "Red Mullet", "15-30cm", "春季", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Mullus_barbatus.jpg/200px-Mullus_barbatus.jpg"),
    ("剝皮魚", "Filefish", "15-40cm", "冬季", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Stephanolepis_hispidus.jpg/200px-Stephanolepis_hispidus.jpg"),
    ("雞泡魚", "Pufferfish", "10-40cm", "全年", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Takifugu_rubripes.jpg/200px-Takifugu_rubripes.jpg"),
    ("鱸魚", "Japanese Sea Bass", "20-70cm", "秋冬", "中級", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Lateolabrax_japonicus_01.jpg/200px-Lateolabrax_japonicus_01.jpg"),
    ("牛鰍", "Conger Eel", "40-150cm", "全年", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Conger_conger.jpg/200px-Conger_conger.jpg"),
    ("門鱔", "Pike Eel", "50-200cm", "全年", "進階", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Muraenesox_cinereus.jpg/200px-Muraenesox_cinereus.jpg"),
    ("石狗公", "Scorpionfish", "10-25cm", "全年", "初級", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Scorpaena_notata.jpg/200px-Scorpaena_notata.jpg"),
    ("黃鰭鮪", "Yellowfin Tuna", "50-200cm", "夏季", "專家", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Thunnus_albacares.jpg/200px-Thunnus_albacares.jpg"),
]

# Output as JS
print("// 香港魚種資料庫 - 由小婷整理")
print("const FISH = [")
for f in FISH:
    print(f'  {json.dumps(list(f), ensure_ascii=False)},')
print("];")
print(f"// Total: {len(FISH)} species")
