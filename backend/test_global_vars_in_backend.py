import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.main import lifespan
from app.api import routes

async def test_global_vars_in_backend():
    print("=== Testing Global Variables in Backend ===")
    
    # Check initial state
    print(f"Initial neo4j_conn: {routes.neo4j_conn}")
    print(f"Initial azure_llm: {routes.azure_llm}")
    
    # Simulate the lifespan function
    async with lifespan(None):
        print(f"During lifespan - neo4j_conn: {routes.neo4j_conn}")
        print(f"During lifespan - azure_llm: {routes.azure_llm}")
        
        # Test the get_services function
        services = routes.get_services()
        print(f"Services from get_services: {services}")
        
        if services["neo4j_conn"]:
            print("Neo4j connection is available")
            # Test a simple query
            try:
                result = await services["neo4j_conn"].run_cypher("MATCH (n) RETURN count(n) as count")
                print(f"Neo4j query result: {result}")
            except Exception as e:
                print(f"Neo4j query error: {e}")
        else:
            print("Neo4j connection is NOT available")
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_global_vars_in_backend())
