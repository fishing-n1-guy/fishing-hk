#!/usr/bin/env python3
"""Clean test records from sync file"""
import subprocess, json, base64, re

def get_token():
    r = subprocess.run(["git", "-C", "/opt/data/fishing-hk", "remote", "-v"],
                      capture_output=True, text=True, timeout=5)
    m = re.search(r"fishing-n1-guy:(.*?)@github", r.stdout)
    return m.group(1)

tok = get_token()
url = "https://api.github.com/repos/fishing-n1-guy/fishing-hk/contents/data/records/sync_master.json"
h = "Authorization: token *** + tok

resp = subprocess.run(["curl", "-s", "--max-time", "10", "-H", h, url],
    capture_output=True, text=True, timeout=15)
d = json.loads(resp.stdout)
sha = d["sha"]
records = json.loads(base64.b64decode(d["content"]).decode())

# Keep only records with location or large IDs (real catches)
real = []
for c in records["catches"]:
    if c.get("location") or c["id"] > 1000000000000:
        real.append(c)
records["catches"] = real
records["updated"] = "cleaned"

n64 = base64.b64encode(json.dumps(records, ensure_ascii=False).encode()).decode()
payload = json.dumps({"message":"clean test data","content":n64,"sha":sha,"branch":"main"})

r2 = subprocess.run(["curl", "-s", "--max-time", "15", "-H", h,
    "-H", "Content-Type: application/json",
    "-X", "PUT", url, "-d", payload],
    capture_output=True, text=True, timeout=20)
res = json.loads(r2.stdout)
if "content" in res:
    print("OK - " + str(len(real)) + " records kept, sha=" + res["content"]["sha"][:10])
else:
    print("FAIL: " + res.get("message", "?"))
