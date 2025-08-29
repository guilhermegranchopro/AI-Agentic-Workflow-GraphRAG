#!/usr/bin/env python3
"""
Comprehensive Repository Cleanup Script
Removes unnecessary files and organizes the repository structure.
"""

import os
import shutil
import sys
from pathlib import Path

def cleanup_repository():
    """Clean up the repository by removing unnecessary files and directories."""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    print("🧹 Starting comprehensive repository cleanup...")
    
    # Files and directories to remove
    cleanup_items = [
        # Python cache files
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        
        # Log files
        "**/*.log",
        "**/logs",
        
        # Temporary files
        "**/*.tmp",
        "**/*.temp",
        "**/.DS_Store",
        "**/Thumbs.db",
        
        # Build artifacts
        "**/dist",
        "**/build",
        "**/.pytest_cache",
        "**/.coverage",
        "**/.mypy_cache",
        "**/.ruff_cache",
        
        # Node.js artifacts (keep node_modules for now as it's needed)
        "frontend/.next",
        "frontend/out",
        
        # IDE files
        "**/.vscode",
        "**/.idea",
        "**/*.swp",
        "**/*.swo",
        
        # OS files
        "**/.DS_Store",
        "**/Thumbs.db",
        "**/desktop.ini",
    ]
    
    removed_count = 0
    
    for pattern in cleanup_items:
        for item_path in project_root.glob(pattern):
            if item_path.is_file():
                try:
                    item_path.unlink()
                    print(f"🗑️  Removed file: {item_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️  Could not remove file {item_path}: {e}")
            elif item_path.is_dir():
                try:
                    shutil.rmtree(item_path)
                    print(f"🗑️  Removed directory: {item_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️  Could not remove directory {item_path}: {e}")
    
    # Clean up empty directories
    for root, dirs, files in os.walk(project_root, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"🗑️  Removed empty directory: {dir_path}")
                    removed_count += 1
            except Exception as e:
                print(f"⚠️  Could not remove empty directory {dir_path}: {e}")
    
    print(f"\n✅ Cleanup completed! Removed {removed_count} items.")
    
    # Verify essential files and directories exist
    essential_items = [
        "backend/app/main.py",
        "backend/requirements.txt",
        "frontend/package.json",
        "frontend/pages",
        "frontend/components",
        ".env",
        "README.md",
        "setup.py",
        "start.py"
    ]
    
    print("\n🔍 Verifying essential files and directories...")
    missing_items = []
    
    for item in essential_items:
        item_path = project_root / item
        if not item_path.exists():
            missing_items.append(item)
        else:
            print(f"✅ Found: {item}")
    
    if missing_items:
        print(f"\n⚠️  Missing essential items: {missing_items}")
    else:
        print("\n✅ All essential files and directories are present!")
    
    return removed_count

def organize_structure():
    """Organize the repository structure for better clarity."""
    
    project_root = Path(__file__).parent
    
    print("\n📁 Organizing repository structure...")
    
    # Create necessary directories if they don't exist
    directories = [
        "backend/data",
        "backend/logs",
        "frontend/public",
        "docs",
        "scripts"
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {directory}")
    
    # Move scripts to scripts directory if they're in the root
    scripts_to_move = [
        "load_mock_data.py",
        "load_contradictory_data.py",
        "test_*.py",
        "check_*.py"
    ]
    
    scripts_dir = project_root / "scripts"
    
    for pattern in scripts_to_move:
        for script_file in project_root.glob(pattern):
            if script_file.is_file() and script_file.parent == project_root:
                try:
                    shutil.move(str(script_file), str(scripts_dir / script_file.name))
                    print(f"📦 Moved script: {script_file.name} -> scripts/")
                except Exception as e:
                    print(f"⚠️  Could not move {script_file.name}: {e}")
    
    print("✅ Repository structure organized!")

def main():
    """Main cleanup function."""
    try:
        removed_count = cleanup_repository()
        organize_structure()
        
        print(f"\n🎉 Repository cleanup completed successfully!")
        print(f"📊 Total items removed: {removed_count}")
        print("\n📋 Next steps:")
        print("1. Run 'python setup.py' to verify the setup")
        print("2. Run 'python start.py' to start the application")
        print("3. Test the backend and frontend communication")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
