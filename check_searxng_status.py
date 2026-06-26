#!/usr/bin/env python3
import json

d = json.load(open('/tmp/searxng_test.json'))
results = d.get("results", [])
suggestions = d.get("suggestions", [])
unresponsive = d.get("unresponsive_engines", [])

engines = set(r["engine"] for r in results)
print(f"Results: {len(results)}")
print(f"Suggestions: {len(suggestions)}")
print(f"Unresponsive engines: {len(unresponsive)}")
print(f"Engines used: {engines}")
if unresponsive:
    for e, reason in unresponsive:
        print(f"  - {e}: {reason}")
print("\nSearch query: test")
print("Status: OK")
