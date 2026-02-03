#!/usr/bin/env python3
"""
Import blog posts from WordPress XML export file
"""
import xml.etree.ElementTree as ET
import re
import html
import os
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.parse

# Namespaces used in WordPress XML
NAMESPACES = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
}

# Category slug mapping to our directory structure
CATEGORY_MAP = {
    'presentations-2': 'presentations',
    'courses': 'teaching',
    'pedagogy': 'teaching',
    'news': 'milestones',
    'interviews': 'milestones',
    'grants': 'milestones',
    'proposals': 'milestones',
    'publications': 'milestones',
    'performances': 'creative-work',
    'editorial-work': 'resources',
    'e-poetry-sites': 'resources',
    'uncategorized': 'milestones',
}

def get_text(element, path, namespaces=None):
    """Extract text from XML element"""
    el = element.find(path, namespaces)
    if el is not None and el.text:
        return el.text.strip()
    return ''

def clean_content(content):
    """Clean WordPress content for static HTML"""
    if not content:
        return ''

    # Unescape HTML entities
    content = html.unescape(content)

    # Fix image URLs - convert to local paths
    content = re.sub(
        r'https?://leonardoflores\.net/wp-content/uploads/',
        '../../../images/wp-content/uploads/',
        content
    )

    # Remove WordPress-specific shortcodes
    content = re.sub(r'\[/?caption[^\]]*\]', '', content)
    content = re.sub(r'\[/?gallery[^\]]*\]', '', content)

    # Convert <!--more--> to nothing (we show full content)
    content = content.replace('<!--more-->', '')

    # Wrap bare text in paragraphs if needed
    if not content.strip().startswith('<'):
        paragraphs = content.split('\n\n')
        content = '\n'.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())

    return content

def get_featured_image(item, attachments):
    """Get featured image for a post"""
    # Look for _thumbnail_id in postmeta
    for meta in item.findall('wp:postmeta', NAMESPACES):
        key = get_text(meta, 'wp:meta_key', NAMESPACES)
        if key == '_thumbnail_id':
            thumb_id = get_text(meta, 'wp:meta_value', NAMESPACES)
            if thumb_id in attachments:
                return attachments[thumb_id]
    return None

def create_post_html(title, date, content, featured_image, category):
    """Create post HTML with proper template"""
    # Format date
    try:
        dt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        formatted_date = dt.strftime('%B %d, %Y')
        date_iso = dt.strftime('%Y-%m-%d')
    except:
        formatted_date = date
        date_iso = date

    # Handle featured image
    if featured_image:
        img_path = featured_image.replace('https://leonardoflores.net/wp-content/uploads/', '')
        local_img = f'../../../images/wp-content/uploads/{img_path}'
        featured_html = f'''<div class="featured-image-container">
        <img src="{local_img}" alt="{html.escape(title)}" class="post-featured-image">
    </div>'''
    else:
        # Use default image
        featured_html = '''<div class="featured-image-container">
        <img src="../../../images/wp-content/uploads/leomatrix.jpg" alt="Leonardo Flores" class="post-featured-image">
    </div>'''

    # Escape title for HTML
    safe_title = html.escape(title)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} - Leonardo Flores</title>
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
                <h1 class="post-title">{safe_title}</h1>
            </div>

            {featured_html}

            <div class="post-content">
                <div class="entry-meta">
                    <time datetime="{date_iso}">{formatted_date}</time>
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

def download_image(url, local_path):
    """Download an image if it doesn't exist"""
    if Path(local_path).exists():
        return True

    try:
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)
        # URL encode the path part
        parsed = urllib.parse.urlparse(url)
        encoded_path = urllib.parse.quote(parsed.path)
        encoded_url = f"{parsed.scheme}://{parsed.netloc}{encoded_path}"

        req = urllib.request.Request(encoded_url, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        urllib.request.urlretrieve(encoded_url, local_path)
        return True
    except Exception as e:
        print(f"    Error downloading {url}: {e}")
        return False

def main():
    print("Importing posts from WordPress XML export...\n")

    # Parse XML
    tree = ET.parse('/Users/floresll/Desktop/blog.xml')
    root = tree.getroot()
    channel = root.find('channel')

    # First pass: collect all attachments (images)
    print("Collecting attachments...")
    attachments = {}
    for item in channel.findall('item'):
        post_type = get_text(item, 'wp:post_type', NAMESPACES)
        if post_type == 'attachment':
            post_id = get_text(item, 'wp:post_id', NAMESPACES)
            url = get_text(item, 'wp:attachment_url', NAMESPACES)
            if post_id and url:
                attachments[post_id] = url

    print(f"  Found {len(attachments)} attachments\n")

    # Get list of posts we need
    needed_posts = set()
    for page_file in Path('.').glob('*.html'):
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        for match in re.findall(r'href="(posts/blog/[^"]*\.html)"', content):
            needed_posts.add(match)
    for page_file in Path('.').glob('page-*.html'):
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        for match in re.findall(r'href="(posts/blog/[^"]*\.html)"', content):
            needed_posts.add(match)

    print(f"Found {len(needed_posts)} posts referenced in pages\n")

    # Second pass: process posts
    print("Processing posts...")
    created = 0
    skipped = 0
    images_downloaded = 0

    for item in channel.findall('item'):
        post_type = get_text(item, 'wp:post_type', NAMESPACES)
        status = get_text(item, 'wp:status', NAMESPACES)

        # Only process published posts
        if post_type != 'post' or status != 'publish':
            continue

        title = get_text(item, 'title')
        slug = get_text(item, 'wp:post_name', NAMESPACES)
        date = get_text(item, 'wp:post_date', NAMESPACES)
        content = get_text(item, 'content:encoded', NAMESPACES)

        # Get category
        category_el = item.find('category[@domain="category"]')
        if category_el is not None:
            cat_slug = category_el.get('nicename', 'milestones')
        else:
            cat_slug = 'milestones'

        # Map to our categories
        category = CATEGORY_MAP.get(cat_slug, cat_slug)

        # Construct file path
        file_path = f'posts/blog/{category}/{slug}.html'

        # Check if this post is needed
        if file_path not in needed_posts:
            continue

        # Skip if already exists
        if Path(file_path).exists():
            skipped += 1
            continue

        # Get featured image
        featured_image = get_featured_image(item, attachments)

        # Download featured image if needed
        if featured_image:
            img_path = featured_image.replace('https://leonardoflores.net/wp-content/uploads/', '')
            local_img_path = f'images/wp-content/uploads/{img_path}'
            if not Path(local_img_path).exists():
                print(f"  Downloading image: {img_path}")
                if download_image(featured_image, local_img_path):
                    images_downloaded += 1

        # Clean content
        content = clean_content(content)

        # Create directory
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Generate HTML
        post_html = create_post_html(title, date, content, featured_image, category)

        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(post_html)

        print(f"  + {file_path}")
        created += 1

    print(f"\n+ Created {created} posts")
    print(f"  Skipped {skipped} existing posts")
    print(f"  Downloaded {images_downloaded} images")

if __name__ == '__main__':
    main()
