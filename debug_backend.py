import asyncio
import sys
sys.path.append('backend')

from app.adapters.neo4j_conn import Neo4jConnection
from app.schemas.config import settings

async def debug_backend():
    print("=== Debugging Backend Initialization ===")
    
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
    
    print("=== End Debug ===")

if __name__ == "__main__":
    asyncio.run(debug_backend())
