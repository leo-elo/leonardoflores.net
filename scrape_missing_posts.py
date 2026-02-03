#!/usr/bin/env python3
"""
Scrape missing blog posts from leonardoflores.net
"""
import os
import re
import urllib.request
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser
import time

BASE_URL = "https://leonardoflores.net"

# Map static paths to original site paths
def get_original_url(static_path):
    """Convert static path to original site URL"""
    # posts/blog/creative-work/wordhack... -> /blog/creative-work/wordhack.../
    path = static_path.replace('posts/', '/').replace('.html', '/')
    # Handle category name differences
    path = path.replace('/presentations/', '/presentations-2/')
    return BASE_URL + path

class PostContentExtractor(HTMLParser):
    """Extract post content from WordPress page"""
    def __init__(self):
        super().__init__()
        self.in_entry_content = False
        self.in_title = False
        self.in_date = False
        self.content = []
        self.title = ""
        self.date = ""
        self.featured_image = ""
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get('class', '')

        if 'entry-content' in class_name:
            self.in_entry_content = True
            self.depth = 0
        elif self.in_entry_content:
            self.depth += 1
            # Rebuild the tag
            attr_str = ' '.join(f'{k}="{v}"' for k, v in attrs)
            if attr_str:
                self.content.append(f'<{tag} {attr_str}>')
            else:
                self.content.append(f'<{tag}>')

        if 'entry-title' in class_name:
            self.in_title = True
        if tag == 'time' and 'entry-date' in class_name:
            self.in_date = True
            self.date = attrs_dict.get('datetime', '')[:10]  # Get date part
        if tag == 'img' and 'wp-post-image' in class_name:
            self.featured_image = attrs_dict.get('src', '')

    def handle_endtag(self, tag):
        if self.in_entry_content:
            if self.depth > 0:
                self.content.append(f'</{tag}>')
                self.depth -= 1
            else:
                self.in_entry_content = False
        if tag in ['h1', 'h2'] and self.in_title:
            self.in_title = False
        if tag == 'time':
            self.in_date = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_entry_content:
            self.content.append(data)

def fetch_url(url):
    """Fetch URL content"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"    Error fetching {url}: {e}")
        return None

def create_post_html(title, date, content, featured_image, category):
    """Create post HTML with proper template"""
    # Format date nicely
    from datetime import datetime
    try:
        dt = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = dt.strftime('%B %d, %Y')
    except:
        formatted_date = date

    # Handle featured image
    if featured_image:
        # Convert to local path
        if 'wp-content/uploads' in featured_image:
            img_path = featured_image.split('wp-content/uploads/')[-1]
            local_img = f'../../../images/wp-content/uploads/{img_path}'
        else:
            local_img = '../../../images/wp-content/uploads/leomatrix.jpg'

        featured_html = f'''<div class="featured-image-container">
        <img src="{local_img}" alt="{title}" class="post-featured-image">
    </div>'''
    else:
        featured_html = ''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Leonardo Flores</title>
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
            <a href="../../../category/milestones.html">Milestones</a>
            <a href="../../../category/teaching.html">Teaching</a>
            <a href="../../../category/creative-work.html">Creative Work</a>
            <a href="../../../category/resources.html">Resources</a>
            <a href="../../../category/en-espanol.html">En Español</a>
        </nav>
    </header>

    <main>
        <article>
            <div class="post-header">
                <h1 class="post-title">{title}</h1>
            </div>

            {featured_html}

            <div class="post-content">
                <div class="entry-meta">
                    <time datetime="{date}">{formatted_date}</time>
                </div>

                <div class="entry-content">
                    {content}
                </div>
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

def scrape_post(static_path):
    """Scrape a single post from the original site"""
    original_url = get_original_url(static_path)

    html = fetch_url(original_url)
    if not html:
        # Try without -2 suffix
        original_url = original_url.replace('/presentations-2/', '/presentations/')
        html = fetch_url(original_url)
        if not html:
            return None

    # Parse the content
    parser = PostContentExtractor()
    parser.feed(html)

    if not parser.title:
        return None

    # Get category from path
    category = static_path.split('/')[2] if len(static_path.split('/')) > 2 else 'milestones'

    return {
        'title': parser.title.strip(),
        'date': parser.date or '2020-01-01',
        'content': ''.join(parser.content),
        'featured_image': parser.featured_image,
        'category': category
    }

def main():
    print("Scraping missing blog posts...\n")

    # Get list of all referenced posts
    referenced = set()
    for page_file in Path('.').glob('*.html'):
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        for match in re.findall(r'href="(posts/blog/[^"]*\.html)"', content):
            referenced.add(match)

    for page_file in Path('.').glob('page-*.html'):
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        for match in re.findall(r'href="(posts/blog/[^"]*\.html)"', content):
            referenced.add(match)

    print(f"Found {len(referenced)} referenced posts")

    # Check which ones exist
    missing = []
    for post_path in referenced:
        if not Path(post_path).exists():
            missing.append(post_path)

    print(f"Missing {len(missing)} posts\n")

    # Scrape missing posts
    created = 0
    errors = 0

    for post_path in sorted(missing):
        print(f"  Scraping: {post_path}")

        # Create directory if needed
        Path(post_path).parent.mkdir(parents=True, exist_ok=True)

        # Scrape post
        post_data = scrape_post(post_path)

        if post_data:
            html = create_post_html(
                post_data['title'],
                post_data['date'],
                post_data['content'],
                post_data['featured_image'],
                post_data['category']
            )

            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(html)

            created += 1
        else:
            print(f"    FAILED: Could not scrape {post_path}")
            errors += 1

        # Be nice to the server
        time.sleep(0.5)

    print(f"\n+ Created {created} posts")
    if errors:
        print(f"! {errors} errors")

if __name__ == '__main__':
    main()
