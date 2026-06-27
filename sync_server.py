#!/usr/bin/env python3
"""Simple HTTP sync server. POST /sync with JSON {catches: [...]}"""
import json, base64, os, subprocess, re
from http.server import HTTPServer, BaseHTTPRequestHandler

GIT_DIR = "/opt/data/fishing-hk"
QUEUE = "/opt/data/fishing-hk/.sync_queue.json"

def get_token():
    r = subprocess.run(["git", "-C", GIT_DIR, "remote", "-v"],
                      capture_output=True, text=True, timeout=5)
    m = re.search(r"fishing-n1-guy:(.*?)@github", r.stdout)
    return m.group(1) if m else None

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        
        try:
            data = json.loads(body)
            catches = data.get("catches", [])
            
            # Queue
            existing = []
            if os.path.exists(QUEUE):
                with open(QUEUE) as f:
                    existing = json.load(f)
            
            ids = {c["id"] for c in existing}
            for c in catches:
                if c["id"] not in ids:
                    existing.append(c)
                    ids.add(c["id"])
            
            with open(QUEUE, "w") as f:
                json.dump(existing, f)
            
            # Try push
            tok = get_token()
            pushed = 0
            if tok:
                url = "https://api.github.com/repos/fishing-n1-guy/fishing-hk/contents/data/records/sync_master.json"
                g = subprocess.run(["curl", "-s", "--max-time", "10",
                    "-H", "Authorization: token " + tok, url],
                    capture_output=True, text=True, timeout=15)
                gdata = json.loads(g.stdout)
                sha = gdata.get("sha")
                b64 = gdata.get("content", "")
                
                if b64 and sha:
                    grecs = json.loads(base64.b64decode(b64).decode())
                    gids = {c["id"] for c in grecs["catches"]}
                    new = [c for c in existing if c["id"] not in gids]
                    
                    if new:
                        for c in new:
                            grecs["catches"].append(c)
                        grecs["catches"].sort(key=lambda x: x["id"], reverse=True)
                        n64 = base64.b64encode(json.dumps(grecs, ensure_ascii=False).encode()).decode()
                        payload = json.dumps({"message":"sync","content":n64,"sha":sha,"branch":"main"})
                        subprocess.run(["curl", "-s", "--max-time", "15",
                            "-H", "Authorization: token " + tok,
                            "-H", "Content-Type: application/json",
                            "-X", "PUT", url, "-d", payload],
                            capture_output=True, text=True, timeout=20)
                        pushed = len(new)
                        with open(QUEUE, "w") as f:
                            json.dump([], f)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "synced": pushed, "queued": len(existing)}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())

if __name__ == "__main__":
    port = 8765
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
    print("Sync server on port " + str(port))
