import asyncio
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.app.adapters.neo4j_conn import Neo4jConnection

async def check_relationship_properties():
    try:
        conn = Neo4jConnection()
        print("✅ Neo4j connection established")
        
        # Check RELATES_TO relationships with type property
        result = await conn.run_cypher("MATCH (a)-[r:RELATES_TO]->(b) WHERE r.type = 'CONTRADICTS' RETURN a, r, b LIMIT 3")
        print(f"\nFound {len(result)} RELATES_TO relationships with type='CONTRADICTS'")
        
        for i, record in enumerate(result):
            print(f"\nRecord {i+1}:")
            print(f"  a: {type(record['a'])} - {record['a']}")
            print(f"  r: {type(record['r'])} - {record['r']}")
            print(f"  b: {type(record['b'])} - {record['b']}")
            
            # Check if r is a tuple
            if isinstance(record['r'], tuple):
                print(f"  r is tuple with {len(record['r'])} elements:")
                for j, elem in enumerate(record['r']):
                    print(f"    r[{j}]: {type(elem)} - {elem}")
            else:
                print(f"  r properties: {dir(record['r'])}")
                if hasattr(record['r'], 'type'):
                    print(f"  r.type: {record['r'].type}")
                if hasattr(record['r'], 'get'):
                    print(f"  r.get('type'): {record['r'].get('type')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_relationship_properties())
