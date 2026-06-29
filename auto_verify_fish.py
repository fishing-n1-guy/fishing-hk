#!/usr/bin/env python3
"""
Auto-verify all fish cap images against HF Vision API.
Reads FISH array + FISH_IMG from index.html, downloads each image,
asks HF Vision "Is this a photo of {scientific_name}?", reports results.

Usage:
  python3 auto_verify_fish.py              # Verify all 64 fish
  python3 auto_verify_fish.py --batch N    # Only verify batch N (1-3)
"""

import re, os, sys, json, base64, urllib.request, time, subprocess

# === CONFIG ===
HF_MODEL = "Qwen/Qwen3-VL-8B-Instruct"
INDEX_HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
CAPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "fish_caps")
MAX_RETRIES = 3
CONFIG_FILE = "/tmp/curl_hf.conf"

def extract_fish_data():
    """Extract FISH array and FISH_IMG from index.html"""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse FISH array
    fish_match = re.search(r"const FISH = \[(.*?)\];", content, re.DOTALL)
    if not fish_match:
        print("ERROR: Could not find FISH array")
        return [], {}

    fish_block = fish_match.group(1)
    fish = re.findall(r'\[\s*"(.*?)",\s*"(.*?)",\s*"(.*?)",\s*"(.*?)",\s*"(.*?)",\s*"(.*?)",\s*"(.*?)"\s*\]', fish_block)

    # Parse FISH_IMG
    img_match = re.search(r"const FISH_IMG = \{(.*?)\};", content, re.DOTALL)
    img_map = {}
    if img_match:
        img_block = img_match.group(1)
        img_entries = re.findall(r'"(.*?)":\s*"(.*?)"', img_block)
        for name, url in img_entries:
            img_map[name] = url

    return fish, img_map

def verify_with_hf_vision(image_path, chinese_name, scientific_name):
    """Use HF Vision API to verify fish image (payload written to file to avoid arg too long)"""
    if not os.path.exists(image_path):
        return "FILE_MISSING", None

    if not os.path.exists(CONFIG_FILE):
        return "NO_CONFIG", None

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    prompt = (
        f"Is this a photo of '{scientific_name}' ({chinese_name})? "
        "Answer ONLY with YES or NO. "
        "If you are not sure or the image is unclear or it is a drawing/illustration, answer NO."
    )

    payload = json.dumps({
        "model": HF_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ],
        "max_tokens": 10,
        "temperature": 0
    })

    # Write payload to temp file to avoid "Argument list too long"
    payload_path = "/tmp/hf_verify_payload.json"
    with open(payload_path, "w", encoding="utf-8") as f:
        f.write(payload)

    for attempt in range(MAX_RETRIES):
        try:
            result = subprocess.run(
                ["curl", "-s", "--max-time", "45",
                 "-X", "POST", "https://router.huggingface.co/v1/chat/completions",
                 "-K", CONFIG_FILE,
                 "-H", "Content-Type: application/json",
                 "-d", f"@{payload_path}"],
                capture_output=True, text=True, timeout=60
            )

            if result.returncode != 0:
                return f"CURL_ERR({result.stderr[:60]})", None

            data = json.loads(result.stdout)

            if "error" in data:
                return f"API_ERR({str(data['error'])[:60]})", None

            if "choices" in data and len(data["choices"]) > 0:
                answer = data["choices"][0]["message"]["content"].strip().upper()
                return answer, data["choices"][0]
            else:
                return "NO_RESP", None

        except json.JSONDecodeError as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return f"JSON_ERR({str(e)[:30]})", None
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            return f"EXCEPT({str(e)[:60]})", None

    return "MAX_RETRIES", None

def check_cap_integrity(path):
    """Check if a JPEG file is valid"""
    if not os.path.exists(path):
        return "MISSING", 0
    size = os.path.getsize(path)
    if size < 1000:
        return "TOO_SMALL", size
    with open(path, "rb") as f:
        header = f.read(3)
    if header == b'\xff\xd8\xff':
        return "OK", size
    else:
        return "INVALID", size

