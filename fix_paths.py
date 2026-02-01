#!/usr/bin/env python3
"""
Fix paths in generated HTML files
"""

import os
import re
from pathlib import Path

def count_directory_levels(filepath):
    """Count how many directories deep a file is from site/"""
    parts = Path(filepath).parts
    # site/posts/blog/presentations-2/file.html = 3 levels deep
    # site/index.html = 0 levels deep
    if 'site' in parts:
        idx = parts.index('site')
        return len(parts) - idx - 2  # -2 for 'site' and filename

    return 0

def fix_html_file(filepath):
    """Fix paths in a single HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count directory depth
    depth = count_directory_levels(filepath)
    prefix = '../' * depth if depth > 0 else ''

    # Fix image paths
    # From: src="../wp-content/ or src="wp-content/
    # To: src="../../../images/wp-content/ (or appropriate depth)
    content = re.sub(
        r'src="(?:\.\.\/)*wp-content\/',
        f'src="{prefix}images/wp-content/',
        content
    )

    # Fix category links
    # From: href="../category/
    # To: href="../../blog/category/ (or appropriate depth)
    content = re.sub(
        r'href="(?:\.\.\/)*category\/',
        f'href="{prefix}blog/category/',
        content
    )

    # Clean up WordPress wrapper divs
    content = re.sub(r'<div id="primary">', '', content)
    content = re.sub(r'<main id="main">', '', content)
    content = re.sub(r'<article id="post-\d+">', '', content)
    content = re.sub(r'</article>\s*</main>', '</article>', content)

    # Fix broken category names
    content = re.sub(r'<a href="[^"]+/categorized-as\.html">Categorized as</a>,?\s*', '', content)
    content = re.sub(r'Categories:\s*,\s*', 'Categories: ', content)
    content = re.sub(r',\s*,', ',', content)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    """Fix all HTML files in site directory"""
    html_files = []

    for root, dirs, files in os.walk('site'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    print(f"Found {len(html_files)} HTML files to fix")

    for filepath in html_files:
        fix_html_file(filepath)
        print(f"Fixed: {filepath}")

    print(f"\nDone! Fixed {len(html_files)} files")

if __name__ == '__main__':
    main()
