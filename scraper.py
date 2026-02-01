#!/usr/bin/env python3
"""
Website scraper for leonardoflores.net
Downloads all pages, assets, and preserves metadata
"""

import os
import re
import json
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
import time

class WebsiteScraper(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.pages = set()
        self.images = set()
        self.styles = set()
        self.scripts = set()
        self.current_page = ''

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'a' and 'href' in attrs_dict:
            href = attrs_dict['href']
            if href.startswith('/') or self.base_url in href:
                self.pages.add(href)

        elif tag == 'img' and 'src' in attrs_dict:
            self.images.add(attrs_dict['src'])

        elif tag == 'link' and 'href' in attrs_dict:
            if attrs_dict.get('rel') in [['stylesheet'], 'stylesheet']:
                self.styles.add(attrs_dict['href'])

        elif tag == 'script' and 'src' in attrs_dict:
            self.scripts.add(attrs_dict['src'])

def download_file(url, filepath):
    """Download a file from URL to filepath"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Download the file
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()

        with open(filepath, 'wb') as f:
            f.write(content)

        print(f"Downloaded: {url} -> {filepath}")
        return True

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def download_page(url):
    """Download a page and return its content"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')

        return content

    except Exception as e:
        print(f"Error downloading page {url}: {e}")
        return None

def normalize_url(url, base_url):
    """Convert relative URLs to absolute URLs"""
    if url.startswith('http'):
        return url
    elif url.startswith('//'):
        return 'https:' + url
    elif url.startswith('/'):
        return base_url.rstrip('/') + url
    else:
        return base_url.rstrip('/') + '/' + url

def url_to_filepath(url, base_url):
    """Convert URL to local filepath"""
    # Remove base URL
    path = url.replace(base_url, '')

    # Remove query strings
    path = path.split('?')[0]

    # Handle root
    if path == '' or path == '/':
        return 'index.html'

    # Remove leading slash
    path = path.lstrip('/')

    # Add .html extension if no extension
    if '.' not in os.path.basename(path):
        path = path.rstrip('/') + '/index.html'

    return path

def main():
    base_url = 'https://leonardoflores.net'
    output_dir = Path('.')

    print(f"Starting scrape of {base_url}")
    print(f"Output directory: {output_dir.absolute()}")

    # Download homepage
    print("\n=== Downloading homepage ===")
    homepage_content = download_page(base_url)

    if not homepage_content:
        print("Failed to download homepage")
        return

    # Save homepage
    homepage_path = output_dir / 'index.html'
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(homepage_content)
    print(f"Saved homepage to {homepage_path}")

    # Parse homepage to find assets
    parser = WebsiteScraper(base_url)
    parser.feed(homepage_content)

    # Download images
    print(f"\n=== Found {len(parser.images)} images ===")
    for img_url in list(parser.images)[:20]:  # Limit to first 20 for now
        full_url = normalize_url(img_url, base_url)
        filepath = output_dir / 'assets' / url_to_filepath(img_url, base_url)
        download_file(full_url, filepath)
        time.sleep(0.5)  # Be nice to the server

    # Download stylesheets
    print(f"\n=== Found {len(parser.styles)} stylesheets ===")
    for style_url in parser.styles:
        full_url = normalize_url(style_url, base_url)
        filepath = output_dir / 'assets' / url_to_filepath(style_url, base_url)
        download_file(full_url, filepath)
        time.sleep(0.5)

    # Download scripts
    print(f"\n=== Found {len(parser.scripts)} scripts ===")
    for script_url in parser.scripts:
        full_url = normalize_url(script_url, base_url)
        filepath = output_dir / 'assets' / url_to_filepath(script_url, base_url)
        download_file(full_url, filepath)
        time.sleep(0.5)

    # Save discovered URLs for reference
    discovered = {
        'pages': list(parser.pages),
        'images': list(parser.images),
        'styles': list(parser.styles),
        'scripts': list(parser.scripts)
    }

    with open(output_dir / 'discovered_urls.json', 'w') as f:
        json.dump(discovered, f, indent=2)

    print(f"\n=== Summary ===")
    print(f"Pages found: {len(parser.pages)}")
    print(f"Images found: {len(parser.images)}")
    print(f"Stylesheets found: {len(parser.styles)}")
    print(f"Scripts found: {len(parser.scripts)}")
    print(f"\nDiscovered URLs saved to discovered_urls.json")

if __name__ == '__main__':
    main()
