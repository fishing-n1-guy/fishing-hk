#!/usr/bin/env python3
import json, re, datetime

with open('/opt/data/fishing-hk/釣魚資訊站.html', 'r') as f:
    content = f.read()

m_w = re.search(r'const PRE_WEATHER = ({.*?});', content, re.DOTALL)
m_m = re.search(r'const PRE_MARINE = ({.*?});', content, re.DOTALL)

weather = json.loads(m_w.group(1))
marine = json.loads(m_m.group(1))

# System time
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
print(f"System HKT time: {now}")
print(f"System UTC: {datetime.datetime.utcnow()}")

# Hourly data
times = weather['hourly']['time']
print(f"\n--- Hourly slots: {len(times)} ---")
print(f"First: {times[0]}, Last: {times[-1]}")

# Find current/latest available time slot
today_str = now.strftime('%Y-%m-%d')
h = now.hour

idx = 0
for i, t in enumerate(times):
    if t.startswith(today_str) and int(t[11:13]) >= h:
        idx = i
        break

print(f"\n--- Current time slot: {times[idx]} (idx={idx}) ---")

temp = weather['hourly']['temperature_2m'][idx]
wind_s = weather['hourly']['wind_speed_10m'][idx]
wind_d = weather['hourly']['wind_direction_10m'][idx]
gust = weather['hourly']['wind_gusts_10m'][idx]
wave_h = marine['hourly']['wave_height'][idx]
swell = marine['hourly']['swell_wave_height'][idx]
wind_wave = marine['hourly']['wind_wave_height'][idx]

bf = min(12, round(wind_s / 10))
bf_names = ["無風","軟風","輕風","微風","和風","清風","強風","疾風","大風","烈風","暴風","狂風","颶風"]
wind_dir = ["北","東北偏北","東北","東北偏東","東","東南偏東","東南","東南偏南","南","西南偏南","西南","西南偏西","西","西北偏西","西北","西北偏北"]
dir_name = wind_dir[round(wind_d/22.5)%16]

ss = "平靜"
if wave_h>=0.1: ss="小浪"
if wave_h>=0.5: ss="中浪"
if wave_h>=1.25: ss="大浪"
if wave_h>=2.5: ss="非常大浪"
if wave_h>=4: ss="巨浪"

# Score
score = 50
if bf<=3: score+=25
elif bf<=5: score+=10
elif bf<=7: score-=10
else: score-=30
if wave_h<0.3: score+=10
elif wave_h<1: score+=5
elif wave_h>2: score-=20
if temp>=22 and temp<=30: score+=15
elif temp<15 or temp>35: score-=10
score = max(0, min(100, score))

msgs = ["😢 唔係好適合釣魚","😐 麻麻地，考慮清楚","👌 一般，可以一試","👍 唔錯，可以出發","🏆 極佳！今日好適合釣魚！"]
msg = msgs[min(4, int(score/25))]

print(f"\n=== 今日天氣重點 ===")
print(f"📍 位置: 香港")
print(f"🕐 時間: {times[idx]}")
print(f"🌡️ 氣溫: {temp:.1f}°C")
print(f"💨 風力: {bf}級 ({bf_names[bf]}) - {wind_s:.0f} km/h")
print(f"🧭 風向: {dir_name} ({wind_d:.0f}°)")
print(f"💥 陣風: {gust:.0f} km/h")
print(f"🌊 浪高: {wave_h:.2f}m ({ss})")
print(f"〰️ 湧浪: {swell:.2f}m")
print(f"🌬️ 風浪: {wind_wave:.2f}m")
print(f"\n🎯 釣魚指數: {score}/100")
print(f"📝 評價: {msg}")
print(f"   🌬️{bf}級 🌊{wave_h:.2f}m 🌡️{temp:.1f}°C")

# Daily forecast
print(f"\n=== 未來三天預測 ===")
days_cn = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
for i in range(min(3, len(weather['daily']['time']))):
    dt = weather['daily']['time'][i]
    tmin = weather['daily']['temperature_2m_min'][i]
    tmax = weather['daily']['temperature_2m_max'][i]
    wmax = min(12, round(weather['daily']['wind_speed_10m_max'][i]/10))
    wavemax = marine['daily']['wave_height_max'][i] if i < len(marine['daily']['wave_height_max']) else 0
    d = datetime.datetime.strptime(dt, '%Y-%m-%d')
    dw = days_cn[d.weekday()]
    print(f"  {d.month}/{d.day}({dw}): {tmin:.0f}-{tmax:.0f}°C 💨{wmax}級 🌊{wavemax:.2f}m")
