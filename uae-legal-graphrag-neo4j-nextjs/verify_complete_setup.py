#!/usr/bin/env python3
"""
UAE Legal GraphRAG - Complete Setup Verification
Checks both Python and Node.js environments are ready for development
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(cmd, shell=True):
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    exists = Path(filepath).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {'Found' if exists else 'Not found'}")
    return exists

def check_environment():
    """Comprehensive environment check"""
    print("🔍 UAE Legal GraphRAG - Complete Setup Verification")
    print("=" * 60)
    
    # Python Environment
    print("\n📍 Python Environment:")
    python_ok, python_version = run_command([sys.executable, "--version"])
    print(f"✅ Python: {python_version}" if python_ok else "❌ Python: Not available")
    
    # Check if in virtual environment
    venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"✅ Virtual Environment: Active" if venv_active else "⚠️  Virtual Environment: Not active")
    
    # Python packages
    print("\n📦 Python Packages:")
    packages = ['neo4j', 'openai', 'pydantic', 'httpx', 'pandas']
    python_deps_ok = True
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}: Installed")
        except ImportError:
            print(f"❌ {package}: Not installed")
            python_deps_ok = False
    
    # Node.js Environment
    print("\n📍 Node.js Environment:")
    node_ok, node_version = run_command("node --version")
    npm_ok, npm_version = run_command("npm --version")
    
    if node_ok and npm_ok:
        print(f"✅ Node.js: {node_version}")
        print(f"✅ npm: {npm_version}")
        
        # Check if node_modules exists
        node_modules_exists = check_file_exists("node_modules", "Node modules")
        
        # Try to get package info
        if Path("package.json").exists():
            try:
                with open("package.json", "r") as f:
                    package_data = json.load(f)
                    print(f"✅ Project: {package_data.get('name', 'Unknown')}")
                    print(f"✅ Next.js Version: {package_data.get('dependencies', {}).get('next', 'Not specified')}")
            except Exception:
                print("⚠️  package.json: Could not read")
    else:
        print("❌ Node.js: Not found or not in PATH")
        print("❌ npm: Not found or not in PATH")
    
    # Configuration Files
    print("\n🔧 Environment Configuration:")
    check_file_exists(".env", "Environment template")
    env_local_exists = check_file_exists(".env.local", "Local environment")
    
    if env_local_exists:
        # Verify key environment variables
        with open(".env.local", "r") as f:
            env_content = f.read()
            required_vars = [
                "NEO4J_URI", "NEO4J_PASSWORD", 
                "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY"
            ]
            for var in required_vars:
                if f"{var}=" in env_content and not f"{var}=your_" in env_content:
                    print(f"✅ {var}: Configured")
                else:
                    print(f"⚠️  {var}: Needs configuration")
    
    # Project Structure
    print("\n📁 Project Structure:")
    structure_items = [
        ("components", "Components directory"),
        ("pages", "Pages directory"),
        ("python-backend", "Python backend"),
        ("requirements.txt", "Python requirements"),
        ("package.json", "Node.js config"),
        ("next.config.js", "Next.js config"),
        ("tsconfig.json", "TypeScript config")
    ]
    
    for item, description in structure_items:
        check_file_exists(item, description)
    
    # Development Readiness Check
    print("\n" + "=" * 60)
    print("📋 Development Readiness:")
    
    ready_items = []
    if python_ok and python_deps_ok:
        ready_items.append("✅ Python environment ready")
    else:
        ready_items.append("❌ Python environment needs setup")
    
    if node_ok and npm_ok:
        if Path("node_modules").exists():
            ready_items.append("✅ Node.js environment ready")
        else:
            ready_items.append("⚠️  Node.js ready, run 'npm install'")
    else:
        ready_items.append("❌ Node.js needs installation")
    
    if env_local_exists:
        ready_items.append("✅ Environment configured")
    else:
        ready_items.append("❌ Environment needs configuration")
    
    for item in ready_items:
        print(f"   {item}")
    
    # Next Steps
    print(f"\n🚀 Next Steps:")
    if not node_ok:
        print("   1. Install Node.js 18+ from https://nodejs.org")
        print("   2. Restart terminal")
        print("   3. Run: npm install")
        print("   4. Run: npm run dev")
    elif not Path("node_modules").exists():
        print("   1. Run: npm install")
        print("   2. Run: npm run dev")
        print("   3. Open: http://localhost:3000")
    else:
        print("   1. Run: npm run dev")
        print("   2. Open: http://localhost:3000")
        print("   3. Start developing! 🎉")

if __name__ == "__main__":
    check_environment()
