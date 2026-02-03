#!/usr/bin/env python3
"""
Build category listing pages with all posts in each category
Updated for new category structure
"""
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

CATEGORY_NAMES = {
    'milestones': 'Milestones',
    'presentations': 'Presentations',
    'creative-work': 'Creative Work',
    'teaching': 'Teaching',
    'resources': 'Resources',
}

def convert_url_to_local(wp_url):
    """Convert WordPress URL to local static URL"""
    match = re.search(r'leonardoflores\.net/blog/([^/]+)/([^/]+)/?', wp_url)
    if match:
        category = match.group(1)
        slug = match.group(2)
        return f"posts/blog/{category}/{slug}.html"
    return wp_url

def create_category_page_html(category_slug, category_name, posts):
    """Generate HTML for a category listing page"""

    post_items = []
    for post in posts:
        title = post.get('title', 'Untitled')
        date = post.get('date_display', '')
        url = convert_url_to_local(post.get('url', '#'))

        post_items.append(f'''        <li class="category-post-item">
            <a href="../{url}" class="category-post-link">{title}</a>
            <span class="category-post-date">{date}</span>
        </li>''')

    posts_html = '\n'.join(post_items)

    # Build category nav links
    cat_links = []
    for slug, name in CATEGORY_NAMES.items():
        if slug == category_slug:
            cat_links.append(f'<span class="current-category">{name}</span>')
        else:
            cat_links.append(f'<a href="{slug}.html">{name}</a>')
    cat_nav = ' | '.join(cat_links)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_name} - Leonardo Flores</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="icon" href="../images/wp-content/uploads/2019/08/cropped-leoprofilememefavicon-32x32.png">
    <style>
        .category-posts {{
            list-style: none;
            padding: 0;
            margin: 2rem 0;
        }}
        .category-post-item {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--color-accent);
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        .category-post-link {{
            color: var(--color-primary);
            text-decoration: none;
            font-size: 1.1rem;
            flex: 1;
            min-width: 200px;
        }}
        .category-post-link:hover {{
            text-decoration: underline;
        }}
        .category-post-date {{
            color: var(--color-text-light);
            font-size: 0.9rem;
            white-space: nowrap;
        }}
        .category-count {{
            color: var(--color-text-light);
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }}
        .category-nav {{
            margin-bottom: 2rem;
            padding: 1rem;
            background: var(--color-background-alt);
            border-radius: 8px;
        }}
        .category-nav a {{
            color: var(--color-primary);
            text-decoration: none;
            padding: 0.25rem 0.5rem;
        }}
        .category-nav a:hover {{
            text-decoration: underline;
        }}
        .current-category {{
            font-weight: bold;
            padding: 0.25rem 0.5rem;
        }}
    </style>
</head>
<body>
<header>
        <div class="header-top">
            <h1><a href="../index.html">Leonardo Flores</a></h1>
