#!/usr/bin/env python3
"""
Build Post Index page - lists all posts with titles and dates
Run this script whenever you add new posts to auto-update the index
"""
import urllib.request
import urllib.error
import re
import json
from html.parser import HTMLParser
from datetime import datetime

BASE_URL = "https://leonardoflores.net"

class PostExtractor(HTMLParser):
    """Extract blog post details from WordPress archive pages"""

    def __init__(self):
        super().__init__()
        self.posts = []
        self.in_article = False
        self.in_h2 = False
        self.in_time = False
        self.current_post = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'article' and 'post-' in attrs_dict.get('class', ''):
            self.in_article = True
            self.current_post = {}

        if self.in_article and tag == 'h2' and 'entry-title' in attrs_dict.get('class', ''):
            self.in_h2 = True

        if self.in_h2 and tag == 'a':
            self.current_post['url'] = attrs_dict.get('href', '')

        if self.in_article and tag == 'time':
            self.in_time = True
            self.current_post['datetime'] = attrs_dict.get('datetime', '')

    def handle_data(self, data):
        if self.in_h2:
            self.current_post['title'] = data.strip()
        elif self.in_time:
            self.current_post['date_display'] = data.strip()

    def handle_endtag(self, tag):
        if tag == 'h2' and self.in_h2:
            self.in_h2 = False

        if tag == 'time' and self.in_time:
            self.in_time = False

        if tag == 'article' and self.in_article:
            self.in_article = False
            if self.current_post.get('title') and self.current_post.get('url'):
                self.posts.append(self.current_post.copy())

def scrape_all_posts():
    """Scrape all posts from the WordPress site"""
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

            parser = PostExtractor()
            parser.feed(html)

            if not parser.posts:
                break

            all_posts.extend(parser.posts)
            print(f"  Found {len(parser.posts)} posts")

            page_num += 1

            if page_num > 50:  # Safety limit
                break

        except urllib.error.HTTPError:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

    return all_posts

def convert_url_to_local(wp_url):
    """Convert WordPress URL to local static URL"""
    # https://leonardoflores.net/blog/category/post-slug/ -> posts/blog/category/post-slug.html
    match = re.search(r'leonardoflores\.net/blog/([^/]+)/([^/]+)/?', wp_url)
    if match:
        category = match.group(1)
        slug = match.group(2)
        return f"posts/blog/{category}/{slug}.html"
    return wp_url

def generate_index_html(posts):
    """Generate the Post Index HTML page"""

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

    # Generate post list HTML
    post_items = []
    for post in posts:
        title = post.get('title', 'Untitled')
        date = post.get('date_display', '')
        url = convert_url_to_local(post.get('url', '#'))

        post_items.append(f'''        <li class="post-index-item">
            <a href="{url}" class="post-index-link">{title}</a>
            <span class="post-index-date">{date}</span>
        </li>''')

    posts_html = '\n'.join(post_items)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Post Index - Leonardo Flores</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" href="images/wp-content/uploads/2019/08/cropped-leoprofilememefavicon-32x32.png">
    <style>
        .post-index {{
            list-style: none;
            padding: 0;
            margin: 2rem 0;
        }}
        .post-index-item {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--color-accent);
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        .post-index-link {{
            color: var(--color-primary);
            text-decoration: none;
            font-size: 1.1rem;
            flex: 1;
            min-width: 200px;
        }}
        .post-index-link:hover {{
            text-decoration: underline;
        }}
        .post-index-date {{
            color: var(--color-text-light);
            font-size: 0.9rem;
            white-space: nowrap;
        }}
        .post-count {{
            color: var(--color-text-light);
            font-size: 0.95rem;
            margin-bottom: 2rem;
        }}
    </style>
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
        <p class="tagline">Professor & Chair, Department of English at Appalachian State University</p>
        <nav>
            <a href="about.html">About</a>
            <a href="publications.html">CV & Publications</a>
            <a href="category/creative-work.html">Creative Work</a>
            <a href="courses.html">Courses</a>
            <a href="https://www.youtube.com/watch?v=qN9fret0PNo">My TEDx Talk</a>
            <a href="mailto:floresll@appstate.edu">Contact</a>
            <a href="calendar.html">Calendar</a>
            <a href="post-index.html">Post Index</a>
        </nav>
    </header>

    <main>
        <h2 style="font-family: var(--font-heading); font-size: 2rem; margin-bottom: 1rem;">Post Index</h2>
        <p class="post-count">{len(posts)} posts total, sorted by date (newest first)</p>

        <ul class="post-index">
{posts_html}
        </ul>
    </main>

    <footer>
        <p>&copy; 2026 Leonardo Flores</p>
    </footer>

    <script src="js/search.js"></script>
</body>
</html>'''

    return html

def add_index_link_to_nav(html_file):
    """Add Post Index link to a page's navigation if not present"""
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'post-index.html' in html:
        return  # Already has link

    # Add Post Index link before </nav>
    html = re.sub(
        r'(<a href="[^"]*calendar\.html">Calendar</a>)',
        r'\1\n            <a href="post-index.html">Post Index</a>',
        html
    )

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    """Build the post index"""
    print("Building Post Index...\n")

    # Scrape all posts
    posts = scrape_all_posts()
    print(f"\nTotal posts found: {len(posts)}")

    # Generate index page
    index_html = generate_index_html(posts)

    # Save index page
    with open('post-index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"\nCreated post-index.html")

    # Save posts data for future reference
    with open('all_posts_full.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"Saved posts data to all_posts_full.json")

    print("\n✓ Post Index built successfully!")
    print("\nTo auto-update when you add new posts, run:")
    print("  python3 build_post_index.py")

if __name__ == '__main__':
    main()
