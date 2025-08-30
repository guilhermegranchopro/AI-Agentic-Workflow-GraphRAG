#!/usr/bin/env python3
"""
UAE Legal GraphRAG - Final Presentation Startup Script
=====================================================

This script starts all components for the final presentation:
1. Backend API (FastAPI + GraphRAG)
2. Frontend (Next.js)
3. Health checks and verification

Usage:
    python start_presentation.py
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

def print_status(message, status="INFO"):
    """Print a formatted status message."""
    print(f"[{status}] {message}")

def check_service(url, name, timeout=10):
    """Check if a service is running."""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print_status(f"✅ {name} is running at {url}", "SUCCESS")
            return True
        else:
            print_status(f"❌ {name} returned status {response.status_code}", "ERROR")
            return False
    except requests.exceptions.RequestException as e:
        print_status(f"❌ {name} is not accessible: {e}", "ERROR")
        return False

def start_backend():
    """Start the backend API server."""
    print_status("Starting Backend API Server...", "INFO")
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print_status("Backend directory not found!", "ERROR")
        return False
    
    # Start backend in background
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8012"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for backend to start
        time.sleep(10)
        
        # Check if backend is running
        if check_service("http://localhost:8012/health", "Backend API"):
            return True
        else:
            print_status("Backend failed to start properly", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Failed to start backend: {e}", "ERROR")
        return False

def start_frontend():
    """Start the frontend Next.js server."""
    print_status("Starting Frontend (Next.js)...", "INFO")
    
    # Change to frontend directory
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print_status("Frontend directory not found!", "ERROR")
        return False
    
    # Start frontend in background
    try:
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for frontend to start
        time.sleep(15)
        
        # Check if frontend is running
        if check_service("http://localhost:3000", "Frontend"):
            return True
        else:
            print_status("Frontend failed to start properly", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Failed to start frontend: {e}", "ERROR")
        return False

def main():
    """Main startup function."""
    print("=" * 60)
    print("UAE Legal GraphRAG - Final Presentation Startup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path(".env").exists():
        print_status("Please run this script from the project root directory", "ERROR")
        return
    
    print_status("Starting UAE Legal GraphRAG System...", "INFO")
    
    # Start backend
    backend_ok = start_backend()
    
    # Start frontend
    frontend_ok = start_frontend()
    
    # Final status
    print("\n" + "=" * 60)
    print("STARTUP COMPLETE")
    print("=" * 60)
    
    if backend_ok and frontend_ok:
        print_status("🎉 All services started successfully!", "SUCCESS")
        print("\nAccess the application at:")
        print("  🌐 Frontend: http://localhost:3000")
        print("  🔧 Backend API: http://localhost:8012")
        print("  📚 API Docs: http://localhost:8012/docs")
        print("\nFeatures available:")
        print("  📊 Graph Visualization")
        print("  🤖 AI Assistant")
        print("  🔍 AI Analysis")
        print("  📈 Knowledge Graph Explorer")
    else:
        print_status("❌ Some services failed to start", "ERROR")
        if not backend_ok:
            print_status("Backend API is not running", "ERROR")
        if not frontend_ok:
            print_status("Frontend is not running", "ERROR")
    
    print("\nPress Ctrl+C to stop all services")

if __name__ == "__main__":
    try:
        main()
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print_status("Shutting down services...", "INFO")
        print_status("Presentation startup script stopped", "INFO")
