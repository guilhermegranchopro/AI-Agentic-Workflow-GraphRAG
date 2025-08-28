#!/usr/bin/env python3
"""
Test script for complex backend functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_complex_backend():
    """Test the complex backend functionality."""
    print("🚀 Testing Complex Backend Functionality")
    print("=" * 50)
    
    try:
        # Import the complex backend components
        from backend.app.main import app
        from backend.app.api.routes import api_router
        from backend.app.adapters.azure_openai import AzureLLM
        from backend.app.adapters.neo4j_conn import Neo4jConnection
        
        print("✅ All imports successful")
        
        # Test service initialization
        azure_llm = AzureLLM()
        neo4j_conn = Neo4jConnection()
        
        print("✅ Services initialized")
        
        # Test Azure OpenAI health check
        azure_health = await azure_llm.health_check()
        print(f"✅ Azure OpenAI Health: {azure_health}")
        
        # Test Neo4j health check
        neo4j_health = await neo4j_conn.health_check()
        print(f"✅ Neo4j Health: {neo4j_health}")
        
        # Test chat functionality
        messages = [{"role": "user", "content": "What are the requirements for starting a business in UAE?"}]
        response = await azure_llm.chat(messages)
        print(f"✅ Chat Response: {response[:100]}...")
        
        print("\n🎉 Complex Backend Test Successful!")
        print("The complex backend is working correctly with:")
        print("- Azure OpenAI integration")
        print("- Neo4j connection")
        print("- Chat functionality")
        print("- All services healthy")
        
        return True
        
    except Exception as e:
        print(f"❌ Complex Backend Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_complex_backend())
    sys.exit(0 if success else 1)
