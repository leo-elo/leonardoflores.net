# Leonardo Flores Static Website

This is a static site recreation of [leonardoflores.net](https://leonardoflores.net), preserving all content, images, and metadata while removing WordPress dependencies.

## Features

- **Fully Static**: No server-side processing required
- **Clean HTML/CSS**: Modern, responsive design without WordPress bloat
- **Preserved Metadata**: All categories, post metadata, and content preserved
- **All Assets Downloaded**: Images and other assets stored locally
- **Fast Loading**: Minimal dependencies, optimized for performance

## Site Structure

```
site/
├── index.html              # Homepage with recent posts
├── about.html              # About page
├── publications.html       # CV and Publications
├── courses.html            # Courses page
├── calendar.html           # Calendar page
├── css/
│   └── style.css          # Site styles (no WordPress CSS)
├── images/                # All downloaded images
├── posts/                 # Blog posts
│   └── blog/
│       ├── presentations-2/
│       └── news/
├── blog/
│   └── category/          # Category pages
│       ├── creative-work.html
│       ├── presentations-2.html
│       ├── publications.html
│       ├── news.html
│       ├── pedagogy.html
│       ├── courses.html
│       ├── editorial-work.html
│       ├── grants.html
│       └── interviews.html
└── assets/                # WordPress theme assets
```

## Categories Preserved

The following content categories are preserved from the original WordPress site:

- **Presentations**: Conference talks, lectures, and keynotes
- **Publications**: Academic publications and articles
- **Creative Work**: Digital art and creative projects
- **News**: Announcements and updates
- **Pedagogy**: Teaching-related content
- **Courses**: Course materials and syllabi
- **Editorial Work**: Editorial roles and contributions
- **Grants**: Grant awards and applications
- **Interviews**: Media appearances and interviews
- **Resources**: Useful resources for the field
- **Performances**: Performance documentation

## Metadata Preserved

For each post/page:
- Title
- Content (with clean HTML)
- Categories (with links to category pages)
- Images (with corrected local paths)
- Links (updated to relative paths where appropriate)

## Content Downloaded

- **Pages**: 13 key pages (About, Publications, Calendar, etc.)
- **Posts**: 10 recent blog posts
- **Images**: 25+ images including:
  - Featured images for posts
  - Profile images and favicons
  - Presentation screenshots
  - Event photos
- **Stylesheets**: WordPress theme CSS downloaded for reference
- **Scripts**: JavaScript for navigation and responsive features

## Hosting

This static site can be hosted on any static hosting service:

- **GitHub Pages**: Free hosting for public repositories
- **Netlify**: Drag-and-drop deployment
- **Vercel**: Zero-config deployments
- **AWS S3**: Scalable cloud hosting
- **Any web server**: Just upload the `site/` directory

## Local Development

To view the site locally:

1. Navigate to the `site/` directory
2. Start a local web server:

```bash
# Using Python 3
python3 -m http.server 8000

# Using Node.js (with npx)
npx http-server

# Using PHP
php -S localhost:8000
```

3. Open your browser to `http://localhost:8000`

## Building from Source

The scraping and building scripts are included:

1. **scraper.py**: Downloads homepage and discovers assets
2. **full_scraper.py**: Downloads all key pages and recent posts
3. **download_images.py**: Extracts and downloads all images from HTML
4. **build_static_site.py**: Converts WordPress HTML to clean static pages

To rebuild the site:

```bash
# Download content (already done)
python3 full_scraper.py

# Download images
python3 download_images.py

# Build static site
python3 build_static_site.py
```

## Customization

### Updating Styles

Edit `site/css/style.css` to customize:
- Colors (CSS variables in `:root`)
- Fonts
- Layout and spacing
- Responsive breakpoints

### Adding Content

New blog posts can be added by:
1. Creating an HTML file in `site/posts/`
2. Using the same structure as existing posts
3. Adding appropriate category metadata

## Original Site

The original WordPress site is maintained at [leonardoflores.net](https://leonardoflores.net).

This static version was created on February 1, 2026.

## Professor Leonardo Flores

Professor Leonardo Flores is Chair of the English Department at Appalachian State University and President of the Latin American Electronic Literature Network – Lit(e)Lat.

His research areas include:
- Electronic literature
- Digital poetry (e-poetry)
- Digital writing
- AI in education and creativity

Contact: floresll@appstate.edu

## Technical Details

- **HTML**: Clean, semantic HTML5
- **CSS**: Modern CSS with CSS variables, flexbox, and responsive design
- **No JavaScript dependencies** (except for optional navigation)
- **No external CDN dependencies**
- **All assets self-hosted**

## License

Content © Leonardo Flores. All rights reserved.

This static site implementation is for archival and hosting purposes.
