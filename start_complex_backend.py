#!/usr/bin/env python3
"""
Startup script for UAE Legal GraphRAG Complex Backend
"""

import os
import sys
import asyncio
import signal
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    print("\n🛑 Received shutdown signal. Stopping backend...")
    sys.exit(0)

async def test_backend_functionality():
    """Test the backend functionality."""
    print("🔍 Testing backend functionality...")
    
    try:
        # Import and test the complex backend components
        from backend.app.adapters.azure_openai import AzureLLM
        from backend.app.adapters.neo4j_conn import Neo4jConnection
        
        # Test Azure OpenAI
        azure_llm = AzureLLM()
        azure_health = await azure_llm.health_check()
        print(f"✅ Azure OpenAI: {azure_health.get('status', 'unknown')}")
        
        # Test Neo4j
        neo4j_conn = Neo4jConnection()
        neo4j_health = await neo4j_conn.health_check()
        print(f"✅ Neo4j: {neo4j_health.get('status', 'unknown')}")
        
        # Test chat functionality
        messages = [{"role": "user", "content": "What are the requirements for starting a business in UAE?"}]
        response = await azure_llm.chat(messages)
        print(f"✅ Chat Response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend functionality test failed: {e}")
        return False

def start_backend():
    """Start the complex backend."""
    print("🚀 Starting UAE Legal GraphRAG Complex Backend")
    print("=" * 60)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Test backend functionality first
        if not asyncio.run(test_backend_functionality()):
            print("❌ Backend functionality test failed. Exiting.")
            return False
        
        print("\n✅ Backend functionality test passed!")
        print("🎯 Starting FastAPI server...")
        
        # Import and start the FastAPI app
        from backend.app.main import app
        import uvicorn
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8012,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
        return True
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = start_backend()
    sys.exit(0 if success else 1)
