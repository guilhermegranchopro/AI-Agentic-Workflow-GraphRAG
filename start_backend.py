#!/usr/bin/env python3
"""
UAE Legal GraphRAG - Backend Startup Script
Starts the complex Python backend with proper error handling.
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def print_banner():
    """Print startup banner."""
    print("=" * 60)
    print("🚀 UAE Legal GraphRAG - Complex Backend Startup")
    print("=" * 60)
    print("🎯 Starting complex Python backend with full GraphRAG capabilities")
    print("📊 Services: Azure OpenAI, Neo4j, FAISS, A2A Protocol")
    print("🔧 Port: 8012")
    print("=" * 60)

def check_environment():
    """Check if environment is properly set up."""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found in project root")
        return False
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not detected")
        print("💡 Please activate the virtual environment first:")
        print("   .\\.venv\\Scripts\\activate")
        return False
    
    print("✅ Environment check passed")
    return True

def start_backend():
    """Start the complex backend."""
    print("\n🚀 Starting complex backend...")
    
    try:
        # Start uvicorn with the complex backend
        cmd = [
            sys.executable, "-m", "uvicorn",
            "backend.app.main:app",
            "--host", "0.0.0.0",
            "--port", "8012",
            "--reload"
        ]
        
        print(f"📝 Command: {' '.join(cmd)}")
        print("⏳ Starting server...")
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print("✅ Backend process started")
        print("🌐 Server will be available at: http://localhost:8012")
        print("📊 Health check: http://localhost:8012/health")
        print("\n📋 Press Ctrl+C to stop the server")
        
        # Monitor the process
        try:
            for line in process.stdout:
                print(line.rstrip())
        except KeyboardInterrupt:
            print("\n🛑 Stopping backend...")
            process.terminate()
            process.wait()
            print("✅ Backend stopped")
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    return True

def main():
    """Main function."""
    print_banner()
    
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above.")
        sys.exit(1)
    
    if not start_backend():
        print("❌ Failed to start backend.")
        sys.exit(1)

if __name__ == "__main__":
    main()
