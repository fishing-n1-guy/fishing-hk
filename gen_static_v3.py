#!/usr/bin/env python3
"""Generate fully static HTML with correct timezone handling."""
import json, urllib.request, datetime

HK_LAT, HK_LON = "22.3193", "114.1694"

def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read())

print("Fetching...")
weather = fetch(f"https://api.open-meteo.com/v1/forecast?latitude={HK_LAT}&longitude={HK_LON}&hourly=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max&timezone=Asia/Hong_Kong&forecast_days=3")
marine = fetch(f"https://marine-api.open-meteo.com/v1/marine?latitude={HK_LAT}&longitude={HK_LON}&hourly=wave_height,wave_direction,wind_wave_height,swell_wave_height&daily=wave_height_max,wave_direction_dominant&timezone=Asia/Hong_Kong")

# Get Hong Kong time
hk_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
today_hk = hk_now.strftime('%Y-%m-%d')  # Format: 2026-06-22
hour_hk = hk_now.hour
date_str = hk_now.strftime('%Y/%m/%d')

# Find current hour in API data
times = weather['hourly']['time']
idx = 0
for i, t in enumerate(times):
    if t.startswith(today_hk) and int(t[11:13]) >= hour_hk:
        idx = i
        break

# Use the found hour for display
display_hour = int(times[idx][11:13])

temp = weather['hourly']['temperature_2m'][idx]
windS = weather['hourly']['wind_speed_10m'][idx]
windD = weather['hourly']['wind_direction_10m'][idx]
gust = weather['hourly']['wind_gusts_10m'][idx]
waveH = marine['hourly']['wave_height'][idx]
swell = marine['hourly']['swell_wave_height'][idx]
windWave = marine['hourly']['wind_wave_height'][idx]

WIND_DIR = ["北","東北偏北","東北","東北偏東","東","東南偏東","東南","東南偏南","南","西南偏南","西南","西南偏西","西","西北偏西","西北","西北偏北"]
windDir = WIND_DIR[round(windD/22.5)%16]
bf = min(12, round(windS / 10))
bf_names = ["無風","軟風","輕風","微風","和風","清風","強風","疾風","大風","烈風","暴風","狂風","颶風"]
bf_name = bf_names[bf]

ss = "平靜"
if waveH >= 0.1: ss = "小浪"
if waveH >= 0.5: ss = "中浪"
if waveH >= 1.25: ss = "大浪"
if waveH >= 2.5: ss = "非常大浪"
if waveH >= 4: ss = "巨浪"

# Fishing score
score = 50
if bf <= 3: score += 25
elif bf <= 5: score += 10
elif bf <= 7: score -= 10
else: score -= 30
if waveH < 0.3: score += 10
elif waveH < 1: score += 5
elif waveH > 2: score -= 20
if 22 <= temp <= 30: score += 15
elif temp < 15 or temp > 35: score -= 10
score = max(0, min(100, score))

score_color = "#2ecc71" if score >= 65 else "#f39c12" if score >= 45 else "#e74c3c"
score_msg = "🏆 極佳！今日好適合釣魚！" if score >= 80 else "👍 唔錯，可以出發" if score >= 65 else "👌 一般，可以一試" if score >= 45 else "😐 麻麻地，考慮清楚" if score >= 25 else "😢 唔係好適合釣魚"
bars = "".join('<div class="ok"></div>' if i*10 < score else '<div></div>' for i in range(10))

