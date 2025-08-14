#!/usr/bin/env python3
"""
Alternative connectivity test with SSL verification disabled.
Note: This is for demonstration only. In production, use proper SSL certificates.
"""

import os
import sys
import ssl
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
from neo4j import GraphDatabase

def test_connectivity_insecure():
    """Test connectivity with SSL verification disabled (demo only)."""
    load_dotenv()
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
    print("⚠️  WARNING: Testing with SSL verification DISABLED")
    print("⚠️  This is for demonstration only!")
    print()
    
    try:
        # Create an SSL context that doesn't verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Use regular bolt:// URI with custom SSL context
        plain_uri = uri.replace("bolt+s://", "bolt://")
        
        driver = GraphDatabase.driver(
            plain_uri, 
            auth=(user, password),
            encrypted=True,
            ssl_context=ssl_context
        )
        
        driver.verify_connectivity()
        print("✅ Neo4j connectivity verified (insecure mode)!")
        
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
        print(f"❌ Connection still failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connectivity_insecure()
    sys.exit(0 if success else 1)
