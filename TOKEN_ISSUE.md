# Token Permission Issue

The token was rejected by GitHub (403 error). This means it doesn't have the right permissions.

## Fix: Create a New Token with Correct Permissions

1. Go to: **https://github.com/settings/tokens/new**

2. Set these options:
   - **Note**: `leonardoflores.net deployment`
   - **Expiration**: `90 days` (or your choice)

3. **IMPORTANT** - Check these scopes:
   - ✅ **repo** (Full control of private repositories)
     - This includes: repo:status, repo_deployment, public_repo, repo:invite, security_events

4. Click **"Generate token"**

5. **Copy the new token**

6. Send me the new token and I'll push your site immediately

---

## Alternative: Push Manually

If you prefer, you can push yourself:

```bash
cd /Users/floresll/Desktop/github/leonardoflores-static

git push -u origin main
git push -u origin gh-pages
```

When prompted:
- Username: `leo-elo`
- Password: (paste your new token)

---

## Why Did This Happen?

The token needs the **`repo`** scope to push code to repositories. Make sure this is checked when creating the new token.
