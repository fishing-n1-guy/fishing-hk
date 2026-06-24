#!/usr/bin/env python3
"""Extract images from the fish identification PDF and save them."""
import subprocess, os, json

pdf_path = '/opt/data/fishing-hk/fish_guide.pdf'
out_dir = '/opt/data/fishing-hk/fish_guide_images'
os.makedirs(out_dir, exist_ok=True)

# Use pdftoimage (poppler-utils) to extract images
try:
    result = subprocess.run(['which', 'pdftoimage'], capture_output=True, text=True, timeout=5)
    if result.returncode != 0:
        print("pdftoimage not found, trying to install...")
        subprocess.run(['apt-get', 'install', '-y', 'poppler-utils'], capture_output=True, timeout=30)
except:
    print("Could not install poppler-utils")

# Try pip install pdf2image
try:
    import pdf2image
    from pdf2image import convert_from_path
    
    print("Converting PDF to images...")
    # Convert first 10 pages to see what's there
    images = convert_from_path(pdf_path, first_page=1, last_page=10, dpi=150)
    for i, img in enumerate(images):
        img_path = f'{out_dir}/page_{i+1}.png'
        img.save(img_path, 'PNG')
        print(f"  Saved page {i+1}: {img_path}")
        if i >= 5:  # Just first 6 pages
            break
    print(f"\nExtracted {len(images)} pages")
except ImportError:
    print("pdf2image not installed, trying to install...")
    subprocess.run(['pip3', 'install', 'pdf2image'], capture_output=True, timeout=30)
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, first_page=1, last_page=10, dpi=150)
        for i, img in enumerate(images):
            img_path = f'{out_dir}/page_{i+1}.png'
            img.save(img_path, 'PNG')
            print(f"  Saved page {i+1}: {img_path}")
    except Exception as e:
        print(f"Error: {e}")
