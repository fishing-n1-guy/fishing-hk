#!/usr/bin/env python3
"""Test import and settings for SearXNG, then start server"""
import sys
import os

os.chdir('/opt/data/searxng')
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')

print('Step 1: Importing searx...')
sys.stdout.flush()

import searx
print('get_setting exists:', hasattr(searx, 'get_setting'))
print('Port:', searx.get_setting('server.port'))
print('Bind address:', searx.get_setting('server.bind_address'))
sys.stdout.flush()

print('Step 2: Importing webapp...')
sys.stdout.flush()
from searx.webapp import app, run

print('Step 3: Starting Flask dev server on port 8889...')
sys.stdout.flush()

# Run with threaded=True so we can see output
app.run(port=8889, host='0.0.0.0', threaded=True, debug=False)
