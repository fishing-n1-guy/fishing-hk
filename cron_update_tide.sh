#!/usr/bin/env bash
# Cron job: Fetch HKO tide data, commit & push to GitHub
set -e

cd /opt/data/fishing-hk

echo "🌊 Fetching HKO tide data..."
python3 fetch_tide.py

# Check if tide_data.json changed
if git diff --quiet tide_data.json; then
    echo "✅ Tide data unchanged, nothing to commit."
    exit 0
fi

echo "📤 Tide data changed, pushing to GitHub..."
git add tide_data.json index.html fetch_tide.py cron_update_tide.py
git commit -m "🌊 自動更新潮汐數據 $(date '+%Y-%m-%d %H:%M')"
git push

echo "✅ Successfully updated tide data on GitHub!"
