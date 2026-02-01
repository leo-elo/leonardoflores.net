#!/usr/bin/env python3
"""
Extract post metadata from current HTML files to create searchable index
"""
import os
import re
import json
from html.parser import HTMLParser

class PostMetadataExtractor(HTMLParser):
    """Extract metadata from a blog post HTML file"""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.date = ""
        self.excerpt = ""
        self.in_title = False
        self.in_time = False
        self.in_excerpt = False
        self.excerpt_text = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'h1' or (tag == 'h2' and 'entry-title' in attrs_dict.get('class', '')):
            self.in_title = True
        elif tag == 'time':
            self.in_time = True
        elif tag == 'div' and 'entry-excerpt' in attrs_dict.get('class', ''):
            self.in_excerpt = True

    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
        elif self.in_time:
            self.date = data.strip()
        elif self.in_excerpt:
            text = data.strip()
            if text:
                self.excerpt_text.append(text)

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2']:
            self.in_title = False
        elif tag == 'time':
            self.in_time = False
        elif tag == 'div' and self.in_excerpt:
            self.in_excerpt = False
            self.excerpt = ' '.join(self.excerpt_text)

def extract_from_index(index_html):
    """Extract post cards from index.html"""
    posts = []

    # Match post-card articles
    card_pattern = r'<article class="post-card">(.*?)</article>'
    cards = re.findall(card_pattern, index_html, re.DOTALL)

    for card in cards:
        post = {}

        # Extract URL
        url_match = re.search(r'href="([^"]+)"', card)
        if url_match:
            post['url'] = url_match.group(1)

        # Extract title
        title_match = re.search(r'<h2 class="entry-title">.*?<a[^>]*>([^<]+)</a>', card, re.DOTALL)
        if title_match:
            post['title'] = title_match.group(1).strip()

        # Extract date
        date_match = re.search(r'<time[^>]*>([^<]+)</time>', card)
        if date_match:
            post['date'] = date_match.group(1).strip()

        # Extract excerpt
        excerpt_match = re.search(r'<div class="entry-excerpt">.*?<p>([^<]+)</p>', card, re.DOTALL)
        if excerpt_match:
            post['excerpt'] = excerpt_match.group(1).strip()

        # Extract category from URL
        if 'url' in post:
            category_match = re.search(r'/blog/([^/]+)/', post['url'])
            if category_match:
                post['category'] = category_match.group(1).replace('-', ' ').title()

        if post.get('title'):
            posts.append(post)

    return posts

def main():
    """Extract posts data and create searchable JSON"""
    print("Extracting post metadata...")

    # Read index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()

    posts = extract_from_index(index_html)

    print(f"Found {len(posts)} posts")

    # Save to JSON
    with open('posts-data.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"Saved to posts-data.json")

if __name__ == '__main__':
    main()
