#!/usr/bin/env python3
"""
UAE Legal GraphRAG - Unified Startup Script
===========================================

This script provides a simple way to start the complex Python backend and frontend.
When the frontend is running but the backend is not available, the app automatically
reverts to mock data/responses.

Usage:
    python start.py                    # Start both backend and frontend
    python start.py --backend-only     # Start only the backend
    python start.py --frontend-only    # Start only the frontend
    python start.py --help             # Show help
"""

import os
import sys
import time
import signal
import subprocess
import argparse
import requests
from pathlib import Path
from typing import Optional, List

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
    UNDERLINE = '\033[4m'

def print_header():
    """Print the application header."""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("🚀 UAE Legal GraphRAG - Unified Startup Script")
    print("=" * 60)
    print(f"{Colors.ENDC}")

def check_environment():
    """Check if the environment is properly set up."""
    print(f"{Colors.OKCYAN}🔍 Checking environment...{Colors.ENDC}")
    
    # Check if .env file exists
    if not Path(".env").exists():
        print(f"{Colors.FAIL}❌ .env file not found!{Colors.ENDC}")
        print(f"{Colors.WARNING}💡 Please create a .env file with your configuration.{Colors.ENDC}")
        return False
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"{Colors.WARNING}⚠️  Virtual environment not detected{Colors.ENDC}")
        print(f"{Colors.OKCYAN}💡 Activating virtual environment...{Colors.ENDC}")
        
        # Try to activate virtual environment
        venv_script = Path(".venv/Scripts/Activate.ps1")
        if venv_script.exists():
            print(f"{Colors.OKGREEN}✅ Virtual environment found at .venv{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}❌ Virtual environment not found at .venv{Colors.ENDC}")
            print(f"{Colors.WARNING}💡 Please create a virtual environment: python -m venv .venv{Colors.ENDC}")
            return False
    
    print(f"{Colors.OKGREEN}✅ Environment check passed{Colors.ENDC}")
    return True

def check_backend_health(url: str = "http://localhost:8012") -> bool:
    """Check if the backend is healthy."""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend() -> Optional[subprocess.Popen]:
    """Start the complex Python backend."""
    print(f"{Colors.OKCYAN}🚀 Starting complex Python backend...{Colors.ENDC}")
    
    # Check if backend is already running
    if check_backend_health():
        print(f"{Colors.OKGREEN}✅ Backend is already running{Colors.ENDC}")
        return None
    
    try:
        # Start the backend using uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "backend.app.main:app",
            "--host", "0.0.0.0",
            "--port", "8012",
            "--reload"
        ]
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if the backend started successfully
        if check_backend_health():
            print(f"{Colors.OKGREEN}✅ Backend started successfully{Colors.ENDC}")
            print(f"{Colors.OKBLUE}🌐 Backend URL: http://localhost:8012{Colors.ENDC}")
            print(f"{Colors.OKBLUE}📊 Health check: http://localhost:8012/health{Colors.ENDC}")
            return process
        else:
            print(f"{Colors.FAIL}❌ Backend failed to start{Colors.ENDC}")
            process.terminate()
            return None
            
    except Exception as e:
        print(f"{Colors.FAIL}❌ Error starting backend: {e}{Colors.ENDC}")
        return None

def start_frontend() -> Optional[subprocess.Popen]:
    """Start the Next.js frontend."""
    print(f"{Colors.OKCYAN}🚀 Starting Next.js frontend...{Colors.ENDC}")
    
    # Check if frontend is already running
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print(f"{Colors.OKGREEN}✅ Frontend is already running{Colors.ENDC}")
            return None
    except:
        pass
    
    try:
        # Change to frontend directory
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            print(f"{Colors.FAIL}❌ Frontend directory not found{Colors.ENDC}")
            return None
        
        # Check if node_modules exists
        if not (frontend_dir / "node_modules").exists():
            print(f"{Colors.WARNING}⚠️  Installing frontend dependencies...{Colors.ENDC}")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # Start the frontend
        cmd = ["npm", "run", "dev"]
        process = subprocess.Popen(
            cmd,
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Wait a moment for the server to start
        time.sleep(5)
        
        # Check if the frontend started successfully
        try:
            response = requests.get("http://localhost:3000", timeout=10)
            if response.status_code == 200:
                print(f"{Colors.OKGREEN}✅ Frontend started successfully{Colors.ENDC}")
                print(f"{Colors.OKBLUE}🌐 Frontend URL: http://localhost:3000{Colors.ENDC}")
                return process
            else:
                print(f"{Colors.FAIL}❌ Frontend failed to start{Colors.ENDC}")
                process.terminate()
                return None
        except:
            print(f"{Colors.FAIL}❌ Frontend failed to start{Colors.ENDC}")
            process.terminate()
            return None
            
    except Exception as e:
        print(f"{Colors.FAIL}❌ Error starting frontend: {e}{Colors.ENDC}")
        return None

def stop_processes(processes: List[subprocess.Popen]):
    """Stop all running processes."""
    print(f"{Colors.WARNING}🛑 Stopping processes...{Colors.ENDC}")
    for process in processes:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

def signal_handler(signum, frame):
    """Handle interrupt signals."""
    print(f"\n{Colors.WARNING}🛑 Received interrupt signal. Stopping all processes...{Colors.ENDC}")
    stop_processes(backend_processes + frontend_processes)
    sys.exit(0)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="UAE Legal GraphRAG Startup Script")
    parser.add_argument("--backend-only", action="store_true", help="Start only the backend")
    parser.add_argument("--frontend-only", action="store_true", help="Start only the frontend")
    parser.add_argument("--no-backend", action="store_true", help="Start frontend without backend")
    
    args = parser.parse_args()
    
    print_header()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    global backend_processes, frontend_processes
    backend_processes = []
    frontend_processes = []
    
    try:
        # Start backend if requested
        if not args.frontend_only:
            backend_process = start_backend()
            if backend_process:
                backend_processes.append(backend_process)
        
        # Start frontend if requested
        if not args.backend_only:
            frontend_process = start_frontend()
            if frontend_process:
                frontend_processes.append(frontend_process)
        
        # Show status
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Startup Complete!{Colors.ENDC}")
        print(f"{Colors.OKBLUE}📊 Backend Status: {'✅ Running' if check_backend_health() else '❌ Not Available'}{Colors.ENDC}")
        print(f"{Colors.OKBLUE}🌐 Frontend Status: {'✅ Running' if frontend_processes else '❌ Not Available'}{Colors.ENDC}")
        
        if not args.no_backend and not check_backend_health():
            print(f"\n{Colors.WARNING}⚠️  Backend is not available. Frontend will use mock data.{Colors.ENDC}")
        
        print(f"\n{Colors.OKCYAN}📋 Press Ctrl+C to stop all services{Colors.ENDC}")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}🛑 Received interrupt signal. Stopping all processes...{Colors.ENDC}")
    finally:
        stop_processes(backend_processes + frontend_processes)
        print(f"{Colors.OKGREEN}✅ All processes stopped{Colors.ENDC}")

if __name__ == "__main__":
    main()
