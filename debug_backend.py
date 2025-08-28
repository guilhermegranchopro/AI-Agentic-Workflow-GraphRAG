#!/usr/bin/env python3
"""
Debug script for UAE Legal GraphRAG backend
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all imports."""
    print("🔍 Testing imports...")
    
    try:
        from backend.app.main import app
        print("✅ Main app import successful")
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        return False
    
    try:
        from backend.app.schemas.config import settings
        print("✅ Settings import successful")
        print(f"   Backend URL: {getattr(settings, 'backend_url', 'Not set')}")
        print(f"   Port: {getattr(settings, 'port', 'Not set')}")
    except Exception as e:
        print(f"❌ Settings import failed: {e}")
        return False
    
    try:
        from backend.app.adapters.azure_openai import AzureLLM
        print("✅ Azure OpenAI adapter import successful")
    except Exception as e:
        print(f"❌ Azure OpenAI adapter import failed: {e}")
        return False
    
    try:
        from backend.app.adapters.neo4j_conn import Neo4jConnection
        print("✅ Neo4j adapter import successful")
    except Exception as e:
        print(f"❌ Neo4j adapter import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables."""
    print("\n🔍 Testing environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Load and check key variables
        from dotenv import load_dotenv
        load_dotenv()
        
        key_vars = [
            'AZURE_OPENAI_API_KEY',
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_DEPLOYMENT',
            'NEO4J_URI',
            'NEO4J_USERNAME',
            'NEO4J_PASSWORD'
        ]
        
        for var in key_vars:
            value = os.getenv(var)
            if value:
                print(f"✅ {var}: {'*' * len(value)} (configured)")
            else:
                print(f"⚠️  {var}: Not configured")
    else:
        print("❌ .env file not found")
        return False
    
    return True

def test_services():
    """Test service initialization."""
    print("\n🔍 Testing service initialization...")
    
    try:
        from backend.app.adapters.azure_openai import AzureLLM
        azure_llm = AzureLLM()
        print("✅ Azure LLM initialized")
        
        health = azure_llm.health_check()
        print(f"   Health: {health}")
        
    except Exception as e:
        print(f"❌ Azure LLM initialization failed: {e}")
    
    try:
        from backend.app.adapters.neo4j_conn import Neo4jConnection
        neo4j_conn = Neo4jConnection()
        print("✅ Neo4j connection initialized")
        
        health = neo4j_conn.health_check()
        print(f"   Health: {health}")
        
    except Exception as e:
        print(f"❌ Neo4j initialization failed: {e}")

def main():
    """Main debug function."""
    print("🚀 UAE Legal GraphRAG - Backend Debug")
    print("=" * 50)
    
    if not test_imports():
        print("\n❌ Import tests failed")
        return
    
    if not test_environment():
        print("\n❌ Environment tests failed")
        return
    
    test_services()
    
    print("\n✅ Debug complete!")

if __name__ == "__main__":
    main()
