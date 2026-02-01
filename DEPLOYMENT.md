# Deployment Guide

This guide explains how to deploy the Leonardo Flores static website to various hosting platforms.

## Quick Start - Local Testing

To preview the site locally:

```bash
cd site
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

## GitHub Pages Deployment

### Method 1: Direct Push (Simplest)

1. Create a new GitHub repository or use this one
2. Push the `site/` directory contents to the `main` branch (or `gh-pages` branch)

```bash
cd site
git init
git add .
git commit -m "Initial commit of Leonardo Flores static site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

3. In your GitHub repository settings:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / `root` (or `gh-pages` if you used that branch)
   - Save

Your site will be available at: `https://YOUR_USERNAME.github.io/YOUR_REPO/`

### Method 2: Subtree (Keep source and site together)

If you want to keep the scraping scripts and the site in the same repo:

```bash
# From the leonardoflores-static directory
git add .
git commit -m "Add static site generator and built site"

# Push just the site/ folder to gh-pages branch
git subtree push --prefix site origin gh-pages
```

Then configure GitHub Pages to use the `gh-pages` branch.

## Netlify Deployment

### Drag-and-Drop (Easiest)

1. Go to [Netlify](https://www.netlify.com/)
2. Sign up or log in
3. Drag the `site/` folder onto the Netlify dashboard
4. Your site is live!

### Git-Based (Recommended for updates)

1. Push your code to GitHub (including the `site/` directory)
2. Go to Netlify and click "New site from Git"
3. Connect to your GitHub repository
4. Configure build settings:
   - Build command: (leave empty, since it's already built)
   - Publish directory: `site`
5. Deploy!

Your site will get a random URL like `https://random-name-123.netlify.app/`, which you can customize.

## Vercel Deployment

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
cd site
vercel
```

3. Follow the prompts
   - When asked about the project directory, use `.` (current directory)
   - Framework: None
   - Output directory: leave as default

Your site will be deployed and you'll get a URL like `https://your-site.vercel.app/`

## Custom Domain

### For GitHub Pages:

1. Go to your repository Settings → Pages
2. Under "Custom domain", enter your domain (e.g., `leonardoflores.net`)
3. Create a `CNAME` file in the `site/` directory with your domain name
4. Configure your domain's DNS:
   - Add a CNAME record pointing to `YOUR_USERNAME.github.io`
   - Or add A records to GitHub's IPs (see GitHub docs)

### For Netlify/Vercel:

1. Go to your site dashboard
2. Add custom domain in settings
3. Follow the DNS configuration instructions
4. SSL certificate will be automatically provisioned

## AWS S3 + CloudFront (Advanced)

For high-traffic sites:

1. Create an S3 bucket
2. Enable static website hosting
3. Upload the `site/` contents
4. Set bucket policy for public read access
5. (Optional) Create a CloudFront distribution for CDN
6. (Optional) Configure custom domain with Route 53

```bash
# Using AWS CLI
aws s3 sync site/ s3://your-bucket-name/ --acl public-read
```

## Traditional Web Hosting

If you have traditional web hosting (shared hosting, VPS, etc.):

1. Connect via FTP/SFTP
2. Upload the contents of the `site/` directory to your web root (usually `public_html/` or `www/`)
3. Ensure file permissions are correct (644 for files, 755 for directories)

```bash
# Using rsync
rsync -avz site/ user@yourserver.com:/path/to/webroot/
```

## Performance Optimization

For production deployment, consider:

1. **Minify CSS**: Use a CSS minifier on `site/css/style.css`
2. **Optimize Images**: Use tools like ImageOptim or TinyPNG
3. **Add Compression**: Enable gzip/brotli on your server
4. **Add Caching Headers**: Configure browser caching for static assets
5. **CDN**: Use a CDN for global performance (CloudFlare, Fastly, etc.)

## Updating the Site

To update content:

1. Re-run the scraper scripts to fetch new content
2. Run the build script to regenerate HTML
3. Fix paths with `python3 fix_paths.py`
4. Test locally
5. Deploy updated `site/` directory

```bash
python3 full_scraper.py
python3 download_images.py
python3 build_static_site.py
python3 fix_paths.py
# Test locally first
cd site && python3 -m http.server 8000
# Then deploy
```

## Troubleshooting

### Images not loading

- Check that the `images/` directory is present in the deployed site
- Verify paths in HTML match the deployed structure
- Check browser console for 404 errors

### CSS not applying

- Verify `css/style.css` is accessible
- Check for typos in the `<link>` tag
- Clear browser cache

### 404 errors on navigation

- Ensure all `.html` files are present
- Check that links don't have extra slashes or wrong extensions
- Verify relative paths are correct

## Security Notes

- No server-side code = reduced attack surface
- No database = no SQL injection risks
- Static files only = highly secure by default
- Consider adding security headers (CSP, HSTS, etc.) via hosting platform

## Monitoring

Set up monitoring for your site:

- Google Analytics (add tracking code to template)
- Uptime monitoring (UptimeRobot, Pingdom)
- Google Search Console for SEO

## Support

For issues with:
- **The site itself**: Check the source files in `leonardoflores-static/`
- **Hosting platforms**: Consult their documentation
- **Domain configuration**: Contact your DNS provider

---

Last updated: February 1, 2026
