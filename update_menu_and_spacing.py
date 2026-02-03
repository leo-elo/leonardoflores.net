#!/usr/bin/env python3
"""
1. Remove Courses and My TEDx Talk from menu
2. Rename Post Index to Index
3. Fix spacing before italicized/linked text
"""
import re
from pathlib import Path

def update_file(file_path):
    """Update menu and fix spacing in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove Courses link from navigation
    content = re.sub(r'\s*<a href="[^"]*courses\.html">Courses</a>', '', content)

    # Remove My TEDx Talk link from navigation
    content = re.sub(r'\s*<a href="https://www\.youtube\.com/watch\?v=qN9fret0PNo">My TEDx Talk</a>', '', content)

    # Rename Post Index to Index in navigation
    content = re.sub(r'>Post Index<', '>Index<', content)

    # Rename post-index.html page title
    content = re.sub(r'<title>Post Index', '<title>Index', content)
    content = re.sub(r'>Post Index<', '>Index<', content)

    # Fix spacing before italicized/linked text (missing space before <i>, <em>, <a>)
    # Pattern: word character followed directly by opening tag without space
    content = re.sub(r'(\w)((?:<(?:i|em|a)[^>]*>))', r'\1 \2', content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Update all HTML files"""
    print("Updating menu and fixing spacing...\n")

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
