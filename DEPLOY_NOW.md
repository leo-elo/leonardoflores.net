# Deploy Your Site Now! 🚀

Your static site is ready to deploy. Here are your options:

## Option 1: GitHub Pages (Recommended - Free)

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository named `leonardoflores-static` (or any name you prefer)
3. **Important**: Do NOT initialize with README, .gitignore, or license
4. Click "Create repository"

### Step 2: Push Your Code

Copy and paste these commands in your terminal:

```bash
cd /Users/floresll/Desktop/github/leonardoflores-static

# Add your GitHub repository as remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/leonardoflores-static.git

# Push main branch
git push -u origin main

# Push gh-pages branch (this is what will be deployed)
git push -u origin gh-pages
```

### Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" (top menu)
3. Click "Pages" (left sidebar)
4. Under "Source":
   - Branch: Select **gh-pages**
   - Folder: Select **/ (root)**
5. Click "Save"

### Step 4: Get Your URL

Your site will be live at:
```
https://USERNAME.github.io/leonardoflores-static/
```

It takes 1-2 minutes to deploy. Refresh the Settings → Pages page to see the URL.

---

## Option 2: Netlify (Super Easy - Drag & Drop)

1. Go to [Netlify](https://app.netlify.com/)
2. Sign up or log in
3. Drag the `site/` folder onto the Netlify dashboard
4. Done! Your site is live with a URL like `https://random-name.netlify.app/`

You can customize the URL in Netlify settings.

---

## Option 3: Vercel (Fast Deploy)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd /Users/floresll/Desktop/github/leonardoflores-static/site
vercel

# Follow the prompts (press Enter for defaults)
```

Your site will be live instantly with a URL like `https://your-site.vercel.app/`

---

## Custom Domain Setup

Once deployed, you can add a custom domain:

### For GitHub Pages:
1. Go to repository Settings → Pages
2. Under "Custom domain", enter your domain
3. Update your domain's DNS:
   - Add a CNAME record pointing to `USERNAME.github.io`

### For Netlify/Vercel:
1. Go to site settings
2. Click "Add custom domain"
3. Follow the DNS configuration instructions

---

## Current Status

✅ Git repository initialized
✅ Initial commit created
✅ gh-pages branch created (ready for GitHub Pages)
✅ Site is 100% ready to deploy

**All you need to do is:**
1. Create a GitHub repository
2. Run the git commands above (replacing USERNAME)
3. Enable GitHub Pages
4. Your site is live!

---

## Need Help?

- **GitHub Pages docs**: https://docs.github.com/en/pages
- **Netlify docs**: https://docs.netlify.com/
- **Vercel docs**: https://vercel.com/docs

## Test Locally First (Optional)

```bash
cd /Users/floresll/Desktop/github/leonardoflores-static/site
python3 -m http.server 8000
# Open http://localhost:8000
```

Press Ctrl+C to stop the server.

---

**Ready to go live? Choose an option above and deploy! 🎉**
