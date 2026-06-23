#!/usr/bin/env python3
"""
Fetch HKO tide prediction data for Hong Kong fishing site.
Extracts tide extremes (high/low) and hourly heights for multiple stations.
Outputs tide_data.json for the website to consume.

Data source: Hong Kong Observatory open data
  PE{station}.{year}.txt = Tide extremes (high/low)
  PH{station}.{year}.txt = Hourly tide heights
"""

import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

# HK tide stations relevant for fishing
STATIONS = {
    "QUB": {"name": "鰂魚涌", "name_en": "Quarry Bay"},
    "CCH": {"name": "長洲", "name_en": "Cheung Chau"},
    "KLW": {"name": "高流灣", "name_en": "Ko Lau Wan"},
    "TMW": {"name": "大廟灣", "name_en": "Tai Miu Wan"},
    "SPW": {"name": "石壁", "name_en": "Shek Pik"},
    "LOP": {"name": "樂安排", "name_en": "Lok On Pai"},
}

HKO_BASE = "https://www.hko.gov.hk/tide/marine/data"


def fetch_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "fishing-hk/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8")
    except Exception as e:
        print(f"  ⚠️  Failed: {e}")
        return None


def parse_pe_line(line):
    """
    HKO PE format - tricky concatenated values:
    
    Format after MMDD: T1 [H1] [T2] (H2)(T3) (H3)(T4) H4
    Each 7-char group = 3-digit height(cm) + 4-digit time(HHMM)
    
    Examples:
      "101 143  64 856 1451147 1321916 252"
      = Jan1: 01:43(0.64) 08:56(1.45) 11:47(1.32) 19:16(2.52)
      
      "623 459 1721031 1231648 1482209  95"
      = Jun23: 04:59(1.72) 10:31(1.23) 16:48(1.48) 22:09(0.95)
    """
    parts = line.strip().split()
    if len(parts) < 3:
        return []

    mmdd = parts[0].strip()
    if len(mmdd) != 3:
        return []
    
    month = int(mmdd[0])
    day = int(mmdd[1:])
    if month < 1 or month > 12 or day < 1 or day > 31:
        return []

    rest = parts[1:]
    
    # Strategy: find all 7-char groups first (they are reliably height+time)
    seven_char_indices = [i for i, p in enumerate(rest) if len(p) == 7 and p.isdigit()]
    non_seven = [i for i, p in enumerate(rest) if len(p) != 7 or not p.isdigit()]
    
    # Extract all values into ordered list of (time, height) pairs
    pairs = []
    
    if not seven_char_indices:
        return []
    
    first_7 = seven_char_indices[0]
    last_7 = seven_char_indices[-1]
    
    # Everything before first 7-char group are standalone times
    # T1 is always the first token
    if first_7 > 0:
        t1_raw = rest[0]
        if len(t1_raw) in [3, 4]:
            pairs.append(("time", t1_raw))
        # If there's a second token before 7-char, it's H1
        if first_7 > 1:
            h1_raw = rest[1]
            pairs.append(("height", h1_raw))
        # If there's a third token before 7-char, it's T2
        if first_7 > 2:
            t2_raw = rest[2]
            pairs.append(("time", t2_raw))
    
    # Each 7-char group = height(3) + time(4)
    for idx in seven_char_indices:
        p = rest[idx]
        pairs.append(("height", p[:3]))  # first 3 = height in cm
        pairs.append(("time", p[3:]))    # last 4 = time HHMM
    
    # Last token (after all 7-char groups) = final height
    last_idx = len(rest) - 1
    if last_idx > last_7:
        h_last = rest[last_idx]
        pairs.append(("height", h_last))
    
    # Now extract time,height pairs in order
    times = [v for kind, v in pairs if kind == "time"]
    heights = [v for kind, v in pairs if kind == "height"]
    
    extremes = []
    for i in range(min(len(times), len(heights))):
        t = times[i]
        h = heights[i]
        try:
            t = t.zfill(4)  # pad to 4 digits: "459" -> "0459"
            hh = int(t[:2])
            mm = int(t[2:])
            if hh > 23 or mm > 59:
                continue
            height_cm = int(h)
            if height_cm > 1500:
                continue
            height_m = round(height_cm / 100.0, 2)
            extremes.append({
                "hour": hh, "min": mm,
                "height_m": height_m,
                "time": f"{hh:02d}:{mm:02d}"
            })
        except (ValueError, IndexError):
            continue
    
    if len(extremes) < 2:
        return []
    
    # Determine high/low types
    if extremes[0]["height_m"] > extremes[1]["height_m"]:
        types = ["high", "low", "high", "low"]
    else:
        types = ["low", "high", "low", "high"]
    for i, e in enumerate(extremes):
        if i < len(types):
            e["type"] = types[i]
    
    return {"month": month, "day": day, "extremes": extremes}


