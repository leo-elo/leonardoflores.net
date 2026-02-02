#!/usr/bin/env python3
"""
Update all HTML pages with new header layout and post structure
"""
import re
from pathlib import Path

def update_header_layout(html):
    """Add header-top wrapper and move search bar inline with title"""

    # Pattern to match the current header structure
    old_header_pattern = r'<header>\s*<h1><a href="([^"]+)">Leonardo Flores</a></h1>\s*<p class="tagline">([^<]+)</p>\s*<nav>'

    # Check if already updated
    if '<div class="header-top">' in html:
        return html

    # Find and restructure the header
    def replace_header(match):
        home_link = match.group(1)
        tagline = match.group(2)
        return f'''<header>
        <div class="header-top">
            <h1><a href="{home_link}">Leonardo Flores</a></h1>
            <div class="search-container">
                <input type="search" id="searchInput" placeholder="Search posts..." aria-label="Search posts">
                <div id="searchResults" class="search-results hidden"></div>
            </div>
        </div>
        <p class="tagline">{tagline}</p>
        <nav>'''

    html = re.sub(old_header_pattern, replace_header, html)

    # Remove the old search container from nav
    html = re.sub(r'<div class="search-container">\s*<input type="search"[^>]+>\s*<div id="searchResults"[^>]+></div>\s*</div>\s*', '', html)

    return html

def fix_post_page(html):
    """Fix post pages: move categories to bottom, remove 'Categorized as', header above image"""

    # Extract categories line
    categories_match = re.search(r'<p class="categories">([^<]*(?:<a[^>]*>[^<]*</a>[^<]*)*)</p>', html)
    categories_html = ""

    if categories_match:
        categories_content = categories_match.group(1)
        # Remove "Categorized as" category
        categories_content = re.sub(r'<a href="[^"]*categorized-as[^"]*">Categorized as</a>,?\s*', '', categories_content)
        categories_content = re.sub(r',\s*$', '', categories_content)  # Remove trailing comma
        categories_content = re.sub(r'^,\s*', '', categories_content)  # Remove leading comma
        categories_content = categories_content.strip()

        if categories_content and '<a' in categories_content:
            categories_html = f'<p class="categories post-categories-bottom">Categories: {categories_content}</p>'

        # Remove original categories line
        html = re.sub(r'\s*<p class="categories">[^<]*(?:<a[^>]*>[^<]*</a>[^<]*)*</p>', '', html)

    # Move featured image after post header (title)
    # Current structure might have featured image before title, let's ensure title comes first

    # Extract the post title from the inner article header
    title_match = re.search(r'<header class="post-header"><h1 class="post-title">([^<]+)</h1></header>', html)

    if title_match:
        post_title = title_match.group(1)

        # Remove the inner duplicate header if exists
        html = re.sub(r'<header class="post-header"><h1 class="post-title">[^<]+</h1></header>', '', html)

        # Check if we have a featured image container
        featured_match = re.search(r'(<div class="featured-image-container">.*?</div>)', html, re.DOTALL)

        if featured_match:
            featured_html = featured_match.group(1)
            # Remove featured image from current position
            html = re.sub(r'\s*<div class="featured-image-container">.*?</div>', '', html, flags=re.DOTALL)

            # Insert title header, then featured image after <article>
            html = re.sub(
                r'(<main>\s*<article>)',
                f'\\1\n            <header class="post-header"><h1 class="post-title">{post_title}</h1></header>\n            {featured_html}',
                html
            )
        else:
            # Just add title header
            html = re.sub(
                r'(<main>\s*<article>)',
                f'\\1\n            <header class="post-header"><h1 class="post-title">{post_title}</h1></header>',
                html
            )

    # Add categories at the bottom before </article>
    if categories_html:
        html = re.sub(r'(</div>\s*</article>)', f'{categories_html}\n        \\1', html)

    return html

def process_file(file_path, is_post=False):
    """Process a single HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update header layout
    html = update_header_layout(html)

    # Fix post-specific items
    if is_post:
        html = fix_post_page(html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    """Update all HTML pages"""
    print("Updating all pages...\n")

    # Update main pages
    main_pages = ['index.html', 'about.html', 'calendar.html', 'courses.html', 'publications.html']
    for page in main_pages:
        path = Path(page)
        if path.exists():
            print(f"Updating {page}...")
            process_file(path)

    # Update pagination pages
    for i in range(2, 18):
        path = Path(f'page-{i}.html')
        if path.exists():
            print(f"Updating page-{i}.html...")
            process_file(path)

    # Update blog category pages
    for path in Path('blog/category').glob('*.html'):
        print(f"Updating {path}...")
        process_file(path)

    # Update blog post pages
    for path in Path('posts/blog').rglob('*.html'):
        print(f"Updating {path} (post)...")
        process_file(path, is_post=True)

    print("\n✓ All pages updated")

if __name__ == '__main__':
    main()
