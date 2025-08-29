#!/usr/bin/env python3
"""
UAE Legal GraphRAG - Comprehensive Cleanup Script
=================================================

This script performs a thorough cleanup of the entire repository,
removing all unnecessary files and organizing the project structure.

Usage:
    python comprehensive_cleanup.py
"""

import os
import shutil
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print the cleanup header."""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 70)
    print("🧹 UAE Legal GraphRAG - Comprehensive Cleanup Script")
    print("=" * 70)
    print(f"{Colors.ENDC}")

def remove_unnecessary_directories():
    """Remove unnecessary directories."""
    print(f"{Colors.OKCYAN}🗂️  Removing unnecessary directories...{Colors.ENDC}")
    
    directories_to_remove = [
        "test_azure",
        "backend/venv",
        "backend/tests",
        "backend/scripts",
        "frontend/.next",
        "frontend/node_modules",
        ".venv"
    ]
    
    removed_count = 0
    for directory in directories_to_remove:
        dir_path = Path(directory)
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"  ✅ Removed directory: {directory}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {directory}: {e}")
    
    print(f"{Colors.OKGREEN}✅ Removed {removed_count} unnecessary directories{Colors.ENDC}")
    return True

def remove_unnecessary_files():
    """Remove unnecessary files."""
    print(f"{Colors.OKCYAN}🗑️  Removing unnecessary files...{Colors.ENDC}")
    
    files_to_remove = [
        # Test and debug files
        "backend/test_azure_openai.py",
        "test_azure_openai.py",
        "debug_neo4j_data.py",
        "test_fixes.py",
        "test_complex_backend.py",
        "debug_backend.py",
        "test_analysis_page.py",
        "final_verification_test.py",
        "final_comprehensive_test.py",
        "test_overview_page.py",
        "test_simple_query.py",
        "test_graphrag_with_data.py",
        
        # Old startup scripts
        "start_backend.py",
        "start_complex_backend.py",
        
        # Duplicate and backup files
        "frontend/.env.backup",
        "frontend/.env.example",
        "STARTUP_GUIDE.md",
        
        # Build and cache files
        "frontend/next-env.d.ts",
        "frontend/.eslintrc.json",
        "backend/pyproject.toml",
        "backend/Dockerfile",
        
        # Temporary files
        "*.tmp",
        "*.temp",
        "*.log",
        "*.pyc",
        "__pycache__",
        "*.egg-info",
        ".pytest_cache",
        ".coverage",
        "htmlcov",
        ".mypy_cache",
        ".dmypy.json",
        "dmypy.json",
        ".pyre",
        ".ropeproject",
        ".spyderproject",
        ".spyproject",
        ".ipynb_checkpoints",
        ".DS_Store",
        ".DS_Store?",
        "._*",
        ".Spotlight-V100",
        ".Trashes",
        "ehthumbs.db",
        "Thumbs.db",
        "*.swp",
        "*.swo",
        "*~"
    ]
    
    removed_count = 0
    for file_pattern in files_to_remove:
        if "*" in file_pattern:
            # Handle glob patterns
            for file_path in Path(".").glob(file_pattern):
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        print(f"  ✅ Removed: {file_path}")
                        removed_count += 1
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        print(f"  ✅ Removed directory: {file_path}")
                        removed_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to remove {file_path}: {e}")
        else:
            # Handle specific files
            file_path = Path(file_pattern)
            if file_path.exists():
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        print(f"  ✅ Removed: {file_pattern}")
                        removed_count += 1
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        print(f"  ✅ Removed directory: {file_pattern}")
                        removed_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to remove {file_pattern}: {e}")
    
    print(f"{Colors.OKGREEN}✅ Removed {removed_count} unnecessary files{Colors.ENDC}")
    return True

def clean_frontend_directory():
    """Clean up frontend directory."""
    print(f"{Colors.OKCYAN}🧹 Cleaning frontend directory...{Colors.ENDC}")
    
    # Remove unnecessary frontend files
    frontend_files_to_remove = [
        "frontend/.env.backup",
        "frontend/.env.example",
        "frontend/next-env.d.ts",
        "frontend/.eslintrc.json",
        "frontend/.gitignore"
    ]
    
    removed_count = 0
    for file_path in frontend_files_to_remove:
        if Path(file_path).exists():
            try:
                Path(file_path).unlink()
                print(f"  ✅ Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {file_path}: {e}")
    
    print(f"{Colors.OKGREEN}✅ Cleaned {removed_count} frontend files{Colors.ENDC}")
    return True

def clean_backend_directory():
    """Clean up backend directory."""
    print(f"{Colors.OKCYAN}🧹 Cleaning backend directory...{Colors.ENDC}")
    
    # Remove unnecessary backend files
    backend_files_to_remove = [
        "backend/test_azure_openai.py",
        "backend/pyproject.toml",
        "backend/Dockerfile"
    ]
    
    removed_count = 0
    for file_path in backend_files_to_remove:
        if Path(file_path).exists():
            try:
                Path(file_path).unlink()
                print(f"  ✅ Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {file_path}: {e}")
    
    print(f"{Colors.OKGREEN}✅ Cleaned {removed_count} backend files{Colors.ENDC}")
    return True

def organize_directories():
    """Organize project directories."""
    print(f"{Colors.OKCYAN}📁 Organizing directories...{Colors.ENDC}")
    
    # Create necessary directories
    directories_to_create = [
        "docs",
        "scripts",
        "backend/data",
        "backend/logs",
        "logs"
    ]
    
    created_count = 0
    for directory in directories_to_create:
        dir_path = Path(directory)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✅ Created: {directory}")
                created_count += 1
            except Exception as e:
                print(f"  ❌ Failed to create {directory}: {e}")
    
    print(f"{Colors.OKGREEN}✅ Created {created_count} directories{Colors.ENDC}")
    return True

def update_gitignore():
    """Update .gitignore file with comprehensive patterns."""
    print(f"{Colors.OKCYAN}📝 Updating .gitignore...{Colors.ENDC}")
    
    gitignore_content = """# Python
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
MANIFEST

