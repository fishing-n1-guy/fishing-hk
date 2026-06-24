#!/usr/bin/env python3
"""Extract JPEGs from the second PDF (Arcadia Press fish book)."""
import os

pdf_path = '/opt/data/fishing-hk/fish_book.pdf'
out_dir = '/opt/data/fishing-hk/fish_book_images'
os.makedirs(out_dir, exist_ok=True)

with open(pdf_path, 'rb') as f:
    data = f.read()

count = 0
start = 0
while True:
    jpeg_start = data.find(b'\xff\xd8\xff', start)
    if jpeg_start == -1:
        break
    jpeg_end = data.find(b'\xff\xd9', jpeg_start)
    if jpeg_end == -1:
        break
    jpeg_end += 2
    jpeg_data = data[jpeg_start:jpeg_end]
    if len(jpeg_data) > 5000:
        count += 1
        out_path = f'{out_dir}/img_{count}.jpg'
        with open(out_path, 'wb') as jpg:
            jpg.write(jpeg_data)
        print(f"  Image {count}: {len(jpeg_data)} bytes")
    start = jpeg_end

print(f"\nTotal: {count} images extracted to {out_dir}")