def parse_ph_data(text, today_mmdd):
    """Parse PH (hourly heights) data."""
    results = []
    if not text:
        return results
    
    for offset in range(3):
        target_mmdd = f"{today_mmdd[0]}{int(today_mmdd[1:]) + offset:02d}" if offset > 0 else today_mmdd
        # Handle month rollover
        m = int(today_mmdd[0])
        d = int(today_mmdd[1:]) + offset
        # Simple handling: assume within same month (Jun 23-25)
        mmdd = f"{m}{d:02d}"
        
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 25:
                continue
            
            # Check if first token matches our date
            first = parts[0].strip()
            if len(first) != 3:
                continue
            try:
                lm = int(first[0])
                ld = int(first[1:])
            except:
                continue
            
            if lm == m and ld == d:
                heights = []
                for i in range(1, 25):
                    try:
                        h = int(parts[i])
                        if h > 1000:
                            heights.append(None)
                        else:
                            heights.append(round(h / 100.0, 2))
                    except:
                        heights.append(None)
                
                valid_heights = [h for h in heights if h is not None]
                results.append({
                    "month": m,
                    "day": d,
                    "heights": heights,
                    "min_h": min(valid_heights) if valid_heights else 0,
                    "max_h": max(valid_heights) if valid_heights else 0
                })
                break
    
    return results


def parse_pe_data(text, today_mmdd):
    """Parse PE (extremes) data."""
    results = []
    if not text:
        return results
    
    m = int(today_mmdd[0])
    d = int(today_mmdd[1:])
    
    for offset in range(3):
        dm = m
        dd = d + offset
        # Assume same month for now
        
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            
            first = parts[0].strip()
            if len(first) != 3:
                continue
            try:
                lm = int(first[0])
                ld = int(first[1:])
            except:
                continue
            
            if lm == dm and ld == dd:
                parsed = parse_pe_line(line)
                if parsed and parsed["extremes"]:
                    results.append(parsed)
                break
    
    return results


def main():
    now = datetime.now(timezone(timedelta(hours=8)))
    today_mmdd = f"{now.month}{now.day:02d}"
    
    all_data = {
        "updated": now.strftime("%Y-%m-%d %H:%M"),
        "stations": {}
    }
    
    for code in sorted(STATIONS.keys()):
        name = STATIONS[code]["name"]
        print(f"Fetching {name} ({code})...")
        
        year = now.year
        url_pe = f"{HKO_BASE}/PE{code}.{year}.txt"
        url_ph = f"{HKO_BASE}/PH{code}.{year}.txt"
        
        text_pe = fetch_text(url_pe)
        text_ph = fetch_text(url_ph)
        
        extremes_data = parse_pe_data(text_pe, today_mmdd)
        hourly_data = parse_ph_data(text_ph, today_mmdd)
        
        all_data["stations"][code] = {
            "station": code,
            "name": name,
            "name_en": STATIONS[code]["name_en"],
            "extremes": extremes_data,
            "hourly": hourly_data
        }
        
        print(f"  ✅ Extremes: {len(extremes_data)} days")
        print(f"  ✅ Hourly: {len(hourly_data)} days")
    
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tide_data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Tide data saved to {out_path}")
    print(f"📊 Stations: {len(all_data['stations'])}")
    
    # Quick validation
    for code, data in all_data["stations"].items():
        for day_data in data["extremes"]:
            for e in day_data["extremes"]:
                if e["hour"] > 23 or e["min"] > 59:
                    print(f"  ❌ {code}: invalid time {e['time']}")
                if e["height_m"] > 10:
                    print(f"  ❌ {code}: invalid height {e['height_m']}m at {e['time']}")


if __name__ == "__main__":
    main()
