#!/usr/bin/env python3
"""
Build proper pagination pages with 12 posts per page
Scrapes all posts from WordPress and generates static pagination
"""
import urllib.request
import urllib.error
import re
import json
from html.parser import HTMLParser
from datetime import datetime

BASE_URL = "https://leonardoflores.net"
POSTS_PER_PAGE = 12

class PostCardExtractor(HTMLParser):
    """Extract full post card data from WordPress pages"""

    def __init__(self):
        super().__init__()
        self.posts = []
        self.in_article = False
        self.in_h2 = False
        self.in_time = False
        self.in_excerpt = False
        self.in_figure = False
        self.current_post = {}
        self.excerpt_text = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '')

        if tag == 'article' and 'post-' in classes:
            self.in_article = True
            self.current_post = {'excerpt': '', 'featured_image': '', 'featured_alt': ''}
            self.excerpt_text = []

        if self.in_article:
            if tag == 'h2' and 'entry-title' in classes:
                self.in_h2 = True

            if self.in_h2 and tag == 'a':
                self.current_post['url'] = attrs_dict.get('href', '')

            if tag == 'time':
                self.in_time = True
                self.current_post['datetime'] = attrs_dict.get('datetime', '')

            if tag == 'div' and 'entry-content' in classes:
                self.in_excerpt = True

            if tag == 'figure' and 'post-thumbnail' in classes:
                self.in_figure = True

            if self.in_figure and tag == 'img':
                src = attrs_dict.get('src', '')
                # Get the best quality image
                srcset = attrs_dict.get('srcset', '')
                if srcset:
                    # Get highest resolution from srcset
                    parts = srcset.split(',')
                    best_src = src
                    best_width = 0
                    for part in parts:
                        part = part.strip()
                        if ' ' in part:
                            img_url, width = part.rsplit(' ', 1)
                            try:
                                w = int(width.replace('w', ''))
                                if w > best_width:
                                    best_width = w
                                    best_src = img_url
                            except:
                                pass
                    src = best_src

                self.current_post['featured_image'] = src
                self.current_post['featured_alt'] = attrs_dict.get('alt', '')

    def handle_data(self, data):
        if self.in_h2:
            self.current_post['title'] = data.strip()
        elif self.in_time:
            self.current_post['date_display'] = data.strip()
        elif self.in_excerpt:
            text = data.strip()
            if text:
                self.excerpt_text.append(text)

    def handle_endtag(self, tag):
        if tag == 'h2' and self.in_h2:
            self.in_h2 = False

        if tag == 'time' and self.in_time:
            self.in_time = False

        if tag == 'div' and self.in_excerpt:
            self.in_excerpt = False
            self.current_post['excerpt'] = ' '.join(self.excerpt_text)

        if tag == 'figure' and self.in_figure:
            self.in_figure = False

        if tag == 'article' and self.in_article:
            self.in_article = False
            if self.current_post.get('title') and self.current_post.get('url'):
                self.posts.append(self.current_post.copy())

def scrape_all_posts():
    """Scrape all posts from WordPress"""
    all_posts = []
    page_num = 1

    while True:
        if page_num == 1:
            url = f"{BASE_URL}/"
        else:
            url = f"{BASE_URL}/page/{page_num}/"

        print(f"Scraping {url}...")

        try:
            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')

            parser = PostCardExtractor()
            parser.feed(html)

            if not parser.posts:
                break

            all_posts.extend(parser.posts)
            print(f"  Found {len(parser.posts)} posts")

            page_num += 1
            if page_num > 50:
                break

        except urllib.error.HTTPError:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

    return all_posts

def convert_url_to_local(wp_url):
    """Convert WordPress URL to local static URL with new category mapping"""
    # Category mapping: old → new
    CATEGORY_MAP = {
        'news': 'milestones',
        'grants': 'milestones',
        'publications': 'milestones',
        'interviews': 'milestones',
        'proposals': 'milestones',
        'editorial-work': 'milestones',
        'e-poetry-sites': 'resources',
        'performances': 'creative-work',
        'courses': 'teaching',
        'pedagogy': 'teaching',
        'presentations-2': 'presentations',
        'uncategorized': 'milestones',
    }

    match = re.search(r'leonardoflores\.net/blog/([^/]+)/([^/]+)/?', wp_url)
    if match:
        category = match.group(1)
        slug = match.group(2)
        # Map to new category
        new_category = CATEGORY_MAP.get(category, category)
        return f"posts/blog/{new_category}/{slug}.html"
    return wp_url

def convert_image_to_local(wp_img):
    """Convert WordPress image URL to local path"""
    if not wp_img:
        return ''
    match = re.search(r'wp-content/uploads/(.+)', wp_img)
    if match:
        return f"images/wp-content/uploads/{match.group(1)}"
    return wp_img

