#!/bin/bash

# Setup script for initializing and pushing to GitHub repository

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up ReasonPy repository...${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git is not installed. Please install Git first.${NC}"
    exit 1
fi

# Check if already in a git repository
if git rev-parse --is-inside-work-tree &> /dev/null; then
    echo -e "${YELLOW}Already in a Git repository. Skipping initialization.${NC}"
else
    echo -e "${GREEN}Initializing Git repository...${NC}"
    git init
fi

# Create artifacts directory if it doesn't exist
echo -e "${GREEN}Creating artifacts directory...${NC}"
mkdir -p ./src/agent/artifacts

# Add .gitkeep to artifacts directory to track it in git
touch ./src/agent/artifacts/.gitkeep

# Create .gitignore
echo -e "${GREEN}Creating .gitignore file...${NC}"
cat > .gitignore << EOL
# Python
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
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env

# Virtual Environment
venv/
ENV/
env/

# IDE files
.idea/
.vscode/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Generated files
/src/agent/artifacts/*
!/src/agent/artifacts/.gitkeep
EOL

# Add remote repository if not already added
if ! git remote | grep -q origin; then
    echo -e "${GREEN}Adding remote repository...${NC}"
    git remote add origin https://github.com/naoufal51/ReasonPy.git
else
    echo -e "${YELLOW}Remote 'origin' already exists. Skipping...${NC}"
fi

# Stage files
echo -e "${GREEN}Staging files...${NC}"
git add .

# Commit
echo -e "${GREEN}Creating initial commit...${NC}"
git commit -m "Initial commit of ReasonPy"

# Push to GitHub
echo -e "${GREEN}Pushing to GitHub...${NC}"
echo -e "${YELLOW}Note: You may be prompted for your GitHub credentials.${NC}"
git push -u origin master || git push -u origin main

echo -e "${GREEN}Setup complete! Your code has been pushed to GitHub.${NC}"
echo -e "${GREEN}Repository URL: https://github.com/naoufal51/ReasonPy${NC}" 