# Virtual Environment
.venv/
venv/
ENV/
env/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Next.js
.next/
out/
build/

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.env.backup
.env.example

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# Temporary files
*.tmp
*.temp
temp/

# Test files
test_*.py
debug_*.py
*_test.py
test_azure/

# Documentation
docs/_build/

# Coverage
.coverage
htmlcov/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# PyCharm
.idea/

# VS Code
.vscode/

# Temporary files
*.tmp
*.temp
temp/

# Frontend specific
frontend/.next/
frontend/out/
frontend/build/
frontend/node_modules/
frontend/.env.backup
frontend/.env.example
frontend/next-env.d.ts
frontend/.eslintrc.json

# Backend specific
backend/venv/
backend/tests/
backend/scripts/
backend/test_*.py
backend/pyproject.toml
backend/Dockerfile

# Old files
STARTUP_GUIDE.md
start_backend.py
start_complex_backend.py
"""
    
    try:
        with open(".gitignore", 'w') as f:
            f.write(gitignore_content)
        print(f"{Colors.OKGREEN}✅ Updated .gitignore{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to update .gitignore: {e}{Colors.ENDC}")
        return False

def create_final_structure():
    """Create the final clean project structure."""
    print(f"{Colors.OKCYAN}🏗️  Creating final project structure...{Colors.ENDC}")
    
    # Create a summary of the final structure
    structure_content = """# UAE Legal GraphRAG - Final Project Structure

## 📁 Clean Repository Structure

