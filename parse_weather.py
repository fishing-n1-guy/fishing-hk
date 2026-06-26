#!/usr/bin/env python3
import json, re, datetime

with open('/opt/data/fishing-hk/釣魚資訊站.html', 'r', encoding='utf-8') as f:
    html = f.read()

w_match = re.search(r'const PRE_WEATHER = (\{.*?\});', html, re.DOTALL)
m_match = re.search(r'const PRE_MARINE = (\{.*?\});', html, re.DOTALL)

weather = json.loads(w_match.group(1))
marine = json.loads(m_match.group(1))

hk = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
today_str = hk.strftime('%Y-%m-%d')
h = hk.hour

times = weather['hourly']['time']
idx = 0
for i, t in enumerate(times):
    if t.startswith(today_str) and int(t[11:13]) >= h:
        idx = i
        break

temp = weather['hourly']['temperature_2m'][idx]
wind_s = weather['hourly']['wind_speed_10m'][idx]
wind_d = weather['hourly']['wind_direction_10m'][idx]
gust = weather['hourly']['wind_gusts_10m'][idx]
wave_h = marine['hourly']['wave_height'][idx]
swell = marine['hourly']['swell_wave_height'][idx]
wind_wave = marine['hourly']['wind_wave_height'][idx]

bf = min(12, round(wind_s / 10))
wind_names = ['無風','軟風','輕風','微風','和風','清風','強風','疾風','大風','烈風','暴風','狂風','颶風']
wind_dir_names = ['北','東北偏北','東北','東北偏東','東','東南偏東','東南','東南偏南','南','西南偏南','西南','西南偏西','西','西北偏西','西北','西北偏北']
dir_name = wind_dir_names[round(wind_d/22.5)%16]

ss = '平靜'
if wave_h >= 0.1: ss='小浪'
if wave_h >= 0.5: ss='中浪'
if wave_h >= 1.25: ss='大浪'
if wave_h >= 2.5: ss='非常大浪'
if wave_h >= 4: ss='巨浪'

score = 50
if bf <= 3: score += 25
elif bf <= 5: score += 10
elif bf <= 7: score -= 10
else: score -= 30
if wave_h < 0.3: score += 10
elif wave_h < 1: score += 5
elif wave_h > 2: score -= 20
if 22 <= temp <= 30: score += 15
elif temp < 15 or temp > 35: score -= 10
score = max(0, min(100, score))

msgs = ['好唔適合釣魚','麻麻地，考慮清楚','一般，可以一試','唔錯，可以出發','極佳！今日好適合釣魚！']
msg = msgs[min(4, score//25)]

print(f"TIME={times[idx]}")
print(f"TEMP={temp:.1f}")
print(f"WIND={bf}|{wind_names[bf]}|{wind_s:.0f}")
print(f"DIR={dir_name}")
print(f"GUST={gust:.0f}")
print(f"WAVE={wave_h:.2f}|{ss}")
print(f"SWELL={swell:.2f}")
print(f"SCORE={score}")
print(f"MSG={msg}")

print("---FORECAST---")
days_en = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六']
for i in range(min(3, len(weather['daily']['time']))):
    d = datetime.datetime.fromisoformat(weather['daily']['time'][i])
    tmax = weather['daily']['temperature_2m_max'][i]
    tmin = weather['daily']['temperature_2m_min'][i]
    wmax = min(12, round(weather['daily']['wind_speed_10m_max'][i]/10))
    wavemax = marine['daily']['wave_height_max'][i] if i < len(marine['daily']['wave_height_max']) else 0
    print(f"DAY={d.month}/{d.day}|{days_en[d.weekday()]}|{tmin:.0f}-{tmax:.0f}|WIND={wmax}|WAVE={wavemax:.2f}")
