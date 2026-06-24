#!/usr/bin/env python3
"""Extract text from fish PDF to get fish names."""
import subprocess, os

pdf = '/opt/data/fishing-hk/fish_guide.pdf'

# Try reading the PDF as text (simple extract)
try:
    # Use python's built-in to read raw bytes and extract text
    with open(pdf, 'rb') as f:
        data = f.read()
    
    # Extract text between parentheses (PDF text objects)
    texts = []
    i = 0
    while i < len(data):
        # Find text between parentheses
        if data[i:i+1] == b'(':
            j = i + 1
            depth = 0
            while j < len(data):
                if data[j:j+1] == b'(' and data[j-1:j] != b'\\':
                    depth += 1
                elif data[j:j+1] == b')' and data[j-1:j] != b'\\':
                    if depth == 0:
                        break
                    depth -= 1
                j += 1
            text = data[i+1:j].decode('latin-1', errors='replace')
            if len(text) > 1 and any(c.isalpha() for c in text):
                texts.append(text)
            i = j
        i += 1
    
    # Print unique fish names found
    seen = set()
    for t in texts:
        t2 = t.replace('\\', '')
        if len(t2) > 1 and len(t2) < 50:
            if t2 not in seen:
                seen.add(t2)
                print(t2)
except Exception as e:
    print(f"Error: {e}")