def main():
    batch_filter = None
    for arg in sys.argv:
        if arg.startswith("--batch="):
            batch_filter = int(arg.split("=")[1])

    # Check config
    if not os.path.exists(CONFIG_FILE):
        print("Missing HF config at " + CONFIG_FILE)
        sys.exit(1)

    # Extract data
    fish, img_map = extract_fish_data()
    print(f"Read {len(fish)} fish, FISH_IMG has {len(img_map)} entries\n")

    batch_size = (len(fish) + 2) // 3
    results = []

    for idx, (cn_name, en_name, size_range, season, level, sci_name, spots) in enumerate(fish):
        fish_num = idx + 1

        # Apply batch filter
        if batch_filter:
            batch_num = (idx // batch_size) + 1
            if batch_num != batch_filter:
                continue

        cap_path = os.path.join(CAPS_DIR, f"cap_{cn_name}.jpg")

        # Check local file
        if os.path.exists(cap_path):
            status, fsize = check_cap_integrity(cap_path)
            if status != "OK":
                results.append((fish_num, cn_name, sci_name, f"BAD({status})", fsize, cap_path))
                print(f"  [{fish_num:2d}] {cn_name:10s} X {status} ({fsize} bytes)")
                continue
            image_for_verify = cap_path
        else:
            results.append((fish_num, cn_name, sci_name, "NO_FILE", 0, ""))
            print(f"  [{fish_num:2d}] {cn_name:10s} X NO_FILE")
            continue

        # Verify with HF Vision
        print(f"  [{fish_num:2d}] {cn_name:10s} ({sci_name[:25]:25s})... ", end="", flush=True)
        verdict, detail = verify_with_hf_vision(image_for_verify, cn_name, sci_name)

        if verdict == "YES":
            print("YES")
        elif verdict == "NO":
            print("NO (wrong fish!)")
        else:
            print(verdict)

        file_size = os.path.getsize(image_for_verify) if os.path.exists(image_for_verify) else 0
        img_url = img_map.get(cn_name, "")
        results.append((fish_num, cn_name, sci_name, verdict, file_size, img_url[:80] if img_url else cap_path))

        time.sleep(0.3)

    # === SUMMARY TABLE ===
    print("\n" + "=" * 90)
    print("VERIFICATION RESULTS")
    print("=" * 90)
    print(f"{'#':>3} | {'Fish':10s} | {'Status':8s} | {'Size':>8s} | Note")
    print("-" * 90)

    yes_count = 0
    no_count = 0
    error_count = 0
    missing_count = 0

    for fish_num, cn_name, sci_name, verdict, fsize, url in results:
        fsize_str = f"{fsize // 1024}KB" if fsize > 0 else "-"

        if verdict == "YES":
            yes_count += 1
            icon = "+"
        elif verdict == "NO":
            no_count += 1
            icon = "X"
        elif verdict == "NO_FILE":
            missing_count += 1
            icon = "?"
            verdict = "NO_FILE"
        else:
            error_count += 1
            icon = "!"

        print(f"{fish_num:3d} | {cn_name:10s} | {icon} {verdict:7s} | {fsize_str:>8s} | ")

    print("-" * 90)
    print(f"\nSummary:")
    print(f"  Correct:   {yes_count}")
    print(f"  Wrong:     {no_count}")
    print(f"  Error:     {error_count}")
    print(f"  Missing:   {missing_count}")
    print(f"  Total:     {len(results)}")

    # Report wrong fish
    if no_count > 0:
        print(f"\nWRONG FISH DETECTED:")
        for fish_num, cn_name, sci_name, verdict, fsize, url in results:
            if verdict == "NO":
                print(f"  [{fish_num}] {cn_name} ({sci_name}) - need replacement!")

if __name__ == "__main__":
    main()
