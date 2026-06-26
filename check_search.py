#!/usr/bin/env python3
"""Check SearXNG installation status."""
import sys, os

sys.path.insert(0, '/opt/data/stt-packages')

# Check installed packages
import pkg_resources
packages = [d for d in os.listdir('/opt/data/stt-packages') if 'searx' in d.lower()]
print(f"SearXNG packages found: {packages}")

# Try to import
try:
    import searxng
    print(f"searxng: OK")
except ImportError:
    print("searxng: not importable")

try:
    import searx
    print(f"searx: OK")
except ImportError:
    print("searx: not importable")

# Check for searxng command
bin_dir = '/opt/data/stt-packages/bin'
if os.path.isdir(bin_dir):
    bins = os.listdir(bin_dir)
    print(f"binaries: {[b for b in bins if 'searx' in b.lower()]}")
