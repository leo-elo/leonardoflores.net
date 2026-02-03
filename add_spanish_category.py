#!/usr/bin/env python3
"""
Add 'En Español' category for Spanish language posts
"""
import json
import re
from pathlib import Path
from datetime import datetime

# Spanish keywords to identify posts
SPANISH_KEYWORDS = [
    'español', 'presentación', 'taller', 'literatura electrónica',
    'ponencia', 'en español', 'curso', 'publicaciones y entrevistas en español',
    'reinventando la literatura', 'congreso de educación'
]

def is_spanish_post(title):
    """Check if a post is in Spanish based on title"""
    title_lower = title.lower()
    return any(kw in title_lower for kw in SPANISH_KEYWORDS)

def create_spanish_category_page(posts):
    """Create the En Español category page"""

    # Sort by date (newest first)
    def get_sort_date(post):
        dt = post.get('datetime', '')
        if dt:
            try:
                return datetime.fromisoformat(dt.replace('Z', '+00:00'))
            except:
                pass
        return datetime.min

    posts.sort(key=get_sort_date, reverse=True)

    # Generate post list
    post_items = []
    for post in posts:
        title = post.get('title', 'Untitled')
        date = post.get('date_display', '')

        # Get local URL
        url = post.get('url', '')
        match = re.search(r'leonardoflores\.net/blog/([^/]+)/([^/]+)/?', url)
        if match:
            category = match.group(1)
            slug = match.group(2)
            # Map to new category
            CATEGORY_MAP = {
                'news': 'milestones', 'grants': 'milestones', 'publications': 'milestones',
                'interviews': 'milestones', 'proposals': 'milestones', 'editorial-work': 'milestones',
                'e-poetry-sites': 'resources', 'performances': 'creative-work',
                'courses': 'teaching', 'pedagogy': 'teaching',
                'presentations-2': 'presentations', 'uncategorized': 'milestones',
            }
            new_category = CATEGORY_MAP.get(category, category)
            local_url = f"../posts/blog/{new_category}/{slug}.html"
        else:
            local_url = '#'

        post_items.append(f'''        <li class="category-post-item">
            <a href="{local_url}" class="category-post-link">{title}</a>
            <span class="category-post-date">{date}</span>
        </li>''')

    posts_html = '\n'.join(post_items)

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>En Español - Leonardo Flores</title>
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
        <p class="tagline">Scholar, Academic Leader, Creator</p>
        <nav>
            <a href="../about.html">About</a>
            <a href="../courses.html">Courses</a>
            <a href="https://www.youtube.com/watch?v=qN9fret0PNo">My TEDx Talk</a>
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
        <h2 style="font-family: var(--font-heading); font-size: 2rem; margin-bottom: 1rem;">En Español</h2>
        <p class="category-count">{len(posts)} publicaciones en español, ordenadas por fecha (más recientes primero)</p>

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

    return html

def main():
    """Create Spanish category page"""
    print("Creating 'En Español' category...\n")

    # Load posts data
    with open('all_posts_full.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)

    # Find Spanish posts
    spanish_posts = [p for p in posts if is_spanish_post(p.get('title', ''))]

    print(f"Found {len(spanish_posts)} Spanish posts:")
    for p in spanish_posts:
        print(f"  - {p.get('title', 'Untitled')}")

    # Create category page
    html = create_spanish_category_page(spanish_posts)

    Path('category').mkdir(exist_ok=True)
    with open('category/en-espanol.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n✓ Created category/en-espanol.html")

if __name__ == '__main__':
    main()
