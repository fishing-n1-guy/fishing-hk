#!/usr/bin/env python3
"""Sync records from local to GitHub. Run as cron every 5 min."""
import json, base64, os, time, subprocess, re

REPO = "fishing-n1-guy/fishing-hk"
FPATH = "data/records/sync_master.json"
QUEUE = "/opt/data/fishing-hk/.sync_queue.json"
STATE = "/tmp/fishing_sync_state.json"
GIT_DIR = "/opt/data/fishing-hk"

def token():
    r = subprocess.run(['git', '-C', GIT_DIR, 'remote', '-v'],
                      capture_output=True, text=True, timeout=5)
    m = re.search(r'fishing-n1-guy:(.*?)@github', r.stdout)
    return m.group(1) if m else None

def github_get(tok):
    url = "https://api.github.com/repos/" + REPO + "/contents/" + FPATH
    h = ["Authorization: token " + tok]
    r = subprocess.run(['curl', '-s', '--max-time', '10', '-H', h[0], url],
                      capture_output=True, text=True, timeout=15)
    return json.loads(r.stdout)

def github_put(tok, sha, records):
    url = "https://api.github.com/repos/" + REPO + "/contents/" + FPATH
    new_b64 = base64.b64encode(json.dumps(records, ensure_ascii=False).encode()).decode()
    payload = json.dumps({
        "message": "sync auto",
        "content": new_b64,
        "sha": sha,
        "branch": "main"
    })
    r = subprocess.run(['curl', '-s', '--max-time', '15',
        '-H', 'Authorization: token ' + tok,
        '-H', 'Content-Type: application/json',
        '-X', 'PUT', url, '-d', payload],
        capture_output=True, text=True, timeout=20)
    return json.loads(r.stdout)

def main():
    tok = token()
    if not tok:
        return print("No token")
    
    gdata = github_get(tok)
    sha = gdata.get('sha')
    b64 = gdata.get('content', '')
    if not b64:
        return print("No content")
    
    grecs = json.loads(base64.b64decode(b64).decode())
    gids = {c['id'] for c in grecs['catches']}
    
    if not os.path.exists(QUEUE):
        return print("No queue")
    
    with open(QUEUE) as f:
        queue = json.load(f)
    
    new = [c for c in queue if c['id'] not in gids]
    if not new:
        with open(STATE, 'w') as f:
            json.dump({"t": time.time(), "n": len(grecs['catches'])}, f)
        return print("OK " + str(len(grecs['catches'])) + " records")
    
    for c in new:
        grecs['catches'].append(c)
    grecs['catches'].sort(key=lambda x: x['id'], reverse=True)
    grecs['updated'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    
    res = github_put(tok, sha, grecs)
    if 'content' in res:
        with open(QUEUE, 'w') as f:
            json.dump([], f)
        with open(STATE, 'w') as f:
            json.dump({"t": time.time(), "n": len(grecs['catches'])}, f)
        print("PUSHED " + str(len(new)) + " recs")
    else:
        print("FAIL: " + res.get('message', '?'))

if __name__ == '__main__':
    main()
