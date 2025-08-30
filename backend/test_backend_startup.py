import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.main import lifespan
from app.api import routes

async def test_backend_startup():
    print("=== Testing Backend Startup ===")
    
    # Check initial state
    print(f"Initial neo4j_conn: {routes.neo4j_conn}")
    print(f"Initial azure_llm: {routes.azure_llm}")
    
    # Simulate the lifespan function
    async with lifespan(None):
        print(f"During lifespan - neo4j_conn: {routes.neo4j_conn}")
        print(f"During lifespan - azure_llm: {routes.azure_llm}")
        
        if routes.neo4j_conn:
            # Test Neo4j connection
            health = await routes.neo4j_conn.health_check()
            print(f"Neo4j health: {health}")
        
        if routes.azure_llm:
            # Test Azure OpenAI connection
            health = await routes.azure_llm.health_check()
            print(f"Azure health: {health}")
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_backend_startup())
