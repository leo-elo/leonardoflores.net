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
        new_category = CATEGORY_MAP.get(category, category)
        return f"posts/blog/{new_category}/{slug}.html"
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
