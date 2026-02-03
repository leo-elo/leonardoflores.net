#!/usr/bin/env python3
"""
Update header structure: move tagline into header-title-menu, position hamburger on right
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

def update_file(file_path):
    """Update header structure in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    prefix = get_prefix(file_path)

    # Pattern to match the old header structure
    old_pattern = r'''<header>
        <div class="header-top">
            <div class="header-title-menu">
                <h1><a href="[^"]*index\.html">Leonardo Flores</a></h1>
                <button class="menu-toggle" aria-label="Toggle menu">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </div>
        <p class="tagline">Scholar, Academic Leader, Creator</p>'''

    # New structure with tagline in header-title-menu and hamburger on right
    new_structure = f'''<header>
        <div class="header-top">
            <div class="header-title-menu">
                <h1><a href="{prefix}index.html">Leonardo Flores</a></h1>
                <p class="tagline">Scholar, Academic Leader, Creator</p>
            </div>
            <button class="menu-toggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>'''

    new_content = re.sub(old_pattern, new_structure, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """Update all HTML files"""
    print("Updating header structure...\n")

    base_dir = Path('.')
    updated = 0

    # Find all HTML files
    files = list(base_dir.glob('*.html'))
    files.extend(base_dir.glob('category/*.html'))
    files.extend(base_dir.glob('posts/blog/**/*.html'))

    for file_path in sorted(files):
        if update_file(file_path):
            print(f"  + {file_path}")
            updated += 1

    print(f"\n+ Updated {updated} files")

if __name__ == '__main__':
    main()
