#!/usr/bin/env python3
"""Generate fully static HTML fishing page with pre-rendered data."""
import json, urllib.request, datetime

HK_LAT, HK_LON = "22.3193", "114.1694"

def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read())

print("Fetching...")
weather = fetch(f"https://api.open-meteo.com/v1/forecast?latitude={HK_LAT}&longitude={HK_LON}&hourly=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max&timezone=Asia/Hong_Kong&forecast_days=3")
marine = fetch(f"https://marine-api.open-meteo.com/v1/marine?latitude={HK_LAT}&longitude={HK_LON}&hourly=wave_height,wave_direction,wind_wave_height,swell_wave_height&daily=wave_height_max,wave_direction_dominant&timezone=Asia/Hong_Kong")
today_s = datetime.date.today().strftime('%Y%m%d')
tide = fetch(f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?station=1617760&begin_date={today_s}&end_date={today_s}&product=predictions&datum=MLLW&units=metric&time_zone=gmt&format=json")

now = datetime.datetime.now()
hour = now.hour
times = weather['hourly']['time']
idx = next((i for i,t in enumerate(times) if t.startswith(today_s) and int(t[11:13])>=hour), 0)

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
if tide.get('predictions'):
    vals = [float(p['v']) for p in tide['predictions'][:288]]
    tmin, tmax = min(vals), max(vals)
    cur_idx = min(len(vals)-1, hour * 12)
    cur_val = vals[cur_idx]
    tide_info = f"最高潮 {tmax:.2f}m · 最低潮 {tmin:.2f}m · 目前水位 {cur_val:.2f}m"

# Daily forecast
days = ["星期日","星期一","星期二","星期三","星期四","星期五","星期六"]
daily_rows = ""
for i in range(min(3, len(weather['daily']['time']))):
    d = datetime.datetime.strptime(weather['daily']['time'][i], '%Y-%m-%d')
    tmax = weather['daily']['temperature_2m_max'][i]
    tmin = weather['daily']['temperature_2m_min'][i]
    wmax = weather['daily']['wind_speed_10m_max'][i]
    wmax_bf = min(12, round(wmax / 10))
    wavemax = marine['daily']['wave_height_max'][i]
    daily_rows += f"<div class='fcast-row'><span class='fw600'>{d.month}/{d.day}({days[d.weekday()]})</span><span>{tmin:.0f}-{tmax:.0f}°C</span><span>💨{wmax_bf}級</span><span>🌊{wavemax:.2f}m</span></div>"

# Fish
fish_data = [
    {"n":"石斑","e":"Grouper","s":"30-100cm","se":"全年","d":"中級"},
    {"n":"黃腳鱲","e":"Yellowfin Bream","s":"20-50cm","se":"秋冬","d":"初級"},
    {"n":"黑鱲","e":"Black Bream","s":"20-45cm","se":"冬季","d":"初級"},
    {"n":"紅鮋","e":"Red Gurnard","s":"15-35cm","se":"夏秋","d":"初級"},
    {"n":"泥鯭","e":"Rabbitfish","s":"15-30cm","se":"夏季","d":"初級"},
    {"n":"牙帶","e":"Ribbonfish","s":"50-120cm","se":"秋冬","d":"進階"},
    {"n":"黃花魚","e":"Yellow Croaker","s":"20-50cm","se":"春季","d":"進階"},
    {"n":"沙鑽","e":"Sand Whiting","s":"15-30cm","se":"全年","d":"初級"},
    {"n":"立魚","e":"Sea Bream","s":"20-60cm","se":"秋冬季","d":"初級"},
    {"n":"火點","e":"Spotty Grouper","s":"20-40cm","se":"夏季","d":"中級"},
    {"n":"左口","e":"Flatfish","s":"20-50cm","se":"全年","d":"中級"},
    {"n":"星鱸","e":"Spotted Sea Bass","s":"30-80cm","se":"秋冬","d":"中級"},
    {"n":"魷魚","e":"Squid","s":"15-40cm","se":"夏秋","d":"初級"},
    {"n":"真鯛","e":"Red Sea Bream","s":"25-60cm","se":"冬季","d":"進階"},
    {"n":"鯆魚","e":"Ray","s":"50-150cm","se":"夏秋","d":"進階"},
    {"n":"黃鰭鮪","e":"Yellowfin Tuna","s":"50-200cm","se":"夏季","d":"專家"},
]
fish_rows = ""
for f in fish_data:
    fish_rows += f"<div class='fish'><div>🐟</div><div class='fn'>{f['n']}</div><div class='ft'>{f['e']}<br>{f['s']} · {f['se']} · {f['d']}</div></div>"

html = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>🐟 香港釣魚資訊站 - by 小婷</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0a1628;color:#e0e8f0;padding:16px;max-width:800px;margin:0 auto}}
h1{{text-align:center;font-size:22px;padding:16px;background:linear-gradient(135deg,#0a3d62,#0d5a7a);border-radius:14px;margin-bottom:16px}}
.card{{background:#0f2a45;border-radius:14px;padding:18px;margin-bottom:14px;border:1px solid #1a3a5a}}
.ct{{font-size:15px;font-weight:600;margin-bottom:10px;color:#3dc1d3}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}}
.item{{background:rgba(10,61,98,0.4);border-radius:12px;padding:14px;text-align:center}}
.item .ic{{font-size:28px}}
.item .lb{{font-size:12px;color:#8899aa;margin:4px 0}}
.item .vl{{font-size:20px;font-weight:700;color:#fff}}
.item .sb{{font-size:11px;color:#8899aa}}
.score{{text-align:center;font-size:42px;font-weight:700;margin:10px 0}}
.bar{{display:flex;gap:4px;margin:12px 0}}
.bar div{{flex:1;height:6px;border-radius:3px;background:#1a3a5a}}
.bar .ok{{background:#3dc1d3}}
.sc{{font-size:13px;color:#8899aa;line-height:1.8;text-align:center}}
.fcast-row{{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:14px}}
.fw600{{font-weight:600}}
.fish-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.fish{{background:rgba(10,61,98,0.3);border-radius:10px;padding:12px;text-align:center;border:1px solid #1a3a5a}}
.fish .fn{{font-size:15px;font-weight:600;margin:4px 0}}
.fish .ft{{font-size:11px;color:#8899aa;line-height:1.4}}
.nav{{text-align:center;margin:16px 0;display:flex;gap:8px;justify-content:center}}
.nav a{{flex:1;padding:10px;background:#0f2a45;border-radius:20px;color:#3dc1d3;text-decoration:none;font-size:14px;border:1px solid #1a3a5a;text-align:center}}
.footer{{text-align:center;font-size:12px;color:#8899aa;padding:20px;line-height:1.6}}
@media(min-width:600px){{.grid{{grid-template-columns:1fr 1fr 1fr}}.fish-grid{{grid-template-columns:1fr 1fr 1fr 1fr}}}}
</style>
</head>
<body>

<h1>🐟 香港釣魚資訊站<br><span style="font-size:14px;color:#8899aa">by 小婷 · {now.year}/{now.month}/{now.day}</span></h1>

<div class="nav">
  <a href="#weather">🌤️ 天氣</a>
  <a href="#fish">🐟 魚種</a>
  <a href="#catches">📝 記錄</a>
</div>

<div class="card" id="weather">
  <div class="ct">🌤️ 即時天氣 ({hour}:00)</div>
  <div class="grid">
    <div class="item"><div class="ic">🌡️</div><div class="lb">氣溫</div><div class="vl">{temp:.1f}°C</div></div>
    <div class="item"><div class="ic">💨</div><div class="lb">風力</div><div class="vl">{bf}級</div><div class="sb">{bf_name}</div></div>
    <div class="item"><div class="ic">🧭</div><div class="lb">風向</div><div class="vl">{windDir}</div><div class="sb">{windS:.0f} km/h</div></div>
    <div class="item"><div class="ic">💥</div><div class="lb">陣風</div><div class="vl">{gust:.0f} km/h</div></div>
    <div class="item"><div class="ic">🌊</div><div class="lb">浪高</div><div class="vl">{waveH:.2f}m</div><div class="sb">{ss}</div></div>
    <div class="item"><div class="ic">〰️</div><div class="lb">湧浪</div><div class="vl">{swell:.2f}m</div><div class="sb">風浪 {windWave:.2f}m</div></div>
  </div>
</div>

<div class="card">
  <div class="ct">🎯 釣魚指數</div>
  <div class="score" style="color:{score_color}">{score}/100</div>
  <div class="bar">{bars}</div>
  <div class="sc" style="margin-bottom:6px">{score_msg}</div>
  <div class="sc">風力{bf}級 · 浪高{waveH:.2f}m · 氣溫{temp:.1f}°C</div>
</div>

<div class="card">
  <div class="ct">🌊 潮汐預報</div>
  <div style="font-size:14px;color:#8899aa;text-align:center">{tide_info}</div>
</div>

<div class="card">
  <div class="ct">📅 未來三天</div>
  {daily_rows}
</div>

<div class="card" id="fish">
  <div class="ct">🐟 香港魚種圖鑑</div>
  <div class="fish-grid">{fish_rows}</div>
</div>

<div class="card" id="catches">
  <div class="ct">📝 釣獲記錄</div>
  <div style="font-size:14px;text-align:center;padding:20px;color:#8899aa">
    記錄功能需要用 browser 嘅 localStorage<br>
    請用互動版本記錄 🎣
  </div>
</div>

<div class="footer">
  資料來源：Open-Meteo · NOAA Tides<br>
  由小婷為 Jay 製作 🎣
</div>

</body>
</html>'''

with open('/opt/data/fishing-hk/釣魚資訊站.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done! {len(html)} bytes")
