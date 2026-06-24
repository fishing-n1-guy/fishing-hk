#!/usr/bin/env python3
"""Replace FISH array in index.html with updated scientific names."""
import os

# Read the generated fish data
with open('/opt/data/fishing-hk/fish_output.txt') as f:
    new_fish = f.read()

# Read the HTML
with open('/opt/data/fishing-hk/index.html') as f:
    html = f.read()

# Find the old FISH array
start = html.find('const FISH = [')
end = html.find('];', start) + 2

if start < 0 or end < 2:
    print("❌ Could not find FISH array")
    exit(1)

old_fish = html[start:end]
print(f"Old FISH: {len(old_fish)} chars")
print(f"New FISH: {len(new_fish)} chars")

# Replace
html = html[:start] + new_fish + html[end:]

# Write back
with open('/opt/data/fishing-hk/index.html', 'w') as f:
    f.write(html)

print("✅ Replaced FISH array")
print(f"HTML file size: {len(html)} bytes")
