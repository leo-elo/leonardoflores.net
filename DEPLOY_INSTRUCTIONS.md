# Deploy to leonardoflores.net 🚀

## Quick Deploy (3 Steps)

### Step 1: Create GitHub Repository

Go to: **https://github.com/new**

Settings:
- Repository name: **leonardoflores.net**
- Description: `Static site for leonardoflores.net`
- **Public** repository
- **Do NOT** initialize with README, .gitignore, or license
- Click **"Create repository"**

### Step 2: Run Deployment

After creating the repository, run:

```bash
cd /Users/floresll/Desktop/github/leonardoflores-static
./deploy.sh
```

This will push your code to GitHub.

### Step 3: Enable GitHub Pages

1. Go to: **https://github.com/leo-elo/leonardoflores.net/settings/pages**
2. Under "Source":
   - Branch: **gh-pages**
   - Folder: **/ (root)**
3. Click **Save**

---

## Your Site URLs

**GitHub Pages URL (temporary):**
- https://leo-elo.github.io/leonardoflores.net/

**Custom Domain (after DNS setup):**
- https://leonardoflores.net/

---

## Custom Domain Setup (Optional - After Deployment)

Once GitHub Pages is enabled, you can point leonardoflores.net to it:

### In GitHub:
1. Go to: https://github.com/leo-elo/leonardoflores.net/settings/pages
2. Under "Custom domain", enter: `leonardoflores.net`
3. Check "Enforce HTTPS"
4. Click Save

### In Your Domain Registrar:
Update DNS records:

**Option A - Using CNAME (Recommended):**
```
Type: CNAME
Name: www
Value: leo-elo.github.io
```

**Option B - Using A Records:**
```
Type: A
Name: @
Value: 185.199.108.153

Type: A
Name: @
Value: 185.199.109.153

Type: A
Name: @
Value: 185.199.110.153

Type: A
Name: @
Value: 185.199.111.153
```

Wait 5-30 minutes for DNS propagation.

---

## Ready to Deploy?

1. **First**: Create the repository at https://github.com/new
2. **Then**: Run `./deploy.sh`
3. **Finally**: Enable GitHub Pages in settings

Your site will be live! 🎉
