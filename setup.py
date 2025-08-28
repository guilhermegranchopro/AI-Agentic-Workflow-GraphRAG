#!/usr/bin/env python3
"""
UAE Legal GraphRAG - Setup Script
=================================

This script helps set up the UAE Legal GraphRAG project for first-time users.
It creates the necessary environment, installs dependencies, and prepares the system.

Usage:
    python setup.py
"""

import os
import sys
import subprocess
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
    """Print the setup header."""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("🔧 UAE Legal GraphRAG - Setup Script")
    print("=" * 60)
    print(f"{Colors.ENDC}")

def check_python_version():
    """Check if Python version is compatible."""
    print(f"{Colors.OKCYAN}🐍 Checking Python version...{Colors.ENDC}")
    
    if sys.version_info < (3, 8):
        print(f"{Colors.FAIL}❌ Python 3.8+ is required. Current version: {sys.version}{Colors.ENDC}")
        return False
    
    print(f"{Colors.OKGREEN}✅ Python {sys.version.split()[0]} is compatible{Colors.ENDC}")
    return True

def check_nodejs():
    """Check if Node.js is installed."""
    print(f"{Colors.OKCYAN}📦 Checking Node.js...{Colors.ENDC}")
    
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Colors.OKGREEN}✅ Node.js {result.stdout.strip()} is installed{Colors.ENDC}")
            return True
        else:
            print(f"{Colors.FAIL}❌ Node.js is not installed{Colors.ENDC}")
            return False
    except FileNotFoundError:
        print(f"{Colors.FAIL}❌ Node.js is not installed{Colors.ENDC}")
        print(f"{Colors.WARNING}💡 Please install Node.js from https://nodejs.org/{Colors.ENDC}")
        return False

def create_virtual_environment():
    """Create Python virtual environment."""
    print(f"{Colors.OKCYAN}🔧 Creating virtual environment...{Colors.ENDC}")
    
    venv_path = Path(".venv")
    if venv_path.exists():
        print(f"{Colors.WARNING}⚠️  Virtual environment already exists{Colors.ENDC}")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print(f"{Colors.OKGREEN}✅ Virtual environment created{Colors.ENDC}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}❌ Failed to create virtual environment: {e}{Colors.ENDC}")
        return False

def install_python_dependencies():
    """Install Python dependencies."""
    print(f"{Colors.OKCYAN}📦 Installing Python dependencies...{Colors.ENDC}")
    
    try:
        # Determine the pip command based on OS
        if os.name == 'nt':  # Windows
            pip_cmd = [".venv/Scripts/pip"]
        else:  # Unix/Linux/Mac
            pip_cmd = [".venv/bin/pip"]
        
        # Install requirements
        subprocess.run(pip_cmd + ["install", "-r", "backend/requirements.txt"], check=True)
        print(f"{Colors.OKGREEN}✅ Python dependencies installed{Colors.ENDC}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}❌ Failed to install Python dependencies: {e}{Colors.ENDC}")
        return False

def install_node_dependencies():
    """Install Node.js dependencies."""
    print(f"{Colors.OKCYAN}📦 Installing Node.js dependencies...{Colors.ENDC}")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print(f"{Colors.FAIL}❌ Frontend directory not found{Colors.ENDC}")
        return False
    
    try:
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        print(f"{Colors.OKGREEN}✅ Node.js dependencies installed{Colors.ENDC}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}❌ Failed to install Node.js dependencies: {e}{Colors.ENDC}")
        return False

def create_env_file():
    """Create .env file from template."""
    print(f"{Colors.OKCYAN}⚙️  Creating environment file...{Colors.ENDC}")
    
    env_file = Path(".env")
    if env_file.exists():
        print(f"{Colors.WARNING}⚠️  .env file already exists{Colors.ENDC}")
        return True
    
    # Create basic .env template
    env_content = """# UAE Legal GraphRAG Environment Configuration

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Frontend Configuration
NEXT_PUBLIC_BACKEND_URL=http://localhost:8012

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"{Colors.OKGREEN}✅ .env file created{Colors.ENDC}")
        print(f"{Colors.WARNING}💡 Please edit .env file with your actual configuration{Colors.ENDC}")
        return True
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to create .env file: {e}{Colors.ENDC}")
        return False

def create_directories():
    """Create necessary directories."""
    print(f"{Colors.OKCYAN}📁 Creating directories...{Colors.ENDC}")
    
    directories = [
        "backend/data",
        "backend/logs",
        "docs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print(f"{Colors.OKGREEN}✅ Directories created{Colors.ENDC}")
    return True

def main():
    """Main setup function."""
    print_header()
    
    print(f"{Colors.OKCYAN}🚀 Starting setup process...{Colors.ENDC}")
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_nodejs():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_python_dependencies():
        sys.exit(1)
    
    if not install_node_dependencies():
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Setup Complete!{Colors.ENDC}")
    print(f"\n{Colors.OKBLUE}📋 Next Steps:{Colors.ENDC}")
    print(f"1. Edit the .env file with your configuration")
    print(f"2. Start Neo4j database (if using real data)")
    print(f"3. Run: python start.py")
    print(f"\n{Colors.OKCYAN}📚 For more information, see README.md{Colors.ENDC}")

if __name__ == "__main__":
    main()
