#!/usr/bin/env python3
"""Find working vision models."""
import requests, base64, glob

key = ""
with open('/app/.env') as f:
    for line in f:
        line = line.strip()
        if 'OPENROUTER_API_KEY' in line and '=' in line:
            key = line.split('=', 1)[1].strip()
            break

images = glob.glob('/app/image_cache/*.jpg') or glob.glob('/opt/data/fishing-hk/*.jpg')
with open(images[0], 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

models = [
    "google/gemini-3.1-flash-image",
    "qwen/qwen3-vl-235b-a22b-instruct",
    "openai/gpt-4o-mini",
    "x-ai/grok-4.3",
    "amazon/nova-lite-v1",
    "meta-llama/llama-3.2-11b-vision-instruct",
    "qwen/qwen2.5-vl-72b-instruct",
]

for model in models:
    try:
        resp = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
            json={
                'model': model,
                'messages': [{'role': 'user', 'content': [
                    {'type': 'text', 'text': 'hi'},
                    {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{img_b64[:200]}'}}
                ]}],
                'max_tokens': 20,
            },
            timeout=15
        )
        s = resp.status_code
        e = ""
        if s != 200:
            e = resp.json().get('error', {}).get('message', '')[:60]
        print(f"{s:3d} {model}: {e}")
    except Exception as ex:
        print(f"ERR {model}: {str(ex)[:40]}")
