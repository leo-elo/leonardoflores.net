#!/usr/bin/env python3
"""
Download all images from scraped pages
"""

import os
import json
import urllib.request
from pathlib import Path
import time
import re

def download_file(url, filepath):
    """Download a file from URL"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()

        with open(filepath, 'wb') as f:
            f.write(content)

        print(f"Downloaded: {filepath}")
        return True

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def extract_images_from_html(html_file):
    """Extract all image URLs from an HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all img src attributes
    img_pattern = r'<img[^>]+src=["\'](https://leonardoflores\.net/[^"\']+)["\']'
    images = re.findall(img_pattern, content)

    # Also find favicon and other icons
    icon_pattern = r'href=["\'](https://leonardoflores\.net/[^"\']+\.(?:png|jpg|jpeg|ico|svg))["\']'
    icons = re.findall(icon_pattern, content)

    return list(set(images + icons))

def main():
    # Find all downloaded HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    print(f"Found {len(html_files)} HTML files")

    # Extract all image URLs
    all_images = set()
    for html_file in html_files:
        images = extract_images_from_html(html_file)
        all_images.update(images)
        if images:
            print(f"{html_file}: {len(images)} images")

    print(f"\nTotal unique images: {len(all_images)}")

    # Download images
    downloaded = 0
    for img_url in sorted(all_images):
        # Convert URL to local path
        path = img_url.replace('https://leonardoflores.net/', '')
        local_path = os.path.join('images', path)

        # Skip if already exists
        if os.path.exists(local_path):
            print(f"Already exists: {local_path}")
            continue

        # Download
        if download_file(img_url, local_path):
            downloaded += 1
            time.sleep(0.3)  # Be nice to the server

    print(f"\n=== Summary ===")
    print(f"Downloaded {downloaded} new images")
    print(f"Total images: {len(all_images)}")

if __name__ == '__main__':
    main()
