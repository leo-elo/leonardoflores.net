#!/usr/bin/env python3
"""
Add Open Graph and Twitter Card meta tags to all HTML pages for social media sharing.
"""
import re
from pathlib import Path
from html.parser import HTMLParser

BASE_URL = "https://leo-elo.github.io/leonardoflores.net"
SITE_NAME = "Leonardo Flores"
DEFAULT_DESCRIPTION = "Scholar, Academic Leader, Creator. Professor Leonardo Flores is Chair of the English Department at Appalachian State University, specializing in electronic literature and digital writing."
DEFAULT_IMAGE = "images/wp-content/uploads/2019/08/cropped-leoprofilememefavicon-32x32.png"

class MetaExtractor(HTMLParser):
    """Extract title, description, and featured image from HTML"""
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.description = ""
        self.featured_image = ""
        self.in_post_content = False
        self.first_paragraph = ""
        self.in_p = False
        self.p_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'title':
            self.in_title = True
        elif tag == 'img' and 'post-featured-image' in attrs_dict.get('class', ''):
            self.featured_image = attrs_dict.get('src', '')
        elif tag == 'img' and 'post-thumbnail-image' in attrs_dict.get('class', ''):
            if not self.featured_image:
                self.featured_image = attrs_dict.get('src', '')
        elif tag == 'div' and 'post-content' in attrs_dict.get('class', ''):
            self.in_post_content = True
        elif tag == 'div' and 'entry-content' in attrs_dict.get('class', ''):
            self.in_post_content = True
        elif tag == 'p' and self.in_post_content and not self.first_paragraph:
            self.in_p = True
            self.p_depth += 1

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'p' and self.in_p:
            self.p_depth -= 1
            if self.p_depth == 0:
                self.in_p = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_p and not self.first_paragraph:
            self.first_paragraph += data

def extract_meta(html_content):
    """Extract metadata from HTML content"""
    parser = MetaExtractor()
    parser.feed(html_content)

    # Clean up description from first paragraph
    description = parser.first_paragraph.strip()
    # Remove extra whitespace
    description = ' '.join(description.split())
    # Limit to 200 chars
    if len(description) > 200:
        description = description[:197] + "..."

    return {
        'title': parser.title.strip(),
        'description': description if description else DEFAULT_DESCRIPTION,
        'image': parser.featured_image
    }

def get_canonical_url(file_path):
    """Get the canonical URL for a file"""
    rel_path = str(file_path).replace('./', '')
    if rel_path == 'index.html':
        return BASE_URL + "/"
    return f"{BASE_URL}/{rel_path}"

def get_image_url(image_path, file_path):
    """Convert relative image path to absolute URL"""
    if not image_path:
        return f"{BASE_URL}/{DEFAULT_IMAGE}"

    # Handle relative paths like ../../../images/...
    if image_path.startswith('../'):
        # Count levels up
        levels = image_path.count('../')
        # Get the actual path part
        actual_path = image_path.replace('../', '')
        return f"{BASE_URL}/{actual_path}"
    elif image_path.startswith('images/'):
        return f"{BASE_URL}/{image_path}"
    else:
        # Relative to current file
        file_dir = Path(file_path).parent
        return f"{BASE_URL}/{file_dir}/{image_path}".replace('//', '/')

def create_meta_tags(title, description, url, image_url, page_type="website"):
    """Generate Open Graph and Twitter Card meta tags"""
    return f'''
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="{page_type}">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:site_name" content="{SITE_NAME}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{url}">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image_url}">
'''

def add_meta_to_file(file_path):
    """Add social meta tags to a single HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has og:title
    if 'og:title' in content:
        return False

    # Extract metadata
    meta = extract_meta(content)

    # Determine page type
    page_type = "article" if 'posts/' in str(file_path) else "website"

    # Build URLs
    canonical_url = get_canonical_url(file_path)
    image_url = get_image_url(meta['image'], file_path)

    # Escape HTML entities in description
    description = meta['description'].replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    title = meta['title'].replace('"', '&quot;')

    # Create meta tags
    meta_tags = create_meta_tags(title, description, canonical_url, image_url, page_type)

    # Also add basic meta description if not present
    if '<meta name="description"' not in content:
        meta_tags = f'    <meta name="description" content="{description}">\n' + meta_tags

    # Insert after <title>...</title>
    new_content = re.sub(
        r'(</title>)',
        r'\1' + meta_tags,
        content,
        count=1
    )

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """Add social meta tags to all HTML files"""
    print("Adding social media meta tags...\n")

    base_dir = Path('.')
    updated = 0

    # Find all HTML files
    files = list(base_dir.glob('*.html'))
    files.extend(base_dir.glob('category/*.html'))
    files.extend(base_dir.glob('posts/blog/**/*.html'))

    for file_path in sorted(files):
        if add_meta_to_file(file_path):
            print(f"  + {file_path}")
            updated += 1

    print(f"\n+ Added meta tags to {updated} files")

if __name__ == '__main__':
    main()
