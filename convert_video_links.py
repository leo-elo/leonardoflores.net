#!/usr/bin/env python3
"""
Convert plain YouTube and Vimeo links to embedded videos
"""
import re
from pathlib import Path

def convert_youtube_to_embed(url):
    """Convert YouTube URL to embed iframe"""
    # Extract video ID from various YouTube URL formats
    patterns = [
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'youtu\.be/([a-zA-Z0-9_-]+)',
        r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
    ]

    video_id = None
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            # Remove any timestamp or extra params for the ID
            video_id = video_id.split('?')[0].split('&')[0]
            break

    if not video_id:
        return None

    return f'''<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>'''

def convert_vimeo_to_embed(url):
    """Convert Vimeo URL to embed iframe"""
    match = re.search(r'vimeo\.com/(\d+)', url)
    if not match:
        return None

    video_id = match.group(1)
    return f'''<div class="video-container">
<iframe src="https://player.vimeo.com/video/{video_id}" width="560" height="315" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
</div>'''

def process_file(file_path):
    """Process a single HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = 0

    # Pattern for standalone YouTube/Vimeo links (not already in iframes or href)
    # Match links that are:
    # 1. On their own line or in a <p> tag
    # 2. Not part of an href attribute
    # 3. Not already in an iframe

    # YouTube patterns - standalone URLs
    youtube_patterns = [
        # <p>https://www.youtube.com/watch?v=xxx</p>
        (r'<p>\s*(https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+)\s*</p>', 'youtube'),
        # <p>http://www.youtube.com/watch?v=xxx</p>
        (r'<p>\s*(http://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+)\s*</p>', 'youtube'),
        # standalone youtu.be links
        (r'<p>\s*(https?://youtu\.be/[a-zA-Z0-9_-]+)\s*</p>', 'youtube'),
        # Plain URL on a line (not in tags)
        (r'^(https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+)\s*$', 'youtube'),
        (r'^(https?://youtu\.be/[a-zA-Z0-9_-]+)\s*$', 'youtube'),
        # URL followed by newline in content
        (r'\n(https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+)\s*\n', 'youtube'),
        (r'\n(https?://youtu\.be/[a-zA-Z0-9_-]+)\s*\n', 'youtube'),
    ]

    # Vimeo patterns
    vimeo_patterns = [
        (r'<p>\s*(https?://(?:www\.)?vimeo\.com/\d+)\s*</p>', 'vimeo'),
        (r'^(https?://(?:www\.)?vimeo\.com/\d+)\s*$', 'vimeo'),
        (r'\n(https?://(?:www\.)?vimeo\.com/\d+)\s*\n', 'vimeo'),
    ]

    all_patterns = youtube_patterns + vimeo_patterns

    for pattern, video_type in all_patterns:
        matches = list(re.finditer(pattern, content, re.MULTILINE))
        for match in reversed(matches):  # Reverse to not mess up positions
            url = match.group(1)

            # Skip if this is inside an href or already embedded
            start = max(0, match.start() - 100)
            context = content[start:match.start()]
            if 'href="' in context[-50:] or 'iframe' in context[-100:]:
                continue

            if video_type == 'youtube':
                embed = convert_youtube_to_embed(url)
            else:
                embed = convert_vimeo_to_embed(url)

            if embed:
                # Replace the full match
                full_match = match.group(0)
                if full_match.startswith('<p>'):
                    replacement = embed
                elif full_match.startswith('\n'):
                    replacement = '\n' + embed + '\n'
                else:
                    replacement = embed

                content = content[:match.start()] + replacement + content[match.end():]
                changes += 1

    if changes > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

def main():
    print("Converting video links to embeds...\n")

    total_changes = 0

    # Process all HTML files in posts/blog
    for html_file in Path('posts/blog').rglob('*.html'):
        changes = process_file(html_file)
        if changes > 0:
            print(f"  + {html_file}: {changes} videos embedded")
            total_changes += changes

    print(f"\n+ Converted {total_changes} video links to embeds")

if __name__ == '__main__':
    main()