# Tide
tide_info = ""
try:
    today_ymd = hk_now.strftime('%Y%m%d')
    tide = fetch(f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?station=1617760&begin_date={today_ymd}&end_date={today_ymd}&product=predictions&datum=MLLW&units=metric&time_zone=gmt&format=json")
    if tide.get('predictions'):
        vals = [float(p['v']) for p in tide['predictions'][:288]]
        tmin, tmax = min(vals), max(vals)
        hk_offset_hours = 8
        tide_idx = min(len(vals)-1, hour_hk * 12 + hk_offset_hours * 0)
        cur_val = vals[min(len(vals)-1, hour_hk * 12)]
        tide_info = f"最高潮 {tmax:.2f}m · 最低潮 {tmin:.2f}m · 目前 {cur_val:.2f}m"
    else:
        tide_info = "潮汐資料暫未能載入"
except:
    tide_info = "潮汐資料暫未能載入"

# Daily forecast
days = ["星期日","星期一","星期二","星期三","星期四","星期五","星期六"]
daily_rows = ""
for i in range(min(3, len(weather['daily']['time']))):
    d = datetime.datetime.strptime(weather['daily']['time'][i], '%Y-%m-%d')
    tmax = weather['daily']['temperature_2m_max'][i]
    tmin = weather['daily']['temperature_2m_min'][i]
    wmax = weather['daily']['wind_speed_10m_max'][i]
    wmax_bf = min(12, round(wmax / 10))
    wavemax = marine['daily']['wave_height_max'][i] if i < len(marine['daily']['wave_height_max']) else 0
    daily_rows += f"<div class='fr'><b>{d.month}/{d.day}({days[d.weekday()]})</b><span>{tmin:.0f}-{tmax:.0f}°C</span><span>💨{wmax_bf}級</span><span>🌊{wavemax:.2f}m</span></div>"

# Fish
fish_data = [
    ("石斑","Grouper","30-100cm","全年","中級"),
    ("黃腳鱲","Yellowfin Bream","20-50cm","秋冬","初級"),
    ("黑鱲","Black Bream","20-45cm","冬季","初級"),
    ("紅鮋","Red Gurnard","15-35cm","夏秋","初級"),
    ("泥鯭","Rabbitfish","15-30cm","夏季","初級"),
    ("牙帶","Ribbonfish","50-120cm","秋冬","進階"),
    ("黃花魚","Yellow Croaker","20-50cm","春季","進階"),
    ("沙鑽","Sand Whiting","15-30cm","全年","初級"),
    ("立魚","Sea Bream","20-60cm","秋冬季","初級"),
    ("火點","Spotty Grouper","20-40cm","夏季","中級"),
    ("左口","Flatfish","20-50cm","全年","中級"),
    ("星鱸","Spotted Sea Bass","30-80cm","秋冬","中級"),
    ("魷魚","Squid","15-40cm","夏秋","初級"),
    ("真鯛","Red Sea Bream","25-60cm","冬季","進階"),
    ("鯆魚","Ray","50-150cm","夏秋","進階"),
    ("黃鰭鮪","Yellowfin Tuna","50-200cm","夏季","專家"),
]
fish_rows = ""
for n, e, s, se, d in fish_data:
    fish_rows += f"<div class='fi'><div>🐟</div><div class='fn'>{n}</div><div class='ft'>{e}<br>{s} · {se} · {d}</div></div>"

html = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🐟 香港釣魚資訊站 - by 小婷</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0a1628;color:#e0e8f0;padding:16px;max-width:800px;margin:0 auto}}
h1{{text-align:center;font-size:20px;padding:16px;background:linear-gradient(135deg,#0a3d62,#0d5a7a);border-radius:14px;margin-bottom:14px}}
.card{{background:#0f2a45;border-radius:14px;padding:16px;margin-bottom:12px;border:1px solid #1a3a5a}}
.ct{{font-size:15px;font-weight:600;margin-bottom:10px;color:#3dc1d3}}
.g{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.it{{background:rgba(10,61,98,0.4);border-radius:10px;padding:12px;text-align:center}}
.ic{{font-size:24px}} .lb{{font-size:11px;color:#8899aa;margin:3px 0}} .vl{{font-size:22px;font-weight:700;color:#fff}} .sb{{font-size:11px;color:#8899aa}}
.scr{{text-align:center;font-size:42px;font-weight:700;margin:10px 0}}
.br{{display:flex;gap:4px;margin:12px 0}} .br div{{flex:1;height:6px;border-radius:3px;background:#1a3a5a}} .br .ok{{background:#3dc1d3}}
.sc{{font-size:13px;color:#8899aa;text-align:center;line-height:1.6}}
.fr{{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:13px}}
.fg{{display:grid;grid-template-columns:1fr 1fr;gap:6px}}
.fi{{background:rgba(10,61,98,0.3);border-radius:10px;padding:10px;text-align:center;border:1px solid #1a3a5a}}
.fn{{font-size:15px;font-weight:600;margin:3px 0}} .ft{{font-size:10px;color:#8899aa;line-height:1.4}}
.nav{{display:flex;gap:6px;margin:14px 0}}
.nav a{{flex:1;padding:8px;background:#0f2a45;border-radius:20px;color:#3dc1d3;text-decoration:none;font-size:13px;text-align:center;border:1px solid #1a3a5a}}
.ftr{{text-align:center;font-size:11px;color:#8899aa;padding:16px;line-height:1.5}}
@media(min-width:600px){{.g{{grid-template-columns:1fr 1fr 1fr}}.fg{{grid-template-columns:1fr 1fr 1fr 1fr}}}}
</style>
</head>
<body>

<h1>🐟 香港釣魚資訊站<br><span style="font-size:13px;color:#8899aa">by 小婷 · {date_str}</span></h1>

<div class="nav">
  <a href="#w">🌤️ 天氣</a>
  <a href="#f">🐟 魚種</a>
  <a href="#c">📝 記錄</a>
</div>

<div class="card" id="w">
  <div class="ct">🌤️ 即時天氣 ({display_hour}:00 香港時間)</div>
  <div class="g">
    <div class="it"><div class="ic">🌡️</div><div class="lb">氣溫</div><div class="vl">{temp:.1f}°C</div></div>
    <div class="it"><div class="ic">💨</div><div class="lb">風力</div><div class="vl">{bf}級</div><div class="sb">{bf_name}</div></div>
    <div class="it"><div class="ic">🧭</div><div class="lb">風向</div><div class="vl">{windDir}</div><div class="sb">{windS:.0f}km/h</div></div>
    <div class="it"><div class="ic">💥</div><div class="lb">陣風</div><div class="vl">{gust:.0f}</div><div class="sb">km/h</div></div>
    <div class="it"><div class="ic">🌊</div><div class="lb">浪高</div><div class="vl">{waveH:.2f}m</div><div class="sb">{ss}</div></div>
    <div class="it"><div class="ic">〰️</div><div class="lb">湧浪</div><div class="vl">{swell:.2f}m</div><div class="sb">風浪{windWave:.2f}m</div></div>
  </div>
</div>

<div class="card">
  <div class="ct">🎯 釣魚指數</div>
  <div class="scr" style="color:{score_color}">{score}/100</div>
  <div class="br">{"".join('<div class="ok"></div>' if i*10<score else '<div></div>' for i in range(10))}</div>
  <div class="sc" style="margin-bottom:6px">{score_msg}</div>
  <div class="sc">風力 {bf}級 · 浪高 {waveH:.2f}m · 氣溫 {temp:.1f}°C</div>
</div>

<div class="card">
  <div class="ct">🌊 潮汐預報</div>
  <div style="font-size:14px;color:#8899aa;text-align:center;padding:6px">{tide_info}</div>
</div>

<div class="card">
  <div class="ct">📅 未來三天預測</div>
  {daily_rows}
</div>

<div class="card" id="f">
  <div class="ct">🐟 香港魚種圖鑑</div>
  <div class="fg">{fish_rows}</div>
</div>

<div class="card" id="c">
  <div class="ct">📝 釣獲記錄</div>
  <div style="font-size:14px;text-align:center;padding:20px;color:#8899aa">
    記錄功能需要 browser 嘅 localStorage<br>
    請用互動版本記錄 🎣
  </div>
</div>

<div class="ftr">
  資料來源：Open-Meteo · NOAA Tides<br>
  由小婷為 Jay 製作 🎣
</div>

</body>
</html>'''

with open('/opt/data/fishing-hk/釣魚資訊站.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done! {len(html)} bytes - HK time: {hk_now}")
