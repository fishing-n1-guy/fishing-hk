#!/usr/bin/env python3
"""Check SearXNG installation."""
import sys, os
sys.path.insert(0, '/opt/data/stt-packages')

pkgs = [d for d in os.listdir('/opt/data/stt-packages') if 'searx' in d.lower()]
print(f"SearXNG packages: {pkgs}")

if os.path.isdir('/opt/data/stt-packages/bin'):
    bins = os.listdir('/opt/data/stt-packages/bin')
    print(f"Bins: {[b for b in bins if 'searx' in b.lower()]}")

try:
    import searx; print(f"searx OK")
except: print("searx: no")
try:
    import searxng; print(f"searxng OK")
except: print("searxng: no")
