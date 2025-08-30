import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.adapters.neo4j_conn import Neo4jConnection
from app.schemas.config import settings

async def test_backend_neo4j():
    print("=== Testing Backend Neo4j Connection ===")
    
    # Test settings
    print(f"Settings loaded: {settings.neo4j_uri}, {settings.neo4j_username}, {settings.neo4j_password is not None}")
    
    # Test Neo4j connection
    conn = Neo4jConnection()
    print(f"Neo4jConnection driver: {conn.driver is not None}")
    
    if conn.driver:
        # Test health check
        health = await conn.health_check()
        print(f"Health check result: {health}")
        
        # Test connectivity
        is_connected = await conn.verify_connectivity()
        print(f"Connectivity test: {is_connected}")
        
        if is_connected:
            # Test a query
            result = await conn.run_cypher("MATCH (n) RETURN count(n) as count")
            print(f"Query result: {result}")
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_backend_neo4j())
