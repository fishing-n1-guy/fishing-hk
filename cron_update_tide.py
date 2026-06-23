#!/usr/bin/env python3
"""
Cron job script: Fetch HKO tide data, commit & push to GitHub.
Run this daily to keep tide_data.json updated.
"""
import subprocess
import sys
import os

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def run(cmd, cwd=REPO_DIR):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"❌ {' '.join(cmd)}: {result.stderr.strip()}")
        return False
    print(result.stdout.strip()[:200])
    return True

def main():
    print("🌊 Fetching HKO tide data...")
    
    # Step 1: Run fetch_tide.py
    r = subprocess.run(
        [sys.executable, os.path.join(REPO_DIR, "fetch_tide.py")],
        cwd=REPO_DIR, capture_output=True, text=True, timeout=30
    )
    print(r.stdout)
    if r.returncode != 0:
        print(f"❌ fetch_tide.py failed: {r.stderr}")
        return False
    
    # Step 2: Check if tide_data.json changed
    r = subprocess.run(
        ["git", "diff", "--quiet", "tide_data.json"],
        cwd=REPO_DIR, capture_output=True, text=True, timeout=10
    )
    if r.returncode == 0:
        print("✅ Tide data unchanged, nothing to commit.")
        return True
    
    # Step 3: Commit and push
    print("📤 Tide data changed, pushing to GitHub...")
    
    if not run(["git", "add", "tide_data.json"]):
        return False
    if not run(["git", "add", "index.html"]):
        return False
    if not run(["git", "commit", "-m", "🌊 自動更新潮汐數據 + 網站更新"]):
        return False
    if not run(["git", "push"]):
        return False
    
    print("✅ Successfully updated tide data on GitHub!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
