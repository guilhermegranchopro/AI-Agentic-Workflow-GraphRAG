#!/usr/bin/env python3
"""Test Neo4j connectivity and display configuration."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
from neo4j import GraphDatabase

def test_connectivity():
    # Load environment variables
    load_dotenv()
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # Display config (masked)
    print("=== Configuration ===")
    print(f"NEO4J_URI: {uri[:25]}...{uri[-10:] if uri and len(uri) > 35 else uri}")
    print(f"NEO4J_DATABASE: {database}")
    print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT', 'NOT_SET')[:30]}...")
    print(f"AZURE_OPENAI_EMBEDDING_DEPLOYMENT: {os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT', 'NOT_SET')}")
    print(f"EMBEDDING_DIM: {os.getenv('EMBEDDING_DIM', 'NOT_SET')}")
    print()
    
    if not all([uri, user, password]):
        print("❌ Missing Neo4j credentials in .env file!")
        print("Required format: neo4j+s://<DBID>.databases.neo4j.io")
        return False
    
    print("=== Testing Neo4j Connection ===")
    try:
        # For bolt+s:// URIs, encryption is automatically enabled
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print("✅ Neo4j connectivity verified!")
        
        # Test database access
        with driver.session(database=database) as session:
            result = session.run("SHOW DATABASES")
            databases = [record["name"] for record in result]
            print(f"✅ Available databases: {databases}")
            
            # Test basic query
            result = session.run("RETURN 'Hello Neo4j' AS message")
            message = result.single()["message"]
            print(f"✅ Test query result: {message}")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nPlease check:")
        print("1. Neo4j Aura instance is running")
        print("2. URI format: neo4j+s://<DBID>.databases.neo4j.io")
        print("3. Username/password are correct")
        print("4. Firewall allows connections")
        return False

if __name__ == "__main__":
    success = test_connectivity()
    sys.exit(0 if success else 1)
