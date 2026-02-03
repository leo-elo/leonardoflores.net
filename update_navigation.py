#!/usr/bin/env python3
"""
Update navigation menu across all pages with new category links
"""
import re
from pathlib import Path

def get_nav_html(depth=0):
    """Generate navigation HTML with correct paths based on depth"""
    prefix = '../' * depth

    return f'''<nav>
            <a href="{prefix}about.html">About</a>
            <a href="{prefix}courses.html">Courses</a>
            <a href="https://www.youtube.com/watch?v=qN9fret0PNo">My TEDx Talk</a>
            <a href="{prefix}calendar.html">Calendar</a>
            <a href="{prefix}post-index.html">Post Index</a>
            <a href="{prefix}category/presentations.html">Presentations</a>
            <a href="{prefix}category/milestones.html">Milestones</a>
            <a href="{prefix}category/teaching.html">Teaching</a>
            <a href="{prefix}category/creative-work.html">Creative Work</a>
            <a href="{prefix}category/resources.html">Resources</a>
            <a href="{prefix}category/en-espanol.html">En Español</a>
        </nav>'''

def update_page_nav(file_path, depth=0):
    """Update navigation in a single page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace the entire nav element
    new_nav = get_nav_html(depth)
    html = re.sub(r'<nav>.*?</nav>', new_nav, html, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    """Update navigation on all pages"""
    print("Updating navigation on all pages...\n")

    # Main pages (depth 0)
    main_pages = ['index.html', 'about.html', 'calendar.html', 'courses.html',
                  'publications.html', 'post-index.html']
    for page in main_pages:
        path = Path(page)
        if path.exists():
            print(f"Updating {page} (depth 0)...")
            update_page_nav(path, depth=0)

    # Pagination pages (depth 0)
    for i in range(2, 15):
        path = Path(f'page-{i}.html')
        if path.exists():
            print(f"Updating page-{i}.html (depth 0)...")
            update_page_nav(path, depth=0)

    # Category pages (depth 1: category/)
    for path in Path('category').glob('*.html'):
        print(f"Updating {path} (depth 1)...")
        update_page_nav(path, depth=1)

    # Blog category pages if they exist (depth 2: blog/category/)
    blog_cat = Path('blog/category')
    if blog_cat.exists():
        for path in blog_cat.glob('*.html'):
            print(f"Updating {path} (depth 2)...")
            update_page_nav(path, depth=2)

    # Post pages (depth 3: posts/blog/category/)
    for path in Path('posts/blog').rglob('*.html'):
        print(f"Updating {path} (depth 3)...")
        update_page_nav(path, depth=3)

    print("\n✓ Navigation updated on all pages")

if __name__ == '__main__':
    main()
