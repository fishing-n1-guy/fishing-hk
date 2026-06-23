#!/usr/bin/env python3
"""Generate hybrid HTML: pre-rendered initial data + live JS updates."""
import json, urllib.request, datetime

HK_LAT, HK_LON = "22.3193", "114.1694"

def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read())

print("Fetching initial data...")
weather = fetch(f"https://api.open-meteo.com/v1/forecast?latitude={HK_LAT}&longitude={HK_LON}&hourly=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max&timezone=Asia/Hong_Kong&forecast_days=3")
marine = fetch(f"https://marine-api.open-meteo.com/v1/marine?latitude={HK_LAT}&longitude={HK_LON}&hourly=wave_height,wave_direction,wind_wave_height,swell_wave_height&daily=wave_height_max,wave_direction_dominant&timezone=Asia/Hong_Kong")

# Pre-encode data for embedding
weather_json = json.dumps(weather, ensure_ascii=False)
marine_json = json.dumps(marine, ensure_ascii=False)

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
.refresh{{text-align:center;font-size:12px;color:#3dc1d3;padding:8px;cursor:pointer}}
.refresh:hover{{text-decoration:underline}}
</style>
</head>
<body>

<h1>🐟 香港釣魚資訊站<br><span style="font-size:13px;color:#8899aa">by 小婷 · <span id="updateTime">載入中</span></span></h1>

<div class="nav">
  <a href="#w">🌤️ 天氣</a>
  <a href="#f">🐟 魚種</a>
  <a href="#c">📝 記錄</a>
</div>

<div class="card" id="w">
  <div class="ct">🌤️ 即時天氣</div>
  <div id="weatherGrid" class="g">
    <div class="it"><div class="ic">🌡️</div><div class="lb">氣溫</div><div class="vl" id="wTemp">--</div></div>
    <div class="it"><div class="ic">💨</div><div class="lb">風力</div><div class="vl" id="wWind">--</div><div class="sb" id="wWindName">--</div></div>
    <div class="it"><div class="ic">🧭</div><div class="lb">風向</div><div class="vl" id="wWindDir">--</div><div class="sb" id="wWindSpeed">--</div></div>
    <div class="it"><div class="ic">💥</div><div class="lb">陣風</div><div class="vl" id="wGust">--</div><div class="sb">km/h</div></div>
    <div class="it"><div class="ic">🌊</div><div class="lb">浪高</div><div class="vl" id="wWave">--</div><div class="sb" id="wWaveState">--</div></div>
    <div class="it"><div class="ic">〰️</div><div class="lb">湧浪</div><div class="vl" id="wSwell">--</div><div class="sb" id="wWindWave">--</div></div>
  </div>
  <div class="refresh" onclick="refreshWeather()">🔄 點擊更新天氣</div>
</div>

<div class="card" id="scoreCard">
  <div class="ct">🎯 釣魚指數</div>
  <div class="scr" id="scoreVal">--</div>
  <div class="br" id="scoreBars"></div>
  <div class="sc" id="scoreMsg"></div>
</div>

<div class="card" id="forecastCard">
  <div class="ct">📅 未來三天</div>
  <div id="forecastRows"></div>
</div>

<div class="card" id="f">
  <div class="ct">🐟 香港魚種圖鑑</div>
  <div class="fg" id="fishGrid"></div>
</div>

<div class="card" id="c">
  <div class="ct">📝 釣獲記錄</div>
  <div style="font-size:14px;text-align:center;padding:20px;color:#8899aa">
    記錄功能需要 browser 嘅 localStorage<br>
    記錄你嘅釣獲 🎣
  </div>
</div>

<div class="ftr">
  資料來源：Open-Meteo<br>
  由小婷為 Jay 製作 🎣<br>
  <span style="font-size:10px">天氣資料每次開頁自動更新</span>
</div>

<script>
// Pre-embedded data (fallback if fetch fails)
const PRE_WEATHER = {weather_json};
const PRE_MARINE = {marine_json};
const FISH_DATA = [
  ["石斑","Grouper","30-100cm","全年","中級"],["黃腳鱲","Yellowfin Bream","20-50cm","秋冬","初級"],
  ["黑鱲","Black Bream","20-45cm","冬季","初級"],["紅鮋","Red Gurnard","15-35cm","夏秋","初級"],
  ["泥鯭","Rabbitfish","15-30cm","夏季","初級"],["牙帶","Ribbonfish","50-120cm","秋冬","進階"],
  ["黃花魚","Yellow Croaker","20-50cm","春季","進階"],["沙鑽","Sand Whiting","15-30cm","全年","初級"],
  ["立魚","Sea Bream","20-60cm","秋冬季","初級"],["火點","Spotty Grouper","20-40cm","夏季","中級"],
  ["左口","Flatfish","20-50cm","全年","中級"],["星鱸","Spotted Sea Bass","30-80cm","秋冬","中級"],
  ["魷魚","Squid","15-40cm","夏秋","初級"],["真鯛","Red Sea Bream","25-60cm","冬季","進階"],
  ["鯆魚","Ray","50-150cm","夏秋","進階"],["黃鰭鮪","Yellowfin Tuna","50-200cm","夏季","專家"]
];

const WIND_DIR = ["北","東北偏北","東北","東北偏東","東","東南偏東","東南","東南偏南","南","西南偏南","西南","西南偏西","西","西北偏西","西北","西北偏北"];
const BF_NAMES = ["無風","軟風","輕風","微風","和風","清風","強風","疾風","大風","烈風","暴風","狂風","颶風"];

// Render fish
(function() {{
  const g = document.getElementById('fishGrid');
  g.innerHTML = FISH_DATA.map(f => 
    '<div class="fi"><div>🐟</div><div class="fn">'+f[0]+'</div><div class="ft">'+f[1]+'<br>'+f[2]+' · '+f[3]+' · '+f[4]+'</div></div>'
  ).join('');
}})();

function renderWeather(data, marine) {{
  const times = data.hourly.time;
  const hkNow = new Date();
  hkNow.setHours(hkNow.getHours() + 8); // UTC to HKT
  const h = hkNow.getUTCHours();
  const today = hkNow.toISOString().slice(0,10);
  
  let idx = 0;
  for(let i=0;i<times.length;i++) {{
    if(times[i].startsWith(today) && parseInt(times[i].slice(11,13)) >= h) {{ idx = i; break; }}
  }}
  
  const temp = data.hourly.temperature_2m[idx];
  const windS = data.hourly.wind_speed_10m[idx];
  const windD = data.hourly.wind_direction_10m[idx];
  const gust = data.hourly.wind_gusts_10m[idx];
  const waveH = marine.hourly.wave_height[idx];
  const swell = marine.hourly.swell_wave_height[idx];
  const windWave = marine.hourly.wind_wave_height[idx];
  
  const bf = Math.min(12, Math.round(windS / 10));
  const dir = WIND_DIR[Math.round(windD/22.5)%16];
  
  let ss = "平靜";
  if(waveH>=0.1) ss="小浪"; if(waveH>=0.5) ss="中浪"; if(waveH>=1.25) ss="大浪"; if(waveH>=2.5) ss="非常大浪"; if(waveH>=4) ss="巨浪";
  
  document.getElementById('wTemp').textContent = temp.toFixed(1)+'°C';
  document.getElementById('wWind').textContent = bf+'級';
  document.getElementById('wWindName').textContent = BF_NAMES[bf];
  document.getElementById('wWindDir').textContent = dir;
  document.getElementById('wWindSpeed').textContent = windS.toFixed(0)+'km/h';
  document.getElementById('wGust').textContent = gust.toFixed(0);
  document.getElementById('wWave').textContent = waveH.toFixed(2)+'m';
  document.getElementById('wWaveState').textContent = ss;
  document.getElementById('wSwell').textContent = swell.toFixed(2)+'m';
  document.getElementById('wWindWave').textContent = '風浪'+windWave.toFixed(2)+'m';
  
  // Score
  let score = 50;
  if(bf<=3) score+=25; else if(bf<=5) score+=10; else if(bf<=7) score-=10; else score-=30;
  if(waveH<0.3) score+=10; else if(waveH<1) score+=5; else if(waveH>2) score-=20;
  if(temp>=22&&temp<=30) score+=15; else if(temp<15||temp>35) score-=10;
  score = Math.max(0, Math.min(100, score));
  
  const el = document.getElementById('scoreVal');
  el.textContent = score+'/100';
  el.style.color = score>=65?'#2ecc71':score>=45?'#f39c12':'#e74c3c';
  
  document.getElementById('scoreBars').innerHTML = Array(10).fill(0).map((_,i)=>'<div'+(i*10<score?' class="ok"':'')+'></div>').join('');
  
  const msgs = ["😢 唔係好適合釣魚","😐 麻麻地，考慮清楚","👌 一般，可以一試","👍 唔錯，可以出發","🏆 極佳！今日好適合釣魚！"];
  document.getElementById('scoreMsg').textContent = msgs[Math.min(4, Math.floor(score/25))] + '  🌬️'+bf+'級 🌊'+waveH.toFixed(2)+'m 🌡️'+temp.toFixed(1)+'°C';
  
  // Daily forecast
  const days = ["星期日","星期一","星期二","星期三","星期四","星期五","星期六"];
  const fRows = document.getElementById('forecastRows');
  fRows.innerHTML = '';
  for(let i=0;i<Math.min(3,data.daily.time.length);i++) {{
    const d = new Date(data.daily.time[i]+'T12:00:00');
    const tmax = data.daily.temperature_2m_max[i];
    const tmin = data.daily.temperature_2m_min[i];
    const wmax = Math.min(12, Math.round(data.daily.wind_speed_10m_max[i]/10));
    const wavemax = marine.daily.wave_height_max[i]||0;
    fRows.innerHTML += '<div class="fr"><b>'+(d.getMonth()+1)+'/'+d.getDate()+'('+days[d.getDay()]+')</b><span>'+tmin.toFixed(0)+'-'+tmax.toFixed(0)+'°C</span><span>💨'+wmax+'級</span><span>🌊'+wavemax.toFixed(2)+'m</span></div>';
  }}
  
  const now = new Date();
  document.getElementById('updateTime').textContent = 
    now.getFullYear()+'-'+(now.getMonth()+1)+'-'+now.getDate()+' '+
    String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0');
}}

async function refreshWeather() {{
  try {{
    const [w, m] = await Promise.all([
      fetch('https://api.open-meteo.com/v1/forecast?latitude={HK_LAT}&longitude={HK_LON}&hourly=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max&timezone=Asia/Hong_Kong&forecast_days=3').then(r=>r.json()),
      fetch('https://marine-api.open-meteo.com/v1/marine?latitude={HK_LAT}&longitude={HK_LON}&hourly=wave_height,wave_direction,wind_wave_height,swell_wave_height&daily=wave_height_max,wave_direction_dominant&timezone=Asia/Hong_Kong').then(r=>r.json())
    ]);
    renderWeather(w, m);
  }} catch(e) {{
    // Fallback to pre-embedded data
    renderWeather(PRE_WEATHER, PRE_MARINE);
  }}
}}

// Initial render with pre-embedded data
renderWeather(PRE_WEATHER, PRE_MARINE);
// Then try to fetch fresh data
refreshWeather();
</script>
</body>
</html>'''

with open('/opt/data/fishing-hk/釣魚資訊站.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done! {len(html)} bytes")
