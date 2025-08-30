import asyncio
import sys
sys.path.append('backend')

from app.adapters.neo4j_conn import Neo4jConnection

async def test_neo4j():
    print("=== Testing Neo4j Connection ===")
    
    # Create connection
    conn = Neo4jConnection()
    print(f"Driver initialized: {conn.driver is not None}")
    
    if conn.driver:
        # Test connectivity
        try:
            is_connected = await conn.verify_connectivity()
            print(f"Connectivity test: {is_connected}")
            
            if is_connected:
                # Test a simple query
                result = await conn.run_cypher("MATCH (n) RETURN count(n) as count")
                print(f"Node count: {result[0]['count'] if result else 'No result'}")
                
                # Get graph stats
                stats = await conn.get_graph_stats()
                print(f"Graph stats: {stats}")
            else:
                print("Failed to connect to Neo4j")
                
        except Exception as e:
            print(f"Error testing Neo4j: {e}")
    else:
        print("Neo4j driver not initialized")

if __name__ == "__main__":
    asyncio.run(test_neo4j())
