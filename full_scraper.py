#!/usr/bin/env python3
"""
Complete website scraper for leonardoflores.net
Downloads all pages, posts, assets, and extracts metadata
"""

import os
import re
import json
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
import time
from collections import defaultdict

class PageParser(HTMLParser):
    """Parser to extract content and metadata from HTML pages"""

    def __init__(self):
        super().__init__()
        self.title = ''
        self.content = []
        self.categories = []
        self.images = []
        self.in_title = False
        self.in_content = False
        self.in_category = False
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.current_tag = tag

        if tag == 'title':
            self.in_title = True

        # WordPress main content area
        if attrs_dict.get('id') == 'primary' or attrs_dict.get('class', '').find('entry-content') != -1:
            self.in_content = True

        # Categories
        if 'category' in attrs_dict.get('class', ''):
            self.in_category = True

        # Images
        if tag == 'img' and 'src' in attrs_dict:
            self.images.append(attrs_dict['src'])

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag in ['article', 'main']:
            self.in_content = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_content and data.strip():
            self.content.append(data.strip())
        if self.in_category and data.strip():
            self.categories.append(data.strip())

def download_url(url, max_retries=3):
    """Download a URL with retry logic"""
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()

                # Handle different content types
                content_type = response.headers.get('Content-Type', '')
                if 'text' in content_type or 'html' in content_type:
                    try:
                        return content.decode('utf-8')
                    except:
                        return content.decode('latin-1')
                else:
                    return content

        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return None

    return None

def save_file(filepath, content):
    """Save content to file"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        if isinstance(content, str):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            with open(filepath, 'wb') as f:
                f.write(content)

        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def url_to_path(url, base_url):
    """Convert URL to local path"""
    path = url.replace(base_url, '').lstrip('/')

    # Remove query parameters
    path = path.split('?')[0].split('#')[0]

    # If empty, it's the homepage
    if not path:
        return 'index.html'

    # If no extension, treat as directory with index.html
    if '.' not in os.path.basename(path):
        path = path.rstrip('/') + '.html'

    return path

def main():
    base_url = 'https://leonardoflores.net'

    # Key pages to download
    key_pages = [
        '/about/',
        '/publications/',
        '/courses/',
        '/calendar/',
        '/blog/category/creative-work/',
        '/blog/category/presentations-2/',
        '/blog/category/publications/',
        '/blog/category/news/',
        '/blog/category/pedagogy/',
        '/blog/category/courses/',
        '/blog/category/editorial-work/',
        '/blog/category/grants/',
        '/blog/category/interviews/',
    ]

    # Load discovered URLs
    with open('discovered_urls.json', 'r') as f:
        discovered = json.load(f)

    metadata = {
        'pages': {},
        'categories': defaultdict(list),
        'archives': defaultdict(list)
    }

    print("=== Downloading key pages ===")
    for page_path in key_pages:
        url = base_url + page_path
        print(f"Downloading: {url}")

        content = download_url(url)
        if content:
            # Save raw HTML
            filepath = 'pages/' + url_to_path(url, base_url)
            save_file(filepath, content)

            # Parse and extract metadata
            parser = PageParser()
            parser.feed(content)

            metadata['pages'][page_path] = {
                'title': parser.title.strip(),
                'url': url,
                'filepath': filepath,
                'images': parser.images,
                'categories': parser.categories
            }

            print(f"  Saved to: {filepath}")
            print(f"  Title: {parser.title.strip()}")

        time.sleep(1)  # Be nice to the server

    print(f"\n=== Downloading recent blog posts ===")
    # Download some recent posts
    recent_posts = [
        '/blog/presentations-2/leo-mla-2026-convention/',
        '/blog/news/leo-isea-2025-seoul/',
        '/blog/presentations-2/presentations-at-the-elo-2025-conference/',
        '/blog/news/public-lecture-the-importance-of-digital-writing-in-the-age-of-ai/',
        '/blog/presentations-2/invited-lecture-dr-cyberleo-or-how-i-learned-to-stop-worrying-and-love-ai/',
        '/blog/news/leo-iit-jodhpur/',
        '/blog/presentations-2/keynote-peering-through-the-cloud-finding-our-way-with-ai-at-app-state/',
        '/blog/presentations-2/webinar-technology-and-evolving-research-practices-in-the-humanities/',
        '/blog/presentations-2/taller-ymaquina-programacion-de-literatura-electronica-con-ia/',
        '/blog/presentations-2/presentacion-la-literatura-electronica-y-su-adopcion-social/',
    ]

    for post_path in recent_posts:
        url = base_url + post_path
        print(f"Downloading post: {url}")

        content = download_url(url)
        if content:
            filepath = 'posts/' + url_to_path(url, base_url)
            save_file(filepath, content)

            # Parse metadata
            parser = PageParser()
            parser.feed(content)

            metadata['pages'][post_path] = {
                'title': parser.title.strip(),
                'url': url,
                'filepath': filepath,
                'type': 'post',
                'categories': parser.categories
            }

            # Categorize
            for cat in parser.categories:
                metadata['categories'][cat].append(post_path)

            print(f"  Saved to: {filepath}")

        time.sleep(1)

    # Save metadata
    with open('metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\n=== Summary ===")
    print(f"Key pages downloaded: {len([p for p in metadata['pages'] if 'posts/' not in metadata['pages'][p].get('filepath', '')])}")
    print(f"Blog posts downloaded: {len([p for p in metadata['pages'] if 'posts/' in metadata['pages'][p].get('filepath', '')])}")
    print(f"Categories found: {len(metadata['categories'])}")
    print(f"\nMetadata saved to metadata.json")

if __name__ == '__main__':
    main()
