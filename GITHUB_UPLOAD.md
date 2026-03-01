# 📤 GitHub Upload Guide

> How to upload Kimi Guardian to your GitHub account (@equacoin)

---

## 🎯 Quick Steps

### 1. Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `kimi-guardian`
3. Description: `AI Agent Security Scanner for Kimi CLI - Inspired by Sage`
4. Make it **Public** ✅
5. Add README (we'll replace it)
6. Add .gitignore: Python
7. Add License: MIT
8. Click **Create repository**

---

### 2. Prepare Local Repository

```bash
# Navigate to the project
cd ~/zed-plus-kimi/kimi_guardian

# Use the GitHub README
cp README_GITHUB.md README.md

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Kimi Guardian v1.3

Features:
- 38 YAML threat detection rules (Sage-compatible)
- MCP Plugin for Kimi CLI integration
- Pre-commit hooks for Git
- 100% offline operation
- CLI wrapper"
```

---

### 3. Connect to GitHub

```bash
# Add remote (replace with your repo URL)
git remote add origin https://github.com/equacoin/kimi-guardian.git

# Push to main branch
git branch -M main
git push -u origin main
```

---

### 4. Verify Upload

1. Go to https://github.com/equacoin/kimi-guardian
2. Check that all files are uploaded:
   - ✅ guardian/ (Python files)
   - ✅ rules/ (YAML rules)
   - ✅ README.md
   - ✅ LICENSE
   - ✅ .gitignore
   - ✅ setup.py
   - ✅ kg (executable)

---

## 🏷️ Create Release

### Tag Version 1.3

```bash
# Create annotated tag
git tag -a v1.3.0 -m "Kimi Guardian v1.3.0

- 38 threat detection rules
- MCP Plugin support
- Pre-commit hooks
- Sage-compatible YAML format"

# Push tag
git push origin v1.3.0
```

### Create Release on GitHub

1. Go to https://github.com/equacoin/kimi-guardian/releases
2. Click **Draft a new release**
3. Choose tag: `v1.3.0`
4. Release title: `Kimi Guardian v1.3`
5. Description:
   ```markdown
   ## 🎉 Kimi Guardian v1.3
   
   First stable release with full feature set.
   
   ### ✨ Features
   - **38 threat detection rules** across 5 categories
   - **MCP Plugin** for Kimi CLI integration
   - **Pre-commit hooks** for Git security
   - **100% offline** - no cloud dependency
   - **Sage-compatible** YAML rule format
   
   ### 📦 Installation
   ```bash
   git clone https://github.com/equacoin/kimi-guardian.git
   cd kimi-guardian
   pip install rich pyyaml
   chmod +x kg
   ./kg --help
   ```
   
   ### 📚 Documentation
   - See [README.md](README.md) for full docs
   - [QUICKSTART.md](QUICKSTART.md) for quick start
   
   ### 🤝 Sage Collaboration
   See [SAGE_PROPOSAL.md](SAGE_PROPOSAL.md) for collaboration proposal.
   ```
6. Click **Publish release**

---

## 🔗 Important URLs

After upload, you'll have:

| URL | Purpose |
|-----|---------|
| `https://github.com/equacoin/kimi-guardian` | Main repository |
| `https://github.com/equacoin/kimi-guardian/releases` | Releases |
| `https://github.com/equacoin/kimi-guardian/issues` | Issue tracker |

Update these in your docs:
- `README.md` - Update clone URL
- `SAGE_EMAIL.md` - Update repository link
- `setup.py` - Update URL field

---

## 📋 Pre-Upload Checklist

- [ ] GitHub account: @equacoin
- [ ] Repository name: kimi-guardian
- [ ] README_GITHUB.md copied to README.md
- [ ] LICENSE file present (MIT)
- [ ] .gitignore present
- [ ] All Python files committed
- [ ] All YAML rules committed
- [ ] No secrets in code
- [ ] setup.py has correct URLs

---

## 🔒 Security Check

Before uploading, verify no secrets:

```bash
# Search for potential secrets
grep -r "api_key\|password\|secret" --include="*.py" --include="*.yml" .
# Should only find example/test data

# Check no personal paths
grep -r "/home/" --include="*.py" --include="*.md" .
# Replace with generic paths
```

---

## 🚀 After Upload

### Share the project

```markdown
🛡️ Just released Kimi Guardian!

AI Agent Security Scanner for Kimi CLI

✅ 38 threat detection rules
✅ MCP Plugin support  
✅ Pre-commit hooks
✅ 100% offline
✅ Sage-compatible

🔗 https://github.com/equacoin/kimi-guardian

#AI #Security #Kimi #OpenSource
```

### Submit to

- [ ] Hacker News (Show HN)
- [ ] Reddit r/programming, r/python
- [ ] Twitter/X
- [ ] LinkedIn

---

## 📧 For Sage Collaboration

Once uploaded, send email:

```
To: sage-team@avast.com
Subject: Collaboration Proposal: Kimi Guardian + Sage

See: https://github.com/equacoin/kimi-guardian/SAGE_PROPOSAL.md

Best regards,
[Your name]
```

---

## 🎉 Success!

Your project is now on GitHub and ready for the world! 🚀
