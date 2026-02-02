#!/usr/bin/env python3
"""
Add 'En Español' link to navigation on all pages
"""
import re
from pathlib import Path

def get_relative_path(html_file, target):
    """Get relative path from html_file to target"""
    html_path = Path(html_file)

    # Determine depth
    if html_path.parent.name == 'leonardoflores-static':
        # Root level: index.html, about.html, page-*.html, post-index.html
        return f"category/{target}"
    elif html_path.parent.name == 'category':
        # Category level: category/*.html
        return target
    elif 'posts/blog' in str(html_path):
        # Post level: posts/blog/category/post.html
        return f"../../../category/{target}"
    else:
        return f"category/{target}"

def add_spanish_nav(html_file):
    """Add En Español link to navigation if not present"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has En Español link
    if 'en-espanol' in content.lower():
        return False

    # Get the correct relative path
    espanol_path = get_relative_path(html_file, 'en-espanol.html')

    # Find the resources link and add En Español after it
    # Pattern: <a href="...resources.html">Resources</a>
    pattern = r'(<a href="[^"]*resources\.html">Resources</a>)'
    replacement = r'\1\n            <a href="' + espanol_path + r'">En Español</a>'

    new_content = re.sub(pattern, replacement, content)

    if new_content == content:
        # Try alternative pattern without the path
        pattern = r'(Resources</a>)(\s*</nav>)'
        replacement = r'\1\n            <a href="' + espanol_path + r'">En Español</a>\2'
        new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False

def main():
    """Add En Español link to all HTML pages"""
    print("Adding 'En Español' link to navigation...\n")

    base_dir = Path('.')
    updated = 0
    skipped = 0

    # Find all HTML files
    html_files = list(base_dir.glob('*.html'))
    html_files.extend(base_dir.glob('category/*.html'))
    html_files.extend(base_dir.glob('posts/blog/**/*.html'))

    for html_file in html_files:
        if add_spanish_nav(html_file):
            print(f"  ✓ Updated: {html_file}")
            updated += 1
        else:
            skipped += 1

    print(f"\n✓ Updated {updated} files")
    print(f"  Skipped {skipped} files (already had link)")

if __name__ == '__main__':
    main()
