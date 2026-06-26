#!/bin/bash
cd /opt/data/searxng
export PYTHONPATH=/opt/data/stt-packages:/opt/data/searxng
export GIT_DIR=/opt/data/searxng/.git
export SEARXNG_SETTINGS_PATH=/opt/data/searxng/settings.yml
export SEARXNG_PORT=8889
export SEARXNG_BIND_ADDRESS=0.0.0.0
exec python3 -c "
import sys
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')
from searx.webapp import run
run()
"
