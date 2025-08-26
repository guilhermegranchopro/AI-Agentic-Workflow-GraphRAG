#!/usr/bin/env python3
"""Test script to debug backend startup issues."""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_startup():
    """Test the backend startup process."""
    try:
        print("Testing backend import...")
        from app.main import app
        print("✅ Backend import successful")
        
        print("Testing FastAPI app creation...")
        print(f"App title: {app.title}")
        print(f"App version: {app.version}")
        print("✅ FastAPI app created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_startup())
    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Tests failed!")
        sys.exit(1)
