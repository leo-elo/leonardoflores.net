#!/usr/bin/env python3
"""
Add Post Index link to all navigation menus
"""
import re
from pathlib import Path

def add_index_link(html, depth=0):
    """Add Post Index link to navigation"""

    if 'post-index.html' in html:
        return html  # Already has link

    # Calculate correct path based on depth
    prefix = '../' * depth

    # Add Post Index link after Calendar
    html = re.sub(
        r'(<a href="[^"]*calendar\.html">Calendar</a>)',
        f'\\1\n            <a href="{prefix}post-index.html">Post Index</a>',
        html
    )

    return html

def process_file(file_path, depth=0):
    """Process a single HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    html = add_index_link(html, depth)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    """Add Post Index link to all pages"""
    print("Adding Post Index link to all pages...\n")

    # Main pages (depth 0)
    for page in Path('.').glob('*.html'):
        if page.name != 'post-index.html':
            print(f"Updating {page}...")
            process_file(page, depth=0)

    # Blog category pages (depth 2: blog/category/)
    for page in Path('blog/category').glob('*.html'):
        print(f"Updating {page}...")
        process_file(page, depth=2)

    # Post pages (depth 3: posts/blog/category/)
    for page in Path('posts/blog').rglob('*.html'):
        print(f"Updating {page}...")
        process_file(page, depth=3)

    print("\n✓ All pages updated with Post Index link")

if __name__ == '__main__':
    main()
