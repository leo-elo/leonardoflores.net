#!/usr/bin/env python3
"""
Update all HTML pages with the new header structure (hamburger menu, search after tagline)
"""
import re
from pathlib import Path

def get_prefix(html_file):
    """Get the correct path prefix based on file location"""
    html_path = Path(html_file)

    if html_path.parent.name == 'leonardoflores-static':
        return ''
    elif html_path.parent.name == 'category':
        return '../'
    elif 'posts/blog' in str(html_path):
        return '../../../'
    else:
        return ''

def update_header(html_file):
    """Update header structure in a single file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has menu-toggle
    if 'menu-toggle' in content:
        return False

    prefix = get_prefix(html_file)

    # Pattern to match old header structure
    old_header_pattern = r'<header>\s*<div class="header-top">\s*<h1><a href="([^"]+)">Leonardo Flores</a></h1>\s*<div class="search-container">\s*<input type="search" id="searchInput" placeholder="Search posts\.\.\." aria-label="Search posts">\s*<div id="searchResults" class="search-results hidden"></div>\s*</div>\s*</div>\s*<p class="tagline">([^<]+)</p>\s*<nav>'

    new_header = f'''<header>
        <div class="header-top">
            <div class="header-title-menu">
                <h1><a href="{prefix}index.html">Leonardo Flores</a></h1>
                <button class="menu-toggle" aria-label="Toggle menu">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </div>
        <p class="tagline">Scholar, Academic Leader, Creator</p>
        <div class="search-container">
            <input type="search" id="searchInput" placeholder="Search posts..." aria-label="Search posts">
            <div id="searchResults" class="search-results hidden"></div>
        </div>
        <nav>'''

    new_content = re.sub(old_header_pattern, new_header, content, flags=re.DOTALL)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False

def main():
    """Update headers on all HTML pages"""
    print("Updating headers with hamburger menu...\n")

    base_dir = Path('.')
    updated = 0
    skipped = 0

    # Find all HTML files
    html_files = list(base_dir.glob('*.html'))
    html_files.extend(base_dir.glob('category/*.html'))
    html_files.extend(base_dir.glob('posts/blog/**/*.html'))

    for html_file in html_files:
        if update_header(html_file):
            print(f"  ✓ Updated: {html_file}")
            updated += 1
        else:
            skipped += 1

    print(f"\n✓ Updated {updated} files")
    print(f"  Skipped {skipped} files (already had menu or no match)")

if __name__ == '__main__':
    main()
