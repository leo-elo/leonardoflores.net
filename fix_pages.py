#!/usr/bin/env python3
"""
Fix pages (about, calendar, courses, publications) to match post template styling
"""
import re
from pathlib import Path
from html.parser import HTMLParser

class ContentExtractor(HTMLParser):
    """Extract the actual content from WordPress markup"""

    def __init__(self):
        super().__init__()
        self.content = []
        self.in_content_div = False
        self.title = ""
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Capture title from inner header
        if tag == 'h1' and not self.title:
            return

        if self.in_content_div:
            self.depth += 1
            # Reconstruct the tag
            attrs_str = ' '.join([f'{k}="{v}"' for k, v in attrs])
            if attrs_str:
                self.content.append(f'<{tag} {attrs_str}>')
            else:
                self.content.append(f'<{tag}>')

    def handle_endtag(self, tag):
        if self.in_content_div:
            if self.depth > 0:
                self.content.append(f'</{tag}>')
                self.depth -= 1

    def handle_data(self, data):
        if self.in_content_div:
            self.content.append(data)

def fix_page_content(html, page_name):
    """Clean up page content and apply post template styling"""

    # Extract title
    title_match = re.search(r'<header><h1>([^<]+)</h1></header>', html)
    title = title_match.group(1) if title_match else page_name

    # Extract content from WordPress div structure
    # Pattern: <div id="primary"><main id="main"><article id="post-xxx"><header>...</header><div>CONTENT</div>
    content_match = re.search(
        r'<div id="primary">.*?<article[^>]*>.*?<header>.*?</header><div>(.*?)</div>\s*(?:</article>)?\s*(?:</main>)?\s*(?:</article>)?',
        html,
        re.DOTALL
    )

    if content_match:
        content = content_match.group(1).strip()
    else:
        # Try simpler extraction
        content_match2 = re.search(r'<div id="primary">.*?<div>(.+?)</div>\s*$', html, re.DOTALL)
        if content_match2:
            content = content_match2.group(1).strip()
        else:
            return html  # Can't extract, return unchanged

    # Create clean article structure matching post template
    new_article = f'''<article class="page-content">
            <header class="post-header">
                <h1 class="post-title">{title}</h1>
            </header>
            <div class="entry-content">
                {content}
            </div>
        </article>'''

    # Replace the main content section
    html = re.sub(
        r'<main>\s*<article>.*?</article>\s*</main>',
        f'<main>\n        {new_article}\n    </main>',
        html,
        flags=re.DOTALL
    )

    return html

def fix_page(file_path):
    """Fix a page to match post template"""
    print(f"Fixing {file_path}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Fix CSS and resource paths (remove ../ prefix for root-level pages)
    html = re.sub(r'href="\.\./css/style\.css"', 'href="css/style.css"', html)
    html = re.sub(r'href="\.\./images/', 'href="images/', html)
    html = re.sub(r'href="\.\./index\.html"', 'href="index.html"', html)
    html = re.sub(r'href="\.\./"', 'href="index.html"', html)
    html = re.sub(r'src="\.\./js/search\.js"', 'src="js/search.js"', html)

    # Fix content structure
    page_name = file_path.stem.title()
    html = fix_page_content(html, page_name)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  ✓ Fixed")

def main():
    """Fix all pages"""
    print("Fixing pages to match post template...\n")

    pages = ['about.html', 'calendar.html', 'courses.html', 'publications.html']

    for page in pages:
        path = Path(page)
        if path.exists():
            fix_page(path)
        else:
            print(f"  Skipping {page} (not found)")

    print("\n✓ All pages fixed")

if __name__ == '__main__':
    main()
