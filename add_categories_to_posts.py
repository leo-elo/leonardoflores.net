#!/usr/bin/env python3
"""
Add category listings to all blog posts
"""
import re
from pathlib import Path

CATEGORIES = {
    'presentations': 'Presentations',
    'news': 'News',
    'teaching': 'Teaching',
    'creative-work': 'Creative Work',
    'resources': 'Resources',
    'en-espanol': 'En Español',
}

def get_category_from_path(file_path):
    """Extract category from file path"""
    parts = str(file_path).split('/')
    for i, part in enumerate(parts):
        if part == 'blog' and i + 1 < len(parts):
            return parts[i + 1]
    return None

def add_categories_to_post(file_path):
    """Add category listing to a single post"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has categories
    if 'post-categories-bottom' in content:
        return False

    # Get category from path
    category = get_category_from_path(file_path)
    if not category or category not in CATEGORIES:
        return False

    # Create category HTML
    cat_name = CATEGORIES[category]
    category_html = f'<p class="categories post-categories-bottom">Categories: <a href="../../../category/{category}.html">{cat_name}</a></p>'

    # Find where to insert - before </div> that closes entry-content or post-content
    # Look for the closing of entry-content div
    patterns = [
        (r'(</div>\s*</div>\s*</article>)', f'{category_html}\n                \\1'),
        (r'(</div>\s*</article>)', f'{category_html}\n            \\1'),
    ]

    new_content = content
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content, count=1)
            break

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False

def main():
    print("Adding categories to posts...\n")

    updated = 0
    skipped = 0

    for html_file in Path('posts/blog').rglob('*.html'):
        if add_categories_to_post(html_file):
            print(f"  + {html_file}")
            updated += 1
        else:
            skipped += 1

    print(f"\n+ Added categories to {updated} posts")
    print(f"  Skipped {skipped} posts (already have categories)")

if __name__ == '__main__':
    main()
