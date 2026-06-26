#!/usr/bin/env python3
"""Test vision models to find the most reliable one."""
import requests, base64, glob

key = ""
with open('/app/.env') as f:
    for line in f:
        line = line.strip()
        if 'OPENROUTER_API_KEY' in line and '=' in line:
            key = line.split('=', 1)[1].strip()
            break
if not key:
    print("No key found");
    exit(1)

images = glob.glob('/app/image_cache/*.jpg') or glob.glob('/opt/data/fishing-hk/*.jpg')
if not images:
    print("No test images");
    exit(1)

with open(images[0], 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

models = [
    "qwen/qwen2.5-vl-72b-instruct",
    "meta-llama/llama-3.2-11b-vision-instruct:free",
    "google/gemma-4-26b-a4b-it:free",
]

for model in models:
    resp = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
        json={
            'model': model,
            'messages': [{'role': 'user', 'content': [
                {'type': 'text', 'text': 'Describe this image'},
                {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{img_b64[:500]}'}}
            ]}],
            'max_tokens': 100,
        },
        timeout=30
    )
    data = resp.json()
    if resp.status_code == 200:
        c = data.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"OK {model}: {len(c)} chars")
    else:
        e = data.get('error', {}).get('message', '')[:80]
        print(f"FAIL {model}: {resp.status_code} - {e}")
