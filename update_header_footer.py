#!/usr/bin/env python3
"""
Remove search from header and update footer with new design
"""
import re
from pathlib import Path

NEW_FOOTER = '''    <footer>
        <div class="footer-content">
            <div class="footer-left">© 2026 Leonardo Flores</div>
            <div class="footer-center"><a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC-BY 4.0</a></div>
            <div class="footer-right">
                <div class="search-container">
                    <input type="search" id="footerSearchInput" placeholder="Search posts..." aria-label="Search posts">
                    <div id="searchResults" class="search-results hidden"></div>
                </div>
            </div>
        </div>
    </footer>'''

def update_file(file_path):
    """Remove search from header and update footer"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove search container from header
    content = re.sub(
        r'\s*<div class="search-container">\s*<input type="search" id="searchInput" placeholder="Search posts\.\.\." aria-label="Search posts">\s*<div id="searchResults" class="search-results hidden"></div>\s*</div>',
        '',
        content
    )

    # Replace old footer with new footer
    content = re.sub(
        r'<footer>\s*<p>&copy; 2026 Leonardo Flores</p>\s*</footer>',
        NEW_FOOTER,
        content
    )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Update all HTML files"""
    print("Updating header and footer...\n")

    base_dir = Path('.')
    updated = 0

    # Find all HTML files
    files = list(base_dir.glob('*.html'))
    files.extend(base_dir.glob('category/*.html'))
    files.extend(base_dir.glob('posts/blog/**/*.html'))

    for file_path in files:
        if update_file(file_path):
            print(f"  ✓ Updated: {file_path}")
            updated += 1

    print(f"\n✓ Updated {updated} files")

if __name__ == '__main__':
    main()
