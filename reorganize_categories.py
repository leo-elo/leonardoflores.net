#!/usr/bin/env python3
"""
Reorganize categories according to new structure:
- news, grants, publications, interviews, proposals, editorial-work → milestones
- e-poetry-sites → resources
- performances → creative-work
- courses, pedagogy → teaching
- uncategorized → assign individually
"""
import json
import re
import os
from pathlib import Path
from collections import defaultdict

# Category mapping: old_slug → new_slug
CATEGORY_MAPPING = {
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
    'creative-work': 'creative-work',
    'resources': 'resources',
}

# Category display names
CATEGORY_NAMES = {
    'milestones': 'Milestones',
    'presentations': 'Presentations',
    'creative-work': 'Creative Work',
    'teaching': 'Teaching',
    'resources': 'Resources',
}

# Uncategorized posts assignment (based on title keywords)
UNCATEGORIZED_ASSIGNMENTS = {
    'Teaching Critical Memes': 'teaching',
    'Presentation: Beyond the Book': 'presentations',
    'Río Grande Review': 'milestones',
    'NEH Summer Stipend Proposal': 'milestones',
    'Proposal for NEH Enduring Questions': 'milestones',
    'Blog updated': 'milestones',
    'Presentation at UPR Ponce': 'presentations',
    'Wordle of my Dissertation': 'milestones',
    'Google it! Workshop': 'presentations',
    'E-Poetry 2011 Presentation': 'presentations',
    'Spring 2011 Update': 'milestones',
    'About Me': 'milestones',
    'Spring 2011 Courses': 'teaching',
    'Presentación Octavo Congreso': 'presentations',
    'Leonardo Flores, Ph.D.': 'milestones',
    'Blast from the Past': 'teaching',
    'Keynote Address at Western TESOL': 'presentations',
    'The Music of Poetry Workshop': 'presentations',
    'The Language of Poetry Workshop': 'presentations',
    'Fall 2009 Update': 'milestones',
    'Spring 2009 Update': 'milestones',
    'Spring 2008 Update': 'milestones',
    'Hello World': 'milestones',
}

def get_new_category(old_category, title=''):
    """Get the new category for a post"""
    if old_category == 'uncategorized':
        # Check title against assignments
        for title_prefix, new_cat in UNCATEGORIZED_ASSIGNMENTS.items():
            if title.startswith(title_prefix):
                return new_cat
        return 'milestones'  # Default for uncategorized

    return CATEGORY_MAPPING.get(old_category, old_category)

def update_post_file(file_path, old_category, new_category):
    """Update a post HTML file with new category"""
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update category links in the post
    old_cat_display = old_category.replace('-', ' ').title()
    if old_category == 'presentations-2':
        old_cat_display = 'Presentations'
    new_cat_display = CATEGORY_NAMES.get(new_category, new_category.replace('-', ' ').title())

    # Update category link hrefs
    html = re.sub(
        rf'href="[^"]*category/{old_category}\.html"',
        f'href="../../../category/{new_category}.html"',
        html
    )
    html = re.sub(
        rf'href="[^"]*{old_category}\.html">({old_cat_display}|{old_category})',
        f'href="../../../category/{new_category}.html">{new_cat_display}',
        html,
        flags=re.IGNORECASE
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

def move_post_file(old_path, new_category):
    """Move post file to new category directory"""
    old_path = Path(old_path)
    if not old_path.exists():
        return None

    # Create new directory
    new_dir = Path(f'posts/blog/{new_category}')
    new_dir.mkdir(parents=True, exist_ok=True)

    # New path
    new_path = new_dir / old_path.name

    # Read, update, and write to new location
    with open(old_path, 'r', encoding='utf-8') as f:
        html = f.read()

    with open(new_path, 'w', encoding='utf-8') as f:
        f.write(html)

    # Remove old file
    old_path.unlink()

    return new_path

def main():
    """Reorganize all categories"""
    print("=== REORGANIZING CATEGORIES ===\n")

    # Load posts data
    with open('all_posts_full.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)

    # Track changes
    changes = defaultdict(list)

    # Process each post
    for post in posts:
        url = post.get('url', '')
        title = post.get('title', '')

        # Extract old category
        match = re.search(r'leonardoflores\.net/blog/([^/]+)/([^/]+)/?', url)
        if not match:
            continue

        old_category = match.group(1)
        slug = match.group(2)

        # Get new category
        new_category = get_new_category(old_category, title)

        if old_category != new_category:
            changes[f'{old_category} → {new_category}'].append(title)

            # Move the file
            old_path = Path(f'posts/blog/{old_category}/{slug}.html')
            if old_path.exists():
                new_path = move_post_file(old_path, new_category)
                if new_path:
                    update_post_file(new_path, old_category, new_category)
                    print(f"Moved: {old_path} → {new_path}")

    # Print summary
    print("\n=== CHANGES SUMMARY ===\n")
    for change, titles in sorted(changes.items()):
        print(f"{change}: {len(titles)} posts")

    # Clean up empty directories
    print("\n=== CLEANING UP ===\n")
    for old_cat in ['news', 'grants', 'publications', 'interviews', 'proposals',
                    'editorial-work', 'e-poetry-sites', 'performances', 'courses',
                    'pedagogy', 'uncategorized', 'presentations-2']:
        old_dir = Path(f'posts/blog/{old_cat}')
        if old_dir.exists():
            try:
                old_dir.rmdir()
                print(f"Removed empty directory: {old_dir}")
            except OSError:
                # Directory not empty, list remaining files
                remaining = list(old_dir.glob('*.html'))
                if remaining:
                    print(f"Directory {old_dir} still has {len(remaining)} files")

    # Update posts data with new categories
    print("\n=== UPDATING POSTS DATA ===\n")
    for post in posts:
        url = post.get('url', '')
        title = post.get('title', '')

        match = re.search(r'leonardoflores\.net/blog/([^/]+)/([^/]+)/?', url)
        if match:
            old_category = match.group(1)
            slug = match.group(2)
            new_category = get_new_category(old_category, title)

            # Update the URL in posts data
            post['url'] = f"https://leonardoflores.net/blog/{new_category}/{slug}/"
            post['category'] = new_category

    # Save updated posts data
    with open('all_posts_full.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print("Updated all_posts_full.json")

    print("\n✓ Category reorganization complete!")
    print("\nNew category structure:")

    # Count posts per new category
    cat_counts = defaultdict(int)
    for post in posts:
        cat = post.get('category', 'unknown')
        cat_counts[cat] += 1

    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {CATEGORY_NAMES.get(cat, cat)}: {count} posts")

if __name__ == '__main__':
    main()
