#!/usr/bin/env python3
"""
Update all HTML pages with the new header structure (hamburger menu, search after tagline)
"""
import re
from pathlib import Path

def get_prefix(html_file):
    """Get the correct path prefix based on file location"""
    html_path = Path(html_file)

    if html_path.parent.name == 'leonardoflores-static':
        return ''
    elif html_path.parent.name == 'category':
        return '../'
    elif 'posts/blog' in str(html_path):
        return '../../../'
    else:
        return ''

def update_header(html_file):
    """Update header structure in a single file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has menu-toggle
    if 'menu-toggle' in content:
        return False

    prefix = get_prefix(html_file)

    # Pattern to match old header structure