def create_post_card_html(post):
    """Generate HTML for a single post card"""
    url = convert_url_to_local(post.get('url', '#'))
    title = post.get('title', 'Untitled')
    date = post.get('date_display', '')
    excerpt = post.get('excerpt', '')[:250]
    if len(post.get('excerpt', '')) > 250:
        excerpt += '...'

    img_src = convert_image_to_local(post.get('featured_image', ''))
    img_alt = post.get('featured_alt', '')

    if img_src:
        thumbnail_html = f'''<figure class="post-thumbnail">
            <img src="{img_src}"
                 alt="{img_alt}"
                 class="post-thumbnail-image"
                 loading="lazy">
        </figure>'''
    else:
        thumbnail_html = '''<div class="post-thumbnail-placeholder">
            <span class="placeholder-icon">📄</span>
        </div>'''

    return f'''<article class="post-card">
    <header class="post-card-header">
        <a href="{url}" class="post-thumbnail-link">
            {thumbnail_html}
        </a>
    </header>

    <div class="post-card-content">
        <h2 class="entry-title">
            <a href="{url}">{title}</a>
        </h2>

        <div class="entry-meta">
            <time>{date}</time>
        </div>

        <div class="entry-excerpt">
            <p>{excerpt}</p>
        </div>

        <a href="{url}" class="read-more">Continue reading →</a>
    </div>
</article>'''

def create_pagination_nav(current_page, total_pages):
    """Generate pagination navigation HTML"""
    if total_pages <= 1:
        return ''

    nav_items = []

    # Previous link
    if current_page > 1:
        prev_url = 'index.html' if current_page == 2 else f'page-{current_page-1}.html'
        nav_items.append(f'<a href="{prev_url}" class="pagination-prev">← Newer Posts</a>')

    # Page numbers with ellipsis
    for i in range(1, total_pages + 1):
        if i == 1 or i == total_pages or (current_page - 2 <= i <= current_page + 2):
            url = 'index.html' if i == 1 else f'page-{i}.html'
            if i == current_page:
                nav_items.append(f'<span class="pagination-current">{i}</span>')
            else:
                nav_items.append(f'<a href="{url}" class="pagination-number">{i}</a>')
        elif i == current_page - 3 or i == current_page + 3:
            nav_items.append('<span class="pagination-ellipsis">...</span>')

    # Next link
    if current_page < total_pages:
        next_url = f'page-{current_page+1}.html'
        nav_items.append(f'<a href="{next_url}" class="pagination-next">Older Posts →</a>')

    return f'<nav class="pagination">{" ".join(nav_items)}</nav>'

def create_page_html(posts, page_num, total_pages):
    """Generate a complete pagination page"""
    posts_html = '\n            '.join([create_post_card_html(p) for p in posts])
    pagination_nav = create_pagination_nav(page_num, total_pages)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leonardo Flores{' - Page ' + str(page_num) if page_num > 1 else ''}</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" href="images/wp-content/uploads/2019/08/cropped-leoprofilememefavicon-32x32.png">
</head>
<body>
<header>
        <div class="header-top">
            <h1><a href="index.html">Leonardo Flores</a></h1>
            <div class="search-container">
                <input type="search" id="searchInput" placeholder="Search posts..." aria-label="Search posts">
                <div id="searchResults" class="search-results hidden"></div>
            </div>
        </div>
        <p class="tagline">Scholar, Academic Leader, Creator</p>
        <nav>
            <a href="about.html">About</a>
            <a href="courses.html">Courses</a>
            <a href="https://www.youtube.com/watch?v=qN9fret0PNo">My TEDx Talk</a>
            <a href="calendar.html">Calendar</a>
            <a href="post-index.html">Post Index</a>
            <a href="category/presentations.html">Presentations</a>
            <a href="category/milestones.html">Milestones</a>
            <a href="category/teaching.html">Teaching</a>
            <a href="category/creative-work.html">Creative Work</a>
            <a href="category/resources.html">Resources</a>
            <a href="category/en-espanol.html">En Español</a>
        </nav>
    </header>

    <main>
        <div class="posts-grid">
            {posts_html}
        </div>

        {pagination_nav}
    </main>

    <footer>
        <p>&copy; 2026 Leonardo Flores</p>
    </footer>

    <script src="js/search.js"></script>
</body>
</html>'''

def main():
    """Build all pagination pages"""
    print("Building pagination pages...\n")

    # Scrape all posts
    posts = scrape_all_posts()
    print(f"\nTotal posts found: {len(posts)}")

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

    # Calculate total pages
    total_pages = (len(posts) + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE
    print(f"Creating {total_pages} pagination pages ({POSTS_PER_PAGE} posts each)\n")

    # Generate each page
    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * POSTS_PER_PAGE
        end_idx = start_idx + POSTS_PER_PAGE
        page_posts = posts[start_idx:end_idx]

        page_html = create_page_html(page_posts, page_num, total_pages)

        filename = 'index.html' if page_num == 1 else f'page-{page_num}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page_html)

        print(f"Created {filename} (posts {start_idx+1}-{min(end_idx, len(posts))})")

    # Save posts data
    with open('all_posts_cards.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Pagination built successfully!")
    print(f"  {total_pages} pages with {POSTS_PER_PAGE} posts each")

if __name__ == '__main__':
    main()
