# leonardoflores.net

Static website for [leonardoflores.net](https://leonardoflores.net) — built with Jekyll 4.3 and hosted on GitHub Pages.

---

## Quick reference

| Item | Value |
|------|-------|
| Live URL | https://leonardoflores.net |
| GitHub repo | https://github.com/leo-elo/leonardoflores.net |
| Deployment branch | `gh-pages` |
| Local path | `/Users/floresll/Desktop/Websites/leonardoflores-static` |
| Jekyll version | 4.3 |
| Ruby version | 3.2 |

---

## Deployment

**Pushing to `gh-pages` deploys the site automatically.**

GitHub Actions (`.github/workflows/jekyll.yml`) triggers on every push to `gh-pages`, builds the site with Jekyll, and publishes it to GitHub Pages. No manual build step needed.

```bash
git add .
git commit -m "Your message"
git push origin gh-pages
```

Other branches (`main`, `jekyll-migration`) do **not** trigger a deploy.

---

## Running locally

```bash
cd /Users/floresll/Desktop/Websites/leonardoflores-static
/opt/homebrew/opt/ruby/bin/bundle install   # first time only
/opt/homebrew/opt/ruby/bin/bundle exec jekyll serve
```

Then visit `http://localhost:4000`. Changes to most files hot-reload; `_config.yml` changes require a restart.

### Local admin UI (jekyll-admin)

With the server running, visit `http://localhost:4000/_jekyll_admin/` for a GUI to create and edit posts without touching the terminal. Changes are saved directly to the local files; commit and push as usual to deploy.

---

## Content Management (Decap CMS — live site)

The live admin interface is at `https://leonardoflores.net/admin/`. It lets you create and edit posts from any browser; changes are committed directly to the `gh-pages` branch and trigger an automatic deploy.

### One-time setup (required before first use)

**Step 1 — Register a GitHub OAuth App**

1. Go to GitHub → Settings → Developer settings → OAuth Apps → **New OAuth App**
2. Fill in:
   - Application name: `leonardoflores.net CMS`
   - Homepage URL: `https://leonardoflores.net`
   - Authorization callback URL: `https://api.netlify.com/auth/done`
3. Click **Register application**, then note the **Client ID** and generate a **Client Secret**

**Step 2 — Configure Netlify as the OAuth proxy**

1. Create a free account at [netlify.com](https://netlify.com) (no need to host the site there)
2. Create any new site (a blank placeholder is fine)
3. Go to **Site Settings → Access control → OAuth → Install provider**
4. Choose **GitHub**, paste in the Client ID and Client Secret from Step 1
5. Save

That's it. Visit `https://leonardoflores.net/admin/`, click **Login with GitHub**, and the CMS is ready.

### CMS config file

`admin/config.yml` defines all fields and collections. To add new fields to posts or create new content types, edit that file.

---

## Directory structure

```
_config.yml                         Site configuration
_layouts/
  default.html                      Base template (header + main + footer)
  landing.html                      Homepage (accordion + modal popups)
  home.html                         Blog index grid with pagination
  post.html                         Individual blog post
  page.html                         Generic static page
  category.html                     Category listing page
  redirect.html                     Redirect helper
_includes/
  head.html                         <head>: SEO, OG tags, CSS, Google Analytics
  header.html                       Site header and navigation
  footer.html                       Footer: copyright, CC-BY 4.0, search box
  post-card.html                    Card component used in the blog grid
_plugins/
  category_page_generator.rb        Auto-generates /category/<slug>.html pages
_posts/                             All blog posts (HTML files, dating to 2007)
css/
  style.css                         Main stylesheet
js/
  search.js                         Client-side search (reads search-data.json)
images/
  cyberleo2026.png                  Default OG/Twitter image and favicon
  creative_works/                   Thumbnails for creator.html
  courses/                          Course thumbnails
  wp-content/                       Migrated WordPress media
courses/                            Course subsites (served at /courses/<name>/)
search-data.json                    Auto-generated search index
```

### Top-level pages

| File | URL | Layout | Notes |
|------|-----|--------|-------|
| `index.html` | `/` | landing | Homepage with accordion/modal |
| `about.html` | `/about.html` | page | Bio, CV link, publications, contact |
| `blog.html` | `/blog.html` | home | Blog grid, page 1 |
| `blog-page-N.html` | `/blog-page-N.html` | home | Blog pages 2–14 |
| `creator.html` | `/creator.html` | page | Published & self-published creative works |
| `leader.html` | `/leader.html` | page | Leadership roles and accomplishments |
| `calendar.html` | `/calendar.html` | page | Events calendar |
| `post-index.html` | `/post-index.html` | default | Full post list sorted by date |
| `courses.html` | `/courses.html` | page | Course listing |
| `404.html` | `/404.html` | default | Custom error page |

---

## Adding a blog post

Create a file in `_posts/` named `YYYY-MM-DD-slug.html` (or `.md`).

### Required front matter

```yaml
---
layout: post
title: "Post Title Here"
date: YYYY-MM-DD
categories: [news]
---
```

### Optional front matter

```yaml
featured_image: /images/your-image.jpg
featured_image_alt: "Description of the image"
```

### Categories

Posts must use one or more of these six category slugs (defined in `_config.yml` and `_plugins/category_page_generator.rb`):

| Slug | Display name | URL |
|------|-------------|-----|
| `news` | News | `/category/news.html` |
| `presentations` | Presentations | `/category/presentations.html` |
| `creative-work` | Creative Work | `/category/creative-work.html` |
| `teaching` | Teaching | `/category/teaching.html` |
| `resources` | Resources | `/category/resources.html` |
| `en-espanol` | En Español | `/category/en-espanol.html` |

Category pages are generated automatically at build time by `_plugins/category_page_generator.rb` — no manual page files needed.

---

## Adding a creative work to creator.html

Open [`creator.html`](creator.html) and add a card inside the appropriate `.creative-works-grid` div:

```html
<div class="creative-work-card">
    <a href="URL_TO_WORK" target="_blank" rel="noopener">
        <img src="{{ '/images/creative_works/your-image.png' | relative_url }}" alt="Work Title" class="work-thumbnail">
        <h3 class="work-title">Work Title</h3>
        <p class="work-metadata">type, year</p>
    </a>
</div>
```

Place the thumbnail image in `images/creative_works/`. Recommended size: 500×500px or similar square crop.

---

## Updating static pages (About, Leader, Creator)

These pages use the `page` layout and contain their content as inline HTML. Edit the files directly:

- [`about.html`](about.html) — bio, CV link, publications, contact
- [`leader.html`](leader.html) — leadership roles and accomplishments
- [`creator.html`](creator.html) — creative works grids

---

## Navigation

The navigation is defined in [`_includes/header.html`](_includes/header.html). To add or reorder nav links, edit that file.

The tagline links in the header (Leader / Scholar / Educator / Creator) also live in `header.html`.

---

## Design

- **Accent color:** `#FDE801` (yellow)
- **Google Analytics ID:** `G-E8G8SJB7V6` (set in `_includes/head.html`)
- **Default OG/social image:** `/images/cyberleo2026.png`
- **License:** CC-BY 4.0

---

## Courses

Course subsites live in the `courses/` directory and are served at `/courses/<name>/`. Each course has its own folder with its own HTML files. A top-level `courses.html` and the `courses/` index list all courses.

---

## Plugins

| Plugin | Purpose |
|--------|---------|
| `jekyll-paginate-v2` | Blog pagination (configured in `_config.yml`) |
| `_plugins/category_page_generator.rb` | Generates category archive pages at build time |

> **Note:** Custom plugins in `_plugins/` are not supported by GitHub Pages' default Jekyll build. This site uses a custom GitHub Actions workflow (`jekyll.yml`) precisely to support the category generator plugin.

---

## Files excluded from build

These files are in the repo but not included in the Jekyll output (see `exclude` in `_config.yml`):

`Gemfile`, `Gemfile.lock`, `*.py`, `all_posts.json`, `all_posts_cards.json`, `all_posts_full.json`, `posts-data.json`, `convert_to_jekyll.py`, `README.md`, `vendor/`
