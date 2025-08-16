# GitHub Setup Guide

This guide will help you set up your Google Product Categories project on GitHub with CI/CD.

## 🚀 **Step 1: Initialize Git Repository (if not already done)**

```bash
# Check if git is already initialized
git status

# If not initialized, run:
git init
```

## 🔗 **Step 2: Add Remote Origin**

```bash
# Replace YOUR_USERNAME and REPO_NAME with your actual GitHub details
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Or using SSH (if you have SSH keys set up):
git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git

# Verify remote
git remote -v
```

## 📝 **Step 3: Create Initial Commit**

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Google Product Categories setup script with nested set model

- Downloads Google Product Taxonomy
- Implements nested set model (left, right, depth)
- Generates JSON, SQL, and SQLite outputs
- Cross-platform setup scripts (Windows, macOS, Linux)
- Comprehensive CI workflow with GitHub Actions"

# Push to main branch
git branch -M main
git push -u origin main
```

## 🏗️ **Step 4: GitHub Repository Setup**

1. **Go to GitHub.com** and create a new repository
2. **Repository name**: `google-product-categories` (or your preferred name)
3. **Description**: `Download and process Google Product Taxonomy into nested set model format`
4. **Visibility**: Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)

## ⚙️ **Step 5: Configure Repository Settings**

### **Branches Protection (Recommended)**
1. Go to **Settings** → **Branches**
2. Add rule for `main` branch:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging

### **GitHub Actions**
1. Go to **Actions** tab
2. The CI workflow will automatically run on your first push
3. Monitor the workflow execution

## 🔄 **Step 6: Development Workflow**

### **For New Features:**
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Add new feature: description"

# Push feature branch
git push origin feature/new-feature

# Create Pull Request on GitHub
```

### **For Bug Fixes:**
```bash
# Create fix branch
git checkout -b fix/bug-description

# Fix the bug
# ... edit files ...

# Commit fix
git add .
git commit -m "Fix: description of the bug fix"

# Push fix branch
git push origin fix/bug-description

# Create Pull Request on GitHub
```

## 📊 **Step 7: Monitor CI/CD Pipeline**

### **GitHub Actions Dashboard:**
- **Actions** tab shows all workflow runs
- **Green checkmark** = All tests passed
- **Red X** = Tests failed (check logs for details)

### **CI Jobs:**
1. **Test**: Runs on multiple Python versions and OS
2. **Validate Outputs**: Tests setup script functionality
3. **Security**: Runs security checks with bandit and safety
4. **Documentation**: Validates README and project structure

## 🐛 **Troubleshooting Common Issues**

### **Permission Denied:**
```bash
# If you get permission errors, check your remote URL
git remote -v

# Make sure you're using the correct authentication method
# HTTPS: Use your GitHub username and personal access token
# SSH: Make sure your SSH key is added to GitHub
```

### **CI Failures:**
1. Check the **Actions** tab for detailed error logs
2. Common issues:
   - Missing dependencies in `requirements.txt`
   - Syntax errors in Python code
   - Missing files referenced in CI workflow

### **Branch Protection Issues:**
```bash
# If you can't push to main due to protection rules
# Always create feature branches and use Pull Requests
git checkout -b feature/your-feature
git push origin feature/your-feature
```

## 📈 **Step 8: Repository Badges**

Add these badges to your README.md:

```markdown
[![CI](https://github.com/YOUR_USERNAME/REPO_NAME/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/REPO_NAME/actions)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
```

## 🎯 **Next Steps After Setup**

1. **Monitor CI runs** to ensure everything works
2. **Set up branch protection** for main branch
3. **Create issues** for future enhancements
4. **Set up project board** for task management
5. **Configure code review** requirements

## 🔐 **Security Best Practices**

- ✅ Never commit API keys or secrets
- ✅ Use environment variables for sensitive data
- ✅ Keep dependencies updated
- ✅ Review security scan results
- ✅ Use branch protection rules

---

**Need Help?** Check the GitHub Actions logs or create an issue in your repository!
