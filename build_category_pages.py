#!/usr/bin/env python3
"""
Build category listing pages with all posts in each category
Updated for new category structure
"""
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

CATEGORY_NAMES = {
    'milestones': 'Milestones',
    'presentations': 'Presentations',
    'creative-work': 'Creative Work',
    'teaching': 'Teaching',
    'resources': 'Resources',
}

def convert_url_to_local(wp_url):
    """Convert WordPress URL to local static URL"""
    match = re.search(r'leonardoflores\.net/blog/([^/]+)/([^/]+)/?', wp_url)
    if match:
        category = match.group(1)
        slug = match.group(2)
        return f"posts/blog/{category}/{slug}.html"
    return wp_url

def create_category_page_html(category_slug, category_name, posts):
    """Generate HTML for a category listing page"""

    post_items = []
    for post in posts:
        title = post.get('title', 'Untitled')
        date = post.get('date_display', '')
        url = convert_url_to_local(post.get('url', '#'))

        post_items.append(f'''        <li class="category-post-item">
            <a href="../{url}" class="category-post-link">{title}</a>
            <span class="category-post-date">{date}</span>
        </li>''')

    posts_html = '\n'.join(post_items)

    # Build category nav links
    cat_links = []
    for slug, name in CATEGORY_NAMES.items():
        if slug == category_slug:
            cat_links.append(f'<span class="current-category">{name}</span>')
        else:
            cat_links.append(f'<a href="{slug}.html">{name}</a>')
    cat_nav = ' | '.join(cat_links)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_name} - Leonardo Flores</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="icon" href="../images/wp-content/uploads/2019/08/cropped-leoprofilememefavicon-32x32.png">
    <style>
        .category-posts {{
            list-style: none;
            padding: 0;
            margin: 2rem 0;
        }}
        .category-post-item {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--color-accent);
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        .category-post-link {{
            color: var(--color-primary);
            text-decoration: none;
            font-size: 1.1rem;
            flex: 1;
            min-width: 200px;
        }}
        .category-post-link:hover {{
            text-decoration: underline;
        }}
        .category-post-date {{
            color: var(--color-text-light);
            font-size: 0.9rem;
            white-space: nowrap;
        }}
        .category-count {{
            color: var(--color-text-light);
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }}
        .category-nav {{
            margin-bottom: 2rem;
            padding: 1rem;
            background: var(--color-background-alt);
            border-radius: 8px;
        }}
        .category-nav a {{
            color: var(--color-primary);
            text-decoration: none;
            padding: 0.25rem 0.5rem;
        }}
        .category-nav a:hover {{
            text-decoration: underline;
        }}
        .current-category {{
            font-weight: bold;
            padding: 0.25rem 0.5rem;
        }}
    </style>
</head>
<body>
<header>
        <div class="header-top">
            <h1><a href="../index.html">Leonardo Flores</a></h1>
            <div class="search-container">
                <input type="search" id="searchInput" placeholder="Search posts..." aria-label="Search posts">
                <div id="searchResults" class="search-results hidden"></div>
            </div>
        </div>
        <p class="tagline">Scholar, Academic Leader, Creator</p>
        <nav>
            <a href="../about.html">About</a>
            <a href="../publications.html">CV & Publications</a>
            <a href="../courses.html">Courses</a>
            <a href="https://www.youtube.com/watch?v=qN9fret0PNo">My TEDx Talk</a>
            <a href="mailto:floresll@appstate.edu">Contact</a>
            <a href="../calendar.html">Calendar</a>
            <a href="../post-index.html">Post Index</a>
            <a href="presentations.html">Presentations</a>
            <a href="milestones.html">Milestones</a>
            <a href="teaching.html">Teaching</a>
            <a href="creative-work.html">Creative Work</a>
            <a href="resources.html">Resources</a>
            <a href="en-espanol.html">En Español</a>
        </nav>
    </header>

    <main>
        <h2 style="font-family: var(--font-heading); font-size: 2rem; margin-bottom: 1rem;">{category_name}</h2>
        <p class="category-count">{len(posts)} posts, sorted by date (newest first)</p>

        <div class="category-nav">
            <strong>Categories:</strong> {cat_nav}
        </div>

        <ul class="category-posts">
{posts_html}
        </ul>
    </main>

    <footer>
        <p>&copy; 2026 Leonardo Flores</p>
    </footer>

    <script src="../js/search.js"></script>
</body>
</html>'''

def main():
    """Build all category listing pages"""
    print("Building category listing pages...\n")

    # Load posts data
    with open('all_posts_full.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)

    # Group posts by category
    categories = defaultdict(list)
    for post in posts:
        category = post.get('category', 'milestones')
        categories[category].append(post)

    print(f"Found {len(categories)} categories\n")

    # Remove old category pages
    old_cats = ['news', 'grants', 'publications', 'interviews', 'proposals',
                'editorial-work', 'e-poetry-sites', 'performances', 'courses',
                'pedagogy', 'uncategorized', 'presentations-2']
    for old_cat in old_cats:
        old_file = Path(f'category/{old_cat}.html')
        if old_file.exists():
            old_file.unlink()
            print(f"Removed old category page: {old_file}")

    # Create category directory if needed
    Path('category').mkdir(exist_ok=True)

    # Generate each category page
    for category_slug in CATEGORY_NAMES.keys():
        category_posts = categories.get(category_slug, [])
        category_name = CATEGORY_NAMES[category_slug]

        # Sort by date (newest first)
        def get_sort_date(post):
            dt = post.get('datetime', '')
            if dt:
                try:
                    return datetime.fromisoformat(dt.replace('Z', '+00:00'))
                except:
                    pass
            return datetime.min

        category_posts.sort(key=get_sort_date, reverse=True)

        html = create_category_page_html(category_slug, category_name, category_posts)

        filename = f'category/{category_slug}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"Created {filename} ({len(category_posts)} posts)")

    print(f"\n✓ Category pages built successfully!")

if __name__ == '__main__':
    main()
