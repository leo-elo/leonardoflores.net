#!/usr/bin/env python3
"""
Build category listing pages with all posts in each category
"""
import json
import re
from pathlib import Path
from collections import defaultdict

def convert_url_to_local(wp_url):
    """Convert WordPress URL to local static URL"""
    match = re.search(r'leonardoflores\.net/blog/([^/]+)/([^/]+)/?', wp_url)
    if match:
        category = match.group(1)
        slug = match.group(2)
        return f"posts/blog/{category}/{slug}.html"
    return wp_url

def extract_category(wp_url):
    """Extract category from WordPress URL"""
    match = re.search(r'leonardoflores\.net/blog/([^/]+)/', wp_url)
    if match:
        return match.group(1)
    return 'uncategorized'

def format_category_name(slug):
    """Convert slug to display name"""
    names = {
        'presentations-2': 'Presentations',
        'news': 'News',
        'creative-work': 'Creative Work',
        'publications': 'Publications',
        'pedagogy': 'Pedagogy',
        'interviews': 'Interviews',
        'editorial-work': 'Editorial Work',
        'grants': 'Grants',
        'courses': 'Courses',
    }
    return names.get(slug, slug.replace('-', ' ').title())

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
            margin-bottom: 2rem;
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
        <p class="tagline">Professor & Chair, Department of English at Appalachian State University</p>
        <nav>
            <a href="../about.html">About</a>
            <a href="../publications.html">CV & Publications</a>
            <a href="creative-work.html">Creative Work</a>
            <a href="../courses.html">Courses</a>
            <a href="https://www.youtube.com/watch?v=qN9fret0PNo">My TEDx Talk</a>
            <a href="mailto:floresll@appstate.edu">Contact</a>
            <a href="../calendar.html">Calendar</a>
            <a href="../post-index.html">Post Index</a>
        </nav>
    </header>

    <main>
        <h2 style="font-family: var(--font-heading); font-size: 2rem; margin-bottom: 1rem;">{category_name}</h2>
        <p class="category-count">{len(posts)} posts in this category, sorted by date (newest first)</p>

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
        category = extract_category(post.get('url', ''))
        categories[category].append(post)

    print(f"Found {len(categories)} categories\n")

    # Create category directory if needed
    Path('category').mkdir(exist_ok=True)

    # Generate each category page
    for category_slug, category_posts in categories.items():
        category_name = format_category_name(category_slug)

        # Sort by date (newest first)
        from datetime import datetime
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
