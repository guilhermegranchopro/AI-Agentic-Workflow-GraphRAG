#!/usr/bin/env python3
"""
UAE Legal GraphRAG - Cleanup Script
===================================

This script cleans up temporary files and organizes the repository.
It removes test files, temporary scripts, and organizes the project structure.

Usage:
    python cleanup.py
"""

import os
import shutil
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
    print("=" * 60)
    print("🧹 UAE Legal GraphRAG - Cleanup Script")
    print("=" * 60)
    print(f"{Colors.ENDC}")

def cleanup_test_files():
    """Remove temporary test files."""
    print(f"{Colors.OKCYAN}🧹 Cleaning up test files...{Colors.ENDC}")
    
    test_files = [
        "test_graphrag_with_data.py",
        "debug_neo4j_data.py",
        "test_fixes.py",
        "test_complex_backend.py",
        "debug_backend.py",
        "test_analysis_page.py",
        "final_verification_test.py",
        "final_comprehensive_test.py",
        "test_overview_page.py",
        "test_simple_query.py"
    ]
    
    removed_count = 0
    for file_path in test_files:
        if Path(file_path).exists():
            try:
                Path(file_path).unlink()
                print(f"  ✅ Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {file_path}: {e}")
    
    print(f"{Colors.OKGREEN}✅ Cleaned up {removed_count} test files{Colors.ENDC}")
    return True

def cleanup_old_scripts():
    """Remove old startup scripts."""
    print(f"{Colors.OKCYAN}🧹 Cleaning up old scripts...{Colors.ENDC}")
    
    old_scripts = [
        "start_backend.py",
        "start_complex_backend.py"
    ]
    
    removed_count = 0
    for script_path in old_scripts:
        if Path(script_path).exists():
            try:
                Path(script_path).unlink()
                print(f"  ✅ Removed: {script_path}")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Failed to remove {script_path}: {e}")
    
    print(f"{Colors.OKGREEN}✅ Cleaned up {removed_count} old scripts{Colors.ENDC}")
    return True

def organize_directories():
    """Organize project directories."""
    print(f"{Colors.OKCYAN}📁 Organizing directories...{Colors.ENDC}")
    
    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Create scripts directory if it doesn't exist
    scripts_dir = Path("scripts")
    scripts_dir.mkdir(exist_ok=True)
    
    # Move utility scripts to scripts directory
    utility_scripts = [
        "load_mock_data.py"
    ]
    
    moved_count = 0
    for script in utility_scripts:
        if Path(script).exists():
            try:
                shutil.move(script, scripts_dir / script)
                print(f"  ✅ Moved: {script} -> scripts/{script}")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Failed to move {script}: {e}")
    
    print(f"{Colors.OKGREEN}✅ Organized {moved_count} scripts{Colors.ENDC}")
    return True

def update_gitignore():
    """Update .gitignore file."""
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
"""
    
    try:
        with open(".gitignore", 'w') as f:
            f.write(gitignore_content)
        print(f"{Colors.OKGREEN}✅ Updated .gitignore{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to update .gitignore: {e}{Colors.ENDC}")
        return False

def create_requirements_txt():
    """Create a unified requirements.txt file."""
    print(f"{Colors.OKCYAN}📦 Creating unified requirements.txt...{Colors.ENDC}")
    
    try:
        # Read backend requirements
        backend_req = Path("backend/requirements.txt")
        if backend_req.exists():
            with open(backend_req, 'r') as f:
                backend_deps = f.read()
            
            # Create unified requirements
            unified_content = f"""# UAE Legal GraphRAG - Unified Requirements
# This file contains all Python dependencies for the project

{backend_deps}

# Additional development dependencies
pytest>=7.0.0
pytest-asyncio>=0.21.0
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
"""
            
            with open("requirements.txt", 'w') as f:
                f.write(unified_content)
            
            print(f"{Colors.OKGREEN}✅ Created unified requirements.txt{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.WARNING}⚠️  Backend requirements.txt not found{Colors.ENDC}")
            return False
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to create requirements.txt: {e}{Colors.ENDC}")
        return False

def main():
    """Main cleanup function."""
    print_header()
    
    print(f"{Colors.OKCYAN}🚀 Starting cleanup process...{Colors.ENDC}")
    
    # Clean up test files
    cleanup_test_files()
    
    # Clean up old scripts
    cleanup_old_scripts()
    
    # Organize directories
    organize_directories()
    
    # Update .gitignore
    update_gitignore()
    
    # Create unified requirements
    create_requirements_txt()
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Cleanup Complete!{Colors.ENDC}")
    print(f"\n{Colors.OKBLUE}📋 Repository is now organized with:{Colors.ENDC}")
    print(f"✅ Clean project structure")
    print(f"✅ Organized scripts in scripts/ directory")
    print(f"✅ Updated .gitignore")
    print(f"✅ Unified requirements.txt")
    print(f"✅ Removed temporary test files")
    print(f"\n{Colors.OKCYAN}📚 Ready for development!{Colors.ENDC}")

if __name__ == "__main__":
    main()
