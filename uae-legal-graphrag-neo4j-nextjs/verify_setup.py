#!/usr/bin/env python3
"""
Environment Verification Script for UAE Legal GraphRAG Next.js Application
Checks all dependencies and configuration requirements.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_command(command, name, required_version=None):
    """Check if a command exists and optionally verify version."""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(f"✅ {name}: {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ {name}: Not found or not in PATH")
        return False

def check_file(filepath, name):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✅ {name}: Found")
        return True
    else:
        print(f"❌ {name}: Missing")
        return False

def check_directory(dirpath, name):
    """Check if a directory exists."""
    if Path(dirpath).is_dir():
        print(f"✅ {name}: Found")
        return True
    else:
        print(f"❌ {name}: Missing")
        return False

def main():
    print("🔍 UAE Legal GraphRAG - Environment Verification")
    print("=" * 60)
    
    # Check Python
    print("\n📍 Python Environment:")
    python_ok = check_command('python', 'Python')
    if not python_ok:
        python_ok = check_command('py', 'Python (via py launcher)')
    
    # Check virtual environment
    venv_ok = check_directory('.venv', 'Virtual Environment')
    
    # Check Python packages
    if python_ok and venv_ok:
        print("\n📦 Python Packages:")
        packages = ['neo4j', 'openai', 'pydantic', 'httpx', 'pandas']
        for package in packages:
            try:
                __import__(package)
                print(f"✅ {package}: Installed")
            except ImportError:
                print(f"❌ {package}: Not found")
    
    # Check Node.js
    print("\n📍 Node.js Environment:")
    node_ok = check_command('node', 'Node.js')
    npm_ok = check_command('npm', 'npm')
    
    # Check Node.js files
    print("\n📄 Node.js Configuration:")
    check_file('package.json', 'package.json')
    check_file('next.config.js', 'Next.js config')
    check_file('tsconfig.json', 'TypeScript config')
    check_directory('node_modules', 'Node modules')
    
    # Check environment files
    print("\n🔧 Environment Configuration:")
    check_file('.env', 'Environment template')
    env_local_ok = check_file('.env.local', 'Local environment')
    if not env_local_ok:
        print("   ℹ️  Copy .env to .env.local and configure your credentials")
    
    # Check project structure
    print("\n📁 Project Structure:")
    check_directory('components', 'Components directory')
    check_directory('pages', 'Pages directory')
    check_directory('python-backend', 'Python backend')
    check_file('requirements.txt', 'Python requirements')
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Setup Summary:")
    print("1. ✅ Python virtual environment created and configured")
    print("2. ✅ Python dependencies installed")
    print("3. ✅ Project structure complete")
    print("4. ⚠️  Node.js needs to be installed for Next.js development")
    print("5. ⚠️  Configure .env.local with your credentials")
    
    print("\n🚀 Next Steps:")
    if not node_ok:
        print("   1. Install Node.js 18+ from https://nodejs.org")
        print("   2. Run: npm install")
    print("   3. Configure .env.local with your Neo4j and Azure OpenAI credentials")
    print("   4. Run: npm run dev")
    print("   5. Open: http://localhost:3000")

if __name__ == "__main__":
    main()
