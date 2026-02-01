#!/usr/bin/env python3
"""
Build static site from WordPress pages
Extracts clean content and creates simple HTML pages
"""

import os
import re
import json
from html.parser import HTMLParser
from pathlib import Path
from datetime import datetime

class ContentExtractor(HTMLParser):
    """Extract main content from WordPress HTML"""

    def __init__(self):
        super().__init__()
        self.title = ''
        self.content_html = []
        self.categories = []
        self.date = ''
        self.in_title = False
        self.in_entry_content = False
        self.in_entry_header = False
        self.in_category_list = False
        self.content_depth = 0
        self.current_tag = None
        self.current_attrs = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.current_tag = tag
        self.current_attrs = attrs_dict

        # Extract title
        if tag == 'title':
            self.in_title = True

        # Entry header (contains post metadata)
        if 'entry-header' in attrs_dict.get('class', ''):
            self.in_entry_header = True

        # Main content
        if 'entry-content' in attrs_dict.get('class', '') or attrs_dict.get('id') == 'primary':
            self.in_entry_content = True
            self.content_depth = 0

        # Category list
        if 'categories-links' in attrs_dict.get('class', '') or 'cat-links' in attrs_dict.get('class', ''):
            self.in_category_list = True

        # Build content HTML
        if self.in_entry_content:
            self.content_depth += 1

            # Rebuild tag with clean attributes
            attrs_clean = []
            for key, value in attrs:
                # Keep certain useful attributes
                if key in ['href', 'src', 'alt', 'title', 'id']:
                    # Fix image paths
                    if key == 'src' and value.startswith('https://leonardoflores.net/'):
                        value = value.replace('https://leonardoflores.net/', '../')
                    # Fix link paths
                    elif key == 'href' and value.startswith('https://leonardoflores.net/'):
                        value = value.replace('https://leonardoflores.net/', '../')

                    attrs_clean.append(f'{key}="{value}"')

            attrs_str = ' ' + ' '.join(attrs_clean) if attrs_clean else ''
            self.content_html.append(f'<{tag}{attrs_str}>')

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

        if self.in_entry_content:
            self.content_html.append(f'</{tag}>')
            self.content_depth -= 1

            if self.content_depth <= 0:
                self.in_entry_content = False

        if tag in ['header'] and self.in_entry_header:
            self.in_entry_header = False

        if self.in_category_list and tag in ['p', 'div']:
            self.in_category_list = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data

        if self.in_entry_content and data.strip():
            # Clean up excessive whitespace
            data = re.sub(r'\s+', ' ', data)
            self.content_html.append(data)

        if self.in_category_list and data.strip() and data.strip() not in ['Categories:', 'Posted in']:
            self.categories.append(data.strip())

def create_html_template(title, content, nav_items, categories=None):
    """Create clean HTML page from content"""

    categories_html = ''
    if categories:
        cat_links = [f'<a href="../category/{cat.lower().replace(" ", "-")}.html">{cat}</a>'
                     for cat in categories]
        categories_html = f'<p class="categories">Categories: {", ".join(cat_links)}</p>'

    nav_html = '\n'.join([f'<a href="{url}">{name}</a>' for name, url in nav_items])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="icon" href="../images/wp-content/uploads/2019/08/cropped-leoprofilememefavicon-32x32.png">
</head>
<body>
    <header>
        <h1><a href="../index.html">Leonardo Flores</a></h1>
        <p class="tagline">Professor & Chair, Department of English at Appalachian State University</p>
        <nav>
            {nav_html}
        </nav>
    </header>

    <main>
        <article>
            {categories_html}
            {content}
        </article>
    </main>

    <footer>
        <p>&copy; {datetime.now().year} Leonardo Flores</p>
    </footer>
</body>
</html>'''

def build_site():
    """Build the static site"""

    # Navigation items
    nav_items = [
        ('About', '../about.html'),
        ('CV & Publications', '../publications.html'),
        ('Creative Work', '../category/creative-work.html'),
        ('Courses', '../courses.html'),
        ('My TEDx Talk', 'https://www.youtube.com/watch?v=qN9fret0PNo'),
        ('Contact', 'mailto:floresll@appstate.edu'),
        ('Calendar', '../calendar.html'),
    ]

    # Load metadata
    with open('metadata.json', 'r') as f:
        metadata = json.load(f)

    # Create output directory
    os.makedirs('site', exist_ok=True)
    os.makedirs('site/category', exist_ok=True)
    os.makedirs('site/posts', exist_ok=True)

    print("=== Building static site ===\n")

    # Process each page
    for page_path, page_data in metadata['pages'].items():
        source_file = page_data['filepath']

        if not os.path.exists(source_file):
            print(f"Skipping {source_file} - not found")
            continue

        print(f"Processing: {source_file}")

        # Read source HTML
        with open(source_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Extract content
        extractor = ContentExtractor()
        extractor.feed(html_content)

        # Build content HTML
        content = ''.join(extractor.content_html)

        # Clean title
        title = extractor.title.replace(' – Leonardo Flores', '').replace('Leonardo Flores – ', '').strip()

        # Generate output path
        if source_file.startswith('pages/'):
            output_path = source_file.replace('pages/', 'site/')
        elif source_file.startswith('posts/'):
            output_path = source_file.replace('posts/', 'site/posts/')
        else:
            output_path = 'site/' + os.path.basename(source_file)

        # Create output directory
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Generate HTML
        html = create_html_template(title, content, nav_items, extractor.categories)

        # Save
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  Created: {output_path}")
        print(f"  Title: {title}")
        if extractor.categories:
            print(f"  Categories: {', '.join(extractor.categories)}")

    # Copy homepage
    print("\n=== Creating homepage ===")
    with open('index.html', 'r', encoding='utf-8') as f:
        homepage_html = f.read()

    extractor = ContentExtractor()
    extractor.feed(homepage_html)

    # For homepage, extract recent posts
    content = ''.join(extractor.content_html)

    nav_items_home = [(name, url.replace('../', '')) for name, url in nav_items]
    html = create_html_template('Leonardo Flores', content, nav_items_home)

    # Fix paths for homepage
    # Fix blog post links: add posts/ prefix and .html extension
    html = re.sub(r'href="(?:\.\./)?blog/([^/]+)/([^"]+)/"', r'href="posts/blog/\1/\2.html"', html)
    # Fix image paths
    html = html.replace('src="../', 'src="')

    with open('site/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Homepage created")

    print("\n=== Site building complete ===")
    print(f"Total pages created: {len(metadata['pages']) + 1}")
    print("Output directory: site/")

if __name__ == '__main__':
    build_site()
