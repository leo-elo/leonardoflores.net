#!/usr/bin/env python3
"""
Remove CV & Publications and Contact links from navigation
"""
import re
from pathlib import Path

def update_nav(file_path):
    """Remove CV & Publications and Contact links from navigation"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove CV & Publications link (handles different path prefixes)
    content = re.sub(r'\s*<a href="[^"]*publications\.html">CV & Publications</a>\n?', '', content)

    # Remove Contact mailto link
    content = re.sub(r'\s*<a href="mailto:floresll@appstate\.edu">Contact</a>\n?', '', content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Update navigation on all files"""
    print("Removing CV & Publications and Contact from navigation...\n")

    base_dir = Path('.')
    updated = 0

    # Find all HTML files
    files = list(base_dir.glob('*.html'))
    files.extend(base_dir.glob('category/*.html'))
    files.extend(base_dir.glob('posts/blog/**/*.html'))

    for file_path in files:
        if update_nav(file_path):
            print(f"  ✓ Updated: {file_path}")
            updated += 1

    print(f"\n✓ Updated {updated} files")

if __name__ == '__main__':
    main()
