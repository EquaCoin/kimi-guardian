#!/bin/bash
# 📤 Upload Kimi Guardian to GitHub
# Usage: ./upload-to-github.sh

set -e

REPO_URL="https://github.com/equacoin/kimi-guardian"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     📤 Kimi Guardian - GitHub Upload Helper              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if in right directory
if [ ! -f "setup.py" ]; then
    echo -e "${RED}❌ Error: Not in kimi-guardian directory${NC}"
    echo "Please run from: ~/zed-plus-kimi/kimi-guardian"
    exit 1
fi

echo "📋 Pre-upload checklist:"
echo ""

# Check files exist
echo -n "  README.md... "
if [ -f "README.md" ]; then echo -e "${GREEN}✅${NC}"; else echo -e "${RED}❌${NC}"; fi

echo -n "  LICENSE... "
if [ -f "LICENSE" ]; then echo -e "${GREEN}✅${NC}"; else echo -e "${RED}❌${NC}"; fi

echo -n "  .gitignore... "
if [ -f ".gitignore" ]; then echo -e "${GREEN}✅${NC}"; else echo -e "${RED}❌${NC}"; fi

echo -n "  guardian/... "
if [ -d "guardian" ]; then echo -e "${GREEN}✅${NC}"; else echo -e "${RED}❌${NC}"; fi

echo -n "  rules/... "
if [ -d "rules" ]; then echo -e "${GREEN}✅${NC}"; else echo -e "${RED}❌${NC}"; fi

echo ""

# Ask confirmation
echo -e "${YELLOW}This will upload Kimi Guardian to:${NC}"
echo "  $REPO_URL"
echo ""
read -p "Continue? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "🚀 Starting upload process..."
echo ""

# Copy GitHub README
echo "📄 Copying GitHub README..."
cp README_GITHUB.md README.md

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
fi

# Add all files
echo "📦 Adding files to git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
else
    # Commit
    echo "💾 Creating commit..."
    git commit -m "Initial release: Kimi Guardian v1.3

Features:
- 38 threat detection rules (filesystem, network, execution, git, secrets)
- MCP Plugin for Kimi CLI integration
- Pre-commit hooks for Git security
- 100% offline operation
- Sage-compatible YAML rule format
- CLI wrapper and interactive mode

See README.md for documentation."
fi

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "🔗 Remote 'origin' already exists"
else
    echo "🔗 Adding remote origin..."
    git remote add origin "$REPO_URL"
fi

# Rename branch to main
git branch -M main 2>/dev/null || true

echo ""
echo "📤 Ready to push!"
echo ""
echo "Next steps:"
echo "  1. Create repository on GitHub:"
echo "     https://github.com/new"
echo ""
echo "  2. Use these settings:"
echo "     - Repository name: kimi-guardian"
echo "     - Public: ✅"
echo "     - Initialize: ❌ (we already have files)"
echo ""
echo "  3. Then run:"
echo "     git push -u origin main"
echo ""
echo "  4. Create release at:"
echo "     $REPO_URL/releases"
echo ""

# Ask if they want to push now
read -p "Push now? (y/n): " push_now

if [ "$push_now" = "y" ]; then
    echo "📤 Pushing to GitHub..."
    if git push -u origin main; then
        echo ""
        echo -e "${GREEN}✅ Successfully uploaded to GitHub!${NC}"
        echo ""
        echo "🔗 Repository: $REPO_URL"
        echo ""
        echo "Next: Create a release at:"
        echo "  $REPO_URL/releases/new"
    else
        echo ""
        echo -e "${RED}❌ Push failed${NC}"
        echo "Make sure:"
        echo "  1. Repository exists on GitHub"
        echo "  2. You're logged in: git config --global user.name 'Your Name'"
        echo "  3. Check credentials"
    fi
else
    echo ""
    echo "To push later, run:"
    echo "  git push -u origin main"
fi

echo ""
echo "📚 See GITHUB_UPLOAD.md for detailed instructions"
