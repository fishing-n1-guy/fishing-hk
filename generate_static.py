#!/usr/bin/env python3
"""Generate a static HTML with pre-fetched weather/marine/tide data."""
import json
import urllib.request
import urllib.error

HK_LAT = "22.3193"
HK_LON = "114.1694"

def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

print("Fetching weather data...")
weather = fetch(f"https://api.open-meteo.com/v1/forecast?latitude={HK_LAT}&longitude={HK_LON}&hourly=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max&timezone=Asia/Hong_Kong&forecast_days=3")

print("Fetching marine data...")
marine = fetch(f"https://marine-api.open-meteo.com/v1/marine?latitude={HK_LAT}&longitude={HK_LON}&hourly=wave_height,wave_direction,wind_wave_height,swell_wave_height&daily=wave_height_max,wave_direction_dominant&timezone=Asia/Hong_Kong")

print("Fetching tide data...")
today = __import__('datetime').date.today().strftime('%Y%m%d')
tide = fetch(f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?station=1617760&begin_date={today}&end_date={today}&product=predictions&datum=MLLW&units=metric&time_zone=gmt&format=json")

# Read the original HTML
with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# Inject the data as JS variables
data_script = f"""
<script>
// Pre-fetched data
window._PRELOADED_WEATHER = {json.dumps(weather)};
window._PRELOADED_MARINE = {json.dumps(marine)};
window._PRELOADED_TIDE = {json.dumps(tide)};
</script>
"""

# Insert before the existing init call
html = html.replace('initWeather();', f'{data_script}\n    initWeather();')

# Also modify the init function to use preloaded data
html = html.replace(
    'Promise.all([fetchWeather(), fetchMarine(), fetchTide()])',
    'Promise.resolve([window._PRELOADED_WEATHER, window._PRELOADED_MARINE, window._PRELOADED_TIDE])'
)

with open('/opt/data/fishing-hk/index_static.html', 'w') as f:
    f.write(html)

print("Done! Saved to index_static.html")
