#!/usr/bin/env python3
"""Test import and settings for SearXNG"""
import sys
import os

os.chdir('/opt/data/searxng')
sys.path.insert(0, '/opt/data/stt-packages')
sys.path.insert(0, '/opt/data/searxng')

print('Step 1: Importing searx.webapp...')
sys.stdout.flush()

try:
    from searx.webapp import app, run
    print('Import succeeded')
    sys.stdout.flush()
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)

print('Step 2: Checking settings...')
sys.stdout.flush()

try:
    from searx.settings_loader import get_setting
    print('Port setting:', get_setting('server.port'))
    print('Bind address:', get_setting('server.bind_address'))
    sys.stdout.flush()
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)

print('All good!')
