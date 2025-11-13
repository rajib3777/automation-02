#!/bin/bash

echo "🚀 RENDER DEPLOYMENT PREPARATION SCRIPT"
echo "======================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already exists"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore file..."
    cat > .gitignore << EOF
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

.DS_Store
.vscode/
.idea/

# Selenium
*.log
screenshot_*.png
geckodriver.log
chromedriver.log

# Application specific
uploads/
tmp/
.backups/
shell_output_save/
EOF
    echo "✅ .gitignore created"
else
    echo "✅ .gitignore already exists"
fi

# Check required files
echo ""
echo "🔍 Checking required files..."

if [ -f "ultra_powerful_app.py" ]; then
    echo "✅ ultra_powerful_app.py found"
else
    echo "❌ ultra_powerful_app.py not found!"
    exit 1
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

if [ -f "render.yaml" ]; then
    echo "✅ render.yaml found"
else
    echo "❌ render.yaml not found!"
    exit 1
fi

if [ -d "templates" ]; then
    echo "✅ templates directory found"
else
    echo "❌ templates directory not found!"
    exit 1
fi

# Add all files to git
echo ""
echo "📦 Adding files to git..."
git add .
echo "✅ Files added to git"

# Create initial commit
echo ""
echo "💾 Creating initial commit..."
git commit -m "Initial deployment setup for Render" || echo "⚠️  No changes to commit"

echo ""
echo "🎉 DEPLOYMENT PREPARATION COMPLETE!"
echo ""
echo "NEXT STEPS:"
echo "1. Create a GitHub repository"
echo "2. Add remote: git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "3. Push code: git push -u origin main"
echo "4. Deploy on Render using the GitHub repository"
echo "5. Set environment variable: SYSTEM_PASSWORD = F@padma2041"
echo ""
echo "📖 See RENDER_DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
