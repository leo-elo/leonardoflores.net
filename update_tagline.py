#!/usr/bin/env python3
"""
Update the tagline/subtitle across all files
"""
from pathlib import Path

OLD_TAGLINE = "Scholar, Academic Leader, Creator"
NEW_TAGLINE = "Scholar, Academic Leader, Creator"

def update_tagline(file_path):
    """Update tagline in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if OLD_TAGLINE not in content:
        return False

    new_content = content.replace(OLD_TAGLINE, NEW_TAGLINE)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    """Update tagline on all files"""
    print(f"Updating tagline to: {NEW_TAGLINE}\n")

    base_dir = Path('.')
    updated = 0

    # Find all HTML and Python files
    files = list(base_dir.glob('*.html'))
    files.extend(base_dir.glob('*.py'))
    files.extend(base_dir.glob('category/*.html'))
    files.extend(base_dir.glob('posts/blog/**/*.html'))

    for file_path in files:
        if update_tagline(file_path):
            print(f"  ✓ Updated: {file_path}")
            updated += 1

    print(f"\n✓ Updated {updated} files")

if __name__ == '__main__':
    main()
