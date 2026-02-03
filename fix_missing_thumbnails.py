#!/usr/bin/env python3
"""
Replace placeholder thumbnails with leomatrix.jpg
"""
import re
from pathlib import Path

# The placeholder pattern to replace
PLACEHOLDER_PATTERN = r'''<div class="post-thumbnail-placeholder">\s*<span class="placeholder-icon">📄</span>\s*</div>'''

# The replacement with actual image
REPLACEMENT = '''<figure class="post-thumbnail">
            <img src="images/wp-content/uploads/leomatrix.jpg"
                 alt="Leonardo Flores"
                 class="post-thumbnail-image"
                 loading="lazy">
        </figure>'''

def fix_file(file_path):
    """Replace placeholders in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count replacements
    count = len(re.findall(PLACEHOLDER_PATTERN, content))

    if count == 0:
        return 0

    # Replace placeholders
    new_content = re.sub(PLACEHOLDER_PATTERN, REPLACEMENT, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return count

def main():
    print("Fixing missing thumbnails with leomatrix.jpg...\n")

    total_fixed = 0

    # Fix pagination pages
    for i in range(2, 15):
        page_file = Path(f'page-{i}.html')
        if page_file.exists():
            count = fix_file(page_file)
            if count > 0:
                print(f"  + {page_file}: fixed {count} thumbnails")
                total_fixed += count

    # Also check index.html just in case
    if Path('index.html').exists():
        count = fix_file('index.html')
        if count > 0:
            print(f"  + index.html: fixed {count} thumbnails")
            total_fixed += count

    print(f"\n+ Fixed {total_fixed} missing thumbnails")

if __name__ == '__main__':
    main()
