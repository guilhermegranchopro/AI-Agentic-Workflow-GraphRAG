import asyncio
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.app.adapters.neo4j_conn import Neo4jConnection

async def check_relationships():
    try:
        conn = Neo4jConnection()
        print("✅ Neo4j connection established")
        
        # Check all relationship types
        result = await conn.run_cypher("MATCH ()-[r]->() RETURN DISTINCT type(r), count(r)")
        print("\nRelationship types in Neo4j:")
        for record in result:
            rel_type, count = record["type(r)"], record["count(r)"]
            print(f"  {rel_type}: {count}")
        
        # Check specific CONTRADICTS relationships
        contradicts_result = await conn.run_cypher("MATCH (a)-[r:CONTRADICTS]->(b) RETURN a.title, b.title")
        print(f"\nCONTRADICTS relationships found: {len(contradicts_result)}")
        for record in contradicts_result:
            print(f"  {record['a.title']} CONTRADICTS {record['b.title']}")
        
        # Check RELATES_TO relationships with type property
        relates_result = await conn.run_cypher("MATCH (a)-[r:RELATES_TO]->(b) WHERE r.type = 'CONTRADICTS' RETURN a.title, b.title")
        print(f"\nRELATES_TO relationships with type='CONTRADICTS': {len(relates_result)}")
        for record in relates_result:
            print(f"  {record['a.title']} RELATES_TO {record['b.title']} (type: CONTRADICTS)")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_relationships())
