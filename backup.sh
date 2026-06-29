#!/bin/bash
# 每星期自動 backup 釣魚網站
BACKUP_DIR="/opt/data/backups/fishing-hk"
mkdir -p "$BACKUP_DIR"

DATE=$(date +%Y%m%d_%H%M)
FILE="$BACKUP_DIR/fishing-hk_$DATE.tar.gz"

# Backup fish images + HTML + tide data
tar czf "$FILE" \
  -C /opt/data/fishing-hk \
  images/fish_caps/ \
  index.html \
  tide_data.json \
  fetch_tide.py \
  cron_update_tide.sh \
  sync_server.py \
  2>/dev/null

SIZE=$(du -h "$FILE" | cut -f1)
echo "✅ Backup done: $FILE ($SIZE)"

# Keep only last 10 backups
ls -t "$BACKUP_DIR"/fishing-hk_*.tar.gz 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null
echo "🧹 Old backups cleaned (keep 10)"
