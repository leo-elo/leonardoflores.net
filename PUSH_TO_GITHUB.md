# Push to GitHub - Authentication Required

Your repository is created and ready, but you need to authenticate with GitHub to push the code.

## Quick Push (Run These Commands)

Open your terminal and run:

```bash
cd /Users/floresll/Desktop/github/leonardoflores-static

# Push main branch
git push -u origin main

# Push gh-pages branch (this is your live site)
git push -u origin gh-pages
```

When prompted:
- **Username**: `leo-elo`
- **Password**: Use a Personal Access Token (not your GitHub password)

## Don't Have a Personal Access Token?

### Create One (2 minutes):

1. Go to: **https://github.com/settings/tokens/new**
2. Note: `leonardoflores.net deployment`
3. Expiration: `90 days` (or your preference)
4. Select scopes: Check **`repo`** (full control of private repositories)
5. Click **Generate token**
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when git asks

---

## Alternative: Use GitHub CLI (Easier)

If you have GitHub CLI installed:

```bash
# Login to GitHub
gh auth login

# Then push
git push -u origin main
git push -u origin gh-pages
```

---

## After Pushing

Once the push succeeds, enable GitHub Pages:

1. Go to: **https://github.com/leo-elo/leonardoflores.net/settings/pages**
2. Source: **gh-pages** branch, **/ (root)** folder
3. Custom domain: **leonardoflores.net**
4. Click **Save**
5. Check **Enforce HTTPS**

Your site will be live at:
- **https://leo-elo.github.io/leonardoflores.net/** (GitHub Pages)
- **https://leonardoflores.net/** (after DNS setup)

---

## Need Help?

Run the commands above in your terminal. GitHub will prompt you for credentials.
