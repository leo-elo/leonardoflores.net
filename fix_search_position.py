#!/usr/bin/env python3
"""
Fix search bar position - add it to header-top div
"""
import re
from pathlib import Path

def fix_search_in_header(html):
    """Add search bar inside header-top div after h1"""

    # Check if search is already in header-top
    if '<div class="header-top">' in html and '<div class="search-container">' in html:
        # Check if search is inside header-top (not in nav)
        header_top_match = re.search(r'<div class="header-top">(.*?)</div>', html, re.DOTALL)
        if header_top_match and 'search-container' in header_top_match.group(1):
            return html  # Already fixed

    # Pattern: header-top with just h1
    pattern = r'(<div class="header-top">)\s*(<h1><a href="[^"]+">Leonardo Flores</a></h1>)\s*(</div>)'

    search_html = '''
            <div class="search-container">
                <input type="search" id="searchInput" placeholder="Search posts..." aria-label="Search posts">
                <div id="searchResults" class="search-results hidden"></div>
            </div>
        '''

    html = re.sub(
        pattern,
        f'\\1\n            \\2{search_html}\\3',
        html
    )

    return html

def process_file(file_path):
    """Process a single HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    html = fix_search_in_header(html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    """Fix all HTML pages"""
    print("Fixing search bar position...\n")

    # All HTML files
    all_html = list(Path('.').glob('*.html')) + \
               list(Path('blog/category').glob('*.html')) + \
               list(Path('posts/blog').rglob('*.html'))

    for path in all_html:
        if path.exists():
            print(f"Fixing {path}...")
            process_file(path)

    print("\n✓ All pages fixed")

if __name__ == '__main__':
    main()
