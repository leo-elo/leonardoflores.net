#!/usr/bin/env python3
"""
Create a new blog post for leonardoflores.net static site

Usage:
    python3 create_post.py --title "My Post Title" --category presentations
    python3 create_post.py --title "My Post" --category news --date 2026-02-15
    python3 create_post.py --title "My Post" --category news --image path/to/image.png

Categories: presentations, news, teaching, creative-work, resources, en-espanol
"""
import argparse
import re
import html
from pathlib import Path
from datetime import datetime
import shutil

CATEGORIES = {
    'presentations': 'Presentations',
    'news': 'News',
    'teaching': 'Teaching',
    'creative-work': 'Creative Work',
    'resources': 'Resources',
    'en-espanol': 'En Español',
}

BASE_URL = "https://leo-elo.github.io/leonardoflores.net"

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def create_post_html(title, date, category, content, featured_image, categories_list):
    """Generate the HTML for a new post"""

    # Format date
    dt = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = dt.strftime('%B %d, %Y')

    # Escape title
    safe_title = html.escape(title)

    # Featured image HTML
    if featured_image:
        img_path = featured_image
        if not img_path.startswith('../'):
            img_path = f'../../../images/wp-content/uploads/{featured_image}'
        featured_html = f'''<div class="featured-image-container">
        <img src="{img_path}" alt="{safe_title}" class="post-featured-image">
    </div>'''
    else:
        featured_html = '''<div class="featured-image-container">
        <img src="../../../images/wp-content/uploads/leomatrix.jpg" alt="Leonardo Flores" class="post-featured-image">
    </div>'''

    # Categories HTML
    cat_links = []
    for cat_slug in categories_list:
        cat_name = CATEGORIES.get(cat_slug, cat_slug.title())
        cat_links.append(f'<a href="../../../category/{cat_slug}.html">{cat_name}</a>')
    categories_html = ', '.join(cat_links) if cat_links else f'<a href="../../../category/{category}.html">{CATEGORIES.get(category, category.title())}</a>'

    # Build canonical URL
    slug = slugify(title)
    canonical_url = f"{BASE_URL}/posts/blog/{category}/{slug}.html"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} - Leonardo Flores</title>
    <meta name="description" content="{safe_title}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{safe_title}">
    <meta property="og:description" content="{safe_title}">
    <meta property="og:image" content="{BASE_URL}/images/wp-content/uploads/leomatrix.jpg">
    <meta property="og:site_name" content="Leonardo Flores">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{safe_title}">
    <meta name="twitter:description" content="{safe_title}">
    <meta name="twitter:image" content="{BASE_URL}/images/wp-content/uploads/leomatrix.jpg">

    <link rel="stylesheet" href="../../../css/style.css">
    <link rel="icon" href="../../../images/wp-content/uploads/2019/08/cropped-leoprofilememefavicon-32x32.png">
</head>
<body>
    <header>
        <div class="header-top">
            <div class="header-title-menu">
                <h1><a href="../../../index.html">Leonardo Flores</a></h1>
                <p class="tagline">Scholar, Leader, Creator</p>
            </div>
            <button class="menu-toggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
        <nav>
            <a href="../../../about.html">About</a>
            <a href="../../../calendar.html">Calendar</a>
            <a href="../../../post-index.html">Index</a>
            <a href="../../../category/presentations.html">Presentations</a>
            <a href="../../../category/news.html">News</a>
            <a href="../../../category/teaching.html">Teaching</a>
            <a href="../../../category/creative-work.html">Creative Work</a>
            <a href="../../../category/resources.html">Resources</a>
            <a href="../../../category/en-espanol.html">En Español</a>
        </nav>
    </header>

    <main>
        <article>
            <div class="post-header">
                <h1 class="post-title">{safe_title}</h1>
            </div>

            {featured_html}

            <div class="post-content">
                <div class="entry-meta">
                    <time datetime="{date}">{formatted_date}</time>
                </div>

                <div class="entry-content">
                    {content}
                </div>

                <p class="categories post-categories-bottom">Categories: {categories_html}</p>
            </div>
        </article>
    </main>

    <footer>
        <div class="footer-content">
            <div class="footer-left">© 2026 Leonardo Flores</div>
            <div class="footer-center"><a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC-BY 4.0</a></div>
            <div class="footer-right">
                <div class="search-container">
                    <input type="search" id="footerSearchInput" placeholder="Search posts..." aria-label="Search posts">
                    <div id="searchResults" class="search-results hidden"></div>
                </div>
            </div>
        </div>
    </footer>

    <script src="../../../js/search.js"></script>
</body>
</html>'''

def main():
    parser = argparse.ArgumentParser(description='Create a new blog post')
    parser.add_argument('--title', '-t', required=True, help='Post title')
    parser.add_argument('--category', '-c', required=True,
                        choices=list(CATEGORIES.keys()),
                        help='Primary category')
    parser.add_argument('--categories', nargs='+',
                        help='Additional categories (space-separated)')
    parser.add_argument('--date', '-d', default=datetime.now().strftime('%Y-%m-%d'),
                        help='Post date (YYYY-MM-DD), defaults to today')
    parser.add_argument('--image', '-i', help='Featured image path (relative to images/wp-content/uploads/)')
    parser.add_argument('--content', help='Initial content (HTML)')

    args = parser.parse_args()

    # Build categories list
    categories_list = [args.category]
    if args.categories:
        categories_list.extend(args.categories)
    categories_list = list(dict.fromkeys(categories_list))  # Remove duplicates, preserve order

    # Default content
    content = args.content or '<p>Your content here...</p>'

    # Generate slug and file path
    slug = slugify(args.title)
    file_path = Path(f'posts/blog/{args.category}/{slug}.html')

    # Create directory if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if file exists
    if file_path.exists():
        print(f"Warning: {file_path} already exists!")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return

    # Generate HTML
    post_html = create_post_html(
        title=args.title,
        date=args.date,
        category=args.category,
        content=content,
        featured_image=args.image,
        categories_list=categories_list
    )

    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(post_html)

    print(f"\n✓ Created: {file_path}")
    print(f"  Title: {args.title}")
    print(f"  Date: {args.date}")
    print(f"  Categories: {', '.join(categories_list)}")
    print(f"\nNext steps:")
    print(f"  1. Edit the post content in {file_path}")
    print(f"  2. Add the post to index.html or appropriate page")
    print(f"  3. Run: git add -A && git commit -m 'Add new post' && git push")

if __name__ == '__main__':
    main()
