#!/bin/bash
# GitHub Pages Deployment Script
# Replace YOUR_GITHUB_USERNAME with your actual GitHub username

# Configuration
GITHUB_USERNAME="leo-elo"
REPO_NAME="leonardoflores.net"

echo "=========================================="
echo "GitHub Pages Deployment Script"
echo "=========================================="
echo ""

# Check if username is set
if [ "$GITHUB_USERNAME" = "YOUR_GITHUB_USERNAME" ]; then
    echo "⚠️  Please edit this file and replace YOUR_GITHUB_USERNAME with your actual GitHub username"
    echo ""
    echo "Edit the file: deploy.sh"
    echo "Line 5: GITHUB_USERNAME=\"YOUR_GITHUB_USERNAME\""
    echo ""
    exit 1
fi

echo "GitHub Username: $GITHUB_USERNAME"
echo "Repository Name: $REPO_NAME"
echo ""

# Step 1: Create repository on GitHub
echo "📋 Step 1: Create GitHub Repository"
echo "Please go to: https://github.com/new"
echo "  - Repository name: $REPO_NAME"
echo "  - Make it Public"
echo "  - Do NOT initialize with README, .gitignore, or license"
echo "  - Click 'Create repository'"
echo ""
read -p "Press Enter after you've created the repository..."

# Step 2: Add remote
echo ""
echo "🔗 Step 2: Adding GitHub remote..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git" 2>/dev/null || {
    echo "Remote already exists, updating URL..."
    git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
}

# Step 3: Push main branch
echo ""
echo "📤 Step 3: Pushing main branch..."
git push -u origin main

# Step 4: Push gh-pages branch
echo ""
echo "📤 Step 4: Pushing gh-pages branch..."
git push -u origin gh-pages

# Step 5: Instructions for enabling GitHub Pages
echo ""
echo "=========================================="
echo "✅ Code pushed successfully!"
echo "=========================================="
echo ""
echo "📋 Final Step: Enable GitHub Pages"
echo ""
echo "1. Go to: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/pages"
echo "2. Under 'Source':"
echo "   - Branch: Select 'gh-pages'"
echo "   - Folder: Select '/ (root)'"
echo "3. Click 'Save'"
echo ""
echo "🌐 Your site will be live at:"
echo "   https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
echo ""
echo "⏱️  It takes 1-2 minutes to deploy."
echo ""
echo "=========================================="
echo "🎉 Deployment Complete!"
echo "=========================================="