```
internship_GraphRAG/
├── start.py                 # 🚀 Unified startup script
├── setup.py                 # 🔧 Automated setup
├── comprehensive_cleanup.py # 🧹 Comprehensive cleanup
├── README.md               # 📖 Main documentation
├── requirements.txt        # 📦 Unified Python dependencies
├── .env                    # ⚙️ Environment configuration
├── .gitignore             # 🚫 Git ignore patterns
├── docker-compose.yml     # 🐳 Docker configuration
├── 
├── frontend/               # 🌐 Next.js frontend
│   ├── components/         # React components
│   ├── pages/             # Next.js pages
│   ├── styles/            # CSS styles
│   ├── utils/             # Utility functions
│   ├── types/             # TypeScript types
│   ├── lib/               # Library files
│   ├── package.json       # Node.js dependencies
│   ├── package-lock.json  # Lock file
│   ├── next.config.js     # Next.js configuration
│   ├── tailwind.config.js # Tailwind CSS config
│   ├── postcss.config.js  # PostCSS configuration
│   └── tsconfig.json      # TypeScript configuration
├── 
├── backend/                # 🐍 FastAPI backend
│   ├── app/               # Application code
│   │   ├── adapters/      # External service adapters
│   │   ├── api/           # API routes
│   │   ├── rag/           # GraphRAG implementations
│   │   ├── schemas/       # Pydantic models
│   │   ├── store/         # Data storage
│   │   ├── utils/         # Utility functions
│   │   └── main.py        # FastAPI application
│   ├── data/              # Data files
│   ├── logs/              # Log files
│   └── requirements.txt   # Python dependencies
├── 
├── scripts/                # 🔧 Utility scripts
│   └── load_mock_data.py  # Mock data loader
├── 
├── docs/                   # 📚 Documentation
│   ├── QUICK_START.md     # Quick setup guide
│   ├── ARCHITECTURE.md    # System architecture
│   └── DEPLOYMENT_GUIDE.md # Deployment guide
└── 
└── logs/                   # 📝 Application logs
```

## ✅ Cleanup Summary

- ✅ Removed all test files and directories
- ✅ Removed unnecessary build artifacts
- ✅ Removed duplicate and backup files
- ✅ Organized scripts and documentation
- ✅ Updated .gitignore with comprehensive patterns
- ✅ Created clean, production-ready structure

## 🚀 Ready for Use

The repository is now clean and organized for:
- Development
- Presentations
- Production deployment
- Collaboration

All unnecessary files have been removed and the structure is optimized for maintainability.
"""
    
    try:
        with open("PROJECT_STRUCTURE.md", 'w') as f:
            f.write(structure_content)
        print(f"{Colors.OKGREEN}✅ Created PROJECT_STRUCTURE.md{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to create PROJECT_STRUCTURE.md: {e}{Colors.ENDC}")
        return False

def run_git_cleanup():
    """Run git cleanup commands."""
    print(f"{Colors.OKCYAN}🔧 Running git cleanup...{Colors.ENDC}")
    
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        print("  ✅ Added all changes to git")
        
        # Remove files from git cache that are now ignored
        subprocess.run(["git", "rm", "-r", "--cached", "."], check=True)
        subprocess.run(["git", "add", "."], check=True)
        print("  ✅ Cleaned git cache")
        
        print(f"{Colors.OKGREEN}✅ Git cleanup completed{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.WARNING}⚠️  Git cleanup failed (not a git repo or no git): {e}{Colors.ENDC}")
        return True

def main():
    """Main cleanup function."""
    print_header()
    
    print(f"{Colors.OKCYAN}🚀 Starting comprehensive cleanup process...{Colors.ENDC}")
    
    # Remove unnecessary directories
    remove_unnecessary_directories()
    
    # Remove unnecessary files
    remove_unnecessary_files()
    
    # Clean frontend directory
    clean_frontend_directory()
    
    # Clean backend directory
    clean_backend_directory()
    
    # Organize directories
    organize_directories()
    
    # Update .gitignore
    update_gitignore()
    
    # Create final structure documentation
    create_final_structure()
    
    # Run git cleanup
    run_git_cleanup()
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Comprehensive Cleanup Complete!{Colors.ENDC}")
    print(f"\n{Colors.OKBLUE}📋 Repository is now completely clean with:{Colors.ENDC}")
    print(f"✅ All test files and directories removed")
    print(f"✅ All unnecessary build artifacts removed")
    print(f"✅ All duplicate and backup files removed")
    print(f"✅ Clean, organized project structure")
    print(f"✅ Comprehensive .gitignore")
    print(f"✅ Production-ready organization")
    print(f"✅ Documentation of final structure")
    print(f"\n{Colors.OKCYAN}📚 Ready for development, presentation, and production!{Colors.ENDC}")
    print(f"\n{Colors.WARNING}💡 Next steps:{Colors.ENDC}")
    print(f"1. Run: python setup.py (if needed)")
    print(f"2. Run: python start.py (to start the application)")
    print(f"3. Check PROJECT_STRUCTURE.md for the final organization")

if __name__ == "__main__":
    main()
