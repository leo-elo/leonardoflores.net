#!/usr/bin/env python3
"""
Add 'En Español' category for Spanish language posts
"""
import json
import re
from pathlib import Path
from datetime import datetime

# Spanish keywords to identify posts
SPANISH_KEYWORDS = [
    'español', 'presentación', 'taller', 'literatura electrónica',
    'ponencia', 'en español', 'curso', 'publicaciones y entrevistas en español',
    'reinventando la literatura', 'congreso de educación'
]

def is_spanish_post(title):
    """Check if a post is in Spanish based on title"""
    title_lower = title.lower()
    return any(kw in title_lower for kw in SPANISH_KEYWORDS)

def create_spanish_category_page(posts):
    """Create the En Español category page"""

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

    # Generate post list
    post_items = []
    for post in posts:
        title = post.get('title', 'Untitled')
        date = post.get('date_display', '')

        # Get local URL
        url = post.get('url', '')
        match = re.search(r'leonardoflores\.net/blog/([^/]+)/([^/]+)/?', url)
        if match:
            category = match.group(1)
            slug = match.group(2)
            # Map to new category
            CATEGORY_MAP = {
                'news': 'milestones', 'grants': 'milestones', 'publications': 'milestones',
                'interviews': 'milestones', 'proposals': 'milestones', 'editorial-work': 'milestones',
                'e-poetry-sites': 'resources', 'performances': 'creative-work',
                'courses': 'teaching', 'pedagogy': 'teaching',
                'presentations-2': 'presentations', 'uncategorized': 'milestones',
            }
            new_category = CATEGORY_MAP.get(category, category)
            local_url = f"../posts/blog/{new_category}/{slug}.html"
        else:
            local_url = '#'

        post_items.append(f'''        <li class="category-post-item">
            <a href="{local_url}" class="category-post-link">{title}</a>
            <span class="category-post-date">{date}</span>
        </li>''')

    posts_html = '\n'.join(post_items)

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>En Español - Leonardo Flores</title>
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
            margin-bottom: 2rem;
        }}
    </style>
</head>
<body>
<header>
        <div class="header-top">
            <h1><a href="../index.html">Leonardo Flores</a></h1>
