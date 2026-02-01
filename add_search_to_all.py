#!/usr/bin/env python3
"""
Add search bar and script to all HTML files
"""
import re
from pathlib import Path

def add_search_to_html(html_content):
    """Add search bar to navigation and script to body"""

    # Add search container to nav (if not already there)
    if '<div class="search-container">' not in html_content:
        nav_pattern = r'(</nav>)'
        search_html = '''<div class="search-container">
    <input type="search" id="searchInput" placeholder="Search posts..." aria-label="Search posts">
    <div id="searchResults" class="search-results hidden"></div>
</div>
        '''
        html_content = re.sub(nav_pattern, f'{search_html}\n\\1', html_content)

    # Add script before </body> (if not already there)
    if '<script src="js/search.js">' not in html_content and '<script src="../js/search.js">' not in html_content:
        # Determine correct path based on file location
        if '/posts/' in html_content or 'posts/' in html_content:
            script_tag = '<script src="../../js/search.js"></script>'
        elif '/blog/' in html_content or 'blog/' in html_content:
            script_tag = '<script src="../../js/search.js"></script>'
        else:
            script_tag = '<script src="js/search.js"></script>'

        html_content = re.sub(r'(</body>)', f'\n    {script_tag}\n\\1', html_content)

    return html_content

def process_file(file_path):
    """Process a single HTML file"""
    print(f"Processing {file_path}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if no nav element (probably not a full page)
    if '<nav>' not in html:
        print(f"  Skipping (no nav element)")
        return

    updated_html = add_search_to_html(html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print(f"  ✓ Updated")

def main():
    """Add search to all HTML files"""
    print("Adding search functionality to all pages...\n")

    # Process pagination pages
    for i in range(2, 18):
        file_path = Path(f'page-{i}.html')
        if file_path.exists():
            process_file(file_path)

    # Process other top-level pages
    for file_path in Path('.').glob('*.html'):
        if file_path.name.startswith('page-'):
            continue  # Already processed
        if file_path.name == 'index.html':
            continue  # Already has search
        process_file(file_path)

    # Process blog category pages
    for file_path in Path('blog/category').glob('*.html'):
        process_file(file_path)

    print("\n✓ Search functionality added to all pages")

if __name__ == '__main__':
    main()
