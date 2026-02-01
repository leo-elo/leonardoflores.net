#!/usr/bin/env python3
"""
Scrape all blog posts from leonardoflores.net and generate pagination
"""
import urllib.request
import urllib.error
import re
import json
import os
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

BASE_URL = "https://leonardoflores.net"
POSTS_PER_PAGE = 10

class PostExtractor(HTMLParser):
    """Extract blog post links from WordPress archive pages"""

    def __init__(self):
        super().__init__()
        self.posts = []
        self.in_article = False
        self.in_h2 = False
        self.current_post = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'article' and any('post-' in attrs_dict.get('class', '') for _ in [1]):
            self.in_article = True
            self.current_post = {}

        if self.in_article and tag == 'h2' and 'entry-title' in attrs_dict.get('class', ''):
            self.in_h2 = True

        if self.in_h2 and tag == 'a':
            self.current_post['url'] = attrs_dict.get('href', '')
            self.current_post['title'] = ''

    def handle_data(self, data):
        if self.in_h2 and 'title' in self.current_post:
            self.current_post['title'] = data.strip()

    def handle_endtag(self, tag):
        if tag == 'h2' and self.in_h2:
            self.in_h2 = False
            if self.current_post and 'url' in self.current_post:
                self.posts.append(self.current_post.copy())

        if tag == 'article' and self.in_article:
            self.in_article = False

def scrape_posts_from_page(page_num=1):
    """Scrape posts from a specific archive page"""
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

        return parser.posts, html
    except urllib.error.HTTPError as e:
        print(f"Page {page_num} not found (404) - reached end of posts")
        return [], None
    except Exception as e:
        print(f"Error scraping page {page_num}: {e}")
        return [], None

def main():
    """Scrape all blog posts"""
    all_posts = []
    page_num = 1

    # Keep scraping until we hit a 404
    while True:
        posts, html = scrape_posts_from_page(page_num)

        if not posts:
            break

        all_posts.extend(posts)
        print(f"Found {len(posts)} posts on page {page_num}")

        page_num += 1

        # Safety limit
        if page_num > 50:
            print("Reached safety limit of 50 pages")
            break

    print(f"\nTotal posts found: {len(all_posts)}")

    # Save to JSON
    with open('all_posts.json', 'w') as f:
        json.dump(all_posts, f, indent=2)

    print(f"Saved to all_posts.json")

    # Calculate pagination
    total_pages = (len(all_posts) + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE
    print(f"Will need {total_pages} pagination pages")

if __name__ == '__main__':
    main()
