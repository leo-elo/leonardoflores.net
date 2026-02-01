#!/usr/bin/env python3
"""
Fix blog post pages to match site design and add featured images properly
"""
import re
from pathlib import Path
from html.parser import HTMLParser

class FeaturedImageExtractor(HTMLParser):
    """Extract the first featured image from post content"""

    def __init__(self):
        super().__init__()
        self.featured_image = None
        self.featured_alt = ""
        self.in_header = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'header':
            self.in_header = True

        if self.in_header and tag == 'img' and not self.featured_image:
            self.featured_image = attrs_dict.get('src', '')
            self.featured_alt = attrs_dict.get('alt', '')

    def handle_endtag(self, tag):
        if tag == 'header':
            self.in_header = False

def fix_post_page(file_path):
    """Fix a single blog post page"""
    print(f"Processing {file_path}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Calculate correct path depth (posts/blog/category/post.html = 3 levels deep)
    depth = 3
    path_prefix = '../' * depth

    # Fix CSS path
    html = re.sub(
        r'<link rel="stylesheet" href="[^"]*css/style\.css">',
        f'<link rel="stylesheet" href="{path_prefix}css/style.css">',
        html
    )

    # Fix favicon path
    html = re.sub(
        r'<link rel="icon" href="[^"]*cropped-leoprofilememefavicon[^"]*">',
        f'<link rel="icon" href="{path_prefix}images/wp-content/uploads/2019/08/cropped-leoprofilememefavicon-32x32.png">',
        html
    )

    # Fix home link
    html = re.sub(
        r'<h1><a href="[^"]*index\.html">',
        f'<h1><a href="{path_prefix}index.html">',
        html
    )

    # Fix navigation links
    nav_links = [
        ('about.html', 'About'),
        ('publications.html', 'CV & Publications'),
        ('category/creative-work.html', 'Creative Work'),
        ('courses.html', 'Courses'),
        ('calendar.html', 'Calendar'),
    ]

    for link, text in nav_links:
        # Fix the href to use correct path
        html = re.sub(
            rf'<a href="[^"]*{link.split("/")[-1]}">',
            f'<a href="{path_prefix}{link}">',
            html
        )

    # Add search bar if missing
    if '<div class="search-container">' not in html:
        search_html = f'''<div class="search-container">
    <input type="search" id="searchInput" placeholder="Search posts..." aria-label="Search posts">
    <div id="searchResults" class="search-results hidden"></div>
</div>
        '''
        html = re.sub(r'(</nav>)', f'{search_html}\n\\1', html)

    # Extract featured image
    extractor = FeaturedImageExtractor()
    extractor.feed(html)

    featured_image_html = ""
    if extractor.featured_image:
        # Fix image path
        img_src = extractor.featured_image
        if img_src.startswith('../wp-content'):
            img_src = img_src.replace('../wp-content', f'{path_prefix}images/wp-content')
        elif img_src.startswith('wp-content'):
            img_src = f'{path_prefix}images/{img_src}'

        # Create featured image HTML
        featured_image_html = f'''
        <div class="featured-image-container">
            <img src="{img_src}" alt="{extractor.featured_alt}" class="post-featured-image">
        </div>
        '''

    # Fix all image paths in content
    html = re.sub(
        r'src="\.\.\/wp-content',
        f'src="{path_prefix}images/wp-content',
        html
    )
    html = re.sub(
        r'src="wp-content',
        f'src="{path_prefix}images/wp-content',
        html
    )

    # Restructure the main content to add featured image at top
    if featured_image_html:
        # Remove the image from the header inside content
        html = re.sub(r'<header><h1>([^<]+)</h1><figure><img[^>]+></img></figure></header>',
                     r'<header class="post-header"><h1 class="post-title">\1</h1></header>',
                     html)

    # Add featured image after opening <main> tag
    if featured_image_html and '<div class="featured-image-container">' not in html:
        html = re.sub(
            r'(<main>\s*<article>)',
            f'\\1{featured_image_html}',
            html
        )

    # Add search script if missing
    if '<script src=' not in html or 'search.js' not in html:
        script_tag = f'<script src="{path_prefix}js/search.js"></script>'
        html = re.sub(r'(</body>)', f'\n    {script_tag}\n\\1', html)

    # Write updated HTML
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ Fixed")

def main():
    """Fix all blog post pages"""
    print("Fixing blog post pages...\n")

    post_files = list(Path('posts/blog').rglob('*.html'))
    print(f"Found {len(post_files)} post files\n")

    for post_file in post_files:
        fix_post_page(post_file)

    print(f"\n✓ All {len(post_files)} post pages fixed")

if __name__ == '__main__':
    main()
